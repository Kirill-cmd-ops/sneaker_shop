from pydantic import BaseModel, Field


class RecordCreateMixin(BaseModel):
    name: str = Field(max_length=50)
