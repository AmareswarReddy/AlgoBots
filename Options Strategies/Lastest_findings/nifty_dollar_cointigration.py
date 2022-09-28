#if running on google colab
!pip install yfinance
#%%
import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt
import pandas as pd
from sklearn import linear_model
period='1500d'
interval='1d'
data = yf.download('^NSEI', period=period, interval=interval)
nifty = data[:]
data_dollar = yf.download('INR=X', period=period, interval=interval)
dollar = data_dollar[:]


sp=np.array(nifty.index)
sc=np.array(dollar.index)
k=np.intersect1d(np.array(sp),np.array(sc))
w=[]
for strike in sp:
    if strike in k:
        w=w+[True]
    else:
        w=w+[False]
v=[]
for strike in sc:
    if strike in k:
        v=v+[True]
    else:
        v=v+[False]
nifty=nifty[w].copy()
dollar=dollar[v].copy()
x=np.zeros((len(dollar),1))
x[:,0] = dollar['Close']
y_nifty= np.array(nifty[['Close']])
regr = linear_model.LinearRegression()
regr.fit(x,y_nifty)
coint_nifty =  regr.predict(x)
indicator=coint_nifty-y_nifty


plt.plot(np.array(nifty['Close']))
plt.plot(coint_nifty,'r')
plt.show()
plt.plot(indicator)
plt.show()

# %%
