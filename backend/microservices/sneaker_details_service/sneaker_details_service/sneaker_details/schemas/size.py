from pydantic import condecimal

from pydantic import BaseModel


class SizeCreate(BaseModel):
    eu_size: condecimal(max_digits=3, decimal_places=1)
