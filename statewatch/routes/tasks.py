from datetime import datetime, timedelta

import pytz
from fastapi import APIRouter

from statewatch.core.config import env
from statewatch.dependencies.auth import AuthenticatedUser
from statewatch.dependencies.db import DB_Session
from statewatch.dependencies.services import Asset_Service, Price_Service
from statewatch.schemas.enums import AssetClass
from statewatch.scrapers import (
    ALPHAVANTAGEScraper,
    CryptocurrencyScraper,
    YFinanceScraper,
)
from statewatch.services import AssetService, PriceService, TransactionOrchestrator

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


@router.get("/add/{ticker}")
async def add_price(
    ticker: str,
    type: AssetClass,
    DB_session: DB_Session,
    _: AuthenticatedUser,
):
    """
    Add a new asset  by its ticker symbol.

    Access Level: Authenticated users only.
    """
    with TransactionOrchestrator(DB_session) as transaction:
        asset_service = AssetService(transaction.session)
        price_service = PriceService(transaction.session)

        scraper = ALPHAVANTAGEScraper(ALPHAVANTAGE_API_KEY=env.ALPHAVANTAGE_API_KEY)
        asset_data = scraper.get_asset_metadata(type, ticker)
        asset = asset_service.create_asset(
            ticker=ticker,
            name=asset_data["3. Digital Currency Name"],
            asset_class=type,
        )
        transaction.session.flush()  # Ensure asset.id is available before adding prices

        price_history = scraper.get_price_history(type, ticker)

        for date, price in price_history.itertuples(index=False):
            price_service.add_price(price=float(price), date=date, asset_id=asset.id)

    return {"message": f"Asset {ticker} and its price history added successfully"}


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
            if asset.asset_class == AssetClass.CRYPTOCURRENCY:
                scraper = CryptocurrencyScraper(env.COINGECKO_DEMO_API_KEY)

                price = await scraper.get_price_by_date(
                    name=asset.name.lower(), date=datetime.now(tz=pytz.timezone(env.TIMEZONE))
                )

                try:
                    price_service.add_price(
                        price=float(price),
                        date=datetime.now(tz=pytz.timezone(env.TIMEZONE)).date(),
                        asset_id=asset.id,
                    )
                except Exception:
                    continue
            else:
                scraper = YFinanceScraper()
                delay = timedelta(days=2)
                date = datetime.now(tz=pytz.timezone(env.TIMEZONE)).date()
                delayed_date = datetime.now(tz=pytz.timezone(env.TIMEZONE)).date() - delay
                price = scraper.get_price_by_date(ticker=asset.ticker, date=delayed_date)

                try:
                    price_service.add_price(
                        price=float(price),
                        date=date,
                        asset_id=asset.id,
                    )
                except Exception:
                    continue

    return {"message": "All prices updated successfully"}
