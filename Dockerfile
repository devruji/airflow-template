FROM apache/airflow:slim-latest-python3.10

COPY airflow.cfg /opt/airflow/airflow.cfg

USER root

# ?: Install system dependencies
RUN apt-get update -y \
    && apt-get install -y gcc \
    && apt-get clean

USER airflow

# ?: Install External libs
RUN pip install --upgrade pip
RUN pip install --no-cache-dir --user "apache-airflow[amazon,apache.spark]==2.5.1" --constraint "https://raw.githubusercontent.com/apache/airflow/constraints-2.5.1/constraints-3.7.txt"
RUN pip install --upgrade psycopg2-binary
RUN pip install --upgrade celery[redis]

ENTRYPOINT [ "airflow" ]
