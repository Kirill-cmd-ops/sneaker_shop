from pydantic import BaseModel


class SizeQuantity(BaseModel):
    size_id: int
    quantity: int = 0


class Sneaker(BaseModel):
    sneaker_id: int


class SneakerSizesCreate(Sneaker):
    sizes: list[SizeQuantity]


class SneakerSizeUpdate(Sneaker):
    size: SizeQuantity


class SneakerSizesRead(SizeQuantity): ...
