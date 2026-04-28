from pydantic import BaseModel, ConfigDict


class FavoriteSneakerGeneral(BaseModel):
    size_id: int


class FavoriteSneakerUpdate(FavoriteSneakerGeneral): ...


class FavoriteSneakerCreate(FavoriteSneakerGeneral):
    sneaker_id: int


class FavoriteSneakerResponse(BaseModel):
    id: int
    favorite_id: int
    sneaker_id: int
    size_id: int

    model_config = ConfigDict(from_attributes=True)
