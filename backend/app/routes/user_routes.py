from fastapi import APIRouter, HTTPException
from app.database import users_collection
from app.models import User

router = APIRouter()

@router.post("/signup")
def signup(user: User):
    if users_collection.find_one({"email": user.email}):
        raise HTTPException(status_code=400, detail="User already exists")
    
    users_collection.insert_one(user.dict())
    return {"message": "User created"}

@router.get("/users")
def get_users():
    return list(users_collection.find({}, {"_id": 0}))

from pydantic import BaseModel

class LoginRequest(BaseModel):
    email: str

@router.post("/login")
def login(data: LoginRequest):
    user = users_collection.find_one({"email": data.email})
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    user.pop("_id", None)
    return {
        "message": "Login successful",
        "user": user
    }