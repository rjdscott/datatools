# DataTools
What will be covered:
1. ETL Pipelines using PySpark and Parquet files
2. API using ProtoBuf and Flask
3. Dashboard using plotly Dash
4. Deployment using Docker

## ETL Pipelines using PySpark
Project path: `datatools/api`

Further information: `datatools/api/README.md`

This project showcases the implementation of a simplified ETL pipeline using pySpark.

What's covered:
1. extract csv files from `datatools/data/` using a predefined schema
2. transform and clean the data by adding some basic analytics
3. store the data in a parquet file in `datatools/data/`

In this example I decided to go with a static pipeline using PySpark. Although there are many tools available for
ETL jobs, PySpark manages very large workloads effortlessly and can also handle data streams.

My next enhancement would be to implement Apache Airflow for job orchestration, scheduling and intelligence dashboards.

#### ToDo
1. implement Airflow and incorporate the `load_ticker_data` job as a DAG
2. read data from a public API, rather than a local CSV's


## API using ProtoBuf and Flask
This project is a minimalistic implementation of an HTTP service that only handles simple GET requests, 
and returns serialized stock time-series data stored in a local parquet file. 

The code/functionality can be found in the `datatools/api` directory.

This project contains the following:
1. a basic HTTP server using Flask
2. an implementation of Protobuf to serialize and send structured data over HTTP 
3. how to use Dask to read/manipulate data from a local parquet file and serialize using protobuf

#### The data
The data served is stored in a parquet in the `datatools/api/data` directory which 
was generated via an ETL pipeline, found in `datatools/pipelines/jobs`.

#### Protobuf
Protobuf was only used for message structuring and serialization. In future efforts, 
I will look to implement a full gRPC service using the `grpcio` library as it provides lower 
latency and more scalability when working with distributed systems. 
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

## Dashboard using plotly Dash
A very minimalist dashboard has been built using plotly Dash, which displays a stock return series and
a daily returns distribution plot.

The dashboard is used in tandem with the `datatools/api` so in order to facilitate smooth simulation
both the dashboard and api have been dockerized and orchestrated using docker-compose.
