from datetime import datetime, timedelta

import pytz
from fastapi import APIRouter

from statewatch.core.config import env
from statewatch.dependencies.auth import AuthenticatedUser
from statewatch.dependencies.services import Asset_Service, Price_Service
from statewatch.schemas.enums import AssetClass
from statewatch.scrapers import ALPHAVANTAGEScraper

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.get("/update/{ticker}")
async def update_price(
    ticker: str,
    type: AssetClass,
    price_service: Price_Service,
    asset_service: Asset_Service,
    _: AuthenticatedUser,
):
    """
    Update the price of a cryptocurrency by its ticker symbol.

    Access Level: Authenticated users only.
    """
    delay = timedelta(days=1)
    asset = asset_service.get_asset_by_ticker(ticker)
    scraper = ALPHAVANTAGEScraper(ALPHAVANTAGE_API_KEY=env.ALPHAVANTAGE_API_KEY)

    delay_date = datetime.now(tz=pytz.timezone(env.TIMEZONE)).date() - delay
    price_data = scraper.get_price_by_date(type, ticker, delay_date)
    price_service.add_price(price=float(price_data), date=delay_date, asset_id=asset.id)
    return {"message": f"Price for {ticker} updated successfully"}
