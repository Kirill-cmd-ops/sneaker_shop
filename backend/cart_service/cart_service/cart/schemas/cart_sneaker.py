from pydantic import BaseModel


class CartSneakerCreate(BaseModel):
    sneaker_id: int
    sneaker_size: float


class CartSneakerDelete(CartSneakerCreate):
    pass


class CartSneakerUpdate(BaseModel):
    sneaker_size: float
