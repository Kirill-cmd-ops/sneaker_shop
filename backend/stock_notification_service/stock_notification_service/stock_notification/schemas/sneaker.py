from typing import Optional

from pydantic import BaseModel, Field


class SneakerUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=100)
    brand_id: Optional[int] = None
    image_url: Optional[str] = Field(None, max_length=200)
    is_active: Optional[bool] = None


class SneakerCreate(BaseModel):
    name: str = Field(max_length=100)
    brand_id: int
    image_url: str = Field(max_length=200)
    is_active: bool = True
