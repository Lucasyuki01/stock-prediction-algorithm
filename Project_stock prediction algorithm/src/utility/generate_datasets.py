from src.helpers.download_prices import prices
from src.helpers.indicators import (
    RSI,
    MA,
    MACD,
    EMA,
    volatility,
    lag_n,
    vwap,
    detrend,
    Bin_RSI,
    CCI,
    SOSC,
    Bin_SOSC,
    zscore,
    RSL,
    direcao,
    direcao_per,
    distance,
)


def create_indicators(df, indicators):
    """
    describe
    """
    for ind in indicators:
        params = indicators[ind]

        if params["ind"] == "RSI":
            df[
                ind
                + "_"
                + params["ticker"]
                + "_"
                + params["column"]
                + "_"
                + str(params["period"])
            ] = RSI(df[f"{params['column']}_{params['ticker']}"], params["period"])

        if params["ind"] == "Bin_RSI":
            (
                df[
                    "RSI_H_"
                    + params["ticker"]
                    + "_"
                    + params["column"]
                    + "_"
                    + str(params["period"])
                ],
                df["RSI_L_" + str(params["period"])],
            ) = Bin_RSI(
                df[params["column"] + "_" + params["ticker"]],
                params["period"],
                params["ema"],
                params["high"],
                params["low"],
            )

        elif params["ind"] == "MA":
            df[
                ind
                + "_"
                + params["ticker"]
                + "_"
                + params["column"]
                + "_"
                + str(params["period"])
            ] = MA(df[f"{params['column']}_{params['ticker']}"], params["period"])

        elif params["ind"] == "DIR":
            df[ind] = direcao(df, params["ticker"])

        elif params["ind"] == "DIR_p":
            df[ind + "_" + params["ticker"] + "_" + str(params["period"])] = (
                direcao_per(df, params["ticker"], params["period"])
            )

        elif params["ind"] == "CCI":
            df[ind + params["ticker"] + "_" + str(params["period"])] = CCI(
                df, params["ticker"], params["period"]
            )

        elif params["ind"] == "zscore":
            df[ind] = zscore(df["Close_" + params["ticker"]], params["period"])

        elif params["ind"] == "RSL":
            df[ind + str(params["column"]) + str(params["period"])] = RSL(
                df[params["column"] + "_" + params["ticker"]], params["period"]
            )

        elif params["ind"] == "SOSC":
            df[ind + str(params["period"])] = SOSC(
                df, params["ticker"], params["period"]
            )

        elif params["ind"] == "Bin_SOSC":
            df["SOSC_H"], df["SOSC_L"] = Bin_SOSC(
                df, params["ticker"], params["period"]
            )

        elif params["ind"] == "detrend":
            df[
                ind
                + "_"
                + params["ticker"]
                + "_"
                + params["column"]
                + "_"
                + str(params["period"])
            ] = detrend(df[f"{params['column']}_{params['ticker']}"], params["period"])

        elif params["ind"] == "EMA":
            df[ind] = EMA(
                df[f"{params['column']}_{params['ticker']}"], params["period"]
            )

        elif params["ind"] == "MACD":
            df[ind], df[f"{ind}_signal"], df[f"{ind}_crossovers"] = MACD(
                df[f"{params['column']}_{params['ticker']}"]
            )

        elif params["ind"] == "volatility":
            df = volatility(df, params["ticker"], params["period"])

        elif params["ind"] == "lag":
            df = lag_n(df, params["ticker"], params["period"])

        elif params["ind"] == "VWAP":
            df[ind] = vwap(df, params["ticker"], params["period"])


        elif params["ind"] == "distance":
            df["distance"] = distance(df)

    return df


def create_df(tickers, indicators, start, end, interval="1d", update=True):
    """
    describe
    """
    df = prices(tickers, start, end, interval, update)
    df.dropna(inplace=True)

    df = create_indicators(df, indicators)
    return df
