from fastapi import APIRouter, Depends
from backend.auth.authentication.fastapi_users import fastapi_users
from backend.auth.models import User

router = APIRouter()

@router.get("/profile")
async def get_profile(user: User = Depends(fastapi_users.current_user())):
    return {
        "id": user.id,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email,
    }
