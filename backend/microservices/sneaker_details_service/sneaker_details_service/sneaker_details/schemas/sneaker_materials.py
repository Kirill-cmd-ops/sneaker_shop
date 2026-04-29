from pydantic import BaseModel, ConfigDict

class SneakerMaterialResponse(BaseModel):
    id: int
    sneaker_id: int
    material_id: int

    model_config = ConfigDict(from_attributes=True)