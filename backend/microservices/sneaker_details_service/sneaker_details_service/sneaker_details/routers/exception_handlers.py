from fastapi import Request
from starlette.responses import JSONResponse

from microservices.sneaker_details_service.sneaker_details_service.sneaker_details.domain.exceptions import \
    RecordAlreadyExists, SneakerNotFound, SneakerAlreadyExists, SneakerAssociationAlreadyExists, \
    SneakerSizeAlreadyExists, SneakerSizeNotFound


async def record_already_exists_handler(request: Request, exc: RecordAlreadyExists):
    return JSONResponse(status_code=409, content={"detail": "Record already exists"})


async def sneaker_not_found_handler(request: Request, exc: SneakerNotFound):
    return JSONResponse(status_code=404, content={"detail": "Sneaker not found"})


async def sneaker_already_exists_handler(request: Request, exc: SneakerAlreadyExists):
    return JSONResponse(status_code=409, content={"detail": "Sneaker already exists"})


async def sneaker_association_already_exists_handler(request: Request, exc: SneakerAssociationAlreadyExists):
    return JSONResponse(status_code=409, content={"detail": "Sneaker association already exists"})


async def sneaker_size_already_exists_handler(request: Request, exc: SneakerSizeAlreadyExists):
    return JSONResponse(status_code=409, content={"detail": "Sneaker size already exists"})


async def sneaker_size_not_found_handler(request: Request, exc: SneakerSizeNotFound):
    return JSONResponse(status_code=404, content={"detail": "Sneaker size not found"})
