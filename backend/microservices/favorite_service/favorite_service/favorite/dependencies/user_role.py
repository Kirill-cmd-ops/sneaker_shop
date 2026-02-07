from fastapi import Header, HTTPException


async def get_current_user_role(user_role: str = Header(..., alias="X-User-Role")):
    return user_role
