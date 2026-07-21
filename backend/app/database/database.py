<<<<<<< HEAD
from pathlib import Path
=======
>>>>>>> aaaa19b7534d463414494a2051f6f1c583eb1cc7
from pymongo import MongoClient
from dotenv import load_dotenv
import os

<<<<<<< HEAD
# Load .env from the backend directory (three levels up from this file)
_env_path = Path(__file__).resolve().parent.parent.parent / ".env"
load_dotenv(_env_path)

MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
DATABASE_NAME = os.getenv("DATABASE_NAME", "nutriai")
=======
load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI", "")
DATABASE_NAME = os.getenv("DATABASE_NAME", "")
>>>>>>> aaaa19b7534d463414494a2051f6f1c583eb1cc7

client = MongoClient(MONGODB_URI)

db = client[DATABASE_NAME]

# Collections
users_collection = db["users"]
recommendations_collection = db["recommendations"]
health_profiles_collection = db["health_profiles"]
foods_collection = db["foods"]
<<<<<<< HEAD
=======

try:
    client.admin.command("ping")
    print("✅ MongoDB Connected Successfully!")
except Exception as e:
    print("❌ MongoDB Connection Failed")
    print(e)
>>>>>>> aaaa19b7534d463414494a2051f6f1c583eb1cc7
