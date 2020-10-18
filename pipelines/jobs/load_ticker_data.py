from pyspark.sql.types import StructType, StructField, FloatType, IntegerType, DateType, StringType
import pyspark.sql.functions as F
from pyspark.sql.window import Window
from pipelines.dependencies.spark import spark_session
import logging

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)


def rename_columns(df, columns):
    if isinstance(columns, dict):
        for old_name, new_name in columns.items():
            df = df.withColumnRenamed(old_name, new_name)
        return df
    else:
        raise ValueError("'columns' should be a dict, like {'old_name_1':'new_name_1', 'old_name_2':'new_name_2'}")


def extract(spark, ticker):
    """
    Extract data from CSV's on disk and store in pySpark DF
    :param spark: Spark session object
    :param ticker: Ticker name of file in data folder
    :return: Spark DataFrame
    """
    logging.info(f'extracting data for {ticker}')

    # set pricing schema for data import
    price_schema = StructType([
        StructField('Date', DateType(), True),
        StructField('Open', FloatType(), True),
        StructField('High', FloatType(), True),
        StructField('Low', FloatType(), True),
        StructField('Close', FloatType(), True),
        StructField('Adj Close', FloatType(), True),
        StructField('Volume', IntegerType(), True)
    ])

    # reads csv data from parent data folder
    df = spark.read.csv(f'../../data/{ticker}.csv', header=True, schema=price_schema)
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

    # rename columns
    column_dict = {
        'Adj Close': 'adj_close',
        'Date': 'date',
        'Open': 'open',
        'High': 'high',
        'Low': 'low',
        'Close': 'close',
        'Volume': 'volume'
    }
    df = rename_columns(df, column_dict)

    # add some analytics
    win = Window.partitionBy("ticker").orderBy("date")
    df = df.withColumn('net_chg_1d', (df.adj_close - F.lag(df.adj_close).over(win)))
    df = df.withColumn('net_chg_5d', (df.adj_close - F.lag(df.adj_close, 5).over(win)))
    df = df.withColumn('net_chg_30d', (df.adj_close - F.lag(df.adj_close, 30).over(win)))
    df = df.withColumn('pct_chg_1d', (df.net_chg_1d / F.lag(df.adj_close).over(win)))
    df = df.withColumn('pct_chg_5d', (df.net_chg_5d / F.lag(df.adj_close, 5).over(win)))
    df = df.withColumn('pct_chg_30d', (df.net_chg_30d / F.lag(df.adj_close, 30).over(win)))
    df = df.withColumn('high_low_range', (df.High - df.Low))
    df = df.withColumn('high_low_range_pct', (df.high_low_range / df.adj_close))
    df = df.withColumn('est_turnover', (df.adj_close * df.volume))

    # drop some columns
    drop_cols = ['Open', 'High', 'Low', 'Close']
    df.drop(*drop_cols)

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
    parquet_file_path = '../../data/etl.parquet'
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
    # read_parquet('../../data/etl.parquet')

