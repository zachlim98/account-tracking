import datetime as dt
import dash_bootstrap_components as dbc
from dash_bootstrap_components._components.Label import Label
import dash_core_components as dcc
import dash_html_components as html

def update_layout(menu_items):
    entry_date = dbc.FormGroup(
        [
            dbc.Label("Entry Date: ", className="mr-2"),
            dcc.DatePickerSingle(
                id="entry-date",
                initial_visible_month = dt.date.today()
            )
        ]
    )

    ticker_form = dbc.FormGroup(
        [
            dbc.Label("Ticker: ", className="mr-2"),
            dcc.Dropdown(
                id = "ticker-select",
                options = menu_items,
                style=dict(width="150px"),
            )
        ],
        row=True
    )

    strike_1 = dbc.Form(
    [
        dbc.FormGroup(
            [
                dbc.Label("Strike 1: ", className="mr-2"),
                dbc.Input(id="strike1", type="number"),
            ],
            className="mr-3",
        ),
        dbc.FormGroup(
            [
                dbc.RadioItems(id="strike1-type",
                options=[{"label":"Call", "value":1}, 
                {"label":"Put","value":0}]),
            ],
            className="mr-3"
        ),
        dbc.FormGroup(
            [
                dcc.DatePickerSingle(
                id="strike1-date",
                initial_visible_month=dt.date.today()
                )
            ],
            className="ml-3",
        )
    ],
    inline=True,
    )

    strike_2 = dbc.Form(
    [
        dbc.FormGroup(
            [
                dbc.Label("Strike 2: ", className="mr-2"),
                dbc.Input(id="strike2", type="number"),
            ],
            className="mr-3",
        ),
        dbc.FormGroup(
            [
                dbc.RadioItems(id="strike2-type",
                options=[{"label":"Call", "value":1}, 
                {"label":"Put","value":0}]),
            ],
            className="mr-3"
        ),
        dbc.FormGroup(
            [
                dcc.DatePickerSingle(
                id="strike2-date",
                initial_visible_month=dt.date.today()
                )
            ],
            className="ml-3",
        )
    ],
    inline=True,
    )

    strike_3 = dbc.Form(
    [
        dbc.FormGroup(
            [
                dbc.Label("Strike 3: ", className="mr-2"),
                dbc.Input(id="strike3", type="number"),
            ],
            className="mr-3",
        ),
        dbc.FormGroup(
            [
                dbc.RadioItems(id="strike3-type",
                options=[{"label":"Call", "value":1}, 
                {"label":"Put","value":0}]),
            ],
            className="mr-3"
        ),
        dbc.FormGroup(
            [
                dcc.DatePickerSingle(
                id="strike3-date",
                initial_visible_month=dt.date.today()
                )
            ],
            className="ml-3",
        )
    ],
    inline=True,
    )

    strike_4 = dbc.Form(
    [
        dbc.FormGroup(
            [
                dbc.Label("Strike 4: ", className="mr-2"),
                dbc.Input(id="strike4", type="number"),
            ],
            className="mr-3",
        ),
        dbc.FormGroup(
            [
                dbc.RadioItems(id="strike4-type",
                options=[{"label":"Call", "value":1}, 
                {"label":"Put","value":0}]),
            ],
            className="mr-3"
        ),
        dbc.FormGroup(
            [
                dcc.DatePickerSingle(
                id="strike4-date",
                initial_visible_month=dt.date.today()
                )
            ],
            className="ml-3",
        )
    ],
    inline=True,
    )

    btn = dbc.Button(
        "Submit", color="primary", id="my-button"
    )

    btn_close = dbc.Button(
        "Close", color="danger", id="my-button-close"
    )

    form = dbc.Container([
                dbc.Row(
                    [
                        dbc.Col(entry_date,
                        width={"size":2, "offset":4}),
                        dbc.Col(ticker_form,
                        width={"size":3})
                    ]
                ),
                dbc.Row(
                    [
                        dbc.Col(strike_1, width={"offset":4}),
                    ]
                ),
                dbc.Row(
                    [
                        dbc.Col(strike_2, width={"offset":4})
                    ]
                ),
                dbc.Row(
                    [
                        dbc.Col(strike_3, width={"offset":4})
                    ]
                ),
                dbc.Row(
                    [
                        dbc.Col(strike_4, width={"offset":4})
                    ]
                ),
                html.Br(),
                dbc.Row(
                    [
                        dbc.Col([dbc.FormGroup([
                            dbc.Label("Net Cost: "),
                            dcc.Input(id="net-cost", type="number")])], width=2),
                        dbc.Col([dbc.FormGroup([
                            dbc.Label("Trade Price: "),
                            dcc.Input(id="trade-price", type="number")])], width=2),
                        dbc.Col([dbc.FormGroup([
                            dbc.Label("Strategy: "),
                            dcc.Input(id='strat', type="text")])],width=2)
                    ], justify="center"
                ),
                dbc.Row(
                    [
                        dbc.Col(btn, width={"offset":5}),
                        dbc.Col(btn_close)
                    ]
                ),

                dbc.Row(
                    [
                        dbc.Col(html.P(id="my-output"))
                    ]
                )
    ])

    return form


def new_trade_layout():
    entry_date = dbc.FormGroup(
        [
            dbc.Label("Entry Date: ", className="mr-2"),
            dcc.DatePickerSingle(
                id="entry-date-new",
                initial_visible_month = dt.date.today()
            )
        ]
    )

    ticker_form = dbc.FormGroup(
        [
            dbc.Label("Ticker: ", className="mr-2"),
            dcc.Input(id="ticker-new", type="text")
        ],
        row=True
    )

    strike_1 = dbc.Form(
    [
        dbc.FormGroup(
            [
                dbc.Label("Strike 1: ", className="mr-2"),
                dbc.Input(id="strike1-new", type="number"),
            ],
            className="mr-3",
        ),
        dbc.FormGroup(
            [
                dbc.RadioItems(id="strike1-type-new",
                options=[{"label":"Call", "value":1}, 
                {"label":"Put","value":0}]),
            ],
            className="mr-3"
        ),
        dbc.FormGroup(
            [
                dcc.DatePickerSingle(
                id="strike1-date-new",
                initial_visible_month=dt.date.today()
                )
            ],
            className="ml-3",
        )
    ],
    inline=True,
    )

    strike_2 = dbc.Form(
    [
        dbc.FormGroup(
            [
                dbc.Label("Strike 2: ", className="mr-2"),
                dbc.Input(id="strike2-new", type="number"),
            ],
            className="mr-3",
        ),
        dbc.FormGroup(
            [
                dbc.RadioItems(id="strike2-type-new",
                options=[{"label":"Call", "value":1}, 
                {"label":"Put","value":0}]),
            ],
            className="mr-3"
        ),
        dbc.FormGroup(
            [
                dcc.DatePickerSingle(
                id="strike2-date-new",
                initial_visible_month=dt.date.today()
                )
            ],
            className="ml-3",
        )
    ],
    inline=True,
    )

    strike_3 = dbc.Form(
    [
        dbc.FormGroup(
            [
                dbc.Label("Strike 3: ", className="mr-2"),
                dbc.Input(id="strike3-new", type="number"),
            ],
            className="mr-3",
        ),
        dbc.FormGroup(
            [
                dbc.RadioItems(id="strike3-type-new",
                options=[{"label":"Call", "value":1}, 
                {"label":"Put","value":0}]),
            ],
            className="mr-3"
        ),
        dbc.FormGroup(
            [
                dcc.DatePickerSingle(
                id="strike3-date-new",
                initial_visible_month=dt.date.today()
                )
            ],
            className="ml-3",
        )
    ],
    inline=True,
    )

    strike_4 = dbc.Form(
    [
        dbc.FormGroup(
            [
                dbc.Label("Strike 4: ", className="mr-2"),
                dbc.Input(id="strike4-new", type="number"),
            ],
            className="mr-3",
        ),
        dbc.FormGroup(
            [
                dbc.RadioItems(id="strike4-type-new",
                options=[{"label":"Call", "value":1}, 
                {"label":"Put","value":0}]),
            ],
            className="mr-3"
        ),
        dbc.FormGroup(
            [
                dcc.DatePickerSingle(
                id="strike4-date-new",
                initial_visible_month=dt.date.today()
                )
            ],
            className="ml-3",
        )
    ],
    inline=True,
    )

    btn = dbc.Button(
        "Submit", color="primary", id="my-button-new"
    )

    form = dbc.Container([
                dbc.Row(
                    [
                        dbc.Col(entry_date,
                        width={"size":2, "offset":4}),
                        dbc.Col(ticker_form,
                        width={"size":3})
                    ]
                ),
                dbc.Row(
                    [
                        dbc.Col(strike_1, width={"offset":4}),
                    ]
                ),
                dbc.Row(
                    [
                        dbc.Col(strike_2, width={"offset":4})
                    ]
                ),
                dbc.Row(
                    [
                        dbc.Col(strike_3, width={"offset":4})
                    ]
                ),
                dbc.Row(
                    [
                        dbc.Col(strike_4, width={"offset":4})
                    ]
                ),
                html.Br(),
                dbc.Row(
                    [
                        dbc.Col([dbc.FormGroup([
                            dbc.Label("Net Cost: "),
                            dcc.Input(id="net-cost-new", type="number")])], width=2),
                        dbc.Col([dbc.FormGroup([
                            dbc.Label("Trade Price: "),
                            dcc.Input(id="trade-price-new", type="number")])], width=2),
                        dbc.Col([dbc.FormGroup([
                            dbc.Label("Strategy: "),
                            dcc.Input(id='strat-new', type="text")])],width=2)
                    ], justify="center"
                ),
                dbc.Row(
                    [
                        dbc.Col(btn, width={"offset":5})
                    ]
                ),

                dbc.Row(
                    [
                        dbc.Col(html.P(id="my-output-new"))
                    ]
                )
    ])

    return form