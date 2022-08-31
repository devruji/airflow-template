FROM apache/airflow:2.3.4

USER airflow

# Update pip
RUN pip install --upgrade pip

# Airflow's Constraints files
RUN pip install --no-cache-dir --user "apache-airflow[azure-servicebus]==2.3.4" --constraint "https://raw.githubusercontent.com/apache/airflow/constraints-2.3.4/constraints-3.7.txt"

ENTRYPOINT [ "airflow" ]
