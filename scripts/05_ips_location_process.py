import IP2Location
import csv
from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["glamira"]
collection = db["summary"]

# New collection to store enriched IP data
geo_collection = db["ips_location"]

# Aggregation pipeline to get unique IPs
pipeline = [{"$group": {"_id": "$ip"}}]
unique_ips_cursor = collection.aggregate(pipeline)
unique_ips = [doc["_id"] for doc in unique_ips_cursor]

# Initialize IP2Location with your BIN file
ip2loc = IP2Location.IP2Location("IP2LOCATION-LITE-DB5.BIN")

# Write results to CSV
with open("pj5_ip_locations.csv", mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["IP", "Country", "Region", "City", "Latitude", "Longitude"])

    for idx, ip in enumerate(unique_ips, start=1):
        print(f"Processing row {idx}/{len(unique_ips)}: {ip}")
        try:
            rec = ip2loc.get_all(ip)
            row = {
                "ip": ip,
                "country": rec.country_long,
                "region": rec.region,
                "city": rec.city,
                "latitude": rec.latitude,
                "longitude": rec.longitude
            }

            # Write to CSV
            writer.writerow(row.values())

            # Insert into new MongoDB collection
            geo_collection.insert_one(row)

        except Exception as e:
            print(f"Error processing {ip}: {e}")