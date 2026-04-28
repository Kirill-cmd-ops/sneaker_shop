from pydantic import BaseModel, ConfigDict, Field

from microservices.favorite_service.favorite_service.favorite.schemas.favorite_sneaker import (
    FavoriteSneakerResponse,
)


class FavoriteResponse(BaseModel):
    id: int
    user_id: int
    sneaker_associations: list[FavoriteSneakerResponse] = Field(default_factory=list)

    model_config = ConfigDict(from_attributes=True)
