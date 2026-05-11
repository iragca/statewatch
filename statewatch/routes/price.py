from typing import List

from fastapi import APIRouter, status
from fastapi.responses import Response

from statewatch.dependencies.services import Price_Service
from statewatch.formats import CSV
from statewatch.schemas import price as price_schema

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


@router.get(
    "/history/{ticker}",
    status_code=status.HTTP_200_OK,
    response_model=List[price_schema.Root],
    responses={
        200: {"content:": {"text/csv": {}}},
    },
)
async def read_price_history(
    ticker: str, price_service: Price_Service, csv: bool = False
):
    """
    Get the price history of a stock by its ticker symbol.

    Access Level: Public
    """
    prices = price_service.get_price_history(ticker)

    if csv:
        return Response(
            content=str(CSV.from_price_list(prices)),
            media_type="text/csv",
            headers={
                "Content-Disposition": f"attachment; filename={ticker}_price_history.csv"
            },
        )

    return [price_schema.Root.model_validate(price) for price in prices]
