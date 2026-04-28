from pydantic import BaseModel, ConfigDict


class CartSneakerGeneral(BaseModel):
    size_id: int


class CartSneakerUpdate(CartSneakerGeneral): ...


class CartSneakerCreate(CartSneakerGeneral):
    sneaker_id: int


class CartSneakerResponse(BaseModel):
    id: int
    cart_id: int
    sneaker_id: int
    size_id: int
    quantity: int

    model_config = ConfigDict(from_attributes=True)
