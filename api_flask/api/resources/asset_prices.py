import protos.asset_prices_pb2 as ap
import pandas as pd
from google.protobuf.json_format import MessageToJson
from google.protobuf.json_format import MessageToDict
from datetime import datetime as dt
import dask.dataframe as dd


def get_ticker_data_dask(ticker: str, file_path: str) -> pd.DataFrame():
    """
    Get ticker data using Dask
    :param ticker: string -> ticker for hist data
    :param file_path: string -> path to parquet file
    :return: DataFrame
    """
    df = dd.read_parquet(file_path, columns=['ticker', 'date', 'adj_close', 'volume', 'pct_chg_1d'])
    df = df[df.ticker == ticker]
    return df.compute()


def get_ticker_data_pandas(ticker: str, file_path: str) -> pd.DataFrame():
    """
    Get ticker data using Pandas
    :param ticker: string -> ticker for hist data
    :param file_path: string -> path to parquet file
    :return: DataFrame
    """
    df = pd.read_parquet(file_path, columns=['ticker', 'date', 'adj_close', 'volume', 'pct_chg_1d'])
    df = df[df.ticker == ticker]
    return df


def asset_price_message_from_df(ticker: str, prices_df: pd.DataFrame()) -> ap.Asset():
    """
    Converts a pricing DataFrame to a Protobuf Message
    :param ticker: string -> stock ticker
    :param prices_df: DataFrame -> stock prices
    :return: ap.Asset() message
    """
    asset = ap.Asset()
    asset.symbol = ticker

    for ix, row in prices_df.iterrows():
        asset_price = asset.price.add()
        asset_price.date = dt.strftime(row['date'], '%Y-%m-%d')
        asset_price.close_adj = row['adj_close']
        asset_price.volume = row['volume']

    return asset


def message_to_bytes(message):
    """
    Converts an ap.Asset() message to byte string
    :param message: ap.Asset()
    :return: string -> byte message
    """
    return message.SerializeToString()


def message_to_json(message):
    """
    Converts an ap.Asset() message to json string
    :param message: ap.Asset()
    :return: string -> json message
    """
    return MessageToJson(message, preserving_proto_field_name=True)


def message_to_dict(message):
    """
    Converts an ap.Asset() message to dictionary
    :param message: ap.Asset()
    :return: dict() -> message objects
    """
    return MessageToDict(message, preserving_proto_field_name=True)


def message_bytes_to_disk(message_bytes, file_path):
    """
    Writes byte string to local dick
    :param message_bytes: string -> byte string
    :param file_path: string -> path to disk
    :return: None
    """
    with open(file_path, 'wb') as f:
        f.write(message_bytes)


def byte_file_to_message(file_path):
    """
    Reads bytes on disk and returns ap.Asset() message
    :param file_path: string -> path to disk
    :return: ap.Asset()
    """
    asset = ap.Asset()
    with open(file_path, "rb") as f:
        asset.ParseFromString(f.read())
        return asset


def byte_to_message(bytes_raw):
    """
    Converts byte string to message
    :param bytes_raw: string - bytes
    :return: ap.Asset()
    """
    asset = ap.Asset()
    asset.ParseFromString(bytes_raw)
    return asset


def get_asset_prices(ticker, parquet_path, data_format=None):
    """
    The main function to read data from local parquet file and return data in
    desired format.
    :param ticker: string
    :param parquet_path: string -> path to parquet file on disk
    :param data_format: string -> can be json, bytes or dict
    :return: bytes, json or dict
    """
    df = get_ticker_data_dask(ticker=ticker, file_path=parquet_path)
    asset_message = asset_price_message_from_df(ticker, df)
    if data_format == 'bytes':
        return message_to_bytes(asset_message)
    elif data_format == 'json':
        return message_to_json(asset_message)
    else:
        return message_to_dict(asset_message)


# if __name__ == '__main__':
#     asset_data = get_asset_prices('AAPL', '../data/etl.parquet')
#     print(asset_data)
