from starlette.responses import JSONResponse

from fastapi import Request

from microservices.stock_notification_service.stock_notification_service.stock_notification.domain.exceptions import \
    SneakerNotFound, SneakerAlreadyExists, SneakerIsInactive, OneTimeSubscriptionIsActive, \
    OneTimeSubscriptionAlreadyExists, OneTimeSubscriptionNotFound, PermanentSubscriptionIsActive, \
    PermanentSubscriptionAlreadyExists, PermanentSubscriptionNotFound


async def sneaker_not_found_handler(request: Request, exc: SneakerNotFound):
    return JSONResponse(status_code=404, content={"detail": "Sneaker not found"})


async def sneaker_already_exists_handler(request: Request, exc: SneakerAlreadyExists):
    return JSONResponse(status_code=409, content={"detail": "Sneaker already exists"})


async def sneaker_is_inactive_handler(request: Request, exc: SneakerIsInactive):
    return JSONResponse(status_code=409, content={"detail": "Sneaker is inactive"})


async def one_time_subscription_is_active_handler(request: Request, exc: OneTimeSubscriptionIsActive):
    return JSONResponse(status_code=409, content={"detail": "One time subscription is active"})


async def one_time_subscription_already_exists_handler(request: Request, exc: OneTimeSubscriptionAlreadyExists):
    return JSONResponse(status_code=409, content={"detail": "One time subscription already exists"})


async def one_time_subscription_not_found_handler(request: Request, exc: OneTimeSubscriptionNotFound):
    return JSONResponse(status_code=404, content={"detail": "One time subscription not found"})


async def permanent_subscription_is_active_handler(request: Request, exc: PermanentSubscriptionIsActive):
    return JSONResponse(status_code=409, content={"detail": "Permanent subscription is active"})


async def permanent_subscription_already_exists_handler(request: Request, exc: PermanentSubscriptionAlreadyExists):
    return JSONResponse(status_code=409, content={"detail": "Permanent subscription already exists"})


async def permanent_subscription_not_found_handler(request: Request, exc: PermanentSubscriptionNotFound):
    return JSONResponse(status_code=404, content={"detail": "Permanent subscription not found"})
