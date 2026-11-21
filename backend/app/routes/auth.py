from datetime import datetime, timezone

from fastapi import APIRouter, HTTPException, status

from app.database.database import users_collection
from app.dependencies.auth import (
    create_access_token,
    get_current_user,
    hash_password,
    verify_password,
)
from app.schemas.auth_schema import LoginRequest, RegisterRequest, TokenResponse
from fastapi import Depends

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(request: RegisterRequest):
    email = str(request.email).strip().lower()
    if users_collection.find_one({"email": email}):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered")

    now = datetime.now(timezone.utc)
    user = {
        "name": request.name.strip(),
        "email": email,
        "password_hash": hash_password(request.password),
        "role": "user",
        "is_active": True,
        "created_at": now,
        "updated_at": now,
    }
    result = users_collection.insert_one(user)
    user["_id"] = str(result.inserted_id)
    user.pop("password_hash", None)
    token = create_access_token(user["_id"], "user")
    return TokenResponse(access_token=token, user=user)


@router.post("/login", response_model=TokenResponse)
def login(request: LoginRequest):
    email = str(request.email).strip().lower()
    user = users_collection.find_one({"email": email})
    if not user or not verify_password(request.password, user.get("password_hash", "")):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")
    if not user.get("is_active", True):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Account is inactive")

    user_id = str(user["_id"])
    role = user.get("role", "user")
    user["_id"] = user_id
    user.pop("password_hash", None)
    token = create_access_token(user_id, role)
    return TokenResponse(access_token=token, user=user)


@router.get("/me")
def me(current_user: dict = Depends(get_current_user)):
    return {"success": True, "user": current_user}
