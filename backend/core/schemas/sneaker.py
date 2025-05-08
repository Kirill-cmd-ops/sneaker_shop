from pydantic import BaseModel, Field

from backend.core.schemas.brand import BrandRead
from backend.core.schemas.size import SizeRead


class SneakerRead(BaseModel):
    id: int
    name: str = Field(max_length=100)
    description: str = Field(max_length=400)
    price: float = Field(gt=0)
    image_url: str = Field(max_length=200)
    is_active: bool = Field(default=True)

    brand: BrandRead
    sizes: list[SizeRead]
