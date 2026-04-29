from pydantic import BaseModel, ConfigDict

from microservices.stock_notification_service.stock_notification_service.stock_notification.enums import SubscriptionStatus


class SubscriptionCreate(BaseModel):
    sneaker_id: int
    size_id: int


class UserSneakerOneTimeSubscriptionResponse(BaseModel):
    id: int
    user_id: int
    sneaker_id: int
    size_id: int
    is_sent: bool
    status: SubscriptionStatus

    model_config = ConfigDict(from_attributes=True)


class UserSneakerPermanentSubscriptionResponse(BaseModel):
    id: int
    user_id: int
    sneaker_id: int
    size_id: int
    status: SubscriptionStatus

    model_config = ConfigDict(from_attributes=True)
