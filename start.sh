#!/bin/zsh

docker-compose up --scale airflow-worker=1 -d --remove-orphans