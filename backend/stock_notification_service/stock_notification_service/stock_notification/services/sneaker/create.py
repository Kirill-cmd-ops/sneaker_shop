from stock_notification_service.stock_notification.schemas import SneakerCreate
from stock_notification_service.stock_notification.models import Sneaker, db_helper


async def create_sneaker_service(
    sneaker_create: SneakerCreate,
):
    async with db_helper.session_context() as session:
        async with session.begin():
            sneaker = Sneaker(**sneaker_create.dict(exclude="size_ids"))
            session.add(sneaker)
