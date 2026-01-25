from pydantic import Field

from catalog_service.catalog.schemas.mixins.record import RecordCreateMixin


class BrandGeneral(RecordCreateMixin):
    image_url: str = Field(max_length=200)


class BrandCreate(BrandGeneral): ...
