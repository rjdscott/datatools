# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.express as px
import pandas as pd

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    html.H1(children='DataTools Dashboard'),
    html.Div([
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
                width='150px',
                display='inline-block',
                verticalAlign="middle")
        )]
    ),
    html.Div([
        html.Button(
            id='submit-button-state',
            n_clicks=0,
            style=dict(
                width='150px',
                display='inline-block',
                verticalAlign="middle"),
            children='Submit')
    ]),
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

    # use pandas to read the parquet file from data dir,
    # todo: update this to call API
    df = pd.read_parquet('../data/etl.parquet', columns=['ticker', 'date', 'adj_close', 'pct_chg_1d'])
    df = df[df.ticker == input1]

    # construct figures for dash output
    fig_line = px.line(df, x="date", y="adj_close", title=f'{input1} Stock History')
    fig_hist = px.histogram(df, x="pct_chg_1d", nbins=300, marginal="box", title=f'{input1}Returns Distribution')

    # construct output object
    output = html.Div([
        dcc.Graph(id='example-graph-1', figure=fig_line),
        dcc.Graph(id='example-graph-2', figure=fig_hist),
    ])

    return output


if __name__ == '__main__':
    app.run_server(debug=True)