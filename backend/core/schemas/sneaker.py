from pydantic import BaseModel, Field

from backend.core.schemas.brand import BrandRead
from backend.core.schemas.size import SizeRead


class SneakerStandard(BaseModel):
    id: int
    name: str = Field(max_length=100)
    description: str = Field(max_length=400)
    price: float = Field(gt=0)
    gender: str = Field(max_length=10, default="Унисекс")
    image_url: str = Field(max_length=200)
    is_active: bool = Field(default=True)


class SneakerOut(SneakerStandard):
    pass

class SneakerRead(SneakerStandard):
    brand: BrandRead
    sizes: list[SizeRead]
