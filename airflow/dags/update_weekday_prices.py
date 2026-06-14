from datetime import datetime

from airflow.sdk import dag

from price_update_tasks import update_commodity_price


@dag(
    dag_id="update_weekday_prices_v2",
    description="Weekday price updates",
    schedule="0 0 * * 1-5",
    start_date=datetime(2026, 6, 15),
    catchup=False,
    max_active_runs=1,
)
def update_wti():
    update_commodity_price.override(task_id="update_wti")("WTI")


update_wti()
