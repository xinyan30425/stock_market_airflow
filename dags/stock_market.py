import sys

from include.stock_market.tasks import _get_stock_prices,_store_prices

from airflow.decorators import dag, task
from airflow.hooks.base import BaseHook
from airflow.sensors.base import PokeReturnValue
from airflow.operators.python import PythonOperator
from airflow.providers.docker.operators.docker import DockerOperator
from datetime import datetime
import requests
import json


import os

SYMBOL = "AAPL"

@dag(
    start_date=datetime(2023, 1, 1),
    schedule_interval='@daily',
    catchup=False,
    tags=['stock_market']
)
def stock_market():
    
    @task.sensor(poke_interval=30,timeout=300, mode='poke')
    def is_api_available() -> PokeReturnValue:
        api = BaseHook.get_connection('stock_api')
        url = f"{api.host}{api.extra_dejson['endpoint']}"
        response = requests.get(url, headers=api.extra_dejson['headers'])
        condition = response.json().get('chart', {}).get('error') is None
        return PokeReturnValue(is_done=condition,xcom_value=url)
     
    
    
    # Define the PythonOperator to get stock prices
    get_stock_prices = PythonOperator(
        task_id='get_stock_prices',
        python_callable=_get_stock_prices,
        op_kwargs={'url': '{{ task_instance.xcom_pull(task_ids="is_api_available") }}','symbol':SYMBOL},
    )
    
    store_prices = PythonOperator(
        task_id = 'store_prices',
        python_callable = store_prices,
        op_kwargs={'stock':'{{ task_instance.xcom_pull(task_ids="get_stock_prices") }}'},
    )
    
    format_prices = DockerOperator (
        task_id = 'format_prices',
        image = 'airflow/stock-app',
        container_name = 'format_prices',
        api_version = 'auto',
        auto_remove = True,
        docker_url = 'tcp://docker-proxy:2375',
        network_mode = 'container:spark-master',
        tty=True,
        xcom_all = False,
        mount_tmp_dir=False,
        environment = {
            'SPARK_APPLICATION_ARGS':'{{task_instance.xcom_pull(task_ids="store_prices")}}'
        }
    )



    # Define the task dependencies
    is_api_available() >> get_stock_prices >> store_prices
   

stock_market()
