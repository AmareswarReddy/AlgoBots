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

def order_button(exclusive_strike,type,lots):
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

def indicator_(x,rosetta,rosetta_ratio,oi_ratio,hightime,time,volume_ind):
    def node_out(input_,weights_bias):
        return np.tanh(weights_bias[0]*input_[0]+weights_bias[1]*input_[1]+weights_bias[2]*input_[2]+weights_bias[3]*input_[3]+weights_bias[4]*input_[4]+weights_bias[5]*input_[5]+weights_bias[6])
    input_=[hightime,oi_ratio,rosetta_ratio,rosetta,time/22440,volume_ind]
    x_=np.reshape(x,(37,len(input_)+1))
    A=[]
    index=0
    for j in range(0,6):
        for i in range(0,6):
            A+=[node_out(input_,x_[index])]
            index+=1
        input_=A
    ultimatum=node_out(input_,x_[index])
    final_indicator=np.array(ultimatum>0)+np.array(ultimatum<0)*-1
    return final_indicator

def options_indicator(option_chain,x,cv,pv,earlier_cv,earlier_pv):
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
    cv=cv+cv_temp
    pv=pv+pv_temp
    cc=cv/(pv+0.1)
    v_ind=((2*cc*cc)/(1+cc*cc))-1
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
    xopt=[-0.09702805, -0.02774222,  0.55378926, -2.96313939,  1.19334288,
       -3.19807198,  4.8563541 ,  0.70299725, -4.79022922, -3.07004235,
       -3.39736456, -2.76042438,  0.72703678, -0.77301038, -1.0315474 ,
       -0.52605416, -1.68643048,  1.47513187, -3.22458197,  1.17752838,
        1.64466743,  2.85421359,  2.68484325,  3.21756952, -3.4039204 ,
       -2.49279985,  2.62264276, -1.16000144, -0.71743641, -0.52809469,
        0.93796332, -2.48006064, -4.5492052 , -4.47860635, -4.84092251,
        2.69849011, -0.82328699, -1.22595799, -1.47644906,  4.19061613,
       -4.13850665, -3.56562429, -1.02410853,  2.10328234, -0.73471332,
       -4.87116251,  4.1553688 ,  2.07515197,  4.85796599,  2.32856693,
       -0.48523613, -3.28388792,  1.69457639,  4.24429117,  3.27337686,
       -3.0212731 , -2.67307398,  1.85486159,  4.31511389, -3.00009912,
       -4.53687501, -3.08255475,  1.57216276,  1.72437544,  1.32418632,
       -3.54219843,  1.00548173, -0.55409696, -0.83975082,  0.40811389,
       -1.38509254,  4.96333415,  2.93610902,  4.13602421, -0.91337789,
        0.82131323,  0.49595749, -1.84725696, -3.69868339,  0.80692808,
        4.82055492, -1.49276501, -2.74397394, -1.86532553,  2.24418428,
       -2.34771053, -3.2580847 , -0.87371977,  4.72281671, -4.91481174,
       -0.04383425, -4.46414517, -0.01425859, -4.1280046 ,  0.18567847,
        3.21124217, -4.98899951, -2.18594277, -1.0648958 , -0.25075625,
       -0.70749162,  0.94046157,  0.14859448,  2.51105954,  2.29238753,
       -1.1234531 , -1.96151102, -0.18472529, -4.08273114, -1.29209829,
       -0.08543588, -2.48531226,  3.9637678 , -1.33537081,  0.13286034,
        0.63999975, -0.52208015, -0.96723022,  1.90585733,  0.4331294 ,
       -1.37674948, -0.84424503, -4.54405633,  0.26624714,  4.09806745,
        4.23967333, -1.13952994, -3.99662516,  0.40623893,  0.87784154,
        4.85747553, -3.6706699 , -0.41613617, -1.29176608,  4.69486575,
        3.34058262,  0.16199863,  4.46521322,  2.66882853, -3.81648743,
        0.83415794, -1.4991497 , -2.62363046,  1.06093506,  0.8859052 ,
       -0.25577941, -1.11054752,  1.58585146, -0.90375275,  3.5662828 ,
        0.58588628,  1.01597793,  0.16117165, -0.91380891,  0.38426633,
       -0.08490125,  0.20018333, -2.27288874, -0.26701708, -4.39356103,
       -1.3241079 , -3.34420392,  0.15759348,  3.70819631, -3.92221959,
       -0.48533561, -3.36603511, -4.9751526 ,  2.08585967,  3.49154628,
        1.40238831,  3.30360972, -3.47609222, -4.57988593, -1.25571647,
        2.76463116, -2.16531052, -3.64151066, -0.17373024, -0.97690367,
       -2.19376892,  0.59257249,  3.50401689,  4.99757827,  0.82664733,
        3.15508256, -4.97709339, -0.94109201,  2.03269369,  2.55015711,
       -0.28924144, -4.30183326, -2.66554279, -1.33421559,  4.05071557,
        2.10150781, -4.22239197, -2.91679131, -3.64579921,  0.13802189,
       -2.93050888, -3.37067789, -0.40289395, -4.38147119, -4.19180152,
       -2.97365118,  1.69077029,  0.27475866, -3.85563616,  1.88629581,
       -0.51090531,  1.74398014,  1.28756763, -1.67189694, -3.12523125,
        1.16814569, -1.02557142, -0.1462316 ,  2.27993096, -2.23054429,
        0.8318706 , -2.22469263, -4.50491342, -1.19611705, -0.62431663,
       -1.33915455, -1.60433211, -4.81904559, -2.42449894,  1.23967099,
        2.71944133, -1.2379805 , -1.11101951,  2.41118186,  4.44920681,
       -1.07004802, -2.27957568, -2.87292595,  2.07372613,  0.98910246,
       -4.30598118,  3.24334361,  1.27745153, -4.68020352,  1.49190957,
       -1.31095952, -0.27541118, -0.68267334,  3.42536606,  2.02978524,
        3.33200382,  1.53006581,  1.12330552, -0.60412693,  4.99827415,
       -3.60876516, -2.95487617,  2.45500265,  0.59273201]
    time=int(ind_time[11:13])*60*60+int(ind_time[14:16])*60-33300
    final=indicator_(xopt,rosetta_indicator,rosetta_ratio_indicator,oi_ratio_indicator,hightime_indicator,time,v_ind)
    return  final

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

def lots_drop(strike,side,yet_to_place):
    k=yet_to_place
    while yet_to_place>0:
        sleep(1)
        yet_to_place-=1
        xx,pending=order_button(strike,side,yet_to_place)
        if pending==0:
            break
    return k-yet_to_place

def buy_kickoff(start,indicator,earlier_indicator,exclusive_strike,day_of_week,tron):
    if abs(indicator-earlier_indicator)==2:
        indicator=0
    if start==0:
        s=indicator
        if s>0:
            exclusive_strike,yet_to_place=order_button(exclusive_strike,'CE_B',tron)
            tron-=lots_drop(exclusive_strike,'CE_B',yet_to_place)
            #exclusive_strike,yet_to_place=order_button(exclusive_strike,'PE_B',tron)
            #exclusive_strike,yet_to_place=order_button(exclusive_strike-day_of_week,'PE_S',tron)
            start=1
        elif s<0:
            exclusive_strike,yet_to_place=order_button(exclusive_strike,'PE_B',tron)
            tron-=lots_drop(exclusive_strike,'PE_B',yet_to_place)
            #exclusive_strike,yet_to_place=order_button(exclusive_strike,'CE_B',tron)
            #exclusive_strike,yet_to_place=order_button(exclusive_strike+day_of_week,'CE_S',tron)
            start=1
    elif start==1:
        if earlier_indicator==0 and indicator==1:
            exclusive_strike,yet_to_place=order_button(exclusive_strike,'CE_B',tron)
            tron-=lots_drop(exclusive_strike,'CE_B',yet_to_place)
            #exclusive_strike,yet_to_place=order_button(exclusive_strike,'PE_B',tron)
            #exclusive_strike,yet_to_place=order_button(exclusive_strike-day_of_week,'PE_S',tron)
        if earlier_indicator==0 and indicator==-1:
            exclusive_strike,yet_to_place=order_button(exclusive_strike,'PE_B',tron)
            tron-=lots_drop(exclusive_strike,'PE_B',yet_to_place)
            #exclusive_strike,yet_to_place=order_button(exclusive_strike,'CE_B',tron)
            #exclusive_strike,yet_to_place=order_button(exclusive_strike+day_of_week,'CE_S',tron)
        if earlier_indicator==-1 and indicator==0:
            exclusive_strike,yet_to_place=order_button(exclusive_strike,'PE_S',tron)
            #exclusive_strike,yet_to_place=order_button(exclusive_strike,'CE_S',tron)
            #exclusive_strike,yet_to_place=order_button(exclusive_strike+day_of_week,'CE_B',tron)
        if earlier_indicator==1 and indicator==0:
            exclusive_strike,yet_to_place=order_button(exclusive_strike,'CE_S',tron)
            #exclusive_strike,yet_to_place=order_button(exclusive_strike,'PE_S',tron)
            #exclusive_strike,yet_to_place=order_button(exclusive_strike-day_of_week,'PE_B',tron)
    return exclusive_strike,tron,start,indicator


def sell_kickoff(x,start,indicator,earlier_indicator,exclusive_strike,d,tron):
    if abs(indicator-earlier_indicator)==2:
        indicator=0
    if start==0:
        s=indicator
        if s>0:
            exclusive_strike=int(np.round(x/100)*100)-d
            exclusive_strike,yet_to_place=order_button(exclusive_strike,'PE_S',tron)
            tron-=lots_drop(exclusive_strike,'PE_S',yet_to_place)
            start=1
        elif s<0:
            exclusive_strike=int(np.round(x/100)*100)+d
            exclusive_strike,yet_to_place=order_button(exclusive_strike,'CE_S',tron)
            tron-=lots_drop(exclusive_strike,'CE_S',yet_to_place)
            start=1
    elif start==1:
        if earlier_indicator==0 and indicator==1:
            exclusive_strike=int(np.round(x/100)*100)-d
            exclusive_strike,yet_to_place=order_button(exclusive_strike,'PE_S',tron)
            tron-=lots_drop(exclusive_strike,'PE_S',yet_to_place)
        if earlier_indicator==0 and indicator==-1:
            exclusive_strike=int(np.round(x/100)*100)+d
            exclusive_strike,yet_to_place=order_button(exclusive_strike,'CE_S',tron)
            tron-=lots_drop(exclusive_strike,'CE_S',yet_to_place)
        if earlier_indicator==-1 and indicator==0:
            exclusive_strike,yet_to_place=order_button(exclusive_strike,'CE_B',tron)
        if earlier_indicator==1 and indicator==0:
            exclusive_strike,yet_to_place=order_button(exclusive_strike,'PE_B',tron)
    return exclusive_strike,tron,start,indicator


def get_strike_from_scrip(scripcode,exchange):
    if exchange=='BANKNIFTY':
        option_chain,a1=data(0)
    k1=option_chain[option_chain['ScripCode']==scripcode]
    return int(k1['StrikeRate'])


def clear_open_positions():

    S=pd.DataFrame(prime_client['login'].positions())
    for i in range(0,len(S)):
        if ('BANKNIFTY' in S['ScripName'].iloc[i]) and S['NetQty'].iloc[i]!=0:
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



#%%
client_name=input('enter the client name Eg: vinathi,bhaskar ')
#client_name   = 'bhaskar'
tron=int(input('enter the number of lots to trade (Eg:3):'))
typical_tron=1
prime_client=client_login(client=client_name)
d=int(input('enter distance from at strike to trade : '))
exclusive_strike=0
type=''
option_chain,x=data(week=0)
ce_data=option_chain[option_chain['CPType']=='CE']
pe_data=option_chain[option_chain['CPType']=='PE']
earlier_pv=np.array(list(pe_data['Volume']))
earlier_cv=np.array(list(ce_data['Volume']))
cv,pv=0,0
earlier_indicator=options_indicator(option_chain,x,cv,pv,earlier_cv,earlier_pv)
start=0
#%%
ind_time = datetime.now(timezone("Asia/Kolkata")).strftime('%Y-%m-%d %H:%M:%S.%f')
while int(ind_time[11:13])*60+int(ind_time[14:16])<561 or int(ind_time[11:13])*60+int(ind_time[14:16])>885 :
    ind_time = datetime.now(timezone("Asia/Kolkata")).strftime('%Y-%m-%d %H:%M:%S.%f')
#%%
start=0
#day_of_week=200#100*(int(input("enter the day from expiry(Eg:enter 1 if it's Wednesday): "))+1)
clear_open_positions()
while int(ind_time[11:13])*60+int(ind_time[14:16])<1135:
    ind_time = datetime.now(timezone("Asia/Kolkata")).strftime('%Y-%m-%d %H:%M:%S.%f')
    option_chain,x=data(week=0)
    B=options_indicator(option_chain,x,cv,pv,earlier_cv,earlier_pv)
    #exclusive_strike,tron,start,earlier_indicator=buy_kickoff(start,B,earlier_indicator,exclusive_strike,day_of_week,tron)
    exclusive_strike,tron,start,earlier_indicator=sell_kickoff(x,start,B,earlier_indicator,exclusive_strike,d,tron)
    print(B)
#clear_open_positions()
# %%
