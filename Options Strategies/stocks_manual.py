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
    client_list[client]['lots']=0
    return client_list[client]
#%%
def loopin(company):
    while True:
        try :
            expiry_timestamps=prime_client['login'].get_expiry("N",company).copy()
            current_expiry_time_stamp_weekly=int(expiry_timestamps['Expiry'][0]['ExpiryDate'][6:19])
            option_chain=pd.DataFrame(prime_client['login'].get_option_chain("N",company,current_expiry_time_stamp_weekly)['Options'])
            x=expiry_timestamps['lastrate'][0]['LTP']
            break
        except Exception :
            pass
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
    a=np.array(option_chain['StrikeRate'])[0]+index*increment
    arr=np.array(option_chain['StrikeRate'])
    t1=np.argmin(np.abs(arr-x))
    at_strike=arr[t1]
    project_k=(2*(x-a))/np.sum(option_chain[option_chain['StrikeRate']==at_strike]['LastRate'])
    return  project_k



client_name   = 'vinathi'
prime_client=client_login(client=client_name)
stocks_to_go=['SBIN',
'HDFCBANK',
'RELIANCE',
'ADANIPORTS',
'ICICIBANK',
'INFY',
'BHARTIARTL',
'AXISBANK',
'TATAMOTORS',
'ADANIENT',
'M&M',
'HDFC',
'LT',
'NMDC',
'HAL',
'PEL',
'BAJFINANCE',
'TCS',
'BAJAJFINSV',
'TATASTEEL']
company=stocks_to_go[-1]

#%%
ind_time = datetime.now(timezone("Asia/Kolkata")).strftime('%Y-%m-%d %H:%M:%S.%f')
while int(ind_time[11:13])*60+int(ind_time[14:16])<555 or int(ind_time[11:13])*60+int(ind_time[14:16])>885 :
    ind_time = datetime.now(timezone("Asia/Kolkata")).strftime('%Y-%m-%d %H:%M:%S.%f')
#%%
while True:
    stocks_manual_json={}
    for company in stocks_to_go:
        stocks_manual_json[company]=loopin(company)
    with open('stocks_manual.json', 'w') as  json_file:
        json.dump(stocks_manual_json, json_file)
        break
# %%
