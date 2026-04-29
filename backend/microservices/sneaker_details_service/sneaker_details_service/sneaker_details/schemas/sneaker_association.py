from pydantic import BaseModel, ConfigDict


class SneakerAssocsGeneral(BaseModel):
    assoc_ids: list[int]


class SneakerAssocsCreate(SneakerAssocsGeneral): ...
