from pydantic import BaseModel


class SneakerAssocsGeneral(BaseModel):
    assoc_ids: list[int]


class SneakerAssocsCreate(SneakerAssocsGeneral): ...


class SneakerAssocsDelete(SneakerAssocsGeneral): ...
