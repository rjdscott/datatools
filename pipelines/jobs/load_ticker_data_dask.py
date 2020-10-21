import dask
import dask.dataframe as dd
import logging

logging.basicConfig(format='%(asctime)s | %(levelname)s | %(message)s', level=logging.INFO)


def extract(ticker):
    """
    Extract data from CSV's on disk and store in Dask DataFrame

    :param ticker: Ticker name of file in data folder
    :return: Dask DataFrame
    """
    logging.info(f'extracting data for {ticker}')

    # reads csv data from parent data folder
    df = dd.read_csv(f'../../data/{ticker}.csv')
    df['ticker'] = ticker
    return df


def transform(df, ticker):
    """
    Transform, clean and enrich original data
    :param df: Dask DataFrame
    :param ticker: ticker
    :return: Pandas Dataframe
    """
    logging.info(f'transforming data for {ticker}')

    # rename columns
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


def load(df, file_path, ticker):
    """
    Load data into Parquet file (for this example)
    :param df: Dask DataFrame
    :param file_path: path to store data
    :param ticker: ticker
    :return: None
    """
    logging.info(f'loading data for {ticker}')
    df.to_parquet(file_path, engine='pyarrow', write_index=False, append=True)


def pipeline(tickers, parquet_file_path, in_parallel=True):
    """
    Pipeline orchestrator function
    :param tickers: list()
    :param parquet_file_path: string
    :param in_parallel: bool
    :return: None
    """
    for ticker in tickers:
        if in_parallel:
            logging.info('pipeline commencing in parallel...')
            ticker_df = dask.delayed(extract)(ticker=ticker)
            transform_df = dask.delayed(transform)(ticker_df, ticker=ticker)
            dask.delayed(load)(transform_df, parquet_file_path, ticker=ticker)

        else:
            logging.info('pipeline commencing in parallel...')
            ticker_df = extract(ticker=ticker)
            transform_df = transform(ticker_df, ticker=ticker)
            load(transform_df, parquet_file_path, ticker=ticker)


def pipeline_manager(parquet_file, in_parallel=True):
    """
    Pipeline manager function
    :param parquet_file: str
    :param in_parallel: bool
    :return: None
    """
    tickers = 'AAPL,AMZN,FB,IBM,MSFT'.split(',')

    if in_parallel:
        dask.compute(pipeline(tickers=tickers, parquet_file_path=parquet_file, in_parallel=in_parallel))
    else:
        pipeline(tickers=tickers, parquet_file_path=parquet_file, in_parallel=in_parallel)


def read_parquet(file_name):
    """
    Test data in parquet file by returning average est_turnover by ticker
    :param file_name: location of parquet file
    :return: console output
    """
    df = dd.read_parquet(file_name, engine='pyarrow')
    print(df.groupby('ticker').turnover.mean().compute())


if __name__ == '__main__':
    parquet_file = '../../data/etl_dask.parquet'
    # pipeline_manager(parquet_file)
    read_parquet(parquet_file)
