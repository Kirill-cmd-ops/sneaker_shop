from microservices.cart_service.cart_service.cart.models import Cart, db_helper


async def create_cart_service(user_id: int):
    async with db_helper.session_context() as session:
        async with session.begin():
            new_cart = Cart(user_id=user_id)
            session.add(new_cart)
