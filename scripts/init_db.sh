#!/usr/bin/env bash

airflow db init
airflow users create --username admin --firstname Rujikorn --lastname Ngoensaard --role Admin --email rujikorn.ngoensaard@wdc.com
airflow webserver