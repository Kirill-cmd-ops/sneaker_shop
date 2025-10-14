from pydantic import BaseModel


class CartSneakerCreate(BaseModel):
    sneaker_id: int
    size_id: int


class CartSneakerDelete(CartSneakerCreate):
    pass

class CartSneakerQuantity(CartSneakerCreate):
    ...


class CartSneakerUpdate(BaseModel):
    sneaker_size: float
