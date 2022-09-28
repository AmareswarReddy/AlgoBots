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
def strike_list(a,b):
    a=np.linspace(int(np.floor(a/100)*100),int(np.ceil(b/100)*100),int((int(np.ceil(b/100)*100)-int(np.floor(a/100)*100))/100)+1)
    if len(a)==1:
        a=a+a[0]
    return a


def max_move2(option_chain,memory,x,put_side1,put_side2,call_side1,call_side2):
    p_data=option_chain[option_chain['CPType']=='PE']
    c_data=option_chain[option_chain['CPType']=='CE']
    pe_data=p_data[(p_data['LastRate']>0)].copy()
    ce_data=c_data[c_data['LastRate']>0].copy()
    try:
        m_p_data=memory[memory['CPType']=='PE']
        m_c_data=memory[memory['CPType']=='CE']
        m_pe_data=m_p_data[(m_p_data['LastRate']>0)].copy()
        m_ce_data=m_c_data[m_c_data['LastRate']>0].copy()
        mp_open=np.array(list(m_pe_data['OpenInterest']))
        mc_open=np.array(list(m_ce_data['OpenInterest']))
        lastrate=x
        p_strikeprices=np.array(list(pe_data['StrikeRate']))
        c_strikeprices=np.array(list(ce_data['StrikeRate']))
        put_lastrates=np.array(list(pe_data['LastRate']))
        call_lastrates=np.array(list(ce_data['LastRate']))
        put_open=np.array(list(pe_data['OpenInterest']))-mp_open
        total_put_open=np.array(list(pe_data['OpenInterest']))
        total_call_open=np.array(list(ce_data['OpenInterest']))
        call_open=np.array(list(ce_data['OpenInterest']))-mc_open

        put_strike_premium=p_strikeprices-put_lastrates
        put_side1=np.dot(put_strike_premium,put_open)+put_side1
        strikes_lastrate=c_strikeprices-lastrate
        strikes_lastrate[strikes_lastrate>0]=0
        call_side1=np.dot(call_lastrates+strikes_lastrate,call_open)+call_side1
        put_strike=(put_side1/np.sum(total_put_open))-(1/np.sum(total_put_open))*(call_side1)

        call_strike_premium=c_strikeprices+call_lastrates
        call_side2=np.dot(call_strike_premium,call_open)+call_side2
        strikes_lastrate=p_strikeprices-lastrate
        strikes_lastrate[strikes_lastrate<0]=0
        put_side2=np.dot(put_lastrates-strikes_lastrate,put_open)+put_side2
        call_strike=(call_side2/np.sum(total_call_open))+(1/np.sum(total_call_open))*(put_side2)
        resistance=(call_side2/np.sum(total_call_open))
        support=(put_side1/np.sum(total_put_open))
    except Exception:
        lastrate=x
        p_strikeprices=np.array(list(pe_data['StrikeRate']))
        c_strikeprices=np.array(list(ce_data['StrikeRate']))
        put_lastrates=np.array(list(pe_data['LastRate']))
        call_lastrates=np.array(list(ce_data['LastRate']))
        put_open=np.array(list(pe_data['OpenInterest']))
        call_open=np.array(list(ce_data['OpenInterest']))

        put_strike_premium=p_strikeprices-put_lastrates
        put_side1=np.dot(put_strike_premium,put_open)
        strikes_lastrate=c_strikeprices-lastrate
        strikes_lastrate[strikes_lastrate>0]=0
        call_side1=np.dot(call_lastrates+strikes_lastrate,call_open)
        put_strike=(put_side1/np.sum(put_open))-(1/np.sum(put_open))*(call_side1)

        call_strike_premium=c_strikeprices+call_lastrates
        call_side2=np.dot(call_strike_premium,call_open)
        strikes_lastrate=p_strikeprices-lastrate
        strikes_lastrate[strikes_lastrate<0]=0
        put_side2=np.dot(put_lastrates-strikes_lastrate,put_open)
        call_strike=(call_side2/np.sum(call_open))+(1/np.sum(call_open))*(put_side2)
        resistance=(call_side2/np.sum(call_open))
        support=(put_side1/np.sum(put_open))
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
#%%
ind_time = datetime.now(timezone("Asia/Kolkata")).strftime('%Y-%m-%d %H:%M:%S.%f')
while int(ind_time[11:13])*60+int(ind_time[14:16])<561 or int(ind_time[11:13])*60+int(ind_time[14:16])>885 :
    ind_time = datetime.now(timezone("Asia/Kolkata")).strftime('%Y-%m-%d %H:%M:%S.%f')
#%%
#variables to be initialised
client_name   = 'vinathi'
#lots=int(input('lots (Eg:3):'))
prime_client=client_login(client=client_name)
expiry_timestamps=prime_client['login'].get_expiry("N","BANKNIFTY").copy()
current_expiry_time_stamp_weekly=int(expiry_timestamps['Expiry'][0]['ExpiryDate'][6:19])
option_chain=pd.DataFrame(prime_client['login'].get_option_chain("N","BANKNIFTY",current_expiry_time_stamp_weekly)['Options'])
x=expiry_timestamps['lastrate'][0]['LTP']
memory=0
tron=int(input('enter the number of lots for buying :'))
put_side1,put_side2,call_side1,call_side2=0,0,0,0
c_strike=9999999999
p_strike=0
max_move_json={'c_strike':[],'p_strike':[],'resistance':[],'support':[]}
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
    call_strike,resistance,put_strike,support,put_side1,put_side2,call_side1,call_side2=max_move2(option_chain,memory,x,put_side1,put_side2,call_side1,call_side2)
    #call_strike,resistance,put_strike,support,put_side1,put_side2,call_side1,call_side2=weighted_max_move2(option_chain,memory,x,put_side1,put_side2,call_side1,call_side2)
    memory=option_chain
    print('c_strike:   ',call_strike)
    print('p_strike:   ',put_strike)
    print('resistance: ',resistance)
    print('support:    ',support)
    max_move_json['c_strike']=max_move_json['c_strike']+[call_strike]
    max_move_json['p_strike']=max_move_json['p_strike']+[put_strike]
    max_move_json['resistance']=max_move_json['resistance']+[resistance]
    max_move_json['support']=max_move_json['support']+[support]
    #strategy
    old_call,old_put=c_strike,p_strike
    c_strike,p_strike=get_new_strikes(old_call=old_call,old_put=old_put,max_move_json=max_move_json)
    #safe straddle

# %%
