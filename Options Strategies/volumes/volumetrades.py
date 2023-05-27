#%%
from indicators import indicators as ind
import pandas as pd
#from ta.utils import dropna
#from ta.volatility import BollingerBands
import matplotlib.pyplot as plt
from py5paisa import FivePaisaClient
from py5paisa.strategy import *
from datetime import datetime 
import numpy as np
from pyswarm import pso
script=pd.read_csv('scripmaster-csv-format.csv')
scrip_codes = script[(script['Exch']=='N') & (script['ExchType']=='C') & (script['Series']=='EQ')]

scripcode_to_Symbol = {}
for index, row in scrip_codes.iterrows():
    scripcode_to_Symbol[row['Scripcode']] = row['Name']
    
#Get only NIFTY200  stocks
nifty200 = pd.read_csv("ind_nifty200list (2).csv")
top200 = scrip_codes[scrip_codes['Name'].isin(nifty200['Symbol'])]

cred={
    "APP_NAME":"5P55115625",
    "APP_SOURCE":'8899',
    "USER_ID":"qZS8Qd5THYc",
    "PASSWORD":"O4X41D47h1g",
    "USER_KEY":"BDYHVFfDodmHw3RXeWzuc2acdOwczZ64",
    "ENCRYPTION_KEY":"jhxJH0k6BIUL6VnXYPIAcqTZLqYWhkLc"
    }
strategy=strategies(user="vinathi.bujji@gmail.com", passw="kittu1@A", dob="19940830",cred=cred)
Client=FivePaisaClient(email='vinathi.bujji@gmail.com', passwd='kittu1@A', dob='19940830',cred=cred)
Client.login()
def avg_V(data,a):
    data['avg_V'] = 0
    vol = data['Volume'].copy()
    avg_Volume = data['avg_V'].copy()
    avg_Volume.iloc[a-1] = vol.iloc[0:a].sum()/a
    for i in range(a,avg_Volume.size):
        avg_Volume.iloc[i]=(vol.iloc[i]-avg_Volume.iloc[i-1])*(2/(a+1))+avg_Volume.iloc[i-1]
    del data['avg_V']
    return avg_Volume        


def is_doji(df,i):
    spread=abs(df.iloc[i]['Open']-df.iloc[i]['Close'])
    lower_wick=df.iloc[i]['Close']-df.iloc[i]['Low']
    volume_ratio=df.iloc[i]['Volume']/df.iloc[i]['avg_Vol']
    mfi=df.iloc[i]['MFI']
    rsi=df.iloc[i]['RSI']
    if spread/lower_wick <0.3 and volume_ratio>1.75:
        return 'yes' 
#%%
for i in range(0,len(top200['Scripcode'])-197):
    scripcode=445
    #Section 1
    # Identify the Candle type for each OHLC(Multiple candles are possible for a OHLC). A column os created for all the types of Candle Patterns found.
    data=Client.historical_data('N','C',scripcode,'1d','2020-01-01','2022-04-19')
    df=ind(data)
    df['avg_Vol']=avg_V(df,14)
    entries=[]
    control=0
    for i in range(20,len(df['Open'])):
        if is_doji(df,i)=='yes' and control==0:
            entry=df.iloc[i]['Close']
            #control=1
            print(df['Datetime'].iloc[i][:10])
            entries=entries+[i]
    """
        if control==1 and df.iloc[i]['RSI']>80:
            exit=df.iloc[i]['Close']
            print(i)
            control=0
    """
    x=np.zeros(len(df['Open']))
    for i in entries:
        x[i]=df['Close'].iloc[0]
    plt.plot(np.linspace(1,len(x),len(x)),np.array(df['Close']))
    plt.scatter(np.linspace(1,len(x),len(x)),x)
    plt.show()
    print()

# %%
def ticker_to_scripcode(ticker):
    return int(scrip_codes[scrip_codes.Name==ticker]['Scripcode'])


# %%
def lows(df,window):
    lows_=np.array(df['Low'])
    avg_lows= np.zeros(len(lows_))
    avg_lows[:window]=lows_[:window]
    for i in range(window,len(lows_)):
        avg_lows[i]=(np.sum(lows_[i-window:i])/window)*(7/10)+(3/10)*lows_[i]
    local_minima=[]
    for j in range(1,len(avg_lows)-1):
        if avg_lows[j-1]>avg_lows[j] and avg_lows[j]<avg_lows[j+1]:
            local_minima=local_minima+[j]
    k=lows_[local_minima]
    return k,local_minima

def highs(df,window):
    highs_=np.array(df['High'])
    avg_highs= np.zeros(len(highs_))
    avg_highs[:window]=highs_[:window]
    for i in range(window,len(highs_)):
        avg_highs[i]=(np.sum(highs_[i-window:i])/window)*(7/10)+(3/10)*highs_[i]
    local_maxima=[]
    for j in range(1,len(avg_highs)-1):
        if avg_highs[j-1]<avg_highs[j] and avg_highs[j]>avg_highs[j+1]:
            local_maxima=local_maxima+[j]
    k=highs_[local_maxima]
    return k,local_maxima

# %%
low_values, indices=lows(df,100)
high_values, indices2=highs(df,100) 
all_highs=np.array(df['High'])
all_lows=np.array(df['Low'])
removal_list=[]
for i in indices:
    kk=min(abs(np.array(indices2)-i))
    if ((all_highs[kk]-all_lows[i])/all_highs[kk])*100<0.01:
        removal_list=removal_list+[i]

for i in removal_list:
    indices.remove(i)
x=np.zeros(len(df['Close']))
x[indices]=low_values
#%%
plt.plot(np.linspace(1,len(x),len(x)),np.array(df['Low']))
plt.scatter(np.linspace(1,len(x),len(x)),x)
plt.show()
# %%




#chatgpt
import numpy as np
import talib

length = 130
coef = 0.2
vcoef = 2.5
signalLength = 5
smoothVFI = False

def ma(x, y):
    return talib.SMA(x, y) if smoothVFI else x

typical = (high + low + close) / 3
inter = np.log(typical) - np.log(typical.shift(1))
vinter = np.std(inter, 30)
cutoff = coef * vinter * close
vave = talib.SMA(volume, length).shift(1)
vmax = vave * vcoef
vc = np.where(volume < vmax, volume, vmax)
mf = typical - typical.shift(1)
vcp = np.where(mf > cutoff, vc, np.where(mf < -cutoff, -vc, 0))

vfi = ma(talib.SUM(vcp, length) / vave, 3)
vfima = talib.EMA(vfi, signalLength)
d = vfi - vfima

plt.plot(np.zeros_like(close), color='gray', linestyle='--')
showHisto = False
if showHisto:
    plt.plot(d, color='gray', linewidth=3, alpha=0.5)
plt.plot(vfima, color='orange', label='EMA of VFI')
plt.plot(vfi, color='green', linewidth=2, label='VFI')
plt.legend()
plt.show()

# %%
