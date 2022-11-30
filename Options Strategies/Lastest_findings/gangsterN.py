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

def order_button(exclusive_strike,type,lots):
    sleep(0.5)
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

def opening_average():
    k=prime_client['login'].historical_data('N','C',999920000,'1d','2022-10-20','9999-06-16')
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
    exclusive_strike=int(np.round((x)/50)*50)
    f=np.sum(option_chain[option_chain['StrikeRate']==int(np.round(x/50)*50)]['LastRate'])
    factor=float(1.3+1.1*np.random.rand(1)/2)*int(np.ceil(f/50)*50)
    factor=int(np.round((factor)/50)*50)
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
    m=rosetta(option_chain)
    return option_chain,2*x-m,x-m

def exit_signal(option_chain,exclusive_strike):
    temp=np.sum(option_chain[option_chain['StrikeRate']==exclusive_strike]['LastRate'])
    if temp<25:
        return 1
    else:
        return 0
def exit_trades(exclusive_strike,tron):
    order_button(exclusive_strike,'PE_B',tron)
    order_button(exclusive_strike,'CE_B',tron)   

def to_exit_at_start(strike,call_lots_bought,put_lots_bought):
    order_button(strike,'PE_S',put_lots_bought)
    order_button(strike,'CE_S',call_lots_bought)  

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
    exclusive_strike=int(np.round((x)/50)*50)
    tron=finalise_tron(c_strike=exclusive_strike,p_strike=exclusive_strike,tron=tron)
    return exclusive_strike,tron

def straddle_special_adjustment(exclusive_strike,x,tron,chameleon_signal):
    if exclusive_strike!=0 and chameleon_signal==0:
        def exclusive_strike_change_signal(earlier_x,x):
            a=(x-earlier_x)/33
            return abs(a)
        if exclusive_strike_change_signal(earlier_x=exclusive_strike,x=x)>1:
            exclusive_strike,tron=exclusive_strike_change_trades(exclusive_strike,x,tron)
        if exit_signal(option_chain,exclusive_strike)==1 and exclusive_strike!=0:
            exit_trades(exclusive_strike,tron)   
            chameleon_signal=1
    return exclusive_strike,tron,chameleon_signal

def leg_adjustments(exclusive_strike,c_strike_b,p_strike_b,x,tron,leg):
    if exclusive_strike!=0 and leg==1:
        def exclusive_strike_change_signal(earlier_x,x):
            a=(x-earlier_x)/33
            return abs(a)
        if exclusive_strike_change_signal(earlier_x=exclusive_strike,x=x)>1:
            exclusive_strike,tron=exclusive_strike_change_trades(exclusive_strike,x,tron)
        if exit_signal(option_chain,exclusive_strike)==1 and exclusive_strike!=0:
            exit_trades(exclusive_strike,tron)   
        if (c_strike_b-x)<25:
            at_strike=int(np.round((x)/50)*50)
            k,j=order_button(2*at_strike-p_strike_b,'CE_B',tron)
            if j==0:
                order_button(c_strike_b,'CE_S',tron)
                c_strike_b=k
        if x-p_strike_b<25:
            at_strike=int(np.round((x)/50)*50)
            k,j=order_button(2*at_strike-c_strike_b,'PE_B',tron)
            if j==0:
                order_button(p_strike_b,'PE_S',tron)
                p_strike_b=2*at_strike-c_strike_b
    return exclusive_strike,c_strike_b,p_strike_b,tron

def day_end_leg_trades(exclusive_strike,c_strike,p_strike,x,tron):
    ind_time = datetime.now(timezone("Asia/Kolkata")).strftime('%Y-%m-%d %H:%M:%S.%f')
    if datetime.today().weekday()!=3 and int(ind_time[11:13])*60+int(ind_time[14:16])>926:
        exclusive_strike=int(np.round((x)/50)*50)
        max_distance=np.sum(option_chain[option_chain['StrikeRate']==exclusive_strike]['LastRate'])
        if (c_strike-p_strike)<0.7*max_distance :
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
            factor=int(np.ceil(max_distance/50)*50)
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
            seller_tron,sell_c_strike,sell_p_strike=initial_strangle_trades(option_chain,x,tron)
            return tron,exclusive_strike,c_strike,p_strike,1,[seller_tron,sell_c_strike,sell_p_strike]
    return tron,exclusive_strike,c_strike,p_strike,0,[0,0,0]

def strangle_adjustments(x,exclusive_strike,c_strike,p_strike,tron):
    if c_strike!=p_strike:
        ce_data=option_chain[option_chain['CPType']=='CE']
        pe_data=option_chain[option_chain['CPType']=='PE']
        c_lastrate=int(ce_data[ce_data['StrikeRate']==c_strike]['LastRate'])
        p_lastrate=int(pe_data[pe_data['StrikeRate']==p_strike]['LastRate'])
        at_strike=int(np.round((x)/50)*50)
        if c_lastrate/p_lastrate>2.1 and (2*at_strike-c_strike)>p_strike :
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
        if p_lastrate/c_lastrate>2.1 and (2*at_strike-p_strike)<c_strike:
            while True:
                strike,yet_to_place=order_button(c_strike,'CE_B',tron)
                if yet_to_place==0:
                    break
            at_strike=int(np.round((x)/50)*50)
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
            at_strike=int(np.round((x)/50)*50)
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

def overnight_tron_decider(x,m,p_strike,c_strike,option_chain,tron,A):
    x1=x-m
    exclusive_strike=int(np.round((x1)/50)*50)
    ce_data=option_chain[option_chain['CPType']=='CE']
    pe_data=option_chain[option_chain['CPType']=='PE']
    c_lastrate=int(ce_data[ce_data['StrikeRate']==c_strike]['LastRate'])
    p_lastrate=int(pe_data[pe_data['StrikeRate']==p_strike]['LastRate'])
    c_e_lastrate=int(ce_data[ce_data['StrikeRate']==exclusive_strike]['LastRate'])
    p_e_lastrate=int(pe_data[pe_data['StrikeRate']==exclusive_strike]['LastRate'])
    def optimisation():
        kk=pd.DataFrame(permutations(np.linspace(0,tron-1,tron),2))
        kk[2]=tron*(p_lastrate+c_lastrate)-kk[0]*p_e_lastrate-kk[1]*c_e_lastrate
        to_check=kk[kk[2]>=0]
        call_breakeven=(to_check[1]*(exclusive_strike+c_e_lastrate)-tron*(c_strike+c_lastrate+p_lastrate)+to_check[0]*(p_e_lastrate))/(to_check[1]-tron)
        put_breakeven=(to_check[0]*(p_e_lastrate-exclusive_strike)+tron*(p_strike-p_lastrate-c_lastrate)+to_check[1]*c_e_lastrate)/(tron-to_check[0])
        to_optimise=((exclusive_strike-put_breakeven-A)*(exclusive_strike-put_breakeven-A))+((call_breakeven-exclusive_strike-A)*(call_breakeven-exclusive_strike-A))
        if len(to_optimise)>0:
            indexer=np.argmin(to_optimise)
            return np.array(to_check[0])[indexer],np.array(to_check[1])[indexer]
        else:
            return 0,0
        
    ptron,ctron=optimisation()
    return int(ptron),int(ctron),exclusive_strike
    
def overnight_safety_trades(x,m,c_strike,p_strike,tron,f2):
    ind_time = datetime.now(timezone("Asia/Kolkata")).strftime('%Y-%m-%d %H:%M:%S.%f')
    f1=4.2-(1+datetime.today().weekday()-5*(datetime.today().weekday()==4))
    A=f1*f2
    if datetime.today().weekday()!=3 and int(ind_time[11:13])*60+int(ind_time[14:16])>921 and c_strike!=p_strike:
        ptron,ctron,exclusive_strike=overnight_tron_decider(x,m,p_strike,c_strike,option_chain,tron,A)
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
        return 1,exclusive_strike,ptron,ctron
    return 0,0,0,0

def reset_day_leg_trades(positions_json):
    if positions_json['leg']['exclusive_strike']!=positions_json['day_end_leg']['exclusive_strike']:
        exclusive_strike,tron=exclusive_strike_change_trades(positions_json['leg']['exclusive_strike'],positions_json['day_end_leg']['exclusive_strike'],positions_json['leg']['tron'])
        positions_json['day_end_leg']['tron']+=tron
    if positions_json['leg']['call_strike']!=positions_json['day_end_leg']['call_strike']:
        k,j=order_button(positions_json['day_end_leg']['call_strike'],'CE_B',tron)
        if j==0:
            order_button(positions_json['leg']['call_strike'],'CE_S',tron)
    if positions_json['leg']['put_strike']!=positions_json['day_end_leg']['put_strike']:
        k,j=order_button(positions_json['day_end_leg']['put_strike'],'PE_B',tron)
        if j==0:
            order_button(positions_json['leg']['put_strike'],'PE_S',tron)
    positions_json['leg']['tron']=positions_json['day_end_leg']['tron']
    positions_json['leg']['exclusive_strike']=positions_json['day_end_leg']['exclusive_strike']
    positions_json['leg']['call_strike']=positions_json['day_end_leg']['call_strike']
    positions_json['leg']['put_strike']=positions_json['day_end_leg']['put_strike']
    positions_json['day_end_leg']['tron']=0
    positions_json['day_end_leg']['exclusive_strike']=0
    positions_json['day_end_leg']['call_strike']=0
    positions_json['day_end_leg']['put_strike']=0
    return positions_json

def chameleon_initial_trades():
    maximum_effort=int(prime_client['login'].margin()[0]['AvailableMargin']/30000)
    exclusive_strike=int(np.round((x)/50)*50)
    c1=exclusive_strike+50
    p1=exclusive_strike-50
    p1,p_yet_to_place=order_button(p1,'PE_B',maximum_effort)
    c1,c_yet_to_place=order_button(c1,'CE_B',maximum_effort)
    return maximum_effort

def chameleon_on_grass(chameleon_start,exclusive_strike,side,side_,prev_x,x,tron,chameleon_signal):
    def good_to_go(prev_x,x):
        a=np.floor(prev_x/50)
        b=np.floor(x/50)
        if a>b:
            return -1
        elif a<b:
            return 1
        else:
            return 0
    def change_of_strike(earlier_x,x):
        a=(x-earlier_x)/50
        return a
    def side_switch(earlier_x,x,side):
        a=(x-earlier_x)
        if a>0 and side=='CE_S':
            return 'PE_S'
        elif a<0 and side=='PE_S':
            return 'CE_S'
        if a>0 and side=='PE_B':
            return 'CE_B'
        elif a<0 and side=='CE_B':
            return 'PE_B'
        else:
            return side
    if chameleon_signal==1:
        if chameleon_start==0:
            if good_to_go(x=x,prev_x=prev_x)>0:
                tron=chameleon_initial_trades()
                exclusive_strike,yet_to_place=order_button(int(np.round(x/50)*50),'PE_S',tron)
                tron=tron-lots_drop(int(np.round(x/50)*50),'PE_S',yet_to_place)
                chameleon_start=1
                side='PE_S'
            if good_to_go(x=x,prev_x=prev_x)<0:
                tron=chameleon_initial_trades()
                exclusive_strike,yet_to_place=order_button(int(np.round(x/50)*50),'CE_S',tron)
                tron=tron-lots_drop(int(np.round(x/50)*50),'CE_S',yet_to_place)
                chameleon_start=1
                side='CE_S'
        if chameleon_start==1:
            if change_of_strike(earlier_x=exclusive_strike,x=x)>1:
                earlier_margin=prime_client['login'].margin()[0]['AvailableMargin']
                order_button(exclusive_strike,'PE_B',tron)
                while True:
                    later_margin=prime_client['login'].margin()[0]['AvailableMargin']
                    if later_margin>earlier_margin:
                        break
                tron=tron+1
                exclusive_strike,yet_to_place=order_button(int(np.round(x/50)*50),'PE_S',tron)
                tron=tron-lots_drop(int(np.round(x/50)*50),'PE_S',yet_to_place)
                side='PE_S'
            if change_of_strike(earlier_x=exclusive_strike,x=x)<-1:
                earlier_margin=prime_client['login'].margin()[0]['AvailableMargin']
                order_button(exclusive_strike,'CE_B',tron)
                while True:
                    later_margin=prime_client['login'].margin()[0]['AvailableMargin']
                    if later_margin>earlier_margin:
                        break
                tron=tron+1
                exclusive_strike,yet_to_place=order_button(int(np.round(x/50)*50),'CE_S',tron)
                tron=tron-lots_drop(int(np.round(x/50)*50),'CE_S',yet_to_place)
                side='CE_S'
            side_=side_switch(earlier_x=exclusive_strike,x=x,side=side)
            if side_!=side:
                if side=='CE_S':
                    earlier_margin=prime_client['login'].margin()[0]['AvailableMargin']
                    order_button(exclusive_strike,'CE_B',tron)
                    while True:
                        later_margin=prime_client['login'].margin()[0]['AvailableMargin']
                        if later_margin>earlier_margin:
                            break
                    tron+=1
                    exclusive_strike,yet_to_place=order_button(int(np.round(x/50)*50),side_,tron)
                    tron=tron-lots_drop(int(np.round(x/50)*50),side_,yet_to_place)
                if side=='PE_S':
                    earlier_margin=prime_client['login'].margin()[0]['AvailableMargin']
                    order_button(exclusive_strike,'PE_B',tron)
                    while True:
                        later_margin=prime_client['login'].margin()[0]['AvailableMargin']
                        if later_margin>earlier_margin:
                            break
                    tron+=1
                    exclusive_strike,yet_to_place=order_button(int(np.round(x/50)*50),side_,tron)
                    tron=tron-lots_drop(int(np.round(x/50)*50),side_,yet_to_place)
                side=side_
        prev_x=x
    return chameleon_start,exclusive_strike,side,side_,prev_x,tron,chameleon_signal
#%%
#variables to be initialised
client_name = input('enter the client name: ')
prime_client=client_login(client=client_name)
option_chain,x,kiki=data(week=0)
prev_x=x-kiki
f2=opening_average()
chameleon_signal=0
chameleon_start,side,side_=0,'',''
start=int(input('enter 0 if starting the strategy for the first time, else 1 :  '))
to_take_from_positions=input('do you wish to take positions from existing json(y/n): ')
if to_take_from_positions=='y':
    positions_record=json.load(open(client_name+'_positions.json'))
    tron=positions_record['strangle']['tron']
    overnight_safety=(positions_record['overnight_safety']['put_tron']+positions_record['overnight_safety']['call_tron'])!=0
    leg=(positions_record['leg']['tron']!=0)
    strike=positions_record['overnight_safety']['exclusive_strike']
    call_lots_bought=positions_record['overnight_safety']['call_tron']
    put_lots_bought=positions_record['overnight_safety']['put_tron']
    c_strike=positions_record['strangle']['call_strike']
    p_strike=positions_record['strangle']['put_strike']
    exclusive_strike=int((c_strike==p_strike)*c_strike)
    tron_leg=positions_record['leg']['tron']
    exclusive_strike_leg=positions_record['leg']['exclusive_strike']
    c_strike_b=positions_record['leg']['call_strike']
    p_strike_b=positions_record['leg']['put_strike']
else:
    tron=int(input('Lots to Sell (Eg 3) :'))
    overnight_safety=int(input('enter 0 if no overnight trades were taken else 1 :  '))
    leg=int(input('enter 0 if no leg trades were taken else 1 :  '))
    if overnight_safety==1:
        strike=int(input('enter the strike at which overnight safety trades were taken: '))
        call_lots_bought=int(input('enter the no. of call lots bought for safety: '))
        put_lots_bought=int(input('enter the no. of puts lots bought for safety: '))
    if start==1:
        c_strike=int(input('enter strangle call strike :  '))
        p_strike=int(input('enter strangle put strike :  '))
        exclusive_strike=int((c_strike==p_strike)*c_strike)
    if leg==1:
        tron_leg=int(input('Lots for leg (Eg 3) :'))
        exclusive_strike_leg=int(input('enter leg exclusive strike :  '))
        c_strike_b=int(input('enter leg call buy strike :  '))
        p_strike_b=int(input('enter leg put buy strike :  '))
    if leg==0:
        tron_leg,exclusive_strike_leg,c_strike_b,p_strike_b=0,0,0,0
#%%
ind_time = datetime.now(timezone("Asia/Kolkata")).strftime('%Y-%m-%d %H:%M:%S.%f')
while int(ind_time[11:13])*60+int(ind_time[14:16])<556 or int(ind_time[11:13])*60+int(ind_time[14:16])>1085 :
    ind_time = datetime.now(timezone("Asia/Kolkata")).strftime('%Y-%m-%d %H:%M:%S.%f')
if start==0:
    option_chain,x,m=data(week=0)
    exclusive_strike,c_strike,p_strike=0,0,0
    tron,c_strike,p_strike=initial_strangle_trades(option_chain,x,tron)

if overnight_safety==1:
    to_exit_at_start(strike,call_lots_bought,put_lots_bought)
#%%
while True:
    option_chain,x,m=data(week=0)
    exclusive_strike,c_strike,p_strike,tron=strangle_adjustments(x-m,exclusive_strike,c_strike,p_strike,tron)
    exclusive_strike,tron,chameleon_signal=straddle_special_adjustment(exclusive_strike,x-m,tron,chameleon_signal)
    exclusive_strike_leg,c_strike_b,p_strike_b,tron_leg=leg_adjustments(exclusive_strike_leg,c_strike_b,p_strike_b,x-m,tron_leg,leg)
    chameleon_start,exclusive_strike,side,side_,prev_x,tron,chameleon_signal=chameleon_on_grass(chameleon_start,exclusive_strike,side,side_,prev_x,x-m,tron,chameleon_signal)
    shoot,overnight_exclusive_strike,ptron,ctron=overnight_safety_trades(x,m,c_strike,p_strike,tron,f2)
    day_end_tron,day_end_exclusive_strike,day_end_c_strike_b,day_end_p_strike_b,is_t_special,strangle_list=day_end_leg_trades(exclusive_strike,c_strike,p_strike,x-m,tron)
    if shoot==1:
        positions_json={'strangle':{'call_strike':c_strike,'put_strike':p_strike,'tron':tron},
                        'overnight_safety':{'exclusive_strike':overnight_exclusive_strike,'put_tron':ptron,'call_tron':ctron},
                        'leg':{'exclusive_strike':exclusive_strike_leg,'call_strike':c_strike_b,'put_strike':p_strike_b,'tron':tron_leg},
                        'day_end_leg':{'exclusive_strike':0,'call_strike':0,'put_strike':0,'tron':0}}
        break
    if is_t_special==1:
        positions_json={'strangle':{'call_strike':strangle_list[1],'put_strike':strangle_list[2],'tron':strangle_list[0]},
                        'overnight_safety':{'exclusive_strike':0,'put_tron':0,'call_tron':0},
                        'leg':{'exclusive_strike':exclusive_strike_leg,'call_strike':c_strike_b,'put_strike':p_strike_b,'tron':tron_leg},
                        'day_end_leg':{'exclusive_strike':day_end_exclusive_strike,'call_strike':day_end_c_strike_b,'put_strike':day_end_p_strike_b,'tron':day_end_tron}}
        positions_json=reset_day_leg_trades(positions_json)
        break

print(positions_json)
out_file = open(client_name+'_positions.json', "w")
json.dump(positions_json, out_file, indent = 6)
out_file.close()



#%%
def reset_day_leg_trades(positions_json):
    if positions_json['leg']['exclusive_strike']!=positions_json['day_end_leg']['exclusive_strike']:
        exclusive_strike,tron=exclusive_strike_change_trades(positions_json['leg']['exclusive_strike'],positions_json['day_end_leg']['exclusive_strike'],positions_json['leg']['tron'])
        positions_json['day_end_leg']['tron']+=tron
    if positions_json['leg']['call_strike']!=positions_json['day_end_leg']['call_strike']:
        k,j=order_button(positions_json['day_end_leg']['call_strike'],'CE_B',tron)
        order_button(positions_json['leg']['call_strike'],'CE_S',tron)
    if positions_json['leg']['put_strike']!=positions_json['day_end_leg']['put_strike']:
        k,j=order_button(positions_json['day_end_leg']['put_strike'],'PE_B',tron)
        
        order_button(positions_json['leg']['put_strike'],'PE_S',tron)
    positions_json['leg']['tron']=positions_json['day_end_leg']['tron']
    positions_json['leg']['exclusive_strike']=positions_json['day_end_leg']['exclusive_strike']
    positions_json['leg']['call_strike']=positions_json['day_end_leg']['call_strike']
    positions_json['leg']['put_strike']=positions_json['day_end_leg']['put_strike']
    positions_json['day_end_leg']['tron']=0
    positions_json['day_end_leg']['exclusive_strike']=0
    positions_json['day_end_leg']['call_strike']=0
    positions_json['day_end_leg']['put_strike']=0
    return positions_json

positions_json={'strangle':{'call_strike':0,'put_strike':0,'tron':0},
                'overnight_safety':{'exclusive_strike':0,'put_tron':0,'call_tron':0},
                'leg':{'exclusive_strike':18700,'call_strike':18850,'put_strike':18600,'tron':1},
                'day_end_leg':{'exclusive_strike':18750,'call_strike':18800,'put_strike':18650,'tron':2}}
def exclusive_strike_change_trades(exclusive_strike,x,tron):
    k,y1=order_button(exclusive_strike,'PE_B',tron)
    k,y1=order_button(exclusive_strike,'CE_B',tron)
    exclusive_strike=int(np.round((x)/50)*50)
    tron=finalise_tron(c_strike=exclusive_strike,p_strike=exclusive_strike,tron=tron)
    return exclusive_strike,tron
def finalise_tron(p_strike,c_strike,tron):
    p_strike,p_yet_to_place=order_button(p_strike,'PE_S',tron)
    c_strike,c_yet_to_place=order_button(c_strike,'CE_S',tron)
    return tron

kk=reset_day_leg_trades(positions_json)
# %%
