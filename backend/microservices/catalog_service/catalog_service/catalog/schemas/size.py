from pydantic import BaseModel, condecimal, ConfigDict


class SizeGeneral(BaseModel):
    eu_size: condecimal(max_digits=3, decimal_places=1)


class SizeCreate(SizeGeneral): ...


class SizeResponse(SizeGeneral):
    id: int

    model_config = ConfigDict(from_attributes=True)