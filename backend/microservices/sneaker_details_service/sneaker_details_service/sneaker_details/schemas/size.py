from pydantic import BaseModel, ConfigDict, condecimal


class SizeCreate(BaseModel):
    eu_size: condecimal(max_digits=3, decimal_places=1)


class SizeResponse(BaseModel):
    id: int
    eu_size: float

    model_config = ConfigDict(from_attributes=True)
