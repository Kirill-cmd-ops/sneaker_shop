from fastapi import Request

from starlette.responses import JSONResponse

from microservices.auth_service.auth_service.auth.domain.exceptions import RoleNotFound, UserNotFound, UserRoleAssociationAlreadyExists, \
    BlacklistAlreadyExists


async def role_not_found_handler(request: Request, exc:RoleNotFound):
    return JSONResponse(status_code=404, content="details: Role not found")


async def user_not_found_handler(request: Request, exc:UserNotFound):
    return JSONResponse(status_code=404, content="details: User not found")


async def user_role_association_already_exists_handler(request: Request, exc:UserRoleAssociationAlreadyExists):
    return JSONResponse(status_code=409, content="details: User role association already exists")


async def blacklist_already_exists_handler(request: Request, exc:BlacklistAlreadyExists):
    return JSONResponse(status_code=409, content="details: Blacklist already exists")
