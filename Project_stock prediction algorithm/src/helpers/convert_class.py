import numpy as np


def convert_to_natural(label, binary=False):
    """
    Convert to natural classes (2,1,0)  => 2=Sell, 1=buy, 0=safe
    For training Pytorch-based models
    """
    nlb = np.zeros((len(label)))

    for i in range(len(label)):
        if label[i] == -1:
            nlb[i] = 2
        if label[i] == 1:
            nlb[i] = 1
        if label[i] == 0:
            nlb[i] = 0

    if binary:
        nlb = nlb - 1

    return nlb


def natural_to_original(label, binary=False):
    """
    Convert to original classes (-1,0,1) => -1=sell, 1=buy, 0=safe
    For training Pytorch-based models
    """

    nlb = np.zeros((len(label)))

    if binary:
        label = label + 1

    for i in range(len(label)):
        if label[i] == 2:
            nlb[i] = -1
        if label[i] == 1:
            nlb[i] = 1
        if label[i] == 0:
            nlb[i] = 0

    return nlb


def convert_to_string(label):
    """
    Convert to string classes (-1,0,1) => -1=sell, 1=buy, 0=safe
    """
    nlb = []

    # print("Labels: ", np.unique(label))
    for i in range(len(label)):
        if label[i] == 2 or label[i] == -1:
            nlb.append("sell")
        if label[i] == 1:
            nlb.append("buy")
        if label[i] == 0:
            nlb.append("safe")

    return nlb


def convert_to_high_low(series):
    y = []
    for i in range(
        len(series) - 1
    ):  # len(ytest) prevent to captur the prediction for last day + 1
        if series[i + 1] > series[i]:
            y.append(1)
        else:
            y.append(0)
    return y
