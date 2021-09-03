#%%
import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt
import pandas as pd
from pyswarm import pso
from sklearn import linear_model
import pickle
period='300d'
Period_data=299
interval='1d'
data = yf.download('ONGC.BO', period=period, interval=interval)
ongc = data[:]
data_oil = yf.download('OIL.BO', period=period, interval=interval)
oil = data_oil[:]
data_hoec = yf.download('HINDOILEXP.BO', period=period, interval=interval)
hoec = data_hoec[:]
data_vedl = yf.download('VEDL.BO', period=period, interval=interval)
vedl= data_vedl[:]
data_petronet = yf.download('PETRONET.BO', period=period, interval=interval)
petronet = data_petronet[:]
x_oil = np.array(oil[['Close']])
y_ongc= np.array(ongc[['Close']])
x_hoec = np.array(hoec[['Close']])
x_vedl = np.array(vedl[['Close']])
x_petronet = np.array(petronet[['Close']])
x=np.zeros((Period_data,4))
x[:,0] = oil['Close']
x[:,1] = hoec['Close']
x[:,2] = vedl['Close']
x[:,3] = petronet['Close']
#%%
i=-1
while i<ongc['Close'].size :
    i=i+1
    if ongc['Close'].size==i:
        break
    if ongc.index[i] != oil.index[i] :
        ongc=ongc.drop(ongc.index[i])
        i=i-1
#%%

regr = linear_model.LinearRegression()
regr.fit(x,y_ongc)
coint_ongc =  regr.predict(x)
indicator=coint_ongc-y_ongc


plt.plot(np.array(ongc['Close']))
plt.plot(coint_ongc,'r')
plt.show()
plt.plot(indicator)
plt.show()

# %%
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline
from sklearn.linear_model import LinearRegression
degree=3
polyreg=make_pipeline(PolynomialFeatures(degree),LinearRegression())
polyreg.fit(x_oil,y_ongc)
predicted_ongc=polyreg.predict(x_oil)
plt.plot(predicted_ongc-y_ongc)

# %%
long_short_index= np.zeros((len(indicator)))
go_long_short_index= np.zeros((len(indicator)))
long=0
short=0
for i in range (4,len(indicator)):
    if indicator[i-4]>indicator[i]:
        short =0
        long=long+1
        #if long == 10:
        long_short_index[i]= long

    elif indicator[i-4]<indicator[i]:
        long = 0
        short = short -1
        #if short == 10:
        long_short_index[i]= short
for i in range (1,len(indicator)):
    if long_short_index[i-1]>=8 and long_short_index[i]<=0 and indicator[i]>0:
        go_long_short_index[i]=1
    elif long_short_index[i-1]<=-8 and long_short_index[i]>=0 and indicator[i]<0:
        go_long_short_index[i]=-1

go_long_short_index=go_long_short_index*10