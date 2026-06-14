import tempfile
import time
from pathlib import Path

import kagglehub
from airflow.sdk import task
from requests import get
from datetime import timedelta


@task(max_active_tis_per_dag=4, retries=3, retry_delay=timedelta(minutes=5))
def fetch_data(ticker: str) -> str:
    url = f"https://statewatch-liart.vercel.app/price/history/{ticker}/?csv=true"

    response = get(url)

    return response.text


@task(max_active_tis_per_dag=4, retries=3, retry_delay=timedelta(minutes=5))
def upload_dataset(data, dataset: str, filename: str):
    current_date = time.strftime("%Y-%m-%d")

    with tempfile.TemporaryDirectory() as tmpdir:
        temp_dir = Path(tmpdir)
        temp_path = temp_dir / f"{filename}.csv"

        # write file
        temp_path.write_text(data, encoding="utf-8")

        kagglehub.dataset_upload(
            dataset, str(temp_path), version_notes=f"Updated {current_date}"
        )
