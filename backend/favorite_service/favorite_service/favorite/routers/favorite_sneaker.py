from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from favorite_service.favorite.models import (
    db_helper,
)
from favorite_service.favorite.schemas import FavoriteSneakerCreate
from favorite_service.favorite.services.check_favorite import check_favorite_exists
from favorite_service.favorite.services.check_permissions import check_role_permissions
from favorite_service.favorite.services.check_sneaker_in_favorite import (
    check_sneaker_in_favorite_exists,
)
from favorite_service.favorite.services.favorite_sneaker import (
    create_sneaker_to_favorite,
    delete_sneaker_to_favorite,
)
from favorite_service.favorite.dependencies.get_current_user import get_user_by_header
from favorite_service.favorite.config import settings

router = APIRouter(
    prefix=settings.api.build_path(
        settings.api.root, settings.api.v1.prefix, settings.api.v1.sneakers
    ),
    tags=["Favorite Sneaker"],
)


@router.post(
    "/",
    response_model=dict,
    dependencies=(Depends(check_role_permissions("favorite.sneaker.add")),),
)
async def call_create_sneaker_to_favorite(
    item_create: FavoriteSneakerCreate,
    user_id: int = Depends(get_user_by_header),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    async with session.begin():
        favorite_id = await check_favorite_exists(session, user_id)
        sneaker_record = await check_sneaker_in_favorite_exists(
            session, favorite_id, item_create
        )

        if not sneaker_record:
            new_item = await create_sneaker_to_favorite(
                session,
                favorite_id=favorite_id,
                sneaker_id=item_create.sneaker_id,
            )
            return {"status": "Элемент добавлен", "item_id": new_item.id}

    return {"status": "Такая запись уже есть в избранном"}


@router.delete(
    "/{favorite_sneaker_id}",
    response_model=dict,
    dependencies=(Depends(check_role_permissions("favorite.sneaker.delete")),),
)
async def call_delete_sneaker_to_favorite(
    favorite_sneaker_id: int,
    user_id: int = Depends(get_user_by_header),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    async with session.begin():
        await delete_sneaker_to_favorite(
            session, user_id=user_id, favorite_sneaker_id=favorite_sneaker_id
        )
        return {"status": "Элемент удалён"}
