import dask
import dask.dataframe as dd
import pandas as pd
from dask.distributed import Client

import logging

logging.basicConfig(format='%(asctime)s | %(levelname)s | %(message)s', level=logging.INFO)


def get_dask_client() -> Client:
    """
    Create a distributed dask client
    :return:
    """
    client = Client(n_workers=2, threads_per_worker=2, memory_limit='2GB')
    try:
        yield client
    finally:
        client.close()


def extract(ticker: str, input_file_path: str) -> pd.DataFrame:
    """
    Extract data from CSV's on disk and store in Dask DataFrame

    :param input_file_path: str
    :param ticker: Ticker name of file in data folder
    :return: Dask DataFrame
    """
    logging.info(f'extracting data for {ticker}')

    # reads csv data from parent data folder
    df = dd.read_csv(f'{input_file_path}{ticker}.csv')
    df['ticker'] = ticker
    return df


def transform(df: pd.DataFrame, ticker: str) -> pd.DataFrame:
    """
    Transform, clean and enrich original data
    :param df: Dask DataFrame
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
    df = df.rename(columns=column_dict)

    df['turnover'] = df.close_adj * df.volume
    return df


def load(df: pd.DataFrame, file_path: str, ticker: str) -> None:
    """
    Load data into Parquet file (for this example)
    :param df: Dask DataFrame
    :param file_path: path to store data
    :param ticker: ticker
    :return: None
    """
    logging.info(f'loading data for {ticker}')
    df.to_parquet(file_path, engine='pyarrow', write_index=False, append=True)
    pass


def pipeline(tickers: list,
             parquet_file_path: str,
             input_file_path: str,
             in_parallel: bool = True) -> None:
    """
    Pipeline orchestrator function
    :param input_file_path: str
    :param tickers: list
    :param parquet_file_path: string
    :param in_parallel: bool
    :return: None
    """
    for ticker in tickers:

        if in_parallel:
            logging.info('pipeline commencing in parallel...')
            ticker_df = dask.delayed(extract)(ticker=ticker, input_file_path=input_file_path)
            transform_df = dask.delayed(transform)(df=ticker_df, ticker=ticker)
            dask.delayed(load)(df=transform_df, file_path=parquet_file_path, ticker=ticker)

        else:
            logging.info('pipeline commencing in serial...')
            ticker_df = extract(ticker=ticker, input_file_path=input_file_path)
            transform_df = transform(df=ticker_df, ticker=ticker)
            load(df=transform_df, file_path=parquet_file_path, ticker=ticker)
    pass


def pipeline_manager(parquet_file_path: str,
                     input_file_path: str,
                     tickers: list,
                     in_parallel: bool = True) -> None:
    """
    Pipeline manager function
    :param tickers: list
    :param input_file_path:
    :param parquet_file_path: str
    :param in_parallel: bool
    :return: None
    """

    if in_parallel:
        client = Client(n_workers=2, threads_per_worker=2, memory_limit='2GB')
        try:
            dask.compute(pipeline(tickers=tickers,
                                  parquet_file_path=parquet_file_path,
                                  input_file_path=input_file_path,
                                  in_parallel=in_parallel))
        finally:
            client.close()
    else:
        pipeline(tickers=tickers, parquet_file_path=parquet_file, in_parallel=in_parallel)


def read_parquet(file_name: str) -> None:
    """
    Test data in parquet file by returning average est_turnover by ticker
    :param file_name: location of parquet file
    :return: console output
    """
    df = dd.read_parquet(file_name, engine='pyarrow')
    print(df.groupby('ticker').turnover.mean().compute())


if __name__ == '__main__':

    parquet_file = '../../data/etl_dask.parquet'
    input_file_path = '../../data/'
    tickers = 'AAPL,AMZN,FB,IBM,MSFT'.split(',')

    pipeline_manager(parquet_file_path=parquet_file,
                     input_file_path=input_file_path,
                     tickers=tickers)
    # read_parquet(parquet_file)
