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
from pyswarm import pso
from itertools import permutations
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
#client_name=input('enter the client name Eg: vinathi,bhaskar '
def data(week):
    exchange='BANKNIFTY'
    while True:
        expiry_timestamps=prime_client['login'].get_expiry("N",exchange).copy()
        current_expiry_time_stamp_weekly=int(expiry_timestamps['Expiry'][week]['ExpiryDate'][6:19])
        try :
            expiry_timestamps=prime_client['login'].get_expiry("N",exchange).copy()
            option_chain=pd.DataFrame(prime_client['login'].get_option_chain("N",exchange,current_expiry_time_stamp_weekly)['Options'])
            x=expiry_timestamps['lastrate'][0]['LTP']
            break
        except Exception :
            pass
    return option_chain,x

def dataN(week):
    exchange='NIFTY'
    while True:
        expiry_timestamps=prime_client['login'].get_expiry("N",exchange).copy()
        current_expiry_time_stamp_weekly=int(expiry_timestamps['Expiry'][week]['ExpiryDate'][6:19])
        try :
            expiry_timestamps=prime_client['login'].get_expiry("N",exchange).copy()
            option_chain=pd.DataFrame(prime_client['login'].get_option_chain("N",exchange,current_expiry_time_stamp_weekly)['Options'])
            x=expiry_timestamps['lastrate'][0]['LTP']
            break
        except Exception :
            pass
    return option_chain,x

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

def order_buttonN(exclusive_strike,type,lots):
    sleep(2)
    exchange='NIFTY'
    lot_size=50
    max_lots_per_order=36
    strike_difference=50
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

def finalise_tron(p_strike,c_strike,tron):
    p_strike,p_yet_to_place=order_button(p_strike,'PE_S',tron)
    c_strike,c_yet_to_place=order_button(c_strike,'CE_S',tron)
    if p_yet_to_place==0 and c_yet_to_place==0:
        return tron
    if p_yet_to_place!=0 and c_yet_to_place==0:
        while True:
            tron=tron-1
            order_button(c_strike,'CE_B',1)
            kkk,y_place=order_button(p_strike,'PE_S',tron)
            if y_place==0:
                break
        return tron
    if p_yet_to_place==0 and c_yet_to_place!=0:
        while True:
            tron=tron-1
            order_button(p_strike,'PE_B',1)
            kkk,y_place=order_button(c_strike,'CE_S',tron)
            if y_place==0:
                break
        return tron
    if p_yet_to_place!=0 and c_yet_to_place!=0:
        return finalise_tron(p_strike=p_strike,c_strike=c_strike,tron=tron-1)

def initial_leg_trades(option_chain,x,tron):
    exclusive_strike=int(np.round((x)/100)*100)
    ce_data=option_chain[option_chain['CPType']=='CE']
    pe_data=option_chain[option_chain['CPType']=='PE']
    c_e_lastrate=int(ce_data[ce_data['StrikeRate']==exclusive_strike]['LastRate'])
    p_e_lastrate=int(pe_data[pe_data['StrikeRate']==exclusive_strike]['LastRate'])
    cp_sum=c_e_lastrate+p_e_lastrate
    f=int(np.ceil((cp_sum)/100)*100)
    while True:
        p_strike_b,yet_to_place=order_button(exclusive_strike-f,'PE_B',tron)
        if yet_to_place==0:
            break
    while True:
        c_strike_b,yet_to_place=order_button(exclusive_strike+f,'CE_B',tron)
        if yet_to_place==0:
            break
    c_strike=exclusive_strike
    p_strike=exclusive_strike
    tron=finalise_tron(p_strike=p_strike,c_strike=c_strike,tron=tron)
    return tron,c_strike,p_strike,c_strike_b,p_strike_b


def Thursday_beast(x,c_strike,p_strike,c_strike_b,p_strike_b,tron):
    c_strike_new,p_strike_new=0,0
    if x-c_strike_b>66:
        c,a=order_button(c_strike_b+100,'CE_B',tron)
        o,a=order_button(c_strike_b,'CE_S',tron)
        c_strike_b=c
    if p_strike_b-x>66:
        p,a=order_button(p_strike_b-100,'PE_B',tron)
        o,a=order_button(p_strike_b,'PE_S',tron)
        p_strike_b=p
    if c_strike<=p_strike:
        if c_strike-x>50:
            o,y=order_button(c_strike,'CE_B',tron)
            while y!=0:
                strike,y=order_button(c_strike,'CE_B',tron)
            c_strike_new,y1=order_button(c_strike-100,'CE_S',tron)
            for i in range(0,5):
                y1=lots_drop(c_strike,'CE_S',y1)
            if y1!=0:
                tron-=y1
                order_button(p_strike,'PE_B',y1)

        if x-p_strike>50:   
            o,y=order_button(p_strike,'PE_B',tron)
            while y!=0:
                strike,y=order_button(p_strike,'PE_B',tron)
            p_strike_new,y1=order_button(p_strike+100,'PE_S',tron)
            for i in range(0,5):
                y1=lots_drop(p_strike,'PE_S',y1)
            if y1!=0:
                tron-=y1
                order_button(c_strike,'CE_B',y1)
    p_strike_new=p_strike*(p_strike_new==0)+p_strike_new
    c_strike_new=c_strike*(c_strike_new==0)+c_strike_new
    return c_strike,p_strike,c_strike_b,p_strike_b,tron

def get_strike_from_scrip(scripcode,exchange):
    if exchange=='BANKNIFTY':
        option_chain,a1=data(0)
    if exchange=='NIFTY':
        option_chain,a1=dataN(0)
    k1=option_chain[option_chain['ScripCode']==scripcode]
    return int(k1['StrikeRate'])

def clear_open_positions():

    S=pd.DataFrame(prime_client['login'].positions())
    if len(S[S['NetQty']!=0])!=0:
        for i in range(0,len(S)):
            if ('NIFTY' in S['ScripName'].iloc[i]) and S['NetQty'].iloc[i]!=0 and ('BANKNIFTY' not in S['ScripName'].iloc[i]):
                if S['NetQty'].iloc[i]<0 and ('PE' in S['ScripName'].iloc[i]):
                    order_buttonN(get_strike_from_scrip(S['ScripCode'].iloc[i],'NIFTY'),'PE_B',int(abs(S['NetQty'].iloc[i])/50))
                elif S['NetQty'].iloc[i]<0 and ('CE' in S['ScripName'].iloc[i]):
                    order_buttonN(get_strike_from_scrip(S['ScripCode'].iloc[i],'NIFTY'),'CE_B',int(abs(S['NetQty'].iloc[i])/50))
                elif S['NetQty'].iloc[i]>0 and ('CE' in S['ScripName'].iloc[i]):
                    order_buttonN(get_strike_from_scrip(S['ScripCode'].iloc[i],'NIFTY'),'CE_S',int(abs(S['NetQty'].iloc[i])/50))
                elif S['NetQty'].iloc[i]>0 and ('PE' in S['ScripName'].iloc[i]):
                    order_buttonN(get_strike_from_scrip(S['ScripCode'].iloc[i],'NIFTY'),'PE_S',int(abs(S['NetQty'].iloc[i])/50))

            elif ('BANKNIFTY' in S['ScripName'].iloc[i]) and S['NetQty'].iloc[i]!=0:
                if S['NetQty'].iloc[i]<0 and ('PE' in S['ScripName'].iloc[i]):
                    order_button(get_strike_from_scrip(S['ScripCode'].iloc[i],'BANKNIFTY'),'PE_B',int(abs(S['NetQty'].iloc[i])/25))
                elif S['NetQty'].iloc[i]<0 and ('CE' in S['ScripName'].iloc[i]):
                    order_button(get_strike_from_scrip(S['ScripCode'].iloc[i],'BANKNIFTY'),'CE_B',int(abs(S['NetQty'].iloc[i])/25))
                elif S['NetQty'].iloc[i]>0 and ('CE' in S['ScripName'].iloc[i]):
                    order_button(get_strike_from_scrip(S['ScripCode'].iloc[i],'BANKNIFTY'),'CE_S',int(abs(S['NetQty'].iloc[i])/25))
                elif S['NetQty'].iloc[i]>0 and ('PE' in S['ScripName'].iloc[i]):
                    order_button(get_strike_from_scrip(S['ScripCode'].iloc[i],'BANKNIFTY'),'PE_S',int(abs(S['NetQty'].iloc[i])/25))
        S=pd.DataFrame(prime_client['login'].positions())
        if len(S[S['NetQty']!=0])!=0:
            return clear_open_positions()
        elif len(S[S['NetQty']!=0])==0:
            return 0
    elif len(S[S['NetQty']!=0])==0:
        return 0

#%%
#variables to be initialised
client_name = input('enter the client name: ')
prime_client=client_login(client=client_name)
option_chain,x=data(week=0)
#%%
option_chain,x=data(week=0)
exclusive_strike,c_strike,p_strike=0,0,0
start=int(input('enter 0 if starting the strategy for the first time: '))
if start==0:
    tron=int(input('enter the number of lots: '))
    ind_time = datetime.now(timezone("Asia/Kolkata")).strftime('%Y-%m-%d %H:%M:%S.%f')
    while int(ind_time[11:13])*60+int(ind_time[14:16])<556 or int(ind_time[11:13])*60+int(ind_time[14:16])>1085 :
        ind_time = datetime.now(timezone("Asia/Kolkata")).strftime('%Y-%m-%d %H:%M:%S.%f')
    clear_open_positions()
    tron,c_strike,p_strike,c_strike_b,p_strike_b=initial_leg_trades(option_chain,x,tron)

if start==1:
    f = open (client_name+'_beast.json', "r")
    positions_json = json.loads(f.read())
    ind_time = datetime.now(timezone("Asia/Kolkata")).strftime('%Y-%m-%d %H:%M:%S.%f')
    while int(ind_time[11:13])*60+int(ind_time[14:16])<556 or int(ind_time[11:13])*60+int(ind_time[14:16])>1085 :
        ind_time = datetime.now(timezone("Asia/Kolkata")).strftime('%Y-%m-%d %H:%M:%S.%f')
    tron,c_strike,p_strike,c_strike_b,p_strike_b=positions_json['tron'],positions_json['c_strike'],positions_json['p_strike'],positions_json['c_strike_b'],positions_json['p_strike_b']

while int(ind_time[11:13])*60+int(ind_time[14:16])<930 :
    option_chain,x=data(week=0)
    c_strike,p_strike,c_strike_b,p_strike_b,tron=Thursday_beast(x,c_strike,p_strike,c_strike_b,p_strike_b,tron)
positions_json={'c_strike':c_strike,'p_strike':p_strike,'c_strike_b':c_strike_b,'p_strike_b':p_strike_b,'tron':tron}
out_file = open(client_name+'_beast.json', "w")
json.dump(positions_json, out_file, indent = 6)
out_file.close()