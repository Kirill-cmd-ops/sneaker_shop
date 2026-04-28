from pydantic import BaseModel, ConfigDict, Field

from microservices.cart_service.cart_service.cart.schemas.cart_sneaker import (
    CartSneakerResponse,
)


class CartResponse(BaseModel):
    id: int
    user_id: int
    total_price: float
    items: list[CartSneakerResponse] = Field(default_factory=list)

    model_config = ConfigDict(from_attributes=True)
