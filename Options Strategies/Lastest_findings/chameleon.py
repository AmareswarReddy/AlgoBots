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
def order_button(exclusive_strike,type,lots,option_chain):
    if type=='CE_B':
        c_data=option_chain[option_chain['CPType']=='CE']
        c_scrip=int(c_data[c_data['StrikeRate']==exclusive_strike]['ScripCode'])
        test_order = Order(order_type='B',exchange='N',exchange_segment='D', scrip_code =c_scrip, quantity=25*lots, price=0 ,is_intraday=False,remote_order_id="tag")
        prime_client['login'].place_order(test_order) 
    if type=='PE_B':
        p_data=option_chain[option_chain['CPType']=='PE']
        p_scrip=int(p_data[p_data['StrikeRate']==exclusive_strike]['ScripCode'])
        test_order = Order(order_type='B',exchange='N',exchange_segment='D', scrip_code =p_scrip, quantity=25*lots, price=0 ,is_intraday=False,remote_order_id="tag")
        prime_client['login'].place_order(test_order) 
    if type=='CE_S':
        c_data=option_chain[option_chain['CPType']=='CE']
        c_scrip=int(c_data[c_data['StrikeRate']==exclusive_strike]['ScripCode'])
        test_order = Order(order_type='S',exchange='N',exchange_segment='D', scrip_code =c_scrip, quantity=25*lots, price=0 ,is_intraday=False,remote_order_id="tag")
        prime_client['login'].place_order(test_order) 
    if type=='PE_S':
        p_data=option_chain[option_chain['CPType']=='PE']
        p_scrip=int(p_data[p_data['StrikeRate']==exclusive_strike]['ScripCode'])
        test_order = Order(order_type='S',exchange='N',exchange_segment='D', scrip_code =p_scrip, quantity=25*lots, price=0 ,is_intraday=False,remote_order_id="tag")
        prime_client['login'].place_order(test_order) 
    return exclusive_strike

def good_to_go(prev_x,x):
    if np.ceil(prev_x/100)-np.ceil(x/100)==1:
        return -1
    elif np.ceil(x/100)-np.ceil(prev_x/100)==1:
        return 1
    else:
        return 0
#for single lot
def change_of_strike(earlier_x,x):
    a=(x-earlier_x)/100
    return a


def side_switch(earlier_x,x,side):
    a=(x-earlier_x)
    if a>0 and side=='CE_S':
        return 'PE_S'
    elif a<0 and side=='PE_S':
        return 'CE_S'
    if a>0 and side=='PE_B':
        return 'CE_B'
    elif a<0 and side=='CE_B':
        return 'PE_B'
    else:
        return side
def daily_buy_sell_switch():
    k=(datetime.today().weekday())%4
    k=k%4
    if k>=1 and k<=2:
        k=1
    return -np.sign(k-1)

def data():
    while True:
        try :
            expiry_timestamps=prime_client['login'].get_expiry("N","BANKNIFTY").copy()
            option_chain=pd.DataFrame(prime_client['login'].get_option_chain("N","BANKNIFTY",current_expiry_time_stamp_weekly)['Options'])
            x=expiry_timestamps['lastrate'][0]['LTP']
            break
        except Exception :
            pass
    return option_chain,x


#%%
#variables to be initialised
client_name = 'bhaskar'
tron=int(input('enter the number of lots for trading (Eg 3):'))
if tron>36:
    tron=36
prime_client=client_login(client=client_name)
expiry_timestamps=prime_client['login'].get_expiry("N","BANKNIFTY").copy()
current_expiry_time_stamp_weekly=int(expiry_timestamps['Expiry'][0]['ExpiryDate'][6:19])
option_chain=pd.DataFrame(prime_client['login'].get_option_chain("N","BANKNIFTY",current_expiry_time_stamp_weekly)['Options'])
prev_x=expiry_timestamps['lastrate'][0]['LTP']
start=0
ind_time = datetime.now(timezone("Asia/Kolkata")).strftime('%Y-%m-%d %H:%M:%S.%f')
#while int(ind_time[11:13])*60+int(ind_time[14:16])<555 or int(ind_time[11:13])*60+int(ind_time[14:16])>885 :
#    ind_time = datetime.now(timezone("Asia/Kolkata")).strftime('%Y-%m-%d %H:%M:%S.%f')

# %%
while True:
    option_chain,x=data()
    #x=int(input('-----'))
    if start==0:
        if good_to_go(x=x,prev_x=prev_x)>0:
            exclusive_strike=order_button(int(np.round(x/100)*100),'CE_B',tron,option_chain)
            u=(prev_x+x)/2
            earlier_x=int(np.round(u/100)*100)
            start=1
            side='CE_B'
        if good_to_go(x=x,prev_x=prev_x)<0:
            exclusive_strike=order_button(int(np.round(x/100)*100),'PE_B',tron,option_chain)
            u=(prev_x+x)/2
            earlier_x=int(np.round(u/100)*100)
            start=1
            side='PE_B'
    if start==1:
        if change_of_strike(earlier_x=earlier_x,x=x)>1:
            order_button(exclusive_strike,'CE_S',tron,option_chain)
            exclusive_strike=order_button(int(np.round(x/100)*100),'CE_B',tron,option_chain)
            u=(prev_x+x)/2
            earlier_x=int(np.round(u/100)*100)
            side='CE_B'
        if change_of_strike(earlier_x=earlier_x,x=x)<-1:
            order_button(exclusive_strike,'PE_S',tron,option_chain)
            exclusive_strike=order_button(int(np.round(x/100)*100),'PE_B',tron,option_chain)
            u=(prev_x+x)/2
            earlier_x=int(np.round(u/100)*100)
            side='PE_B'
        side_=side_switch(earlier_x=earlier_x,x=x,side=side)
        if side_!=side:
            if side=='PE_B':
                order_button(exclusive_strike,'PE_S',tron,option_chain)
                exclusive_strike=order_button(int(np.round(x/100)*100),side_,tron,option_chain)
            if side=='CE_B':
                order_button(exclusive_strike,'CE_S',tron,option_chain)
                exclusive_strike=order_button(int(np.round(x/100)*100),side_,tron,option_chain)
            u=(prev_x+x)/2
            earlier_x=int(np.round(u/100)*100)
            side=side_
    prev_x=x

# %%
