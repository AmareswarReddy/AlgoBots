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
stocks_to_go=['HDFC','ONGC','INFY','HDFCBANK','RELIANCE','TATAPOWER','IRCTC','AXISBANK']
raw_df=pd.read_csv('scripmaster-csv-format-4.csv')
df=raw_df[raw_df['Exch']=='N']
company=stocks_to_go[-1]
def details(company):
    eq_scrip=str(int(df[df['Name']==company]['Scripcode']))
    return eq_scrip
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
    arr=np.array(option_chain['StrikeRate'])
    t1=np.argmin(np.abs(arr-b))
    lower_strike=arr[t1]
    t2=np.argmin(np.abs(arr-c))
    upper_strike=arr[t2]
    return  a,lower_strike,upper_strike

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


#%%
ind_time = datetime.now(timezone("Asia/Kolkata")).strftime('%Y-%m-%d %H:%M:%S.%f')
while int(ind_time[11:13])*60+int(ind_time[14:16])<555 or int(ind_time[11:13])*60+int(ind_time[14:16])>885 :
    ind_time = datetime.now(timezone("Asia/Kolkata")).strftime('%Y-%m-%d %H:%M:%S.%f')
#%%
prime_client=client_login(client=client_name)
#%%
expiry_timestamps=prime_client['login'].get_expiry("N",company).copy()
current_expiry_time_stamp_weekly=int(expiry_timestamps['Expiry'][0]['ExpiryDate'][6:19])
option_chain=pd.DataFrame(prime_client['login'].get_option_chain("N",company,current_expiry_time_stamp_weekly)['Options'])
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
if datetime.today().weekday()==3:
    time=916
else:
    time=928
company_scrip=details(company)
arr=np.array(option_chain['StrikeRate'])
expiry_timestamps=prime_client['login'].get_expiry("N",company).copy()
current_expiry_time_stamp_weekly=int(expiry_timestamps['Expiry'][oi_chain]['ExpiryDate'][6:19])
while True:
    while True:
        try :
            option_chain=pd.DataFrame(prime_client['login'].get_option_chain("N",company,current_expiry_time_stamp_weekly)['Options'])
            x=expiry_timestamps['lastrate'][0]['LTP']
            break
        except Exception :
            pass
    proj,Cyi,Phf=rosetta_strikes(option_chain)
    project_k=(x-proj)
    print(company+': ',project_k)
    ind_time = datetime.now(timezone("Asia/Kolkata")).strftime('%Y-%m-%d %H:%M:%S.%f')
    c_data=option_chain[option_chain['CPType']=='CE']
    p_data=option_chain[option_chain['CPType']=='PE']
    at_strikerate=int(np.argmin(np.abs(arr-x)))
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
    if len(to_deal)>corr_window+1 and oi_chain==0:
        if to_deal[-1]>30 or to_deal[-1]<-30 :
            s.play()
    if int(ind_time[11:13])*60+int(ind_time[14:16])>time :
        json_data = {'lastrate': list(b_lastrate[corr_window+1:]), 'k':list(to_deal[corr_window+1:]),'corr':list(np.array(corr)*10),company:list(np.array(indicator[corr_window+1:]))}
        with open(company+'_'+str(datetime.today().weekday())+'.json', 'w') as  json_file:
            json.dump(json_data, json_file)
        break
    json_data = {'lastrate': list(b_lastrate[corr_window+1:][-240:]), 'k':list(to_deal[corr_window+1:][-240:]),'corr':list(np.array(corr[-240:])*10),company:list(np.array(indicator[-240:]))}
    with open(company+'.json', 'w') as  json_file:
        json.dump(json_data, json_file)
fig, ax_left = plt.subplots()
ax_right = ax_left.twinx()
ax_left.plot(b_lastrate, color='blue')
ax_right.plot(to_deal, color='red')


# %%
