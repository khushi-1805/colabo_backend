from fastapi import APIRouter, HTTPException
from app.database import applications_collection
from app.models import Application

router = APIRouter()

@router.post("/apply")
def apply(application: Application):
    
    # Check if already applied
    existing = applications_collection.find_one({
        "campaign_id": application.campaign_id,
        "influencer_email": application.influencer_email
    })

    if existing:
        raise HTTPException(status_code=400, detail="Already applied to this campaign")

    applications_collection.insert_one(application.dict())

    return {"message": "Applied successfully"}

@router.get("/applications/{campaign_id}")
def get_applications(campaign_id: str):
    applications = list(
        applications_collection.find(
            {"campaign_id": campaign_id},
            {"_id": 0}
        )
    )
    return applications