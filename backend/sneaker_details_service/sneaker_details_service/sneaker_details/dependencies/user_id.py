from fastapi import Header, HTTPException


async def get_current_user_id(
    user_id: str = Header(None, alias="X-User-Id")
) -> int | None:
    try:
        if user_id:
            return int(user_id)
        return None
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid X-User-Id Header")
