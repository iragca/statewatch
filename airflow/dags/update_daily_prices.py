from datetime import datetime

from airflow.sdk import dag

from price_update_tasks import (
    update_crypto_price,
    update_commodity_price,
    update_index_price,
    update_fund_price,
)


@dag(
    dag_id="update_daily_prices",
    description="Daily price update for XMR, BTC, XAU, WTI, ^GSPC, M1ALFMMU",
    schedule="@daily",
    start_date=datetime(2026, 5, 11),
    catchup=False,
    max_active_runs=1,
)
def update_prices():
    update_crypto_price.override(task_id="update_xmr")("XMR", "monero")
    update_crypto_price.override(task_id="update_btc")("BTC", "bitcoin")
    update_commodity_price.override(task_id="update_xau")("XAU")
    update_commodity_price.override(task_id="update_wti")("WTI")
    update_index_price.override(task_id="update_gspc")("^GSPC")
    update_fund_price.override(task_id="update_m1alfmmu")("M1ALFMMU")


update_prices()
