import protos.asset_prices_pb2 as ap
import pandas as pd
from google.protobuf.json_format import MessageToJson
from google.protobuf.json_format import MessageToDict
from datetime import datetime as dt
import dask.dataframe as dd


def get_ticker_data_dask(ticker, file_path):
    df = dd.read_parquet(file_path, columns=['ticker', 'date', 'adj_close', 'volume', 'pct_chg_1d'])
    df = df[df.ticker == ticker]
    return df.compute()


def get_ticker_data_pandas(ticker, file_path):
    df = pd.read_parquet(file_path, columns=['ticker', 'date', 'adj_close', 'volume', 'pct_chg_1d'])
    df = df[df.ticker == ticker]
    return df


def asset_price_message_from_df(ticker, prices_df):
    asset = ap.Asset()
    asset.symbol = ticker

    for ix, row in prices_df.iterrows():
        asset_price = asset.price.add()
        asset_price.date = dt.strftime(row['date'], '%Y-%m-%d')
        asset_price.close_adj = row['adj_close']
        asset_price.volume = row['volume']

    return asset


def asset_message_from_df(ticker, prices_df):
    asset = ap.Asset()
    asset.symbol = ticker

    for ix, row in prices_df.iterrows():
        asset_price = asset.price.add()
        asset_price.date = dt.strftime(dt.strptime(row['Date'], '%m/%d/%y'), '%Y-%m-%d')
        asset_price.open = row['Open']
        asset_price.high = row['High']
        asset_price.low = row['Low']
        asset_price.close = row['Close']
        asset_price.close_adj = row['Adj Close']
        asset_price.volume = row['Volume']

    return asset


def message_to_bytes(message):
    return message.SerializeToString()


def message_to_json(message):
    return MessageToJson(message, preserving_proto_field_name=True)


def message_to_dict(message):
    return MessageToDict(message, preserving_proto_field_name=True)


def message_bytes_to_disk(message_bytes, file_path):
    with open(file_path, 'wb') as f:
        f.write(message_bytes)


def byte_file_to_message(file_path):
    asset = ap.Asset()
    with open(file_path, "rb") as f:
        asset.ParseFromString(f.read())
        return asset


def byte_to_message(bytes_raw):
    asset = ap.Asset()
    asset.ParseFromString(bytes_raw)
    return asset


def get_asset_prices(ticker, parquet_path, data_format=None):
    df = get_ticker_data_pandas(ticker=ticker, file_path=parquet_path)
    asset_message = asset_price_message_from_df(ticker, df)
    if data_format == 'bytes':
        return message_to_bytes(asset_message)
    elif data_format == 'json':
        return message_to_json(asset_message)
    else:
        return message_to_dict(asset_message)

#
# if __name__ == '__main__':
#     asset_data = get_asset_prices('AAPL', '../data/etl.parquet', 'json')
#     print(asset_data)
