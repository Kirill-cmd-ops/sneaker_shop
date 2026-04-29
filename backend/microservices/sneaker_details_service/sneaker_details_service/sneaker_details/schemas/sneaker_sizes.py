from pydantic import BaseModel, ConfigDict


class SizeQuantity(BaseModel):
    size_id: int
    quantity: int = 0


class SneakerSizesCreate(BaseModel):
    sizes: list[SizeQuantity]


class SneakerSizeUpdate(BaseModel):
    size: SizeQuantity


class SneakerSizeResponse(BaseModel):
    id: int
    sneaker_id: int
    size_id: int
    quantity: int
    is_active: bool

    model_config = ConfigDict(from_attributes=True)
