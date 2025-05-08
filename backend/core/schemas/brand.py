from pydantic import BaseModel, Field

class BrandRead(BaseModel):
    id: int
    name: str = Field(max_length=50)
    image_url: str = Field(max_length=200)