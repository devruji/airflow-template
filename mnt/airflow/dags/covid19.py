import json
import requests

from datetime import datetime, timedelta

from airflow import DAG
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago



def get_covid19_report_today():
    url = 'https://covid19.th-stat.com/api/open/today'
    response = requests.get(url)
    data = response.json()
    with open('data.json', 'w') as f:
        json.dump(data, f)

    return data


def save_data_into_db():
    pg_hook = PostgresHook(postgres_conn_id='covid19')
    with open('data.json') as f:
        data = json.load(f)

    insert = """
        INSERT INTO dev_bossruji.daily_covid19_reports (
            confirmed,
            recovered,
            hospitalized,
            deaths,
            new_confirmed,
            new_recovered,
            new_hospitalized,
            new_deaths,
            update_date,
            source,
            dev_by,
            server_by)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
    """

    pg_hook.run(insert, parameters=(data['Confirmed'],
                                       data['Recovered'],
                                       data['Hospitalized'],
                                       data['Deaths'],
                                       data['NewConfirmed'],
                                       data['NewRecovered'],
                                       data['NewHospitalized'],
                                       data['NewDeaths'],
                                       datetime.strptime(data['UpdateDate'], '%d/%m/%Y %H:%M'),
                                       data['Source'],
                                       data['DevBy'],
                                       data['SeverBy']))

default_args = {
    'owner': 'bossruji',
    'depends_on_past': False,
    # 'email': ['airflow@example.com'],
    # 'email_on_failure': False,
    # 'email_on_retry': False,
    'retries': 1,
    # 'retry_delay': timedelta(minutes=5),
    # 'queue': 'bash_queue',
    # 'pool': 'backfill',
    # 'priority_weight': 10,
    # 'end_date': datetime(2016, 1, 1),
    # 'wait_for_downstream': False,
    # 'dag': dag,
    # 'sla': timedelta(hours=2),
    # 'execution_timeout': timedelta(seconds=300),
    # 'on_failure_callback': some_function,
    # 'on_success_callback': some_other_function,
    # 'on_retry_callback': another_function,
    # 'sla_miss_callback': yet_another_function,
    # 'trigger_rule': 'all_success'
}

with DAG(
        'covid19_data_pipeline',
         default_args=default_args,
         description='A simple data pipeline for COVID-19 report',
         schedule_interval='@daily', # 12:30 PM TH Time Zone
         start_date=datetime(2021, 2, 14),
         tags=['covid-19']
        ) as dag:

    t1 = PythonOperator(
        task_id='get_covid19_report_today',
        python_callable=get_covid19_report_today
    )

    t2 = PythonOperator(
        task_id='save_data_into_db',
        python_callable=save_data_into_db
    )

    t1 >> t2