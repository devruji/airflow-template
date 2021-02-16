import json
import requests

from datetime import datetime, timedelta

from airflow import DAG
# from airflow.providers.microsoft.mssql.hooks.mssql import MsSqlHook
from airflow.providers.presto.hooks.presto import PrestoHook
from airflow.operators.python import PythonOperator


def get_data_from_e2e():
    ph_hook = PrestoHook(presto_conn_id='prd-bdp-presto-e2e-bossruji')
    sql = "SELECT count(1) AS num FROM airflow.static_babynames"
    data = ph_hook.get_records(sql)
    print(data)

    return data


# def save_data_into_db():
    # pg_hook = MsSqlHook(presto_conn_id='prd-bdp-presto-e2e-bossruji')
    # with open('data.json') as f:
    #     data = json.load(f)

    # insert = """
    #     INSERT INTO dev_bossruji.daily_covid19_reports (
    #         confirmed,
    #         recovered,
    #         hospitalized,
    #         deaths,
    #         new_confirmed,
    #         new_recovered,
    #         new_hospitalized,
    #         new_deaths,
    #         update_date,
    #         source,
    #         dev_by,
    #         server_by)
    #     VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
    # """

    # pg_hook.run(insert, parameters=(data['Confirmed'],
    #                                    data['Recovered'],
    #                                    data['Hospitalized'],
    #                                    data['Deaths'],
    #                                    data['NewConfirmed'],
    #                                    data['NewRecovered'],
    #                                    data['NewHospitalized'],
    #                                    data['NewDeaths'],
    #                                    datetime.strptime(data['UpdateDate'], '%d/%m/%Y %H:%M'),
    #                                    data['Source'],
    #                                    data['DevBy'],
    #                                    data['SeverBy']))

default_args = {
    'owner': 'bossruji',
    'depends_on_past': False,
    # 'email': ['airflow@example.com'],
    # 'email_on_failure': False,
    # 'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
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
        'ent-top5-failure-pareto-etl',
         default_args=default_args,
         description='A simple data pipeline to etl data for monitor failure pareto in enterprise products',
         schedule_interval='@daily', # 12:30 PM TH Time Zone
         start_date=datetime(2021, 2, 14),
         tags=['ent-top5-fr-pareto']
        ) as dag:

    t1 = PythonOperator(
        task_id='get_data_from_e2e',
        python_callable=get_data_from_e2e
    )

    # t2 = PythonOperator(
    #     task_id='save_data_into_db',
    #     python_callable=save_data_into_db
    # )

    # t1 >> t2
    t1