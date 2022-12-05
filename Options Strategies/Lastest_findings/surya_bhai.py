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
#client_name=input('enter the client name Eg: vinathi,bhaskar '

def order_button(exclusive_strike,type,lots):
    sleep(0.5)
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

def initial_strangle_trades(option_chain,x,tron):
    exclusive_strike=int(np.round((x)/100)*100)
    f=np.sum(option_chain[option_chain['StrikeRate']==int(np.round(x/100)*100)]['LastRate'])
    factor=float(1.6+1.1*np.random.rand(1)/2)*int(np.ceil(f/100)*100)
    factor=int(np.round((factor)/100)*100)
    c_strike=exclusive_strike+factor
    p_strike=exclusive_strike-factor
    tron=finalise_tron(p_strike=p_strike,c_strike=c_strike,tron=tron)
    return tron,c_strike,p_strike

def strangle_adjustments(x,exclusive_strike,c_strike,p_strike,tron):
    if c_strike!=p_strike:
        ce_data=option_chain[option_chain['CPType']=='CE']
        pe_data=option_chain[option_chain['CPType']=='PE']
        c_lastrate=int(ce_data[ce_data['StrikeRate']==c_strike]['LastRate'])
        p_lastrate=int(pe_data[pe_data['StrikeRate']==p_strike]['LastRate'])
        at_strike=int(np.round((x)/100)*100)
        if c_lastrate/p_lastrate>2.13 and (2*at_strike-c_strike)>p_strike :
            while True:
                strike,yet_to_place=order_button(p_strike,'PE_B',tron)
                if yet_to_place==0:
                    break
            p_strike,yet_to_place=order_button(2*at_strike-c_strike,'PE_S',tron)
            while True:
                if yet_to_place!=0:
                    tron=tron-1
                    while True:
                        strike,y=order_button(c_strike,'CE_B',1)
                        if y==0:
                            break
                    sleep(1)
                    p_strike,yet_to_place=order_button(2*at_strike-c_strike,'PE_S',tron)
                if yet_to_place==0:
                    break
            exclusive_strike=(c_strike==p_strike)*c_strike
        if p_lastrate/c_lastrate>2.13 and (2*at_strike-p_strike)<c_strike:
            while True:
                strike,yet_to_place=order_button(c_strike,'CE_B',tron)
                if yet_to_place==0:
                    break
            at_strike=int(np.round((x)/100)*100)
            c_strike,yet_to_place=order_button(2*at_strike-p_strike,'CE_S',tron)
            while True:
                if yet_to_place!=0:
                    tron=tron-1
                    while True:
                        strike,y=order_button(p_strike,'PE_B',1)
                        if y==0:
                            break
                    sleep(1)
                    c_strike,yet_to_place=order_button(2*at_strike-p_strike,'CE_S',tron)
                if yet_to_place==0:
                    break
            exclusive_strike=(c_strike==p_strike)*c_strike
        if x>=c_strike or x<=p_strike:
            at_strike=int(np.round((x)/100)*100)
            if at_strike==p_strike and at_strike==c_strike:
                pass
            elif at_strike==p_strike and at_strike!=c_strike:
                while True:
                    strike,yet_to_place=order_button(c_strike,'CE_B',tron)
                    if yet_to_place==0:
                        break
                c_strike,yet_to_place=order_button(at_strike,'CE_S',tron)
                while True:
                    if yet_to_place!=0:
                        tron=tron-1
                        while True:
                            strike,y=order_button(p_strike,'PE_B',1)
                            if y==0:
                                break
                        sleep(1)
                        c_strike,yet_to_place=order_button(at_strike,'CE_S',tron)
                    if yet_to_place==0:
                        break
                exclusive_strike,c_strike,p_strike=at_strike,at_strike,at_strike
            elif at_strike!=p_strike and at_strike==c_strike:
                while True:
                    strike,yet_to_place=order_button(p_strike,'PE_B',tron)
                    if yet_to_place==0:
                        break
                p_strike,yet_to_place=order_button(at_strike,'PE_S',tron)
                while True:
                    if yet_to_place!=0:
                        tron=tron-1
                        while True:
                            strike,y=order_button(c_strike,'CE_B',1)
                            if y==0:
                                break
                        sleep(1)
                        p_strike,yet_to_place=order_button(at_strike,'PE_S',tron)
                    if yet_to_place==0:
                        break
                exclusive_strike,c_strike,p_strike=at_strike,at_strike,at_strike
            elif at_strike!=p_strike and at_strike!=c_strike:
                k,y1=order_button(p_strike,'PE_B',tron)
                while True:
                    if y1!=0:
                        k,y1=order_button(p_strike,'PE_B',tron)
                    if y1==0:
                        break
                k,y1=order_button(p_strike,'CE_B',tron)
                while True:
                    if y1!=0:
                        k,y1=order_button(p_strike,'CE_B',tron)
                    if y1==0:
                        break
                tron=finalise_tron(c_strike=at_strike,p_strike=at_strike,tron=tron)
                exclusive_strike,c_strike,p_strike=at_strike,at_strike,at_strike
    return exclusive_strike,c_strike,p_strike,tron


def initial_leg_trades(x,tron):
    exclusive_strike=int(np.round((x)/100)*100)
    factor=100
    c_strike=exclusive_strike+factor
    p_strike=exclusive_strike-factor
    k,y1=order_button(p_strike,'PE_B',tron)
    while True:
        if y1!=0:
            k,y1=order_button(p_strike,'PE_B',tron)
        if y1==0:
            break
    k,y1=order_button(c_strike,'CE_B',tron)
    while True:
        if y1!=0:
            k,y1=order_button(c_strike,'CE_B',tron)
        if y1==0:
            break
    final_tron=finalise_tron(c_strike=exclusive_strike,p_strike=exclusive_strike,tron=tron)
    if final_tron!=tron:
        order_button(p_strike,'PE_S',tron-final_tron)
        order_button(c_strike,'CE_S',tron-final_tron)
    return final_tron,final_tron,c_strike,p_strike


def surya(x,c_strike_b,p_strike_b,c_leg_tron,p_leg_tron,exclusive_strike,strangle_c_strike,strangle_p_strike,strangle_tron):
    strangle_c_strike=(exclusive_strike==0)*strangle_c_strike+exclusive_strike
    strangle_p_strike=(exclusive_strike==0)*strangle_p_strike+exclusive_strike
    if x>c_strike_b:
        new_c_strike_b,y=order_button(c_strike_b+100,'CE_B',c_leg_tron+1)
        while y!=0:
            order_button(strangle_c_strike,'CE_B',1)
            order_button(strangle_p_strike,'PE_B',1)
            strangle_tron-=1
            new_c_strike_b,y=order_button(c_strike_b+100,'CE_B',c_leg_tron+1)
        o,y=order_button(c_strike_b,'CE_S',c_leg_tron+1)
        while y!=0:
            order_button(strangle_c_strike,'CE_B',1)
            order_button(strangle_p_strike,'PE_B',1)
            strangle_tron-=1
            o,y=order_button(c_strike_b,'CE_S',c_leg_tron+1)
        c_leg_tron+=1
    elif x<p_strike_b:
        new_p_strike_b,y=order_button(p_strike_b-100,'PE_B',p_leg_tron+1)
        while y!=0:
            order_button(strangle_c_strike,'CE_B',1)
            order_button(strangle_p_strike,'PE_B',1)
            strangle_tron-=1
            new_p_strike_b,y=order_button(p_strike_b-100,'PE_B',p_leg_tron+1)
        o,y=order_button(p_strike_b,'PE_S',p_leg_tron+1)
        while y!=0:
            order_button(strangle_c_strike,'CE_B',1)
            order_button(strangle_p_strike,'PE_B',1)
            strangle_tron-=1
            o,y=order_button(p_strike_b,'PE_S',p_leg_tron+1)
        p_leg_tron+=1
    else:
        new_c_strike_b,new_p_strike_b=c_strike_b,p_strike_b
    return new_c_strike_b,new_p_strike_b,c_leg_tron,p_leg_tron,strangle_tron

def exclusive_strike_change_trades(exclusive_strike,x,tron):
    k,y1=order_button(exclusive_strike,'PE_B',tron)
    while True:
        if y1!=0:
            k,y1=order_button(exclusive_strike,'PE_B',tron)
        if y1==0:
            break
    k,y1=order_button(exclusive_strike,'CE_B',tron)
    while True:
        if y1!=0:
            k,y1=order_button(exclusive_strike,'CE_B',tron)
        if y1==0:
            break
    exclusive_strike=int(np.round((x)/100)*100)
    tron=finalise_tron(c_strike=exclusive_strike,p_strike=exclusive_strike,tron=tron)
    return exclusive_strike,tron

def exit_signal(option_chain,exclusive_strike):
    temp=np.sum(option_chain[option_chain['StrikeRate']==exclusive_strike]['LastRate'])
    if temp<66:
        return 1
    else:
        return 0

def exit_trades(exclusive_strike,tron):
    order_button(exclusive_strike,'PE_B',tron)
    order_button(exclusive_strike,'CE_B',tron)   

def straddle_special_adjustment(exclusive_strike,x,tron):
    if exclusive_strike!=0 and tron!=0:
        def exclusive_strike_change_signal(earlier_x,x):
            a=(x-earlier_x)/66
            return abs(a)
        if exclusive_strike_change_signal(earlier_x=exclusive_strike,x=x)>1:
            exclusive_strike,tron=exclusive_strike_change_trades(exclusive_strike,x,tron)
        if exit_signal(option_chain,exclusive_strike)==1 and exclusive_strike!=0:
            exit_trades(exclusive_strike,tron)  
            tron=0 
    return exclusive_strike,tron

#%%
client_name = input('enter the client name: ')
leg_tron=int(input('leg_tron'))
prime_client=client_login(client=client_name)
option_chain,x=data(week=0)
c_leg_tron,p_leg_tron,c_strike_b,p_strike_b=initial_leg_trades(x,leg_tron)
tron=int(prime_client['login'].margin()[0]['AvailableMargin']/140000)
strangle_tron,strangle_c_strike,strangle_p_strike=initial_strangle_trades(option_chain,x,tron)
exclusive_strike=0
while True:
    option_chain,x=data(week=0)
    exclusive_strike,strangle_c_strike,strangle_p_strike,tron=strangle_adjustments(x,exclusive_strike,strangle_c_strike,strangle_p_strike,tron)
    exclusive_strike,strangle_tron=straddle_special_adjustment(exclusive_strike,x,strangle_tron)
    new_c_strike_b,new_p_strike_b,c_leg_tron,p_leg_tron,strangle_tron=surya(x,c_strike_b,p_strike_b,c_leg_tron,p_leg_tron,exclusive_strike,strangle_c_strike,strangle_p_strike,strangle_tron)
# %%
