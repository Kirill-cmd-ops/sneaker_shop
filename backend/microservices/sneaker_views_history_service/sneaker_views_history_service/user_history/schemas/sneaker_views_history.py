from datetime import datetime

from pydantic import BaseModel, ConfigDict


class SneakerViewsHistoryResponse(BaseModel):
    user_id: int
    sneaker_id: int
    view_timestamp: datetime
    sign: int
    version: int

    model_config = ConfigDict(from_attributes=True)
