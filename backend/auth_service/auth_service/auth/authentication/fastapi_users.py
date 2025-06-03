from fastapi_users import FastAPIUsers

from auth_service.auth.authentication.backends import auth_backend
from auth_service.auth.dependencies.user_manager import get_user_manager
from auth_service.auth.models import User
from auth_service.auth.types.user_id import UserIdType

fastapi_users = FastAPIUsers[User, UserIdType](
    get_user_manager,
    [auth_backend],
)