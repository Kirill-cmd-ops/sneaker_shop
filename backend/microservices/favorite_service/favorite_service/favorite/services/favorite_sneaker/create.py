from sqlalchemy.ext.asyncio import AsyncSession

from microservices.favorite_service.favorite_service.favorite.models import FavoriteSneakerAssociation


async def add_sneaker_to_favorite_service(
        session: AsyncSession,
        favorite_id: int,
        sneaker_id: int,
        size_id: int,
):
    new_sneaker = FavoriteSneakerAssociation(
        favorite_id=favorite_id,
        sneaker_id=sneaker_id,
        size_id=size_id,
    )
    session.add(new_sneaker)
    return new_sneaker
