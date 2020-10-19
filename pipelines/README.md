# DataTools Pipelines

### Getting started
1. Initialise your venv or pipenv, 
2. install required packages `pip install -r requirements.txt`
3. make sure you have Java installed, if not, follow this [link](https://towardsdatascience.com/how-to-get-started-with-pyspark-1adc142456ec)
4. run the example `jobs/load_ticker_data.py` to perform a basic ETL pipeline

This project aims to highlight a simple pySpark ETL pipeline, with scope to enhance using Apache Airflow.

### ToDo
1. Add Airflow
2. Migrate `jobs/load_ticker_data.py` into a proper DAG
3. Dockerize