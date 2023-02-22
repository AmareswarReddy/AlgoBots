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
from scipy import interpolate
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
    sleep(0.5)
    if "S" in type:
        type=type[:-1]+"B"
    elif "B" in type:
        type=type[:-1]+"S"
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


def indicator_(x,rosetta,rosetta_ratio,oi_ratio,hightime,time,volume_ind):
    def node_out(input_,weights_bias):
        return np.tanh(weights_bias[0]*input_[0]+weights_bias[1]*input_[1]+weights_bias[2]*input_[2]+weights_bias[3]*input_[3]+weights_bias[4]*input_[4]+weights_bias[5]*input_[5]+weights_bias[6])
    input_=[hightime,oi_ratio,rosetta_ratio,rosetta,time/22440,volume_ind]
    x_=np.reshape(x,(37,len(input_)+1))
    index=0
    for j in range(0,6):
        A=[]
        for i in range(0,6):
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
    xopt=[  5.47991331,  13.16663219,  15.28246107,  -6.4056601 ,
         15.63428305,  -6.88221896, -11.08925845,   5.15123558,
        -17.1464609 ,  -4.12327024,  -1.62925441,   2.25979971,
          1.1747748 ,   3.88119192,  -0.44427041,   2.71893084,
        -19.97864608, -13.09387723, -17.8131945 ,  19.9997865 ,
          8.71685254,  -3.87719701,  14.94596754,  10.72170082,
         13.27855014, -13.90377575, -18.12273638, -15.14243837,
          6.11918275,  -1.52058568,  19.59550341,  -8.67650244,
         12.8776444 ,   1.22127802,  -8.4613598 , -14.44155808,
         18.62613773,   8.27166653, -15.24635678,   3.52734346,
        -11.21913738,  12.90402567,  18.28266998,  16.2550572 ,
          2.36693277,   7.19959663,  -7.57915412,  19.97299641,
          9.19728777,   2.98273747,   8.46066271, -10.72811543,
        -12.68481783,   9.37158423,   2.16248843,  16.70073103,
        -16.2462397 ,   8.14580946,  -9.32485984,  -1.08843727,
         -6.23852731,  -0.69285787, -15.28739539,  10.25514487,
         -6.05133665,  17.98159358,   0.67482484, -14.897653  ,
        -11.74903422, -19.63513631,   1.31026664,  -2.3784058 ,
         -1.11565067,   5.90896035, -14.11060749, -13.70227801,
         19.17661829,   5.67404069, -19.87553055,  -4.98224059,
          4.03737689,  -9.70068624,  -1.92323941,   5.03904961,
        -16.25736985,   6.03035598,  10.4058891 ,   7.55805948,
         16.5498668 ,  -8.44846763,   3.98570392,   1.1103903 ,
        -19.94287299,  -8.78985171,  -9.83696984, -10.43274403,
         -3.82000907, -12.67816189,  15.00742845, -19.85483796,
          5.65304695,   1.93093498,  -2.20411953, -18.82914316,
         -2.38786921,  -7.9938734 ,  19.99927445, -17.3117827 ,
         -4.21781857,  19.99838327, -15.96713382,  19.81299998,
          0.37496587,  -2.41370777,  13.91107213, -14.88977995,
        -19.84277918,  19.86347182,   6.92184611,  18.38452782,
          9.72268029,  17.46482228, -13.06005071,  -5.57775541,
        -16.96509337, -12.08854536, -10.44855177,  16.51759918,
         -2.02460032,  -7.70244837,  13.82193137,  17.03187253,
         -8.94177209,   2.79796808,  16.25520437,  -2.83462678,
         -9.14643651,  -2.77148713,  15.59327797,   2.74848307,
        -13.94286455,  -1.4078556 ,   5.02237414,   2.55827262,
          0.13700511,  -6.42498243,  -4.78343867,   1.57700671,
          2.3844911 ,  15.75567534,  13.51936854,   5.74006843,
        -13.93996626,   1.12508746,   4.47497203,   7.65363699,
          5.48619215, -19.94702319,  -0.21390307, -11.74188084,
        -15.84495906,   1.59502813, -19.9965671 , -19.95770654,
        -18.09505071,  19.98511442,  14.59521092, -14.4763512 ,
          3.78188858,  16.30124328,  -9.43301663, -19.75254556,
         -4.10550198, -10.94868247,   1.31050625, -11.84264771,
        -19.55980104, -19.99601533,  -7.24827335,  -0.91204746,
          4.8266535 ,  -4.80569872, -17.24810051,   2.4982498 ,
         -7.74016044,  -6.04556707, -17.62907074, -19.8359111 ,
         19.94319803,   4.51224156, -19.45080182,  -0.21656335,
          8.34834134,   0.7111164 , -17.46840116, -12.06985516,
         -12.16805757,  16.31853456,  -6.71618516,   2.62843858,
         19.97582435,  15.16674528,  -7.74187739,  20.        ,
         -3.87582733,   6.53509025,   5.34504396,  18.52148885,
        -13.29232373,   6.57427113,  13.37874856,  -7.6963758 ,
         -1.93006811,  -8.93365422, -14.81395036,  13.81030056,
         -8.86558071, -18.41050577,  -0.6533642 ,  16.50341412,
         11.38410505,  13.87974437,  13.42817535,  -3.99858691,
         10.93457061,   6.39174352,   5.55141687,  15.8019391 ,
        -14.09260587, -12.00706576,  -3.45110367, -11.58107716,
         19.81587397,   7.96028983,   3.71306472,  -9.97087482,
         12.75115381,   0.02131132, -13.78833337, -17.88348398,
         -1.0426155 ,   6.67429719, -18.37172244,   0.0937282 ,
        -18.016327  ,  16.70704723,   3.46730822,  -1.55327872,
          3.31417551,  -9.09440781,   9.30208845, -19.43693891,
        -16.34520702,   6.05873022,  -2.08781919,   5.36209894,
        -13.98614788,   3.15184275,   7.34325003]
    time=int(ind_time[11:13])*60*60+int(ind_time[14:16])*60-33300
    final=indicator_(xopt,rosetta_indicator,rosetta_ratio_indicator,oi_ratio_indicator,hightime_indicator,time,v_ind)
    return  final,cv,pv,earlier_cv,earlier_pv


def options_vwap_json(option_chain,calloptions_vwap,putoptions_vwap,primary_oi,x,prev_final_c_shape,prev_final_p_shape):
    stoploss=17
    ce_data=option_chain[option_chain['CPType']=='CE']
    pe_data=option_chain[option_chain['CPType']=='PE']
    ce_data_prime=primary_oi[primary_oi['CPType']=='CE']
    pe_data_prime=primary_oi[primary_oi['CPType']=='PE']
    taken_c=np.multiply((np.array(ce_data['StrikeRate'])>x-50), (np.array(ce_data['StrikeRate'])<x+600))
    taken_p=np.multiply((np.array(pe_data['StrikeRate'])>x-600), (np.array(pe_data['StrikeRate'])<x+50))
    c_lastrate=np.array(ce_data['LastRate'])
    p_lastrate= np.array(pe_data['LastRate'])
    c_volumes=  np.array(ce_data['Volume'])
    p_volumes=  np.array(pe_data['Volume'])
    c_oi=  np.array(ce_data['OpenInterest'])
    p_oi=  np.array(pe_data['OpenInterest'])
    prev_c_lastrate=    np.array(calloptions_vwap['LastRate'])
    prev_p_lastrate=    np.array(putoptions_vwap['LastRate'])
    prev_c_volumes=     np.array(calloptions_vwap['Volume'])
    prev_p_volumes=     np.array(putoptions_vwap['Volume'])
    primary_c_oi=  np.array(ce_data_prime['OpenInterest'])
    primary_p_oi=  np.array(pe_data_prime['OpenInterest'])
    c_shape=np.multiply((c_oi-primary_c_oi)>0,taken_c)
    p_shape=np.multiply((p_oi-primary_p_oi)>0,taken_p)
    c_net=np.multiply(c_volumes-prev_c_volumes,c_lastrate)
    p_net=np.multiply(p_volumes-prev_p_volumes,p_lastrate)
    c_volumes[c_volumes==0]=1
    p_volumes[p_volumes==0]=1
    call_vwap=np.multiply((c_net+np.multiply(prev_c_lastrate,prev_c_volumes)),1/c_volumes)
    put_vwap=np.multiply((p_net+np.multiply(prev_p_lastrate,prev_p_volumes)),1/p_volumes)
    calloptions_vwap=ce_data[['StrikeRate','LastRate','Volume']].copy()
    putoptions_vwap=pe_data[['StrikeRate','LastRate','Volume']].copy()
    calloptions_vwap['LastRate']=call_vwap    
    calloptions_vwap['Volume']=ce_data['Volume']
    putoptions_vwap['LastRate']=put_vwap    
    putoptions_vwap['Volume']=pe_data['Volume']
    final_c_shape=np.multiply(np.sign(((c_lastrate-call_vwap)<-stoploss)*-1),c_shape)
    final_p_shape=np.multiply(np.sign(((p_lastrate-put_vwap)<-stoploss)*-1),p_shape)
    to_correct_c_shape=np.multiply(np.sign(((c_lastrate-call_vwap)<0)*-1),c_shape)
    to_correct_p_shape=np.multiply(np.sign(((p_lastrate-put_vwap)<0)*-1),p_shape)
    if len(prev_final_p_shape)==0:
        prev_final_c_shape=final_c_shape
        prev_final_p_shape=final_p_shape
    final_c_shape=final_c_shape-np.multiply(to_correct_c_shape-final_c_shape,prev_final_c_shape)
    final_p_shape=final_p_shape-np.multiply(to_correct_p_shape-final_p_shape,prev_final_p_shape)
    call_seller=ce_data[['StrikeRate']].copy()
    call_seller['indicator']=final_c_shape
    put_seller=pe_data[['StrikeRate']].copy()
    put_seller['indicator']=final_p_shape
    return calloptions_vwap,putoptions_vwap,put_seller,call_seller,final_c_shape,final_p_shape

def get_strike_from_scrip(scripcode,exchange):
    if exchange=='BANKNIFTY':
        option_chain,a1=data(0)
    k1=option_chain[option_chain['ScripCode']==scripcode]
    return int(k1['StrikeRate'])


def buy_kickoff(start,indicator,earlier_indicator,exclusive_strike,tron):
    if abs(indicator-earlier_indicator)==2:
        indicator=0
    if start==0:
        s=indicator
        if s>0:
            exclusive_strike,yet_to_place=order_button(exclusive_strike,'CE_S',tron)
            tron-=lots_drop(exclusive_strike,'CE_S',yet_to_place)
            start=1
        elif s<0:
            exclusive_strike,yet_to_place=order_button(exclusive_strike,'PE_S',tron)
            tron-=lots_drop(exclusive_strike,'PE_S',yet_to_place)
            start=1
    elif start==1:
        if earlier_indicator==0 and indicator==1:
            exclusive_strike,yet_to_place=order_button(exclusive_strike,'CE_S',tron)
            tron-=lots_drop(exclusive_strike,'CE_S',yet_to_place)

        if earlier_indicator==0 and indicator==-1:
            exclusive_strike,yet_to_place=order_button(exclusive_strike,'PE_S',tron)
            tron-=lots_drop(exclusive_strike,'PE_S',yet_to_place)
        if earlier_indicator==-1 and indicator==0:
            exclusive_strike,yet_to_place=order_button(exclusive_strike,'PE_B',tron)
        if earlier_indicator==1 and indicator==0:
            exclusive_strike,yet_to_place=order_button(exclusive_strike,'CE_B',tron)

    return exclusive_strike,tron,start,indicator

def initial_straddle_trades(x,tron):
    exclusive_strike=int(np.round((x)/100)*100)
    order_button(exclusive_strike,'CE_S',tron*7)
    order_button(exclusive_strike,'PE_S',tron*7)

def clear_open_positions():

    S=pd.DataFrame(prime_client['login'].positions())
    if len(S)==0:
        return 0
    if len(S[S['NetQty']!=0])!=0:
        for i in range(0,len(S)):
            if ('BANKNIFTY' in S['ScripName'].iloc[i]) and S['NetQty'].iloc[i]!=0:
                if S['NetQty'].iloc[i]<0 and ('PE' in S['ScripName'].iloc[i]):
                    order_button(get_strike_from_scrip(S['ScripCode'].iloc[i],'BANKNIFTY'),'PE_S',int(abs(S['NetQty'].iloc[i])/25))
                elif S['NetQty'].iloc[i]<0 and ('CE' in S['ScripName'].iloc[i]):
                    order_button(get_strike_from_scrip(S['ScripCode'].iloc[i],'BANKNIFTY'),'CE_S',int(abs(S['NetQty'].iloc[i])/25))
                elif S['NetQty'].iloc[i]>0 and ('CE' in S['ScripName'].iloc[i]):
                    order_button(get_strike_from_scrip(S['ScripCode'].iloc[i],'BANKNIFTY'),'CE_B',int(abs(S['NetQty'].iloc[i])/25))
                elif S['NetQty'].iloc[i]>0 and ('PE' in S['ScripName'].iloc[i]):
                    order_button(get_strike_from_scrip(S['ScripCode'].iloc[i],'BANKNIFTY'),'PE_B',int(abs(S['NetQty'].iloc[i])/25))
        S=pd.DataFrame(prime_client['login'].positions())
        if len(S[S['NetQty']!=0])!=0:
            return clear_open_positions()
        elif len(S[S['NetQty']!=0])==0:
            return 0
    elif len(S[S['NetQty']!=0])==0:
        return 0


#%%
client_name = input('enter the client name: ')
tron=int(input('enter the number of lots at each strike'))
betatron=tron
prime_client=client_login(client=client_name)
option_chain,x=data(week=0)
primary_oi=option_chain
ce_data=option_chain[option_chain['CPType']=='CE']
pe_data=option_chain[option_chain['CPType']=='PE']
calloptions_vwap=ce_data[['StrikeRate','LastRate','Volume']].copy()
putoptions_vwap=pe_data[['StrikeRate','LastRate','Volume']].copy()

#start=int(input('enter 0 if starting the strategy for the first time, else 1 :  '))
#%%
ind_time = datetime.now(timezone("Asia/Kolkata")).strftime('%Y-%m-%d %H:%M:%S.%f')
while int(ind_time[11:13])*60+int(ind_time[14:16])<656:
    ind_time = datetime.now(timezone("Asia/Kolkata")).strftime('%Y-%m-%d %H:%M:%S.%f')
option_chain,x=data(week=0)
calloptions_vwap,putoptions_vwap,put_seller,call_seller,prev_final_c_shape,prev_final_p_shape=options_vwap_json(option_chain,calloptions_vwap,putoptions_vwap,primary_oi,x,[],[])
e_put_seller=put_seller['indicator']*0
e_call_seller=call_seller['indicator']*0
x_prime=x
ce_data=option_chain[option_chain['CPType']=='CE']
pe_data=option_chain[option_chain['CPType']=='PE']
earlier_pv=np.array(list(pe_data['Volume']))
earlier_cv=np.array(list(ce_data['Volume']))
cv,pv=0,0
earlier_indicator=options_indicator(option_chain,x,cv,pv,earlier_cv,earlier_pv)
start=0
exclusive_strike=0
clear_open_positions()
initial_straddle_trades(x,tron)
while int(ind_time[11:13])*60+int(ind_time[14:16])<921:
    ind_time = datetime.now(timezone("Asia/Kolkata")).strftime('%Y-%m-%d %H:%M:%S.%f')
    option_chain,x=data(week=0)
    B,cv,pv,earlier_cv,earlier_pv=options_indicator(option_chain,x,cv,pv,earlier_cv,earlier_pv)
    exclusive_strike,betatron,start,earlier_indicator=buy_kickoff(start,B,earlier_indicator,exclusive_strike,betatron)
    calloptions_vwap,putoptions_vwap,put_seller,call_seller,prev_final_c_shape,prev_final_p_shape=options_vwap_json(option_chain,calloptions_vwap,putoptions_vwap,primary_oi,x_prime,prev_final_c_shape,prev_final_p_shape)
    final_put_seller=np.array(put_seller['indicator']-e_put_seller)
    final_call_seller=np.array(call_seller['indicator']-e_call_seller)
    shine_c_strike=np.array(call_seller['StrikeRate'])
    shine_p_strike=np.array(put_seller['StrikeRate'])
    for i in range(len(final_call_seller)):
        if final_call_seller[i]<0:
            a,b=order_button(shine_c_strike[i],'CE_S',tron)
            c=0
            while b!=0:
                c+=1
                sleep(5)
                a,b=order_button(shine_c_strike[i],'CE_S',tron)
                if c>5:
                    if b!=0:
                        final_call_seller[i]=0
                    break
        elif final_call_seller[i]>0:
            order_button(shine_c_strike[i],'CE_B',tron)
    for i in range(len(final_put_seller)):
        if final_put_seller[i]<0:
            a,b=order_button(shine_p_strike[i],'PE_S',tron)
            c=0
            while b!=0:
                c+=1
                sleep(5)
                a,b=order_button(shine_p_strike[i],'PE_S',tron)
                if c>5:
                    if b!=0:
                        final_put_seller[i]=0
                    break
        elif final_put_seller[i]>0:
            order_button(shine_p_strike[i],'PE_B',tron)
    e_put_seller=put_seller['indicator']
    e_call_seller=call_seller['indicator']
    if abs(x_prime-x)>99:
        x_prime=x

clear_open_positions()
# %%
