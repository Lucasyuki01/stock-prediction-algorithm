import requests, datetime, yfinance, pandas as pd
from src.helpers import data_fb


def search_bacen(cod_bacen):
    start = pd.to_datetime("1980-01-01")
    end = pd.Timestamp.now()

    url = f"http://api.bcb.gov.br/dados/serie/bcdata.sgs.{cod_bacen}/dados?formato=json"
    df = pd.read_json(url)
    df["data"] = pd.to_datetime(df["data"])
    df = df.rename(columns={"data": "Date", "valor": "Close"})

    i = start
    days = []
    while i < end - pd.Timedelta(days=1):
        i += pd.Timedelta(days=1)
        days.append(i)

    df2 = pd.DataFrame({"Date": days})
    df_all = pd.merge(df2, df, how="left", on="Date")

    aux = []
    last = 0
    for i in df_all["Close"]:
        if not pd.isnull(i):
            last = i
        else:
            i = last

        aux.append(i)

    df_all["Close"] = aux
    df_all["Open"] = df_all["Close"].shift(1)
    return df_all


def yf_process(ticker, interval):
    stock = yfinance.Ticker(ticker)
    df = stock.history(period="max", interval=interval)
    df.reset_index(inplace=True)

    return df


def search_stock_real(ticker, interval):
    if ticker == "CDI.VAI":
        df = search_bacen(12)
    else:
        df = yf_process(ticker, interval)

    df["Date"] = [str(i)[:10] for i in df["Date"]]

    return df.dropna()


def search_stock_vulture(ticker, interval):
    data_json = data_fb.search_data(
        f"/databases_apis/{ticker.replace('.','_')}_{interval}"
    )
    database = []
    try:
        for i in data_json.items():
            datas = i[1]
            datas["Date"] = i[0]
            database.append(datas)

        return pd.json_normalize(database)
    except:
        print("No datas in vulture dataset:", ticker)
        return database


def process_databases_apis(ticker, interval, update):
    if update:
        print("Requested update vulture datasets:", ticker)
        df_real = search_stock_real(ticker, interval)
        df_vulture = search_stock_vulture(ticker, interval)

        if len(df_real) > len(df_vulture):
            data_fb.update_data(
                f"/databases_apis/{ticker.replace('.','_')}_{interval}",
                df_real.set_index("Date").to_dict(orient="index"),
            )
            return df_real
        else:
            return df_vulture

    else:
        print("Direct request from vulture datasets:", ticker)
        df_vulture = search_stock_vulture(ticker, interval)
        if len(df_vulture) > 0:
            return df_vulture
        else:
            print("Vulture datasets not exist: update=True required")


def vulture_prices_process(ticker, start, end, interval="1d", update=True):
    df = process_databases_apis(ticker, interval, update)    
    df_filtered = df[(df["Date"] >= start) & (df["Date"] <= end)]

    if ticker == "CDI.VAI":
        df_filtered["Cumulative day"] = df_filtered["Close"].cumsum()

    return df_filtered.set_index("Date")
