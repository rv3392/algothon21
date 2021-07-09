#!/usr/bin/env python
# coding: utf-8

# In[1]:


import sys
sys.path.insert(1,'../src')

import numpy as np, pandas as pd
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.tsa.stattools import pacf, acf
import matplotlib.pyplot as plt
import warnings
from pmdarima.arima.utils import ndiffs
from statsmodels.tsa.arima_model import ARIMA

plt.rcParams.update({'figure.figsize':(16, 8), 'figure.dpi':300})
warnings.filterwarnings("ignore")


# In[2]:


df = pd.read_csv("data/prices250.csv")
ParamDict = {}


# In[3]:


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


# In[4]:


for i in df.columns:
    ParamDict[i] = get_parameter(df[i])


# In[5]:


filtered_dict = {key:value for key, value in ParamDict.items() if (value[0] > 0) & (value[2] > 0)}
model_dict = {}


# In[6]:


filtered_dict


# In[7]:


for key in filtered_dict.keys():
    order = filtered_dict[key]
    model = ARIMA(df[key], order=(order[0], order[1], 1)) # only use 1 ma term
    try:
        model_fit = model.fit(disp=0)
        print("%s has been fitted" % key)
        model_dict[key] = model_fit
    except:
        print("%s cannot be done" % key)


# In[24]:


key = '99'
order = filtered_dict[key]
model = ARIMA(df[key][:230], order=(order[0], order[1], 1))
model_fit = model.fit(disp=0)
print(model_fit.summary())
model_fit.plot_predict(dynamic=False)


# In[25]:


fc, se, conf = model_fit.forecast(20, alpha=0.05)  # 95% conf
plt.plot(range(230, 250), fc, label='forecast')
plt.plot(df[key])
plt.title('Forecast vs Actuals')
plt.legend(loc='upper left', fontsize=8)
plt.show()


# In[ ]:




