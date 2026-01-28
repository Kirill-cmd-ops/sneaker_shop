from microservices.favorite_service.favorite_service.favorite.models import Favorite, db_helper


async def create_favorite_service(user_id: int):
    async with db_helper.session_context() as session:
        async with session.begin():
            new_favorite = Favorite(user_id=user_id)
            session.add(new_favorite)
