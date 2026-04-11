from fastapi import Request
from starlette.responses import JSONResponse

from microservices.sneaker_details_service.sneaker_details_service.sneaker_details.domain.exceptions import \
    RecordAlreadyExists, SneakerNotFound, SneakerAlreadyExists, SneakerAssociationAlreadyExists, \
    SneakerSizeAlreadyExists, SneakerSizeNotFound


def record_already_exists_handler(request: Request, exc: RecordAlreadyExists) -> JSONResponse:
    return JSONResponse(status_code=409, content={"detail": "Record already exists"})


def sneaker_not_found_handler(request: Request, exc: SneakerNotFound) -> JSONResponse:
    return JSONResponse(status_code=404, content={"detail": "Sneaker not found"})


def sneaker_already_exists_handler(request: Request, exc: SneakerAlreadyExists) -> JSONResponse:
    return JSONResponse(status_code=409, content={"detail": "Sneaker already exists"})


def sneaker_association_already_exists_handler(request: Request, exc: SneakerAssociationAlreadyExists) -> JSONResponse:
    return JSONResponse(status_code=409, content={"detail": "Sneaker association already exists"})


def sneaker_size_already_exists_handler(request: Request, exc: SneakerSizeAlreadyExists) -> JSONResponse:
    return JSONResponse(status_code=409, content={"detail": "Sneaker size already exists"})


def sneaker_size_not_found_handler(request: Request, exc: SneakerSizeNotFound) -> JSONResponse:
    return JSONResponse(status_code=404, content={"detail": "Sneaker size not found"})
