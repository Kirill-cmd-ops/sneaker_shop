from auth_service.auth.authentication.transport import cookie_transport
from auth_service.auth.authentication.custom_strategy import get_jwt_strategy

from fastapi_users.authentication import AuthenticationBackend


auth_backend = AuthenticationBackend(
    name="backend_jwt",
    transport=cookie_transport,
    get_strategy=get_jwt_strategy,
)
