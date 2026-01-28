from pydantic import Field

from microservices.stock_notification_service.stock_notification_service.stock_notification.schemas.mixins.record import \
    RecordCreateMixin


class BrandGeneral(RecordCreateMixin):
    image_url: str = Field(max_length=200)


class BrandCreate(BrandGeneral): ...
