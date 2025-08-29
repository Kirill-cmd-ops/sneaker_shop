from pydantic import BaseModel


class Sneaker(BaseModel):
    sneaker_id: int


class SneakerAssocsGeneral(Sneaker):
    assoc_ids: list[int]


class SneakerAssocsCreate(SneakerAssocsGeneral): ...


class SneakerAssocsDelete(SneakerAssocsGeneral): ...
