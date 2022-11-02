from fastapi import Header
from apps.extensions.depends_exc import TokenAuthError,TokenExpired


async def token_dep(token: str = Header(..., )):
    if token =="1":
        raise TokenExpired()
    elif token =="2":
        raise TokenAuthError()
    else:
        return {"name":"1234"}
