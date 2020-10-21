# DataTools Pipelines

This project aims to highlight different implementations of ETL pipelines using different but
readily available tools.

### Getting started
1. Activate your venv or pipenv, 
2. install required packages `pip install -r requirements.txt`
3. make sure you have Java installed, if not, follow this [link](https://towardsdatascience.com/how-to-get-started-with-pyspark-1adc142456ec)
4. run the different example jobs in `jobs/` 
5. the data used for these examples lies in the `../data/` directory

## Implementation flavours

### Pandas: `jobs/load_ticker_data_pandas.py`
For simple, single source and memory light loads, pandas is a solid tool to use.

##### Things to note:
* to write parquet files you need to `pip install pyarrow` and be sure to append tables instead of rewriting
* processes are executed in serial
* all procedures require data to be committed to memory (i.e. not lazy-loaded)

Read more: 
* [Pandas](https://pandas.pydata.org/docs/user_guide/index.html)
* [PyArrow](https://arrow.apache.org/docs/python/parquet.html)

### PySpark: `jobs/load_ticker_data_pyspark.py`
Spark is a popular distributed computing tool that s written in Scala and runs on the JVM.
PySpark is a python wrapper/api that allows us to interact with the spark framework directly using python

##### Things to note:
* has a look and feel similar somewhat to Pandas and workflows can revolve around DataFrames
* DataFrames are immutable and do not have an index
* implements a large subset of the SQL language
* data transformations are lazy
* supports streaming datasets
* scales from a single node to thousand-node clusters.

Read more: 
* [PySpark](https://spark.apache.org/docs/latest/api/python/pyspark.html)


### Dask: `jobs/load_ticker_data_dask.py`
Like Spark, Dask is built or large distributed workflows. However, it is built in python for python, having bindings to
key libraries such asPandas, numpy, scikit-learn. Also, Dask is generally a smaller and lighter weight tool than Spark

##### Things to note:
* feels more like Pandas pandas. Workflows also revolve around DataFrames too
* data transformations are lazy
* supports streaming datasets
* scales from a single node to thousand-node clusters.

Read more:
* [Dask](https://docs.dask.org/en/latest/)