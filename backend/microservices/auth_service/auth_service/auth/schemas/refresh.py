from pydantic import BaseModel, Field


class RefreshSessionResponse(BaseModel):
    refresh_token: str
