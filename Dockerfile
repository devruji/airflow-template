FROM apache/airflow:2.0.0-python3.8

# RUN apt-get install -y --no-install-recommends \
#         freetds-bin \
#         krb5-user \
#         ldap-utils \
#         libffi6 \
#         libsasl2-2 \
#         libsasl2-modules \
#         libssl1.1 \
#         locales  \
#         lsb-release \
#         sasl2-bin \
#         sqlite3 \
#         unixodbc

# RUN python -m pip install --upgrade pip

RUN pip install --no-cache-dir apache-airflow-providers-presto
RUN pip install --no-cache-dir apache-airflow-providers-microsoft-mssql[odbc]
RUN pip install --no-cache-dir apache-airflow-providers-apache-hive