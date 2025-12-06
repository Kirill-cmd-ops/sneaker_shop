from typing import Optional

from pydantic import Field

from pydantic import BaseModel

from sneaker_details_service.sneaker_details.schemas.mixins.record import RecordCreateMixin


class BrandCreate(RecordCreateMixin):
    image_url: str = Field(max_length=200)

class BrandUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=50)
    image_url: Optional[str] = Field(None, max_length=200)