from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from sneaker_details_service.sneaker_details.config import settings
from sneaker_details_service.sneaker_details.models import db_helper, Country
from sneaker_details_service.sneaker_details.schemas.country import CountryCreate
from sneaker_details_service.sneaker_details.services.record import (
    create_record,
    delete_record,
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
async def call_create_country(
    country_create: CountryCreate, session: AsyncSession = Depends(db_helper.session_getter)
):
    async with session.begin():
        new_country = await create_record(session, Country, country_create)
        return new_country


@router.delete("/{country_id}")
async def call_delete_country(
    country_id: int,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    async with session.begin():
        result = await delete_record(session, Country, country_id)
        return result
