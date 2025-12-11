from pydantic import BaseModel


class SubscriptionCreate(BaseModel):
    sneaker_id: int
    size_id: int