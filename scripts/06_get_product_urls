import json

# List of JSON files
files = [
    "view_product_detail.json",
    "select_product_option.json",
    "select_product_option_quality.json",
    "add_to_cart_action.json",
    "product_detail_recommendation_visible.json",
    "product_detail_recommendation_noticed.json",
    "product_view_all_recommend_clicked.json"
]

total_rows = 0
product_map = {}

for filename in files:
    try:
        with open(filename, "r", encoding="utf-8") as f:
            docs = json.load(f)
            total_rows += len(docs)

            for doc in docs:
                if filename != "product_view_all_recommend_clicked.json":
                    pid = doc.get("product_id")
                    url = doc.get("current_url")
                else:
                    pid = doc.get("product_id")
                    url = doc.get("referrer_url")

                if pid and url:
                    # Deduplicate by product_id, collect unique URLs in a set
                    if pid not in product_map:
                        product_map[pid] = set()
                    product_map[pid].add(url)

        print(f"Read {len(docs)} rows from {filename}")
    except Exception as e:
        print(f"Error reading {filename}: {e}")

# Convert sets to lists for JSON serialization
unique_results = [{"product_id": pid, "url": list(urls)} for pid, urls in product_map.items()]

# Save distinct product_id → unique url array mapping
output_file = "list_products_with_urls.json"
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(unique_results, f, ensure_ascii=False, indent=4)

print("\nSummary:")
print(f"Total rows read: {total_rows}")
print(f"Distinct product IDs: {len(unique_results)}")
print(f"Saved to {output_file}")
