import json
import requests
import pandas as pd

from datetime import datetime, timedelta

from airflow import DAG
from airflow.providers.presto.hooks.presto import PrestoHook
from airflow.operators.python import PythonOperator


def get_data_from_e2e():
    ph_hook = PrestoHook(presto_conn_id='prd-bdp-presto-e2e-bossruji')
    sql = '''
            WITH tmp AS (
                SELECT
                    product,
                    mtype,
                    asmdate,
                    COUNT(DISTINCT(hddsn)) AS n_serial_num,
                    CASE WHEN pfcode = '0000' THEN 'P' ELSE 'F' END AS drive_pass_fail,
                    procid || ' - ' || pfcode AS station_failcode,
                    SUM(COUNT(DISTINCT(hddsn))) OVER (PARTITION BY product, mtype, asmdate, procid) AS n_serial_num_loading,
                    SUM(COUNT(DISTINCT(hddsn))) OVER (PARTITION BY product, mtype, asmdate, CASE WHEN pfcode = '0000' THEN 'P' ELSE 'F' END) AS n_serial_num_failure
                FROM
                    hive.vqaa.fact_hdd_association
                WHERE
                    enddt BETWEEN DATE_FORMAT(DATE_ADD('month', -2, CURRENT_DATE), '%Y%m%d') AND DATE_FORMAT(CURRENT_DATE, '%Y%m%d')
                    AND product = 'vl6'
                    AND mtype = 'VL66'
                    AND site IN ('prb', 'bpi')
                    AND asmdate BETWEEN DATE_FORMAT(DATE_ADD('month', -2, CURRENT_DATE), '%Y%m%d') AND DATE_FORMAT(CURRENT_DATE, '%Y%m%d')
                    AND hddcycle = 1
                    AND SUBSTRING(partflag, 7, 1) IN ('0')
                    AND hddtrial NOT BETWEEN 'A000' AND 'LZZZ'
                    AND SUBSTRING(dpcode, 1, 1) NOT IN ('R', 'Z')
                    AND procid IN ('6400','6600','6800')
                GROUP BY mtype, product, asmdate, CASE WHEN pfcode = '0000' THEN 'P' ELSE 'F' END, procid || ' - ' || pfcode, procid)


            SELECT
                product,
                mtype,
                asmdate,
                station_failcode,
                n_serial_num_loading AS n_loading,
                n_serial_num AS n_failed,
                ROUND((n_serial_num * 100.0) / n_serial_num_loading, 3) as failre_rate,
                ROUND((n_serial_num * 100.0) / n_serial_num_failure, 3) as failre_pareto
            FROM tmp
            WHERE drive_pass_fail <> 'P'
            ORDER BY asmdate DESC, 
                n_failed DESC
    '''
    # data = ph_hook.get_records(sql)
    data = ph_hook.get_pandas_df(sql)
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
         start_date=datetime(2021, 2, 16),
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