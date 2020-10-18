from pyspark.sql.types import StructType, StructField, FloatType, IntegerType, DateType, StringType
import pyspark.sql.functions as F
from pyspark.sql.window import Window
from data_strategy_tools.dependencies.spark import spark_session
import logging

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)


def extract(spark, ticker):
    """
    Extract data from CSV's on disk and store in pySpark DF
    :param spark: Spark session object
    :param ticker: Ticker name of file in data folder
    :return: Spark DataFrame
    """
    logging.info(f'extracting data for {ticker}')
    price_schema = StructType([
        StructField('date', DateType(), True),
        StructField('open', FloatType(), True),
        StructField('high', FloatType(), True),
        StructField('low', FloatType(), True),
        StructField('close', FloatType(), True),
        StructField('adj_close', FloatType(), True),
        StructField('volume', IntegerType(), True)
    ])
    df = spark.read.csv(f'data/{ticker}.csv', header=True, schema=price_schema)
    df = df.withColumn('ticker', F.lit(ticker))
    return df


def transform(df, ticker):
    """
    Transform, clean and enrich original data
    :param df: Spark DataFrame
    :param ticker: ticker
    :return: Spark Dataframe
    """
    logging.info(f'transforming data for {ticker}')
    win = Window.partitionBy("ticker").orderBy("date")
    df = df.withColumn('net_chg_1d', (df.adj_close - F.lag(df.adj_close).over(win)))
    df = df.withColumn('net_chg_5d', (df.adj_close - F.lag(df.adj_close, 5).over(win)))
    df = df.withColumn('net_chg_30d', (df.adj_close - F.lag(df.adj_close, 30).over(win)))
    df = df.withColumn('pct_chg_1d', (df.net_chg_1d / F.lag(df.adj_close).over(win)))
    df = df.withColumn('pct_chg_5d', (df.net_chg_5d / F.lag(df.adj_close, 5).over(win)))
    df = df.withColumn('pct_chg_30d', (df.net_chg_30d / F.lag(df.adj_close, 30).over(win)))
    df = df.withColumn('high_low_range', (df.high - df.low))
    df = df.withColumn('high_low_range_pct', (df.high_low_range / df.adj_close))
    df = df.withColumn('est_turnover', (df.adj_close * df.volume))
    return df


def load(df, file_path, ticker):
    """
    Load data into Parquet file (for this example)
    :param df: Spark DataFrame
    :param file_path: path to store data
    :param ticker: ticker
    :return: None
    """
    logging.info(f'loading data for {ticker}')
    df.write.mode('append').parquet(file_path)


def pipeline():
    """
    The pipeline controller
    :return: None
    """
    logging.info('pipeline commencing')
    tickers = 'AAPL,AMZN,FB,IBM,MSFT'.split(',')
    parquet_file_path = 'data/etl.parquet'
    spark = spark_session()

    for ticker in tickers:
        ticker_df = extract(spark=spark, ticker=ticker)
        transform_df = transform(ticker_df, ticker=ticker)
        load(transform_df, parquet_file_path, ticker=ticker)

    logging.info('pipeline complete')


def read_parquet(file_name):
    """
    Test data in parquet file by returning average est_turnover by ticker
    :param file_name: location of parquet file
    :return: console output
    """
    spark = spark_session()
    df = spark.read.parquet(file_name)
    df.groupBy('ticker').avg('est_turnover').show(truncate=False)


if __name__ == '__main__':
    pipeline()
    # read_parquet('data/etl.parquet')

