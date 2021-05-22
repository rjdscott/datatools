# DataTools
#### Contents:
1. [API using FastAPI + SQLAlchemy + pydantic](#api-using-fastapi--sqlalchemy--pydantic)
2. [API using Flask + Protobuf](#api-using-flask--protobuf)
3. [Plotly Dash + API and Docker](#plotly-dash--api-and-docker)
4. [ETL Pipelines](#etl-pipelines)
5. [Airflow + Docker](#airflow--docker)

## API using FastAPI + SQLAlchemy + pydantic
This project is a minimalistic implementation of a FastAPI HTTP REST service that only returns serialized stock 
time-series data stored in a sqlite database. We will be using SQLAlchemy as the ORM and pydantic for serialization 
and validation for our endpoints.

Project path: `datatools/api_fastapi`

Further information: [datatools/api_fastapi/README.md](https://github.com/rjdscott/datatools/blob/master/api_fastapi/README.md)

This project contains the following:
1. a basic synchronous HTTP server using [FastAPI](https://fastapi.tiangolo.com/), a modern, high-performance web framework for building APIs
2. use FastAPI's swagger documentation to access the app's endpoints.
3. how to use [SQLAlchemy](https://docs.sqlalchemy.org/en/14/) to model and query the data stored in a local [SQLite](https://www.sqlite.org/index.html)
4. how to create data schemas to enforce type hints at runtime using [pydantic](https://pydantic-docs.helpmanual.io/)

#### The data
Using a simple ETL script `datatools/api_fastapi/sync/create_db_data.py` 
extracted all ticker data from the parquet files in `data/all-tickers` 
and stored it in a single `prices` table in `api_fastapi/sync/app.db`.

#### How to run
```bash
(venv) ➜ cd datatools/api_fastapi/sync
(venv) ➜ uvicorn app.main:app --reload

INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [29317] using statreload
INFO:     Started server process [29319]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

You can use the command line to test the tickers endpoint
```bash
curl -X 'GET' 'http://localhost:8000/tickers/' -H 'accept: application/json'

[
  {
    "ticker": "AAPL"
  },
  {
    "ticker": "AMZN"
  },
  {
    "ticker": "FB"
  },
  {
    "ticker": "IBM"
  },
  {
    "ticker": "MSFT"
  }
]
```

Or you can navigate to the api documentation page at http://127.0.0.1:8000/docs and execute the same query

<img src="https://github.com/rjdscott/datatools/blob/master/data/img/api_fastapi.png?raw=true">

#### ToDo's
1. implement an async api - which is what really makes FastAPI's performance comparative to node, etc.
2. customize the swagger documentation to use less generic text and placeholders
3. dockerize the application

## API using Flask + Protobuf
This project is a minimalistic implementation of a flask HTTP REST service that only returns serialized stock 
time-series data originally stored in a local parquet file. Protobuf is only used for the serialization/deserialization
of messages over HTTP. 

Project path: `datatools/api`

Further information: [datatools/api/README.md](https://github.com/rjdscott/datatools/blob/master/airflow/README.md)

This project contains the following:
1. a basic HTTP server using [Flask Restful](https://flask-restful.readthedocs.io/en/latest/quickstart.html)
2. an implementation of [Protobuf](https://developers.google.com/protocol-buffers/docs/pythontutorial) to serialize and send structured data over HTTP 
3. how to use [Dask](https://dask.org/) on the backend to read/manipulate data from a local parquet file and serialize using protobuf

#### The data
The data served is stored in a parquet in the `datatools/api/data` directory which 
was generated via an ETL pipeline, found in `datatools/pipelines/jobs`.

#### Protobuf
Protobuf was only used for message structuring and serialization. In future efforts, 
I will look to implement a full gRPC service using the `grpcio` library as it provides lower 
latency bi-directional streaming, which are better suited for distributed systems. 
However, for the scope of this project, the combination of Flask and Protobuf allows me to implement a satisfactory 
solution for demonstrative purposes much faster.

#### Dask vs Pandas vs PySpark
Dask was used to read data from the local parquet file for a number of reasons. Firstly, while Pandas is simple to use, 
it needs to read the full parquet file before filtering. This is too memory intensive and only works on single workloads. 

Secondly, PySpark has a performance overhead since every time you need to access data you need to initiate a spark session.
Since this project does not work with large distributed datasets and the requests are pretty simple, pySpark is not best suited.

So then you have Dask. It is built purely in python and leverages numpy and pandas but is designed to work with distributed
loads. Dask does not have the lag of pyspark but allows you to specify the dataframe operations/filtering in advance,
so it is not as memory heavy as pandas. 

#### ToDos
1. Upgrade the API to be a fully implemented RPC framework (maybe create a second project to run comparisons)
2. Add some more useful meaningful services 

## Plotly Dash + API and Docker
A very minimalist dashboard has been built using plotly Dash, which displays a stock return series and
a daily returns distribution plot.

Project path: `datatools/dashboard`

Further information: [datatools/dashboard/README.md](https://github.com/rjdscott/datatools/blob/master/dashboard/README.md)

The dashboard is used in tandem with the `datatools/api` so in order to facilitate smooth simulation
both the dashboard and api have been dockerized and orchestrated using docker-compose.

To run the dashboard and API:

```
git clone https://github.com/rjdscott/datatools.git
cd datatools/dashboard
docker-compose build
docker-compose up -d --force-recreate
```

Then navigate to [http://localhost:8050](http://localhost:8050) to see the dashboard.

<img src="https://github.com/rjdscott/datatools/blob/master/data/img/dashboard.png?raw=true" width="706" height="744">

## ETL Pipelines
Project path: `datatools/pipelines`

Further information: [datatools/pipelines/README.md](https://github.com/rjdscott/datatools/blob/master/api/README.md)

This project showcases the implementation of a simplified ETL pipeline using pySpark, Dask, Pandas and Parquet.

What's covered:
1. extract csv files from `datatools/data/` using a predefined schema
2. transform and clean the data by adding some basic analytics
3. store the data in a parquet file in `datatools/data/`

In this example I decided to go with a static pipeline that takes stock data from CSVs, 
transforms then loads into a parquet file. 
Although there are many tools available for ETL jobs, you will find an implementation of the same pipeline using 
PySpark, Dask and Pandas. 

The goal of having the same pipeline implemented in different ways is to allow for direct comparison of use and ease of
implementation. On one end, you have the simplicity of Pandas, which can be used for lighter and simpler workloads. 
On the other you have tools that cna be scaled up to thousand core clusters for computation on terabytes of data with
ease. You will also see how easy it is to implement a parallel pipeline using Dask. 

## Airflow + Docker
A minimalist implementation of airflow with docker. 

Project path: `datatools/airflow`

Further information: [datatools/airflow/README.md](https://github.com/rjdscott/datatools/blob/master/airflow/README.md)

To use:
- create your own DAG in the `airflow/dags` 
- run `docker-compose up -d` you can add `--build` arg to build all images
- view the dashboard available at http://localhost:8080

<img src="https://chessmate-public.s3.amazonaws.com/airflow.png">
