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
        already_placed=0
        c_data=option_chain[option_chain['CPType']=='CE']
        c_scrip=int(c_data[c_data['StrikeRate']==exclusive_strike]['ScripCode'])
        temp2=lots
        temp=int(temp2/56)
        end=temp2-temp*56
        test_order = Order(order_type='B',exchange='N',exchange_segment='D', scrip_code =c_scrip, quantity=50*56, price=0 ,is_intraday=False,remote_order_id="tag")
        while temp>0:
            status=prime_client['login'].place_order(test_order)
            temp=temp-1 
            if status['Message']=='Success':
                already_placed+=56
            sleep(0.5)
        if temp==0 and end!=0:
            test_order = Order(order_type='B',exchange='N',exchange_segment='D', scrip_code =c_scrip, quantity=50*end, price=0 ,is_intraday=False,remote_order_id="tag")
            status=prime_client['login'].place_order(test_order)
            if status['Message']=='Success':
                already_placed+=end
        yet_to_place=lots-already_placed 
    if type=='PE_B':
        already_placed=0
        p_data=option_chain[option_chain['CPType']=='PE']
        p_scrip=int(p_data[p_data['StrikeRate']==exclusive_strike]['ScripCode'])
        temp2=lots
        temp=int(temp2/56)
        end=temp2-temp*56
        test_order = Order(order_type='B',exchange='N',exchange_segment='D', scrip_code =p_scrip, quantity=50*56, price=0 ,is_intraday=False,remote_order_id="tag")
        while temp>0:
            status=prime_client['login'].place_order(test_order) 
            temp=temp-1
            if status['Message']=='Success':
                already_placed+=56
            sleep(0.5)
        if temp==0 and end!=0:
            test_order = Order(order_type='B',exchange='N',exchange_segment='D', scrip_code =p_scrip, quantity=50*end, price=0 ,is_intraday=False,remote_order_id="tag")
            status=prime_client['login'].place_order(test_order) 
            if status['Message']=='Success':
                already_placed+=end
        yet_to_place=lots-already_placed
    if type=='CE_S':
        already_placed=0
        c_data=option_chain[option_chain['CPType']=='CE']
        c_scrip=int(c_data[c_data['StrikeRate']==exclusive_strike]['ScripCode'])
        temp2=lots
        temp=int(temp2/56)
        end=temp2-temp*56
        test_order = Order(order_type='S',exchange='N',exchange_segment='D', scrip_code =c_scrip, quantity=50*56, price=0 ,is_intraday=False,remote_order_id="tag")
        while temp>0:
            status=prime_client['login'].place_order(test_order) 
            temp=temp-1
            if status['Message']=='Success':
                already_placed+=56
            sleep(0.5)
        if temp==0 and end!=0:
            test_order = Order(order_type='S',exchange='N',exchange_segment='D', scrip_code =c_scrip, quantity=50*end, price=0 ,is_intraday=False,remote_order_id="tag")
            status=prime_client['login'].place_order(test_order) 
            if status['Message']=='Success':
                already_placed+=end
        yet_to_place=lots-already_placed
    if type=='PE_S':
        already_placed=0
        p_data=option_chain[option_chain['CPType']=='PE']
        p_scrip=int(p_data[p_data['StrikeRate']==exclusive_strike]['ScripCode'])
        temp2=lots
        temp=int(temp2/56)
        end=temp2-temp*56
        test_order = Order(order_type='S',exchange='N',exchange_segment='D', scrip_code =p_scrip, quantity=50*56, price=0 ,is_intraday=False,remote_order_id="tag")
        while temp>0:
            status=prime_client['login'].place_order(test_order) 
            temp=temp-1
            if status['Message']=='Success':
                already_placed+=56
            sleep(0.5)
        if temp==0 and end!=0:
            test_order = Order(order_type='S',exchange='N',exchange_segment='D', scrip_code =p_scrip, quantity=50*end, price=0 ,is_intraday=False,remote_order_id="tag")
            status=prime_client['login'].place_order(test_order) 
            if status['Message']=='Success':
                already_placed+=end
        yet_to_place=lots-already_placed
    return exclusive_strike,yet_to_place
def good_to_go(prev_x,x):
    a=np.floor(prev_x/50)
    b=np.floor(x/50)
    if a>b:
        return -1
    elif a<b:
        return 1
    else:
        return 0
#for single lot
def change_of_strike(earlier_x,x):
    a=(x-earlier_x)/50
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
            expiry_timestamps=prime_client['login'].get_expiry("N","NIFTY").copy()
            option_chain=pd.DataFrame(prime_client['login'].get_option_chain("N","NIFTY",current_expiry_time_stamp_weekly)['Options'])
            x=expiry_timestamps['lastrate'][0]['LTP']
            break
        except Exception :
            pass
    return option_chain,x

def troner(tron,step):
    tron2=np.floor(tron/step)
    rest=tron-tron2*step
    return tron2,rest
def lots_drop(strike,side,yet_to_place):
    k=yet_to_place
    while yet_to_place>0:
        yet_to_place-=1
        xx,pending=order_button(strike,side,yet_to_place)
        if pending==0:
            break
    return k-yet_to_place
        

#%%
#variables to be initialised
client_name = 'rahul'
tron=int(input('enter the number of lots for trading (Eg 3):'))
prime_client=client_login(client=client_name)
expiry_timestamps=prime_client['login'].get_expiry("N","NIFTY").copy()
current_expiry_time_stamp_weekly=int(expiry_timestamps['Expiry'][0]['ExpiryDate'][6:19])
option_chain=pd.DataFrame(prime_client['login'].get_option_chain("N","NIFTY",current_expiry_time_stamp_weekly)['Options'])
prev_x=expiry_timestamps['lastrate'][0]['LTP']
start=0
#%%
#m=int(input('enter the lastrate at which you would like to enter trades Eg: 35,55,60,40'))
ind_time = datetime.now(timezone("Asia/Kolkata")).strftime('%Y-%m-%d %H:%M:%S.%f')
while int(ind_time[11:13])*60+int(ind_time[14:16])<=555 or int(ind_time[11:13])*60+int(ind_time[14:16])>885 :
    ind_time = datetime.now(timezone("Asia/Kolkata")).strftime('%Y-%m-%d %H:%M:%S.%f')
#%%
daily_switch=daily_buy_sell_switch()
if daily_switch<=0:
    while True:
        option_chain,x=data()
        #x=int(input('-----'))
        if start==0:
            if good_to_go(x=x,prev_x=prev_x)>0:
                exclusive_strike,yet_to_place=order_button(int(np.round(x/50)*50),'PE_S',tron)
                tron=tron-lots_drop(int(np.round(x/50)*50),'PE_S',yet_to_place)
                start=1
                side='PE_S'
            if good_to_go(x=x,prev_x=prev_x)<0:
                exclusive_strike,yet_to_place=order_button(int(np.round(x/50)*50),'CE_S',tron)
                tron=tron-lots_drop(int(np.round(x/50)*50),'CE_S',yet_to_place)
                start=1
                side='CE_S'
        if start==1:
            if change_of_strike(earlier_x=exclusive_strike,x=x)>1:
                order_button(exclusive_strike,'PE_B',tron)
                tron=tron+1
                exclusive_strike,yet_to_place=order_button(int(np.round(x/50)*50),'PE_S')
                tron=tron-lots_drop(int(np.round(x/50)*50),'PE_S',yet_to_place)
                side='PE_S'
            if change_of_strike(earlier_x=exclusive_strike,x=x)<-1:
                order_button(exclusive_strike,'CE_B',tron)
                tron=tron+1
                exclusive_strike,yet_to_place=order_button(int(np.round(x/50)*50),'CE_S',tron)
                tron=tron-lots_drop(int(np.round(x/50)*50),'CE_S',yet_to_place)
                side='CE_S'
            side_=side_switch(earlier_x=exclusive_strike,x=x,side=side)
            if side_!=side:
                if side=='CE_S':
                    order_button(exclusive_strike,'CE_B',tron)
                    exclusive_strike,yet_to_place=order_button(int(np.round(x/50)*50),side_,tron)
                    tron=tron-lots_drop(int(np.round(x/50)*50),side_,yet_to_place)
                if side=='PE_S':
                    order_button(exclusive_strike,'PE_B',tron)
                    exclusive_strike,yet_to_place=order_button(int(np.round(x/50)*50),side_,tron)
                    tron=tron-lots_drop(int(np.round(x/50)*50),side_,yet_to_place)
                side=side_
        prev_x=x
# %%
