from datetime import datetime, timedelta

import pytz
from fastapi import APIRouter

from statewatch.core.config import env
from statewatch.dependencies.auth import AuthenticatedUser
from statewatch.dependencies.db import DB_Session
from statewatch.schemas.enums import AssetClass
from statewatch.scrapers import (
    ALPHAVANTAGEScraper,
    CryptocurrencyScraper,
    YFinanceScraper,
)
from statewatch.services import AssetService, PriceService, TransactionOrchestrator
from time import sleep

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.get("/update_all")
async def update_all_prices(
    DB_session: DB_Session,
    _: AuthenticatedUser,
):
    """
    Update the prices of all cryptocurrencies in the database.

    Access Level: Authenticated users only.
    """
    with TransactionOrchestrator(DB_session) as transaction:
        asset_service = AssetService(transaction.session)
        price_service = PriceService(transaction.session)

        assets = asset_service.get_all_assets()

        for asset in assets:
            try:
                print(f"Updating price for {asset.name} ({asset.ticker})")
                if asset.asset_class == AssetClass.CRYPTOCURRENCY:
                    scraper = CryptocurrencyScraper(env.COINGECKO_DEMO_API_KEY)
                    date = datetime.now(tz=pytz.timezone(env.TIMEZONE)).date()

                    price = await scraper.get_price_by_date(
                        name=asset.name.lower(),
                        date=date,
                    )
                    price_service.add_price(
                        price=float(price),
                        date=date,
                        asset_id=asset.id,
                    )
                    print(f"Price for {asset.name} on {date} updated successfully: {price}")
                elif asset.asset_class == AssetClass.COMMODITY:
                    scraper = ALPHAVANTAGEScraper(env.ALPHAVANTAGE_API_KEY)
                    date = datetime.now(tz=pytz.timezone(env.TIMEZONE)).date()
                    delay = timedelta(days=1)
                    delayed_date = date - delay
                    price = scraper.get_price_by_date(
                        type=AssetClass.COMMODITY,
                        ticker=asset.ticker,
                        date=delayed_date,
                    )
                    price_service.add_price(
                        asset_id=asset.id,
                        price=float(price),
                        date=delayed_date,
                    )
                    print(f"Price for {asset.name} on {date} updated successfully: {price}")
                else:
                    scraper = YFinanceScraper()
                    delay = timedelta(days=2)
                    date = datetime.now(tz=pytz.timezone(env.TIMEZONE)).date()
                    delayed_date = date - delay
                    price = scraper.get_price_by_date(
                        ticker=asset.ticker, date=delayed_date
                    )
                    price_service.add_price(
                        price=float(price),
                        date=delayed_date,
                        asset_id=asset.id,
                    )
                    print(f"Price for {asset.name} on {delayed_date} updated successfully: {price}")
            except ValueError as e:
                if "Price record already exists" in str(e):
                    print(f"Price for {asset.name} on {date} already exists. Skipping.")
                    continue
                if "Price for" in str(e) and "not found" in str(e):
                    print(f"Price for {asset.name} on {date} not found. Skipping.")
                    continue
                else:
                    print(f"Error updating price for {asset.name} on {date}: {e}")
                    raise e

            sleep(1)

    return {"message": "All prices updated successfully"}
