from microservices.favorite_service.favorite_service.favorite.services.favorite.create import create_favorite_service


async def handle_favorite_event(key, value):
    user_id = key or value.get("id")
    await create_favorite_service(user_id=int(user_id))
