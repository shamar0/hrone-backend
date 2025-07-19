from pymongo import MongoClient

import os
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

mongo_uri = os.getenv("MONGODB_URI")

client = MongoClient(mongo_uri)

db = client["hrone_db"]
product_collection = db["products"]
order_collection = db["orders"]