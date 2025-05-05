from .transport import cookie_transport
from .strategy import get_jwt_strategy
from fastapi_users.authentication import AuthenticationBackend


auth_backend = AuthenticationBackend(
    name="backend_jwt",
    transport=cookie_transport,
    get_strategy=get_jwt_strategy,
)