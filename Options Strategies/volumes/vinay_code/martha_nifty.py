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
import pygame
pygame.init()
s = pygame.mixer.Sound("alarm.wav")
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
    client_list[client]['lots']=0
    return client_list[client]
#client_name=input('enter the client name Eg: vinathi,bhaskar ')
import sys
client_name   = 'bhaskar'
#%%
#lots=int(input('lots (Eg:3):'))
tron=int(input('enter the number of lots for buying :'))
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
    increment=(n-i)/15
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
    return  a,round(b/50)*50,round(c/50)*50

def past_picture(indicator,project_k,b_lastrate,x):
    indicator=indicator+[project_k]
    b_lastrate=b_lastrate+[x]
    n=len(b_lastrate)
    div_factor=0
    local_div_factor=0
    instant_div_factor=0
    '''if n>2:'''
    '''    for i in range(1,n):'''
    '''        a=(b_lastrate[n-1]-b_lastrate[i])'''
    '''        b=(indicator[n-1]-indicator[i])'''
    '''        div_factor=div_factor+b '''
    '''    div_factor=div_factor/n'''
    if n>121:
        for i in range(n-120,n):
            b=(indicator[n-1]-indicator[i])
            local_div_factor=local_div_factor+b
        local_div_factor=local_div_factor/120
    if n>21:
        for i in range(n-20,n):
            b=(indicator[n-1]-indicator[i])
            instant_div_factor=instant_div_factor+b
        instant_div_factor=instant_div_factor/20
    return indicator,b_lastrate,div_factor,local_div_factor,instant_div_factor

def strike_list(strike1,strike2):
    k=[]
    if strike1>strike2:
        a=strike2
        while a<=strike1:
            k=k+[a]
            a=a+100
    else:
        a=strike1
        while a<=strike2:
            k=k+[a]
            a=a+100
    return k

def packup(option_chain,prime_client,taken_trade,exclusive_strike,tron):
    if taken_trade==-1:
        p_data=option_chain[option_chain['CPType']=='PE']
        p_scrip=int(p_data[p_data['StrikeRate']==exclusive_strike]['ScripCode'])
        test_order = Order(order_type='S',exchange='N',exchange_segment='D', scrip_code =p_scrip, quantity=50*tron, price=0 ,is_intraday=False,remote_order_id="tag")
        prime_client['login'].place_order(test_order)
    elif taken_trade==1:
        c_data=option_chain[option_chain['CPType']=='CE']
        c_scrip=int(c_data[c_data['StrikeRate']==exclusive_strike]['ScripCode'])
        test_order = Order(order_type='S',exchange='N',exchange_segment='D', scrip_code =c_scrip, quantity=50*tron, price=0 ,is_intraday=False,remote_order_id="tag")
        prime_client['login'].place_order(test_order)
    return 0

def decoy4(option_chain,exclusive_strike,taken_trade,to_deal,del_to_deal,tempo,lots_tuner,tron,corr,x,limit_breaker):
    if local_div_factor!=0 :
        if del_to_deal>0.4 and to_deal<-tempo and taken_trade==0 and limit_breaker>-0.25:
            exclusive_strike=int(np.round(x/50)*50)
            c_data=option_chain[option_chain['CPType']=='CE']
            c_scrip=int(c_data[c_data['StrikeRate']==exclusive_strike]['ScripCode'])
            test_order = Order(order_type='B',exchange='N',exchange_segment='D', scrip_code =c_scrip, quantity=50*lots_tuner, price=0 ,is_intraday=False,remote_order_id="tag")
            prime_client['login'].place_order(test_order) 
            tempo=tempo+10
            taken_trade=1
        if del_to_deal<-0.4 and to_deal>tempo and taken_trade==0 and limit_breaker<0.25 :
            exclusive_strike=int(np.round(x/50)*50)
            p_data=option_chain[option_chain['CPType']=='PE']
            p_scrip=int(p_data[p_data['StrikeRate']==exclusive_strike]['ScripCode'])
            test_order = Order(order_type='B',exchange='N',exchange_segment='D', scrip_code =p_scrip, quantity=50*lots_tuner, price=0 ,is_intraday=False,remote_order_id="tag")
            prime_client['login'].place_order(test_order) 
            tempo=tempo+10
            taken_trade=-1
        if del_to_deal<0 and to_deal>0 and taken_trade==1 :
            c_data=option_chain[option_chain['CPType']=='CE']
            c_scrip=int(c_data[c_data['StrikeRate']==exclusive_strike]['ScripCode'])
            test_order = Order(order_type='S',exchange='N',exchange_segment='D', scrip_code =c_scrip, quantity=50*(lots_tuner), price=0 ,is_intraday=False,remote_order_id="tag")
            prime_client['login'].place_order(test_order)
            tempo=20
            lots_tuner=tron
            taken_trade=0
        if del_to_deal>0 and to_deal<0 and taken_trade==-1:
            p_data=option_chain[option_chain['CPType']=='PE']
            p_scrip=int(p_data[p_data['StrikeRate']==exclusive_strike]['ScripCode'])
            test_order = Order(order_type='S',exchange='N',exchange_segment='D', scrip_code =p_scrip, quantity=50*(lots_tuner), price=0 ,is_intraday=False,remote_order_id="tag")
            prime_client['login'].place_order(test_order)
            taken_trade=0
            lots_tuner=tron
            tempo=20
        if del_to_deal>0 and to_deal<-tempo and taken_trade==1 and lots_tuner<=28 and limit_breaker>-0.25:
            c_data=option_chain[option_chain['CPType']=='CE']
            c_scrip=int(c_data[c_data['StrikeRate']==exclusive_strike]['ScripCode'])
            test_order = Order(order_type='B',exchange='N',exchange_segment='D', scrip_code =c_scrip, quantity=50*lots_tuner, price=0 ,is_intraday=False,remote_order_id="tag")
            prime_client['login'].place_order(test_order) 
            tempo=tempo+10
            lots_tuner=lots_tuner*2
        if del_to_deal<0 and to_deal>tempo and taken_trade==-1 and lots_tuner<=28 and limit_breaker<0.25:
            p_data=option_chain[option_chain['CPType']=='PE']
            p_scrip=int(p_data[p_data['StrikeRate']==exclusive_strike]['ScripCode'])
            test_order = Order(order_type='B',exchange='N',exchange_segment='D', scrip_code =p_scrip, quantity=25*lots_tuner, price=0 ,is_intraday=False,remote_order_id="tag")
            prime_client['login'].place_order(test_order) 
            tempo=tempo+10
            lots_tuner=lots_tuner*2
    return taken_trade,exclusive_strike,tempo,lots_tuner
#%%
ind_time = datetime.now(timezone("Asia/Kolkata")).strftime('%Y-%m-%d %H:%M:%S.%f')
while int(ind_time[11:13])*60+int(ind_time[14:16])<555 or int(ind_time[11:13])*60+int(ind_time[14:16])>885 :
    ind_time = datetime.now(timezone("Asia/Kolkata")).strftime('%Y-%m-%d %H:%M:%S.%f')
#%%
prime_client=client_login(client=client_name)
expiry_timestamps=prime_client['login'].get_expiry("N","NIFTY").copy()
current_expiry_time_stamp_weekly=int(expiry_timestamps['Expiry'][0]['ExpiryDate'][6:19])
option_chain=pd.DataFrame(prime_client['login'].get_option_chain("N","NIFTY",current_expiry_time_stamp_weekly)['Options'])
proj,c_striker,p_striker=rosetta_strikes(option_chain)
c_data=option_chain[option_chain['CPType']=='CE']
p_data=option_chain[option_chain['CPType']=='PE']
c_scrip=int(c_data[c_data['StrikeRate']==c_striker]['ScripCode'])
p_scrip=int(p_data[p_data['StrikeRate']==p_striker]['ScripCode'])
indicator=[]
b_lastrate=[]
diverge=[]
l_diverge=[]
inst_diverge=[]
to_deal=[]
corr=[]
corr_window=10
exclusive_strike=0
taken_trade=0
oi_chain=0
tempo=20
nifty_bank=[]
lots_tuner=tron
if datetime.today().weekday()==3:
    time=916
else:
    time=928

while True:
    while True:
        try :
            expiry_timestamps=prime_client['login'].get_expiry("N","NIFTY").copy()
            current_expiry_time_stamp_weekly=int(expiry_timestamps['Expiry'][oi_chain]['ExpiryDate'][6:19])
            option_chain=pd.DataFrame(prime_client['login'].get_option_chain("N","NIFTY",current_expiry_time_stamp_weekly)['Options'])
            x=expiry_timestamps['lastrate'][0]['LTP']
            break
        except Exception :
            pass
    proj,Cyi,Phf=rosetta_strikes(option_chain)
    project_k=(x-proj)
    print('Nifty:  ',project_k)
    ind_time = datetime.now(timezone("Asia/Kolkata")).strftime('%Y-%m-%d %H:%M:%S.%f')
    c_data=option_chain[option_chain['CPType']=='CE']
    p_data=option_chain[option_chain['CPType']=='PE']
    c1=int(c_data[c_data['StrikeRate']==int(np.floor(x/50)*50)]['LastRate'])
    c2=int(c_data[c_data['StrikeRate']==int(np.ceil(x/50)*50)]['LastRate'])
    p1=int(p_data[p_data['StrikeRate']==int(np.floor(x/50)*50)]['LastRate'])
    p2=int(p_data[p_data['StrikeRate']==int(np.ceil(x/50)*50)]['LastRate'])
    dynamic_crossover=(c1+c2+p1+p2)/4
    indicator,b_lastrate,div_factor,local_div_factor,instant_div_factor=past_picture(indicator,project_k,b_lastrate,x)
    diverge=diverge+[div_factor]
    to_deal=to_deal+[instant_div_factor-local_div_factor]
    print('sample no.:',len(to_deal))
    print('base_indicator :',to_deal[-1])
    if len(to_deal)>corr_window+1:
        corr=corr+[pearsonr(to_deal[-corr_window:],b_lastrate[-corr_window:])[0]]
    if len(to_deal)>corr_window+1:
        del_to_deal=to_deal[-1]-to_deal[-2]
        print('new_indicator',del_to_deal)
        print('')
    if tron>0 and len(to_deal)>corr_window+1 and oi_chain==0:
        if to_deal[-1]>30 or to_deal[-1]<-30 :
            s.play()
        limit_breaker=project_k/dynamic_crossover
        taken_trade,exclusive_strike,tempo,lots_tuner=decoy4(option_chain,exclusive_strike,taken_trade,to_deal[-1],del_to_deal,tempo,lots_tuner,tron,corr,x,limit_breaker)
    if int(ind_time[11:13])*60+int(ind_time[14:16])>time :
        packup(option_chain,prime_client,taken_trade,exclusive_strike,lots_tuner)
        json_data = {'lastrate': list(b_lastrate[corr_window+1:]), 'k':list(to_deal[corr_window+1:]),'corr':list(np.array(corr)*10),'nifty':list(np.array(indicator[corr_window+1:]))}
        with open('nifty_'+str(datetime.today().weekday())+'.json', 'w') as  json_file:
            json.dump(json_data, json_file)
        if datetime.today().weekday()==3:
            oi_chain=1
        else:
            break
    json_data = {'lastrate': list(b_lastrate[corr_window+1:][-240:]), 'k':list(to_deal[corr_window+1:][-240:]),'corr':list(np.array(corr[-240:])*10),'nifty':list(np.array(indicator[-240:]))}
    with open('nifty.json', 'w') as  json_file:
        json.dump(json_data, json_file)
fig, ax_left = plt.subplots()
ax_right = ax_left.twinx()
ax_left.plot(b_lastrate, color='blue')
ax_right.plot(to_deal, color='red')

