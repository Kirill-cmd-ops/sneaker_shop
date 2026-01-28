from aiokafka import AIOKafkaProducer
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from microservices.sneaker_details_service.sneaker_details_service.sneaker_details.dependencies.user_id import (
    get_current_user_id,
)
from microservices.sneaker_details_service.sneaker_details_service.sneaker_details.kafka.producers.sneaker_views import (
    publish_sneaker_viewed,
)
from microservices.sneaker_details_service.sneaker_details_service.sneaker_details.dependencies.permissions import (
    check_role_permissions,
)
from microservices.sneaker_details_service.sneaker_details_service.sneaker_details.config import settings
from microservices.sneaker_details_service.sneaker_details_service.sneaker_details.dependencies.kafka_producer import (
    get_kafka_producer,
)
from microservices.sneaker_details_service.sneaker_details_service.sneaker_details.kafka.producers.sneakers import (
    publish_sneaker_created,
    publish_sneaker_updated,
    publish_sneaker_deleted,
)
from microservices.sneaker_details_service.sneaker_details_service.sneaker_details.models import db_helper

from microservices.sneaker_details_service.sneaker_details_service.sneaker_details.schemas import (
    SneakerCreate,
    SneakerUpdate,
)
from microservices.sneaker_details_service.sneaker_details_service.sneaker_details.services.sneaker.create import (
    create_sneaker_service,
)
from microservices.sneaker_details_service.sneaker_details_service.sneaker_details.services.sneaker.delete import (
    delete_sneaker_service,
)
from microservices.sneaker_details_service.sneaker_details_service.sneaker_details.services.sneaker.fetch import (
    get_sneaker_service,
)
from microservices.sneaker_details_service.sneaker_details_service.sneaker_details.services.sneaker.update import (
    update_sneaker_service,
)

router = APIRouter(
    prefix=settings.api.build_path(
        settings.api.root,
        settings.api.v1.prefix,
        settings.api.v1.sneakers,
    ),
    tags=["Sneaker"],
)


@router.post(
    "/",
    dependencies=(Depends(check_role_permissions("details.sneaker.create")),),
)
async def create_sneaker(
        sneaker_create: SneakerCreate,
        session: AsyncSession = Depends(db_helper.session_getter),
        producer: AIOKafkaProducer = Depends(get_kafka_producer),
):
    sneaker = await create_sneaker_service(
        session=session,
        sneaker_create=sneaker_create,
    )

    await publish_sneaker_created(
        producer=producer,
        sneaker_id=sneaker.id,
        sneaker_create=sneaker_create,
    )
    return sneaker


@router.delete(
    "/{sneaker_id}",
    dependencies=(Depends(check_role_permissions("details.sneaker.delete")),),
)
async def delete_sneaker(
        sneaker_id: int,
        session: AsyncSession = Depends(db_helper.session_getter),
        producer: AIOKafkaProducer = Depends(get_kafka_producer),
):
    await delete_sneaker_service(
        session=session,
        sneaker_id=sneaker_id,
    )

    await publish_sneaker_deleted(producer=producer, sneaker_id=sneaker_id)
    return "Товар успешно удален"


@router.patch(
    "/{sneaker_id}",
    dependencies=(Depends(check_role_permissions("details.sneaker.update")),),
)
async def update_sneaker(
        sneaker_id: int,
        sneaker_update: SneakerUpdate,
        session: AsyncSession = Depends(db_helper.session_getter),
        producer: AIOKafkaProducer = Depends(get_kafka_producer),
):
    await update_sneaker_service(
        session=session,
        sneaker_id=sneaker_id,
        sneaker_update=sneaker_update,
    )

    await publish_sneaker_updated(
        producer=producer,
        sneaker_id=sneaker_id,
        sneaker_update=sneaker_update,
    )
    return "Товар успешно обновлен"


@router.get("/{sneaker_id}")
async def get_sneaker(
        sneaker_id: int,
        session: AsyncSession = Depends(db_helper.session_getter),
        producer: AIOKafkaProducer = Depends(get_kafka_producer),
        user_id: int = Depends(get_current_user_id),
):
    sneaker_info = await get_sneaker_service(
        session=session,
        sneaker_id=sneaker_id,
    )

    if not sneaker_info:
        raise HTTPException(status_code=404, detail="Кроссовки не найдены")

    if user_id is not None:
        await publish_sneaker_viewed(
            producer=producer,
            sneaker_id=sneaker_id,
            user_id=user_id,
        )
    return sneaker_info
