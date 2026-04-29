from pydantic import BaseModel, ConfigDict

from microservices.sneaker_details_service.sneaker_details_service.sneaker_details.schemas.mixins.record import (
    RecordCreateMixin,
)


class MaterialCreate(RecordCreateMixin):
    ...


class MaterialResponse(BaseModel):
    id: int
    name: str

    model_config = ConfigDict(from_attributes=True)
