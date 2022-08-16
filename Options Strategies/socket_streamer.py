#%%
import matplotlib.pyplot as plt
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
from py5paisa.order import Basket_order

def client_login(client):
    import json
    f = open ('credentials.json', "r")
    creds = json.loads(f.read())
    client_list={}
    client_list[client]={'strategy':{},'login':{},'lots':{}}
    vinathi_cred = creds[client]["keys"]
    user = creds[client]["user"]
    passw = creds[client]["passw"]
    dob = creds[client]["dob"]
    client_list[client]['strategy']=strategies(user=user, passw=passw, dob=dob,cred=vinathi_cred)
    client_list[client]['login']=FivePaisaClient(email=user, passwd=passw, dob=dob,cred=vinathi_cred)
    client_list[client]['login'].login()
    client_list[client]['lots']=round((client_list[client]['login'].margin()[0]['AvailableMargin']-200000)/180000)
    return client_list[client]
#client_name=input('enter the client name Eg: vinathi,bhaskar ')
import sys
client_name   = 'vinathi'
prime_client=client_login(client=client_name)
#%%
expiry_timestamps=prime_client['login'].get_expiry("N","BANKNIFTY").copy()
current_expiry_time_stamp_weekly=int(expiry_timestamps['Expiry'][0]['ExpiryDate'][6:19])
option_chain=pd.DataFrame(prime_client['login'].get_option_chain("N","BANKNIFTY",current_expiry_time_stamp_weekly)['Options'])
c_data=option_chain[option_chain['CPType']=='CE']
p_data=option_chain[option_chain['CPType']=='PE']
c_scrips={}
p_scrips={}
c_strikes={}
p_strikes={}
#%%
for i in range(0,len(c_data)):
    c_scrips[c_data['StrikeRate'].iloc[i]]=int(c_data[c_data['StrikeRate']==c_data['StrikeRate'].iloc[i]]['ScripCode'])
    c_strikes[int(c_data[c_data['StrikeRate']==c_data['StrikeRate'].iloc[i]]['ScripCode'])]=c_data['StrikeRate'].iloc[i]
for i in range(0,len(p_data)):
    p_scrips[p_data['StrikeRate'].iloc[i]]=int(p_data[p_data['StrikeRate']==p_data['StrikeRate'].iloc[i]]['ScripCode'])
    p_strikes[int(p_data[p_data['StrikeRate']==p_data['StrikeRate'].iloc[i]]['ScripCode'])]=p_data['StrikeRate'].iloc[i]
#%%
req_list=[]
a=list(c_strikes.keys())
b=list(p_strikes.keys())
for i in a:
    req_list=req_list+[
                { "Exch":"N","ExchType":"D","ScripCode":i},
                ]
for i in b:
    req_list=req_list+[
                { "Exch":"N","ExchType":"D","ScripCode":i},
                ]
req_data=prime_client['login'].Request_Feed('oi','s',req_list)
req_data2=prime_client['login'].Request_Feed('mf','s',req_list)
c_oi={}
p_oi={}
def on_message(ws, message):
    print(message)
    a=json.loads(message)
    try:
        c_oi[c_strikes[a['Token']]]=a['OpenInterest']
    except Exception:
        p_oi[p_strikes[a['Token']]]=a['OpenInterest']
    print(c_oi)
    print(p_oi)

c_lastrate={}
p_lastrate={}
def on_message2(ws,message2):
    a=json.loads(message2)[0]
    try:
        c_lastrate[c_strikes[a['Token']]]=a['LastRate']
    except Exception:
        p_lastrate[p_strikes[a['Token']]]=a['LastRate']
    print(c_lastrate)
    print(p_lastrate)


prime_client['login'].connect(req_data)
prime_client['login'].connect(req_data2)
prime_client['login'].receive_data(on_message)
prime_client['login'].receive_data(on_message2)

# %%
def rosetta_strikes(option_chain):
    pe_data=option_chain[option_chain['CPType']=='PE']
    ce_data=option_chain[option_chain['CPType']=='CE']
    i=np.array(pe_data['StrikeRate'])[0]
    n=np.array(pe_data['StrikeRate'])[1]
    end=np.array(pe_data['StrikeRate'])[-1]
    ss=np.array(pe_data['StrikeRate'])
    p_lastrate=np.array(pe_data['LastRate'])
    c_lastrate=np.array(ce_data['LastRate'])
    p_openinterest=np.array(pe_data['OpenInterest'])
    c_openinterest=np.array(ce_data['OpenInterest'])
    data=[]
    data1=[]
    data2=[]
    increment=(n-i)/100
    while i<end:
        i=i+increment
        init_ce=0
        init_pe=0
        end_pe=0
        end_ce=0
        for k in range(0,len(ss)):
            init_pe=init_pe+p_lastrate[k]*p_openinterest[k]
            init_ce=init_ce+c_lastrate[k]*c_openinterest[k]
            end_pe=end_pe+p_openinterest[k]*max((ss[k]-i),0)
            end_ce=end_ce+c_openinterest[k]*max((i-ss[k]),0)
        data=data+[init_ce-end_ce-init_pe+end_pe]
        data1=data1+[init_ce-end_ce]
        data2=data2+[-init_pe+end_pe]
    index=np.argmin(np.abs(data))
    index1=np.argmin(np.abs(data1))
    index2=np.argmin(np.abs(data2))
    a=np.array(option_chain['StrikeRate'])[0]+index*increment
    b=np.array(option_chain['StrikeRate'])[0]+index1*increment
    c=np.array(option_chain['StrikeRate'])[0]+index2*increment
    return  a,round(b/100)*100,round(c/100)*100