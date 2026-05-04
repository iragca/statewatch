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
                elif asset.asset_class == AssetClass.COMMODITY:
                    scraper = ALPHAVANTAGEScraper(env.ALPHAVANTAGE_API_KEY)
                    date= datetime.now(tz=pytz.timezone(env.TIMEZONE)).date()
                    price = scraper.get_price_by_date(
                        type=AssetClass.COMMODITY,
                        ticker=asset.ticker,
                        date=date,
                    )
                    price_service.add_price(
                        asset_id=asset.id,
                        price=float(price),
                        date=date,
                    )

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
                        date=date,
                        asset_id=asset.id,
                    )
            except ValueError as e:
                if "Price record already exists" in str(e):
                    continue
                if "Price for" in str(e) and "not found" in str(e):
                    continue
                else:
                    raise e

    return {"message": "All prices updated successfully"}
