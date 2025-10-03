from fastapi import Header, HTTPException


async def get_user_role_by_header(user_role: str = Header(..., alias="X-User-Role")):
    try:
        return user_role
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid X-User-Role Header")
