from fastapi import Request
from starlette.responses import JSONResponse

from microservices.cart_service.cart_service.cart.domain.exceptions import (
    CartNotFound,
    SneakerNotFound,
    SneakerSizeNotAvailable,
    SneakerNotFoundInCart,
)


async def cart_not_found_handler(request: Request, exc: CartNotFound):
    return JSONResponse(status_code=404, content={"detail": "Cart not Found"})


async def sneaker_not_found_handler(request: Request, exc: SneakerNotFound):
    return JSONResponse(status_code=404, content={"detail": "Sneaker not found"})


async def sneaker_size_not_available_handler(request: Request, exc: SneakerSizeNotAvailable):
    return JSONResponse(status_code=404, content={"detail": "Sneaker size not available"})


async def sneaker_not_found_in_cart_handler(request: Request, exc: SneakerNotFoundInCart):
    return JSONResponse(status_code=404, content={"detail": "Sneaker not found in cart"})
