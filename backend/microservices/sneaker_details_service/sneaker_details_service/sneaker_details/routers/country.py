from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeBase

from microservices.sneaker_details_service.sneaker_details_service.sneaker_details.config import settings
from microservices.sneaker_details_service.sneaker_details_service.sneaker_details.models import db_helper, Country
from microservices.sneaker_details_service.sneaker_details_service.sneaker_details.schemas.country import CountryCreate
from microservices.sneaker_details_service.sneaker_details_service.sneaker_details.services.record.create import (
    create_record_service,
)
from microservices.sneaker_details_service.sneaker_details_service.sneaker_details.services.record.delete import (
    delete_record_service,
)

router = APIRouter(
    prefix=settings.api.build_path(
        settings.api.root,
        settings.api.v1.prefix,
        settings.api.v1.countries,
    ),
    tags=["Country"],
)


@router.post("/")
async def create_country(
        country_create: CountryCreate,
        session: AsyncSession = Depends(db_helper.session_getter),
) -> DeclarativeBase:
    country_data = country_create.model_dump()

    return await create_record_service(
        session=session,
        table_name=Country,
        data=country_data,
    )


@router.delete("/{country_id}")
async def delete_country(
        country_id: int,
        session: AsyncSession = Depends(db_helper.session_getter),
) -> dict[str, str]:
    return await delete_record_service(
        session=session,
        table_name=Country,
        record_id=country_id,
    )
