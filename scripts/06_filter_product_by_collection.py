import json
from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["glamira"]
collection = db["summary"]

# Targets where we want product_id/viewing_product_id + current_url
targets_main = [
    "view_product_detail",
    "select_product_option",
    "select_product_option_quality",
    "add_to_cart_action",
    "product_detail_recommendation_visible",
    "product_detail_recommendation_noticed"
]

# Special case: product_view_all_recommend_clicked
target_special = "product_view_all_recommend_clicked"

# Process main targets
for target in targets_main:
    cursor = collection.find({"collection": target})
    docs = []
    for doc in cursor:
        # Convert ObjectId to string
        doc["_id"] = str(doc["_id"])
        # Choose product_id or viewing_product_id
        pid = doc.get("product_id") or doc.get("viewing_product_id")
        docs.append({
            "product_id": pid,
            "current_url": doc.get("current_url")
        })
    filename = f"{target}.json"
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(docs, f, ensure_ascii=False, indent=4)
    print(f"Saved {len(docs)} docs to {filename}")

# Process special case
cursor = collection.find({"collection": target_special})
docs = []
for doc in cursor:
    doc["_id"] = str(doc["_id"])
    docs.append({
        "product_id": doc.get("viewing_product_id"),
        "referrer_url": doc.get("referrer_url")
    })
filename = f"{target_special}.json"
with open(filename, "w", encoding="utf-8") as f:
    json.dump(docs, f, ensure_ascii=False, indent=4)
print(f"Saved {len(docs)} docs to {filename}")
