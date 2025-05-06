from fastapi_users import FastAPIUsers

from core.authentication.backends import auth_backend
from core.dependencies.user_manager import get_user_manager
from core.models import User
from core.types.user_id import UserIdType

fastapi_users = FastAPIUsers[User, UserIdType](
    get_user_manager,
    [auth_backend],
)