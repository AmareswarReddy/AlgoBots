#%%
import numpy as np
import pandas as pd
import json
from time import sleep, strftime,time
from py5paisa import FivePaisaClient
from py5paisa.strategy import strategies
from py5paisa.logging import log_response
from datetime import datetime 
from datetime import date
import requests
from pytz import timezone 
from cred import *
import os

cred={
    "APP_NAME":"5P56936208",
    "APP_SOURCE":"2179",
    "USER_ID":"w6MJ1dw5Yd0",
    "PASSWORD":"V7JkGTUudjt",
    "USER_KEY":"8Q4SSCEo0bOgroVMFcNB0nTTB6CGPQuE",
    "ENCRYPTION_KEY":"HEgo6erh7qmqnDjRXIbaRTSNyfI6eofO"
        }
Client = FivePaisaClient(email='vinaykumar7295@gmail.com', passwd='godofwar1@A',dob='19700701', cred=cred)
Client.login()

def get_scripcode(symbol,strike,expiry,opt):
    month={
        "01":'JAN',
        "02":'FEB',
        "03":'MAR',
        "04":'APR',
        "05":'MAY',
        "06":'JUN',
        "07":'JUL',
        "08":'AUG',
        "09":'SEP',
        "10":'OCT',
        "11":'NOV',
        "12":'DEC'      
    }
    date=expiry[6:]
    mon=month[expiry[4:6]]
    year=expiry[:4]
    symbol=symbol.upper()
    strike_f="{:.2f}".format(float(strike))
    sym=f'{symbol} {date} {mon} {year} {opt} {strike_f}'
    req=[{"Exch":"N","ExchType":"D","Symbol":sym,"Expiry":expiry,"StrikePrice":strike,"OptionType":opt}]
    res=Client.fetch_market_feed(req)
    token=res['Data'][0]['Token']
    return token

starttime = time()
tracker = 1
expiry=str(input('enter the current expiry(Eg: "20210916" ) : '))
req_list_=[{"Exch":"N","ExchType":"C","Symbol":"BANKNIFTY","Scripcode":"999920005","OptionType":"EQ"}]          
a=Client.fetch_market_feed(req_list_)
x=a['Data'][0]['LastRate']
directory_pe={}
directory_ce={}
req_list=[]
for i in range(0,30):
    temp=get_scripcode(symbol='banknifty',strike=str((round(x/100)*100)-i*100),expiry=expiry,opt='PE')
    req_list=req_list+[
                { "Exch":"N","ExchType":"D","Scripcode":str(temp)},
                ]
    
    directory_pe[str(temp)]= {}
    directory_pe[str(temp)]['type']= 'PE'
    directory_pe[str(temp)]['oi']= []
    directory_pe[str(temp)]['strikeprice']= str((round(x/100)*100)-i*100)
    #print(directory_pe)
#dict1=Client.Request_Feed('oi','s',req_list)
for i in range(0,30):
    temp=get_scripcode(symbol='banknifty',strike=str((round(x/100)*100)+i*100),expiry=expiry,opt='CE')
    req_list=req_list+[
                { "Exch":"N","ExchType":"D","Scripcode":str(temp)},
                ]
    directory_ce[str(temp)]= {}
    directory_ce[str(temp)]['type']= 'CE'
    directory_ce[str(temp)]['oi']= []
    directory_ce[str(temp)]['strikeprice']= str((round(x/100)*100)+i*100)
dict1=Client.Request_Feed('oi','s',req_list)

def on_message(ws,message):
    message=json.loads(message)
    a=message
    global tracker
    try:
        if directory_ce[str(a['Token'])]['type']=='CE':
            directory_ce[str(a['Token'])]['oi'].append(a['OpenInterest'])
            print(directory_ce[str(a['Token'])])
    except Exception:
        if directory_pe[str(a['Token'])]['type']=='PE':
            directory_pe[str(a['Token'])]['oi'].append(a['OpenInterest'])
            print(max(directory_pe[str(a['Token'])]['oi']))
            print(min(directory_pe[str(a['Token'])]['oi']))
            print(np.average(directory_pe[str(a['Token'])]['oi']))
            print(directory_pe[str(a['Token'])]['oi'][-1])
            

    trial_time=int((time()-starttime)/1800)
    if trial_time ==  tracker :
        tracker = tracker + 1


Client.Streming_data(dict1, on_message)

# Note : Pass Dictionary in Parameter Field
# %%
