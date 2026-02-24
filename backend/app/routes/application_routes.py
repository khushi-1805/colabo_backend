from fastapi import APIRouter, HTTPException
from app.database import applications_collection
from app.models import Application
from bson import ObjectId
from fastapi import HTTPException

router = APIRouter()

@router.post("/apply")
def apply(application: Application):

    campaign_object_id = ObjectId(application.campaign_id)

    existing = applications_collection.find_one({
        "campaign_id": campaign_object_id,
        "influencer_email": application.influencer_email
    })

    if existing:
        raise HTTPException(status_code=400, detail="Already applied")

    applications_collection.insert_one({
        "campaign_id": campaign_object_id,
        "influencer_email": application.influencer_email,
        "status": "pending"
    })

    return {"message": "Applied successfully"}


@router.get("/applications/{campaign_id}")
def get_applications(campaign_id: str):

    campaign_object_id = ObjectId(campaign_id)

    applications = list(
        applications_collection.find(
            {"campaign_id": campaign_object_id}
        )
    )

    for app in applications:
        app["_id"] = str(app["_id"])
        app["campaign_id"] = str(app["campaign_id"])

    return applications
@router.post("/application/{application_id}/accept")
def accept_application(application_id: str):
    result = applications_collection.update_one(
        {"_id": ObjectId(application_id)},
        {"$set": {"status": "accepted"}}
    )

    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Application not found")

    return {"message": "Application accepted"}

@router.post("/application/{application_id}/reject")
def reject_application(application_id: str):
    result = applications_collection.update_one(
        {"_id": ObjectId(application_id)},
        {"$set": {"status": "rejected"}}
    )

    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Application not found")

    return {"message": "Application rejected"}