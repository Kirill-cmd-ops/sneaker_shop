from fastapi import Request
from starlette.responses import JSONResponse

from microservices.favorite_service.favorite_service.favorite.domain.exceptions import FavoriteNotFound, \
    SneakerNotFound, SneakerSizeNotAvailable, SneakerNotFoundInFavorite


async def favorite_not_found_handler(request: Request, exc: FavoriteNotFound):
    return JSONResponse(status_code=404, content={"detail": "Favorite not found"})


async def sneaker_not_found_handler(request: Request, exc: SneakerNotFound):
    return JSONResponse(status_code=404, content={"detail": "Sneaker not found"})


async def sneaker_size_not_available_handler(request: Request, exc: SneakerSizeNotAvailable):
    return JSONResponse(status_code=409, content={"detail": "Sneaker size not available"})


async def sneaker_not_found_in_favorite_handler(request: Request, exc: SneakerNotFoundInFavorite):
    return JSONResponse(status_code=404, content={"detail": "Sneaker not found in favorite"})
