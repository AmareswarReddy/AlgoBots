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
def order_button(exclusive_strike,type,lots):
    if exclusive_strike==0:
        while True:
            try :
                expiry_timestamps=prime_client['login'].get_expiry("N","NIFTY").copy()
                current_expiry_time_stamp_weekly=int(expiry_timestamps['Expiry'][0]['ExpiryDate'][6:19])
                option_chain=pd.DataFrame(prime_client['login'].get_option_chain("N","NIFTY",current_expiry_time_stamp_weekly)['Options'])
                x=expiry_timestamps['lastrate'][0]['LTP']
                break
            except Exception :
                pass
        exclusive_strike=int(np.round(x/50)*50)
    else:
        while True:
            try :
                expiry_timestamps=prime_client['login'].get_expiry("N","NIFTY").copy()
                current_expiry_time_stamp_weekly=int(expiry_timestamps['Expiry'][0]['ExpiryDate'][6:19])
                option_chain=pd.DataFrame(prime_client['login'].get_option_chain("N","NIFTY",current_expiry_time_stamp_weekly)['Options'])
                x=expiry_timestamps['lastrate'][0]['LTP']
                break
            except Exception :
                pass
    if type=='CE_B':
        c_data=option_chain[option_chain['CPType']=='CE']
        c_scrip=int(c_data[c_data['StrikeRate']==exclusive_strike]['ScripCode'])
        temp2=lots
        temp=int(temp2/56)
        end=temp2-temp*56
        test_order = Order(order_type='B',exchange='N',exchange_segment='D', scrip_code =c_scrip, quantity=50*56, price=0 ,is_intraday=False,remote_order_id="tag")
        while temp>0:
            prime_client['login'].place_order(test_order) 
            temp=temp-1
            sleep(0.5)
        if temp==0 and end!=0:
            test_order = Order(order_type='B',exchange='N',exchange_segment='D', scrip_code =c_scrip, quantity=50*end, price=0 ,is_intraday=False,remote_order_id="tag")
            prime_client['login'].place_order(test_order) 
    if type=='PE_B':
        p_data=option_chain[option_chain['CPType']=='PE']
        p_scrip=int(p_data[p_data['StrikeRate']==exclusive_strike]['ScripCode'])
        temp2=lots
        temp=int(temp2/56)
        end=temp2-temp*56
        test_order = Order(order_type='B',exchange='N',exchange_segment='D', scrip_code =p_scrip, quantity=50*56, price=0 ,is_intraday=False,remote_order_id="tag")
        while temp>0:
            prime_client['login'].place_order(test_order) 
            temp=temp-1
            sleep(0.5)
        if temp==0 and end!=0:
            test_order = Order(order_type='B',exchange='N',exchange_segment='D', scrip_code =p_scrip, quantity=50*end, price=0 ,is_intraday=False,remote_order_id="tag")
            prime_client['login'].place_order(test_order) 
    if type=='CE_S':
        c_data=option_chain[option_chain['CPType']=='CE']
        c_scrip=int(c_data[c_data['StrikeRate']==exclusive_strike]['ScripCode'])
        temp2=lots
        temp=int(temp2/56)
        end=temp2-temp*56
        test_order = Order(order_type='S',exchange='N',exchange_segment='D', scrip_code =c_scrip, quantity=50*56, price=0 ,is_intraday=False,remote_order_id="tag")
        while temp>0:
            prime_client['login'].place_order(test_order) 
            temp=temp-1
            sleep(0.5)
        if temp==0 and end!=0:
            test_order = Order(order_type='S',exchange='N',exchange_segment='D', scrip_code =c_scrip, quantity=50*end, price=0 ,is_intraday=False,remote_order_id="tag")
            prime_client['login'].place_order(test_order) 
                

    if type=='PE_S':
        p_data=option_chain[option_chain['CPType']=='PE']
        p_scrip=int(p_data[p_data['StrikeRate']==exclusive_strike]['ScripCode'])
        temp2=lots
        temp=int(temp2/56)
        end=temp2-temp*56
        test_order = Order(order_type='S',exchange='N',exchange_segment='D', scrip_code =p_scrip, quantity=50*56, price=0 ,is_intraday=False,remote_order_id="tag")
        while temp>0:
            prime_client['login'].place_order(test_order) 
            temp=temp-1
            sleep(0.5)
        if temp==0 and end!=0:
            test_order = Order(order_type='S',exchange='N',exchange_segment='D', scrip_code =p_scrip, quantity=50*end, price=0 ,is_intraday=False,remote_order_id="tag")
            prime_client['login'].place_order(test_order) 
    return exclusive_strike

def buyer_adjustment_signal(c_strike,p_strike,exclusive_strike):
    ind_time = datetime.now(timezone("Asia/Kolkata")).strftime('%Y-%m-%d %H:%M:%S.%f')
    timer=int(ind_time[11:13])*60+int(ind_time[14:16])
    c_lastrate=float(option_chain[(option_chain['StrikeRate']==c_strike) & (option_chain['CPType']=='CE')]['LastRate'])
    p_lastrate=float(option_chain[(option_chain['StrikeRate']==p_strike) & (option_chain['CPType']=='PE')]['LastRate'])
    lastrate_sum=np.sum(option_chain[option_chain['StrikeRate']==exclusive_strike]['LastRate'])
    if (c_strike-p_strike>np.floor(2*lastrate_sum/50)*50) or timer>925 or c_lastrate/p_lastrate>3 or p_lastrate/c_lastrate>3:
        return 1,np.floor(lastrate_sum/50)*50
    else:
        return 0,0 #(change_of_buyside_strikes?, This_far_to_take_new_buy_side_positions, timer_trigger)

def buyer_adjustments(exclusive_strike,k,c_strike,p_strike,buy_tron):
    #k=(change_of_buyside_strikes, This_far_to_take_new_buy_side_positions, timer_trigger)
    if k[0]==1:
        c_strike_new=exclusive_strike+k[1]
        p_strike_new=exclusive_strike-k[1]
        if c_strike_new!=c_strike:
            #enter new buyside positions
            order_button(c_strike_new,'CE_B',buy_tron)
            #exit old buyside positions
            order_button(c_strike,'CE_S',buy_tron)
        if p_strike_new!=p_strike:
            #enter new buyside positions
            order_button(p_strike_new,'PE_B',buy_tron)
            #exit old buyside positions
            order_button(p_strike,'PE_S',buy_tron)
        c_strike=c_strike_new
        p_strike=p_strike_new
    return c_strike,p_strike

def initial_trades(option_chain,x):
    exclusive_strike=int(np.round(x/50)*50)
    f=np.sum(option_chain[option_chain['StrikeRate']==int(np.round(x/50)*50)]['LastRate'])
    factor=int(np.floor(f/50)*50)
    c_strike=exclusive_strike+factor
    p_strike=exclusive_strike-factor
    #first buyside
    order_button(p_strike,'PE_B',buy_tron)
    order_button(c_strike,'CE_B',buy_tron)
    #sell side
    order_button(exclusive_strike,'PE_S',tron)
    order_button(exclusive_strike,'CE_S',tron)
    return exclusive_strike,c_strike,p_strike

def good_to_go(prev_x,x):
    k=np.round(x/50)*50
    if (prev_x>k and k>x) or (prev_x<k and k<x):
        return 1
    else:
        return 0

#for single lot
def exclusive_strike_change_signal(earlier_x,x):
    a=(x-earlier_x)/50
    return abs(a)
def exclusive_strike_change_trades(exclusive_strike,x):
    order_button(exclusive_strike,'PE_B',tron)
    order_button(exclusive_strike,'CE_B',tron)
    exclusive_strike=order_button(int(np.round(x/50)*50),'PE_S',tron)
    exclusive_strike=order_button(int(np.round(x/50)*50),'CE_S',tron)
def data():
    while True:
        try :
            expiry_timestamps=prime_client['login'].get_expiry("N","NIFTY").copy()
            option_chain=pd.DataFrame(prime_client['login'].get_option_chain("N","NIFTY",current_expiry_time_stamp_weekly)['Options'])
            x=expiry_timestamps['lastrate'][0]['LTP']
            break
        except Exception :
            pass
    return option_chain,x
def exit_signal(option_chain,exclusive_strike):
    temp=np.sum(option_chain[option_chain['StrikeRate']==exclusive_strike]['LastRate'])
    if temp<75:
        return 1
    else:
        return 0
def exit_trades(c_strike,p_strike,exclusive_strike):        
    order_button(exclusive_strike,'PE_B',tron)
    order_button(exclusive_strike,'CE_B',tron)   
    order_button(c_strike,'CE_S',tron)
    order_button(p_strike,'PE_S',tron)
#%%
#variables to be initialised
client_name = 'rahul'
tron=int(input('enter the number of lots for trading (Eg 3):'))
buy_tron=int(tron*1.3)
prime_client=client_login(client=client_name)
expiry_timestamps=prime_client['login'].get_expiry("N","NIFTY").copy()
current_expiry_time_stamp_weekly=int(expiry_timestamps['Expiry'][0]['ExpiryDate'][6:19])
option_chain=pd.DataFrame(prime_client['login'].get_option_chain("N","NIFTY",current_expiry_time_stamp_weekly)['Options'])
prev_x=expiry_timestamps['lastrate'][0]['LTP']
start=int(input('enter 0 if starting the strategy for the first time. else 1 :  '))
if start==1:
    exclusive_strike=int(input('enter exclusive strike :  '))
    c_strike=int(input('enter call strike buyside :  '))
    p_strike=int(input('enter put strike buyside :  '))
elif start==0:
    option_chain,x=data()
    exclusive_strike,c_strike,p_strike=0,0,0
#%%
ind_time = datetime.now(timezone("Asia/Kolkata")).strftime('%Y-%m-%d %H:%M:%S.%f')
while int(ind_time[11:13])*60+int(ind_time[14:16])<555 or int(ind_time[11:13])*60+int(ind_time[14:16])>885 :
    ind_time = datetime.now(timezone("Asia/Kolkata")).strftime('%Y-%m-%d %H:%M:%S.%f')
#%%
while True:
    option_chain,x=data()
    #x=int(input('--'))
    if start==0:
        if good_to_go(x=x,prev_x=prev_x)>0:
            exclusive_strike,c_strike,p_strike=initial_trades(option_chain=option_chain,x=x)
            start=1
    if start==1:
        k=buyer_adjustment_signal(c_strike,p_strike,exclusive_strike) 
        c_strike,p_strike=buyer_adjustments(exclusive_strike,k,c_strike,p_strike,buy_tron)
        if exclusive_strike_change_signal(earlier_x=exclusive_strike,x=x)>1:
            exclusive_strike_change_trades(exclusive_strike,x)
    if exit_signal(option_chain,exclusive_strike)==1 and exclusive_strike!=0: 
        exit(c_strike=c_strike,p_strike=p_strike,exclusive_strike=exclusive_strike)   
        break   
    prev_x=x