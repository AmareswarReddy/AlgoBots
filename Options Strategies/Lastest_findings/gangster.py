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
    exchange='BANKNIFTY'
    lot_size=25
    max_lots_per_order=48
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

def opening_average():
    k=prime_client['login'].historical_data('N','C',999920005,'1d','2022-10-20','9999-06-16')
    k=k[(k['Open']!=0)]
    k=k[(k['Close']!=0)]
    average_opening_movement=np.average(np.abs(np.array(k['Open'])[-5:]-np.array(k['Close'])[-6:-1]))
    return average_opening_movement

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

def initial_strangle_trades(option_chain,x,tron):
    exclusive_strike=int(np.round((x)/100)*100)
    f=np.sum(option_chain[option_chain['StrikeRate']==int(np.round(x/100)*100)]['LastRate'])
    factor=2*int(np.ceil(f/100)*100)
    c_strike=exclusive_strike+factor
    p_strike=exclusive_strike-factor
    tron=finalise_tron(p_strike=p_strike,c_strike=c_strike,tron=tron)
    return tron,c_strike,p_strike

def rosetta(option_chain):
    ce_data=option_chain[option_chain['CPType']=='CE']
    pe_data=option_chain[option_chain['CPType']=='PE']
    i=np.array(pe_data['StrikeRate'])[0]
    end=np.array(pe_data['StrikeRate'])[-1]
    ss=np.array(pe_data['StrikeRate'])
    p_lastrate=np.array(list(pe_data['LastRate']))
    c_lastrate=np.array(list(ce_data['LastRate']))
    p_openinterest=np.array(list(pe_data['OpenInterest']))
    c_openinterest=np.array(list(ce_data['OpenInterest']))
    def loss_function(v):
        init_pe=np.dot(p_lastrate,p_openinterest)
        init_ce=np.dot(c_lastrate,c_openinterest)
        tmax=ss-v[0]
        tmax[tmax<0]=0
        tmin=v[0]-ss
        tmin[tmin<0]=0
        end_pe=np.dot(p_openinterest,tmax)
        end_ce=np.dot(c_openinterest,tmin)
        data=init_ce-end_ce-init_pe+end_pe
        return abs(data)
    a,b=pso(func=loss_function,lb=[i],ub=[end],minfunc=0.1)
    return  np.round_(a[0],1)

def rosetta_oi_indicator(option_chain):
    ce_data=option_chain[option_chain['CPType']=='CE']
    pe_data=option_chain[option_chain['CPType']=='PE']
    p_openinterest=np.sum(np.array(list(pe_data['OpenInterest'])))
    c_openinterest=np.sum(np.array(list(ce_data['OpenInterest'])))
    k=np.sign(p_openinterest-c_openinterest)
    return k*((k>0)*(p_openinterest/c_openinterest)+(k<0)*(c_openinterest/p_openinterest))

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
    m=rosetta(option_chain)
    return option_chain,2*x-m,x-m

def straddle_special_adjustment(exclusive_strike,x,tron):
    if exclusive_strike!=0:
        def exclusive_strike_change_signal(earlier_x,x):
            a=(x-earlier_x)/100
            return abs(a)
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
        if exclusive_strike_change_signal(earlier_x=exclusive_strike,x=x)>1:
            exclusive_strike,tron=exclusive_strike_change_trades(exclusive_strike,x,tron)
    return exclusive_strike,tron

def day_end_leg_trades(c_strike,p_strike,x,tron):
    if datetime.today().weekday()!=3:
        exclusive_strike=int(np.round((x)/100)*100)
        max_distance=np.sum(option_chain[option_chain['StrikeRate']==exclusive_strike]['LastRate'])
        if ((c_strike-p_strike)<0.7*max_distance and int(ind_time[11:13])*60+int(ind_time[14:16])>926) :
            if c_strike!=p_strike:
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
                tron=finalise_tron(c_strike=exclusive_strike,p_strike=exclusive_strike,tron=tron)
            factor=int(np.ceil(max_distance/100)*100)
            c_strike=exclusive_strike+factor
            p_strike=exclusive_strike-factor
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
            return exclusive_strike,c_strike,p_strike,1
    return 0,c_strike,p_strike,0

def strangle_adjustments(x,c_strike,p_strike,tron):
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
                c_strike=at_strike
                p_strike=at_strike
    exclusive_strike=(c_strike==p_strike)*int(np.round((x)/100)*100)
    return exclusive_strike,c_strike,p_strike,tron

def overnight_tron_decider(x,m,p_strike,c_strike,option_chain,tron,A):
    x1=x-m
    exclusive_strike=int(np.round((x1)/100)*100)
    ce_data=option_chain[option_chain['CPType']=='CE']
    pe_data=option_chain[option_chain['CPType']=='PE']
    c_lastrate=int(ce_data[ce_data['StrikeRate']==c_strike]['LastRate'])
    p_lastrate=int(pe_data[pe_data['StrikeRate']==p_strike]['LastRate'])
    c_e_lastrate=int(ce_data[ce_data['StrikeRate']==exclusive_strike]['LastRate'])
    p_e_lastrate=int(pe_data[pe_data['StrikeRate']==exclusive_strike]['LastRate'])
    def breakeven_finder(ptron,ctron):
        call_breakeven=(ctron*(exclusive_strike+c_e_lastrate)-tron*(c_strike+c_lastrate+p_lastrate)+ptron*(p_e_lastrate))/(ctron-tron)
        put_breakeven=(ptron*(p_e_lastrate-exclusive_strike)+tron*(p_strike-p_lastrate-c_lastrate)+ctron*c_e_lastrate)/(tron-ptron)
        return put_breakeven,call_breakeven
    def objective_function(parameters):
        ptron=parameters[0]
        ctron=parameters[1]
        put_breakeven,call_breakeven=breakeven_finder(ptron,ctron)
        return ((exclusive_strike-put_breakeven-A)*(exclusive_strike-put_breakeven-A))+((call_breakeven-exclusive_strike-A)*(call_breakeven-exclusive_strike-A))
    def constraints(parameters):
        ptron=parameters[0]
        ctron=parameters[1]
        ss=tron*(p_lastrate+c_lastrate)-ptron*p_e_lastrate-ctron*c_e_lastrate
        return [ss]
    xopt,fopt=pso(objective_function,[0,0],[tron-1+(tron==1),tron-1+(tron==1)],f_ieqcons=constraints,swarmsize=10000,maxiter=10000)
    ptron,ctron=int(xopt[0]),int(xopt[1])
    return ptron,ctron

def overnight_safety_trades(x,m,c_strike,p_strike,tron,f2):
    f1=4.2-(1+datetime.today().weekday()-5*(datetime.today().weekday()==4))
    A=f1*f2
    if datetime.today().weekday()!=3 and int(ind_time[11:13])*60+int(ind_time[14:16])>921:
        ptron,ctron=overnight_tron_decider(x,m,p_strike,c_strike,option_chain,tron,A)
        k,y1=order_button(exclusive_strike,'PE_B',ptron)
        while True:
            if y1!=0:
                k,y1=order_button(exclusive_strike,'PE_B',ptron)
            if y1==0:
                break
        k,y1=order_button(exclusive_strike,'CE_B',ctron)
        while True:
            if y1!=0:
                k,y1=order_button(exclusive_strike,'CE_B',ctron)
            if y1==0:
                break
        return 1
    return 0

#%%
#variables to be initialised
tron=int(input('Lots to Sell (Eg 3) :'))
start=int(input('enter 0 if starting the strategy for the first time, else 1 :  '))
client_name = input('enter the client name: ')
prime_client=client_login(client=client_name)
option_chain,x,kiki=data(week=0)
prev_x=x+kiki
f2=opening_average()
if start==1:
    c_strike=int(input('enter call strike :  '))
    p_strike=int(input('enter put strike :  '))
    exclusive_strike=int((c_strike==p_strike)*c_strike)
#%%
ind_time = datetime.now(timezone("Asia/Kolkata")).strftime('%Y-%m-%d %H:%M:%S.%f')
while int(ind_time[11:13])*60+int(ind_time[14:16])<556 or int(ind_time[11:13])*60+int(ind_time[14:16])>885 :
    ind_time = datetime.now(timezone("Asia/Kolkata")).strftime('%Y-%m-%d %H:%M:%S.%f')
if start==0:
    option_chain,x,m=data(week=0)
    exclusive_strike,c_strike,p_strike=0,0,0
    tron,c_strike,p_strike=initial_strangle_trades(option_chain,x,tron)

while True:
    option_chain,x,m=data(week=0)
    exclusive_strike,c_strike,p_strike,tron=strangle_adjustments(x,c_strike,p_strike,tron)
    exclusive_strike,tron=straddle_special_adjustment(exclusive_strike,x,tron)
    shoot=overnight_safety_trades(x,m,c_strike,p_strike,tron,f2)
    exclusive_strike,c_strike_b,p_strike_b,is_t_special=day_end_leg_trades(c_strike,p_strike,x,tron)
    if is_t_special==1 or shoot==1:
        break

# %%
