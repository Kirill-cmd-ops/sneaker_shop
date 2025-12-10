from pydantic import Field

from sneaker_details_service.sneaker_details.schemas.mixins.record import RecordCreateMixin


class BrandGeneral(RecordCreateMixin):
    image_url: str = Field(max_length=200)


class BrandCreate(BrandGeneral): ...
