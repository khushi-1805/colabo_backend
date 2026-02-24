from fastapi import APIRouter
from app.database import campaigns_collection
from app.models import Campaign
from datetime import datetime
from bson import ObjectId
from app.database import applications_collection

router = APIRouter()

@router.post("/campaign")
def create_campaign(campaign: Campaign):
    campaign_data = campaign.dict()
    campaign_data["created_at"] = datetime.utcnow().isoformat()

    result = campaigns_collection.insert_one(campaign_data)

    return {
        "message": "Campaign created successfully",
        "campaign_id": str(result.inserted_id)
    }


@router.get("/campaigns/{brand_email}")
def get_campaigns(brand_email: str):
    campaigns = list(
        campaigns_collection.find({"created_by": brand_email})
    )

    for campaign in campaigns:
        campaign["_id"] = str(campaign["_id"])

    return campaigns
@router.get("/dashboard/{brand_email}")
def get_dashboard_stats(brand_email: str):

    # Get campaigns created by brand
    campaigns = list(
        campaigns_collection.find({"created_by": brand_email})
    )

    campaign_ids = [c["_id"] for c in campaigns]

    # Count total applications
    total_applicants = applications_collection.count_documents({
        "campaign_id": {"$in": campaign_ids}
    })

    # Count accepted
    selected_influencers = applications_collection.count_documents({
        "campaign_id": {"$in": campaign_ids},
        "status": "accepted"
    })

    return {
        "active_campaigns": len(campaign_ids),
        "total_applicants": total_applicants,
        "selected_influencers": selected_influencers
    }