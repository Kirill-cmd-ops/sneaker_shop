from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from sneaker_details_service.sneaker_details.models import db_helper, Country
from sneaker_details_service.sneaker_details.schemas.country import CountryCreate
from sneaker_details_service.sneaker_details.services.record import (
    create_record,
    delete_record,
)

router = APIRouter()

@router.post("/create_country/")
async def call_create_country(
    country_create: CountryCreate, session: AsyncSession = Depends(db_helper.session_getter)
):
    new_country = await create_record(session, Country, country_create)
    return new_country


@router.delete("/delete_country/")
async def call_delete_country(
    country_id: int,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    result = await delete_record(session, Country, country_id)
    return result
