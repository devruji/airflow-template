from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.macros import ds_format
# from airflow.utils.dates import days_ago



def get_date_part(ds, **kwargs):
    print('ds >>', ds)
    print('ds_format >>', ds_format(ds, '%Y-%m-%d', '%Y/%m/%d/'))
    return ds_format(ds, '%Y-%m-%d', '%Y/%m/%d/')

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
        'test_print_datetime',
         default_args=default_args,
         description='A simple pipeline to print out current datetime',
         schedule_interval='*/5 * * * *', # 12:30 PM TH Time Zone
         start_date=datetime(2021, 2, 14),
         tags=['print-dt']
        ) as dag:

    t1 = PythonOperator(
        task_id='get_covid19_report_today',
        python_callable=get_date_part,
        op_kwargs={'ds': '{{ ds }}'}
    )

    t1