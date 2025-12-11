from pydantic import BaseModel


class SneakerAssocsDelete(BaseModel):
    assoc_ids: list[int]
