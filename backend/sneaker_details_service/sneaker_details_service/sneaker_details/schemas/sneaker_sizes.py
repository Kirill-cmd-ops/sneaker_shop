from pydantic import BaseModel


class SizeQuantity(BaseModel):
    size_id: int
    quantity: int = 0


class SneakerSizesCreate(BaseModel):
    sneaker_id: int
    sizes: list[SizeQuantity]


class SneakerSizeUpdate(BaseModel):
    sneaker_id: int
    size: SizeQuantity


class SneakerSizesRead(SizeQuantity): ...


class SneakerSizesDelete(BaseModel):
    sneaker_id: int
    size_ids: list[int]
