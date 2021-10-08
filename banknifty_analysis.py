#%%
import pandas as pd
from ta.utils import dropna
from ta.volatility import BollingerBands
import matplotlib.pyplot as plt
from py5paisa import FivePaisaClient
from py5paisa.strategy import *
from datetime import datetime 
import numpy as np
cred={
    "APP_NAME":"5P59470899",
    "APP_SOURCE":"6176",
    "USER_ID":"1v73mtvQk3L",
    "PASSWORD":"8DASLLALpZH",
    "USER_KEY":"nNaWVqHIXsgi6FEPnjBknpPPjK1LOHQL",
    "ENCRYPTION_KEY":"HSE2AS6SIEH0UgwfpmwiymkdiRId7eZU"
}
Client = FivePaisaClient(email="p.amareswar20@dmsiitd.org", passwd="Amarreddy@123456", dob="19930714", cred=cred)
Client.login()

#Section 1
# Identify the Candle type for each OHLC(Multiple candles are possible for a OHLC). A column os created for all the types of Candle Patterns found.
data=Client.historical_data('N','C',999920005,'1d','2020-09-17','2021-09-17')
data['O_L']=data['Open']-data['Low']
data['C_L']=data['Close']-data['Low']
data['H_C']=data['High']-data['Close']
plt.bar(np.linspace(1,len(data['O_L']),len(data['O_L'])),-data['O_L'])
plt.bar(np.linspace(1,len(data['C_L']),len(data['C_L'])),data['C_L'])
#plt.bar(np.linspace(1,len(data['H_C']),len(data['H_C'])),-data['H_C'])
plt.show()
plt.plot(data['C_L']/data['O_L'])
plt.show()

# %%
