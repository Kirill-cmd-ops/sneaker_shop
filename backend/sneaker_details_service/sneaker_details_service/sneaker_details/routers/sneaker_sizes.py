from aiokafka import AIOKafkaProducer
from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from sneaker_details_service.sneaker_details.config import settings

from sneaker_details_service.sneaker_details.dependencies.kafka_producer import (
    get_kafka_producer,
)
from sneaker_details_service.sneaker_details.kafka.producers.sneaker_sizes import (
    publish_sneaker_sizes_created,
    publish_sneaker_size_updated,
    publish_sneaker_sizes_deleted,
)

from sneaker_details_service.sneaker_details.schemas import (
    SneakerSizesCreate,
    SneakerSizeUpdate,
    SneakerAssocsDelete,
)
from sneaker_details_service.sneaker_details.dependencies.permissions import (
    check_role_permissions,
)


from sneaker_details_service.sneaker_details.models import (
    SneakerSizeAssociation,
    db_helper,
)
from sneaker_details_service.sneaker_details.services.sneaker_association.delete import (
    delete_sneaker_associations_service,
)
from sneaker_details_service.sneaker_details.services.sneaker_association.fetch import (
    get_sneaker_associations_service,
)
from sneaker_details_service.sneaker_details.services.sneaker_size.create import (
    add_sizes_to_sneaker_service,
)
from sneaker_details_service.sneaker_details.services.sneaker_size.update import (
    update_sneaker_size_quantity_service,
)

router = APIRouter(
    prefix=settings.api.build_path(
        settings.api.root,
        settings.api.v1.prefix,
        settings.api.v1.sneakers,
    ),
    tags=["Sneaker Sizes"],
)


@router.post(
    "/{sneaker_id}/sizes",
    dependencies=(Depends(check_role_permissions("details.sneaker.size.create")),),
)
async def add_sizes_to_sneaker(
    sneaker_id: int,
    sneaker_sizes_create: SneakerSizesCreate,
    session: AsyncSession = Depends(db_helper.session_getter),
    producer: AIOKafkaProducer = Depends(get_kafka_producer),
):
    await add_sizes_to_sneaker_service(
        session=session,
        sneaker_id=sneaker_id,
        sneaker_sizes_create=sneaker_sizes_create,
    )

    await publish_sneaker_sizes_created(
        producer=producer,
        sneaker_id=sneaker_id,
        sneaker_sizes_create=sneaker_sizes_create,
    )
    return "Запись нового размера прошла успешно"


@router.delete(
    "/{sneaker_id}/sizes",
    dependencies=(Depends(check_role_permissions("details.sneaker.size.delete")),),
)
async def delete_sizes_from_sneaker(
    sneaker_id: int,
    sneaker_sizes_delete: SneakerAssocsDelete,
    session: AsyncSession = Depends(db_helper.session_getter),
    producer: AIOKafkaProducer = Depends(get_kafka_producer),
):
    await delete_sneaker_associations_service(
        session=session,
        sneaker_id=sneaker_id,
        sneaker_assoc_delete=sneaker_sizes_delete,
        sneaker_association_model=SneakerSizeAssociation,
        field_name="size_id",
    )

    await publish_sneaker_sizes_deleted(
        producer=producer,
        sneaker_id=sneaker_id,
        sneaker_sizes_delete=sneaker_sizes_delete,
    )
    return "Размеры товара успешно удалены"


@router.patch(
    "/{sneaker_id}/sizes",
    dependencies=(Depends(check_role_permissions("details.sneaker.size.update")),),
)
async def update_sneaker_size_quantity(
    sneaker_id: int,
    sneaker_size_update: SneakerSizeUpdate,
    session: AsyncSession = Depends(db_helper.session_getter),
    producer: AIOKafkaProducer = Depends(get_kafka_producer),
):
    await update_sneaker_size_quantity_service(
        session=session,
        sneaker_id=sneaker_id,
        sneaker_size_update=sneaker_size_update,
    )

    await publish_sneaker_size_updated(
        producer=producer,
        sneaker_id=sneaker_id,
        sneaker_size_update=sneaker_size_update,
    )
    return "Размер был изменен корректно"


@router.get(
    "/{sneaker_id}/sizes",
    dependencies=(Depends(check_role_permissions("details.sneaker.size.view")),),
)
async def get_sneaker_sizes(
    sneaker_id: int,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    return await get_sneaker_associations_service(
        session=session,
        sneaker_association_model=SneakerSizeAssociation,
        sneaker_id=sneaker_id,
    )
