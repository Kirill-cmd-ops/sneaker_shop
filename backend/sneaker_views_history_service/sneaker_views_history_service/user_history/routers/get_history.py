from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session


from sneaker_views_history_service.user_history.config import settings
from sneaker_views_history_service.user_history.dependencies.get_current_user import (
    get_user_by_header,
)
from sneaker_views_history_service.user_history.models.db_helper import db_helper
from sneaker_views_history_service.user_history.services.sneaker_view.fetch import (
    clickhouse_select,
)

router = APIRouter(
    prefix=settings.api.build_path(settings.api.root, settings.api.v1.prefix),
    tags=["Sneakers Views"],
)


@router.get("/")
async def call_get_sneaker_views_clickhouse(
    session: Session = Depends(db_helper.session_getter),
    user_id: int = Depends(get_user_by_header),
):
    return await clickhouse_select(
        session=session,
        user_id=user_id,
    )
