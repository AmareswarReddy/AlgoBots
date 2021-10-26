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
cred={
    "APP_NAME":"5P56936208",
    "APP_SOURCE":"2179",
    "USER_ID":"w6MJ1dw5Yd0",
    "PASSWORD":"V7JkGTUudjt",
    "USER_KEY":"8Q4SSCEo0bOgroVMFcNB0nTTB6CGPQuE",
    "ENCRYPTION_KEY":"zeoxSiZ1pbQsOJ2vaMlOllCeJwNzRQeFlcjc0WGYyl5nLzoCRtWZI5Z2xwChp6Ip"
    }
Client = FivePaisaClient(email='vinaykumar7295@gmail.com', passwd='godofwarvinay1@A',dob='19700701', cred=cred)
Client.login()
#%%
scripcode=999920000
#Section 1
# Identify the Candle type for each OHLC(Multiple candles are possible for a OHLC). A column os created for all the types of Candle Patterns found.
data=Client.historical_data('N','C',scripcode,'1d','2015-01-01','2021-09-10')
df=ind(data)

profit=0
a=0
j=0
entry_rsi=35
exit_rsi=40
max_days_in_trade=10
for i in range(201,len(df['RSI'])):
    if df['RSI'][i]<entry_rsi and df['EMA200'][i]<data['Close'][i] and a==0:
        print('entry point is : ',df['Close'][i])
        start=df['Close'][i]
        a=1
        rsi_var=0
        exit_status=0
        temp=df['Close'][i]
        j=i
    if a==1 and df['RSI'][i]>exit_rsi and (i-j)<max_days_in_trade and exit_status==0:
        print('exit point is : ',df['Open'][i+1])
        print('days in the trade :',i+1-j)
        print('')
        a=0
        profit=profit+df['Open'][i+1]-temp
    elif a==1 and start-df['Close'][i]>df['Close'][i]*0.01 and (i-j)<max_days_in_trade and rsi_var==0:
        print('exit point is : ',df['Close'][i])
        print('days in the trade :',i+1-j)
        print(df.index[i])
        print('')
        profit=profit+df['Close'][i]-temp
        rsi_var=1
        exit_status=1
    if a==1 and (i-j)>=max_days_in_trade and rsi_var==0:
        print('exit point is : ',df['Close'][i])
        print('days in the trade :',i+1-j)
        print(df.index[i])
        print('')
        profit=profit+df['Close'][i]-temp
        rsi_var=1
    if df['RSI'][i]>exit_rsi:
        a=0
print('profit: ',profit)
# %%
