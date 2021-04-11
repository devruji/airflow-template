#!/bin/bash

docker-compose -f airflow-compose.yml up --scale worker=4 -d