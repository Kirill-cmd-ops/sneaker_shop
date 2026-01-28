from pydantic import Field

from microservices.favorite_service.favorite_service.favorite.schemas.mixins.record import RecordCreateMixin


class BrandGeneral(RecordCreateMixin):
    image_url: str = Field(max_length=200)


class BrandCreate(BrandGeneral): ...
