from pydantic import BaseModel

from pydantic import condecimal


class SizeCreate(BaseModel):
    eu_size: condecimal(max_digits=3, decimal_places=1)
