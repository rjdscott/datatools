import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq

import logging

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)


def extract(ticker):
    """
    Extract data from CSV's on disk and store in Dask DataFrame

    :param ticker: Ticker name of file in data folder
    :return: Dask DataFrame
    """
    logging.info(f'extracting data for {ticker}')

    # reads csv data from parent data folder
    df = pd.read_csv(f'../../data/{ticker}.csv')
    df['ticker'] = ticker
    return df


def transform(df, ticker):
    """
    Transform, clean and enrich original data
    :param df: Pandas DataFrame
    :param ticker: ticker
    :return: Pandas Dataframe
    """
    logging.info(f'transforming data for {ticker}')

    column_dict = {
        'Adj Close': 'close_adj',
        'Date': 'date',
        'Open': 'open',
        'High': 'high',
        'Low': 'low',
        'Close': 'close',
        'Volume': 'volume'
    }
    df.rename(columns=column_dict, inplace=True)

    df['turnover'] = df.close_adj * df.volume
    return df


def load(df, file_path, ticker):
    """
    Load data into Parquet file (for this example)
    :param df: DataFrame
    :param file_path: path to store data
    :param ticker: ticker
    :return: None
    """
    logging.info(f'loading data for {ticker}')

    # infer parquet table from pandas df
    table = pa.Table.from_pandas(df=df)

    # write table to local file
    pq.write_to_dataset(table, root_path=file_path)


def pipeline():
    """
    The pipeline controller
    :return: None
    """
    logging.info('pipeline commencing')

    tickers = 'AAPL,AMZN,FB,IBM,MSFT'.split(',')
    parquet_file_path = '../../data/etl_pandas.parquet'

    for ticker in tickers:
        ticker_df = extract(ticker=ticker)
        transform_df = transform(df=ticker_df, ticker=ticker)
        load(df=transform_df, file_path=parquet_file_path, ticker=ticker)

    logging.info('pipeline complete')


def read_parquet(file_path):
    """
    Test data in parquet file by returning average est_turnover by ticker
    :param file_path: location of parquet file
    :return: console output
    """
    df = pq.read_table(file_path).to_pandas()
    print(df[['ticker', 'turnover']].groupby('ticker').mean())


if __name__ == '__main__':
    # pipeline()
    read_parquet('../../data/etl_pandas.parquet')

