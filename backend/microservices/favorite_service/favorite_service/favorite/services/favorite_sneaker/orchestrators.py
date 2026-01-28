from sqlalchemy.ext.asyncio import AsyncSession

from microservices.favorite_service.favorite_service.favorite.services.favorite.fetch import (
    get_user_favorite_id_service,
)
from microservices.favorite_service.favorite_service.favorite.services.favorite_sneaker.checkers import (
    get_sneaker_in_favorite_service,
)
from microservices.favorite_service.favorite_service.favorite.services.favorite_sneaker.create import (
    add_sneaker_to_favorite_service,
)
from microservices.favorite_service.favorite_service.favorite.services.sneaker.checkers import (
    check_sneaker_exists_service,
)
from microservices.favorite_service.favorite_service.favorite.services.sneaker_size.checkers import (
    check_sneaker_has_size_service,
)


async def create_sneaker_to_favorite_orchestrator(
        session: AsyncSession,
        user_id: int,
        sneaker_id: int,
        size_id: int,
):
    async with session.begin():
        favorite_id = await get_user_favorite_id_service(
            session=session,
            user_id=user_id,
        )
        await check_sneaker_exists_service(
            session=session,
            sneaker_id=sneaker_id,
        )
        await check_sneaker_has_size_service(
            session=session,
            sneaker_id=sneaker_id,
            size_id=size_id,
        )
        sneaker_record = await get_sneaker_in_favorite_service(
            session=session,
            favorite_id=favorite_id,
            sneaker_id=sneaker_id,
        )

        if sneaker_record is None:
            await add_sneaker_to_favorite_service(
                session=session,
                favorite_id=favorite_id,
                sneaker_id=sneaker_id,
                size_id=size_id,
            )
            return {"status": "Элемент добавлен"}

    return {"status": "Такая запись уже есть в избранном"}
