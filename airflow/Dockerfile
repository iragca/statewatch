FROM apache/airflow:3.2.1

COPY ../statewatch /opt/airflow/statewatch
ENV PYTHONPATH="/opt/airflow/statewatch:${PYTHONPATH}"
RUN pip install --no-cache-dir kagglehub>=1.0.2 yfinance>=1.3.0 coingecko-sdk==1.14.1 alpha-vantage>=3.0.0
