from pydantic import BaseModel

class FavoriteSneakerCreate(BaseModel):
    sneaker_id: int
    sneaker_size: float

