from fastapi import APIRouter, status
from fastapi.responses import FileResponse


router = APIRouter(tags=["Root"])


@router.get("/", status_code=status.HTTP_200_OK)
async def read_root():
    """
    Root endpoint.

    Access Level: Public
    """
    return "Hello, from StateWatch!"


@router.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return FileResponse("./statewatch/favicon.ico")
