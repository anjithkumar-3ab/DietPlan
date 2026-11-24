from pathlib import Path
from pymongo import MongoClient
from dotenv import load_dotenv
import os
import dns.resolver

# Configure DNS resolver to use reliable public DNS servers if system DNS times out on SRV records
try:
    resolver = dns.resolver.get_default_resolver()
    public_dns = ['8.8.8.8', '1.1.1.1', '8.8.4.4', '1.0.0.1']
    for dns_ip in reversed(public_dns):
        if dns_ip not in resolver.nameservers:
            resolver.nameservers.insert(0, dns_ip)
except Exception:
    pass

# Load .env from the backend directory (three levels up from this file)
_env_path = Path(__file__).resolve().parent.parent.parent / ".env"
load_dotenv(_env_path)

MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
DATABASE_NAME = os.getenv("DATABASE_NAME", "dietplan")

client = MongoClient(MONGODB_URI)

db = client[DATABASE_NAME]

# Collections
users_collection = db["users"]
recommendations_collection = db["recommendations"]
health_profiles_collection = db["health_profiles"]
foods_collection = db["foods"]
calendar_events_collection = db["calendar_events"]


def configure_database():
    """Create collection validators and indexes used by the application."""
    try:
        if "calendar_events" not in db.list_collection_names():
            db.create_collection(
                "calendar_events",
                validator={
                    "$jsonSchema": {
                        "bsonType": "object",
                        "required": [
                            "_id",
                            "title",
                            "event_type",
                            "status",
                            "start_at",
                            "end_at",
                            "timezone",
                            "created_by",
                            "created_at",
                            "updated_at",
                        ],
                        "properties": {
                            "_id": {"bsonType": "objectId"},
                            "title": {"bsonType": "string", "minLength": 2, "maxLength": 150},
                            "description": {"bsonType": ["string", "null"]},
                            "event_type": {
                                "enum": ["diet_plan", "reminder", "consultation", "follow_up"]
                            },
                            "status": {
                                "enum": ["scheduled", "in_progress", "completed", "cancelled"]
                            },
                            "start_at": {"bsonType": "date"},
                            "end_at": {"bsonType": "date"},
                            "all_day": {"bsonType": "bool"},
                            "timezone": {"bsonType": "string"},
                            "user_id": {"bsonType": ["objectId", "string", "null"]},
                            "recommendation_id": {"bsonType": ["objectId", "string", "null"]},
                            "created_by": {"bsonType": ["objectId", "string"]},
                            "meal_types": {"bsonType": "array"},
                            "completion": {"bsonType": "object"},
                            "created_at": {"bsonType": "date"},
                            "updated_at": {"bsonType": "date"},
                            "deleted_at": {"bsonType": ["date", "null"]},
                        },
                    }
                },
                validationLevel="strict",
                validationAction="error",
            )

        calendar_events_collection.create_index(
            [("start_at", 1), ("end_at", 1)],
            name="calendar_date_range",
        )
        calendar_events_collection.create_index(
            [("user_id", 1), ("start_at", 1)],
            name="user_calendar",
        )
        calendar_events_collection.create_index(
            [("status", 1), ("start_at", 1)],
            name="calendar_status",
        )
        calendar_events_collection.create_index(
            [("recommendation_id", 1)],
            name="recommendation_calendar_event",
            sparse=True,
        )
        recommendations_collection.create_index(
            [("plan_date", 1), ("created_at", -1)],
            name="plan_calendar_lookup",
        )
        users_collection.create_index("email", unique=True, name="unique_user_email")
        foods_collection.update_many(
            {"S.No": {"$exists": True}},
            {"$unset": {"S.No": ""}},
        )
        foods_collection.update_many(
            {"name": {"$exists": False}},
            [{"$set": {"name": "$food_name"}}],
        )
    except Exception as exc:
        print(f"❌ MongoDB schema setup failed: {exc}")


configure_database()

try:
    client.admin.command("ping")
    print("✅ MongoDB Connected Successfully!")
except Exception as e:
    print("❌ MongoDB Connection Failed")
    print(e)