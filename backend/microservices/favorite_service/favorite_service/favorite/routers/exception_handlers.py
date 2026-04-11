from fastapi import Request
from starlette.responses import JSONResponse

from microservices.favorite_service.favorite_service.favorite.domain.exceptions import FavoriteNotFound, \
    SneakerNotFound, SneakerSizeNotAvailable, SneakerNotFoundInFavorite


def favorite_not_found_handler(request: Request, exc: FavoriteNotFound) -> JSONResponse:
    return JSONResponse(status_code=404, content={"detail": "Favorite not found"})


def sneaker_not_found_handler(request: Request, exc: SneakerNotFound) -> JSONResponse:
    return JSONResponse(status_code=404, content={"detail": "Sneaker not found"})


def sneaker_size_not_available_handler(request: Request, exc: SneakerSizeNotAvailable) -> JSONResponse:
    return JSONResponse(status_code=409, content={"detail": "Sneaker size not available"})


def sneaker_not_found_in_favorite_handler(request: Request, exc: SneakerNotFoundInFavorite) -> JSONResponse:
    return JSONResponse(status_code=404, content={"detail": "Sneaker not found in favorite"})
