import dask
import dask.dataframe as dd
import pandas as pd
from dask.distributed import Client
import os
import logging

logging.basicConfig(format='%(asctime)s | %(levelname)s | %(message)s', level=logging.INFO)


def extract(ticker: str, input_file_path: str) -> pd.DataFrame:
    """
    Extract data from CSV's on disk and store in Dask DataFrame

    :param input_file_path: str
    :param ticker: Ticker name of file in data folder
    :return: Dask DataFrame
    """
    logging.info(f'extracting data for {ticker}')

    # reads csv data from parent data folder
    full_file_name = f'{os.path.join(input_file_path, ticker)}.csv'
    df = pd.read_csv(full_file_name)

    column_dict = {
        'Adj Close': 'close_adj',
        'Date': 'date',
        'Open': 'open',
        'High': 'high',
        'Low': 'low',
        'Close': 'close',
        'Volume': 'volume'
    }
    df = df.rename(columns=column_dict)
    df['ticker'] = ticker
    df['turnover'] = df.close_adj * df.volume
    return df


def load(df: pd.DataFrame, file_path: str) -> None:
    """
    Load data into Parquet file (for this example)
    :param df: Dask DataFrame
    :param file_path: path to store data
    :return: None
    """
    logging.info(f'writing data to {file_path}')
    df.to_parquet(file_path, engine='pyarrow', write_index=False, partition_on=['ticker'], compression='snappy')
    pass


def pipeline(tickers: list,
             parquet_file_path: str,
             input_file_path: str) -> None:
    """
    Pipeline orchestrator function
    :param input_file_path: str
    :param tickers: list
    :param parquet_file_path: string
    :return: None
    """
    client = Client(n_workers=2, threads_per_worker=2, memory_limit='2GB')

    try:
        logging.info('pipeline commencing in parallel...')
        ticker_df_list = [dask.delayed(extract)(ticker, input_file_path) for ticker in tickers]
        ticker_df = dd.from_delayed(ticker_df_list)
        load(df=ticker_df, file_path=parquet_file_path)
    finally:
        client.close()


def read_parquet(file_name: str) -> None:
    """
    Test data in parquet file by returning average est_turnover by ticker
    :param file_name: location of parquet file
    :return: console output
    """
    df = dd.read_parquet(file_name, engine='pyarrow')
    print(df.groupby('ticker').turnover.mean().compute())


if __name__ == '__main__':

    parquet_file = os.path.join('../', '../', 'data/', 'all-tickers')
    input_file_path = os.path.join('../', '../', 'data', 'raw')
    tickers = 'AAPL,AMZN,FB,IBM,MSFT'.split(',')

    pipeline(parquet_file_path=parquet_file,
             input_file_path=input_file_path,
             tickers=tickers)
