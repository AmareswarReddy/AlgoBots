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
    client_list[client]['lots']=round((client_list[client]['login'].margin()[0]['AvailableMargin']-100000)/200000)
    return client_list[client]
#client_name=input('enter the client name Eg: vinathi,bhaskar ')
import sys
client_name   = 'vinathi'
#lots=int(input('lots (Eg:3):'))


#%%
ind_time = datetime.now(timezone("Asia/Kolkata")).strftime('%Y-%m-%d %H:%M:%S.%f')
while int(ind_time[11:13])*60+int(ind_time[14:16])<561 or int(ind_time[11:13])*60+int(ind_time[14:16])>885 :
    ind_time = datetime.now(timezone("Asia/Kolkata")).strftime('%Y-%m-%d %H:%M:%S.%f')
#%%
prime_client=client_login(client=client_name)
expiry_timestamps=prime_client['login'].get_expiry("N","BANKNIFTY").copy()
current_expiry_time_stamp_weekly=int(expiry_timestamps['Expiry'][0]['ExpiryDate'][6:19])
option_chain=pd.DataFrame(prime_client['login'].get_option_chain("N","BANKNIFTY",current_expiry_time_stamp_weekly)['Options'])

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
    return  a,round(b/100)*100,round(c/100)*100


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

trend_indicator={
            'timestamp':[],
            'simple':[],
            'complex':[],
            'projected':[],
            'spotprice':[]
            }
control=0
tim=0
orders_track={}

proj,c_striker,p_striker=rosetta_strikes(option_chain)
c_data=option_chain[option_chain['CPType']=='CE']
p_data=option_chain[option_chain['CPType']=='PE']
c_scrip=int(c_data[c_data['StrikeRate']==c_striker]['ScripCode'])
p_scrip=int(p_data[p_data['StrikeRate']==p_striker]['ScripCode'])
test_order = Order(order_type='S',exchange='N',exchange_segment='D', scrip_code =p_scrip , quantity=25*prime_client['lots'], price=0 ,is_intraday=False,remote_order_id="tag")
status = prime_client['login'].place_order(test_order)
test_order = Order(order_type='S',exchange='N',exchange_segment='D', scrip_code =c_scrip , quantity=25*prime_client['lots'], price=0 ,is_intraday=False,remote_order_id="tag")
status = prime_client['login'].place_order(test_order)
rosetta_quotient1=0.3
rosetta_quotient2=-0.3
breaker=0
c_lots_track=prime_client['lots']
p_lots_track=prime_client['lots']
initial_lots=prime_client['lots']


def decoy1(option_chain,c_striker,p_striker,dynamic_crossover,prime_client,c_lots_track,p_lots_track):
    c_temp = c_striker
    p_temp = p_striker
    proj,C,P=rosetta_strikes(option_chain)
    p_data=option_chain[option_chain['CPType']=='PE']
    if abs(C-c_striker)>dynamic_crossover:
        c_data=option_chain[option_chain['CPType']=='CE']
        c_scrip=int(c_data[c_data['StrikeRate']==c_striker]['ScripCode'])
        test_order = Order(order_type='B',exchange='N',exchange_segment='D', scrip_code =c_scrip , quantity=25*c_lots_track, price=0 ,is_intraday=False,remote_order_id="tag")
        prime_client['login'].place_order(test_order)
        c_scrip=int(c_data[c_data['StrikeRate']==C]['ScripCode'])
        test_order = Order(order_type='S',exchange='N',exchange_segment='D', scrip_code =c_scrip , quantity=25*c_lots_track, price=0 ,is_intraday=False,remote_order_id="tag")
        prime_client['login'].place_order(test_order)
        c_temp=C
    if abs(P-p_striker)>dynamic_crossover:
        p_data=option_chain[option_chain['CPType']=='PE']
        p_scrip=int(p_data[p_data['StrikeRate']==p_striker]['ScripCode'])
        test_order = Order(order_type='B',exchange='N',exchange_segment='D', scrip_code =p_scrip , quantity=25*p_lots_track, price=0 ,is_intraday=False,remote_order_id="tag")
        prime_client['login'].place_order(test_order)
        p_scrip=int(p_data[p_data['StrikeRate']==P]['ScripCode'])
        test_order = Order(order_type='S',exchange='N',exchange_segment='D', scrip_code =p_scrip , quantity=25*p_lots_track, price=0 ,is_intraday=False,remote_order_id="tag")
        prime_client['login'].place_order(test_order)
        p_temp=P
    return c_temp,p_temp


def decoy2(x,option_chain,c_striker,p_striker,dynamic_crossover,prime_client,c_lots_track,p_lots_track,rosetta_quotient1,rosetta_quotient2,initial_lots):
    c_lots_track_temp=c_lots_track
    p_lots_track_temp=p_lots_track
    rosetta_quotient1_temp=rosetta_quotient1
    rosetta_quotient2_temp=rosetta_quotient2
    proj,C,P=rosetta_strikes(option_chain)
    if (proj-x)/dynamic_crossover>rosetta_quotient1 and p_lots_track>5 and p_lots_track<=c_lots_track:  
        p_data=option_chain[option_chain['CPType']=='PE']
        c_data=option_chain[option_chain['CPType']=='CE']
        p_scrip=int(p_data[p_data['StrikeRate']==p_striker]['ScripCode'])
        test_order = Order(order_type='B',exchange='N',exchange_segment='D', scrip_code =p_scrip , quantity=25*5, price=0 ,is_intraday=False,remote_order_id="tag")
        prime_client['login'].place_order(test_order)
        c_scrip=int(c_data[c_data['StrikeRate']==c_striker]['ScripCode'])
        test_order = Order(order_type='S',exchange='N',exchange_segment='D', scrip_code =c_scrip , quantity=25, price=0 ,is_intraday=False,remote_order_id="tag")
        status=prime_client['login'].place_order(test_order)
        p_lots_track_temp=p_lots_track-5
        rosetta_quotient1_temp=rosetta_quotient1+0.2
        if status['Message']=='Success':
            c_lots_track_temp=c_lots_track+1
    if (proj-x)/dynamic_crossover>0.1 and p_lots_track>c_lots_track:  
        p_data=option_chain[option_chain['CPType']=='PE']
        c_data=option_chain[option_chain['CPType']=='CE']
        p_scrip=int(p_data[p_data['StrikeRate']==p_striker]['ScripCode'])
        if p_lots_track-initial_lots>0:
            test_order = Order(order_type='B',exchange='N',exchange_segment='D', scrip_code =p_scrip , quantity=25*(p_lots_track-initial_lots), price=0 ,is_intraday=False,remote_order_id="tag")
            p_lots_track_temp=initial_lots
            prime_client['login'].place_order(test_order)
        c_scrip=int(c_data[c_data['StrikeRate']==c_striker]['ScripCode'])
        test_order = Order(order_type='S',exchange='N',exchange_segment='D', scrip_code =c_scrip , quantity=25*(initial_lots-c_lots_track), price=0 ,is_intraday=False,remote_order_id="tag")
        status=prime_client['login'].place_order(test_order)
        
        rosetta_quotient1_temp=0.3
        if status['Message']=='Success':
            c_lots_track_temp=initial_lots
    if (proj-x)/dynamic_crossover<rosetta_quotient2 and c_lots_track>5 and p_lots_track>=c_lots_track:  
        p_data=option_chain[option_chain['CPType']=='PE']
        c_data=option_chain[option_chain['CPType']=='CE']
        c_scrip=int(c_data[c_data['StrikeRate']==c_striker]['ScripCode'])
        test_order = Order(order_type='B',exchange='N',exchange_segment='D', scrip_code =c_scrip , quantity=25*5, price=0 ,is_intraday=False,remote_order_id="tag")
        prime_client['login'].place_order(test_order)
        p_scrip=int(p_data[p_data['StrikeRate']==p_striker]['ScripCode'])
        test_order = Order(order_type='S',exchange='N',exchange_segment='D', scrip_code =p_scrip , quantity=25, price=0 ,is_intraday=False,remote_order_id="tag")
        status=prime_client['login'].place_order(test_order)
        c_lots_track_temp=c_lots_track-5
        rosetta_quotient2_temp=rosetta_quotient2-0.2
        if status['Message']=='Success':
            p_lots_track_temp=p_lots_track+1
            
    if (proj-x)/dynamic_crossover<-0.1 and p_lots_track<c_lots_track:  
        p_data=option_chain[option_chain['CPType']=='PE']
        c_data=option_chain[option_chain['CPType']=='CE']
        c_scrip=int(c_data[c_data['StrikeRate']==c_striker]['ScripCode'])
        if c_lots_track-initial_lots>0:
            test_order = Order(order_type='B',exchange='N',exchange_segment='D', scrip_code =c_scrip , quantity=25*(c_lots_track-initial_lots), price=0 ,is_intraday=False,remote_order_id="tag")
            c_lots_track_temp=initial_lots
            prime_client['login'].place_order(test_order) 
        p_scrip=int(p_data[p_data['StrikeRate']==p_striker]['ScripCode'])
        test_order = Order(order_type='S',exchange='N',exchange_segment='D', scrip_code =p_scrip , quantity=25*(initial_lots-p_lots_track), price=0 ,is_intraday=False,remote_order_id="tag")
        status=prime_client['login'].place_order(test_order)
        rosetta_quotient1_temp=-0.3
        if status['Message']=='Success':
            p_lots_track_temp=initial_lots
        
    return p_lots_track_temp,c_lots_track_temp,rosetta_quotient1_temp,rosetta_quotient2_temp    
expiry_timestamps=prime_client['login'].get_expiry("N","BANKNIFTY").copy()
current_expiry_time_stamp_weekly=int(expiry_timestamps['Expiry'][0]['ExpiryDate'][6:19])
#%%
while True:
    while True:
        try :
            option_chain=pd.DataFrame(prime_client['login'].get_option_chain("N","BANKNIFTY",current_expiry_time_stamp_weekly)['Options'])
            banknifty_lastrate=expiry_timestamps['lastrate'][0]['LTP']
            break
        except Exception :
            pass
    proj,Cyi,Phf=rosetta_strikes(option_chain)
    project_k=banknifty_lastrate-proj
    print('Niftybank:  ',project_k)
    x=banknifty_lastrate
    ind_time = datetime.now(timezone("Asia/Kolkata")).strftime('%Y-%m-%d %H:%M:%S.%f')
    c_data=option_chain[option_chain['CPType']=='CE']
    p_data=option_chain[option_chain['CPType']=='PE']
    #strategy
    c1=int(c_data[c_data['StrikeRate']==int(np.floor(x/100)*100)]['LastRate'])
    c2=int(c_data[c_data['StrikeRate']==int(np.ceil(x/100)*100)]['LastRate'])
    p1=int(p_data[p_data['StrikeRate']==int(np.floor(x/100)*100)]['LastRate'])
    p2=int(p_data[p_data['StrikeRate']==int(np.ceil(x/100)*100)]['LastRate'])
    dynamic_crossover=(c1+c2+p1+p2)/4

    c_striker,p_striker = decoy1(option_chain,c_striker,p_striker,dynamic_crossover,prime_client,c_lots_track,p_lots_track)
    p_lots_track,c_lots_track,rosetta_quotient1,rosetta_quotient2=decoy2(x,option_chain,c_striker,p_striker,dynamic_crossover,prime_client,c_lots_track,p_lots_track,rosetta_quotient1,rosetta_quotient2,initial_lots)

# %%
