from pathlib import Path
from pymongo import MongoClient
from dotenv import load_dotenv
import os

# Load .env from the backend directory (three levels up from this file)
_env_path = Path(__file__).resolve().parent.parent.parent / ".env"
load_dotenv(_env_path)

MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
DATABASE_NAME = os.getenv("DATABASE_NAME", "nutriai")

client = MongoClient(MONGODB_URI)

db = client[DATABASE_NAME]

# Collections
users_collection = db["users"]
recommendations_collection = db["recommendations"]
health_profiles_collection = db["health_profiles"]
foods_collection = db["foods"]
