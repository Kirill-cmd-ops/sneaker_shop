from stock_notification_service.stock_notification.models import db_helper
from stock_notification_service.stock_notification.services.subscription.one_time.deactivate_bulk import (
    deactivate_all_one_time_subscriptions_for_sneaker_service,
)
from stock_notification_service.stock_notification.services.subscription.one_time.reactivate_bulk import (
    reactivate_all_one_time_subscriptions_for_sneaker_service,
)
from stock_notification_service.stock_notification.services.subscription.permanent.deactivate_bulk import (
    deactivate_all_permanent_subscriptions_for_sneaker_service,
)
from stock_notification_service.stock_notification.services.subscription.permanent.reactivate_bulk import (
    reactivate_all_permanent_subscriptions_for_sneaker_service,
)


async def deactivate_all_subscriptions_for_sneaker_orchestrator(sneaker_id):
    async with db_helper.session_context() as session:
        async with session.begin():
            await deactivate_all_permanent_subscriptions_for_sneaker_service(
                session=session,
                sneaker_id=sneaker_id,
            )
            await deactivate_all_one_time_subscriptions_for_sneaker_service(
                session=session,
                sneaker_id=sneaker_id,
            )


async def reactivate_all_subscriptions_for_sneaker_orchestrator(sneaker_id):
    async with db_helper.session_context() as session:
        async with session.begin():
            await reactivate_all_permanent_subscriptions_for_sneaker_service(
                session=session,
                sneaker_id=sneaker_id,
            )
            await reactivate_all_one_time_subscriptions_for_sneaker_service(
                session=session,
                sneaker_id=sneaker_id,
            )
