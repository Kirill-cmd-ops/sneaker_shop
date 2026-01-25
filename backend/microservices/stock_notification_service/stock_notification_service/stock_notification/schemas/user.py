from typing import Optional

from pydantic import BaseModel, Field


class UserUpdate(BaseModel):
    email: Optional[str] = Field(None, max_length=320)
    is_active: Optional[bool] = None
    is_verified: Optional[bool] = None


class UserCreate(BaseModel):
    email: str = Field(max_length=320)
    is_active: bool = True
    is_verified: bool = False
