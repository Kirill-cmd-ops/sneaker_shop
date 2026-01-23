from sqlalchemy.ext.asyncio import AsyncSession

from stock_notification_service.stock_notification.models import db_helper
from stock_notification_service.stock_notification.schemas.subscription import (
    SubscriptionCreate,
)
from stock_notification_service.stock_notification.services.sneaker.checkers import (
    check_sneaker_active_service,
)
from stock_notification_service.stock_notification.services.sneaker_size.checkers import (
    check_inactive_sneaker_size_service,
)
from stock_notification_service.stock_notification.services.subscription.one_time.checkers import (
    check_active_one_time_subscription_service,
)
from stock_notification_service.stock_notification.services.subscription.one_time.create import (
    create_user_one_time_subscription_service,
)
from stock_notification_service.stock_notification.services.subscription.one_time.deactivate_bulk import (
    deactivate_all_one_time_subscriptions_for_sneaker_service,
)
from stock_notification_service.stock_notification.services.subscription.one_time.fetch import (
    get_inactive_one_time_subscription_for_user_service,
)
from stock_notification_service.stock_notification.services.subscription.one_time.reactivate import (
    reactivate_one_time_subscription_by_sneaker_size_service,
    reactivate_one_time_subscription_by_id_service,
)
from stock_notification_service.stock_notification.services.subscription.one_time.reactivate_bulk import (
    reactivate_all_one_time_subscriptions_for_sneaker_service,
)
from stock_notification_service.stock_notification.services.subscription.permanent.checkers import (
    check_active_permanent_subscription_service,
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


async def create_user_one_time_subscription_orchestrator(
    session: AsyncSession,
    user_id: int,
    subscription_create: SubscriptionCreate,
):
    async with session.begin():
        # проверка активности sneaker
        await check_sneaker_active_service(
            session=session,
            sneaker_id=subscription_create.sneaker_id,
        )

        # проверка доступности размера для sneaker и проверка неактивности размера
        await check_inactive_sneaker_size_service(
            session=session,
            sneaker_id=subscription_create.sneaker_id,
            size_id=subscription_create.size_id,
        )

        # проверка активной одноразовой подписки
        await check_active_one_time_subscription_service(
            session=session,
            user_id=user_id,
            sneaker_id=subscription_create.sneaker_id,
            size_id=subscription_create.size_id,
        )

        # проверка активной перманентной подписки
        await check_active_permanent_subscription_service(
            session=session,
            user_id=user_id,
            sneaker_id=subscription_create.sneaker_id,
            size_id=subscription_create.size_id,
        )

        # реактивация деактивированной разовой подписки
        update_subscription = (
            await reactivate_one_time_subscription_by_sneaker_size_service(
                session=session,
                user_id=user_id,
                sneaker_id=subscription_create.sneaker_id,
                size_id=subscription_create.size_id,
            )
        )
        if update_subscription:
            result = update_subscription
        else:
            # создание разовой подписки
            result = await create_user_one_time_subscription_service(
                sneaker_id=subscription_create.sneaker_id,
                size_id=subscription_create.size_id,
                user_id=user_id,
                session=session,
            )

    return result
