# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.express as px
import requests
from resources import asset_prices as ap
import pandas as pd


def get_ticker_data(ticker):
    url = f'http://datatools-api/{ticker}'
    req = requests.get(url)
    price_message = ap.byte_to_message(req.content)
    price_dict = ap.message_to_dict(price_message)
    price_df = pd.DataFrame(price_dict.get('price'))
    price_df['pct_chg_1d'] = price_df.close_adj.pct_change(periods=1)
    price_df['ticker'] = ticker
    return price_df


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

app.layout = html.Div([
    html.H2(children='DataTools Dashboard'),
    html.Div(["Select Ticker: ",
              dcc.Dropdown(
                  id='input-1-state',
                  options=[
                      {'label': 'AAPL', 'value': 'AAPL'},
                      {'label': 'AMZN', 'value': 'AMZN'},
                      {'label': 'FB', 'value': 'FB'},
                      {'label': 'IBM', 'value': 'IBM'},
                      {'label': 'MSFT', 'value': 'MSFT'}
                  ],
                  value='AAPL',
                  style=dict(
                      width='120px',
                      display='inline-block',
                      verticalAlign="middle"
                  )
              ),
              html.Button(
                  id='submit-button-state',
                  n_clicks=0,
                  style=dict(
                      width='100px',
                      display='inline-block',
                      verticalAlign="middle"),
                  children='Run')]
             ),
    html.Div(id='output-state')
])


@app.callback(Output('output-state', 'children'),
              [Input('submit-button-state', 'n_clicks')],
              [State('input-1-state', 'value')])
def update_output(n_clicks, input1):
    """
    Callback function for Dashboard
    :param n_clicks: Button click counter
    :param input1: Value of the dropdown
    :return: dash html.Div() with graphs
    """

    # comment out below to use pandas to read the parquet file from data dir
    # df = pd.read_parquet('../data/etl.parquet', columns=['ticker', 'date', 'adj_close', 'pct_chg_1d'])
    # df = df[df.ticker == input1]

    # call api service to get data
    df = get_ticker_data(input1)

    # construct figures for dash output
    fig_line = px.line(df, x="date", y="close_adj", title=f'{input1} Stock History')
    fig_hist = px.histogram(df, x="pct_chg_1d", nbins=300, marginal="box", title=f'{input1} Returns Distribution')

    # construct output object
    output = html.Div([
        dcc.Graph(id='example-graph-1', figure=fig_line),
        dcc.Graph(id='example-graph-2', figure=fig_hist),
    ])

    return output


if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=80)