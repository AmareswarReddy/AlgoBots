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
    client_list[client]['lots']=round((client_list[client]['login'].margin()[0]['AvailableMargin']-200000)/180000)
    return client_list[client]
#client_name=input('enter the client name Eg: vinathi,bhaskar ')
import sys
client_name   = 'vinathi'
#lots=int(input('lots (Eg:3):'))
tron=int(input('enter the number of lots for buying :'))
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


def smart_ass(option_chain,c_delta_O,p_delta_O,e_ce,e_pe,i_ce,i_pe,ricker):
    pe_data=option_chain[option_chain['CPType']=='PE']
    ce_data=option_chain[option_chain['CPType']=='CE']
    i=np.array(pe_data['StrikeRate'])[0]
    n=np.array(pe_data['StrikeRate'])[1]
    end=np.array(pe_data['StrikeRate'])[-1]
    ss=np.array(pe_data['StrikeRate'])
    p_lastrate=np.array(pe_data['LastRate'])
    c_lastrate=np.array(ce_data['LastRate'])
    data=[]
    data1=[]
    data2=[]
    c_war=[]
    p_war=[]
    c_truce=[]
    p_truce=[]
    increment=(n-i)/15
    kk=0
    while i<end:
        i=i+increment
        init_ce=0
        init_pe=0
        end_pe=0
        end_ce=0
        if ricker!=0:
            for k in range(0,len(ss)):
                init_pe=init_pe+p_lastrate[k]*p_delta_O[k]
                init_ce=init_ce+c_lastrate[k]*c_delta_O[k]
                end_pe=end_pe+p_delta_O[k]*max((ss[k]-i),0)
                end_ce=end_ce+c_delta_O[k]*max((i-ss[k]),0)
            c_war=c_war+[init_ce]
            p_war=p_war+[init_pe]
            c_truce=c_truce+[end_ce]
            p_truce=p_truce+[end_pe]
            data=data+[init_ce+i_ce[kk]-e_ce[kk]-end_ce-i_pe[kk]-init_pe+e_pe[kk]+end_pe]
            data1=data1+[init_ce+i_ce[kk]-end_ce-e_ce[kk]]
            data2=data2+[-init_pe-i_pe[kk]+end_pe+e_pe[kk]]
            kk=kk+1
        else:
            p_openinterest=np.array(pe_data['OpenInterest'])
            c_openinterest=np.array(ce_data['OpenInterest'])
            for k in range(0,len(ss)):
                init_pe=init_pe+p_lastrate[k]*p_openinterest[k]
                init_ce=init_ce+c_lastrate[k]*c_openinterest[k]
                end_pe=end_pe+p_openinterest[k]*max((ss[k]-i),0)
                end_ce=end_ce+c_openinterest[k]*max((i-ss[k]),0)
            c_war=c_war+[init_ce]
            p_war=p_war+[init_pe]
            c_truce=c_truce+[end_ce]
            p_truce=p_truce+[end_pe]
            data=data+[init_ce-end_ce-init_pe+end_pe]
            data1=data1+[init_ce-end_ce]
            data2=data2+[-init_pe+end_pe]
    index=np.argmin(np.abs(data))
    index1=np.argmin(np.abs(data1))
    index2=np.argmin(np.abs(data2))
    a=np.array(option_chain['StrikeRate'])[0]+index*increment
    b=np.array(option_chain['StrikeRate'])[0]+index1*increment
    c=np.array(option_chain['StrikeRate'])[0]+index2*increment
    return  a,round(b/100)*100,round(c/100)*100, np.array(c_truce)+e_ce,np.array(p_truce)+e_pe,np.array(c_war)+i_ce,np.array(p_war)+i_pe

def past_picture(indicator,project_k,b_lastrate,x,delta):
    indicator=indicator+[project_k]
    b_lastrate=b_lastrate+[x]
    n=len(b_lastrate)
    div_factor=0
    local_div_factor=0
    instant_div_factor=0
    if n>2:
        for i in range(1,n):
            a=(b_lastrate[n-1]-b_lastrate[i])
            b=(indicator[n-1]-indicator[i])
            div_factor=div_factor+b+a*delta/4
        div_factor=div_factor/n
    if n>121:
        for i in range(n-120,n):
            a=(b_lastrate[n-1]-b_lastrate[i])
            b=(indicator[n-1]-indicator[i])
            local_div_factor=local_div_factor+b+a*delta/4
        local_div_factor=local_div_factor/120
    if n>21:
        for i in range(n-20,n):
            a=(b_lastrate[n-1]-b_lastrate[i])
            b=(indicator[n-1]-indicator[i])
            instant_div_factor=instant_div_factor+b+a*delta/4
        instant_div_factor=instant_div_factor/20
    return indicator,b_lastrate,div_factor,local_div_factor,instant_div_factor

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
        sleep(5)
        test_order = Order(order_type='S',exchange='N',exchange_segment='D', scrip_code =c_scrip , quantity=25*c_lots_track, price=0 ,is_intraday=False,remote_order_id="tag")
        status1=prime_client['login'].place_order(test_order)
        if status1['Message']!='Success':
            com=c_lots_track
            shrink=round(prime_client['login'].margin()[0]['AvailableMargin']/180000)
            while shrink<=com:
                test_order_k1 = Order(order_type='S',exchange='N',exchange_segment='D', scrip_code =c_scrip , quantity=25*(shrink), price=0 ,is_intraday=False,remote_order_id="tag")
                prime_client['login'].place_order(test_order_k1)
                com=com-shrink
                sleep(2)
                shrink=round(prime_client['login'].margin()[0]['AvailableMargin']/180000)
            test_order_k1 = Order(order_type='S',exchange='N',exchange_segment='D', scrip_code =c_scrip , quantity=25*(com), price=0 ,is_intraday=False,remote_order_id="tag")
            prime_client['login'].place_order(test_order_k1)
        c_temp=C
    if abs(P-p_striker)>dynamic_crossover:
        p_data=option_chain[option_chain['CPType']=='PE']
        p_scrip=int(p_data[p_data['StrikeRate']==p_striker]['ScripCode'])
        test_order = Order(order_type='B',exchange='N',exchange_segment='D', scrip_code =p_scrip , quantity=25*p_lots_track, price=0 ,is_intraday=False,remote_order_id="tag")
        prime_client['login'].place_order(test_order)
        p_scrip=int(p_data[p_data['StrikeRate']==P]['ScripCode'])
        test_order = Order(order_type='S',exchange='N',exchange_segment='D', scrip_code =p_scrip , quantity=25*p_lots_track, price=0 ,is_intraday=False,remote_order_id="tag")
        sleep(5)
        status1=prime_client['login'].place_order(test_order)
        if status1['Message']!='Success':
            com=p_lots_track
            shrink=round(prime_client['login'].margin()[0]['AvailableMargin']/180000)
            while shrink<=com:
                test_order_k1 = Order(order_type='S',exchange='N',exchange_segment='D', scrip_code =p_scrip , quantity=25*(shrink), price=0 ,is_intraday=False,remote_order_id="tag")
                prime_client['login'].place_order(test_order_k1)
                com=com-shrink
                sleep(2)
                shrink=round(prime_client['login'].margin()[0]['AvailableMargin']/180000)
            test_order_k1 = Order(order_type='S',exchange='N',exchange_segment='D', scrip_code =p_scrip , quantity=25*(com), price=0 ,is_intraday=False,remote_order_id="tag")
            prime_client['login'].place_order(test_order_k1)
        p_temp=P
    return c_temp,p_temp


def decoy2(x,option_chain,c_striker,p_striker,dynamic_crossover,prime_client,c_lots_track,p_lots_track,rosetta_quotient1,rosetta_quotient2,initial_lots):
    v=min(1/np.floor(prime_client['lots']/5),0.3)
    c_lots_track_temp=c_lots_track
    p_lots_track_temp=p_lots_track
    rosetta_quotient1_temp=rosetta_quotient1
    rosetta_quotient2_temp=rosetta_quotient2
    proj,C,P=rosetta_strikes(option_chain)
    decider=((proj-x)/dynamic_crossover)
    if decider>rosetta_quotient1 and p_lots_track>5 and p_lots_track<=c_lots_track:  
        p_data=option_chain[option_chain['CPType']=='PE']
        c_data=option_chain[option_chain['CPType']=='CE']
        p_scrip=int(p_data[p_data['StrikeRate']==p_striker]['ScripCode'])
        test_order = Order(order_type='B',exchange='N',exchange_segment='D', scrip_code =p_scrip , quantity=25*5, price=0 ,is_intraday=False,remote_order_id="tag")
        prime_client['login'].place_order(test_order)
        c_scrip=int(c_data[c_data['StrikeRate']==c_striker]['ScripCode'])
        test_order = Order(order_type='S',exchange='N',exchange_segment='D', scrip_code =c_scrip , quantity=25, price=0 ,is_intraday=False,remote_order_id="tag")
        status=prime_client['login'].place_order(test_order)
        p_lots_track_temp=p_lots_track-5
        rosetta_quotient1_temp=rosetta_quotient1+v/2
        if status['Message']=='Success':
            c_lots_track_temp=c_lots_track+1
    if decider>v/2 and p_lots_track>c_lots_track:  
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
        
        rosetta_quotient1_temp=v
        if status['Message']=='Success':
            c_lots_track_temp=initial_lots
        elif status['Message']!='Success':
            c_lots_track_temp=initial_lots
            com=initial_lots-c_lots_track
            shrink=round(prime_client['login'].margin()[0]['AvailableMargin']/180000)
            while shrink<=com:
                test_order_k1 = Order(order_type='S',exchange='N',exchange_segment='D', scrip_code =c_scrip , quantity=25*(shrink), price=0 ,is_intraday=False,remote_order_id="tag")
                prime_client['login'].place_order(test_order_k1)
                com=com-shrink
                sleep(5)
                shrink=round(prime_client['login'].margin()[0]['AvailableMargin']/180000)
            test_order_k1 = Order(order_type='S',exchange='N',exchange_segment='D', scrip_code =c_scrip , quantity=25*(com), price=0 ,is_intraday=False,remote_order_id="tag")
            prime_client['login'].place_order(test_order_k1)
    if decider<rosetta_quotient2 and c_lots_track>5 and p_lots_track>=c_lots_track:  
        p_data=option_chain[option_chain['CPType']=='PE']
        c_data=option_chain[option_chain['CPType']=='CE']
        c_scrip=int(c_data[c_data['StrikeRate']==c_striker]['ScripCode'])
        test_order = Order(order_type='B',exchange='N',exchange_segment='D', scrip_code =c_scrip , quantity=25*5, price=0 ,is_intraday=False,remote_order_id="tag")
        prime_client['login'].place_order(test_order)
        p_scrip=int(p_data[p_data['StrikeRate']==p_striker]['ScripCode'])
        test_order = Order(order_type='S',exchange='N',exchange_segment='D', scrip_code =p_scrip , quantity=25, price=0 ,is_intraday=False,remote_order_id="tag")
        status=prime_client['login'].place_order(test_order)
        c_lots_track_temp=c_lots_track-5
        rosetta_quotient2_temp=rosetta_quotient2-v/2
        if status['Message']=='Success':
            p_lots_track_temp=p_lots_track+1
            
    if decider<-v/2 and p_lots_track<c_lots_track:  
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
        rosetta_quotient2_temp=-v
        if status['Message']=='Success':
            p_lots_track_temp=initial_lots
        elif status['Message']!='Success':
            p_lots_track_temp=initial_lots
            com=initial_lots-p_lots_track
            shrink=round(prime_client['login'].margin()[0]['AvailableMargin']/180000)
            while shrink<=com:
                test_order_k1 = Order(order_type='S',exchange='N',exchange_segment='D', scrip_code =p_scrip , quantity=25*(shrink), price=0 ,is_intraday=False,remote_order_id="tag")
                prime_client['login'].place_order(test_order_k1)
                com=com-shrink
                sleep(5)
                shrink=round(prime_client['login'].margin()[0]['AvailableMargin']/180000)
            test_order_k1 = Order(order_type='S',exchange='N',exchange_segment='D', scrip_code =p_scrip , quantity=25*(com), price=0 ,is_intraday=False,remote_order_id="tag")
            prime_client['login'].place_order(test_order_k1)
    return p_lots_track_temp,c_lots_track_temp,rosetta_quotient1_temp,rosetta_quotient2_temp    


def decoy3(option_chain,c_striker,p_striker,prime_client,c_lots_track,p_lots_track,taken_trade,exclusive_strike,tron):
    if c_lots_track!=p_lots_track:
        c_data=option_chain[option_chain['CPType']=='CE']
        c_scrip=int(c_data[c_data['StrikeRate']==c_striker]['ScripCode'])
        test_order = Order(order_type='B',exchange='N',exchange_segment='D', scrip_code =c_scrip , quantity=25*c_lots_track, price=0 ,is_intraday=False,remote_order_id="tag")
        prime_client['login'].place_order(test_order)
        p_data=option_chain[option_chain['CPType']=='PE']
        p_scrip=int(p_data[p_data['StrikeRate']==p_striker]['ScripCode'])
        test_order = Order(order_type='B',exchange='N',exchange_segment='D', scrip_code =p_scrip , quantity=25*p_lots_track, price=0 ,is_intraday=False,remote_order_id="tag")
        prime_client['login'].place_order(test_order)
    if c_lots_track>p_lots_track:
        c_data=option_chain[option_chain['CPType']=='CE']
        c_scrip=int(c_data[c_data['StrikeRate']==c_striker+500]['ScripCode'])
        test_order = Order(order_type='S',exchange='N',exchange_segment='D', scrip_code =c_scrip , quantity=25*c_lots_track, price=0 ,is_intraday=False,remote_order_id="tag")
        prime_client['login'].place_order(test_order)
    if p_lots_track>c_lots_track:
        p_data=option_chain[option_chain['CPType']=='PE']
        p_scrip=int(p_data[p_data['StrikeRate']==p_striker-500]['ScripCode'])
        test_order = Order(order_type='S',exchange='N',exchange_segment='D', scrip_code =p_scrip , quantity=25*p_lots_track, price=0 ,is_intraday=False,remote_order_id="tag")
        prime_client['login'].place_order(test_order)
    if taken_trade==-1:
        p_data=option_chain[option_chain['CPType']=='PE']
        p_scrip=int(p_data[p_data['StrikeRate']==exclusive_strike]['ScripCode'])
        test_order = Order(order_type='S',exchange='N',exchange_segment='D', scrip_code =p_scrip, quantity=25*tron, price=0 ,is_intraday=False,remote_order_id="tag")
        prime_client['login'].place_order(test_order)
    elif taken_trade==1:
        c_data=option_chain[option_chain['CPType']=='CE']
        c_scrip=int(c_data[c_data['StrikeRate']==exclusive_strike]['ScripCode'])
        test_order = Order(order_type='S',exchange='N',exchange_segment='D', scrip_code =c_scrip, quantity=25*tron, price=0 ,is_intraday=False,remote_order_id="tag")
        prime_client['login'].place_order(test_order)
    return 0

def decoy4(option_chain,exclusive_strike,tron,taken_trade,del_to_deal):
    if del_to_deal>0.4 and local_div_factor!=0 and taken_trade==0:
        exclusive_strike=int(np.round(x/100)*100)
        c_data=option_chain[option_chain['CPType']=='CE']
        c_scrip=int(c_data[c_data['StrikeRate']==exclusive_strike]['ScripCode'])
        test_order = Order(order_type='B',exchange='N',exchange_segment='D', scrip_code =c_scrip, quantity=25*tron, price=0 ,is_intraday=False,remote_order_id="tag")
        prime_client['login'].place_order(test_order) 
        taken_trade=1
    elif del_to_deal<-0.4 and taken_trade==1:
        c_data=option_chain[option_chain['CPType']=='CE']
        c_scrip=int(c_data[c_data['StrikeRate']==exclusive_strike]['ScripCode'])
        test_order = Order(order_type='S',exchange='N',exchange_segment='D', scrip_code =c_scrip, quantity=25*tron, price=0 ,is_intraday=False,remote_order_id="tag")
        prime_client['login'].place_order(test_order)
        taken_trade=0
    if del_to_deal<-0.4 and local_div_factor!=0 and taken_trade==0:
        exclusive_strike=int(np.round(x/100)*100)
        p_data=option_chain[option_chain['CPType']=='PE']
        p_scrip=int(p_data[p_data['StrikeRate']==exclusive_strike]['ScripCode'])
        test_order = Order(order_type='B',exchange='N',exchange_segment='D', scrip_code =p_scrip, quantity=25*tron, price=0 ,is_intraday=False,remote_order_id="tag")
        prime_client['login'].place_order(test_order) 
        taken_trade=-1
    elif del_to_deal>0.4 and taken_trade==-1:
        p_data=option_chain[option_chain['CPType']=='PE']
        p_scrip=int(p_data[p_data['StrikeRate']==exclusive_strike]['ScripCode'])
        test_order = Order(order_type='S',exchange='N',exchange_segment='D', scrip_code =p_scrip, quantity=25*tron, price=0 ,is_intraday=False,remote_order_id="tag")
        prime_client['login'].place_order(test_order)
        taken_trade=0
    return taken_trade,exclusive_strike
#%%
'''ind_time = datetime.now(timezone("Asia/Kolkata")).strftime('%Y-%m-%d %H:%M:%S.%f')'''
'''while int(ind_time[11:13])*60+int(ind_time[14:16])<561 or int(ind_time[11:13])*60+int(ind_time[14:16])>885 :'''
'''    ind_time = datetime.now(timezone("Asia/Kolkata")).strftime('%Y-%m-%d %H:%M:%S.%f')'''
#%%
prime_client=client_login(client=client_name)
expiry_timestamps=prime_client['login'].get_expiry("N","BANKNIFTY").copy()
current_expiry_time_stamp_weekly=int(expiry_timestamps['Expiry'][0]['ExpiryDate'][6:19])
option_chain=pd.DataFrame(prime_client['login'].get_option_chain("N","BANKNIFTY",current_expiry_time_stamp_weekly)['Options'])
proj,c_striker,p_striker=rosetta_strikes(option_chain)
c_data=option_chain[option_chain['CPType']=='CE']
p_data=option_chain[option_chain['CPType']=='PE']
c_scrip=int(c_data[c_data['StrikeRate']==c_striker]['ScripCode'])
p_scrip=int(p_data[p_data['StrikeRate']==p_striker]['ScripCode'])
test_order = Order(order_type='S',exchange='N',exchange_segment='D', scrip_code =p_scrip , quantity=25*prime_client['lots'], price=0 ,is_intraday=False,remote_order_id="tag")
status = prime_client['login'].place_order(test_order)
test_order = Order(order_type='S',exchange='N',exchange_segment='D', scrip_code =c_scrip , quantity=25*prime_client['lots'], price=0 ,is_intraday=False,remote_order_id="tag")
status = prime_client['login'].place_order(test_order)
rosetta_quotient1=min(1/np.floor(prime_client['lots']/5),0.25)
rosetta_quotient2=-min(1/np.floor(prime_client['lots']/5),0.25)
c_lots_track=prime_client['lots']
p_lots_track=prime_client['lots']
initial_lots=prime_client['lots']
option_chain_store=option_chain
indicator=[]
b_lastrate=[]
diverge=[]
l_diverge=[]
inst_diverge=[]
to_deal=[]
exclusive_strike=0
taken_trade=0
del_to_deal=0
ricker=0
e_ce,e_pe,i_ce,i_pe=0,0,0,0
while True:
    re=[{"Exch":"N","ExchType":"C","Symbol":"BANKNIFTY","Scripcode":"999920005","OptionType":"EQ"}]          
    aa=prime_client['login'].fetch_market_feed(re)
    x=aa['Data'][0]['LastRate']
    while True:
        try :
            expiry_timestamps=prime_client['login'].get_expiry("N","BANKNIFTY").copy()
            current_expiry_time_stamp_weekly=int(expiry_timestamps['Expiry'][0]['ExpiryDate'][6:19])
            option_chain=pd.DataFrame(prime_client['login'].get_option_chain("N","BANKNIFTY",current_expiry_time_stamp_weekly)['Options'])
            break
        except Exception :
            pass
    proj,Cyi,Phf=rosetta_strikes(option_chain)
    project_k=(x-proj)
    print('Niftybank:  ',project_k)
    ind_time = datetime.now(timezone("Asia/Kolkata")).strftime('%Y-%m-%d %H:%M:%S.%f')
    c_data=option_chain[option_chain['CPType']=='CE']
    p_data=option_chain[option_chain['CPType']=='PE']
    try:
        c_data_store=option_chain_store[option_chain_store['CPType']=='CE']
        p_data_store=option_chain_store[option_chain_store['CPType']=='PE']
        c_delta_O=np.array(c_data['OpenInterest']-c_data_store['OpenInterest'])
        p_delta_O=np.array(p_data['OpenInterest']-p_data_store['OpenInterest'])
        vin,s1,s2, e_ce,e_pe,i_ce,i_pe=smart_ass(option_chain,c_delta_O,p_delta_O,e_ce,e_pe,i_ce,i_pe,ricker)
        print('vinays_best_work',x-vin)
    except Exception:
        pass
    c1=int(c_data[c_data['StrikeRate']==int(np.floor(x/100)*100)]['LastRate'])
    c2=int(c_data[c_data['StrikeRate']==int(np.ceil(x/100)*100)]['LastRate'])
    p1=int(p_data[p_data['StrikeRate']==int(np.floor(x/100)*100)]['LastRate'])
    p2=int(p_data[p_data['StrikeRate']==int(np.ceil(x/100)*100)]['LastRate'])
    dynamic_crossover=(c1+c2+p1+p2)/4
    delta=(c1-c2+p2-p1)/200
    indicator,b_lastrate,div_factor,local_div_factor,instant_div_factor=past_picture(indicator,project_k,b_lastrate,x,delta)
    print('total divergence :',div_factor)
    print('local divergence :',local_div_factor)
    print('instant divergence :',instant_div_factor)
    
    c_striker,p_striker = decoy1(option_chain,c_striker,p_striker,dynamic_crossover,prime_client,c_lots_track,p_lots_track)
    p_lots_track,c_lots_track,rosetta_quotient1,rosetta_quotient2=decoy2(x,option_chain,c_striker,p_striker,dynamic_crossover,prime_client,c_lots_track,p_lots_track,rosetta_quotient1,rosetta_quotient2,initial_lots)
    diverge=diverge+[div_factor]
    l_diverge=l_diverge+[local_div_factor]
    inst_diverge=inst_diverge+[instant_div_factor]
    to_deal=to_deal+[instant_div_factor-local_div_factor]
    if len(to_deal)>2:
        del_to_deal=to_deal[-1]-to_deal[-2]
        print('new_indicator',del_to_deal)
        print('')
    if tron>0 and del_to_deal!=0:
        taken_trade,exclusive_strike=decoy4(option_chain,exclusive_strike,tron,taken_trade, del_to_deal)
    if int(ind_time[11:13])*60+int(ind_time[14:16])>913 :
        decoy3(option_chain,c_striker,p_striker,prime_client,c_lots_track,p_lots_track,taken_trade,exclusive_strike,tron)
        break
    option_chain_store=option_chain
    ricker=1
    sleep(2)

fig, ax_left = plt.subplots()
ax_right = ax_left.twinx()
ax_left.plot(b_lastrate, color='blue')
ax_right.plot(diverge, color='red')
ax_right.plot(l_diverge, color='white')
ax_right.plot(inst_diverge, color='orange')

#%%
k=-np.array(l_diverge)+np.array(inst_diverge)
iso=[]
for i in range(1,len(k)):
    iso=iso+[k[i]-k[i-1]]
iso=[0]+iso
profit=0
loss=0
c1=0
c2=0
pair1=[]
pair2=[]
number_of_trades=0
for iter in range(200,len(iso)):
    if iso[iter]>0.4 and c1==0 :
        pair1=pair1+[b_lastrate[iter]]
        c1=1
    if iso[iter]<-0.4 and c2==0 :
        pair2=pair2+[b_lastrate[iter]]
        c2=1
    if c1==1 and iso[iter]<-0.4  :
        pair1=pair1+[b_lastrate[iter]]
        c1=0
    if c2==1 and iso[iter]>0.4  :
        pair2=pair2+[b_lastrate[iter]]
        c2=0
    if len(pair1)==2:
        if pair1[1]-pair1[0]>0:
            profit=profit+pair1[1]-pair1[0]
        else:
            loss=loss+pair1[1]-pair1[0]
        pair1=[]
        number_of_trades=number_of_trades+1
    if len(pair2)==2:
        if pair2[1]-pair2[0]<0:
            profit=profit+pair2[0]-pair2[1]
        else:
            loss=loss-(pair2[1]-pair2[0])
            print(pair2)
        pair2=[]
        number_of_trades=number_of_trades+1
print('total profit',profit)
print('number of trades',number_of_trades)
print('profit per trade',(profit+loss)/number_of_trades)
print('loss',loss)
print('success ratio',-profit/loss)
# %%
