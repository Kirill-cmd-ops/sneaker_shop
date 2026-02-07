from fastapi import Header, HTTPException


async def get_current_user_id(
        user_id: str = Header(None, alias="X-User-Id")
) -> int | None:
    if user_id:
        return int(user_id)
    return None
