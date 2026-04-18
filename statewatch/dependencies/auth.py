from typing import Annotated

from fastapi import Depends, HTTPException, status, Header
from .services import Key_Service


async def get_client_user(
    key_service: Key_Service,
    key: Annotated[str, Header(alias="Api-Key")],
) -> str:
    if not key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API key is missing",
            headers={"WWW-Authenticate": "Api-Key"},
        )

    if key_service.does_key_exist(api_key=key):
        return key

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="API key is invalid",
        headers={"WWW-Authenticate": "Api-Key"},
    )


AuthenticatedUser = Annotated[str, Depends(get_client_user)]
