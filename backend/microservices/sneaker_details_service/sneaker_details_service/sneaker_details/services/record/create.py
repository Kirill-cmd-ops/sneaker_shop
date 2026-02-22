from typing import Callable, Dict, Any

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeBase

from microservices.sneaker_details_service.sneaker_details_service.sneaker_details.domain.exceptions import \
    RecordAlreadyExists


async def create_record_service(
        session: AsyncSession,
        table_name: Callable,
        data: Dict[str, Any],
) -> DeclarativeBase:
    try:
        async with session.begin():
            new_record = table_name(**data)
            session.add(new_record)
        return new_record
    except IntegrityError:
        raise RecordAlreadyExists()
