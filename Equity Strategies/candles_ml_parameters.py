"""
url = 'https://anaconda.org/conda-forge/libta-lib/0.4.0/download/linux-64/libta-lib-0.4.0-h516909a_0.tar.bz2'
!curl -L $url | tar xj -C /usr/lib/x86_64-linux-gnu/ lib --strip-components=1
url = 'https://anaconda.org/conda-forge/ta-lib/0.4.19/download/linux-64/ta-lib-0.4.19-py37ha21ca33_2.tar.bz2'
!curl -L $url | tar xj -C /usr/local/lib/python3.7/dist-packages/ lib/python3.7/site-packages/talib --strip-components=3
!pip install py5paisa
!pip install ta
!pip install cred
!pip install pyswarm
!pip install pyswarms

import talib
"""
#%%
from indicators import indicators as ind
import pandas as pd
from ta.utils import dropna
from ta.volatility import BollingerBands
import matplotlib.pyplot as plt
import talib
from py5paisa import FivePaisaClient
from py5paisa.strategy import *
from datetime import datetime 
import numpy as np
from pyswarm import pso
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
scripcode=999920005
#Section 1
# Identify the Candle type for each OHLC(Multiple candles are possible for a OHLC). A column os created for all the types of Candle Patterns found.
data=Client.historical_data('N','C',scripcode,'15m','2021-04-17','2021-09-10')
candle_names = talib.get_function_groups()['Pattern Recognition']

for candle in candle_names:
        # below is same as;
        # df["CDL3LINESTRIKE"] = talib.CDL3LINESTRIKE(op, hi, lo, cl)
        data.loc[:,candle] = getattr(talib, candle)(data.loc[:,'Open'], data.loc[:,'High'], data.loc[:,'Low'], data.loc[:,'Close'])
data.to_excel("temp.xlsx")


# Section 2
# Raking the candles, and creating a column with the high ranked candle
candle_rankings = {
        "CDL3LINESTRIKE_Bull": 1,
        "CDL3LINESTRIKE_Bear": 2,
        "CDL3BLACKCROWS_Bull": 3,
        "CDL3BLACKCROWS_Bear": 3,
        "CDLEVENINGSTAR_Bull": 4,
        "CDLEVENINGSTAR_Bear": 4,
        "CDLTASUKIGAP_Bull": 5,
        "CDLTASUKIGAP_Bear": 5,
        "CDLINVERTEDHAMMER_Bull": 6,
        "CDLINVERTEDHAMMER_Bear": 6,
        "CDLMATCHINGLOW_Bull": 7,
        "CDLMATCHINGLOW_Bear": 7,
        "CDLABANDONEDBABY_Bull": 8,
        "CDLABANDONEDBABY_Bear": 8,
        "CDLBREAKAWAY_Bull": 10,
        "CDLBREAKAWAY_Bear": 10,
        "CDLMORNINGSTAR_Bull": 12,
        "CDLMORNINGSTAR_Bear": 12,
        "CDLPIERCING_Bull": 13,
        "CDLPIERCING_Bear": 13,
        "CDLSTICKSANDWICH_Bull": 14,
        "CDLSTICKSANDWICH_Bear": 14,
        "CDLTHRUSTING_Bull": 15,
        "CDLTHRUSTING_Bear": 15,
        "CDLINNECK_Bull": 17,
        "CDLINNECK_Bear": 17,
        "CDL3INSIDE_Bull": 20,
        "CDL3INSIDE_Bear": 56,
        "CDLHOMINGPIGEON_Bull": 21,
        "CDLHOMINGPIGEON_Bear": 21,
        "CDLDARKCLOUDCOVER_Bull": 22,
        "CDLDARKCLOUDCOVER_Bear": 22,
        "CDLIDENTICAL3CROWS_Bull": 24,
        "CDLIDENTICAL3CROWS_Bear": 24,
        "CDLMORNINGDOJISTAR_Bull": 25,
        "CDLMORNINGDOJISTAR_Bear": 25,
        "CDLXSIDEGAP3METHODS_Bull": 27,
        "CDLXSIDEGAP3METHODS_Bear": 26,
        "CDLTRISTAR_Bull": 28,
        "CDLTRISTAR_Bear": 76,
        "CDLGAPSIDESIDEWHITE_Bull": 46,
        "CDLGAPSIDESIDEWHITE_Bear": 29,
        "CDLEVENINGDOJISTAR_Bull": 30,
        "CDLEVENINGDOJISTAR_Bear": 30,
        "CDL3WHITESOLDIERS_Bull": 32,
        "CDL3WHITESOLDIERS_Bear": 32,
        "CDLONNECK_Bull": 33,
        "CDLONNECK_Bear": 33,
        "CDL3OUTSIDE_Bull": 34,
        "CDL3OUTSIDE_Bear": 39,
        "CDLRICKSHAWMAN_Bull": 35,
        "CDLRICKSHAWMAN_Bear": 35,
        "CDLSEPARATINGLINES_Bull": 36,
        "CDLSEPARATINGLINES_Bear": 40,
        "CDLLONGLEGGEDDOJI_Bull": 37,
        "CDLLONGLEGGEDDOJI_Bear": 37,
        "CDLHARAMI_Bull": 38,
        "CDLHARAMI_Bear": 72,
        "CDLLADDERBOTTOM_Bull": 41,
        "CDLLADDERBOTTOM_Bear": 41,
        "CDLCLOSINGMARUBOZU_Bull": 70,
        "CDLCLOSINGMARUBOZU_Bear": 43,
        "CDLTAKURI_Bull": 47,
        "CDLTAKURI_Bear": 47,
        "CDLDOJISTAR_Bull": 49,
        "CDLDOJISTAR_Bear": 51,
        "CDLHARAMICROSS_Bull": 50,
        "CDLHARAMICROSS_Bear": 80,
        "CDLADVANCEBLOCK_Bull": 54,
        "CDLADVANCEBLOCK_Bear": 54,
        "CDLSHOOTINGSTAR_Bull": 55,
        "CDLSHOOTINGSTAR_Bear": 55,
        "CDLMARUBOZU_Bull": 71,
        "CDLMARUBOZU_Bear": 57,
        "CDLUNIQUE3RIVER_Bull": 60,
        "CDLUNIQUE3RIVER_Bear": 60,
        "CDL2CROWS_Bull": 61,
        "CDL2CROWS_Bear": 61,
        "CDLBELTHOLD_Bull": 62,
        "CDLBELTHOLD_Bear": 63,
        "CDLHAMMER_Bull": 65,
        "CDLHAMMER_Bear": 65,
        "CDLHIGHWAVE_Bull": 67,
        "CDLHIGHWAVE_Bear": 67,
        "CDLSPINNINGTOP_Bull": 69,
        "CDLSPINNINGTOP_Bear": 73,
        "CDLUPSIDEGAP2CROWS_Bull": 74,
        "CDLUPSIDEGAP2CROWS_Bear": 74,
        "CDLGRAVESTONEDOJI_Bull": 77,
        "CDLGRAVESTONEDOJI_Bear": 77,
        "CDLHIKKAKEMOD_Bull": 82,
        "CDLHIKKAKEMOD_Bear": 81,
        "CDLHIKKAKE_Bull": 85,
        "CDLHIKKAKE_Bear": 83,
        "CDLENGULFING_Bull": 84,
        "CDLENGULFING_Bear": 91,
        "CDLMATHOLD_Bull": 86,
        "CDLMATHOLD_Bear": 86,
        "CDLHANGINGMAN_Bull": 87,
        "CDLHANGINGMAN_Bear": 87,
        "CDLRISEFALL3METHODS_Bull": 94,
        "CDLRISEFALL3METHODS_Bear": 89,
        "CDLKICKING_Bull": 96,
        "CDLKICKING_Bear": 102,
        "CDLDRAGONFLYDOJI_Bull": 98,
        "CDLDRAGONFLYDOJI_Bear": 98,
        "CDLCONCEALBABYSWALL_Bull": 101,
        "CDLCONCEALBABYSWALL_Bear": 101,
        "CDL3STARSINSOUTH_Bull": 103,
        "CDL3STARSINSOUTH_Bear": 103,
        "CDLDOJI_Bull": 104,
        "CDLDOJI_Bear": 104,
        "CDLLONGLINE_Bull" : 105,
    "CDLSHORTLINE_Bull":52,
    "CDLLONGLINE_Bear" : 72,
    "CDLSHORTLINE_Bear" : 52,
    'CDLSTALLEDPATTERN_Bear': 107,
    'CDLCOUNTERATTACK_Bull':108,
    'CDLCOUNTERATTACK_Bear':1
    }

df = data
df['candlestick_pattern'] = np.nan
df['candlestick_match_count'] = np.nan
for index, row in df.iterrows():
    # no pattern found
    if len(row[candle_names]) - sum(row[candle_names] == 0) == 0:
        df.loc[index,'candlestick_pattern'] = "NO_PATTERN"
        df.loc[index, 'candlestick_match_count'] = 0
    # single pattern found
    elif len(row[candle_names]) - sum(row[candle_names] == 0) == 1:
        # bull pattern 100 or 200
        if any(row[candle_names].values > 0):
            patternsTemp = np.compress(row[candle_names].values != 0, row[candle_names].keys())
            pattern = list(patternsTemp[:].values)[0] + '_Bull'
            print(pattern)
            df.loc[index, 'candlestick_pattern'] = pattern
            df.loc[index, 'candlestick_match_count'] = 1
        # bear pattern -100 or -200
        else:
            patternsTemp = np.compress(row[candle_names].values != 0, row[candle_names].keys())            
            pattern = list(patternsTemp[:].values)[0] + '_Bear'
            print(pattern)
            df.loc[index, 'candlestick_pattern'] = pattern
            df.loc[index, 'candlestick_match_count'] = 1
    # multiple patterns matched -- select best performance
    else:
        # filter out pattern names from bool list of values
        patternsTemp = np.compress(row[candle_names].values != 0, row[candle_names].keys())
        patterns = list(patternsTemp[:].values)
        print(patterns)
        container = []
        for pattern in patterns:
            if row[pattern] > 0:
                container.append(pattern + '_Bull')
            else:
                container.append(pattern + '_Bear')
        rank_list = [candle_rankings[p] for p in container]
        if len(rank_list) == len(container):
            rank_index_best = rank_list.index(min(rank_list))
            df.loc[index, 'candlestick_pattern'] = container[rank_index_best]
            df.loc[index, 'candlestick_match_count'] = len(container)
# clean up candle columns
df.drop(candle_names, axis = 1, inplace = True) 



#Section 3
#Creating Dummies for all the Candle Patters found that are used in Machine Learning Algos
Dummy_variables = pd.get_dummies(df['candlestick_pattern'])
concated_dummy_columns = pd.concat([df,Dummy_variables], axis=1)
concated_dummy_columns.tail()
temp=df

#%%
#simple expected candle
# function that helps to take trades for the next candle
def f(df,candle_name,intrade_period,risk_to_reward):
    profit=[]
    loss=[]
    try:
        for i in range(0,len(df['candlestick_pattern'])-intrade_period):
            temp=df['candlestick_pattern']
            if temp[i] == candle_name and i!=len(temp):
                if df['Close'][i+intrade_period]-df['Open'][i+1]>0:
                    profit=profit+[df['Close'][i+intrade_period]-df['Open'][i+1]]
                else :
                    loss =loss+[df['Close'][i+intrade_period]-df['Open'][i+1]]
        if len(loss)+len(profit)<=20:
            raise Exception
        bull_probability=len(profit)/(len(profit)+len(loss))
        avg_profit=np.sum(np.array(profit))/len(profit)
        avg_loss=-np.sum(np.array(loss))/len(loss)
        if bull_probability*avg_profit>(1/risk_to_reward)*(1-bull_probability)*avg_loss:
            #a='going long is profitable'
            a_rep=1
        elif (1/risk_to_reward)*bull_probability*avg_profit<(1-bull_probability)*avg_loss:
            #a='going short is profitable'
            a_rep=-1
        else :
            #a='no trade is profitable'
            a_rep=0
    except Exception:
        #a='not enough data to conclude any decision'
        a_rep=0
    return a_rep

def g(df,previous_candle_name,current_candle_name,intrade_period,risk_to_reward):
    profit=[]
    loss=[]
    try:
        for i in range(1,len(df['candlestick_pattern'])-intrade_period):
            temp=df['candlestick_pattern']
            if  temp[i-1]== previous_candle_name and temp[i] == current_candle_name :
                if df['Close'][i+intrade_period]-df['Open'][i+1]>0:
                    profit=profit+[df['Close'][i+intrade_period]-df['Open'][i+1]]
                else :
                    loss =loss+[df['Close'][i+intrade_period]-df['Open'][i+1]]
        if len(loss)+len(profit)<=15:
            raise Exception
        bull_probability=len(profit)/(len(profit)+len(loss))
        avg_profit=np.sum(np.array(profit))/len(profit)
        avg_loss=-np.sum(np.array(loss))/len(loss)
        if bull_probability*avg_profit>(1/risk_to_reward)*(1-bull_probability)*avg_loss:
            #a='going long is profitable'
            a_rep=1
        elif (1/risk_to_reward)*bull_probability*avg_profit<(1-bull_probability)*avg_loss:
            #a='going short is profitable'
            a_rep=-1
        else :
            #a='no trade is profitable'
            a_rep=0
    except Exception:
        #a='not enough data to conclude'
        a_rep=0
    return a_rep

def h(df,primordial_candle_name,previous_candle_name,current_candle_name,intrade_period,risk_to_reward):
    profit=[]
    loss=[]
    try:
        for i in range(2,len(df['candlestick_pattern'])-intrade_period):
            temp=df['candlestick_pattern']
            if  temp[i-2] == primordial_candle_name and temp[i-1]==previous_candle_name and temp[i] == current_candle_name :
                if df['Close'][i+intrade_period]-df['Open'][i+1]>0:
                    profit=profit+[df['Close'][i+intrade_period]-df['Open'][i+1]]
            else :
                    loss =loss+[df['Close'][i+intrade_period]-df['Open'][i+1]]
            if len(loss)+len(profit)<=25:
                raise Exception
        bull_probability=len(profit)/(len(profit)+len(loss))
        avg_profit=np.sum(np.array(profit))/len(profit)
        avg_loss=-np.sum(np.array(loss))/len(loss)
        if bull_probability*avg_profit>(1/risk_to_reward)*(1-bull_probability)*avg_loss:
            #a='going long is profitable'
            a_rep=1
        elif (1/risk_to_reward)*bull_probability*avg_profit<(1-bull_probability)*avg_loss:
            #a='going short is profitable'
            a_rep=-1
        else :
            #a='no trade is profitable'
            a_rep=0
    except Exception:
        #a='not enough data to conclude'
        a_rep=0
    return a_rep
#storing data to temp for future use of functions f,g,h
#%%
#running the program again to get recent data to test over
#Section 1
# Identify the Candle type for each OHLC(Multiple candles are possible for a OHLC). A column os created for all the types of Candle Patterns found.
data=Client.historical_data('N','C',scripcode,'15m','2021-09-20','2021-09-28')
candle_names = talib.get_function_groups()['Pattern Recognition']

for candle in candle_names:
        # below is same as;
        # df["CDL3LINESTRIKE"] = talib.CDL3LINESTRIKE(op, hi, lo, cl)
        data.loc[:,candle] = getattr(talib, candle)(data.loc[:,'Open'], data.loc[:,'High'], data.loc[:,'Low'], data.loc[:,'Close'])
data.to_excel("temp.xlsx")

df = data
df['candlestick_pattern'] = np.nan
df['candlestick_match_count'] = np.nan
for index, row in df.iterrows():
    # no pattern found
    if len(row[candle_names]) - sum(row[candle_names] == 0) == 0:
        df.loc[index,'candlestick_pattern'] = "NO_PATTERN"
        df.loc[index, 'candlestick_match_count'] = 0
    # single pattern found
    elif len(row[candle_names]) - sum(row[candle_names] == 0) == 1:
        # bull pattern 100 or 200
        if any(row[candle_names].values > 0):
            patternsTemp = np.compress(row[candle_names].values != 0, row[candle_names].keys())
            pattern = list(patternsTemp[:].values)[0] + '_Bull'
            print(pattern)
            df.loc[index, 'candlestick_pattern'] = pattern
            df.loc[index, 'candlestick_match_count'] = 1
        # bear pattern -100 or -200
        else:
            patternsTemp = np.compress(row[candle_names].values != 0, row[candle_names].keys())            
            pattern = list(patternsTemp[:].values)[0] + '_Bear'
            print(pattern)
            df.loc[index, 'candlestick_pattern'] = pattern
            df.loc[index, 'candlestick_match_count'] = 1
    # multiple patterns matched -- select best performance
    else:
        # filter out pattern names from bool list of values
        patternsTemp = np.compress(row[candle_names].values != 0, row[candle_names].keys())
        patterns = list(patternsTemp[:].values)
        print(patterns)
        container = []
        for pattern in patterns:
            if row[pattern] > 0:
                container.append(pattern + '_Bull')
            else:
                container.append(pattern + '_Bear')
        rank_list = [candle_rankings[p] for p in container]
        if len(rank_list) == len(container):
            rank_index_best = rank_list.index(min(rank_list))
            df.loc[index, 'candlestick_pattern'] = container[rank_index_best]
            df.loc[index, 'candlestick_match_count'] = len(container)
# clean up candle columns
df.drop(candle_names, axis = 1, inplace = True) 
df1=df
data=Client.historical_data('N','C',scripcode,'15m','2021-09-10','2021-09-20')
candle_names = talib.get_function_groups()['Pattern Recognition']

for candle in candle_names:
        # below is same as;
        # df["CDL3LINESTRIKE"] = talib.CDL3LINESTRIKE(op, hi, lo, cl)
        data.loc[:,candle] = getattr(talib, candle)(data.loc[:,'Open'], data.loc[:,'High'], data.loc[:,'Low'], data.loc[:,'Close'])
data.to_excel("temp.xlsx")

df = data
df['candlestick_pattern'] = np.nan
df['candlestick_match_count'] = np.nan
for index, row in df.iterrows():
    # no pattern found
    if len(row[candle_names]) - sum(row[candle_names] == 0) == 0:
        df.loc[index,'candlestick_pattern'] = "NO_PATTERN"
        df.loc[index, 'candlestick_match_count'] = 0
    # single pattern found
    elif len(row[candle_names]) - sum(row[candle_names] == 0) == 1:
        # bull pattern 100 or 200
        if any(row[candle_names].values > 0):
            patternsTemp = np.compress(row[candle_names].values != 0, row[candle_names].keys())
            pattern = list(patternsTemp[:].values)[0] + '_Bull'
            print(pattern)
            df.loc[index, 'candlestick_pattern'] = pattern
            df.loc[index, 'candlestick_match_count'] = 1
        # bear pattern -100 or -200
        else:
            patternsTemp = np.compress(row[candle_names].values != 0, row[candle_names].keys())            
            pattern = list(patternsTemp[:].values)[0] + '_Bear'
            print(pattern)
            df.loc[index, 'candlestick_pattern'] = pattern
            df.loc[index, 'candlestick_match_count'] = 1
    # multiple patterns matched -- select best performance
    else:
        # filter out pattern names from bool list of values
        patternsTemp = np.compress(row[candle_names].values != 0, row[candle_names].keys())
        patterns = list(patternsTemp[:].values)
        print(patterns)
        container = []
        for pattern in patterns:
            if row[pattern] > 0:
                container.append(pattern + '_Bull')
            else:
                container.append(pattern + '_Bear')
        rank_list = [candle_rankings[p] for p in container]
        if len(rank_list) == len(container):
            rank_index_best = rank_list.index(min(rank_list))
            df.loc[index, 'candlestick_pattern'] = container[rank_index_best]
            df.loc[index, 'candlestick_match_count'] = len(container)
# clean up candle columns
df.drop(candle_names, axis = 1, inplace = True) 


#Section 3
#Creating Dummies for all the Candle Patters found that are used in Machine Learning Algos
Dummy_variables = pd.get_dummies(df['candlestick_pattern'])
concated_dummy_columns = pd.concat([df,Dummy_variables], axis=1)
concated_dummy_columns.tail()

#%%
# simple program to decide whether to enter into the trade or avoid 
# positive rating indicates long and negative rating indicates short 
def lead_trade(temp,current_rsi,RSI1,RSI2,intrade_period,risk_to_reward,current_candle_name,previous_candle_name,primordial_candle_name):

    a=f(temp,current_candle_name,intrade_period=intrade_period,risk_to_reward=risk_to_reward)
    a1=g(temp,previous_candle_name,current_candle_name,intrade_period=intrade_period,risk_to_reward=risk_to_reward)
    a2=h(temp,primordial_candle_name,previous_candle_name,current_candle_name,intrade_period=intrade_period,risk_to_reward=risk_to_reward)
    if a>=0 and a1>=0 and a2>=0 and current_rsi<=RSI1:
        rating = a+a1+a2
    elif a<=0 and a1<=0 and a2<=0 and current_rsi>=RSI2:
        rating = a+a1+a2
    else:
        rating=0
    return rating
#%%
# program that decides the risk to reward ratio and candles to wait while in a trade.
# please note that it is optimised by Particle Swarm Optimisation (global optimisation technique) and might not give same result every time we run it with all parameters remained same
#x[0] is number of candles to wait for exit
#x[1] is risk_to_reward ratio
# find(x) is the function that returns objective
#plot1 is the test data progress
#plot2 is the train data progress
#intrade_period is int(x[0])
#Eg: x=[1,3]
#Eg: temp is 2020 jan to 2021 sep1,
# df sep1 to sep5
# df2 sep6 to sep10
temp = ind(temp)
temp['def']=temp['MFI']-temp['RSI']
df=ind(df)
df['def']=df['MFI']-df['RSI']
df1=ind(df1)
df1['def']=df1['MFI']-df1['RSI']
item=0
x_on_iter=[]
plot1=[]
plot2=[]
lb = [2,0.01,temp['def'].min(),temp['def'].min()]
ub = [2.1,1,temp['def'].max(),temp['def'].max()]
swarmsize=20
def find(x):
    global plot1
    global plot2
    global item
    global x_on_iter
    global swarmsize
    global temp
    today_profit = 0
    today_profit1=0
    trades_taken = 0
    intrade_period = int(x[0])
    risk_to_reward = x[1]
    def1=x[2]
    def2=x[3]
    for i in range(23,len(df['candlestick_pattern'])-intrade_period):
        a=f(temp,df['candlestick_pattern'][i],intrade_period=intrade_period,risk_to_reward=risk_to_reward)
        a1=g(temp,df['candlestick_pattern'][i-1],df['candlestick_pattern'][i],intrade_period=intrade_period,risk_to_reward=risk_to_reward)
        a2=h(temp,df['candlestick_pattern'][i-2],df['candlestick_pattern'][i-1],df['candlestick_pattern'][i],intrade_period=intrade_period,risk_to_reward=risk_to_reward)
        #p_str = 'going long is profitable'
        #l_str = 'going short is profitable'
        if a>=0 and a1>=0 and a2>=0 and df['def'][i]<=def1:
            rating = a+a1+a2
        elif a<=0 and a1<=0 and a2<=0 and df['def'][i]>=def2:
            rating = a+a1+a2
        else:
            rating=0
        
        if df['candlestick_pattern'][i]!='NO_PATTERN':
            if rating>0 :
                trades_taken=trades_taken+1
                today_profit=today_profit+df['Close'][i+intrade_period]-df['Open'][i+1]
            elif rating<0 :
                trades_taken=trades_taken+1
                today_profit=today_profit+df['Open'][i+1]-df['Close'][i+intrade_period]
        
    for i in range(2,len(df1['candlestick_pattern'])-intrade_period):
        b=f(temp,df1['candlestick_pattern'][i],intrade_period=intrade_period,risk_to_reward=risk_to_reward)
        b1=g(temp,df1['candlestick_pattern'][i-1],df1['candlestick_pattern'][i],intrade_period=intrade_period,risk_to_reward=risk_to_reward)
        b2=h(temp,df1['candlestick_pattern'][i-2],df1['candlestick_pattern'][i-1],df1['candlestick_pattern'][i],intrade_period=intrade_period,risk_to_reward=risk_to_reward)
        #p_str = 'going long is profitable'
        #l_str = 'going short is profitable'
        if b>=0 and b1>=0 and b2>=0 and df1['def'][i]<=def1:
            rating1 = b+b1+b2
        elif b<=0 and b1<=0 and b2<=0 and df1['def'][i]>=def2:
            rating1 = b+b1+b2
        else:
            rating1=0
        if df1['candlestick_pattern'][i]!='NO_PATTERN':
            if rating1>0 :
                today_profit1=today_profit1+df1['Close'][i+intrade_period]-df1['Open'][i+1]
            elif rating1<0 :
                today_profit1=today_profit1+df1['Open'][i+1]-df1['Close'][i+intrade_period]
    index=int(item/swarmsize)
    item=item+1
    if len(plot1)>=index+1:
        if plot1[-1]<=today_profit:
            plot1[-1]=today_profit
            plot2[-1]=today_profit1
            x_on_iter[-1] = x
    elif len(plot1)<index+1:
        plot1=plot1+[today_profit]
        plot2=plot2+[today_profit1]
        x_on_iter = x_on_iter+[x]
    return -today_profit/intrade_period
(xopt,fopt)=pso(find,lb=lb,ub=ub,swarmsize=swarmsize,maxiter=15)
plt.plot(-np.array(plot1))
plt.plot(-np.array(plot2))
plt.show()
# please use the function lead_trade() to enter into the trade.
#plot1 and plot2 gives a brief idea on how PSO is working with datasets
#int(xopt[0]) is the last iteration's best possibility for intrade_period
#xopt[1] is the last iteration's best possibility for risk_to_reward ratio

# %%
