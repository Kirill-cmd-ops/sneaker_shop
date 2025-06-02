from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
import jwt
from starlette.responses import Response

from favorite_service.favorite.config import settings


class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        auth_header: str = request.headers.get("Authorization")
        if auth_header:
            scheme, _, token = auth_header.partition(" ")
            if scheme.lower() != "bearer" or not token:
                raise HTTPException(
                    status_code=401, detail="Неверная схема авторизации"
                )
            try:
                payload = jwt.decode(
                    token,
                    settings.auth_config.jwt_private_key,
                    algorithms=[settings.auth_config.algorithm],
                )
                request.state.user = payload.get("sub")
            except jwt.PyJWTError:
                raise HTTPException(
                    status_code=401, detail="Неккорректный или просроченный токен"
                )
        else:
            request.state.user = None

        response = await call_next(request)
        return response
