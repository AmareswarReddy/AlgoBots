import pandas as pd
from ta.utils import dropna
from ta.volatility import BollingerBands
import matplotlib.pyplot as plt
import talib
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
data=Client.historical_data('N','C',1660,'15m','2021-08-17','2021-09-17')
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
    "CDLSHORTLINE_Bear" : 52
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

#simple expected candle
# function that helps to take trades for the next candle
def f(df,candle_name):

    profit=[]
    loss=[]
    try:
        for i in range(0,len(df['candlestick_pattern'])):
            temp=df['candlestick_pattern']
            if temp[i] == candle_name and i!=len(temp):
                if df['Close'][i+1]-df['Open'][i+1]>0:
                    profit=profit+[df['Close'][i+1]-df['Open'][i+1]]
                else :
                    loss =loss+[df['Close'][i+1]-df['Open'][i+1]]
        if len(loss)+len(profit)<=4:
            raise Exception
        bull_probability=len(profit)/(len(profit)+len(loss))
        avg_profit=np.sum(np.array(profit))/len(profit)
        avg_loss=-np.sum(np.array(loss))/len(loss)
        if bull_probability*avg_profit>(1-bull_probability)*avg_loss:
            a='going long is profitable'
        elif bull_probability*avg_profit<(1-bull_probability)*avg_loss:
            a='going short is profitable'
        else :
            a='no trade is profitable'
    except Exception:
        a='not enough data to conclude any decision'
    return a
f(df,candle_name='CDLBELTHOLD_Bull')

def g(df,previous_candle_name,current_candle_name):
    profit=[]
    loss=[]
    try:
        for i in range(0,len(df['candlestick_pattern'])):
            temp=df['candlestick_pattern']
            if  temp[i]== previous_candle_name and temp[i+1] == current_candle_name and i<(len(temp)-1):
                if df['Close'][i+2]-df['Open'][i+2]>0:
                    profit=profit+[df['Close'][i+2]-df['Open'][i+2]]
                else :
                    loss =loss+[df['Close'][i+2]-df['Open'][i+2]]
        if len(loss)+len(profit)<=4:
            raise Exception
        bull_probability=len(profit)/(len(profit)+len(loss))
        avg_profit=np.sum(np.array(profit))/len(profit)
        avg_loss=-np.sum(np.array(loss))/len(loss)
        if bull_probability*avg_profit>(1-bull_probability)*avg_loss:
            a='going long is profitable'
        elif bull_probability*avg_profit<(1-bull_probability)*avg_loss:
            a='going short is profitable'
        else :
            a='no trade is profitable'
    except Exception:
        a='not enough data to conclude'
    return a
g(df,previous_candle_name='NO_PATTERN',current_candle_name='CDLBELTHOLD_Bull')


def h(df,primordial_candle_name,previous_candle_name,current_candle_name):
    profit=[]
    loss=[]
    try:
        for i in range(0,len(df['candlestick_pattern'])):
            temp=df['candlestick_pattern']
            if  temp[i]== primordial_candle_name and temp[i+1]==previous_candle_name and temp[i+2] == current_candle_name and i<(len(temp)-2):
                if df['Close'][i+3]-df['Open'][i+3]>0:
                    profit=profit+[df['Close'][i+3]-df['Open'][i+3]]
            else :
                    loss =loss+[df['Close'][i+3]-df['Open'][i+3]]
            if len(loss)+len(profit)<=4:
                raise Exception
        bull_probability=len(profit)/(len(profit)+len(loss))
        avg_profit=np.sum(np.array(profit))/len(profit)
        avg_loss=-np.sum(np.array(loss))/len(loss)
        if bull_probability*avg_profit>(1-bull_probability)*avg_loss:
            a='going long is profitable'
        elif bull_probability*avg_profit<(1-bull_probability)*avg_loss:
            a='going short is profitable'
        else :
            a='no trade is profitable'
    except Exception:
        a='not enough data to conclude'
    return a
h(df,primordial_candle_name='NO_PATTERN',previous_candle_name='NO_PATTERN',current_candle_name='CDLBELTHOLD_Bull')