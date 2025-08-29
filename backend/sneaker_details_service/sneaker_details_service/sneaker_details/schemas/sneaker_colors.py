from pydantic import BaseModel


class SneakerColorsRead(BaseModel):
    color_id: int