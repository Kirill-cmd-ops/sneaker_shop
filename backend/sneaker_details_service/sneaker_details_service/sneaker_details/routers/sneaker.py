from aiokafka import AIOKafkaProducer
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from sneaker_details_service.sneaker_details.services.check_permissions import (
    check_role_permissions,
)
from sneaker_details_service.sneaker_details.config import settings
from sneaker_details_service.sneaker_details.dependencies.get_kafka_producer import (
    get_kafka_producer,
)
from sneaker_details_service.sneaker_details.kafka.producer_event.create_sneaker_data import (
    send_create_sneaker_data,
)
from sneaker_details_service.sneaker_details.kafka.producer_event.delete_sneaker_data import (
    send_delete_sneaker_data,
)
from sneaker_details_service.sneaker_details.kafka.producer_event.update_sneaker_data import (
    send_update_sneaker_data,
)
from sneaker_details_service.sneaker_details.models import db_helper
from sneaker_details_service.sneaker_details.services.sneaker import get_sneaker_details

from sneaker_details_service.sneaker_details.schemas import (
    SneakerCreate,
    SneakerUpdate,
)
from sneaker_details_service.sneaker_details.services.sneaker import (
    create_sneaker,
    delete_sneaker,
    update_sneaker,
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
    "/create/",
    dependencies=(Depends(check_role_permissions("details.sneaker.create")),),
)
async def call_create_sneaker(
    sneaker_create: SneakerCreate,
    session: AsyncSession = Depends(db_helper.session_getter),
    producer: AIOKafkaProducer = Depends(get_kafka_producer),
):
    sneaker = await create_sneaker(session, sneaker_create)
    await send_create_sneaker_data(producer, sneaker.id, sneaker_create)
    return sneaker


@router.delete(
    "/delete/",
    dependencies=(Depends(check_role_permissions("details.sneaker.delete")),),
)
async def call_delete_sneaker(
    sneaker_id: int,
    session: AsyncSession = Depends(db_helper.session_getter),
    producer: AIOKafkaProducer = Depends(get_kafka_producer),
):
    await delete_sneaker(session, sneaker_id)
    await send_delete_sneaker_data(producer, sneaker_id)
    return "Товар успешно удален"


@router.patch(
    "/update/",
    dependencies=(Depends(check_role_permissions("details.sneaker.update")),),
)
async def call_update_sneaker(
    sneaker_id: int,
    sneaker_update: SneakerUpdate,
    session: AsyncSession = Depends(db_helper.session_getter),
    producer: AIOKafkaProducer = Depends(get_kafka_producer),
):
    await update_sneaker(session, sneaker_id, sneaker_update)
    await send_update_sneaker_data(producer, sneaker_id, sneaker_update)
    return "Товар успешно обновлен"


@router.get("/view/{sneaker_id}")
async def call_get_sneaker_details(
    sneaker_id: int,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    sneaker_info = await get_sneaker_details(session=session, sneaker_id=sneaker_id)

    if not sneaker_info:
        raise HTTPException(status_code=404, detail="Кроссовки не найдены")

    return sneaker_info
