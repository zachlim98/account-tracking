import dash
from dash_bootstrap_components._components.Button import Button
from dash_bootstrap_components._components.Jumbotron import Jumbotron
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import plotly.express as px

import pandas as pd
import sqlite3 as sl
import uuid
import datetime as dt
import julian
import numpy as np
from functions import enter, create_new_entry, close, update_trade, stats_table
from layout import update_layout, new_trade_layout

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

#######################################
## SETTING UP DATABASE AND FUNCTIONS ##
#######################################

# connect to database
con = sl.connect("mydata.db", check_same_thread=False)

# get list of active trades to present in dropdown
data = con.execute("""
    SELECT * FROM TRADE_MAIN GROUP BY trade_group_id
""")
menu_items = []
for i in data:
    menu_items.append({'label':i[3], 'value':i[1]})

# prepare graph of account balance
balance_sql  = """

SELECT julianday(exit_date), pnl FROM TRADE_SUMMARY ORDER BY exit_date

"""

data = con.execute(balance_sql)

dates = []
pnl = []

for i in data:
    dates.append(julian.from_jd(i[0], fmt='jd').date())
    pnl.append(i[1])

#####################
## DASH APP LAYOUT ##
#####################

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

update_form = update_layout(menu_items)
new_form = new_trade_layout()

app.layout = dbc.Container([
    html.Div([
        html.Div([
            html.Div([
                html.H1("Overview")
            ]),
            dcc.Tabs(id='tabs-sit', value='tab-active', children=[
                dcc.Tab(label="Active Trades", value='tab-active'),
                dcc.Tab(label="Account Graph", value='tab-history')
            ]),
            html.Br(),
            html.Div(id="tabs-sit-output")
        ]),
        html.Br(),
        html.Div([
            html.Div([
                html.H1("Trade Entry")
            ]),
            html.Br(),
            dcc.Tabs(id='tabs-trades', value='tab-update', children=[
                dcc.Tab(label="Update Trades", value='tab-update'),
                dcc.Tab(label="New Trade", value='tab-new')
            ]),
            html.Br(),
            html.Div(id="tabs-output")
        ]),
        html.Br()
    ])
])

########################
## DASH APP FUNCTIONS ##
########################

# changing trade overview tabs
@app.callback(
    Output('tabs-sit-output','children'),
    [Input('tabs-sit', 'value')]
)
def render_content(tab):
    if tab == "tab-active":
        return html.Div([dbc.Table.from_dataframe(stats_table(con), striped=True, bordered=True, hover=True)])
    elif tab == "tab-history":
        return html.Div([dcc.Graph(figure=px.line(x=dates, y=np.cumsum(pnl)))])

# changing trade entry tabs
@app.callback(
    Output('tabs-output','children'),
    Input('tabs-trades', 'value')
)
def render_content(tab):
    if tab == "tab-update":
        return update_form
    elif tab == "tab-new":
        return new_form

# add new trades
@app.callback(
    Output(component_id="my-output-new", component_property="children"),
    [Input('my-button-new','n_clicks')],
    [State(component_id="entry-date-new", component_property='date'),
    State(component_id='ticker-new', component_property='value'),
    State(component_id='strike1-new', component_property='value'),
    State(component_id='strike1-type-new', component_property='value'),
    State(component_id='strike1-date-new', component_property='date'),
    State(component_id='strike2-new', component_property='value'),
    State(component_id='strike2-type-new', component_property='value'),
    State(component_id='strike2-date-new', component_property='date'),
    State(component_id='strike3-new', component_property='value'),
    State(component_id='strike3-type-new', component_property='value'),
    State(component_id='strike3-date-new', component_property='date'),
    State(component_id='strike4-new', component_property='value'),
    State(component_id='strike4-type-new', component_property='value'),
    State(component_id='strike4-date-new', component_property='date'),
    State(component_id='net-cost-new', component_property='value'),
    State(component_id='trade-price-new', component_property='value'),
    State(component_id="strat-new", component_property='value')]
)
def update_value(clicked, entry_date, ticker_label,
strike1, strike1_type, strike1_date, 
strike2, strike2_type, strike2_date,
strike3, strike3_type, strike3_date,
strike4, strike4_type, strike4_date, nc, tp, strat):
    
    entry = create_new_entry(entry_date, ticker_label, strike1, strike1_type, strike1_date, 
strike2, strike2_type, strike2_date, strike3, strike3_type, strike3_date,
strike4, strike4_type, strike4_date, nc, tp, strat)

    enter(con, entry)

    return f"Successfully added: {ticker_label}"


# update trades
@app.callback(
    Output(component_id="my-output", component_property="children"),
    [Input('my-button','n_clicks'),
    Input('my-button-close', 'n_clicks')],
    [State(component_id="entry-date", component_property='date'),
    State(component_id='ticker-select', component_property='value'),
    State(component_id='ticker-select', component_property='options'),
    State(component_id='strike1', component_property='value'),
    State(component_id='strike1-type', component_property='value'),
    State(component_id='strike1-date', component_property='date'),
    State(component_id='strike2', component_property='value'),
    State(component_id='strike2-type', component_property='value'),
    State(component_id='strike2-date', component_property='date'),
    State(component_id='strike3', component_property='value'),
    State(component_id='strike3-type', component_property='value'),
    State(component_id='strike3-date', component_property='date'),
    State(component_id='strike4', component_property='value'),
    State(component_id='strike4-type', component_property='value'),
    State(component_id='strike4-date', component_property='date'),
    State(component_id='net-cost', component_property='value'),
    State(component_id='trade-price', component_property='value'),
    State(component_id="strat", component_property="value")]
)
def update_value(click_update, click_close, entry_date, group_id, ticker_select_l, strike1, strike1_type, strike1_date, 
strike2, strike2_type, strike2_date, 
strike3, strike3_type, strike3_date, 
strike4, strike4_type, strike4_date,nc, tp, strat):

    ticker_name = [x['label'] for x in ticker_select_l if x['value'] == group_id][0]

    if click_update == 1:
    
        entry = update_trade(group_id, entry_date, ticker_name, strike1, strike1_type, strike1_date, 
    strike2, strike2_type, strike2_date, strike3, strike3_type, strike3_date, 
    strike4, strike4_type, strike4_date, nc, tp, strat)

        enter(con, entry)

        return f"Successfully updated: {ticker_name}"

    elif click_close == 1:

        entry = update_trade(group_id, entry_date, ticker_name, strike1, strike1_type, strike1_date, 
    strike2, strike2_type, strike2_date, strike3, strike3_type, strike3_date, 
    strike4, strike4_type, strike4_date, nc, tp, strat)

        close(con, entry)

        return f"Successfully closed: {ticker_name}"

if __name__ == '__main__':
    app.run_server(debug=True)

