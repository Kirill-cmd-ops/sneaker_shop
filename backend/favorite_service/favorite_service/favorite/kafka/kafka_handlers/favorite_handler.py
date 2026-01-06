from favorite_service.favorite.models import db_helper
from favorite_service.favorite.services.favorite.create import create_favorite


async def handle_favorite(key, value):
    user_id = key or value.get("id")
    async with db_helper.session_context() as session:
        await create_favorite(session, user_id=int(user_id))