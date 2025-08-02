from fastapi import Header, HTTPException


async def get_user_by_header(user_id: str = Header(..., alias="x-credential-identifier")) -> int:
    try:
        return int(user_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid x-credential-identifier header")
