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

def strike_list(a,b):
    a=np.linspace(int(np.floor(a/100)*100),int(np.ceil(b/100)*100),int((int(np.ceil(b/100)*100)-int(np.floor(a/100)*100))/100)+1)
    if len(a)==1:
        a=a+a[0]
    return a


def weighted_max_move2(option_chain,memory,x,put_side1,put_side2,call_side1,call_side2):
    #option_chain=option_chain[(option_chain['StrikeRate']>option_chain['lastrate'].iloc[0]-2000) & (option_chain['StrikeRate']<option_chain['lastrate'].iloc[0]+2000)].copy()
    p_data=option_chain[option_chain['CPType']=='PE']
    c_data=option_chain[option_chain['CPType']=='CE']
    pe_data=p_data[(p_data['LastRate']>0)].copy()
    ce_data=c_data[c_data['LastRate']>0].copy()
    sp=pe_data['StrikeRate']
    sc=ce_data['StrikeRate']
    k=np.intersect1d(np.array(sp),np.array(sc))
    w=[]
    for strike in sp:
        if strike in k:
            w=w+[True]
        else:
            w=w+[False]
    v=[]
    for strike in sc:
        if strike in k:
            v=v+[True]
        else:
            v=v+[False]
    v=np.array(v)
    pe_data=pe_data[w].copy()
    ce_data=ce_data[v].copy()
    try:
        memory_pe_data=memory[memory['CPType']=='PE']
        memory_ce_data=memory[memory['CPType']=='CE']
        memory_pe_data=memory_pe_data[p_data['LastRate']>0].copy()
        memory_ce_data=memory_ce_data[c_data['LastRate']>0].copy()
        memory_pe_data=memory_pe_data[w].copy()
        memory_ce_data=memory_ce_data[v].copy()
        mp_open=np.array(list(memory_pe_data['OpenInterest']))
        mc_open=np.array(list(memory_ce_data['OpenInterest']))
        lastrate=x
        p_strikeprices=np.array(list(pe_data['StrikeRate']))
        c_strikeprices=np.array(list(ce_data['StrikeRate']))
        put_lastrates=np.array(list(pe_data['LastRate']))
        call_lastrates=np.array(list(ce_data['LastRate']))
        put_open=np.array(list(pe_data['OpenInterest']))-mp_open
        total_put_open=np.array(list(pe_data['OpenInterest']))
        total_call_open=np.array(list(ce_data['OpenInterest']))
        call_open=np.array(list(ce_data['OpenInterest']))-mc_open
        c_delta=np.array(ce_data['LastRate'])/(np.array(ce_data['LastRate'])+np.array(pe_data['LastRate']))
        p_delta=np.array(pe_data['LastRate'])/(np.array(ce_data['LastRate'])+np.array(pe_data['LastRate']))

        put_strike_premium=np.multiply(p_strikeprices-put_lastrates,p_delta)
        put_side1=np.dot(put_strike_premium,put_open)+put_side1
        strikes_lastrate=c_strikeprices-lastrate
        strikes_lastrate[strikes_lastrate>0]=0
        variable1=call_lastrates+strikes_lastrate
        variable1[variable1<0]=0
        call_side1=np.dot(variable1,np.multiply(call_open,c_delta))+call_side1
        weight=np.dot(total_put_open,p_delta)
        put_strike=(put_side1/weight)-(1/weight)*(call_side1)

        call_strike_premium=np.multiply(c_strikeprices+call_lastrates,c_delta)
        call_side2=np.dot(call_strike_premium,call_open)+call_side2
        strikes_lastrate=p_strikeprices-lastrate
        strikes_lastrate[strikes_lastrate<0]=0
        variable2=put_lastrates-strikes_lastrate
        variable2[variable2<0]=0
        put_side2=np.dot(variable2,np.multiply(put_open,p_delta))+put_side2
        weight2=np.dot(total_call_open,c_delta)
        call_strike=(call_side2/weight2)+(1/weight2)*(put_side2)
        resistance=(call_side2/weight2)
        support=(put_side1/weight)
    except Exception:
        lastrate=x
        p_strikeprices=np.array(list(pe_data['StrikeRate']))
        c_strikeprices=np.array(list(ce_data['StrikeRate']))
        put_lastrates=np.array(list(pe_data['LastRate']))
        call_lastrates=np.array(list(ce_data['LastRate']))
        put_open=np.array(list(pe_data['OpenInterest']))
        call_open=np.array(list(ce_data['OpenInterest']))
        c_delta=np.array(ce_data['LastRate'])/np.array((ce_data['LastRate'])+np.array(pe_data['LastRate']))
        p_delta=np.array(pe_data['LastRate'])/(np.array(ce_data['LastRate'])+np.array(pe_data['LastRate']))

        put_strike_premium=np.multiply(p_strikeprices-put_lastrates,p_delta)
        put_side1=np.dot(put_strike_premium,put_open)
        strikes_lastrate=c_strikeprices-lastrate
        strikes_lastrate[strikes_lastrate>0]=0
        variable1=call_lastrates+strikes_lastrate
        variable1[variable1<0]=0
        call_side1=np.dot(variable1,np.multiply(call_open,c_delta))
        weight=np.dot(put_open,p_delta)
        put_strike=(put_side1/weight)-(1/weight)*(call_side1)

        call_strike_premium=np.multiply(c_strikeprices+call_lastrates,c_delta)
        call_side2=np.dot(call_strike_premium,call_open)
        strikes_lastrate=p_strikeprices-lastrate
        strikes_lastrate[strikes_lastrate<0]=0
        variable2=put_lastrates-strikes_lastrate
        variable2[variable2<0]=0
        put_side2=np.dot(variable2,np.multiply(put_open,p_delta))
        weight2=np.dot(call_open,c_delta)
        call_strike=(call_side2/weight2)+(1/weight2)*(put_side2)
        
        resistance=(call_side2/weight2)
        support=(put_side1/weight)
    return call_strike,resistance,put_strike,support,put_side1,put_side2,call_side1,call_side2


def get_new_strikes(old_call,old_put,max_move_json):
    resistance=max_move_json['resistance'][-1]
    support=max_move_json['support'][-1]
    call_strike=max_move_json['c_strike'][-1]
    put_strike=max_move_json['p_strike'][-1]
    if resistance>old_call:
        t1=strike_list(resistance,call_strike+100)
        final_call=t1[int(np.floor((len(t1)-1)/2))]
    elif call_strike<old_call:
        t1=strike_list(resistance,call_strike+100)
        final_call=t1[int(np.floor((len(t1)-1)/2))]
    else:
        final_call=old_call
    if support<old_put:
        t1=strike_list(put_strike-100,support)
        final_put=t1[int(np.floor((len(t1)-1)/2))]
    elif put_strike>old_put:
        t1=strike_list(put_strike-100,support)
        final_put=t1[int(np.floor((len(t1)-1)/2))]
    else:
        final_put=old_put
    return int(final_call),int(final_put)
#orders_placing_defination
def place_orders(old_call,old_put,c_strike,p_strike,tron):

    if old_call!=c_strike:
        if old_call!=0:
            order_button(old_call,'CE_B',tron)
        order_button(c_strike,'CE_S',tron)
    if old_put!=p_strike:
        if old_put!=0:
            order_button(old_put,'PE_B',tron)
        order_button(p_strike,'PE_S',tron)

#%%
#variables to be initialised
client_name   = 'vinathi'
tron=int(input('enter the number of lots for buying (Eg 3):'))
prime_client=client_login(client=client_name)
expiry_timestamps=prime_client['login'].get_expiry("N","BANKNIFTY").copy()
current_expiry_time_stamp_weekly=int(expiry_timestamps['Expiry'][0]['ExpiryDate'][6:19])
option_chain=pd.DataFrame(prime_client['login'].get_option_chain("N","BANKNIFTY",current_expiry_time_stamp_weekly)['Options'])
x=expiry_timestamps['lastrate'][0]['LTP']
memory=0
put_side1,put_side2,call_side1,call_side2=0,0,0,0
c_strike=0
p_strike=0
max_move_json={'c_strike':[],'p_strike':[],'resistance':[],'support':[]}
#%%
ind_time = datetime.now(timezone("Asia/Kolkata")).strftime('%Y-%m-%d %H:%M:%S.%f')
while int(ind_time[11:13])*60+int(ind_time[14:16])<561 or int(ind_time[11:13])*60+int(ind_time[14:16])>885 :
    ind_time = datetime.now(timezone("Asia/Kolkata")).strftime('%Y-%m-%d %H:%M:%S.%f')
#%%
while True:
    while True:
        try :
            expiry_timestamps=prime_client['login'].get_expiry("N","BANKNIFTY").copy()
            option_chain=pd.DataFrame(prime_client['login'].get_option_chain("N","BANKNIFTY",current_expiry_time_stamp_weekly)['Options'])
            x=expiry_timestamps['lastrate'][0]['LTP']
            break
        except Exception :
            pass
    call_strike,resistance,put_strike,support,put_side1,put_side2,call_side1,call_side2=weighted_max_move2(option_chain,memory,x,put_side1,put_side2,call_side1,call_side2)
    memory=option_chain
    print('c_strike:   ',call_strike)
    print('p_strike:   ',put_strike)
    print('resistance: ',resistance)
    print('support:    ',support)
    max_move_json['c_strike']=max_move_json['c_strike']+[call_strike]
    max_move_json['p_strike']=max_move_json['p_strike']+[put_strike]
    max_move_json['resistance']=max_move_json['resistance']+[resistance]
    max_move_json['support']=max_move_json['support']+[support]
    old_call,old_put=c_strike,p_strike
    c_strike,p_strike=get_new_strikes(old_call=old_call,old_put=old_put,max_move_json=max_move_json)
    #strategy
    place_orders(old_put=old_put,old_call=old_call,c_strike=c_strike,p_strike=p_strike,tron=tron)

# %%
