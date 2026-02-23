import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

client = MongoClient(os.getenv("MONGO_URI"))
db = client["collabo_db"]

users_collection = db["users"]
campaigns_collection = db["campaigns"]
applications_collection = db["applications"]