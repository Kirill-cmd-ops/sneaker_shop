from pydantic import BaseModel


class SizeQuantity(BaseModel):
    size_id: int
    quantity: int = 0


class SneakerSizesCreate(BaseModel):
    sizes: list[SizeQuantity]


class SneakerSizeUpdate(BaseModel):
    size: SizeQuantity
