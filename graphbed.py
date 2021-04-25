import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from dash_html_components.Button import Button
import plotly.express as px

import pandas as pd
import sqlite3 as sl
import uuid
import datetime as dt4
import julian
import numpy as np

# external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

#######################################
## SETTING UP DATABASE AND FUNCTIONS ##
#######################################

#####################
## DASH APP LAYOUT ##
#####################

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = \
dbc.Container\
([
    html.Br(),
    dbc.Row([
    dbc.Col([dbc.Button("row 1 col 1",style={"width":"100%"})],width=3),
    dbc.Col([dbc.Button("row 1 col 2", style={"width": "100%"})],width=3),
    # dbc.Col([dbc.Button("row 1 col 3",style={"width":"100%"})],width=3),
    # dbc.Col([dbc.Button("row 1 col 4",style={"width":"100%"})],width=3),
    ], justify="center"),
    html.Br(),
    dbc.Row([
    dbc.Col([dbc.Button("row 2 col 1",style={"width":"100%"})],width=3),
    dbc.Col([dbc.Button("row 2 col 2", style={"width": "100%"})],width=3),
    dbc.Col([dbc.Button("row 2 col 3",style={"width":"100%"})],width=6),
    ]),
    html.Br(),
    dbc.Row([
    dbc.Col([dbc.Button("row 3 col 1",style={"width":"100%"})],width=9),
    dbc.Col([dbc.Button("row 3 col 2", style={"width": "100%"})],width=3),
    ])
])


if __name__ == '__main__':
    app.run_server(debug=True)

