from fastapi import APIRouter
from fastapi_users import FastAPIUsers, schemas

from auth_service.auth.authentication.custom_register_router import get_register_router_custom


class FastAPIUsersCustom(FastAPIUsers):
    def get_register_router(
        self, user_schema: type[schemas.U], user_create_schema: type[schemas.UC]
    ) -> APIRouter:
        return get_register_router_custom(
            self.get_user_manager, user_schema, user_create_schema
        )
