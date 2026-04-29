from pydantic import BaseModel, ConfigDict, Field

from microservices.sneaker_details_service.sneaker_details_service.sneaker_details.schemas.mixins.record import (
    RecordCreateMixin,
)


class BrandGeneral(RecordCreateMixin):
    image_url: str = Field(max_length=200)


class BrandCreate(BrandGeneral): ...


class BrandResponse(BaseModel):
    id: int
    name: str
    image_url: str

    model_config = ConfigDict(from_attributes=True)
