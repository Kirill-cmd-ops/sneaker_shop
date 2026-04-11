from fastapi import Header


def get_current_user_role(user_role: str = Header(..., alias="X-User-Role")) -> str:
    return user_role
