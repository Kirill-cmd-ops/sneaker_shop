from pydantic import BaseModel


class SneakerMaterialsRead(BaseModel):
    material_id: int