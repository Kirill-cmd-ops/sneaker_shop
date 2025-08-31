from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, Field, condecimal

from catalog_service.catalog.schemas.brand import BrandRead
from catalog_service.catalog.schemas.size import SizeRead


class SneakerSizeQuantity(BaseModel):
    size_id: int
    quantity: int = 0


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


class SneakerUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=100)
    price: Optional[Decimal] = Field(None, ge=0, max_digits=10, decimal_places=2)
    brand_id: Optional[int] = None
    image_url: Optional[str] = Field(None, max_length=200)
    is_active: Optional[bool] = None
    gender: Optional[str] = None


class SneakerCreate(BaseModel):
    name: str = Field(max_length=100)
    price: condecimal(max_digits=10, decimal_places=2, gt=0)
    brand_id: int
    image_url: str = Field(max_length=200)
    is_active: bool = Field(default=True)
    gender: str = Field(default="унисекс")

    size_ids: list[SneakerSizeQuantity] = []
