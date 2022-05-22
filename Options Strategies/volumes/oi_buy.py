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
#Eg sample inputs: orders_track={} ,scrip_name='36500_CE_B',lots=3,price=234
def orders(orders_track,scrip_name,lots,price):
    a=orders_track.copy()
    ind_time = datetime.now(timezone("Asia/Kolkata")).strftime('%Y-%m-%d %H:%M:%S.%f')
    keys=list(orders_track.keys())
    if scrip_name in keys:
        a[scrip_name]=a[scrip_name]+[{'timestamp':ind_time,'lots':lots,'price':price}]
    else:
        a[scrip_name]=[{'timestamp':ind_time,'lots':lots,'price':price}]
    return a

    
#orders_track Eg: {'36000_CE_B' : [{'timestamp':,'lots':,'price':}],
#                              '35000_PE_S' : [{'timestamp':,'lots':,'price':},{'timestamp':,'lots':,'price':}]}  
def net_profit(orders_track):
    net=0
    for i in orders_track:
        temp=i.split('_')
        temp_price=0
        for k in range(0,len(orders_track[i])):
            temp_price=temp_price+orders_track[i][k]['price']*orders_track[i][k]['lots']
        net=net+temp_price*(-1*(temp[2]=='B')+(temp[2]=='S'))
    return net

def client_login(client,lots):
    import json
    f = open ('credentials.json', "r")
    creds = json.loads(f.read())
    client_list={}
    client_list[client]={'strategy':{},'login':{},'lots':{}}
    client_list[client]['lots']=lots
    vinathi_cred = creds[client]["keys"]
    user = creds[client]["user"]
    passw = creds[client]["passw"]
    dob = creds[client]["dob"]
    client_list[client]['strategy']=strategies(user=user, passw=passw, dob=dob,cred=vinathi_cred)
    client_list[client]['login']=FivePaisaClient(email=user, passwd=passw, dob=dob,cred=vinathi_cred)
    client_list[client]['login'].login()
    return client_list[client]
client_name=input('enter the client name Eg: vinathi,bhaskar ')
lots=int(input('lots (Eg:3):'))
#%%
ind_time = datetime.now(timezone("Asia/Kolkata")).strftime('%Y-%m-%d %H:%M:%S.%f')
while int(ind_time[11:13])*60+int(ind_time[14:16])<561 or int(ind_time[11:13])*60+int(ind_time[14:16])>885 :
    ind_time = datetime.now(timezone("Asia/Kolkata")).strftime('%Y-%m-%d %H:%M:%S.%f')
#%%
prime_client=client_login(client=client_name,lots=lots)
expiry_timestamps=prime_client['login'].get_expiry("N","BANKNIFTY")
current_expiry_time_stamp=int(expiry_timestamps['Expiry'][0]['ExpiryDate'][6:19])
option_chain=pd.DataFrame(prime_client['login'].get_option_chain("N","BANKNIFTY",current_expiry_time_stamp)['Options'])
def pe_oi(strikeprice):
    c_strike=option_chain[option_chain['StrikeRate']==strikeprice]
    to_return=int(c_strike[c_strike['CPType']=='PE']['OpenInterest'])
    return to_return
def ce_oi(strikeprice):
    c_strike=option_chain[option_chain['StrikeRate']==strikeprice]
    to_return=int(c_strike[c_strike['CPType']=='CE']['OpenInterest'])
    return to_return
def pe_oi_change(strikeprice):
    c_strike=option_chain[option_chain['StrikeRate']==strikeprice]
    to_return=int(c_strike[c_strike['CPType']=='PE']['ChangeInOI'])
    return to_return
def ce_oi_change(strikeprice):
    c_strike=option_chain[option_chain['StrikeRate']==strikeprice]
    to_return=int(c_strike[c_strike['CPType']=='CE']['ChangeInOI'])
    return to_return
def simple_trend():
    req_list_=[{"Exch":"N","ExchType":"C","Symbol":"BANKNIFTY","Scripcode":"999920005","OptionType":"EQ"}]          
    a=prime_client['login'].fetch_market_feed(req_list_)
    x=a['Data'][0]['LastRate']
    bot=np.floor(x/100)*100
    top=np.ceil(x/100)*100
    bot_at=np.floor(x/500)*500
    top_at=np.ceil(x/500)*500

    if top_at-x>250:
        bot_500=bot_at-500
        top_500=bot_at+500
        top_1000=bot_at+1000
        bot_1000=bot_at-1000
    else:
        bot_500=top_at-500
        top_500=top_at+500
        top_1000=top_at+1000
        bot_1000=top_at-1000
    ce_net=ce_oi(bot)+ce_oi(top)+ce_oi(top_500)+ce_oi(top_1000)
    pe_net=pe_oi(bot)+pe_oi(top)+pe_oi(bot_500)+pe_oi(bot_1000)
    if ce_net>pe_net:
        return 'downtrend'
    else:
        return 'uptrend'

def complex_trend():
    req_list_=[{"Exch":"N","ExchType":"C","Symbol":"BANKNIFTY","Scripcode":"999920005","OptionType":"EQ"}]          
    a=prime_client['login'].fetch_market_feed(req_list_)
    x=a['Data'][0]['LastRate']
    x_change=a['Data'][0]['Chg']
    bot=np.floor(x/100)*100
    top=np.ceil(x/100)*100
    bot_at=np.floor(x/500)*500
    top_at=np.ceil(x/500)*500
    if top_at-x>250:
        bot_500=bot_at-500
        top_500=bot_at+500
        top_1000=bot_at+1000
        bot_1000=bot_at-1000
    else:
        bot_500=top_at-500
        top_500=top_at+500
        top_1000=top_at+1000
        bot_1000=top_at-1000
    ce_net_change=ce_oi_change(bot)+ce_oi_change(top)+ce_oi_change(top_500)+ce_oi_change(top_1000)
    pe_net_change=pe_oi_change(bot)+pe_oi_change(top)+pe_oi_change(bot_500)+pe_oi_change(bot_1000)
    if x_change>0 :
        if pe_net_change>0 and ce_net_change<0:
            return "uptrend at it's peak"
        if pe_net_change<0 and ce_net_change>0:
            return "strong downtrend about to start in a while"
        if pe_net_change<0 and ce_net_change<0:
            return "A strong move on either side is a possibility"
        if pe_net_change>0 and ce_net_change>0 and pe_net_change>ce_net_change:
            return "slightly uptrend"
        if pe_net_change>0 and ce_net_change>0 and pe_net_change<ce_net_change:
            return "slightly downtrend"
    if x_change<=0 :
        if pe_net_change>0 and ce_net_change<0:
            return "strong uptrend about to start in a while"
        if pe_net_change<0 and ce_net_change>0:
            return "downtrend at it's peak"
        if pe_net_change<0 and ce_net_change<0:
            return "A strong move on either side is a possibility"
        if pe_net_change>0 and ce_net_change>0 and pe_net_change>ce_net_change:
            return "slightly uptrend"    
        if pe_net_change>0 and ce_net_change>0 and pe_net_change<ce_net_change:
            return "slightly downtrend"

def projected():
    kkk=option_chain[option_chain['CPType']=='PE']
    i=np.array(kkk['StrikeRate'])[0]
    end=np.array(kkk['StrikeRate'])[-1]
    ss=np.array(kkk['StrikeRate'])
    pe_data=option_chain[option_chain['CPType']=='PE']
    ce_data=option_chain[option_chain['CPType']=='CE']
    p_lastrate=np.array(pe_data['LastRate'])
    c_lastrate=np.array(ce_data['LastRate'])
    p_openinterest=np.array(pe_data['OpenInterest'])
    c_openinterest=np.array(ce_data['OpenInterest'])
    data=[]
    while i<end:
        i=i+1
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
    index=np.argmin(np.abs(data))
    return   np.array(option_chain['StrikeRate'])[0]+index
        #print(init_ce-end_ce-init_pe+end_pe)
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


control=0
tim=0
orders_track={}
first_iter=0
p_slabs=0
n_slabs=0
p_slabs1=0
n_slabs1=0
total_lots=0
reversal=3
while True:
    while True:
        try :
            expiry_timestamps=prime_client['login'].get_expiry("N","BANKNIFTY")
            current_expiry_time_stamp=int(expiry_timestamps['Expiry'][0]['ExpiryDate'][6:19])
            option_chain=pd.DataFrame(prime_client['login'].get_option_chain("N","BANKNIFTY",current_expiry_time_stamp)['Options'])
            break
        except Exception :
            pass
    req_list_=[{"Exch":"N","ExchType":"C","Symbol":"BANKNIFTY","Scripcode":"999920005","OptionType":"EQ"}]      
    a=prime_client['login'].fetch_market_feed(req_list_)
    x=a['Data'][0]['LastRate']
    simple=simple_trend()
    complex=complex_trend()
    proj=projected()
    if first_iter==0:
        referance=x-proj
        strike = round(x/100)*100
        first_iter=1
    ind_time = datetime.now(timezone("Asia/Kolkata")).strftime('%Y-%m-%d %H:%M:%S.%f')
    print(proj)
    c_data=option_chain[option_chain['CPType']=='CE']
    p_data=option_chain[option_chain['CPType']=='PE']
    ind=np.round((x-proj-referance)/10)
    trend=x-proj
    c1=int(c_data[c_data['StrikeRate']==int(np.floor(x/100)*100)]['LastRate'])
    c2=int(c_data[c_data['StrikeRate']==int(np.ceil(x/100)*100)]['LastRate'])
    p1=int(p_data[p_data['StrikeRate']==int(np.floor(x/100)*100)]['LastRate'])
    p2=int(p_data[p_data['StrikeRate']==int(np.ceil(x/100)*100)]['LastRate'])
    dynamic_crossover=(c1+c2+p1+p2)/20
    if trend>dynamic_crossover :
        if reversal==0:
            #squareoff puts
            test_order = Order(order_type='S',exchange='N',exchange_segment='D', scrip_code =p_scrip , quantity=25*total_lots, price=0 ,is_intraday=False,remote_order_id="ta")
            total_lots=0
            p_slabs=0
            n_slabs=0
            p_slabs1=0
            n_slabs1=0
        reversal=1
        if ind>=p_slabs:
            c_scrip=int(c_data[c_data['StrikeRate']==strike]['ScripCode'])
            c_lastrate=float(c_data[c_data['StrikeRate']==strike]['LastRate'])
            test_order = Order(order_type='B',exchange='N',exchange_segment='D', scrip_code =c_scrip , quantity=25*prime_client['lots'], price=0 ,is_intraday=False,remote_order_id="tag")
            status = prime_client['login'].place_order(test_order)
            p_slabs=p_slabs+1
            if status['Message']=='Success' :
                orders_track=orders(orders_track=orders_track,scrip_name=str(strike)+'_CE_B',lots=prime_client['lots'],price=c_lastrate)
                total_lots=total_lots+prime_client['lots']
                
        if ind<n_slabs and total_lots>0:
            test_order = Order(order_type='S',exchange='N',exchange_segment='D', scrip_code =c_scrip , quantity=25*prime_client['lots'], price=0 ,is_intraday=False,remote_order_id="ta")
            status = prime_client['login'].place_order(test_order)
            c_lastrate=float(c_data[c_data['StrikeRate']==strike]['LastRate'])
            orders_track=orders(orders_track=orders_track,scrip_name=str(strike)+'_CE_S',lots=prime_client['lots'],price=c_lastrate)
            total_lots=total_lots-prime_client['lots']
            n_slabs=n_slabs-1
            
    if trend<-dynamic_crossover:
        if reversal==1:
            #squareoff calls
            test_order = Order(order_type='S',exchange='N',exchange_segment='D', scrip_code =c_scrip , quantity=25*total_lots, price=0 ,is_intraday=False,remote_order_id="ta")
            total_lots=0
            p_slabs=0
            n_slabs=0
            p_slabs1=0
            n_slabs1=0
        reversal=0
        if ind<=n_slabs1:
            p_scrip=int(p_data[p_data['StrikeRate']==strike]['ScripCode'])
            p_lastrate=float(p_data[p_data['StrikeRate']==strike]['LastRate'])
            test_order = Order(order_type='B',exchange='N',exchange_segment='D', scrip_code =p_scrip , quantity=25*prime_client['lots'], price=0 ,is_intraday=False,remote_order_id="tag")
            status = prime_client['login'].place_order(test_order)
            n_slabs1=n_slabs1-1
            if status['Message']=='Success' :
                orders_track=orders(orders_track=orders_track,scrip_name=str(strike)+'_PE_B',lots=prime_client['lots'],price=p_lastrate)
                total_lots=total_lots+prime_client['lots']
                
        if ind>p_slabs1 and total_lots>0:
            test_order = Order(order_type='S',exchange='N',exchange_segment='D', scrip_code =p_scrip , quantity=25*prime_client['lots'], price=0 ,is_intraday=False,remote_order_id="ta")
            status = prime_client['login'].place_order(test_order)
            p_lastrate=float(p_data[p_data['StrikeRate']==strike]['LastRate'])
            orders_track=orders(orders_track=orders_track,scrip_name=str(strike)+'_PE_S',lots=prime_client['lots'],price=c_lastrate)
            total_lots=total_lots-prime_client['lots']
            p_slabs1=p_slabs1+1    
            
    ind_time = datetime.now(timezone("Asia/Kolkata")).strftime('%Y-%m-%d %H:%M:%S.%f')
    if int(ind_time[11:13])==15 and int(ind_time[14:16])>=25 :
        if reversal==1:
            test_order = Order(order_type='S',exchange='N',exchange_segment='D', scrip_code =c_scrip , quantity=25*total_lots, price=0 ,is_intraday=False,remote_order_id="ta")
        if reversal==0:
            test_order = Order(order_type='S',exchange='N',exchange_segment='D', scrip_code =p_scrip , quantity=25*total_lots, price=0 ,is_intraday=False,remote_order_id="ta")
        break
# %%
