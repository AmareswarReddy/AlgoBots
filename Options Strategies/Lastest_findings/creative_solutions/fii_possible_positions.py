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
from scipy.interpolate import interp1d
from itertools import permutations
import random




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
    client_list[client]['strategy']=0
    client_list[client]['login']=FivePaisaClient(email=user, passwd=passw, dob=dob,cred=vinathi_cred)
    client_list[client]['login'].login()
    client_list[client]['lots']=round((client_list[client]['login'].margin()[0]['AvailableMargin']-200000)/180000)
    return client_list[client]
#client_name=input('enter the client name Eg: vinathi,bhaskar '

def order_button(exclusive_strike,type,lots):
    sleep(2)
    exchange='BANKNIFTY'
    lot_size=25
    max_lots_per_order=36
    strike_difference=100
    if exclusive_strike==0:
        while True:
            try :
                expiry_timestamps=prime_client['login'].get_expiry("N",exchange).copy()
                current_expiry_time_stamp_weekly=int(expiry_timestamps['Expiry'][0]['ExpiryDate'][6:19])
                option_chain=pd.DataFrame(prime_client['login'].get_option_chain("N",exchange,current_expiry_time_stamp_weekly)['Options'])
                x=expiry_timestamps['lastrate'][0]['LTP']
                break
            except Exception :
                pass
        exclusive_strike=int(np.round(x/strike_difference)*strike_difference)
    else:
        while True:
            try :
                expiry_timestamps=prime_client['login'].get_expiry("N",exchange).copy()
                current_expiry_time_stamp_weekly=int(expiry_timestamps['Expiry'][0]['ExpiryDate'][6:19])
                option_chain=pd.DataFrame(prime_client['login'].get_option_chain("N",exchange,current_expiry_time_stamp_weekly)['Options'])
                x=expiry_timestamps['lastrate'][0]['LTP']
                break
            except Exception :
                pass
    if type=='CE_B':
        already_placed=0
        c_data=option_chain[option_chain['CPType']=='CE']
        c_scrip=int(c_data[c_data['StrikeRate']==exclusive_strike]['ScripCode'])
        temp2=lots
        temp=int(temp2/max_lots_per_order)
        end=temp2-temp*max_lots_per_order
        test_order = Order(order_type='B',exchange='N',exchange_segment='D', scrip_code =c_scrip, quantity=lot_size*max_lots_per_order, price=0 ,is_intraday=False,remote_order_id="tag")
        while temp>0:
            status=prime_client['login'].place_order(test_order)
            temp=temp-1 
            if status['Message']=='Success':
                already_placed+=max_lots_per_order
            sleep(0.5)
        if temp==0 and end!=0:
            test_order = Order(order_type='B',exchange='N',exchange_segment='D', scrip_code =c_scrip, quantity=lot_size*end, price=0 ,is_intraday=False,remote_order_id="tag")
            status=prime_client['login'].place_order(test_order)
            if status['Message']=='Success':
                already_placed+=end
        yet_to_place=lots-already_placed 
    if type=='PE_B':
        already_placed=0
        p_data=option_chain[option_chain['CPType']=='PE']
        p_scrip=int(p_data[p_data['StrikeRate']==exclusive_strike]['ScripCode'])
        temp2=lots
        temp=int(temp2/max_lots_per_order)
        end=temp2-temp*max_lots_per_order
        test_order = Order(order_type='B',exchange='N',exchange_segment='D', scrip_code =p_scrip, quantity=lot_size*max_lots_per_order, price=0 ,is_intraday=False,remote_order_id="tag")
        while temp>0:
            status=prime_client['login'].place_order(test_order) 
            temp=temp-1
            if status['Message']=='Success':
                already_placed+=max_lots_per_order
            sleep(0.5)
        if temp==0 and end!=0:
            test_order = Order(order_type='B',exchange='N',exchange_segment='D', scrip_code =p_scrip, quantity=lot_size*end, price=0 ,is_intraday=False,remote_order_id="tag")
            status=prime_client['login'].place_order(test_order) 
            if status['Message']=='Success':
                already_placed+=end
        yet_to_place=lots-already_placed
    if type=='CE_S':
        already_placed=0
        c_data=option_chain[option_chain['CPType']=='CE']
        c_scrip=int(c_data[c_data['StrikeRate']==exclusive_strike]['ScripCode'])
        temp2=lots
        temp=int(temp2/max_lots_per_order)
        end=temp2-temp*max_lots_per_order
        test_order = Order(order_type='S',exchange='N',exchange_segment='D', scrip_code =c_scrip, quantity=lot_size*max_lots_per_order, price=0 ,is_intraday=False,remote_order_id="tag")
        while temp>0:
            status=prime_client['login'].place_order(test_order) 
            temp=temp-1
            if status['Message']=='Success':
                already_placed+=max_lots_per_order
            sleep(0.5)
        if temp==0 and end!=0:
            test_order = Order(order_type='S',exchange='N',exchange_segment='D', scrip_code =c_scrip, quantity=lot_size*end, price=0 ,is_intraday=False,remote_order_id="tag")
            status=prime_client['login'].place_order(test_order) 
            if status['Message']=='Success':
                already_placed+=end
        yet_to_place=lots-already_placed
    if type=='PE_S':
        already_placed=0
        p_data=option_chain[option_chain['CPType']=='PE']
        p_scrip=int(p_data[p_data['StrikeRate']==exclusive_strike]['ScripCode'])
        temp2=lots
        temp=int(temp2/max_lots_per_order)
        end=temp2-temp*max_lots_per_order
        test_order = Order(order_type='S',exchange='N',exchange_segment='D', scrip_code =p_scrip, quantity=lot_size*max_lots_per_order, price=0 ,is_intraday=False,remote_order_id="tag")
        while temp>0:
            status=prime_client['login'].place_order(test_order) 
            temp=temp-1
            if status['Message']=='Success':
                already_placed+=max_lots_per_order
            sleep(0.5)
        if temp==0 and end!=0:
            test_order = Order(order_type='S',exchange='N',exchange_segment='D', scrip_code =p_scrip, quantity=lot_size*end, price=0 ,is_intraday=False,remote_order_id="tag")
            status=prime_client['login'].place_order(test_order) 
            if status['Message']=='Success':
                already_placed+=end
        yet_to_place=lots-already_placed
    return exclusive_strike,yet_to_place

def lots_drop(strike,side,yet_to_place):
    k=yet_to_place
    while yet_to_place>0:
        sleep(1)
        yet_to_place-=1
        xx,pending=order_button(strike,side,yet_to_place)
        if pending==0:
            break
    return k-yet_to_place

def data(week):
    exchange='NIFTY'
    while True:
        try :
            expiry_timestamps=prime_client['login'].get_expiry("N",exchange).copy()
            current_expiry_time_stamp_weekly=int(expiry_timestamps['Expiry'][week]['ExpiryDate'][6:19])
            option_chain=pd.DataFrame(prime_client['login'].get_option_chain("N",exchange,current_expiry_time_stamp_weekly)['Options'])
            x=expiry_timestamps['lastrate'][0]['LTP']
            break
        except Exception :
            pass
    return option_chain,x


def add_position(positions,strike,type,lots):
    positions[len(positions)]=[strike,type,lots]
    return positions

def y_axis(x,single_position,option_chain):
    if single_position[1]=='CE_B':
        k=x-single_position[0]
        k[k<0]=0
        lastrate=float(option_chain[(option_chain['StrikeRate']==single_position[0]) & (option_chain['CPType']=='CE')]['LastRate'])
        y=single_position[2]*(k-lastrate)

    if single_position[1]=='CE_S':
        k=single_position[0]-x
        k[k>0]=0
        lastrate=float(option_chain[(option_chain['StrikeRate']==single_position[0]) & (option_chain['CPType']=='CE')]['LastRate'])
        y=single_position[2]*(k+lastrate)

    if single_position[1]=='PE_B':
        k=single_position[0]-x
        k[k<0]=0
        lastrate=float(option_chain[(option_chain['StrikeRate']==single_position[0]) & (option_chain['CPType']=='PE')]['LastRate'])
        y=single_position[2]*(k-lastrate)
    if single_position[1]=='PE_S':
        k=x-single_position[0]
        k[k>0]=0
        lastrate=float(option_chain[(option_chain['StrikeRate']==single_position[0]) & (option_chain['CPType']=='PE')]['LastRate'])
        y=single_position[2]*(k+lastrate)
    return y


def pnl_graph_N(call_positions,put_positions,option_chain):
    try:
        k1=pd.DataFrame(call_positions)
        k2=pd.DataFrame(put_positions)
        a1=np.array(k1.iloc[0])
        a2=np.array(k2.iloc[0])
        x1=np.linspace(min(a1)-150,max(a1)+150,int((max(a1)-min(a1)+300)/50)+1)
        y1=np.zeros(len(x1))
        for i in range(0,len(call_positions)):
            y1+=np.array(y_axis(x1,call_positions[i],option_chain))  
        for j in range(0,len(put_positions)):
            y1+=np.array(y_axis(x1,put_positions[j],option_chain))
    except Exception:
        x1=[0]
        y1=[0]
    return x1,y1

#%%
#variables to be initialised
client_name = input('enter the client name: ')
prime_client=client_login(client=client_name)
option_chain,x=data(week=0)





# %%
call_net_long=723239
call_net_short=492944
put_net_long=969561
put_net_short=628940
def call_side_positions(option_chain,call_net_long,call_net_short):
    call_net_long=int(call_net_long*50)
    call_net_short=int(call_net_short*50)
    c_data=option_chain[option_chain['CPType']=='CE']
    strikes=np.array(c_data['StrikeRate'])
    ois=np.array(c_data['OpenInterest'])
    lastrates=np.array(c_data['LastRate'])
    long_call_oi_distributer=[]
    for oi in ois:
        if oi<call_net_long:
            long_call_oi_distributer+=[oi]
            call_net_long-=oi
        elif oi>=call_net_long:
            long_call_oi_distributer+=[call_net_long]
            call_net_long=0

    short_call_oi_distributer=[]
    for o in range(0,len(ois)):
        oi=ois[len(ois)-o-1]
        if oi<call_net_short:
            short_call_oi_distributer=[oi]+short_call_oi_distributer
            call_net_short-=oi
        elif oi>=call_net_short:
            short_call_oi_distributer=[call_net_short]+short_call_oi_distributer
            call_net_short=0

    nifty_positions={}
    for i in range(0,len(long_call_oi_distributer)):
        nifty_positions=add_position(nifty_positions,strikes[i],'CE_B',long_call_oi_distributer[i])
    for i in range(0,len(short_call_oi_distributer)):
        nifty_positions=add_position(nifty_positions,strikes[i],'CE_S',short_call_oi_distributer[i])
    return nifty_positions


def get_break_evens(x,y):
    k=[]
    if len(y)>2:
        for i in range(1,len(y)):
            if np.sign(y[i-1])!=np.sign(y[i]):
                f=interp1d([y[i-1],y[i]],[x[i-1],x[i]])
                k+=[f(0)]
    return np.array(k)

def put_side_positions(option_chain,put_net_long,put_net_short):
    put_net_long=int(put_net_long*50)
    put_net_short=int(put_net_short*50)
    p_data=option_chain[option_chain['CPType']=='PE']
    strikes=np.array(p_data['StrikeRate'])
    ois=np.array(p_data['OpenInterest'])
    lastrates=np.array(p_data['LastRate'])
    short_put_oi_distributer=[]
    for oi in ois:
        if oi<put_net_short:
            short_put_oi_distributer+=[oi]
            put_net_short-=oi
        elif oi>=put_net_short:
            short_put_oi_distributer+=[put_net_short]
            put_net_short=0

    long_put_oi_distributer=[]
    for o in range(0,len(ois)):
        oi=ois[len(ois)-o-1]
        if oi<put_net_long:
            long_put_oi_distributer=[oi]+long_put_oi_distributer
            put_net_long-=oi
        elif oi>=put_net_long:
            long_put_oi_distributer=[put_net_long]+long_put_oi_distributer
            put_net_long=0

    nifty_positions={}
    for i in range(0,len(long_put_oi_distributer)):
        nifty_positions=add_position(nifty_positions,strikes[i],'PE_B',long_put_oi_distributer[i])
    for i in range(0,len(short_put_oi_distributer)):
        nifty_positions=add_position(nifty_positions,strikes[i],'PE_S',short_put_oi_distributer[i])
    return nifty_positions
call_positions=call_side_positions(option_chain,call_net_long,call_net_short)
put_positions=put_side_positions(option_chain,put_net_long,put_net_short)
x,y=pnl_graph_N(call_positions,put_positions,option_chain)
breakevens=get_break_evens(x,y)
plt.plot(x,y)
print('breakevens : ',breakevens)
#%%
def sums(length, total_sum):
    if length == 1:
        yield (total_sum,)
    else:
        for value in range(total_sum + 1):
            for permutation in sums(length - 1, total_sum - value):
                yield (value,) + permutation

#%%
def random_distributer(option_chain,net_oi,side):
    if side==1:
        c_data=option_chain[option_chain['CPType']=='CE']
        strikes=np.array(c_data['StrikeRate'])
        ois=np.array(c_data['OpenInterest'])
        while True:
            random_ois=np.array(sums(len(ois),net_oi))
            if np.all(ois>=random_ois)==True:
                break
        return list(random_ois),strikes

    if side==-1:
        p_data=option_chain[option_chain['CPType']=='PE']
        strikes=np.array(p_data['StrikeRate'])
        ois=np.array(p_data['OpenInterest'])
        while True:
            random_ois=np.array(sums(len(ois),net_oi))
            if np.all(ois>=random_ois)==True:
                break
        return list(random_ois),strikes



def call_side_oi_distributer(option_chain,call_net_long,call_net_short):
    call_net_long=int(call_net_long*50)
    call_net_short=int(call_net_short*50)
    long_call_oi_distributer,strikes=random_distributer(option_chain,call_net_long,1)

    short_call_oi_distributer,strikes=random_distributer(option_chain,call_net_short,1)

    nifty_positions={}
    for i in range(0,len(long_call_oi_distributer)):
        nifty_positions=add_position(nifty_positions,strikes[i],'CE_B',long_call_oi_distributer[i])
    for i in range(0,len(short_call_oi_distributer)):
        nifty_positions=add_position(nifty_positions,strikes[i],'CE_S',short_call_oi_distributer[i])
    return nifty_positions


def put_side_oi_distributer(option_chain,call_net_long,call_net_short):
    call_net_long=int(call_net_long*50)
    call_net_short=int(call_net_short*50)
    long_call_oi_distributer,strikes=random_distributer(option_chain,call_net_long,1)

    short_call_oi_distributer,strikes=random_distributer(option_chain,call_net_short,1)

    nifty_positions={}
    for i in range(0,len(long_call_oi_distributer)):
        nifty_positions=add_position(nifty_positions,strikes[i],'CE_B',long_call_oi_distributer[i])
    for i in range(0,len(short_call_oi_distributer)):
        nifty_positions=add_position(nifty_positions,strikes[i],'CE_S',short_call_oi_distributer[i])
    return nifty_positions


def lobes(x,y):
    max_profit=max(y)

    return max_profit,lobe,center

def max_profit_and_lobe():
    while True:
        call_positions=call_side_positions(option_chain,call_net_long,call_net_short)
        put_positions=put_side_positions(option_chain,put_net_long,put_net_short)
        x,y=pnl_graph_N(call_positions,put_positions,option_chain)
        final,lobe,center=lobes(x,y)

    return final,lobe


profit_final=0
no_change_iter=0
while True:
    profit,lobe,center=max_profit_and_lobe()
    if profit>profit_final:
        profit_final=profit
        no_change_iter=0
    else:
        no_change_iter+=1
    if no_change_iter>100:
        break
plt.plot(x,y)
breakevens=get_break_evens(x,y)
print('breakevens : ',breakevens)

# %%
