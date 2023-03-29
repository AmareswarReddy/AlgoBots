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
from pyswarm import pso
import requests
from pytz import timezone 
from cred import *
from py5paisa.order import Basket_order
from scipy import interpolate
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

def finalise_tron(p_strike,c_strike,tron,to_take_c_strike,to_take_p_strike):
    if tron<0:
        return 0
    if to_take_p_strike==1:
        p_strike,p_yet_to_place=order_button(p_strike,'PE_S',tron)
    else:
        p_yet_to_place=0
    if to_take_c_strike==1:
        c_strike,c_yet_to_place=order_button(c_strike,'CE_S',tron)
    else:
        c_yet_to_place=0
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
        return finalise_tron(p_strike=p_strike,c_strike=c_strike,tron=tron-1,to_take_c_strike=to_take_c_strike,to_take_p_strike=to_take_p_strike)


def data(week):
    exchange='BANKNIFTY'
    while True:
        try :
            expiry_timestamps=prime_client['login'].get_expiry("N",exchange).copy()
            current_expiry_time_stamp_weekly=int(expiry_timestamps['Expiry'][week]['ExpiryDate'][6:19])
            expiry_timestamps=prime_client['login'].get_expiry("N",exchange).copy()
            option_chain=pd.DataFrame(prime_client['login'].get_option_chain("N",exchange,current_expiry_time_stamp_weekly)['Options'])
            x=expiry_timestamps['lastrate'][0]['LTP']
            break
        except Exception :
            pass
    return option_chain,x

def initial_strangle_trades(option_chain,x):
    exclusive_strike=int(np.round((x)/100)*100)
    tron=int(prime_client['login'].margin()[0]['AvailableMargin']/170000)
    f=np.sum(option_chain[option_chain['StrikeRate']==int(np.round(x/100)*100)]['LastRate'])
    factor=float(1.9+1.1*np.random.rand(1)/2)*int(np.ceil(f/100)*100)
    factor=int(np.round((factor)/100)*100)
    c_strike=exclusive_strike+factor
    p_strike=exclusive_strike-factor
    tron=finalise_tron(p_strike=p_strike,c_strike=c_strike,tron=tron,to_take_c_strike=1,to_take_p_strike=1)
    return tron,c_strike,p_strike


def margin_utilizer(c_strike,p_strike,tron_towards_leg):
    try:
        k=prime_client['login'].margin()[0]['AvailableMargin']
        tron=int(k/(400000+tron_towards_leg*60000))
        tron=finalise_tron(p_strike=p_strike,c_strike=c_strike,tron=tron,to_take_c_strike=1,to_take_p_strike=1)
        return tron
    except Exception:
        return 0

def re_adjust_strangle(strangle_lastrate_sum,option_chain,x):
    exclusive_strike=int(np.round((x)/100)*100)
    f=np.sum(option_chain[option_chain['StrikeRate']==int(np.round(x/100)*100)]['LastRate'])
    factor=float(1.9+1.1*np.random.rand(1)/2)*int(np.ceil(f/100)*100)
    factor=int(np.round((factor)/100)*100)
    c_strike=exclusive_strike+factor
    p_strike=exclusive_strike-factor
    ce_data=option_chain[option_chain['CPType']=='CE']
    pe_data=option_chain[option_chain['CPType']=='PE']
    c_lastrate=float(ce_data[ce_data['StrikeRate']==c_strike]['LastRate'])
    p_lastrate=float(pe_data[pe_data['StrikeRate']==p_strike]['LastRate'])
    cp_sum=c_lastrate+p_lastrate
    if 2.13*strangle_lastrate_sum<cp_sum:
        return True
    else:
        return False

def new_strangle_adjustment_trades(option_chain,x,tron,sell_value,c_strike,p_strike):
    def strangle_sum(c_strike,p_strike):
        ce_data=option_chain[option_chain['CPType']=='CE']
        pe_data=option_chain[option_chain['CPType']=='PE']
        c_lastrate=float(ce_data[ce_data['StrikeRate']==c_strike]['LastRate'])
        p_lastrate=float(pe_data[pe_data['StrikeRate']==p_strike]['LastRate'])
        return c_lastrate+p_lastrate
    exclusive_strike=int(np.round((x)/100)*100)
    f=np.sum(option_chain[option_chain['StrikeRate']==int(np.round(x/100)*100)]['LastRate'])
    factor=float(2+np.random.rand(1)/2)*int(np.ceil(f/100)*100)
    factor=int(np.round((factor)/100)*100)
    old_c_strike=c_strike
    old_p_strike=p_strike
    while True:
        factor-=100
        c_strike=exclusive_strike+factor
        p_strike=exclusive_strike-factor
        new_sell_value=strangle_sum(c_strike,p_strike)
        if new_sell_value>sell_value or factor==0:
            if c_strike==old_c_strike:
                to_take_c_strike=0
            elif c_strike!=old_c_strike:
                order_button(old_c_strike,'CE_B',tron)
                to_take_c_strike=1
            if p_strike==old_p_strike:
                to_take_p_strike=0
            elif p_strike!=old_p_strike:
                order_button(old_p_strike,'PE_B',tron)
                to_take_p_strike=1
            tron=finalise_tron(p_strike=p_strike,c_strike=c_strike,tron=tron,to_take_c_strike=to_take_c_strike,to_take_p_strike=to_take_p_strike)
            break
    return tron,c_strike,p_strike

def strangle_adjustments(x,exclusive_strike,c_strike,p_strike,tron,tron_towards_leg):
    if c_strike!=p_strike:
        ce_data=option_chain[option_chain['CPType']=='CE']
        pe_data=option_chain[option_chain['CPType']=='PE']
        c_lastrate=float(ce_data[ce_data['StrikeRate']==c_strike]['LastRate'])
        p_lastrate=float(pe_data[pe_data['StrikeRate']==p_strike]['LastRate'])
        if re_adjust_strangle(c_lastrate+p_lastrate,option_chain,x):
            while True:
                strike,yet_to_place=order_button(p_strike,'PE_B',tron)
                if yet_to_place==0:
                    break
            while True:
                strike,yet_to_place=order_button(c_strike,'CE_B',tron)
                if yet_to_place==0:
                    break
            tron,c_strike,p_strike=initial_strangle_trades(option_chain,x)
        at_strike=int(np.round((x)/100)*100)
        at_strike_premium_sum=float(ce_data[ce_data['StrikeRate']==at_strike]['LastRate'])+float(pe_data[pe_data['StrikeRate']==at_strike]['LastRate'])
        if (c_lastrate/p_lastrate>(1+at_strike_premium_sum/(c_lastrate+p_lastrate)) or p_lastrate/c_lastrate>(1+at_strike_premium_sum/(c_lastrate+p_lastrate)) ) :
            tron,c_strike,p_strike=new_strangle_adjustment_trades(option_chain,x,tron,c_lastrate+p_lastrate,c_strike,p_strike)
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
                tron=finalise_tron(c_strike=at_strike,p_strike=at_strike,tron=tron,to_take_c_strike=1,to_take_p_strike=1)
                exclusive_strike,c_strike,p_strike=at_strike,at_strike,at_strike
        tron=tron+margin_utilizer(c_strike,p_strike,tron_towards_leg)
    return exclusive_strike,c_strike,p_strike,tron

def initial_leg_trades(x,option_chain,tron):
    exclusive_strike=int(np.round((x)/100)*100)
    ce_data=option_chain[option_chain['CPType']=='CE']
    pe_data=option_chain[option_chain['CPType']=='PE']
    c_lastrate=float(ce_data[ce_data['StrikeRate']==exclusive_strike]['LastRate'])
    p_lastrate=float(pe_data[pe_data['StrikeRate']==exclusive_strike]['LastRate'])
    f=(p_lastrate+c_lastrate)
    factor=max(100,int(np.floor((f)/100)*100))
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
    final_tron=finalise_tron(c_strike=exclusive_strike,p_strike=exclusive_strike,tron=tron,to_take_c_strike=1,to_take_p_strike=1)
    if final_tron!=tron:
        order_button(p_strike,'PE_S',tron-final_tron)
        order_button(c_strike,'CE_S',tron-final_tron)
    return final_tron,final_tron,c_strike,p_strike,exclusive_strike,exclusive_strike

def buy_kickoff(start,indicator,earlier_indicator,exclusive_strike,tron,lots_to_be_added):
    if abs(indicator-earlier_indicator)==2 and start==0:
        indicator=0
    if start==0:
        s=indicator
        if s>0:
            exclusive_strike,yet_to_place=order_button(exclusive_strike,'CE_B',tron)
            tron-=lots_drop(exclusive_strike,'CE_B',yet_to_place)
            start=1
        elif s<0:
            exclusive_strike,yet_to_place=order_button(exclusive_strike,'PE_B',tron)
            tron-=lots_drop(exclusive_strike,'PE_B',yet_to_place)
            start=1
    elif start==1:
        #if earlier_indicator==0 and indicator==1:
        #    exclusive_strike,yet_to_place=order_button(0,'CE_B',tron)
        #    tron-=lots_drop(exclusive_strike,'CE_B',yet_to_place)
        #if earlier_indicator==0 and indicator==-1:
        #    exclusive_strike,yet_to_place=order_button(0,'PE_B',tron)
        #    tron-=lots_drop(exclusive_strike,'PE_B',yet_to_place)
        #if earlier_indicator==-1 and indicator==0:
        #    exclusive_strike,yet_to_place=order_button(exclusive_strike,'PE_S',tron)
        #if earlier_indicator==1 and indicator==0:
        #    exclusive_strike,yet_to_place=order_button(exclusive_strike,'CE_S',tron)
        

        if earlier_indicator==-1 and indicator==1:
            exclusive_strike,yet_to_place=order_button(exclusive_strike,'PE_S',tron)
            exclusive_strike,yet_to_place=order_button(0,'CE_B',tron)
            tron-=lots_drop(exclusive_strike,'CE_B',yet_to_place)

        if earlier_indicator==1 and indicator==-1:
            exclusive_strike,yet_to_place=order_button(exclusive_strike,'CE_S',tron)
            exclusive_strike,yet_to_place=order_button(0,'PE_B',tron)
            tron-=lots_drop(exclusive_strike,'PE_B',yet_to_place)


        if lots_to_be_added!=0:
            if indicator==1:
                exclusive_strike,yet_to_place=order_button(exclusive_strike,'CE_B',lots_to_be_added)
                tron+=lots_to_be_added
                lots_to_be_added=0
            if indicator==-1:
                exclusive_strike,yet_to_place=order_button(exclusive_strike,'PE_B',lots_to_be_added)
                tron+=lots_to_be_added
                lots_to_be_added=0
    return exclusive_strike,tron,start,indicator,lots_to_be_added

def extra_lots_decider():
    a=datetime.today().weekday()
    if a==4:
        return 1
    if a!=4:
        return a+1

def surya(x,option_chain,c_strike_b,p_strike_b,c_leg_tron,p_leg_tron,exclusive_strike,strangle_c_strike,strangle_p_strike,strangle_tron,indicator):
    if strangle_tron>0:
        strangle_c_strike=(exclusive_strike==0)*strangle_c_strike+exclusive_strike
        strangle_p_strike=(exclusive_strike==0)*strangle_p_strike+exclusive_strike
        ce_data=option_chain[option_chain['CPType']=='CE']
        pe_data=option_chain[option_chain['CPType']=='PE']
        c_lastrate=float(ce_data[ce_data['StrikeRate']==c_strike_b]['LastRate'])
        p_lastrate=float(pe_data[pe_data['StrikeRate']==p_strike_b]['LastRate'])
        call_factor=max(100,int(np.ceil((c_lastrate)/100)*100))
        put_factor=max(100,int(np.ceil((p_lastrate)/100)*100))
        new_p_strike_b,new_c_strike_b=0,0
        extra_lots=extra_lots_decider()
        if x>c_strike_b and c_lastrate>100 and indicator<0:
            new_c_strike_b,y=order_button(c_strike_b+call_factor,'CE_B',c_leg_tron+extra_lots)
            while y!=0:
                if strangle_tron==0:
                    break
                order_button(strangle_c_strike,'CE_B',1)
                order_button(strangle_p_strike,'PE_B',1)
                strangle_tron-=1
                new_c_strike_b,y=order_button(c_strike_b+call_factor,'CE_B',c_leg_tron+extra_lots)
                
            o,y=order_button(c_strike_b,'CE_S',c_leg_tron+extra_lots)
            while y!=0:
                if strangle_tron==0:
                    break
                order_button(strangle_c_strike,'CE_B',1)
                order_button(strangle_p_strike,'PE_B',1)
                strangle_tron-=1
                o,y=order_button(c_strike_b,'CE_S',c_leg_tron+extra_lots)
            c_leg_tron+=extra_lots
        elif x<p_strike_b and p_lastrate>100 and indicator>0:
            new_p_strike_b,y=order_button(p_strike_b-put_factor,'PE_B',p_leg_tron+extra_lots)
            while y!=0:
                if strangle_tron==0:
                    break            
                order_button(strangle_c_strike,'CE_B',1)
                order_button(strangle_p_strike,'PE_B',1)
                strangle_tron-=1
                new_p_strike_b,y=order_button(p_strike_b-put_factor,'PE_B',p_leg_tron+extra_lots)
            o,y=order_button(p_strike_b,'PE_S',p_leg_tron+extra_lots)
            while y!=0:
                if strangle_tron==0:
                    break            
                order_button(strangle_c_strike,'CE_B',1)
                order_button(strangle_p_strike,'PE_B',1)
                strangle_tron-=1
                o,y=order_button(p_strike_b,'PE_S',p_leg_tron+extra_lots)
            p_leg_tron+=extra_lots
        new_c_strike_b,new_p_strike_b=c_strike_b*(new_c_strike_b==0)+new_c_strike_b,p_strike_b*(new_p_strike_b==0)+new_p_strike_b
    if strangle_tron==0:
        new_c_strike_b,new_p_strike_b=c_strike_b,p_strike_b
    return new_c_strike_b,new_p_strike_b,c_leg_tron,p_leg_tron,strangle_tron

def intel_strike_mover(x,c_strike_intel,p_strike_intel,tron_intel,strangle_c_strike,strangle_p_strike,strangle_tron):
    at_strike=int(np.round((x)/100)*100)
    new_c_strike_intel=c_strike_intel
    new_p_strike_intel=p_strike_intel
    if c_strike_intel-x>53:
        order_button(c_strike_intel,'CE_B',tron_intel)
        new_c_strike_intel,y=order_button(at_strike,'CE_S',tron_intel)
        while y!=0:
            if strangle_tron==0:
                break            
            order_button(strangle_c_strike,'CE_B',1)
            order_button(strangle_p_strike,'PE_B',1)
            strangle_tron-=1
            o,y=order_button(at_strike,'CE_S',tron_intel)
    if x-p_strike_intel>53:
        order_button(p_strike_intel,'PE_B',tron_intel)
        new_p_strike_intel,y=order_button(at_strike,'PE_S',tron_intel)
        while y!=0:
            if strangle_tron==0:
                break            
            order_button(strangle_c_strike,'CE_B',1)
            order_button(strangle_p_strike,'PE_B',1)
            strangle_tron-=1
            o,y=order_button(at_strike,'PE_S',tron_intel)
    return new_c_strike_intel,new_p_strike_intel

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
    tron=finalise_tron(c_strike=exclusive_strike,p_strike=exclusive_strike,tron=tron,to_take_c_strike=1,to_take_p_strike=1)
    return exclusive_strike,tron

def exit_signal(option_chain,exclusive_strike):
    ind_time = datetime.now(timezone("Asia/Kolkata")).strftime('%Y-%m-%d %H:%M:%S.%f')
    temp=np.sum(option_chain[option_chain['StrikeRate']==exclusive_strike]['LastRate'])
    if temp<66 or int(ind_time[11:13])*60+int(ind_time[14:16])>925:
        return 1
    else:
        return 0

def exit_trades(exclusive_strike,tron):
    order_button(exclusive_strike,'PE_B',tron)
    order_button(exclusive_strike,'CE_B',tron)   

def straddle_special_adjustment(exclusive_strike,x,tron,indicator,option_chain):
    if exclusive_strike!=0 and tron!=0 and np.sign(x-exclusive_strike)==indicator:
        def exclusive_strike_change_signal(earlier_x,x,option_chain):
            ce_data=option_chain[option_chain['CPType']=='CE']
            pe_data=option_chain[option_chain['CPType']=='PE']
            c_lastrate=float(ce_data[ce_data['StrikeRate']==exclusive_strike]['LastRate'])
            p_lastrate=float(pe_data[pe_data['StrikeRate']==exclusive_strike]['LastRate'])
            premium_sum=c_lastrate+p_lastrate
            a=2*(x-earlier_x)/premium_sum
            return abs(a)
        if exclusive_strike_change_signal(earlier_x=exclusive_strike,x=x,option_chain=option_chain)>1:
            exclusive_strike,tron=exclusive_strike_change_trades(exclusive_strike,x,tron)
        #if exit_signal(option_chain,exclusive_strike)==1 and exclusive_strike!=0:
        #    exit_trades(exclusive_strike,tron) 
        #    exclusive_strike=0 
        #    tron=0 
    return exclusive_strike,tron

def indicator_(x,market_ripper,day_volume_indicator,day_market_ripper,rosetta,rosetta_ratio,oi_ratio,hightime,time,volume_ind):
    def node_out(input_,weights_bias):
        return np.tanh(weights_bias[0]*input_[0]+weights_bias[1]*input_[1]+weights_bias[2]*input_[2]+weights_bias[3]*input_[3]+weights_bias[4]*input_[4]+weights_bias[5]*input_[5]+weights_bias[6]*input_[6]+weights_bias[7]*input_[7]+weights_bias[8]*input_[8]+weights_bias[9])
    input_=[market_ripper,day_volume_indicator,day_market_ripper,hightime,oi_ratio,rosetta_ratio,rosetta,time/22440,volume_ind]
    x_=np.reshape(x,(82,len(input_)+1))
    index=0
    for j in range(0,9):
        A=[]
        for i in range(0,9):
            A+=[node_out(input_,x_[index])]
            index+=1
        input_=A
    ultimatum=node_out(input_,x_[index])
    final_indicator=np.array(ultimatum>0)+np.array(ultimatum<0)*-1
    return final_indicator

def blue_factor(option_chain,x):
    final_chain=option_chain[(option_chain['StrikeRate']>x-1000) & (option_chain['StrikeRate']<x+1000)]
    p=final_chain[final_chain['CPType']=='PE']
    c=final_chain[final_chain['CPType']=='CE']
    strikes=p['StrikeRate']
    p_lastrates=p['LastRate']
    c_lastrates=c['LastRate']
    f_p = interpolate.interp1d(strikes, p_lastrates,kind='quadratic')
    f_c = interpolate.interp1d(strikes, c_lastrates,kind='quadratic')
    return (f_p(x)+f_c(x))/2

def options_indicator(option_chain,x,cv,pv,earlier_cv,earlier_pv,main_cv,main_pv,day_coi,day_poi,c_oi,p_oi):
    ind_time = datetime.now(timezone("Asia/Kolkata")).strftime('%Y-%m-%d %H:%M:%S.%f')
    ce_data=option_chain[option_chain['CPType']=='CE']
    pe_data=option_chain[option_chain['CPType']=='PE']
    p_strikerates=np.array(list(pe_data['StrikeRate']))
    c_strikerates=np.array(list(ce_data['StrikeRate']))
    p_lastrate=np.array(list(pe_data['LastRate']))
    c_lastrate=np.array(list(ce_data['LastRate']))
    p_openinterest=np.array(list(pe_data['OpenInterest']))
    c_openinterest=np.array(list(ce_data['OpenInterest']))
    p_volume=np.array(list(pe_data['Volume']))
    c_volume=np.array(list(ce_data['Volume']))
    p_volume_change=p_volume-earlier_pv
    c_volume_change=c_volume-earlier_cv
    cv_temp=np.sum(np.multiply(c_volume_change,c_lastrate))
    pv_temp=np.sum(np.multiply(p_volume_change,p_lastrate))
    coi_temp=np.sum(np.multiply(c_openinterest,c_lastrate))
    poi_temp=np.sum(np.multiply(p_openinterest,p_lastrate))
    day_coi+=coi_temp
    day_poi+=poi_temp
    c_oi+=coi_temp
    p_oi+=poi_temp
    uu=c_oi/p_oi
    day_uu=day_coi/day_poi
    oi_davat=((2*uu*uu)/(1+uu*uu))-1
    day_oi_davat=((2*day_uu*day_uu)/(1+day_uu*day_uu))-1
    cv=cv+cv_temp
    pv=pv+pv_temp
    cc=cv/(pv+0.1)
    v_ind=((2*cc*cc)/(1+cc*cc))-1

    main_cv=main_cv+cv_temp
    main_pv=main_pv+pv_temp
    main_cc=main_cv/(main_pv+0.1)
    main_v_ind=((2*main_cc*main_cc)/(1+main_cc*main_cc))-1


    earlier_pv=p_volume
    earlier_cv=c_volume
    average_p_strike=np.dot(p_strikerates,p_openinterest)/np.sum(p_openinterest)
    average_c_strike=np.dot(c_strikerates,c_openinterest)/np.sum(c_openinterest)
    p1=x-average_p_strike
    c1=average_c_strike-x
    oi_ratio=np.sum(p_openinterest)/np.sum(c_openinterest)
    i=np.array(pe_data['StrikeRate'])[0]
    end=np.array(pe_data['StrikeRate'])[-1]
    ss=np.array(pe_data['StrikeRate'])
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
    x1=x-np.round_(a[0],1)
    factor5=blue_factor(option_chain,x)
    pp=p_lastrate[np.multiply(p_lastrate!=0, p_openinterest!=0)]
    po=p_openinterest[np.multiply(p_lastrate!=0, p_openinterest!=0)]
    cp=c_lastrate[np.multiply(c_lastrate!=0, c_openinterest!=0)]
    co=c_openinterest[np.multiply(c_lastrate!=0, c_openinterest!=0)]

    a1=np.dot(np.array(pp),np.array(po))
    a2=np.dot(np.array(cp),np.array(co))
    aa=a1/a2
    hightime_indicator= ((2*(c1/p1)*(c1/p1))/(1+(c1/p1)*(c1/p1)))-1
    rosetta_indicator=x1/factor5
    rosetta_ratio_indicator=((2*aa*aa)/(1+aa*aa))-1
    oi_ratio_indicator=((2*oi_ratio*oi_ratio)/(1+oi_ratio*oi_ratio))-1
    xopt=[ 1.83470370e+01,  1.45728705e+01,  1.41472216e+01, -6.88230338e+00,
       -8.75698332e+00, -2.06859319e+01, -1.18086614e+01,  1.39622014e+01,
       -5.75393989e+00,  4.73370187e+00,  2.48271771e+01, -1.11266281e+01,
       -9.20013764e+00,  1.37846619e+01, -1.92582248e+01, -2.34012332e+01,
        9.61221910e+00,  1.03919993e+01, -3.48786893e+00,  2.12263036e+01,
        1.43668658e+01, -2.01223757e+01, -2.92780384e+01, -4.36814770e+00,
        1.88358468e+01,  9.80858384e+00,  2.85297812e+01, -3.86630553e+00,
       -1.46802026e+01, -3.00000000e+01,  2.29923601e+00, -8.22205952e+00,
        1.51065500e+01, -1.97383607e+01, -2.11078725e-02, -3.00000000e+01,
        1.67016251e+01,  1.35856612e+01, -1.10747763e+01, -6.40618409e+00,
        6.08068368e+00,  1.00231352e+01,  1.21616648e+01, -1.24424641e+01,
       -9.18686595e+00, -1.50132096e+01,  1.89310064e+01, -1.01666771e+00,
        4.64600937e-01,  2.11663819e+01,  1.94336698e+01, -4.09104894e+00,
        1.10963430e+00, -2.39419175e+01,  2.83035181e+01,  7.24378220e+00,
        2.29126589e+00,  7.01194816e+00, -2.49591398e+01, -1.66721431e+01,
        5.10303950e+00, -2.39198189e+01, -2.42762850e+01,  2.87040165e+01,
        1.70968196e+01,  2.96541493e+01,  1.37816069e+01, -3.55672188e+00,
       -5.62280851e+00, -1.62093867e+01, -5.32768067e+00,  2.20327409e+00,
        8.98977519e+00,  9.52593374e+00,  7.63361582e-02, -2.23340529e+01,
       -6.85167183e+00,  1.91426134e+01,  2.34463289e+01, -2.70711941e+01,
       -1.29688855e+01,  5.62758599e+00,  1.91451240e+00, -2.67592467e+01,
        1.89595664e+01, -3.46547357e+00, -3.00000000e+01, -5.65046053e+00,
        4.62151554e+00, -9.26513016e-01, -1.18956969e+01, -1.14880137e+01,
        1.67321031e+01,  2.16781388e+01, -6.77749242e+00, -6.17643292e+00,
        1.33628813e+01, -5.58527286e+00,  5.21577736e+00, -2.59235409e+01,
       -3.43396094e+00,  1.13038600e+01, -2.95142304e+00, -1.98564894e+01,
       -2.68934843e+01, -3.67507736e+00, -6.30856684e+00, -8.57027929e+00,
        8.52857414e+00,  7.28818577e+00, -3.68080635e+00, -1.06888580e+01,
        3.67433451e+00,  9.08843641e+00, -8.78509939e+00,  1.36408310e+01,
       -1.72001894e+01,  2.87315006e+00, -2.00643525e+01,  2.34675406e+01,
       -1.43116305e+00, -6.07203957e+00,  4.79124490e-01, -1.81128338e+01,
       -1.84252055e+01, -1.60252249e+01,  2.07295221e+00,  2.96458600e+01,
       -1.23775800e+01,  2.55807935e+01, -4.84929811e+00,  1.25657552e+01,
       -2.04851817e+01, -1.74978558e+01,  1.58041535e+01,  2.27540734e+01,
        1.92577604e+01,  7.74395614e-01, -2.58280100e+01, -4.79056848e+00,
       -1.15375373e+01,  5.68246453e+00, -1.65025062e+01, -1.91208771e+01,
       -2.72862773e+01, -1.64710603e+01, -1.28148676e+01, -5.18744239e+00,
       -5.40964725e+00, -1.17708198e+01,  5.85225734e+00,  2.46051951e+01,
        1.11464446e+01, -3.24666944e+00, -2.54832266e+01, -1.16593123e+01,
       -4.24061349e+00, -4.33543882e+00, -2.12931276e-01,  5.33841483e+00,
       -1.71679469e+01, -4.66474235e+00, -1.20721823e+01, -1.81359121e+01,
        3.16593465e+00, -2.28100234e+00,  1.27507981e+01, -1.69475628e+01,
        1.25143598e+01, -1.03902498e+01,  2.25861816e+00,  1.85445654e+00,
        1.22651143e+01,  2.96868018e+00,  1.51202655e+01,  2.45601485e+01,
       -6.47109955e+00,  1.18274274e+01,  1.76322340e+01, -1.47131295e+01,
        2.49236830e+01, -2.75229008e+01, -1.25792537e+00,  1.84466703e+01,
       -2.08613120e+01, -7.10574799e-01,  1.55689891e+01, -5.14042339e-01,
       -1.65827680e+01, -7.38615206e+00, -2.37436860e+01, -5.21631342e+00,
       -1.28292910e+01, -2.00526304e+01, -1.64976777e+01,  4.53889264e-01,
       -9.36039754e-01, -1.88234259e+01, -1.00436184e+01, -9.98277260e+00,
        5.64951420e+00, -2.28866826e+01, -5.36005318e+00,  1.28602123e+01,
        3.87781939e+00, -2.52151091e+01,  5.45969310e+00, -1.30783108e+01,
        1.29529589e+01,  1.27107714e+00, -3.26528469e+00,  2.92667839e+00,
        1.79410779e+01,  9.02835517e-01,  5.08809498e-01, -2.47336474e+00,
       -1.85937733e+01, -9.14033269e+00, -6.55242669e+00,  1.50856310e+01,
       -3.63214494e+00, -1.70461735e+01, -2.23662312e-01,  2.72651363e+00,
        3.00250627e+00, -1.03040419e+01,  6.76130934e+00,  8.10814997e+00,
        1.48325848e+01,  8.20296765e+00,  1.52680900e+01,  1.49065556e+00,
       -2.09173582e+01,  1.27290974e+01,  1.87980032e+01, -2.87349606e+01,
        1.05223440e+01,  2.61867780e+01, -5.55174954e+00, -4.99270110e+00,
       -1.00653469e+01,  2.25519604e+01, -1.13700720e+01, -1.17423350e+00,
       -1.87099320e+00,  7.46502765e+00, -2.67369059e+01,  1.88474464e+01,
       -4.44463013e+00, -6.01820606e+00, -1.87348720e+00, -7.02443843e+00,
       -7.85910430e+00, -1.69627428e+01, -1.57506185e+01, -2.10005143e+01,
        6.52347854e+00,  1.43595507e+01, -1.44610907e+01, -5.08982955e+00,
        6.14063665e+00,  1.60008830e+01,  2.64130742e+01,  1.39064292e+01,
       -5.41684585e+00,  2.82075500e+00,  1.12788112e+01, -5.07919357e-01,
        6.41463736e+00,  1.70462151e+00,  2.13742248e+01, -1.74868698e+00,
        4.93957211e+00, -1.61020059e+01,  2.02320102e+01,  3.14638576e+00,
        1.80004330e+00, -3.10229425e+00, -2.48334390e+01, -2.48882337e+01,
       -7.81376728e+00, -2.49527338e+01,  1.93986518e+01,  1.92887763e+01,
       -8.41620551e+00,  1.65374785e+01,  7.80214694e+00,  1.18196790e+01,
        1.25140320e+01,  1.65136196e+01,  1.95613602e+01,  6.50630372e+00,
        4.55048564e+00,  1.04071300e+01,  1.81345181e+01, -9.77205818e+00,
       -6.33343339e+00,  1.66763899e+01, -7.78457275e+00,  9.41761730e+00,
        1.01776546e+01,  6.68203344e+00,  2.32057810e+01,  9.12378722e+00,
        2.67661699e+00, -1.97550662e+01,  1.02593090e+01, -1.18382915e+01,
       -6.98399899e+00,  1.52654918e+01, -2.27301831e+01, -2.45850783e+01,
        8.03622702e+00, -2.01945947e+00, -8.16504049e+00,  3.81581978e+00,
       -3.96023276e-01,  5.02865552e+00,  1.88032683e+01, -2.78783987e+01,
       -8.54653646e+00, -1.12595728e+00, -1.16211955e+01,  3.38045519e+00,
        9.47166326e+00,  1.23495019e+01, -3.13689481e+00, -6.36458165e+00,
        1.07820415e+01,  1.90361413e+00,  1.40395873e+01, -3.34411759e+00,
        8.38648889e+00,  2.38942068e+01,  2.67700292e+01,  1.66147195e+01,
        4.68114575e+00,  8.61673145e+00, -2.46970786e+00,  3.38054841e+00,
       -7.53296750e-01,  9.18714213e+00,  7.38544797e+00, -6.72502466e+00,
       -8.86050099e+00, -1.70117131e+00,  1.41547592e+01, -2.01349911e+01,
        2.50262235e+00, -1.07698788e+01,  2.16695817e+01,  1.55273509e+01,
        6.62017712e+00, -5.45605889e+00, -4.93735428e+00, -8.77898540e+00,
        1.40297850e+01, -8.85927919e+00, -6.14513004e+00,  1.40151128e+01,
        3.29179154e+00, -1.48204362e+01, -1.62090327e+01, -2.21136974e+01,
        1.45317502e+01,  1.59894481e+01, -3.01737140e+00, -1.21649464e+01,
        9.79158195e-01,  2.77181337e+01, -1.56618836e+01,  7.32993408e+00,
        1.54911660e+01,  7.58169967e+00,  5.54334777e+00, -1.23333115e+01,
       -1.27906187e+00, -9.97004066e+00,  1.62923977e+01, -2.13503570e-01,
       -8.68758476e-01,  2.07496226e+01, -3.18243475e+00, -7.46262352e+00,
       -7.81876663e+00, -1.16142374e+01,  2.20456986e+01, -1.19061926e+00,
       -9.92263676e+00,  2.44191796e+01, -2.45854192e+01,  2.26484430e+01,
        9.46034345e+00, -2.28228337e+00,  1.30846369e+01,  1.12475326e+01,
       -4.33064542e+00,  1.03879293e+01,  1.49007996e+01,  4.48159071e-01,
       -7.39785932e+00, -2.20444170e+00, -5.27180976e+00, -8.72522562e+00,
       -6.15349521e+00, -2.09506774e+00,  3.41134806e+00,  2.72244488e+01,
        4.51808479e+00,  1.13927909e+01, -8.09934037e+00, -1.67283246e+00,
        8.17723870e-01, -9.51795387e+00,  7.12363892e+00,  1.40538274e+01,
       -9.88751139e+00, -1.23842944e+01, -2.07932361e+01,  1.70854693e+01,
       -8.10197684e+00,  1.49190047e+01, -9.36949885e-01, -1.74572890e+00,
        6.22625735e-01,  1.72367239e+01, -6.70163424e+00, -4.72214064e+00,
       -1.03793235e+00,  1.28289314e+01, -9.67403223e+00, -2.51423933e+01,
       -1.08649616e+01,  3.00000000e+01, -2.36148766e+01,  1.25021964e+01,
       -1.93988930e+00,  3.16043771e+00, -2.21950349e+01,  9.98995892e+00,
       -1.69643624e+01, -2.45989294e+01,  2.48141358e+01, -2.76572568e+00,
       -1.56170852e+01,  1.25279647e+01,  2.07662831e+00,  1.03141571e+01,
       -9.45040454e+00, -3.02101559e+00, -1.57019351e+01, -1.36078747e+01,
       -1.92301804e+01,  2.12571749e+01,  1.47847193e+01, -2.95973752e+00,
       -1.91716652e+01, -4.92077664e-01,  1.14839866e+01,  1.17975640e+00,
        2.41749706e+01,  4.49943967e+00, -1.79775154e+01,  3.97449971e+00,
       -7.97483880e+00,  9.99411053e+00, -1.04109197e+01, -1.00519112e+01,
        1.67393003e+01, -1.74175380e+01, -1.11127808e+01, -2.03425498e+00,
        2.94816732e-01,  9.30765399e+00, -1.59220826e+01, -1.38557705e+01,
        2.29571208e+00,  5.64840922e+00, -5.93326924e+00, -9.88087851e+00,
        4.52711912e+00,  2.06418479e+01,  4.29062216e+00, -1.00552613e+01,
        1.01678339e+01,  9.08533507e+00,  1.94053295e+01, -1.59222772e+01,
        5.11640314e+00, -2.97451005e+01,  1.08763776e+01,  1.06929629e+00,
        9.46177099e+00, -1.98891183e+00, -9.77466866e+00, -3.62536238e+00,
        2.77064145e+00,  1.54450822e+01,  2.12674618e+01, -7.46519721e+00,
        3.96122510e+00, -5.34778751e-01, -1.53627217e+01, -2.98060985e+01,
       -6.60382121e+00,  7.90737872e+00,  2.58165566e+01,  5.80123601e+00,
       -1.41547404e+01,  1.04595326e+01,  1.32736379e+00,  1.22214581e+01,
        2.69362918e+01, -7.02744379e-01, -2.26912074e+01, -4.76310820e+00,
       -1.28806442e+00, -5.31249684e+00, -7.33419815e+00, -2.09105485e+01,
       -8.08748774e+00,  1.79220159e+01, -2.10510940e+01, -5.96544400e+00,
        1.61184968e+01, -8.45430620e+00,  2.59233639e+01,  1.66649531e+01,
        2.41719599e+01,  1.21442943e-01, -1.10133024e+01,  2.28837733e+01,
        3.00000000e+01,  1.14550063e+01, -8.74314222e+00,  6.74193693e+00,
        5.02717483e+00,  9.47970027e+00, -1.11193940e+00,  9.50541989e+00,
       -3.29255964e+00, -7.07756543e+00,  9.73738647e+00, -3.21280985e-01,
       -3.16731149e+00,  1.16429211e+01, -1.68520720e+01, -4.64876612e+00,
       -4.27813383e+00, -2.83519765e+01,  3.97856671e+00,  2.64947743e+01,
        3.29230801e+00, -7.31948324e+00,  4.85919738e+00, -9.09089113e+00,
        1.97156710e+01,  1.36428237e+01,  8.55950812e+00, -5.19954602e+00,
       -1.85450510e+01, -5.83929971e+00, -1.07830852e+01, -1.40244548e+01,
       -1.36206659e+01, -1.40469537e+01, -2.18673459e+01,  2.52131995e+01,
        1.23040721e+01, -1.78176636e+01, -9.40547352e+00, -2.18073125e+01,
       -1.29022276e+01, -1.41593286e+01, -1.01127956e+00, -2.16203232e+01,
        1.67804755e+01, -7.51942691e+00, -1.47451839e+01, -1.28557143e+01,
       -1.79878107e+01,  2.81292011e+01,  1.93544188e+01, -1.05496741e+01,
       -7.92964879e+00,  2.46408677e+01,  6.22675295e+00,  2.20151234e+01,
        4.11000765e+00, -2.33007218e+00, -8.33148768e+00,  1.46385398e+01,
       -1.76191519e+01,  1.98130752e+01,  8.72366081e+00, -1.93637012e+01,
       -1.66403229e+01,  2.42661579e+01,  1.18733056e+01,  6.44950633e+00,
       -3.03017789e-01, -1.46782995e+01,  1.67803654e+01, -6.54356269e+00,
        3.18601657e+00,  7.22178432e+00, -1.83666643e+01, -1.00768265e+01,
        1.80335235e+01, -1.01952069e+01, -6.59579329e+00,  3.14553973e+00,
       -5.42215699e+00,  9.64644893e-01, -2.01813224e+01,  9.29732575e+00,
       -4.55492551e+00, -2.44674105e+01, -1.99763283e+01,  6.59423014e+00,
       -5.38276973e+00,  9.94294400e+00,  1.32011676e+01, -1.34240850e+01,
        9.35200012e+00, -1.82526498e+01, -4.33682828e+00,  1.72890326e+01,
        2.05463954e+01, -1.08753688e+01, -3.10791821e+00, -5.38255110e+00,
        7.89501082e-02,  4.50851955e+00,  1.48288498e+01, -1.67401809e+01,
       -9.06420519e+00,  2.48691430e+01,  1.17402037e+01, -2.21761440e+01,
       -2.01362649e+01, -2.36296314e+01,  1.53262159e+01,  1.11075962e+01,
        2.05491235e+01, -1.79991938e+01,  1.97358876e+01,  8.14074478e+00,
        5.84496912e+00, -1.46318881e+01,  7.55350513e+00, -4.57499008e+00,
       -1.79988019e+01, -1.97149242e+01,  1.15758797e+01,  1.56382627e+01,
        5.40615411e+00,  1.19752930e+00, -1.56233899e+01,  1.63099721e+01,
        8.96440227e+00,  2.85838972e+01,  1.96123987e+00, -1.44663331e+01,
        4.64670037e+00,  2.88927851e-01,  1.54145158e+01,  2.24342736e+01,
       -1.16615566e+01,  2.15826028e+01,  1.23176891e+01, -1.92752350e+01,
       -1.03993969e+01,  1.12469941e+01, -1.23222782e+01, -1.15402490e+01,
       -2.88233883e+01, -1.10414942e+01,  1.64426004e+01,  1.50227810e-01,
       -2.42919146e+01,  9.41393304e+00, -8.63257917e+00,  1.79313537e+01,
       -1.36480830e+01,  1.45123445e+01,  2.77446395e+00, -4.01682429e-01,
       -1.53738919e+01,  5.72396337e-01, -3.54972784e+00, -1.99930788e+01,
       -9.22333369e+00,  2.31191373e+01, -1.26699045e+01, -6.94377426e+00,
       -2.06914393e+01,  1.65227673e+01, -1.76781535e+01,  2.80885549e+00,
       -2.83942205e+01,  3.91149205e+00, -1.88794403e+01,  2.06415836e+01,
        2.62890807e+01,  1.48338951e+01,  3.94217445e+00, -2.11299673e+01,
        8.67763672e+00,  1.42254526e+01, -1.18800287e+01, -5.33825838e+00,
       -1.76999624e+01, -1.49246519e+01, -1.06980697e+00,  1.21975990e+01,
        1.29526903e+01,  1.57076698e+01,  6.83138034e+00,  3.27725302e+00,
        8.09869165e+00, -2.13334757e+01, -7.04527961e+00,  1.77731125e-01,
        6.17487068e+00, -5.58259684e+00,  2.68876105e+01,  5.62638530e+00,
       -2.72422137e+01, -4.77613018e+00, -1.19607440e+00, -1.05468645e+01,
       -2.29271193e+01, -2.31078595e+01, -1.07597988e+01, -8.04839018e+00,
       -9.84791403e+00,  2.39485158e+01,  8.14301430e+00, -2.08460202e+01,
        7.94696760e+00, -1.13300943e+01,  1.90334639e+01,  5.12037049e+00,
        5.26524656e+00, -3.91680597e-01,  9.50011138e-01, -1.77724947e+01,
        3.32069273e+00, -9.19633883e+00, -5.87311072e+00, -9.48478904e+00,
        1.65976247e+00, -3.25571553e+00, -2.35897448e+01,  7.47045363e+00,
        1.03688999e+01, -6.41868587e+00, -1.39662297e+01,  2.33805281e+00,
        3.69727527e+00,  2.00680835e+01,  1.04719995e+01, -6.19538373e+00,
        7.38632583e+00,  1.53710533e+01, -1.31427089e+01,  4.13455160e+00,
       -2.52205330e+01,  7.52673608e+00, -1.74031251e+01, -1.98772329e+01,
       -8.34391071e+00, -5.91201069e+00, -3.52697811e+00,  8.03928154e+00,
        1.69169571e+01,  1.33765145e+01,  3.10552751e+00,  3.34352973e+00,
        1.28299911e+00,  1.18133115e+01, -2.06998514e+01,  1.89190421e+01,
        1.75352137e+01, -1.27644292e+01, -1.63356223e+01, -1.33512609e+01,
       -2.25823874e+00, -1.80188192e+01,  7.90608958e-01, -1.73910180e+01,
       -3.80538985e+00,  5.07047268e+00,  2.26795356e+01,  1.11935863e+01,
       -4.50283150e+00,  1.00752711e+01, -7.02204793e+00,  1.86882737e+01,
        2.82441159e+01,  1.12244540e+01, -9.90088403e+00, -2.62243897e+01,
       -9.99865447e+00,  2.16729651e+01,  1.73336877e+01, -1.20438898e+01,
       -1.98962367e+01, -9.87347183e-01,  9.04527577e+00,  1.41345948e+00,
       -1.43600967e+01, -2.12974356e+01,  1.87448244e+01,  5.04432340e+00,
        3.69295422e+00,  1.25410184e+01, -1.50000229e+01,  1.74943443e+00]
    time=int(ind_time[11:13])*60*60+int(ind_time[14:16])*60-33300
    final=indicator_(xopt,oi_davat,v_ind,day_oi_davat,rosetta_indicator,rosetta_ratio_indicator,oi_ratio_indicator,hightime_indicator,time,main_v_ind)
    return  final,cv,pv,earlier_cv,earlier_pv,main_cv,main_pv,day_coi,day_poi,c_oi,p_oi

#%%
client_name = input('enter the client name: ')
prime_client=client_login(client=client_name)
option_chain,x=data(week=0)

ce_data=option_chain[option_chain['CPType']=='CE']
pe_data=option_chain[option_chain['CPType']=='PE']
earlier_pv=np.array(list(pe_data['Volume']))
earlier_cv=np.array(list(ce_data['Volume']))
cv,pv,day_coi,day_poi=0,0,0,0
a=datetime.today().weekday()
if a==4:
    main_cv,main_pv,c_oi,p_oi=0,0,0,0
else:
    indicator_json=json.load(open('indicator_variables.json'))
    main_cv,main_pv,c_oi,p_oi=indicator_json['main_cv'],indicator_json['main_pv'],indicator_json['c_oi'],indicator_json['p_oi']

start=int(input('enter 0 if starting the strategy for the first time, else 1 :  '))
from_json=input('to take positions from existing positions json file (y/n): ')
if start==0:
    leg_tron=int(input('leg_tron'))
    tron_intel=leg_tron
    tron=int(prime_client['login'].margin()[0]['AvailableMargin']/140000)
    ind_time = datetime.now(timezone("Asia/Kolkata")).strftime('%Y-%m-%d %H:%M:%S.%f')
    while int(ind_time[11:13])*60+int(ind_time[14:16])<555 :
        ind_time = datetime.now(timezone("Asia/Kolkata")).strftime('%Y-%m-%d %H:%M:%S.%f')
    sleep(80)
    option_chain,x=data(week=0)
    c_leg_tron,p_leg_tron,c_strike_b,p_strike_b,c_strike_intel,p_strike_intel=initial_leg_trades(x,option_chain,leg_tron)
    strangle_tron,strangle_c_strike,strangle_p_strike=initial_strangle_trades(option_chain,x)
    exclusive_strike=0
    buying_exclusive_strike=0
    tron_buyer=1
    start_buy_kick_off=0
    lots_to_be_added=0
    earlier_indicator,cv,pv,earlier_cv,earlier_pv,main_cv,main_pv,day_coi,day_poi,c_oi,p_oi=options_indicator(option_chain,x,cv,pv,earlier_cv,earlier_pv,main_cv,main_pv,day_coi,day_poi,c_oi,p_oi)
elif start==1 and from_json=='n':
    c_leg_tron=int(input('enter number of existing lots on call side buy: '))
    p_leg_tron=int(input('enter number of existing lots on put side buy: '))
    c_strike_b=int(input('enter the call bought strike: '))
    p_strike_b=int(input('enter the put bought strike: '))
    strangle_tron=int(input('strangle tron:  '))
    strangle_c_strike=int(input('enter strangle call strike: '))
    strangle_p_strike=int(input('enter strangle put strike: '))
    tron_intel=int(input(' tron_intel:  '))
    c_strike_intel=int(input('enter call_strike_intel: '))
    p_strike_intel=int(input('enter put_strike_intel: '))
    exclusive_strike=int((strangle_c_strike==strangle_p_strike)*strangle_p_strike)
    start_buy_kick_off=1
    lots_to_be_added=0
    buying_exclusive_strike=int(input('enter the exclusive_strike for buy_kick_off: '))
    tron_buyer=int(input('enter the number of lots for buying for buy_kick_off'))
    earlier_indicator=int(input('enter 1 if call is bought or 0 if put was bought'))
elif start==1 and from_json=='y':
    start_buy_kick_off=1
    positions_record=json.load(open(client_name+'_suryabhai_positions.json'))
    c_leg_tron          =   positions_record['surya']['c_leg_tron']
    p_leg_tron          =   positions_record['surya']['p_leg_tron']
    c_strike_b          =   positions_record['surya']['c_strike_b']
    p_strike_b          =   positions_record['surya']['p_strike_b']
    strangle_tron       =   positions_record['strangle']['tron']
    strangle_c_strike   =   positions_record['strangle']['c_strike']
    strangle_p_strike   =   positions_record['strangle']['p_strike']
    tron_intel          =   positions_record['intel']['tron_intel']
    c_strike_intel      =   positions_record['intel']['c_strike_intel']
    p_strike_intel      =   positions_record['intel']['p_strike_intel']
    exclusive_strike    =   int((strangle_c_strike==strangle_p_strike)*strangle_p_strike)
    buying_exclusive_strike = positions_record['buy_kick_off']['exclusive_strike']
    tron_buyer          =   positions_record['buy_kick_off']['tron']
    earlier_indicator   =   positions_record['buy_kick_off']['earlier_indicator']
    lots_to_be_added    =   positions_record['buy_kick_off']['lots_to_be_added']
ind_time = datetime.now(timezone("Asia/Kolkata")).strftime('%Y-%m-%d %H:%M:%S.%f')
while int(ind_time[11:13])*60+int(ind_time[14:16])<555 :
    ind_time = datetime.now(timezone("Asia/Kolkata")).strftime('%Y-%m-%d %H:%M:%S.%f')
while int(ind_time[11:13])*60+int(ind_time[14:16])<929:
    sleep(60)
    option_chain,x=data(week=0)
    ind_time = datetime.now(timezone("Asia/Kolkata")).strftime('%Y-%m-%d %H:%M:%S.%f')
    B,cv,pv,earlier_cv,earlier_pv,main_cv,main_pv,day_coi,day_poi,c_oi,p_oi=options_indicator(option_chain,x,cv,pv,earlier_cv,earlier_pv,main_cv,main_pv,day_coi,day_poi,c_oi,p_oi)
    #B=int(input('enter B'))
    #x=int(input('enter x'))
    tron_towards_leg=max(c_leg_tron,p_leg_tron)
    exclusive_strike,strangle_c_strike,strangle_p_strike,strangle_tron=strangle_adjustments(x,exclusive_strike,strangle_c_strike,strangle_p_strike,strangle_tron,tron_towards_leg)
    exclusive_strike,strangle_tron=straddle_special_adjustment(exclusive_strike,x,strangle_tron,B,option_chain)
    c_strike_b,p_strike_b,c_leg_tron,p_leg_tron,strangle_tron=surya(x,option_chain,c_strike_b,p_strike_b,c_leg_tron,p_leg_tron,exclusive_strike,strangle_c_strike,strangle_p_strike,strangle_tron,B)
    lots_to_be_added=int(max(c_leg_tron,p_leg_tron))-tron_buyer
    buying_exclusive_strike,tron_buyer,start_buy_kick_off,earlier_indicator,lots_to_be_added=buy_kickoff(start_buy_kick_off,B,earlier_indicator,buying_exclusive_strike,tron_buyer,lots_to_be_added)
    #c_strike_intel,p_strike_intel=intel_strike_mover(x,c_strike_intel,p_strike_intel,tron_intel,strangle_c_strike,strangle_p_strike,strangle_tron)
    if strangle_tron==0:
        if exclusive_strike!=0:
            temp=np.sum(option_chain[option_chain['StrikeRate']==exclusive_strike]['LastRate'])
            if temp>66:
                exclusive_strike==0
                strangle_tron,strangle_c_strike,strangle_p_strike=initial_strangle_trades(option_chain,x)
        elif exclusive_strike==0:
            strangle_tron,strangle_c_strike,strangle_p_strike=initial_strangle_trades(option_chain,x)
positions_json={'strangle':{'c_strike':strangle_c_strike,'p_strike':strangle_p_strike,'tron':strangle_tron},
                'surya':{'c_strike_b':c_strike_b,'p_strike_b':p_strike_b,'c_leg_tron':c_leg_tron,'p_leg_tron':p_leg_tron},
                'intel':{'c_strike_intel':c_strike_intel,'p_strike_intel':p_strike_intel,'tron_intel':tron_intel},
                'buy_kick_off':{'tron':tron_buyer,'exclusive_strike':buying_exclusive_strike,'earlier_indicator':int(B),'lots_to_be_added':lots_to_be_added}}

print(positions_json)
out_file = open(client_name+'_suryabhai_positions.json', "w")
json.dump(positions_json, out_file, default= str)
out_file.close()
indicator_saver={'main_cv':main_cv,'main_pv':main_pv,'c_oi':c_oi,'p_oi':p_oi}
out_file = open('indicator_variables.json', "w")
json.dump(indicator_saver, out_file, default= str)
out_file.close()
# %%