from typing import Annotated

from fastapi import Depends, HTTPException, status, Header
from .services import Key_Service


async def get_client_user(
    key_service: Key_Service,
    # Alias changed to Authorization
    auth_header: Annotated[str, Header(alias="Authorization")],
) -> str:
    if not auth_header:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization header is missing",
            headers={"WWW-Authenticate": "Bearer"},
        )

    try:
        scheme, key = auth_header.split()
        if scheme.lower() != "bearer":
            raise ValueError()
    except (ValueError, AttributeError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication scheme",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if key_service.does_key_exist(api_key=key):
        return key

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="API key is invalid",
        headers={"WWW-Authenticate": "Bearer"},
    )


AuthenticatedUser = Annotated[str, Depends(get_client_user)]
