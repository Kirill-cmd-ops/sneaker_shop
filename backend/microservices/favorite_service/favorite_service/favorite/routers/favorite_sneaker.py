from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from microservices.favorite_service.favorite_service.favorite.models import (
    db_helper,
)
from microservices.favorite_service.favorite_service.favorite.schemas import FavoriteSneakerCreate

from microservices.favorite_service.favorite_service.favorite.dependencies.user_id import get_current_user_id
from microservices.favorite_service.favorite_service.favorite.config import settings
from microservices.favorite_service.favorite_service.favorite.services.favorite_sneaker.delete import (
    delete_sneaker_from_favorite_service,
)
from microservices.favorite_service.favorite_service.favorite.services.favorite_sneaker.orchestrators import (
    create_sneaker_to_favorite_orchestrator,
)
from microservices.favorite_service.favorite_service.favorite.services.favorite_sneaker.update import (
    update_sneaker_in_favorite_service,
)

router = APIRouter(
    prefix=settings.api.build_path(
        settings.api.root, settings.api.v1.prefix, settings.api.v1.sneakers
    ),
    tags=["Favorite Sneaker"],
)


@router.post(
    "/",
    response_model=dict,
)
async def create_sneaker_to_favorite(
        item_create: FavoriteSneakerCreate,
        user_id: int = Depends(get_current_user_id),
        session: AsyncSession = Depends(db_helper.session_getter),
):
    sneaker_id = item_create.sneaker_id
    size_id = item_create.size_id

    return await create_sneaker_to_favorite_orchestrator(
        session=session,
        user_id=user_id,
        sneaker_id=sneaker_id,
        size_id=size_id,
    )


@router.put(
    "/{favorite_sneaker_id}",
    response_model=dict,
)
async def update_sneaker_in_favorite(
        favorite_sneaker_id: int,
        size_id: int,
        user_id: int = Depends(get_current_user_id),
        session: AsyncSession = Depends(db_helper.session_getter),
):
    updated_item = await update_sneaker_in_favorite_service(
        session=session,
        favorite_sneaker_id=favorite_sneaker_id,
        size_id=size_id,
        user_id=user_id,
    )
    return {"status": "Элемент обновлён", "item_id": updated_item.id}


@router.delete(
    "/{favorite_sneaker_id}",
    response_model=dict,
)
async def delete_sneaker_from_favorite(
        favorite_sneaker_id: int,
        user_id: int = Depends(get_current_user_id),
        session: AsyncSession = Depends(db_helper.session_getter),
):
    return await delete_sneaker_from_favorite_service(
        session=session,
        user_id=user_id,
        favorite_sneaker_id=favorite_sneaker_id,
    )
