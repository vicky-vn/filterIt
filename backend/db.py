from pymongo import MongoClient

# Connection URI for local MongoDB
uri = "mongodb://localhost:27017"

client = MongoClient(uri)

db = client["filterIt"]  # Local database name
collection = db["uploads"]  # Collection name

try:
    client.admin.command('ping')
    print("Pinged your local MongoDB instance. You successfully connected to MongoDB!")
except Exception as e:
    print(f"Connection error: {e}")