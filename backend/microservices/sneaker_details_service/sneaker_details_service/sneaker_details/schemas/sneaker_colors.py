from pydantic import BaseModel, ConfigDict

class SneakerColorResponse(BaseModel):
    id: int
    sneaker_id: int
    color_id: int

    model_config = ConfigDict(from_attributes=True)