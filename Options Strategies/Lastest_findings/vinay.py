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
#pygame.init()
#s = pygame.mixer.Sound("alarm.wav")
def pearsonr(x, y):
    n = len(x)
    x = np.asarray(x)
    y = np.asarray(y)
    dtype = type(1.0 + x[0] + y[0])
    if n == 2:
        return dtype(np.sign(x[1] - x[0])*np.sign(y[1] - y[0])), 1.0
    xmean = x.mean(dtype=dtype)
    ymean = y.mean(dtype=dtype)
    xm = x.astype(dtype) - xmean
    ym = y.astype(dtype) - ymean
    normxm = np.linalg.norm(xm)
    normym = np.linalg.norm(ym)
    r = np.dot(xm/normxm, ym/normym)
    r = max(min(r, 1.0), -1.0)
    return r,0

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
#lots=int(input('lots (Eg:3):'))
#tron=int(input('enter the number of lots for buying :'))
change=1000
def rosetta_strikes(option_chain,x,change):
    pe_data=option_chain[option_chain['CPType']=='PE']
    #pe_data=pe_data[pe_data['StrikeRate']<x+change]
    ce_data=option_chain[option_chain['CPType']=='CE']
    #ce_data=ce_data[ce_data['StrikeRate']>x-change]
    i=np.array(pe_data['StrikeRate'])[0]
    end=np.array(pe_data['StrikeRate'])[-1]
    ss=np.array(pe_data['StrikeRate'])
    p_lastrate=np.array(list(pe_data[pe_data['StrikeRate']<=x+change]['LastRate'])+list(pe_data[pe_data['StrikeRate']>x+change]['LastRate']*0))
    c_lastrate=np.array(list(ce_data[ce_data['StrikeRate']<x-change]['LastRate']*0)+list(ce_data[ce_data['StrikeRate']>=x-change]['LastRate']))
    p_openinterest=np.array(list(pe_data[pe_data['StrikeRate']<=x+change]['OpenInterest'])+list(pe_data[pe_data['StrikeRate']>x+change]['OpenInterest']*0))
    c_openinterest=np.array(list(ce_data[ce_data['StrikeRate']<x-change]['OpenInterest']*0)+list(ce_data[ce_data['StrikeRate']>=x-change]['OpenInterest']))
    data=[]
    data1=[]
    data2=[]
    increment=2
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

def rosetta_ratio(option_chain,memory,a2,a1):
    pe_data=option_chain[option_chain['CPType']=='PE']
    ce_data=option_chain[option_chain['CPType']=='CE']
    try:
        pe_data2=memory[memory['CPType']=='PE']
        ce_data2=memory[memory['CPType']=='CE']
        p_openinterest2=np.array(list(pe_data2['OpenInterest']))
        c_openinterest2=np.array(list(ce_data2['OpenInterest']))
        p_openinterest=np.array(list(pe_data['OpenInterest']))-p_openinterest2
        c_openinterest=np.array(list(ce_data['OpenInterest']))-c_openinterest2
    except Exception:
        p_openinterest=np.array(list(pe_data['OpenInterest']))
        c_openinterest=np.array(list(ce_data['OpenInterest']))
    p_lastrate=np.array(list(pe_data['LastRate']))
    c_lastrate=np.array(list(ce_data['LastRate']))
    pp=p_lastrate[np.multiply(p_lastrate!=0, p_openinterest!=0)]
    po=p_openinterest[np.multiply(p_lastrate!=0, p_openinterest!=0)]
    cp=c_lastrate[np.multiply(c_lastrate!=0, c_openinterest!=0)]
    co=c_openinterest[np.multiply(c_lastrate!=0, c_openinterest!=0)]
    a1=a1+np.dot(1/np.array(pp),np.array(po))
    a2=a2+np.dot(1/np.array(cp),np.array(co))
    a=a2/a1
    return  np.round_(((1/np.exp(a))-(1/np.exp(1)))*158.2,2),a2,a1

def rosetta_distance_ratio(option_chain,memory,b2,b1,x):
    pe_data=option_chain[option_chain['CPType']=='PE']
    ce_data=option_chain[option_chain['CPType']=='CE']
    
    try:
        pe_data2=memory[memory['CPType']=='PE']
        ce_data2=memory[memory['CPType']=='CE']
        p_openinterest2=np.array(list(pe_data2['OpenInterest']))
        c_openinterest2=np.array(list(ce_data2['OpenInterest']))
        p_openinterest=np.array(list(pe_data['OpenInterest']))-p_openinterest2
        c_openinterest=np.array(list(ce_data['OpenInterest']))-c_openinterest2
    except Exception:
        p_openinterest=np.array(list(pe_data['OpenInterest']))
        c_openinterest=np.array(list(ce_data['OpenInterest']))
    p_lastrate=np.array(list(pe_data['LastRate']))
    c_lastrate=np.array(list(ce_data['LastRate']))
    pp=p_lastrate[np.multiply(p_lastrate!=0, p_openinterest!=0)]
    po=p_openinterest[np.multiply(p_lastrate!=0, p_openinterest!=0)]
    cp=c_lastrate[np.multiply(c_lastrate!=0, c_openinterest!=0)]
    co=c_openinterest[np.multiply(c_lastrate!=0, c_openinterest!=0)]
    p_strikes=np.exp((x-np.array(list(pe_data['StrikeRate'])))/2000)[np.multiply(p_lastrate!=0, p_openinterest!=0)]
    c_strikes=np.exp((np.array(list(ce_data['StrikeRate']))-x)/2000)[np.multiply(c_lastrate!=0, c_openinterest!=0)]
    tone1=1/np.multiply(p_strikes,np.array(pp))
    tone2=1/np.multiply(c_strikes,np.array(cp))
    b1=b1+np.dot(tone1,np.array(po))
    b2=b2+np.dot(tone2,np.array(co))
    b=b2/b1
    return  np.round_(((1/np.exp(b))-(1/np.exp(1)))*158.2,2),b2,b1
prime_client=client_login(client=client_name)
memory=0
a1,a2=0,0
b1,b2=0,0
capture=[]
capture2=[]
lastrate=[]
#%%

while True:
    while True:
        try :
            expiry_timestamps=prime_client['login'].get_expiry("N","BANKNIFTY").copy()
            current_expiry_time_stamp_weekly=int(expiry_timestamps['Expiry'][0]['ExpiryDate'][6:19])
            option_chain=pd.DataFrame(prime_client['login'].get_option_chain("N","BANKNIFTY",current_expiry_time_stamp_weekly)['Options'])
            x=expiry_timestamps['lastrate'][0]['LTP']
            break
        except Exception :
            pass
    a,a2,a1=rosetta_ratio(option_chain,memory,a2,a1)
    b,b2,b1=rosetta_distance_ratio(option_chain,memory,b2,b1,x)
    memory=option_chain.copy()
    capture=capture+[a]
    capture2=capture2+[b]
    lastrate=lastrate+[x]
    print('new_generation',a)
    print('high in the sky',b)
    sleep(1)
#%%
fig, ax_left = plt.subplots()
ax_right = ax_left.twinx()
ax_left.plot(lastrate[-1500:], color='blue')
ax_right.plot(capture2[-1500:], color='red')
# %%
