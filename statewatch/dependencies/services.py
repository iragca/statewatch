from statewatch import services
from typing import Annotated

from .db import DB_Session
from fastapi import Depends


def get_asset_service(
    db_session: DB_Session,
) -> services.AssetService:
    return services.AssetService(db_session)


def get_key_service(
    db_session: DB_Session,
) -> services.KeyService:
    return services.KeyService(db_session)


def get_price_service(
    db_session: DB_Session,
) -> services.PriceService:
    return services.PriceService(db_session)


def get_task_service(
    db_session: DB_Session,
) -> services.TaskService:
    return services.TaskService(db_session)


Asset_Service = Annotated[services.AssetService, Depends(get_asset_service)]
Key_Service = Annotated[services.KeyService, Depends(get_key_service)]
Price_Service = Annotated[services.PriceService, Depends(get_price_service)]
Task_Service = Annotated[services.TaskService, Depends(get_task_service)]
