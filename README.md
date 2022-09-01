# Airflow template
long learn apache-airflow

## Get Started
```bash
start.sh
```
or
![image](https://user-images.githubusercontent.com/43924465/187859368-39264548-65c5-4911-9eb4-5b7d2d8f5bb4.png)

Cr: [Marc lamberti @linkedin](https://www.linkedin.com/posts/marclamberti_dataengineer-airflow-dataengineering-activity-6970022178763194369-H_PJ?utm_source=share&utm_medium=member_desktop)


## Airflow CLI

👉 `airflow standalone`<br />
💡 Run all-one-copy of Airflow; Great for quick testing/debugging

👉 `airflow db clean --clean-before-timestamp 2022-01-01`<br />
💡 Purge old records in the metastore; Keep your DB clean!

👉 `airflow connections export --file-format json connections.json`<br />
💡 Export connections; don't recreate them ever again

👉 `airflow variables export variables.json`<br />
💡 Export variables; don't recreate them ever again

👉 `airflow users export users.json`<br />
💡 Export users; don't lose your users

👉 `airflow tasks test`<br />
💡 Test a task; never wait to run your DAG before getting errors

👉 `airflow dags backfill my_dag -s 2022-01-01 -e 2022-02-01`<br />
💡Run/Rerun DAG Runs for a specific period

👉 `airflow dags test my_dag 2022-01-01`<br />
💡 Execute a single DAG Run for a DAG; Test your DAG first
## Ref:
- [https://airflow.apache.org/](https://airflow.apache.org/)
- [YAML Template](https://airflow.apache.org/docs/apache-airflow/stable/docker-compose.yaml)
- [Airflow CLI](#airflow-cli) - [Marc lamberti @linkedin](https://www.linkedin.com/posts/marclamberti_airflow-dataengineering-dataengineer-activity-6966051745110093825-CkOt)
