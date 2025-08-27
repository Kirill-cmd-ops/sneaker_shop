from pydantic import BaseModel, Field, condecimal


class SneakerCreate(BaseModel):
    name: str = Field(max_length=100)
    description: str = Field(max_length=400)
    price: condecimal(max_digits=10, decimal_places=2, gt=0)
    brand_id: int
    country_id: int
    image_url: str = Field(max_length=200)
    is_active: bool = Field(default=True)
    gender: str = Field(default="унисекс")

    size_ids: list[int] = []
    color_ids: list[int] = []
    material_ids: list[int] = []
