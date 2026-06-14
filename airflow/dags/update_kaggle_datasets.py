from airflow.sdk import dag
from datetime import datetime

from update_kaggle_datasets_tasks import (
    fetch_data,
    upload_dataset,
)


@dag(
    dag_id="update_kaggle_datasets",
    description="Update datasets XMR, BTC, GOLD, WTI, ^GSPC",
    start_date=datetime(2026, 5, 11),
    schedule="@daily",
    catchup=False,
    max_active_runs=1,
)
def update_datasets():
    assets = [
        {
            "id": "xmr",
            "ticker": "XMR",
            "dataset": "iragca/monero-xmr-historical-data",
            "filename": "monero_xmr",
        },
        {
            "id": "btc",
            "ticker": "btc",
            "dataset": "iragca/bitcoin-btc-historical-data",
            "filename": "bitcoin_btc",
        },
        {
            "id": "xau",
            "ticker": "xau",
            "dataset": "iragca/gold-xau-historical-data",
            "filename": "gold_xau",
        },
        {
            "id": "wti",
            "ticker": "wti",
            "dataset": "iragca/crude-oil-wti-historical-data",
            "filename": "crude-oil_wti",
        },
        {
            "id": "gspc",
            "ticker": "^gspc",
            "dataset": "iragca/s-and-p-500-gspc-historical-data",
            "filename": "s-and-p-500_gspc",
        }
    ]
    for asset in assets:
        fetched = fetch_data.override(task_id=f"fetch_{asset["id"]}")(
            asset["ticker"]
        )

        upload_dataset.override(task_id=f"upload_{asset["id"]}")(
            fetched,
            asset["dataset"],
            asset["filename"],
        )


update_datasets()
