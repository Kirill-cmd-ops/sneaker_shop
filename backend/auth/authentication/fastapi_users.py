from fastapi_users import FastAPIUsers

from backend.auth.authentication.backends import auth_backend
from backend.auth.dependencies.user_manager import get_user_manager
from backend.auth.models import User
from backend.auth.types.user_id import UserIdType

fastapi_users = FastAPIUsers[User, UserIdType](
    get_user_manager,
    [auth_backend],
)