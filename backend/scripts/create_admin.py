import os
import sys
from datetime import datetime, timezone
from getpass import getpass
from pathlib import Path

backend_root = Path(__file__).resolve().parents[1]
if str(backend_root) not in sys.path:
    sys.path.insert(0, str(backend_root))

from app.database.database import users_collection
from app.dependencies.auth import hash_password


def main():
    name = os.getenv("ADMIN_NAME") or input("Admin name: ").strip()
    email = (os.getenv("ADMIN_EMAIL") or input("Admin email: ").strip()).lower()
    password = os.getenv("ADMIN_PASSWORD") or getpass("Admin password (minimum 8 characters): ")

    if not name or not email or len(password) < 8:
        raise SystemExit("Admin name, email, and a password of at least 8 characters are required.")

    existing = users_collection.find_one({"email": email})
    if existing:
        users_collection.update_one(
            {"email": email},
            {"$set": {"role": "admin", "is_active": True, "updated_at": datetime.now(timezone.utc)}},
        )
        print(f"Updated existing account to admin: {email}")
        return

    now = datetime.now(timezone.utc)
    users_collection.insert_one({
        "name": name,
        "email": email,
        "password_hash": hash_password(password),
        "role": "admin",
        "is_active": True,
        "created_at": now,
        "updated_at": now,
    })
    print(f"Created admin account: {email}")


if __name__ == "__main__":
    main()
