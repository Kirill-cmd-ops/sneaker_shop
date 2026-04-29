from pydantic import BaseModel, ConfigDict

from .size import SizeResponse


class SneakerSizeQuantity(BaseModel):
    size_id: int
    quantity: int = 0


class SneakerSizesCreate(BaseModel):
    sizes: list[SneakerSizeQuantity]


class SneakerSizeUpdate(BaseModel):
    size: SneakerSizeQuantity


class SneakerSizeResponse(BaseModel):
    id: int
    sneaker_id: int
    size_id: int
    quantity: int
    is_active: bool
    size: SizeResponse

    model_config = ConfigDict(from_attributes=True)