from pydantic import Field

from microservices.catalog_service.catalog_service.catalog.schemas.mixins.record import RecordCreateMixin


class BrandGeneral(RecordCreateMixin):
    image_url: str = Field(max_length=200)


class BrandCreate(BrandGeneral): ...
