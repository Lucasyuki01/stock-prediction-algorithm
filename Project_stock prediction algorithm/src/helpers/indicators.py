import numpy as np
import pandas as pd
from scipy.stats import entropy as ent


def RSI(base_list, periods=3, ema=True):
    """
    Returns the relative strength index
    """
    try:
        delta = base_list.diff()
    except:
        delta = base_list.diff()

    # Make two series: one for lower closes and one for higher closes
    up = delta.clip(lower=0)
    down = -1 * delta.clip(upper=0)
    # print('tamanho', len(delta), len(base_list))

    if ema == True:
        # Use exponential moving average
        ma_up = up.ewm(com=periods - 1, adjust=True, min_periods=periods).mean()
        ma_down = down.ewm(com=periods - 1, adjust=True, min_periods=periods).mean()
    else:
        # Use simple moving average
        ma_up = up.rolling(window=periods).mean()
        ma_down = down.rolling(window=periods).mean()

    rsi = ma_up / ma_down
    rsi = 100 - (100 / (1 + rsi))
    # print("RSI", len(rsi), len(base_list))
    rsi[:periods] = np.random.normal(rsi[periods:].mean(), 5, periods)

    return rsi


def MA(base_list, periods=5):
    """
    Returns the moving average
    """
    return base_list.rolling(periods).mean()


def EMA(base_list, days):
    """
    Returns exponential moving average
    """
    ema = base_list.ewm(span=days, adjust=False, min_periods=days).mean()

    return ema


def MACD(base_list):
    """
    Returns moving average convergence divergence, signal, crossover
    Ref: https://www.alpharithms.com/calculate-macd-python-272222
    """

    p1 = 12
    p2 = 26
    p3 = 9

    ema_12 = EMA(base_list, p1)  # 20
    ema_26 = EMA(base_list, p2)  # 35

    macd = ema_12 - ema_26
    macd_s = EMA(macd, p3)  # 15
    macd_h = macd - macd_s

    return macd, macd_s, macd_h


def volatility(df, ticker, days):
    """
    Working on...
    Returns the volatilities
    """
    # df[f'VolP_{ticker}'] = df[f"Close_{ticker}"].rolling(days).std()
    # df[str('Vol'+str(days)+'_'+str(ticker))] = df[f"Close_{ticker}"].rolling(days).std()
    df[str("Vol" + str(days) + "_" + str(ticker))] = df[f"Close_{ticker}"].rolling(
        days
    ).std() * np.sqrt(days)

    return df


def extra_vol(df, ticker, days=3):
    """
    Working on...
    Returns the volatilities
    """

    # df[f'EVol_{ticker}'] = 100*(df[f"High_{ticker}"]-df[f"Low_{ticker}"])/df[f"Low_{ticker}"]
    evol = 100 * (df[f"High_{ticker}"] - df[f"Low_{ticker}"]) / df[f"Low_{ticker}"]
    mm = evol.rolling(days).mean()
    gap = evol - mm
    # df[f'GapVol_{ticker}'] = df[f'EVol_{ticker}'] - mm
    # df[f'RollingVol_{ticker}'] = df[f'EVol_{ticker}'].rolling(days).mean() # it was working
    # df[f'VMin_{ticker}'] = 100*(df[f"Open_{ticker}"]/df[f"Low_{ticker}"])-1
    # df[f'VMax_{ticker}'] = 100*(df[f"High_{ticker}"]/df[f"Open_{ticker}"])-1
    # df[f'VM_{ticker}']   = 100*((df[f"High_{ticker}"]/df[f"Low_{ticker}"])-1)

    return evol, gap


def return_volatility(df, ticker, days):
    """
    Working on...
    Returns the volatilities
    """
    df[str("VolRet" + str(days) + "_" + str(ticker))] = (
        df[f"Close_{ticker}"].rolling(days).std()
    )
    # df[str('Vol'+str(days)+'_'+str(ticker))] = df[f"Close_{ticker}"].rolling(days).std()
    # df[str('Vol'+str(days)+'_'+str(ticker))] = df[f"Close_{ticker}"].rolling(days).std()*np.sqrt(days)

    return df


def lag_n(df, ticker, days):
    """
    R
    """
    names = []
    aux = 100 * (df[f"Close_{ticker}"].pct_change())
    j = 1

    for i in range(days):
        names.append("lag_" + str(i + 1))
        df[names[i]] = aux

    for i in range(1, days):
        aux = df[names[0]][j:]
        # df[names[i]][j+1:] = aux[:len(aux)-j]
        df[names[i]][j + j :] = aux[: len(aux) - j]
        j += 1

    return df[j:]


def lag_any(df, ticker, column, days):
    """
    R
    """
    names = []
    col = column
    try:
        aux = df[col + "_" + ticker]
    except:
        aux = df[col]

    j = 1

    for i in range(days):
        names.append("lag_" + col + "_" + str(i + 1))
        df[names[i]] = aux

    for i in range(1, days):
        aux = df[names[0]][j:]
        df[names[i]][j + j :] = aux[: len(aux) - j]
        j += 1

    return df[j:]


def log_any(df, ticker, column):
    """
    Applies log
    """

    cte = 1e-7
    col = column

    name = "log_" + col + "_" + ticker

    try:
        df[name] = np.log(df[col + "_" + ticker] + cte)
    except:
        df[name] = np.log(df[col] + cte)  # for plain indicators

    return df


def bollinger_bands(df, ticker):
    """ "
    A
    """

    a = df[f"Close_{ticker}"].rolling(20).mean()
    a[:20] = a[20]

    b = df[f"Close_{ticker}"].rolling(20).std()
    b[:20] = b[20]

    df[f"BB_center_{ticker}"] = a
    df[f"BB_upper_{ticker}"] = a + 2 * b
    df[f"BB_lower_{ticker}"] = a - 2 * b

    return df


def vwap(df, ticker, days):
    """ "
    Volume Weighted Average Price
    Aqui vamos avaliar como o preço e o volume se relacionam e comportam ao longo do tempo
    """

    volume_price = df[f"Close_{ticker}"] * df[f"Volume_{ticker}"]
    vp = volume_price.rolling(days).sum()
    vp[:days] = vp[days]
    volume = df[f"Volume_{ticker}"].rolling(days).sum()
    volume[:days] = volume[days]

    volume_price = vp / volume

    return volume_price


def entropy_orig(df, ticker, col="Close", days=5):
    """
    Entropy-based features
    working on...
    """

    # df[f'Ent_{ticker}'] = np.empty(len(df))
    name = str("Ent_" + str(col) + str(days) + "_" + str(ticker))

    df[name] = np.empty(len(df))

    cte = int(len(df) - days)

    for i in range(cte):
        try:
            df[name][i : i + days] = ent(df[col + "_" + ticker][i : i + days])
        except:
            df[name][i : i + days] = ent(df[col][i : i + days])
        # df[f'Ent_{ticker}'][i:i+days] = ent(df['Close_'+ticker][i:i+days])
        # df[f'Ent_{ticker}'][i] = ent(df['Close_'+ticker][i-days:i])
    # print("The number of i", i, len(df))
    try:
        # df[name][i:] = ent(df[col+'_'+ticker][i:])
        df[name][i + days :] = ent(df[col + "_" + ticker][i:])
    except:
        df[name][i + days :] = ent(df[col][i:])

    return df


def entropy(df, ticker, column="Close", days=5):
    """
    Entropy-based features
    working on...
    """

    col = column

    name = str("Ent_" + str(col) + str(days) + "_" + str(ticker))
    # print("Entro", name)

    df[name] = np.empty(len(df))

    cte = int(len(df))

    for i in range(days, cte):
        try:
            df[name][i - 1] = ent(df[col + "_" + ticker][i - days : i])
        except:
            df[name][i - 1] = ent(df[col][i - days : i])

    try:
        df[name][i:] = ent(df[col + "_" + ticker][i - days + 1 : i + 1])
    except:
        df[name][i:] = ent(df[col][i - days + 1 : i + 1])

    return df


def MACD_mod(base_list, p1=20, p2=35, p3=15):
    """
    Returns moving average convergence divergence, signal, crossover
    Ref: https://www.alpharithms.com/calculate-macd-python-272222
    """

    # p1 = 12
    # p2 = 26
    # p3 = 9

    ema_12 = EMA(base_list, p1)  # 20
    ema_26 = EMA(base_list, p2)  # 35

    macd = ema_12 - ema_26
    macd_s = EMA(macd, p3)  # 15
    macd_h = macd - macd_s

    return macd, macd_s, macd_h


def detrend(base_list, periods=34):
    """
    Return the de-trend series
    """

    return base_list - base_list.rolling(periods).mean()


def Bin_RSI(base_list, periods=3, ema=True, high=70, low=30):
    """
    Binary threshold for RSI indicator
    """

    rsi = RSI(base_list, periods, ema)

    rsi_high = np.zeros(len(base_list))
    rsi_high[rsi > high] = 1

    rsi_low = np.zeros(len(base_list))
    rsi_low[rsi < low] = 1

    return rsi_high, rsi_low


def CCI(base_df, name, periods=20):
    """
    Return the CCI Index
    """

    tipical_price = (
        base_df["Close_" + name] + base_df["High_" + name] + base_df["Low_" + name]
    ) / 3
    tipical_price = tipical_price.rolling(periods).sum()

    ma = MA(tipical_price, periods)
    mdev = MA((tipical_price - ma).abs(), periods)

    cci = (tipical_price - ma) / (0.015 * mdev)

    return cci


def SOSC(base_df, name, days=14):
    """
    Returns the stochastic oscilator
    """
    low = base_df["Low_" + name].rolling(days).min()
    high = base_df["High_" + name].rolling(days).max()
    cprice = base_df["Close_" + name]  # .rolling(days)

    sosc = 100 * ((cprice - low) / (high - low))

    return sosc


def Bin_SOSC(base_df, name, high=70, low=30, days=14):
    """
    Returns the stochastic oscilator
    """

    sosc = SOSC(base_df, name, days)

    high_sosc = np.zeros(len(sosc))
    high_sosc[sosc > high] = 1
    low_sosc = np.zeros(len(sosc))
    low_sosc[sosc < low] = 1

    return high_sosc, low_sosc


def zscore(base_list, period=15):

    z = base_list - base_list.rolling(period).mean()
    z = z / base_list.rolling(period).std()

    return z


def RSL(base_list, period=15):

    mm = base_list.rolling(period).mean()
    rsl = (base_list / mm) - 1

    return rsl


def direcao(base_df, name):

    direc = np.zeros(len(base_df))
    direc[base_df["Close_" + name] > base_df["Open_" + name]] = 1

    return direc


def direcao_per(base_df, name, period=5):

    direc = np.zeros(len(base_df))
    direc[base_df["Close_" + name].shift(period) > base_df["Close_" + name]] = 1
    # direc[base_df['Close_'+name]>base_df['Open_'+name]] = 1

    return direc


def velocidade(base_list, days=5):
    """
    velocidade de movimentação dos candles
    """

    v = base_list.pct_change().fillna(0)
    v = ((v - v.shift(days)) / days).fillna(0)

    return v


def aceleracao(base_list, days=5):
    """
    aceleração de movimentação dos candles
    """

    v = velocidade(base_list, days)
    a = ((v - v.shift(days)) / days).fillna(0)

    return a


def massa(base_list, days=5):
    """
    massa de movimentação dos candles
    """

    m = base_list.pct_change().fillna(0)
    m = m.rolling(days).sum().fillna(0)

    return m


def forca(base_list, days=5):
    """
    força resultante da movimentação dos candles
    """

    m = massa(base_list, days)
    a = aceleracao(base_list, days)

    f = m * a

    return f


def energia_cinetica(base_list, days=5):
    """
    energia cinética da movimentação dos candles
    """

    v = velocidade(base_list, days)
    e = 0.5 * massa(base_list, days) * v * v

    return e


def trabalho(base_list, days=5):
    """
    trabalho da movimentação dos candles
    """

    ret = base_list.pct_change().fillna(0)
    cat_op = ret.rolling(days).sum() - ret.rolling(1).sum()
    cat_ad = days
    cat = cat_op / cat_ad
    w = forca(base_list, days) * np.cos(np.arctan(cat))

    return w


def e_potencial(base_list, days=5):
    """
    energia potencial da movimentação dos candles
    """

    ret = base_list.pct_change().fillna(0)
    cat_op = ret.rolling(days).sum() - ret.rolling(1).sum()
    m = massa(base_list, days)

    ep = cat_op * m

    return ep


def torque(base_list, days=5):
    """
    torque da movimentação dos candles
    """

    f = forca(base_list, days)
    ret = base_list.pct_change().fillna(0)
    cat_op = ret.rolling(days).sum() - ret.rolling(1).sum()
    cat_ad = days
    cat = cat_op / cat_ad

    t = f * np.sin(np.arctan(cat))

    return t


def momento(base_list, days=5):
    """
    momento da movimentação dos candles
    """

    m = massa(base_list, days)
    v = velocidade(base_list, days)

    return m * v


def relative_gap(df, name, perc=0.1):
    """
    relative binary gap for candles
    """

    candle_body = np.array(df["Close_" + name] - df["Open_" + name])

    upper = np.array(df["High_" + name] - df["Close_" + name])
    lower = np.array(df["Low_" + name] - df["Close_" + name])

    upper[upper > candle_body] = 1
    upper[upper < candle_body] = 0

    lower[lower > candle_body] = 1
    lower[lower < candle_body] = 0

    return upper, lower


def quart_var(base_list, qtd=5):
    """
    Quartile any variable in 'qtd' intervals
    """

    qq = pd.qcut(base_list, qtd, labels=False)

    return qq


def inclinacao(base_list, period=5):
    """
    Inclinação da curva passada em base_list
    """

    cat_op = base_list.rolling(period).sum() - base_list.rolling(1).sum()
    cat = (cat_op / period).fillna(0)

    theta = np.arctan(cat)

    return theta


def inclinacao_2(base_list, period=5):
    """
    Inclinação da curva passada em base_list
    """

    cat_op = base_list.rolling(period).cumsum() - base_list.rolling(1).cumsum()
    cat = (cat_op / period).fillna(0)

    theta = np.arctan(cat)

    return theta


def fourier(base_list):
    """ "
    Real component of DFT
    """

    fft = base_list
    fft[~np.isnan(fft)] = np.abs(np.fft.fftn(base_list[~np.isnan(base_list)]))

    return fft


def distance(base_list):
    """
    Apply the pairwise euclidean distance over all features.
    """
    from sklearn.metrics.pairwise import euclidean_distances

    aux = np.zeros(len(base_list))
    d = base_list.shift(1).fillna(0)

    for i in range(len(aux)):
        if not base_list.iloc[i].isnull().values.any():
            aux[i] = euclidean_distances(
                np.array(base_list.iloc[i]).reshape(1, -1),
                np.array(d.iloc[i]).reshape(1, -1),
            )

    return aux


def skewness(base_list, periods=10):
    """
    Apply the skewness over all features.
    """

    sk = base_list.rolling(periods).skew()

    return sk


def kurtosis(base_list, periods=10):
    """
    Apply the kurtosis over all features.
    """

    kurt = base_list.rolling(periods).kurt()  # .fillna(0)

    return kurt


def percent_variation(base_list, periods=1):
    """
    Apply the percentual return.
    """

    return base_list.diff(periods).fillna(0)  # .pct_change(periods).fillna(0)*100


def rolling_beta(base_list, periods=5, lower=-0.25, upper=0.25):

    betas = np.zeros(len(base_list))

    for i in range(periods, len(base_list)):
        cov = (periods) * (
            base_list[i - periods : i] - base_list[i - periods : i].mean()
        )
        var = (base_list[i - periods : i] - base_list[i - periods : i].mean()) ** 2

        # Computando beta
        beta = cov.sum() / var.sum()
        betas[i] = beta
    betas[betas > upper] = 1
    betas[betas < lower] = -1
    return betas


def ind_predictor(base_list, periods=5):

    preds = np.zeros(len(base_list))

    for i in range(periods, len(base_list)):
        cov = (base_list[i - periods : i] - base_list[i - periods : i].mean()) * (
            base_list[i - periods : i].shift(1)
            - base_list[i - periods : i].shift(1).mean()
        )
        var = (base_list[i - periods : i] - base_list[i - periods : i].mean()) ** 2

        # Computando beta  e alpha
        beta = cov.sum() / var.sum()
        alpha = base_list[i - periods : i].shift(1).mean() - (
            beta * base_list[i - periods : i].mean()
        )
        preds[i] = alpha + beta * base_list[i]

    return preds


def structural_entropy(df_logret, sequence_length, t):
    # needs reimplementation...
    from scipy.sparse.csgraph import connected_components

    def get_timespan(df, start, end):
        return df.iloc[:, start:end].T

    def corr_matrix(df, start, end):
        seq = get_timespan(df, start, end)
        corr_seq = seq.corr().values
        return corr_seq

    structural_entropy = {"timestamp": [], "structural_entropy": []}

    for d in range(sequence_length, df_logret.shape[1]):

        _corr = corr_matrix(df_logret, d - sequence_length, d)

        _corr = (np.abs(_corr) > t).astype(int)
        _, _labels = connected_components(_corr)

        _, _count = np.unique(_labels, return_counts=True)
        _countnorm = _count / _count.sum()
        _entropy = -(_countnorm * np.log2(_countnorm)).sum()

        structural_entropy["timestamp"].append(df_logret.columns[d])
        structural_entropy["structural_entropy"].append(_entropy)

    structural_entropy = pd.Series(
        structural_entropy["structural_entropy"], index=structural_entropy["timestamp"]
    )

    return structural_entropy
