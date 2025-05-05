from fastapi_users.authentication import CookieTransport
from core.config import settings

cookie_transport = CookieTransport(
    cookie_name=settings.cookie.cookie_name,
    cookie_max_age=settings.cookie.cookie_max_age,
    cookie_path=settings.cookie.cookie_path,
    cookie_secure=settings.cookie.cookie_secure,    # при продакшене заменить на True
    cookie_httponly=settings.cookie.cookie_httponly,
    cookie_samesite=settings.cookie.cookie_samesite,
)
