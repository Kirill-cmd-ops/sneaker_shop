from pydantic import BaseModel, Field

class SizeRead(BaseModel):
    id: int
    eu_size: float = Field(ge=15, le=50)