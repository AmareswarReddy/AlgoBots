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


#%%
def avg_V(data,a):
    data['avg_V'] = 0
    vol = data['Volume'].copy()
    avg_Volume = data['avg_V'].copy()
    avg_Volume.iloc[a-1] = vol.iloc[0:a].sum()/a
    for i in range(a,avg_Volume.size):
        avg_Volume.iloc[i]=(vol.iloc[i]-avg_Volume.iloc[i-1])*(2/(a+1))+avg_Volume.iloc[i-1]
    del data['avg_V']
    return avg_Volume         
#%%
df['avg_Vol']=avg_V(df,14)
#%%
def is_doji(df,i):
    a=abs(df.iloc[i]['Open']-df.iloc[i]['Close'])
    b=df.iloc[i]['Close']-df.iloc[i]['Low']
    c=df.iloc[i]['Volume']/df.iloc[i]['avg_Vol']
    rsi=df.iloc[i]['MFI']
    if a/b <0.5 and c>2:
        return 'yes'

# %%
entries=[]
control=0
for i in range(20,len(df['Open'])):
    if is_doji(df,i)=='yes' and control==0:
        entry=df.iloc[i]['Close']
        control=1
        print(i)
        entries=entries+[i]
    if control==1 and df.iloc[i]['RSI']>80:
        exit=df.iloc[i]['Close']
        print(i)
        control=0
x=np.zeros(len(df['Open']))
for i in entries:
    x[i]=1000
plt.plot(np.linspace(1,len(x),len(x)),np.array(df['Close']))
plt.scatter(np.linspace(1,len(x),len(x)),x)
plt.show()

# %%
