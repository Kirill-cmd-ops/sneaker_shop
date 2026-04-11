from fastapi import Request
from starlette.responses import JSONResponse

from microservices.cart_service.cart_service.cart.domain.exceptions import (
    CartNotFound,
    SneakerNotFound,
    SneakerSizeNotAvailable,
    SneakerNotFoundInCart,
)


def cart_not_found_handler(request: Request, exc: CartNotFound) -> JSONResponse:
    return JSONResponse(status_code=404, content={"detail": "Cart not Found"})


def sneaker_not_found_handler(request: Request, exc: SneakerNotFound) -> JSONResponse:
    return JSONResponse(status_code=404, content={"detail": "Sneaker not found"})


def sneaker_size_not_available_handler(request: Request, exc: SneakerSizeNotAvailable) -> JSONResponse:
    return JSONResponse(status_code=409, content={"detail": "Sneaker size not available"})


def sneaker_not_found_in_cart_handler(request: Request, exc: SneakerNotFoundInCart) -> JSONResponse:
    return JSONResponse(status_code=404, content={"detail": "Sneaker not found in cart"})
