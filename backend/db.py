from pymongo import MongoClient

MONGO_URI = "your_mongo_uri_here"  # Replace with your actual MongoDB URI
client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
db = client["receipt_dashboard"]
receipts_collection = db["receipts"]

def reset_receipts():
    receipts_collection.delete_many({})
