import requests
from api.resources import asset_prices as ap
import pandas as pd


def get_ticker_data(ticker):
    url = f'http://localhost:5000/{ticker}'
    req = requests.get(url)
    price_message = ap.byte_to_message(req.content)
    price_dict = ap.message_to_dict(price_message)
    price_df = pd.DataFrame(price_dict.get('price'))
    return price_df


if __name__ == '__main__':
    get_ticker_data('AAPL')