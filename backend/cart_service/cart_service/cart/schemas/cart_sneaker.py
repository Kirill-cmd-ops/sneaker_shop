from pydantic import BaseModel


class CartSneakerGeneral(BaseModel):
    size_id: int


class CartSneakerUpdate(CartSneakerGeneral): ...


class CartSneakerCreate(CartSneakerGeneral):
    sneaker_id: int
