FROM apache/airflow:2.4.1-python3.10

USER root

COPY airflow.cfg /opt/airflow/airflow.cfg

# ?: Install system dependencies
RUN apt-get update -y \
    && apt-get install -y gcc \
    && apt-get clean

USER airflow

# ?: Install External libs
RUN pip install --upgrade pip
RUN pip install --upgrade "algoliasearch>=2.0,<3.0"

# Airflow's Constraints files
# RUN pip install --no-cache-dir --user "apache-airflow[azure-servicebus]==2.3.4" --constraint "https://raw.githubusercontent.com/apache/airflow/constraints-2.3.4/constraints-3.7.txt"

ENTRYPOINT [ "airflow" ]
