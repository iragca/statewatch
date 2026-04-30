from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import APIKeyHeader

from .services import Key_Service

api_key_header = APIKeyHeader(name="Authorization")


async def get_client_user(
    key_service: Key_Service,
    auth_header: str = Depends(api_key_header),
) -> str:
    if not auth_header:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization header is missing",
        )

    try:
        scheme, key = auth_header.split()
        if scheme.lower() != "bearer":
            raise ValueError()
    except (ValueError, AttributeError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication scheme",
        )

    if key_service.does_key_exist(api_key=key):
        return key

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="API key is invalid",
    )


AuthenticatedUser = Annotated[str, Depends(get_client_user)]
