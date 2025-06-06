from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
import jwt
from starlette.responses import Response

from auth_service.auth.config import settings


class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        token = None
        auth_header: str = request.headers.get("Authorization")
        if auth_header:
            scheme, _, token_from_header = auth_header.partition(" ")
            if scheme.lower() == "bearer" and token_from_header:
                token = token_from_header

        if not token:
            token = request.cookies.get("jwt_session_cookie")

        if token:
            try:
                print(settings.auth_config.jwt_public_key)
                payload = jwt.decode(
                    token,
                    settings.auth_config.jwt_public_key,
                    algorithms=[settings.auth_config.algorithm],
                )
                request.state.user = payload.get("sub")
            except jwt.PyJWTError:
                raise HTTPException(
                    status_code=401, detail="Некорректный или просроченный токен"
                )
        else:
            request.state.user = None

        response = await call_next(request)
        return response

