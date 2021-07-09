import numpy as np
from statsmodels.tsa.stattools import pacf, acf
from pmdarima.arima.utils import ndiffs
from statsmodels.tsa.arima_model import ARIMA


def get_parameter(df):
    # find order of differencing
    d = ndiffs(df, test='adf')

    # differencing
    differenced = df
    for i in range(d):
        differenced = differenced.diff()
    differenced = differenced.dropna()

    # AR term
    coef = pacf(differenced)
    level = np.exp(2 * 1.96 / np.sqrt(len(differenced) - 3) - 1) / np.exp(2 * 1.96 / np.sqrt(len(differenced) - 3) + 1)

    a = coef > level
    p = len(np.split(a, np.where(a != 1)[0])[0]) - 1

    # MA term
    coef = acf(differenced)

    a = coef > level
    q = len(np.split(a, np.where(a != 1)[0])[0]) - 1
    return p, d, q

def get_ARIMA(df):
    ParamDict = {}
    for i in df.columns:
        ParamDict[i] = get_parameter(df[i])

    filtered_dict = {key: value for key, value in ParamDict.items() if (value[0] > 0) & (value[2] > 0)}
    models_dict = {}

    for key in filtered_dict.keys():
        order = filtered_dict[key]
        model = ARIMA(df[key], order=(order[0], order[1], 1))  # only use 1 ma term
        try:
            model_fit = model.fit(disp=0)
            print("%s has been fitted" % key)
            models_dict[key] = model_fit
        except:
            print("%s cannot be done" % key)

    return models_dict