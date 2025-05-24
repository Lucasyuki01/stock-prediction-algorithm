import pandas as pd
from src.helpers.prices_apis_valid import vulture_prices_process


def prices(tickers, start, end=None, interval="1d", update=True):
    """
    ### IMPORT OF MARKET PRICES
    Check tickers in https://finance.yahoo.com

    tickers (exemple): {
        'ticker1': ['Open', 'High', 'Low', 'Close', 'Volume'],
        'ticker2': ['Open', 'High', 'Low'], ...}

    start: Search start date in yyyy-mm-dd format

    end: End date for the search in yyyy-mm-dd format (default: now)
    """
    if end == None:
        end = str(pd.Timestamp.now())[:10]

    databases = []
    for ticker in tickers:

        database = vulture_prices_process(ticker, start, end, interval, update=update)
        database = database[tickers[ticker]].copy()
        databases.append(database.add_suffix(f"_{ticker}"))

    concat_dbs = pd.concat(databases, axis=1)  # Concatenate tables based on rows
    try:
        concat_dbs[f"Close_CDI.VAI"].interpolate(method="pad", limit=2, inplace=True)
        concat_dbs[f"Cumulative day_CDI.VAI"].interpolate(
            method="pad", limit=2, inplace=True
        )
        concat_dbs[f"Open_CDI.VAI"].interpolate(method="pad", limit=2, inplace=True)

    except:
        pass

    try:
        concat_dbs["Close_BRL=X"].interpolate(inplace=True)
    except:
        pass

    return concat_dbs
