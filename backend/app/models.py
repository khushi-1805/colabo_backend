from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class User(BaseModel):
    name: str
    email: str
    role: str  # brand or influencer

class Campaign(BaseModel):
    title: str
    category: str
    description: Optional[str] = None
    budget: str
    deadline: str
    created_by: str
    created_at: Optional[str] = None

class Application(BaseModel):
    campaign_id: str
    influencer_email: str
    status: Optional[str] = "pending"