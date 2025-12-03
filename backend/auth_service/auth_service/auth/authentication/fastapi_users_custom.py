from fastapi import APIRouter
from fastapi_users import FastAPIUsers, schemas

from auth_service.auth.authentication.custom_register_router import get_register_router_custom
from auth_service.auth.authentication.custom_reset_router import get_reset_password_router_custom
from auth_service.auth.authentication.custom_users_router import get_users_router_custom
from auth_service.auth.authentication.custom_verify_router import get_verify_router_custom


class FastAPIUsersCustom(FastAPIUsers):
    def get_register_router(
        self, user_schema: type[schemas.U], user_create_schema: type[schemas.UC]
    ) -> APIRouter:
        return get_register_router_custom(
            self.get_user_manager, user_schema, user_create_schema
        )

    def get_verify_router(self, user_schema: type[schemas.U]) -> APIRouter:
        return get_verify_router_custom(self.get_user_manager, user_schema)

    def get_reset_password_router(self) -> APIRouter:
        return get_reset_password_router_custom(self.get_user_manager)

    def get_users_router(
        self,
        user_schema: type[schemas.U],
        user_update_schema: type[schemas.UU],
        requires_verification: bool = False,
    ) -> APIRouter:
        return get_users_router_custom(
            self.get_user_manager,
            user_schema,
            user_update_schema,
            self.authenticator,
            requires_verification,
        )
