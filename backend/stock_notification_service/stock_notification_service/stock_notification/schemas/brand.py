from typing import Optional

from pydantic import Field

from pydantic import BaseModel

from stock_notification_service.stock_notification.schemas.mixins.record import RecordCreateMixin


class BrandCreate(RecordCreateMixin):
    image_url: str = Field(max_length=200)

class BrandUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=50)
    image_url: Optional[str] = Field(None, max_length=200)

class BrandRead(BaseModel):
    id: int
    name: str = Field(max_length=50)
    image_url: str = Field(max_length=200)