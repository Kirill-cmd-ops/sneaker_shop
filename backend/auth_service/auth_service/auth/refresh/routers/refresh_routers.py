import secrets

from fastapi import APIRouter
from fastapi.params import Depends, Cookie
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import Response

from auth_service.auth.config import settings

from auth_service.auth.models import db_helper
from auth_service.auth.refresh.services.orchestrators import (
    update_refresh_token_orchestrator,
)

refresh_router = APIRouter(
    prefix=settings.api.build_path(
        settings.api.root,
        settings.api.v1.prefix,
        settings.api.v1.refresh,
    ),
    tags=["Refresh Token"],
)


@refresh_router.post("/")
async def update_refresh_token(
    response: Response,
    token_aud: list[str],
    session: AsyncSession = Depends(db_helper.session_getter),
    refresh_token: str = Cookie(alias="refresh_session_cookie"),
):
    return await update_refresh_token_orchestrator(
        session=session,
        response=response,
        token_aud=token_aud,
        refresh_token=refresh_token,
    )
