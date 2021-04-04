FROM apache/airflow:2.0.1-python3.8

USER root

# Install cmd utils
RUN apt-get update -yqq \
    && apt-get install -y git \
                          libsasl2-dev \
                          python-dev \
                          libldap2-dev \
                          libssl-dev \
                          procps \
                          vim \
    && apt-get autoremove -yqq --purge \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install MS SQL Support (ODBC Driver)
RUN apt-get update \
    && apt-get install -y gnupg curl \
    && curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add --no-tty - \
    && curl https://packages.microsoft.com/config/debian/10/prod.list > /etc/apt/sources.list.d/mssql-release.list \
    && apt-get update \
    && ACCEPT_EULA=Y apt-get install -y msodbcsql17 unixodbc-dev g++ \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# DAG Folder
COPY mnt/airflow/dags /opt/airflow/dags
RUN chmod 777 /opt/airflow/dags/dags_from_s3

USER airflow

# Install airflow packages
RUN pip install --no-cache-dir --user apache-airflow[ldap,amazon,celery,redis,apache.hive,odbc,microsoft.mssql,presto,postgres]==2.0.1 --constraint https://raw.githubusercontent.com/apache/airflow/constraints-2.0.1/constraints-3.8.txt

# Install bossruji's plugin dependencies
RUN pip install --user python-ldap

COPY /mnt/airflow/airflow.cfg /opt/airflow/airflow.cfg
COPY /mnt/airflow/webserver_config.py /opt/airflow/webserver_config.py

ENTRYPOINT [ "airflow" ]
# EXPOSE 8080
# EXPOSE 8793
# EXPOSE 5555

# CMD ["airflow", "webserver", "-H", "0.0.0.0", "-p", "8080", "-w", "4"]
# CMD ["airflow", "scheduler"]
# CMD ["airflow", "celery", "worker"]
# CMD ["airflow", "celery", "flower"]
