from datetime import datetime, timezone
import os

from fastapi import APIRouter, Depends, HTTPException
from bson import ObjectId

from app.database.database import health_profiles_collection, recommendations_collection
from app.dependencies.auth import get_current_user
from app.schemas.profile_schema import HealthProfile
from app.services.profile_service import save_profile
from app.schemas.recommendation_schema import RecommendationRequest
from app.services.recommendation_service import generate_diet_plan

router = APIRouter(prefix="/users", tags=["Users"])


def _today_key() -> str:
    return datetime.now(timezone.utc).date().isoformat()


def _serialize_plan(plan: dict) -> dict:
    plan["_id"] = str(plan["_id"])
    plan["recommendation_id"] = plan["_id"]
    if isinstance(plan.get("created_at"), datetime):
        plan["created_at"] = plan["created_at"].isoformat()
    return plan


@router.get("/profile")
def get_profile(current_user: dict = Depends(get_current_user)):
    profile = health_profiles_collection.find_one({"user_id": current_user["_id"]})
    if not profile:
        return {"success": True, "profile": None}
    profile["_id"] = str(profile["_id"])
    return {"success": True, "profile": profile}


@router.put("/profile")
def update_profile(profile: HealthProfile, current_user: dict = Depends(get_current_user)):
    return save_profile(profile, user_id=current_user["_id"])


@router.post("/diet-plan")
def create_diet_plan(request: RecommendationRequest, current_user: dict = Depends(get_current_user)):
    if not request.name or request.name.strip() in ("", "User"):
        request.name = current_user.get("name", "User")
    today = _today_key()
    demo_mode = os.getenv("DEMO_MODE", "false").strip().lower() in {"1", "true", "yes"}
    query = {"plan_date": today, "is_finalized": True}
    if not demo_mode:
        query["user_id"] = current_user["_id"]

    existing = recommendations_collection.find_one(query, sort=[("created_at", -1)])
    if existing:
        return {
            "success": False,
            "message": "Today's diet plan is already finalized.",
            "recommendation": _serialize_plan(existing),
        }

    draft_query = {"plan_date": today}
    if not demo_mode:
        draft_query["user_id"] = current_user["_id"]
    existing_draft = recommendations_collection.find_one(draft_query, sort=[("created_at", -1)])
    if existing_draft and not existing_draft.get("is_accepted", existing_draft.get("is_finalized", False)):
        return {
            "success": False,
            "message": "A draft diet plan already exists for today. Review or regenerate it.",
            "recommendation": _serialize_plan(existing_draft),
        }

    result = generate_diet_plan(request, user_id=current_user["_id"])
    meal_checklist = {
        "breakfast": False,
        "lunch": False,
        "snacks": False,
        "dinner": False,
    }
    recommendations_collection.update_one(
        {"_id": ObjectId(result["recommendation_id"])},
        {
            "$set": {
                "plan_date": today,
                "is_finalized": False,
                "is_accepted": False,
                "status": "draft",
                "meal_checklist": meal_checklist,
                "completion_percentage": 0,
            }
        },
    )
    result["plan_date"] = today
    result["is_finalized"] = False
    result["is_accepted"] = False
    result["status"] = "draft"
    result["meal_checklist"] = meal_checklist
    result["completion_percentage"] = 0
    return result


@router.get("/today")
def get_today_plan(current_user: dict = Depends(get_current_user)):
    today = _today_key()
    demo_mode = os.getenv("DEMO_MODE", "false").strip().lower() in {"1", "true", "yes"}
    query = {"plan_date": today}
    if not demo_mode:
        query["user_id"] = current_user["_id"]
    plan = recommendations_collection.find_one(query, sort=[("created_at", -1)])
    if not plan:
        return {"success": True, "plan": None}
    return {"success": True, "plan": _serialize_plan(plan)}


@router.put("/today/accept")
def accept_today_plan(current_user: dict = Depends(get_current_user)):
    today = _today_key()
    demo_mode = os.getenv("DEMO_MODE", "false").strip().lower() in {"1", "true", "yes"}
    query = {"plan_date": today}
    if not demo_mode:
        query["user_id"] = current_user["_id"]

    accepted = recommendations_collection.find_one(
        {**query, "is_accepted": True},
        sort=[("created_at", -1)],
    )
    if accepted:
        return {
            "success": True,
            "message": "Today's diet plan is already accepted.",
            "plan": _serialize_plan(accepted),
        }

    draft = recommendations_collection.find_one(
        query,
        sort=[("created_at", -1)],
    )
    if not draft:
        raise HTTPException(status_code=404, detail="Today's diet plan was not found")

    recommendations_collection.update_one(
        {"_id": draft["_id"]},
        {
            "$set": {
                "is_accepted": True,
                "is_finalized": True,
                "status": "accepted",
                "accepted_at": datetime.now(timezone.utc),
            }
        },
    )
    draft["is_accepted"] = True
    draft["is_finalized"] = True
    draft["status"] = "accepted"
    return {
        "success": True,
        "message": "Diet plan accepted for today.",
        "plan": _serialize_plan(draft),
    }


@router.post("/today/regenerate")
def regenerate_today_plan(request: RecommendationRequest, current_user: dict = Depends(get_current_user)):
    today = _today_key()
    demo_mode = os.getenv("DEMO_MODE", "false").strip().lower() in {"1", "true", "yes"}
    query = {"plan_date": today}
    if not demo_mode:
        query["user_id"] = current_user["_id"]

    accepted = recommendations_collection.find_one(
        {**query, "is_accepted": True},
        sort=[("created_at", -1)],
    )
    if accepted:
        return {
            "success": False,
            "message": "An accepted diet plan cannot be regenerated.",
            "recommendation": _serialize_plan(accepted),
        }

    if not request.name or request.name.strip() in ("", "User"):
        request.name = current_user.get("name", "User")

    recommendations_collection.delete_many({**query, "is_accepted": {"$ne": True}})
    result = generate_diet_plan(request, user_id=current_user["_id"])
    meal_checklist = {
        "breakfast": False,
        "lunch": False,
        "snacks": False,
        "dinner": False,
    }
    recommendations_collection.update_one(
        {"_id": ObjectId(result["recommendation_id"])},
        {
            "$set": {
                "plan_date": today,
                "is_finalized": False,
                "is_accepted": False,
                "status": "draft",
                "meal_checklist": meal_checklist,
                "completion_percentage": 0,
            }
        },
    )
    result["plan_date"] = today
    result["is_finalized"] = False
    result["is_accepted"] = False
    result["status"] = "draft"
    result["meal_checklist"] = meal_checklist
    result["completion_percentage"] = 0
    return result


@router.put("/today/checklist")
def update_today_checklist(payload: dict, current_user: dict = Depends(get_current_user)):
    meal = str(payload.get("meal", "")).strip().lower()
    if meal not in {"breakfast", "lunch", "snacks", "dinner"}:
        raise HTTPException(status_code=400, detail="Invalid meal name")

    checked = bool(payload.get("checked", False))
    today = _today_key()
    demo_mode = os.getenv("DEMO_MODE", "false").strip().lower() in {"1", "true", "yes"}
    query = {"plan_date": today, "is_finalized": True}
    if not demo_mode:
        query["user_id"] = current_user["_id"]
    plan = recommendations_collection.find_one(query)
    if not plan:
        raise HTTPException(status_code=404, detail="Today's diet plan was not found")

    checklist = plan.get("meal_checklist") or {
        "breakfast": False,
        "lunch": False,
        "snacks": False,
        "dinner": False,
    }
    checklist[meal] = checked
    completed = sum(1 for value in checklist.values() if value)
    completion_percentage = round((completed / 4) * 100)
    recommendations_collection.update_one(
        {"_id": plan["_id"]},
        {"$set": {"meal_checklist": checklist, "completion_percentage": completion_percentage}},
    )
    plan["meal_checklist"] = checklist
    plan["completion_percentage"] = completion_percentage
    return {"success": True, "plan": _serialize_plan(plan)}


@router.get("/diet-plan")
def list_diet_plans(current_user: dict = Depends(get_current_user)):
    demo_mode = os.getenv("DEMO_MODE", "false").strip().lower() in {"1", "true", "yes"}
    query = {} if demo_mode else {"user_id": current_user["_id"]}
    cursor = recommendations_collection.find(query).sort("created_at", -1)
    plans = []
    for plan in cursor:
        plan["_id"] = str(plan["_id"])
        plan["recommendation_id"] = plan["_id"]
        if isinstance(plan.get("created_at"), datetime):
            plan["created_at"] = plan["created_at"].isoformat()
        plans.append(plan)
    return {"success": True, "count": len(plans), "recommendations": plans}
