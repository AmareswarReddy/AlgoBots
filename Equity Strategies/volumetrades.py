#%%
from indicators import indicators as ind
import pandas as pd
from ta.utils import dropna
from ta.volatility import BollingerBands
import matplotlib.pyplot as plt
from py5paisa import FivePaisaClient
from py5paisa.strategy import *
from datetime import datetime 
import numpy as np
from pyswarm import pso
script=pd.read_csv('scripmaster-csv-format.csv')
scrip_codes = script[(script['Exch']=='N') & (script['ExchType']=='C') & (script['Series']=='EQ')]
#%%
scripcode_to_Symbol = {}
for index, row in scrip_codes.iterrows():
    scripcode_to_Symbol[row['Scripcode']] = row['Name']
    #Get only NIFTY200  stocks
nifty200 = pd.read_csv("ind_nifty200list (2).csv")
top200 = scrip_codes[scrip_codes['Name'].isin(nifty200['Symbol'])]
#%%
cred={
    "APP_NAME":"5P56936208",
    "APP_SOURCE":"2179",
    "USER_ID":"w6MJ1dw5Yd0",
    "PASSWORD":"V7JkGTUudjt",
    "USER_KEY":"8Q4SSCEo0bOgroVMFcNB0nTTB6CGPQuE",
    "ENCRYPTION_KEY":"HEgo6erh7qmqnDjRXIbaRTSNyfI6eofO"
    }
Client = FivePaisaClient(email='vinaykumar7295@gmail.com', passwd='godofwarvinay1@A',dob='19700701', cred=cred)
Client.login()
#%%
scripcode=1333
#Section 1
# Identify the Candle type for each OHLC(Multiple candles are possible for a OHLC). A column os created for all the types of Candle Patterns found.
data=Client.historical_data('N','C',scripcode,'1d','2018-06-01','2021-11-19')
df=ind(data)
def MFI(data):
    data['MFI'] = 0
    data['aa']=0
    close = data['Close'].copy()  # only volume now
    mfi = data['MFI'].copy()
    aa = data['aa'].copy()
    aa.iloc[1:]=close.iloc[:-1]
    bb=(close-aa)
    bb.iloc[0]=0 
    bb=data['Volume'] #bb in the place of 1 for volume*
    i=15
    first_14= bb.iloc[i-14:i]
    U = first_14.loc[first_14>0].sum()
    U_count = len(first_14.loc[first_14>0])
    L = first_14.loc[first_14<0].sum()
    L_count = len(first_14.loc[first_14<0])
    U_average = U/U_count
    L_average = -L/L_count
    k = (U_average)/(L_average)
    mfi.iloc[i] = 100-(100/(1+k))
    for i in range(16,close.size):
        last= bb.iloc[i]
        U_new = last*(last>0)
        L_new = last*(last<0)
        U_average = (U_average*13+U_new)/14
        L_average = (L_average*13-L_new)/14
        k = (U_average)/(L_average)
        mfi.iloc[i] = 100-(100/(1+k))
    del data['aa']
    return mfi


# %%
