from datetime import datetime, timedelta

from fastapi import APIRouter

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
    asset = asset_service.get_asset_by_ticker(ticker)
    scraper = YFinanceScraper()

    yesterdays_date = datetime.now().date() - timedelta(days=1)
    price_data = scraper.get_price_by_date(ticker, yesterdays_date)
    price_service.add_price(price=float(price_data), date=yesterdays_date, asset_id=asset.id)
    return {"message": f"Price for {ticker} updated successfully"}
