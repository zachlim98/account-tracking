import uuid
import pandas as pd
import datetime as dt

# creation of new entry
def create_new_entry(entry_date, ticker, stk1, s1t, s1e, stk2, s2t, s2e, stk3, s3t, s3e, stk4, s4t, s4e, cost, trdprice, strategy):
    """
    This function creates a list for entry
    """
    entry = [
        (str(uuid.uuid4()), entry_date, ticker, stk1, s1t, s1e, stk2, s2t, s2e, stk3, s3t, s3e, stk4, s4t, s4e, 
        cost, trdprice, (((stk2-stk1)*100)-cost), strategy)
    ]

    return entry

# function to update trade (with uuid)
def update_trade(uuid, entry_date, ticker, stk1, s1t, s1e, stk2, s2t, s2e, stk3, s3t, s3e, stk4, s4t, s4e, 
cost, trdprice, strategy):
    """
    This function is to help you prepare trade information in the right format for writing to the database
    """
    entry = [
    (uuid, entry_date, ticker, stk1, s1t, s1e, stk2, s2t, s2e, stk3, s3t, s3e, stk4, s4t, s4e, 
    cost, trdprice, (((stk2-stk1)*100)-cost), strategy)
]
    return entry


# function for entering trade
def enter(dbcon, new_entryl):
    """
    This function directly enters the information into the database
    """
    sql = """
        INSERT INTO TRADE_MAIN(
        trade_group_id, 
        entry_date,
        ticker,
        stk1 ,
        stk1_type,
        stk1_exp,
        stk2,
        stk2_type,
        stk2_exp,
        stk3 ,
        stk3_type,
        stk3_exp,
        stk4,
        stk4_type,
        stk4_exp,
        cost,
        trdprice,
        BRP,
        strategy
        ) VALUES (?, julianday(?),?,?,?,julianday(?),?,?,julianday(?),?,?,julianday(?),?,?,julianday(?),?,?,?,?)

    """
    with dbcon:
        dbcon.executemany(sql,new_entryl)

# Inserts new entry, create aggregate into overview table, transfers to historical table
def close(dbcon, close_entry):
    """
    This function helps to close a trade
    """

    uuid = close_entry[0][0]

    sql = """
        INSERT INTO TRADE_MAIN(
        trade_group_id, 
        entry_date,
        ticker,
        stk1 ,
        stk1_type,
        stk1_exp,
        stk2,
        stk2_type,
        stk2_exp,
        stk3 ,
        stk3_type,
        stk3_exp,
        stk4,
        stk4_type,
        stk4_exp,
        cost,
        trdprice,
        BRP,
        strategy 
        ) VALUES (?, julianday(?),?,?,?,julianday(?),?,?,julianday(?),?,?,julianday(?),?,?,julianday(?),?,?,?,?)

    """
    with dbcon:
        dbcon.executemany(sql,close_entry)

    data = dbcon.execute(f"""
    SELECT ticker, max(date(entry_date)), min(date(entry_date)), sum(trdprice), sum(cost), min(stk1), stk2 FROM TRADE_MAIN
    WHERE trade_group_id = '{uuid}'
    """)

    for i in data:
        ticker = i[0]
        exit_date = str(i[1])
        entry_date = str(i[2])
        days_in_trade = (dt.datetime.strptime(exit_date, '%Y-%m-%d').date() - dt.datetime.strptime(entry_date, '%Y-%m-%d').date()).days
        pnl = round(i[4],2)
        stk_width = i[-1] - i[-2]
        strat = i[-1]

    update_close = [(entry_date, exit_date, days_in_trade,ticker,stk_width,pnl,strat)]

    sql2 = """
        INSERT INTO TRADE_SUMMARY( 
        entry_date,
        exit_date,
        trade_length,
        ticker,
        stk_width,
        pnl,
        strategy
        ) VALUES (julianday(?),julianday(?),?,?,?,?,?)
    """
     
    sql3 = f"""

    INSERT INTO TRADE_HIST 
    SELECT * FROM TRADE_MAIN
    WHERE trade_group_id = '{uuid}'

    """

    sql4 = f"""

        DELETE FROM TRADE_MAIN
        WHERE trade_group_id = '{uuid}'

    """

    with dbcon:
        dbcon.executemany(sql2, update_close)
        dbcon.execute(sql3)
        dbcon.execute(sql4)

def get_stats(con):
    data = con.execute(f"""
    SELECT ticker, date(entry_date), sum(trdprice), sum(cost), stk1, stk2 FROM TRADE_MAIN
    GROUP BY trade_group_id
""")

    for i in data:
        ticker = i[0]
        exp_date = dt.datetime.strptime(i[1], '%Y-%m-%d').date()
        dte = (exp_date - dt.date.today()).days
        bes = round(i[-1] - i[2],1)
        bem = i[2]
        bema = round(i[3]/100,2)
        m50 = round(i[2]/2,2)
        cost = round(i[-3],2)
        return ticker, exp_date, dte, bes, bem, bema, m50, cost

# def get_stats(dbcon, uuid):
#     data = dbcon.execute(f"""
#     SELECT ticker, sum(cost) FROM TRADE_MAIN
#     WHERE trade_group_id = '{uuid}'
# """)

#     for i in data:
#         ticker = i[0]
#         cost = i[1]
#         return ticker, cost

def stats_table(con):
    data2 = con.execute(f"""
    SELECT ticker, date(entry_date), sum(trdprice), sum(cost), stk1, stk2 FROM TRADE_MAIN
    GROUP BY trade_group_id
""")

    ticker = []
    start_date = []
    be_price = []
    cost = []
    stk1 = []
    stk2 = []
    be50 = []

    for i in data2:
        ticker.append(i[0])
        start_date.append(i[1])
        cost.append(round(i[3]/100,2))
        be50.append(round(i[3]/100/2,2))
        stk1.append(i[4])
        stk2.append(i[5])
        be_price.append(int(i[-2])-round(i[3]/100,2))

    trade_overview = pd.DataFrame({
        "ticker": ticker,
        "date": start_date,
        "Breakeven" : cost,
        "Breakeven 50" : be50,
        # "Strike 1" : stk1,
        # "Strike 2" : stk2,
        "Breakeven Stock Price" : be_price
    })

    return trade_overview