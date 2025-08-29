from pydantic import BaseModel


class SneakerAssocsCreate(BaseModel):
    sneaker_id: int
    assoc_ids: list[int]