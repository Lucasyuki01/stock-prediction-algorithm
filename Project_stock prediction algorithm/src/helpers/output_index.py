import pandas as pd
import numpy as np


def percent_return(data, ticker, preds=[]):
    """
    - param data: Pandas DataFrame with data regarding the period
    - param ticker: Stock ticker name, or Ibovespa
    - param preds: Model prediction regarding the data from _data_

    - return: retp, retp_m
    """

    perc = pd.DataFrame(data["Close_" + ticker]).pct_change()
    # perc.dropna(inplace=True)
    perc.fillna(0, inplace=True)
    retp = 100 * perc["Close_" + ticker]

    if len(preds) > 0:
        if len(preds) > len(perc):
            pred = preds
            print("Wrong dimension", pred.shape)
        else:
            pred = np.concatenate((np.zeros(1), preds))
        retp_m = pred[:-1] * retp
    else:
        retp_m = []

    return retp, retp_m


def percent_return_p(data, period, ticker, preds=[]):
    """
    - param data: Pandas DataFrame with data regarding the period
    - param ticker: Stock ticker name, or Ibovespa
    - param preds: Model prediction regarding the data from _data_

    - return: retp, retp_m
    """

    perc = pd.DataFrame(data["Close_" + ticker]).pct_change(period)
    # perc.dropna(inplace=True)
    perc.fillna(0, inplace=True)
    retp = 100 * perc["Close_" + ticker]

    retp_m = np.zeros(len(perc))

    #print("Len", len(retp), len(preds), len(perc))

    for i in range(period, len(perc)):
        retp_m[i] = preds[i - period] * retp.iloc[i]

    return retp, pd.Series(retp_m)


def sharpe(return_series, annualize, rf=0):
    """
    Calculate sharpe ratio

    - param return_series: DataFrame or array with percentual returns regarding the period in analysis
    - param annualize: int periods to use for annualization (252 daily, 12 monthly, 4 quarterly)
    - param rf: float risk-free rate in decimal format (e.g., selic, ipca,... -> renda fixa)

    - return: float sharpe ratio
    - Ref: https://www.codearmo.com/blog/sharpe-sortino-and-calmar-ratios-python
    """
    mean = return_series.mean() * annualize - rf
    sigma = return_series.std() * np.sqrt(annualize)

    return mean / sigma


def patrimony(data, ticker, preds, qtd=1):
    """
    - param data: Pandas DataFrame with data regarding the period
    - param ticker: Stock ticker name, or Ibovespa
    - param preds: Model prediction regarding the data from _data_
    - param qtd: Amount of stock on the fractionary market (default: 1)

    - return: ret, ret_m
    """
    ret = [qtd * (data["Close_" + ticker][0])]
    ret_m = [qtd * (data["Close_" + ticker][0])]

    if len(preds) > 0:
        if len(preds) <= len(data):
            preds = np.concatenate((np.zeros(1), preds))
    # preds = preds.reshape((len(preds), 1))

    for i in range(1, len(data)):
        # ret.append(ret[i-1]+qtd*(data['Close_'+ticker][i]-data['Open_'+ticker][i]))
        # ret_m.append(ret_m[i-1]+(qtd*preds[i-1]*(data['Close_'+ticker][i]-data['Open_'+ticker][i])).item())
        # ret.append(ret[i-1]+(data['Close_'+ticker][i] - data['Open_'+ticker][i]))
        ret.append(data["Close_" + ticker][i])
        ret_m.append(
            ret_m[i - 1]
            + (
                preds[i] * (data["Close_" + ticker][i] - data["Open_" + ticker][i])
            ).item()
        )

    ret = np.array(ret).reshape((len(ret), 1))
    ret_m = np.array(ret_m).reshape((len(ret_m), 1))

    # ret_m = pd.DataFrame(ret_m)
    # ret = pd.DataFrame(ret)

    return ret, ret_m


def drawdown(data, ticker, preds, qtd=1, percent=True, days=1):
    """
    - param data: Pandas DataFrame with data regarding the period
    - param ticker: Stock ticker name, or Ibovespa
    - param preds: Model prediction regarding the data from _data_
    - param qtd: Amount of stock on the fractionary market (default: 1)
    - param percent: If True, employs percent_return, otherwise cumulative patrimony

    - return: drawdown_default, drawdown_model (pd.Series)
    """

    ret, ret_m = 0, 0

    if percent:
        # ret, ret_m = percent_return(data, ticker, preds)
        ret, ret_m = percent_return_p(data, days, ticker, preds)
        ret /= 100
        ret_m /= 100
    else:
        ret, ret_m = patrimony(data, ticker, preds, qtd)

    wea_idx = qtd * (ret + 1).cumprod()
    picos = wea_idx.cummax()

    wea_idx_m = 1 * (ret_m + 1).cumprod()
    picos_m = wea_idx_m.cummax()

    drawdown_default = (wea_idx - picos) / picos
    drawdown_model = (wea_idx_m - picos_m) / picos_m

    return np.round(drawdown_default * 100, 2), np.round(drawdown_model * 100, 2)
