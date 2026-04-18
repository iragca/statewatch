from fastapi import APIRouter, status
from statewatch.dependencies.services import Price_Service
from statewatch.schemas import price as price_schema
from typing import List

router = APIRouter(prefix="/price", tags=["Price"])


@router.get("/latest/{ticker}", status_code=status.HTTP_200_OK)
async def read_price_latest(
    ticker: str, price_service: Price_Service
) -> price_schema.Root:
    """
    Get the latest price of a stock by its ticker symbol.

    Access Level: Public
    """
    price = price_service.get_latest_price(ticker)
    return price_schema.Root.model_validate(price)


@router.get("/history/{ticker}", status_code=status.HTTP_200_OK)
async def read_price_history(
    ticker: str, price_service: Price_Service
) -> List[price_schema.Root]:
    """
    Get the price history of a stock by its ticker symbol.

    Access Level: Public
    """
    prices = price_service.get_price_history(ticker)
    return [price_schema.Root.model_validate(price) for price in prices]
