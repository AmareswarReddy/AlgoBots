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
    "APP_NAME":"5P55115625",
    "APP_SOURCE":'8899',
    "USER_ID":"qZS8Qd5THYc",
    "PASSWORD":"O4X41D47h1g",
    "USER_KEY":"BDYHVFfDodmHw3RXeWzuc2acdOwczZ64",
    "ENCRYPTION_KEY":"jhxJH0k6BIUL6VnXYPIAcqTZLqYWhkLc"
    }
strategy=strategies(user="vinathi.bujji@gmail.com", passw="alliswell1@A", dob="19940830",cred=cred)
Client=FivePaisaClient(email='vinathi.bujji@gmail.com', passwd='alliswell1@A', dob='19940830',cred=cred)
Client.login()
#%%
scripcode=1333
#Section 1
# Identify the Candle type for each OHLC(Multiple candles are possible for a OHLC). A column os created for all the types of Candle Patterns found.
data=Client.historical_data('N','C',scripcode,'1d','2018-06-01','2022-04-09')
df=ind(data)


# %%
for i in range(0,len(df['Open'])):
    
