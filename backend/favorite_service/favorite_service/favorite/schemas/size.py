from pydantic import BaseModel, Field

from pydantic import condecimal


class SizeCreate(BaseModel):
    eu_size: condecimal(max_digits=3, decimal_places=1)


class SizeRead(BaseModel):
    id: int
    eu_size: float = Field(ge=15, le=50)
