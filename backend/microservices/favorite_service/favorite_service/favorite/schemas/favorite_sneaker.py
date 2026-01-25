from pydantic import BaseModel


class FavoriteSneakerGeneral(BaseModel):
    size_id: int


class FavoriteSneakerUpdate(FavoriteSneakerGeneral): ...


class FavoriteSneakerCreate(FavoriteSneakerGeneral):
    sneaker_id: int
