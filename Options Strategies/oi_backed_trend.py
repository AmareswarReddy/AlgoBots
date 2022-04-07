#%%
import numpy as np
import pandas as pd
import json
from time import sleep, strftime
from py5paisa import FivePaisaClient
from py5paisa.strategy import *
from py5paisa.logging import log_response
from datetime import datetime 
from datetime import date
import requests
from pytz import timezone 
from cred import *
expiry=input('enter the expiry Eg:"07-Apr-2022"')
cred={
    "APP_NAME":"5P55115625",
    "APP_SOURCE":'8899',
    "USER_ID":"qZS8Qd5THYc",
    "PASSWORD":"O4X41D47h1g",
    "USER_KEY":"BDYHVFfDodmHw3RXeWzuc2acdOwczZ64",
    "ENCRYPTION_KEY":"jhxJH0k6BIUL6VnXYPIAcqTZLqYWhkLc"
    }
strategy=strategies(user="vinathi.bujji@gmail.com", passw="alliswell1@A", dob="19940830",cred=cred)

#%%
def pe_oi(strikeprice):
    return df[df['strikePrice']==strikeprice]['PE'].iloc[0]['openInterest']
def ce_oi(strikeprice):
    return df[df['strikePrice']==strikeprice]['CE'].iloc[0]['openInterest']
def pe_oi_change(strikeprice):
    return df[df['strikePrice']==strikeprice]['PE'].iloc[0]['changeinOpenInterest']
def ce_oi_change(strikeprice):
    return df[df['strikePrice']==strikeprice]['CE'].iloc[0]['changeinOpenInterest']
def simple_trend():
    req_list_=[{"Exch":"N","ExchType":"C","Symbol":"BANKNIFTY","Scripcode":"999920005","OptionType":"EQ"}]          
    a=strategy.fetch_market_feed(req_list_)
    x=a['Data'][0]['LastRate']
    bot=np.floor(x/100)*100
    top=np.ceil(x/100)*100
    bot_at=np.floor(x/500)*500
    top_at=np.ceil(x/500)*500
    if top_at-x>250:
        bot_500=bot_at-500
        top_500=bot_at+500
        top_1000=bot_at+1000
        bot_1000=bot_at-1000
    else:
        bot_500=top_at-500
        top_500=top_at+500
        top_1000=top_at+1000
        bot_1000=top_at-1000
    ce_net=ce_oi(bot)+ce_oi(top)+ce_oi(top_500)+ce_oi(top_1000)
    pe_net=pe_oi(bot)+pe_oi(top)+pe_oi(bot_500)+pe_oi(bot_1000)
    if ce_net>pe_net:
        return 'downtrend'
    else:
        return 'uptrend'

def complex_trend():
    req_list_=[{"Exch":"N","ExchType":"C","Symbol":"BANKNIFTY","Scripcode":"999920005","OptionType":"EQ"}]          
    a=strategy.fetch_market_feed(req_list_)
    x=a['Data'][0]['LastRate']
    x_change=a['Data'][0]['Chg']
    bot=np.floor(x/100)*100
    top=np.ceil(x/100)*100
    bot_at=np.floor(x/500)*500
    top_at=np.ceil(x/500)*500
    if top_at-x>250:
        bot_500=bot_at-500
        top_500=bot_at+500
        top_1000=bot_at+1000
        bot_1000=bot_at-1000
    else:
        bot_500=top_at-500
        top_500=top_at+500
        top_1000=top_at+1000
        bot_1000=top_at-1000
    ce_net_change=ce_oi_change(bot)+ce_oi_change(top)+ce_oi_change(top_500)+ce_oi_change(top_1000)
    pe_net_change=pe_oi_change(bot)+pe_oi_change(top)+pe_oi_change(bot_500)+pe_oi_change(bot_1000)
    if x_change>0 :
        if pe_net_change>0 and ce_net_change<0:
            return "uptrend at it's peak"
        if pe_net_change<0 and ce_net_change>0:
            return "strong downtrend about to start in a while"
        if pe_net_change<0 and ce_net_change<0:
            return "A strong move on either side is a possibility"
        if pe_net_change>0 and ce_net_change>0:
            return "stable market begins"
    if x_change<=0 :
        if pe_net_change>0 and ce_net_change<0:
            return "strong uptrend about to start in a while"
        if pe_net_change<0 and ce_net_change>0:
            return "downtrend at it's peak"
        if pe_net_change<0 and ce_net_change<0:
            return "A strong move on either side is a possibility"
        if pe_net_change>0 and ce_net_change>0:
            return "stable market begins"    
def projected():
    i=np.array(df['strikePrice'])[0]
    end=np.array(df['strikePrice'])[-1]
    ss=np.array(df['strikePrice'])
    data=[]
    while i<end:
        i=i+10
        init_ce=0
        init_pe=0
        end_pe=0
        end_ce=0
        for k in range(0,len(np.array(df['strikePrice']))):
            init_pe=init_pe+df['PE'].iloc[k]['lastPrice']*df['PE'].iloc[k]['openInterest']
            init_ce=init_ce+df['CE'].iloc[k]['lastPrice']*df['CE'].iloc[k]['openInterest']
            end_pe=end_pe+df['PE'].iloc[k]['openInterest']*max((ss[k]-i),0)
            end_ce=end_ce+df['CE'].iloc[k]['openInterest']*max((i-ss[k]),0)
        data=data+[init_ce-end_ce-init_pe+end_pe]
    index=np.argmin(np.abs(data))
    return   np.array(df['strikePrice'])[0]+10*index
        #print(init_ce-end_ce-init_pe+end_pe)



while True:
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; '
                'x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36'}
    main_url = "https://www.nseindia.com/"
    response = requests.get(main_url, headers=headers)
    '''print(response.status_code)'''
    cookies = response.cookies
    url = "https://www.nseindia.com/api/option-chain-indices?symbol=BANKNIFTY"
    bank_nifty_oi_data = requests.get(url, headers=headers, cookies=cookies)
    '''print(bank_nifty_oi_data.status_code)'''
    '''print("BN OI data", bank_nifty_oi_data.text)'''
    url = "https://www.nseindia.com/api/option-chain-indices?symbol=NIFTY"
    nifty_oi_data = requests.get(url, headers=headers, cookies=cookies)
    '''print(nifty_oi_data.status_code)'''
    '''print("Nifty OI data", nifty_oi_data.text)'''
    a=json.loads(bank_nifty_oi_data.text)
    k=pd.DataFrame(a['records']['data'])
    df=k[k.expiryDate==expiry]
    df.drop(['expiryDate'],axis=1)
    print(simple_trend())
    print(complex_trend())
    print(projected())
# %%
