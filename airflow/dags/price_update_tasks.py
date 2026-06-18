import os
from datetime import date, timedelta

import requests
from airflow.sdk import task, get_current_context

from statewatch.core.config import env
from statewatch.schemas.enums import AssetClass, Currency
from statewatch.scrapers import (
    ALPHAVANTAGEScraper,
    BPIScraper,
    CryptocurrencyScraper,
    YFinanceScraper,
)

STATEWATCH_API_BASE_URL = os.environ["STATEWATCH_API_BASE_URL"]
STATEWATCH_API_KEY = os.environ["STATEWATCH_API_KEY"]


def _post_price(ticker: str, price: float, dt: date, currency: Currency = Currency.USD):
    url = f"{STATEWATCH_API_BASE_URL}/price/add"
    headers = {"Authorization": f"Bearer {STATEWATCH_API_KEY}"}
    body = {"ticker": ticker, "price": price, "date": dt.isoformat(), "currency": currency.value}
    resp = requests.post(url, json=body, headers=headers, timeout=30)
    resp.raise_for_status()


@task(retries=3, retry_delay=timedelta(minutes=5))
def update_crypto_price(ticker: str, coin_id: str):
    context = get_current_context()
    dt = context["logical_date"].date()
    print(f"Updating price for {ticker} on {dt}")
    scraper = CryptocurrencyScraper(env.COINGECKO_DEMO_API_KEY)
    import asyncio

    price = asyncio.run(scraper.get_price_by_date(name=coin_id, date=dt))
    _post_price(ticker, float(price), dt)


@task(retries=3, retry_delay=timedelta(minutes=5))
def update_commodity_price(ticker: str):
    context = get_current_context()
    dt = context["logical_date"].date()
    scraper = ALPHAVANTAGEScraper(env.ALPHAVANTAGE_API_KEY)
    price = scraper.get_price_by_date(type=AssetClass.COMMODITY, ticker=ticker, date=dt)
    _post_price(ticker, float(price), dt)


@task(retries=3, retry_delay=timedelta(minutes=5))
def update_index_price(ticker: str):
    context = get_current_context()
    dt = context["logical_date"].date()
    scraper = YFinanceScraper()
    price = scraper.get_price_by_date(ticker=ticker, date=dt)
    _post_price(ticker, float(price), dt)


@task(retries=3, retry_delay=timedelta(minutes=5))
def update_fund_price(ticker: str):
    context = get_current_context()
    dt = context["logical_date"].date()
    scraper = BPIScraper()
    price = scraper.get_price_by_date(ticker=ticker, target_date=dt)
    _post_price(ticker, float(price), dt, currency=Currency.PHP)
