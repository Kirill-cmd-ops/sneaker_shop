from fastapi import APIRouter, Depends

from auth_service.auth.config import settings
from auth_service.profile.dependencies.get_current_user import get_current_user

router = APIRouter(
    prefix=settings.api.v1.profile,
    tags=["Profile"],
)


@router.get("/profile")
async def get_profile(user: str = Depends(get_current_user)):
    return {
        "id": user.id,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email,
    }
