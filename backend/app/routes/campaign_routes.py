from fastapi import APIRouter
from app.database import campaigns_collection
from app.models import Campaign
from datetime import datetime

router = APIRouter()

@router.post("/campaign")
def create_campaign(campaign: Campaign):
    campaign_data = campaign.dict()
    campaign_data["created_at"] = datetime.utcnow().isoformat()
    campaigns_collection.insert_one(campaign_data)
    return {"message": "Campaign created successfully"}

@router.get("/campaigns/{brand_email}")
def get_campaigns(brand_email: str):
    campaigns = list(
        campaigns_collection.find(
            {"created_by": brand_email},
            {"_id": 0}
        )
    )
    return campaigns