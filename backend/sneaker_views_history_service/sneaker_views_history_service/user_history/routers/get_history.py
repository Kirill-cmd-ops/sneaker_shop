from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session


from sneaker_views_history_service.user_history.config import settings
from sneaker_views_history_service.user_history.dependencies.user_id import (
    get_current_user_id,
)
from sneaker_views_history_service.user_history.models.db_helper import db_helper
from sneaker_views_history_service.user_history.services.sneaker_view_history.fetch import (
    get_user_sneaker_view_history_service,
)

router = APIRouter(
    prefix=settings.api.build_path(settings.api.root, settings.api.v1.prefix),
    tags=["Sneakers Views"],
)


@router.get("/")
async def get_user_sneaker_view_history(
    session: Session = Depends(db_helper.session_getter),
    user_id: int = Depends(get_current_user_id),
):
    return await get_user_sneaker_view_history_service(session=session, user_id=user_id)
