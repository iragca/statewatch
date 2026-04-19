from datetime import datetime, timedelta

import pytz
from fastapi import APIRouter

from statewatch.core.config import env
from statewatch.dependencies.auth import AuthenticatedUser
from statewatch.dependencies.services import Asset_Service, Price_Service
from statewatch.scrapers import YFinanceScraper

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.get("/update/{ticker}")
async def update_price(
    ticker: str,
    price_service: Price_Service,
    asset_service: Asset_Service,
    _: AuthenticatedUser,
):
    """
    Update the price of a cryptocurrency by its ticker symbol.

    Access Level: Authenticated users only.
    """
    delay = timedelta(days=2)
    asset = asset_service.get_asset_by_ticker(ticker)
    scraper = YFinanceScraper()

    delay_date = datetime.now(tz=pytz.timezone(env.TIMEZONE)).date() - delay
    price_data = scraper.get_price_by_date(ticker, delay_date)
    price_service.add_price(price=float(price_data), date=delay_date, asset_id=asset.id)
    return {"message": f"Price for {ticker} updated successfully"}
