from pydantic import BaseModel, Field, ConfigDict

from microservices.catalog_service.catalog_service.catalog.schemas.mixins import RecordCreateMixin


class BrandGeneral(RecordCreateMixin):
    image_url: str = Field(max_length=200)


class BrandCreate(BrandGeneral): ...


class BrandResponse(BaseModel):
    id: int
    name: str
    image_url: str
    
    model_config = ConfigDict(from_attributes=True)