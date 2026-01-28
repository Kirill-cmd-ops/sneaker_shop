from pydantic import BaseModel, condecimal


class SizeCreate(BaseModel):
    eu_size: condecimal(max_digits=3, decimal_places=1)
