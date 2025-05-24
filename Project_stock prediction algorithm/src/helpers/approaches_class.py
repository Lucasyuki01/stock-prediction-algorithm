import numpy as np


def sigmoid(x):
    return 1.0 / (1.0 + np.exp(-x))


def hard_classification(base_list, days_window=3):
    """
    Returns a pd.Series with the classified dataframe (-1=sale, 1=buy)
    """
    days = days_window

    aux = np.ones(len(base_list))

    for i in range(len(base_list) - days):
        if base_list[i + days] > base_list[i]:
            aux[i] = 1
        else:
            if base_list[i + days] < base_list[i]:
                aux[i] = -1

    print("Classified-hardly")

    return aux

def smooth_classification(base_list, days=5, perc=0.01):
    """
    Returns a pd.Series with the classified dataframe (-1=sale, 1=buy, 0=safe)
    """

    aux = np.zeros(len(base_list))

    for i in range(len(base_list) - days):

        if base_list[i + days] > base_list[i] + base_list[i] * perc:
            aux[i] = 1
        elif base_list[i + days] < base_list[i] - base_list[i] * perc:
            aux[i] = -1
        else:
            aux[i] = 0

    print(f"Classified-smooth {len(base_list)} -> {len(aux)}")

    return aux
