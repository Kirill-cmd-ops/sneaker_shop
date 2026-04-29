from pydantic import BaseModel, ConfigDict

from microservices.sneaker_details_service.sneaker_details_service.sneaker_details.schemas.mixins.record import (
    RecordCreateMixin,
)


class ColorCreate(RecordCreateMixin):
    ...


class ColorResponse(BaseModel):
    id: int
    name: str

    model_config = ConfigDict(from_attributes=True)
