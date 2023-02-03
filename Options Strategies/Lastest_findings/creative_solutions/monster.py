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
# globalx=[-0.17029294,  2.24607897,  4.02404807,  4.96762373,  1.32848933,2.04125874,  3.44274129,  0.43390382, -4.45726496, -0.25688519,2.25589913,  0.52429517,  1.45407642,  4.8564242 ,  2.97517898,1.28676788,  4.1999809 ,  4.66388321, -4.19800915,  0.60788653,2.16063401, -0.51621476]
#local=[-9.90583632e-01,  1.42267393e+00, -2.82415313e+00, -1.27224410e+00,4.99726990e+00,  1.51728279e+00,  1.46607700e+00,  2.88698326e+00,4.79469914e+00, -3.72371740e+00,  3.67489330e+00, -4.20116354e+00,-9.29778613e-01, -9.66096762e-01,  2.23164066e+00,  1.44144079e+00,4.38337232e-01,  4.90414991e+00, -3.66912192e+00,  1.91147868e+00,3.33686629e-01, -1.82144148e-04]
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

def indicator(x,hightime,oi_ratio,rosetta_ratio,rosetta,time):
    w11,w12,w13,w14,w15,c11,c12,c13,c14,c15,outw11,outw12,outw13,outw14,outw15,outc11,outw21,outw22,outw23,outw24,outw25,outc21=x[0],x[1],x[2],x[3],x[4],x[5],x[6],x[7],x[8],x[9],x[10],x[11],x[12],x[13],x[14],x[15],x[16],x[17],x[18],x[19],x[20],x[21]
    A1=np.tanh(w11*hightime+c11)
    A2=np.tanh(w12*oi_ratio+c12)
    A3=np.tanh(w13*rosetta_ratio+c13)
    A4=np.tanh(w14*rosetta+c14)
    A5=np.tanh(w15*time/22440+c15)
    layer11=outw11*A1+outw12*A2+outw13*A3+outw14*A4+outw15*A5
    layer12=outw21*A1+outw22*A2+outw23*A3+outw24*A4+outw25*A5
    output1=np.tanh(layer11+outc11)
    output2=(np.tanh(layer12+outc21)+1)/2
    final_indicator=np.multiply((np.array(output2)>0.5),(np.array(output1>0)+np.array(output1<0)*-1))
    return final_indicator

def options_indicator(option_chain,x):
    ind_time = datetime.now(timezone("Asia/Kolkata")).strftime('%Y-%m-%d %H:%M:%S.%f')
    ce_data=option_chain[option_chain['CPType']=='CE']
    pe_data=option_chain[option_chain['CPType']=='PE']
    p_strikerates=np.array(list(pe_data['StrikeRate']))
    c_strikerates=np.array(list(ce_data['StrikeRate']))
    p_lastrate=np.array(list(pe_data['LastRate']))
    c_lastrate=np.array(list(ce_data['LastRate']))
    p_openinterest=np.array(list(pe_data['OpenInterest']))
    c_openinterest=np.array(list(ce_data['OpenInterest']))
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
    #xopt=[-3.52154161,  3.62338935,  4.89043935, -1.01552487,  4.94413512,-0.43404158, -4.40578643, -0.0183265 ,  3.83645581, -4.95346292, 2.48773254,  0.81135561, -3.45979877, -3.62235891, -1.7944221 ,-2.46141404, -3.61953669, -4.31216943, -1.21343265,  0.49192755,-4.34743932, -2.29521168]
    #xopt=[ 1.593797  , -1.6964851 , -1.30712909, -1.77346566, -1.32151318,1.33003003, -0.19281429,  0.09006752,  3.40276633,  1.27680066,-0.62896567,  1.52599676,  1.99139416, -3.21629391,  1.57262102,2.56654468,  0.53669149, -1.6079863 , -0.99419409,  2.3638444 ,2.7427471 ,  3.23056616]
    xopt=[-4.99943279,  4.6916429 ,  4.2639786 , -0.30161161, -2.00795885, -3.22138697,  1.42935836, -0.21944782,  1.70992947,  0.96601996,1.33457848, -2.34361743, -2.34929068, -1.16943402,  1.81891989,2.26812312, -2.37571711,  2.18754469, -1.53913964,  3.16551106,-0.79012491,  2.47577859]#latest
    time=33300-int(ind_time[11:13])*60*60+int(ind_time[14:16])*60
    final=indicator(xopt,rosetta_indicator,rosetta_ratio_indicator,oi_ratio_indicator,hightime_indicator,time)
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

def buy_kickoff(start,indicator,earlier_indicator,exclusive_strike,type,tron,typical_tron):
    if abs(indicator-earlier_indicator)==2:
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
        if earlier_indicator==0 and indicator==1:
            exclusive_strike,yet_to_place=order_button(exclusive_strike,'CE_B',typical_tron)
            tron-=lots_drop(exclusive_strike,'CE_B',yet_to_place)
        if earlier_indicator==0 and indicator==-1:
            exclusive_strike,yet_to_place=order_button(exclusive_strike,'PE_B',typical_tron)
            tron-=lots_drop(exclusive_strike,'PE_B',yet_to_place)
        if earlier_indicator==-1 and indicator==0:
            exclusive_strike,yet_to_place=order_button(exclusive_strike,'PE_S',typical_tron)
        if earlier_indicator==1 and indicator==0:
            exclusive_strike,yet_to_place=order_button(exclusive_strike,'CE_S',typical_tron)
    return exclusive_strike,tron,start,indicator


#%%
#client_name=input('enter the client name Eg: vinathi,bhaskar ')
client_name   = 'midya'
tron=int(input('enter the number of lots for buying (Eg:3):'))
typical_tron=1
prime_client=client_login(client=client_name)
exclusive_strike,type=0,''
option_chain,x=data(week=0)
earlier_indicator=options_indicator(option_chain,x)
start=0
#%%
ind_time = datetime.now(timezone("Asia/Kolkata")).strftime('%Y-%m-%d %H:%M:%S.%f')
while int(ind_time[11:13])*60+int(ind_time[14:16])<561 or int(ind_time[11:13])*60+int(ind_time[14:16])>885 :
    ind_time = datetime.now(timezone("Asia/Kolkata")).strftime('%Y-%m-%d %H:%M:%S.%f')
#%%
start=0
while True:
    option_chain,x=data(week=0)
    B=options_indicator(option_chain,x)
    #exclusive_strike,tron,start,earlier_indicator=buy_kickoff(start,B,earlier_indicator,exclusive_strike,type,tron,typical_tron)
    print(B)

# %%
