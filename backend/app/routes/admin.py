from datetime import datetime, timezone
import math
from typing import Any, Literal, Optional

from bson import ObjectId
from bson.errors import InvalidId
from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel, Field

from app.database.database import (
    calendar_events_collection,
    foods_collection,
    health_profiles_collection,
    recommendations_collection,
    users_collection,
)
from app.dependencies.auth import require_admin

router = APIRouter(prefix="/admin", tags=["Admin"])


class AdminUserUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=2, max_length=100)
    role: Optional[str] = Field(default=None, pattern="^(user|admin)$")
    is_active: Optional[bool] = None


class FoodCreate(BaseModel):
    food_name: str = Field(..., min_length=2, max_length=200)
    category: str = "General"
    meal_type: str = Field(..., pattern="^(Breakfast|Lunch|Dinner|Snack)$")
    food_preference: str = Field(..., pattern="^(Veg|Non-Veg|Any)$")
    calories: float = Field(..., ge=0)
    protein: float = Field(..., ge=0)
    carbohydrates: float = Field(..., ge=0)
    fat: float = Field(..., ge=0)
    fiber: float = Field(default=0, ge=0)
    sugar: float = Field(default=0, ge=0)
    sodium: float = Field(default=0, ge=0)
    allergens: str = "None"


class CalendarEventCreate(BaseModel):
    title: str = Field(..., min_length=2, max_length=150)
    description: Optional[str] = Field(default=None, max_length=1000)
    event_type: Literal["diet_plan", "reminder", "consultation", "follow_up"] = "reminder"
    status: Literal["scheduled", "in_progress", "completed", "cancelled"] = "scheduled"
    start_at: datetime
    end_at: datetime
    all_day: bool = True
    timezone_name: str = Field(default="Asia/Kolkata", alias="timezone", max_length=80)
    user_id: Optional[str] = None
    recommendation_id: Optional[str] = None
    meal_types: list[str] = Field(default_factory=list)
    completion_percentage: int = Field(default=0, ge=0, le=100)


class CalendarEventUpdate(BaseModel):
    title: Optional[str] = Field(default=None, min_length=2, max_length=150)
    description: Optional[str] = Field(default=None, max_length=1000)
    event_type: Optional[Literal["diet_plan", "reminder", "consultation", "follow_up"]] = None
    status: Optional[Literal["scheduled", "in_progress", "completed", "cancelled"]] = None
    start_at: Optional[datetime] = None
    end_at: Optional[datetime] = None
    all_day: Optional[bool] = None
    timezone_name: Optional[str] = Field(default=None, alias="timezone", max_length=80)
    user_id: Optional[str] = None
    recommendation_id: Optional[str] = None
    meal_types: Optional[list[str]] = None
    completion_percentage: Optional[int] = Field(default=None, ge=0, le=100)


def _object_id(value: str) -> ObjectId:
    try:
        return ObjectId(value)
    except InvalidId:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid resource ID")


def _json_safe(value: Any) -> Any:
    if isinstance(value, float):
        return value if math.isfinite(value) else 0.0
    if isinstance(value, dict):
        return {key: _json_safe(item) for key, item in value.items()}
    if isinstance(value, list):
        return [_json_safe(item) for item in value]
    if isinstance(value, ObjectId):
        return str(value)
    if isinstance(value, datetime):
        return value.isoformat()
    return value


@router.get("/dashboard")
def dashboard(admin: dict = Depends(require_admin)):
    now = datetime.utcnow()
    today = now.date().isoformat()
    recommendation_count = recommendations_collection.count_documents({})
    finalized_count = recommendations_collection.count_documents({"is_finalized": True})
    accepted_count = recommendations_collection.count_documents({"is_accepted": True})
    draft_count = recommendations_collection.count_documents({
        "$or": [
            {"is_accepted": {"$ne": True}},
            {"status": "draft"},
        ]
    })
    today_count = recommendations_collection.count_documents({"plan_date": today})
    today_accepted_count = recommendations_collection.count_documents({
        "plan_date": today,
        "is_accepted": True,
    })
    completed_today = recommendations_collection.count_documents({
        "plan_date": today,
        "is_accepted": True,
        "completion_percentage": 100,
    })
    user_count = users_collection.count_documents({"role": "user"})
    admin_count = users_collection.count_documents({"role": "admin"})
    food_count = foods_collection.count_documents({})
    profile_count = health_profiles_collection.count_documents({})
    active_user_count = users_collection.count_documents({"role": "user", "is_active": True})

    return {
        "success": True,
        "stats": {
            "total_users": user_count,
            "active_users": active_user_count,
            "admin_count": admin_count,
            "food_count": food_count,
            "profile_count": profile_count,
            "recommendation_count": recommendation_count,
            "finalized_plan_count": finalized_count,
            "accepted_plan_count": accepted_count,
            "draft_plan_count": draft_count,
            "today_plan_count": today_count,
            "today_accepted_count": today_accepted_count,
            "completed_today_count": completed_today,
        },
        "generated_at": now.isoformat(),
    }


@router.get("/users")
def list_users(
    limit: int = Query(default=20, ge=1, le=100),
    skip: int = Query(default=0, ge=0),
    search: str = "",
    admin: dict = Depends(require_admin),
):
    query: dict[str, Any] = {}
    if search.strip():
        query["$or"] = [
            {"name": {"$regex": search.strip(), "$options": "i"}},
            {"email": {"$regex": search.strip(), "$options": "i"}},
        ]

    cursor = users_collection.find(query, {"password_hash": 0}).sort("created_at", -1).skip(skip).limit(limit)
    users = []
    for user in cursor:
        user["_id"] = str(user["_id"])
        users.append(user)
    return {"success": True, "count": len(users), "users": users}


@router.put("/users/{user_id}")
def update_user(user_id: str, update: AdminUserUpdate, admin: dict = Depends(require_admin)):
    oid = _object_id(user_id)
    changes = {key: value for key, value in update.model_dump().items() if value is not None}
    if not changes:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No changes provided")
    changes["updated_at"] = datetime.utcnow()
    result = users_collection.update_one({"_id": oid}, {"$set": changes})
    if not result.matched_count:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return {"success": True, "message": "User updated successfully"}


@router.delete("/users/{user_id}")
def delete_user(user_id: str, admin: dict = Depends(require_admin)):
    oid = _object_id(user_id)
    if str(admin["_id"]) == user_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Cannot delete the current admin")
    result = users_collection.delete_one({"_id": oid})
    if not result.deleted_count:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    health_profiles_collection.delete_many({"user_id": user_id})
    recommendations_collection.delete_many({"user_id": user_id})
    return {"success": True, "message": "User and owned records deleted successfully"}


@router.get("/foods")
def list_foods(
    limit: int = Query(default=20, ge=1, le=200),
    skip: int = Query(default=0, ge=0),
    search: str = "",
    admin: dict = Depends(require_admin),
):
    query: dict[str, Any] = {}
    if search.strip():
        query["$or"] = [
            {"food_name": {"$regex": search.strip(), "$options": "i"}},
            {"name": {"$regex": search.strip(), "$options": "i"}},
        ]
    cursor = foods_collection.find(query).sort("food_name", 1).skip(skip).limit(limit)
    foods = []
    for food in cursor:
        food = _json_safe(food)
        food["_id"] = str(food["_id"])
        foods.append(food)
    return {"success": True, "count": len(foods), "foods": foods}


@router.post("/foods", status_code=status.HTTP_201_CREATED)
def create_food(food: FoodCreate, admin: dict = Depends(require_admin)):
    data = food.model_dump()
    data["name"] = data["food_name"]
    data["created_at"] = datetime.utcnow()
    data["updated_at"] = datetime.utcnow()
    result = foods_collection.insert_one(data)
    data["_id"] = str(result.inserted_id)
    return {"success": True, "food": data}


@router.put("/foods/{food_id}")
def update_food(food_id: str, food: FoodCreate, admin: dict = Depends(require_admin)):
    oid = _object_id(food_id)
    data = food.model_dump()
    data["name"] = data["food_name"]
    data["updated_at"] = datetime.utcnow()
    result = foods_collection.update_one({"_id": oid}, {"$set": data})
    if not result.matched_count:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Food not found")
    return {"success": True, "message": "Food updated successfully"}


@router.delete("/foods/{food_id}")
def delete_food(food_id: str, admin: dict = Depends(require_admin)):
    oid = _object_id(food_id)
    result = foods_collection.delete_one({"_id": oid})
    if not result.deleted_count:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Food not found")
    return {"success": True, "message": "Food deleted successfully"}


def _stored_object_id(value: Optional[str], field_name: str) -> Optional[Any]:
    if not value:
        return None
    try:
        return ObjectId(value)
    except InvalidId:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid {field_name}",
        )


def _serialize_calendar_event(event: dict) -> dict:
    event = _json_safe(event)
    event["_id"] = str(event["_id"]) if event.get("_id") else ""
    return event


@router.get("/calendar")
def list_calendar_events(
    start: str = "",
    end: str = "",
    status_filter: str = Query(default="", alias="status"),
    user_id: str = "",
    admin: dict = Depends(require_admin),
):
    now = datetime.now(timezone.utc)
    try:
        start_date = datetime.fromisoformat(start.replace("Z", "+00:00")) if start else now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        end_date = datetime.fromisoformat(end.replace("Z", "+00:00")) if end else (now.replace(day=28) + __import__("datetime").timedelta(days=4)).replace(day=1)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid calendar date range")

    query: dict[str, Any] = {
        "deleted_at": None,
        "$or": [
            {"start_at": {"$gte": start_date, "$lte": end_date}},
            {"end_at": {"$gte": start_date, "$lte": end_date}},
        ],
    }
    if status_filter:
        query["status"] = status_filter
    if user_id:
        query["user_id"] = {"$in": [user_id, _stored_object_id(user_id, "user ID")]}

    events = [
        _serialize_calendar_event(event)
        for event in calendar_events_collection.find(query).sort("start_at", 1)
    ]

    plan_query: dict[str, Any] = {}
    if user_id:
        plan_query["user_id"] = {"$in": [user_id, _stored_object_id(user_id, "user ID")]}
    start_key = start_date.date().isoformat()
    end_key = end_date.date().isoformat()
    plan_query["plan_date"] = {"$gte": start_key, "$lte": end_key}
    for plan in recommendations_collection.find(plan_query).sort("plan_date", 1):
        plan_id = str(plan["_id"])
        explicit_ids = {
            event.get("recommendation_id")
            for event in events
            if event.get("event_type") == "diet_plan"
        }
        if plan_id in explicit_ids:
            continue
        plan_date = plan.get("plan_date")
        try:
            start_at = datetime.fromisoformat(plan_date).replace(tzinfo=timezone.utc)
        except (TypeError, ValueError):
            continue
        status_value = plan.get("status") or (
            "accepted" if plan.get("is_accepted") else "finalized" if plan.get("is_finalized") else "draft"
        )
        events.append({
            "_id": f"plan-{plan_id}",
            "title": f"{plan.get('user_name') or plan.get('request_params', {}).get('name') or 'User'} diet plan",
            "description": "Generated nutrition plan",
            "event_type": "diet_plan",
            "status": status_value,
            "start_at": start_at.isoformat(),
            "end_at": start_at.isoformat(),
            "all_day": True,
            "timezone": "Asia/Kolkata",
            "user_id": plan.get("user_id"),
            "recommendation_id": plan_id,
            "completion": {
                "percentage": int(plan.get("completion_percentage") or 0),
                "meals_completed": sum(
                    1 for value in (plan.get("meal_checklist") or {}).values() if value
                ),
                "meals_total": 4,
            },
        })

    events.sort(key=lambda event: event.get("start_at", ""))
    return {"success": True, "count": len(events), "events": events}


@router.post("/calendar", status_code=status.HTTP_201_CREATED)
def create_calendar_event(
    event: CalendarEventCreate,
    admin: dict = Depends(require_admin),
):
    if event.end_at < event.start_at:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="End date must be after start date")

    now = datetime.now(timezone.utc)
    data = event.model_dump(by_alias=True)
    data["timezone"] = data.pop("timezone_name", event.timezone_name)
    data["user_id"] = _stored_object_id(event.user_id, "user ID")
    data["recommendation_id"] = _stored_object_id(event.recommendation_id, "recommendation ID")
    data["created_by"] = (
        ObjectId(admin["_id"])
        if str(admin["_id"]).isalnum() and len(str(admin["_id"])) == 24
        else str(admin["_id"])
    )
    data["completion"] = {
        "percentage": event.completion_percentage,
        "meals_completed": 0,
        "meals_total": len(event.meal_types) if event.meal_types else 4,
    }
    data["created_at"] = now
    data["updated_at"] = now
    data["deleted_at"] = None
    result = calendar_events_collection.insert_one(data)
    data["_id"] = str(result.inserted_id)
    return {"success": True, "event": _serialize_calendar_event(data)}


@router.put("/calendar/{event_id}")
def update_calendar_event(
    event_id: str,
    event: CalendarEventUpdate,
    admin: dict = Depends(require_admin),
):
    oid = _object_id(event_id)
    changes = event.model_dump(exclude_unset=True, by_alias=True)
    if not changes:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No changes provided")
    if "timezone_name" in changes:
        changes["timezone"] = changes.pop("timezone_name")
    if "completion_percentage" in changes:
        percentage = changes.pop("completion_percentage")
        changes["completion"] = {"percentage": percentage}
    if "user_id" in changes:
        changes["user_id"] = _stored_object_id(changes["user_id"], "user ID")
    if "recommendation_id" in changes:
        changes["recommendation_id"] = _stored_object_id(
            changes["recommendation_id"],
            "recommendation ID",
        )
    if changes.get("start_at") and changes.get("end_at"):
        if changes["end_at"] < changes["start_at"]:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="End date must be after start date")
    changes["updated_at"] = datetime.now(timezone.utc)
    result = calendar_events_collection.update_one({"_id": oid, "deleted_at": None}, {"$set": changes})
    if not result.matched_count:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Calendar event not found")
    return {"success": True, "message": "Calendar event updated successfully"}


@router.delete("/calendar/{event_id}")
def delete_calendar_event(event_id: str, admin: dict = Depends(require_admin)):
    oid = _object_id(event_id)
    result = calendar_events_collection.update_one(
        {"_id": oid, "deleted_at": None},
        {"$set": {"deleted_at": datetime.now(timezone.utc), "status": "cancelled", "updated_at": datetime.now(timezone.utc)}},
    )
    if not result.matched_count:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Calendar event not found")
    return {"success": True, "message": "Calendar event cancelled successfully"}


@router.get("/recommendations")
def list_recommendations(
    limit: int = Query(default=20, ge=1, le=100),
    skip: int = Query(default=0, ge=0),
    admin: dict = Depends(require_admin),
):
    cursor = recommendations_collection.find().sort("created_at", -1).skip(skip).limit(limit)
    recommendations = []
    for recommendation in cursor:
        recommendation = _json_safe(recommendation)
        recommendation["_id"] = str(recommendation["_id"]) if "_id" in recommendation else ""
        recommendations.append(recommendation)
    return {"success": True, "count": len(recommendations), "recommendations": recommendations}
