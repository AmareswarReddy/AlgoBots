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
client_name   = 'vinathi'
prime_client=client_login(client=client_name)
def order_button(exclusive_strike,type,lots):
    if exclusive_strike==0:
        while True:
            try :
                expiry_timestamps=prime_client['login'].get_expiry("N","BANKNIFTY").copy()
                current_expiry_time_stamp_weekly=int(expiry_timestamps['Expiry'][0]['ExpiryDate'][6:19])
                option_chain=pd.DataFrame(prime_client['login'].get_option_chain("N","BANKNIFTY",current_expiry_time_stamp_weekly)['Options'])
                x=expiry_timestamps['lastrate'][0]['LTP']
                break
            except Exception :
                pass
        exclusive_strike=int(np.round(x/100)*100)
    else:
        while True:
            try :
                expiry_timestamps=prime_client['login'].get_expiry("N","BANKNIFTY").copy()
                current_expiry_time_stamp_weekly=int(expiry_timestamps['Expiry'][0]['ExpiryDate'][6:19])
                option_chain=pd.DataFrame(prime_client['login'].get_option_chain("N","BANKNIFTY",current_expiry_time_stamp_weekly)['Options'])
                x=expiry_timestamps['lastrate'][0]['LTP']
                break
            except Exception :
                pass
    if type=='CE_B':
        c_data=option_chain[option_chain['CPType']=='CE']
        c_scrip=int(c_data[c_data['StrikeRate']==exclusive_strike]['ScripCode'])
        temp2=lots
        temp=int(temp2/48)
        end=temp2-temp*48
        test_order = Order(order_type='B',exchange='N',exchange_segment='D', scrip_code =c_scrip, quantity=25*48, price=0 ,is_intraday=False,remote_order_id="tag")
        while temp>0:
            prime_client['login'].place_order(test_order) 
            temp=temp-1
            sleep(0.5)
        if temp==0 and end!=0:
            test_order = Order(order_type='B',exchange='N',exchange_segment='D', scrip_code =c_scrip, quantity=25*end, price=0 ,is_intraday=False,remote_order_id="tag")
            prime_client['login'].place_order(test_order) 
    if type=='PE_B':
        p_data=option_chain[option_chain['CPType']=='PE']
        p_scrip=int(p_data[p_data['StrikeRate']==exclusive_strike]['ScripCode'])
        temp2=lots
        temp=int(temp2/48)
        end=temp2-temp*48
        test_order = Order(order_type='B',exchange='N',exchange_segment='D', scrip_code =p_scrip, quantity=25*48, price=0 ,is_intraday=False,remote_order_id="tag")
        while temp>0:
            prime_client['login'].place_order(test_order) 
            temp=temp-1
            sleep(0.5)
        if temp==0 and end!=0:
            test_order = Order(order_type='B',exchange='N',exchange_segment='D', scrip_code =p_scrip, quantity=25*end, price=0 ,is_intraday=False,remote_order_id="tag")
            prime_client['login'].place_order(test_order) 
    if type=='CE_S':
        c_data=option_chain[option_chain['CPType']=='CE']
        c_scrip=int(c_data[c_data['StrikeRate']==exclusive_strike]['ScripCode'])
        temp2=lots
        temp=int(temp2/48)
        end=temp2-temp*48
        test_order = Order(order_type='S',exchange='N',exchange_segment='D', scrip_code =c_scrip, quantity=25*48, price=0 ,is_intraday=False,remote_order_id="tag")
        while temp>0:
            prime_client['login'].place_order(test_order) 
            temp=temp-1
            sleep(0.5)
        if temp==0 and end!=0:
            test_order = Order(order_type='S',exchange='N',exchange_segment='D', scrip_code =c_scrip, quantity=25*end, price=0 ,is_intraday=False,remote_order_id="tag")
            prime_client['login'].place_order(test_order) 
                

    if type=='PE_S':
        p_data=option_chain[option_chain['CPType']=='PE']
        p_scrip=int(p_data[p_data['StrikeRate']==exclusive_strike]['ScripCode'])
        temp2=lots
        temp=int(temp2/48)
        end=temp2-temp*48
        test_order = Order(order_type='S',exchange='N',exchange_segment='D', scrip_code =p_scrip, quantity=25*48, price=0 ,is_intraday=False,remote_order_id="tag")
        while temp>0:
            prime_client['login'].place_order(test_order) 
            temp=temp-1
            sleep(0.5)
        if temp==0 and end!=0:
            test_order = Order(order_type='S',exchange='N',exchange_segment='D', scrip_code =p_scrip, quantity=25*end, price=0 ,is_intraday=False,remote_order_id="tag")
            prime_client['login'].place_order(test_order) 
    return exclusive_strike
# %%
