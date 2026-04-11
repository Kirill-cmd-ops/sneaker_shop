from fastapi import Header, HTTPException


def get_current_user_id(user_id: str = Header(..., alias="X-User-Id")) -> int:
    return int(user_id)
