# Airflow template

long learn apache-airflow

## Get Started

```bash
start.sh
```

or

```bash
curl -LfO 'https://airflow.apache.org/docs/apache-airflow/2.4.1/docker-compose.yaml'
```

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
- [Command line cheat sheet](https://levelup.gitconnected.com/airflow-command-line-interface-cli-cheat-sheet-6e5d90bd3552)
