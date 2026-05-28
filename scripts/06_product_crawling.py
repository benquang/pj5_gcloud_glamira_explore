import asyncio
import time
import os
import glob
import aiohttp  
from urllib.parse import urlparse, parse_qs
import json
import re
from bs4 import BeautifulSoup


CRAWLER_BATCH_SIZE = 100
PID_FILTER_DIR = ""
PRODUCT_INFO_DIR = "\product_info"
CRAWLER_SEMAPHORE = 5
CRAWLER_TIMEOUT = 20
CRAWLER_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

CRAWLER_MAX_RETRIES = 3

CRAWLER_UA = "glamira-crawler/1.0"

def get_product_list_from_filter():
    with open("list_products_with_urls.json", "r") as file:
        products = json.load(file)

    return products

def _get_ordered_urls(urls):
    valid_urls = []
    for u in urls:
        if not isinstance(u, str):
            continue
        parsed = urlparse(u)
        if parsed.scheme in ("http", "https"):
            valid_urls.append(u)

    def _score(url):
        parsed = urlparse(url)
        num_params = len(parse_qs(parsed.query))
        is_stage = 1 if "stage." in parsed.netloc else 0
        return (is_stage, num_params, len(url))

    return sorted(valid_urls, key=_score)



def extract_product_data(html: str) -> dict:
    soup = BeautifulSoup(html, "html.parser")

    # Tìm tất cả script type="text/javascript"
    scripts = soup.find_all("script", type="text/javascript")

    for script in scripts:
        if not script.string:
            continue

        # Regex tìm đoạn var react_data = {...}
        match = re.search(r'var\s+react_data\s*=\s*(\{.*?\});', script.string, re.DOTALL)
        if match:
            json_str = match.group(1)
            data = json.loads(json_str)

            # Chỉ lấy các trường cần thiết
            product_data = {
                "product_id": data.get("product_id"),
                "product_name": data.get("name"),
                "product_sku": data.get("sku"),
                "product_type_id": data.get("type_id"),
                "price": data.get("price"),
                "min_price": data.get("min_price"),
                "max_price": data.get("max_price"),
                "qty": data.get("qty"),
                "collection": data.get("collection"),
                "collection_id": data.get("collection_id"),
                "product_type": data.get("product_type"),
                "product_type_value": data.get("product_type_value"),
                "category": data.get("category"),
                "category_name": data.get("category_name"),
            }
            return product_data

    return {}

async def get_product_info(session, product, initialized_domains, failed_domains, semaphore):
    pid = str(product["product_id"])
    candidate_urls = _get_ordered_urls(product["url"])[:10]

    #print(candidate_urls)

    if not candidate_urls:
        return "invalid_url", {"pid": pid, "url": None, "all_urls": product.get("urls", [])}

    last_status = "failed"
    last_url_tried = None

    for url in candidate_urls:
        last_url_tried = url
        headers = CRAWLER_HEADERS.copy()
        headers["User-Agent"] = CRAWLER_UA
        domain = urlparse(url).netloc
        headers["Referer"] = f"https://{domain}/"

        # Bỏ qua nếu domain này đã từng lỗi (rác)
        if domain in failed_domains:
            continue

        if domain not in initialized_domains:
            initialized_domains.add(domain)
            try:
                # Chỉ lock semaphore khi thực sự cần gọi network
                async with semaphore:
                    async with session.get(
                        f"https://{domain}/", headers=headers, allow_redirects=True, timeout=10
                    ) as home_resp:
                        await home_resp.text()
                        #logger.info(f"Initialized session for domain: {domain}")
            except Exception as e:
                #logger.warning(f"Failed to initialize domain {domain}: {e}")
                initialized_domains.discard(domain)
                if any(x in domain for x in ["dev", "test", "stage"]):
                    failed_domains.add(domain)
                continue

        for retry in range(1, CRAWLER_MAX_RETRIES + 1):
            try:
                async with semaphore:
                    async with session.get(url, headers=headers, allow_redirects=True) as response:
                        if response.status == 200:
                            html = await response.text()
                            #print(html)
                            product_data = extract_product_data(html)

                            if product_data:
                                print("OK 200)))")
                            #    #logger.info(f"SUCCESS | ID: {pid} | URL: {url}")
                                return "success", product_data
                            
                            #print("OK 200)))")

                            status = "no_json_ld"
                            break  # Thử URL khác

                        status = response.status
                        if status == 403:
                            print("403 ne")
                            await asyncio.sleep(1 * retry)
                            break

                        if status >= 500 or status == 429:
                            print("loi khac")
                            await asyncio.sleep(1 * retry)
                        else:
                            break

            except asyncio.TimeoutError:
                status = "TimeoutError"
                await asyncio.sleep(0.5 * retry)
            except Exception as e:
                status = type(e).__name__
                break

        last_status = status

    return last_status, {"pid": pid, "url": last_url_tried, "all_urls": product.get("url", [])}

def save_success_data_to_files(file_idx, success_products):
    """
    Lưu danh sách sản phẩm thành file JSON.
    
    Parameters:
        file_idx (int): chỉ số file (ví dụ 1, 2, 3...)
        success_products (list[dict]): danh sách object sản phẩm
    """
    # Tạo tên file theo chỉ số
    filename = f"2405_Success_products_{file_idx}.json"
    
    # Đảm bảo thư mục tồn tại
    os.makedirs("output", exist_ok=True)
    filepath = os.path.join("output", filename)

    # Ghi dữ liệu ra file JSON
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(success_products, f, ensure_ascii=False, indent=4)

    print(f"✅ Đã lưu {len(success_products)} sản phẩm vào {filepath}")

import nest_asyncio
nest_asyncio.apply()

async def _crawl_products_async(batch_size):
    """Hàm chính thực hiện crawl theo lô (batch) tương tự project Tiki, hỗ trợ checkpoint."""
    start_time = time.perf_counter()

    products = get_product_list_from_filter()
    if not products:
        print("not products")
        return

    success_products = []
    success_cnt = 0
    error_cnt = 0
    exception_cnt = 0
    file_idx = 1

    
    
    # Checkpoint setup
    #checkpoint_manager = get_checkpoint_manager("product_crawler")
    #checkpoint = checkpoint_manager.get_checkpoint()
    #start_index = int(checkpoint) if checkpoint else 0
    start_index = 0

    os.makedirs(PRODUCT_INFO_DIR, exist_ok=True)
    #logger.info(f"JOB START | CRAWLING {len(products)} products from Glamira PID Filter")

    

    semaphore = asyncio.Semaphore(CRAWLER_SEMAPHORE)
    connector = aiohttp.TCPConnector(limit_per_host=CRAWLER_SEMAPHORE)
    timeout = aiohttp.ClientTimeout(total=CRAWLER_TIMEOUT)

    

    async with aiohttp.ClientSession(timeout=timeout, connector=connector) as session:
        initialized_domains = set()
        failed_domains = set()
        

        for i in range(0, len(products), batch_size):
            
            batch = products[i : i + batch_size]
            tasks = [
                get_product_info(session, p, initialized_domains, failed_domains, semaphore)
                for p in batch
            ]

            for task in asyncio.as_completed(tasks):
                status, result = await task

                if status == "success":
                    success_products.append(result)
                    success_cnt += 1
                    if len(success_products) >= batch_size:
                        save_success_data_to_files(file_idx, success_products)
                        success_products.clear()
                        file_idx += 1
                elif isinstance(status, int):  # HTTP status code for error
                    #save_error_data_to_files(status, result, logger)  # result here is pid
                    error_cnt += 1
                else:  # Exception status (string)
                    #save_exception_data_to_files(status, result, logger)  # result here is pid
                    exception_cnt += 1
            
            # Cập nhật checkpoint sau mỗi batch hoàn tất
            #checkpoint_manager.save_checkpoint(min(i + batch_size, len(products)))

    # Lưu phần còn lại sau khi hết vòng lặp
    #if success_products:
        #save_success_data_to_files(file_idx, success_products, logger)

    total_time = time.perf_counter() - start_time
    total_failed_products = error_cnt + exception_cnt
    #logger.info(
    #    f"JOB END | SUCCESS: {success_cnt} | FAILED: {total_failed_products} "
    #    f"| ERROR: {error_cnt} | EXCEPTION: {exception_cnt} "
    #    f"| TIME: {format_duration(total_time)}"
    #)


def run_product_crawler(batch_size=CRAWLER_BATCH_SIZE):
    """Chạy crawler (đồng bộ) thông qua asyncio.run()."""
    asyncio.run(_crawl_products_async(batch_size))

if __name__ == "__main__":
    run_product_crawler()
