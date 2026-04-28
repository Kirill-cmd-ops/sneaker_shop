from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import Response


from microservices.favorite_service.favorite_service.favorite.config import settings

from microservices.favorite_service.favorite_service.favorite.models import db_helper, Favorite
from microservices.favorite_service.favorite_service.favorite.schemas import FavoriteResponse
from microservices.favorite_service.favorite_service.favorite.dependencies.user_id import get_current_user_id

from microservices.favorite_service.favorite_service.favorite.services.favorite.delete import delete_favorite_service
from microservices.favorite_service.favorite_service.favorite.services.favorite.fetch import get_favorite_service

router = APIRouter(
    prefix=settings.api.build_path(settings.api.root, settings.api.v1.prefix),
    tags=["Favorite"],
)


@router.get(
    "/", 
    response_model=FavoriteResponse
)
async def get_favorite(
        user_id: int = Depends(get_current_user_id),
        session: AsyncSession = Depends(db_helper.session_getter),
) -> Favorite:
    return await get_favorite_service(
        session=session,
        user_id=user_id,
    )


@router.delete(
    "/",
    status_code=status.HTTP_204_NO_CONTENT,
    response_class=Response,
)
async def delete_favorite(
        user_id: int = Depends(get_current_user_id),
        session: AsyncSession = Depends(db_helper.session_getter),
) -> None:
    await delete_favorite_service(
        session=session,
        user_id=user_id,
    )
