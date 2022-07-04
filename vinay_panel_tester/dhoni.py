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

def client_login(client,lots):
    import json
    f = open ('credentials.json', "r")
    creds = json.loads(f.read())
    client_list={}
    client_list[client]={'strategy':{},'login':{},'lots':{}}
    client_list[client]['lots']=lots
    vinathi_cred = creds[client]["keys"]
    user = creds[client]["user"]
    passw = creds[client]["passw"]
    dob = creds[client]["dob"]
    client_list[client]['strategy']=strategies(user=user, passw=passw, dob=dob,cred=vinathi_cred)
    client_list[client]['login']=FivePaisaClient(email=user, passwd=passw, dob=dob,cred=vinathi_cred)
    client_list[client]['login'].login()
    return client_list[client]


def proj_BN(bank_rates,bank_weights):
    bank_list=list(bank_rates.keys())
    p=0
    for bank in bank_list:
        p=p+bank_rates[bank]*bank_weights[bank]
    return p

def indicator2(banknifty_lastrate,bank_lastrates,bank_weights,projections):
    ratio = banknifty_lastrate/proj_BN(bank_rates=bank_lastrates,bank_weights=bank_weights)
    return banknifty_lastrate-ratio*proj_BN(bank_rates=projections,bank_weights=bank_weights)
import sys
client_name   = sys.argv[1]
lots=int(sys.argv[2])
#lots=int(input('lots (Eg:3):'))


#%%
ind_time = datetime.now(timezone("Asia/Kolkata")).strftime('%Y-%m-%d %H:%M:%S.%f')
while int(ind_time[11:13])*60+int(ind_time[14:16])<561 or int(ind_time[11:13])*60+int(ind_time[14:16])>885 :
    ind_time = datetime.now(timezone("Asia/Kolkata")).strftime('%Y-%m-%d %H:%M:%S.%f')
#%%
prime_client=client_login(client=client_name,lots=lots)
expiry_timestamps=prime_client['login'].get_expiry("N","BANKNIFTY").copy()
current_expiry_time_stamp_weekly=int(expiry_timestamps['Expiry'][0]['ExpiryDate'][6:19])
option_chain=pd.DataFrame(prime_client['login'].get_option_chain("N","BANKNIFTY",current_expiry_time_stamp_weekly)['Options'])
bank_weights={'HDFCBANK':27.58,'ICICIBANK':23.72,'AXISBANK':10.69,'KOTAKBANK':12.3,'SBIN':10.81,'INDUSINDBK':5.4,'AUBANK':2.46,'BANDHANBNK':1.97,'BANKBARODA':1.66,'FEDERALBNK':1.58,'IDFCFIRSTB':1.01,'PNB':0.83}
bank_lots={'HDFCBANK':550,'ICICIBANK':1375,'AXISBANK':1200,'KOTAKBANK':400,'SBIN':1500,'INDUSINDBK':900,'AUBANK':500,'BANDHANBNK':1800,'BANKBARODA':5850,'FEDERALBNK':10000,'IDFCFIRSTB':11100,'PNB':16000}
bank_strike_diff={'HDFCBANK':20,'ICICIBANK':10,'AXISBANK':10,'KOTAKBANK':20,'SBIN':5,'INDUSINDBK':10,'AUBANK':20,'BANDHANBNK':5,'BANKBARODA':2.5,'FEDERALBNK':1,'IDFCFIRSTB':1,'PNB':1}
order_books={'HDFCBANK':{},'ICICIBANK':{},'AXISBANK':{},'KOTAKBANK':{},'SBIN':{},'INDUSINDBK':{},'AUBANK':{},'BANDHANBNK':{},'BANKBARODA':{},'FEDERALBNK':{},'IDFCFIRSTB':{},'PNB':{}}
bank_scripcodes={'HDFCBANK':'1333','ICICIBANK':'4963','AXISBANK':'5900','KOTAKBANK':'1922','SBIN':'3045','INDUSINDBK':'5258','AUBANK':'21238','BANDHANBNK':'2263','BANKBARODA':'4668','FEDERALBNK':'1023','IDFCFIRSTB':'11184','PNB':'10666'}
bank_controls={'HDFCBANK':0,'ICICIBANK':0,'AXISBANK':0,'KOTAKBANK':0,'SBIN':0,'INDUSINDBK':0,'AUBANK':0,'BANDHANBNK':0,'BANKBARODA':0,'FEDERALBNK':0,'IDFCFIRSTB':0,'PNB':0}
profit_statements={'HDFCBANK':0,'ICICIBANK':0,'AXISBANK':0,'KOTAKBANK':0,'SBIN':0,'INDUSINDBK':0,'AUBANK':0,'BANDHANBNK':0,'BANKBARODA':0,'FEDERALBNK':0,'IDFCFIRSTB':0,'PNB':0}
bank_p_trades={'HDFCBANK':0,'ICICIBANK':0,'AXISBANK':0,'KOTAKBANK':0,'SBIN':0,'INDUSINDBK':0,'AUBANK':0,'BANDHANBNK':0,'BANKBARODA':0,'FEDERALBNK':0,'IDFCFIRSTB':0,'PNB':0}
bank_c_trades={'HDFCBANK':0,'ICICIBANK':0,'AXISBANK':0,'KOTAKBANK':0,'SBIN':0,'INDUSINDBK':0,'AUBANK':0,'BANDHANBNK':0,'BANKBARODA':0,'FEDERALBNK':0,'IDFCFIRSTB':0,'PNB':0}
bank_scrips={'HDFCBANK':0,'ICICIBANK':0,'AXISBANK':0,'KOTAKBANK':0,'SBIN':0,'INDUSINDBK':0,'AUBANK':0,'BANDHANBNK':0,'BANKBARODA':0,'FEDERALBNK':0,'IDFCFIRSTB':0,'PNB':0}
bank_p_scrips={'HDFCBANK':0,'ICICIBANK':0,'AXISBANK':0,'KOTAKBANK':0,'SBIN':0,'INDUSINDBK':0,'AUBANK':0,'BANDHANBNK':0,'BANKBARODA':0,'FEDERALBNK':0,'IDFCFIRSTB':0,'PNB':0}
bank_c_scrips={'HDFCBANK':0,'ICICIBANK':0,'AXISBANK':0,'KOTAKBANK':0,'SBIN':0,'INDUSINDBK':0,'AUBANK':0,'BANDHANBNK':0,'BANKBARODA':0,'FEDERALBNK':0,'IDFCFIRSTB':0,'PNB':0}
bank_proj1={'HDFCBANK':50000,'ICICIBANK':50000,'AXISBANK':50000,'KOTAKBANK':50000,'SBIN':50000,'INDUSINDBK':50000,'AUBANK':50000,'BANDHANBNK':50000,'BANKBARODA':50000,'FEDERALBNK':50000,'IDFCFIRSTB':50000,'PNB':50000}
bank_proj2={'HDFCBANK':0,'ICICIBANK':0,'AXISBANK':0,'KOTAKBANK':0,'SBIN':0,'INDUSINDBK':0,'AUBANK':0,'BANDHANBNK':0,'BANKBARODA':0,'FEDERALBNK':0,'IDFCFIRSTB':0,'PNB':0}
bank_list=list(bank_weights.keys())
option_chains={}
for bank in bank_list:
    expiry_timestamps=prime_client['login'].get_expiry("N",bank).copy()
    current_expiry_time_stamp=int(expiry_timestamps['Expiry'][0]['ExpiryDate'][6:19])
    option_chains[bank]=pd.DataFrame(prime_client['login'].get_option_chain("N",bank,current_expiry_time_stamp)['Options'])

def pe_oi(strikeprice):
    c_strike=option_chain[option_chain['StrikeRate']==strikeprice]
    to_return=int(c_strike[c_strike['CPType']=='PE']['OpenInterest'])
    return to_return
def ce_oi(strikeprice):
    c_strike=option_chain[option_chain['StrikeRate']==strikeprice]
    to_return=int(c_strike[c_strike['CPType']=='CE']['OpenInterest'])
    return to_return
def pe_oi_change(strikeprice):
    c_strike=option_chain[option_chain['StrikeRate']==strikeprice]
    to_return=int(c_strike[c_strike['CPType']=='PE']['ChangeInOI'])
    return to_return
def ce_oi_change(strikeprice):
    c_strike=option_chain[option_chain['StrikeRate']==strikeprice]
    to_return=int(c_strike[c_strike['CPType']=='CE']['ChangeInOI'])
    return to_return

def pro(option_chain):
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
    index=np.argmin(np.abs(data))
    return   np.array(option_chain['StrikeRate'])[0]+index*increment

def simple_trend():
    req_list_=[{"Exch":"N","ExchType":"C","Symbol":"BANKNIFTY","Scripcode":"999920005","OptionType":"EQ"}]          
    a=prime_client['login'].fetch_market_feed(req_list_)
    x=a['Data'][0]['LastRate']
    bot=np.floor(x/100)*100
    top=np.ceil(x/100)*100
    bot_at=np.floor(x/500)*500
    top_at=np.ceil(x/500)*500

    if top_at-x>250:
        bot_500=bot_at-500
        top_500=bot_at+500
        top_1000=bot_at+1000
        bot_1000=bot_at-1000
    else:
        bot_500=top_at-500
        top_500=top_at+500
        top_1000=top_at+1000
        bot_1000=top_at-1000
    ce_net=ce_oi(bot)+ce_oi(top)+ce_oi(top_500)+ce_oi(top_1000)
    pe_net=pe_oi(bot)+pe_oi(top)+pe_oi(bot_500)+pe_oi(bot_1000)
    if ce_net>pe_net:
        return 'downtrend'
    else:
        return 'uptrend'

def complex_trend():
    req_list_=[{"Exch":"N","ExchType":"C","Symbol":"BANKNIFTY","Scripcode":"999920005","OptionType":"EQ"}]          
    a=prime_client['login'].fetch_market_feed(req_list_)
    x=a['Data'][0]['LastRate']
    x_change=a['Data'][0]['Chg']
    bot=np.floor(x/100)*100
    top=np.ceil(x/100)*100
    bot_at=np.floor(x/500)*500
    top_at=np.ceil(x/500)*500
    if top_at-x>250:
        bot_500=bot_at-500
        top_500=bot_at+500
        top_1000=bot_at+1000
        bot_1000=bot_at-1000
    else:
        bot_500=top_at-500
        top_500=top_at+500
        top_1000=top_at+1000
        bot_1000=top_at-1000
    ce_net_change=ce_oi_change(bot)+ce_oi_change(top)+ce_oi_change(top_500)+ce_oi_change(top_1000)
    pe_net_change=pe_oi_change(bot)+pe_oi_change(top)+pe_oi_change(bot_500)+pe_oi_change(bot_1000)
    if x_change>0 :
        if pe_net_change>0 and ce_net_change<0:
            return "uptrend at it's peak"
        if pe_net_change<0 and ce_net_change>0:
            return "strong downtrend about to start in a while"
        if pe_net_change<0 and ce_net_change<0:
            return "A strong move on either side is a possibility"
        if pe_net_change>0 and ce_net_change>0 and pe_net_change>ce_net_change:
            return "slightly uptrend"
        if pe_net_change>0 and ce_net_change>0 and pe_net_change<ce_net_change:
            return "slightly downtrend"
    if x_change<=0 :
        if pe_net_change>0 and ce_net_change<0:
            return "strong uptrend about to start in a while"
        if pe_net_change<0 and ce_net_change>0:
            return "downtrend at it's peak"
        if pe_net_change<0 and ce_net_change<0:
            return "A strong move on either side is a possibility"
        if pe_net_change>0 and ce_net_change>0 and pe_net_change>ce_net_change:
            return "slightly uptrend"    
        if pe_net_change>0 and ce_net_change>0 and pe_net_change<ce_net_change:
            return "slightly downtrend"

def projected(option_chain):
    kkk=option_chain[option_chain['CPType']=='PE']
    i=np.array(kkk['StrikeRate'])[0]
    end=np.array(kkk['StrikeRate'])[-1]
    ss=np.array(kkk['StrikeRate'])
    pe_data=option_chain[option_chain['CPType']=='PE']
    ce_data=option_chain[option_chain['CPType']=='CE']
    p_lastrate=np.array(pe_data['LastRate'])
    c_lastrate=np.array(ce_data['LastRate'])
    p_openinterest=np.array(pe_data['OpenInterest'])
    c_openinterest=np.array(ce_data['OpenInterest'])
    data=[]
    while i<end:
        i=i+1
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
    index=np.argmin(np.abs(data))
    return   np.array(option_chain['StrikeRate'])[0]+index
        #print(init_ce-end_ce-init_pe+end_pe)
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

trend_indicator={
            'timestamp':[],
            'simple':[],
            'complex':[],
            'projected':[],
            'spotprice':[]
            }
control=0
tim=0
orders_track={}

def bank_LTPs(bank_list,bank_scripcodes):
    req_list_=[]
    for bank in bank_list:
        req_list_=req_list_+[{"Exch":"N","ExchType":"C","Symbol":bank,"Scripcode":bank_scripcodes[bank],"OptionType":"EQ"}]      
    a=prime_client['login'].fetch_market_feed(req_list_)
    life=pd.DataFrame(a['Data'])
    bank_lastrates={}
    for bank in bank_list :
        bank_lastrates[bank]=float(life[life['Symbol']==bank]['LastRate'])
    return bank_lastrates

def bank_proj(option_chains,bank_list):
    proj_list={}
    for bank in bank_list:
        proj_list[bank]=pro(option_chains[bank])
    return proj_list
    
def get_option_chains(prime_client,bank_list):
    while True:
        try :
            option_chains={}
            for bank in bank_list:
                expiry_timestamps=prime_client['login'].get_expiry("N",bank).copy()
                current_expiry_time_stamp=int(expiry_timestamps['Expiry'][0]['ExpiryDate'][6:19])
                option_chains[bank]=pd.DataFrame(prime_client['login'].get_option_chain("N",bank,current_expiry_time_stamp)['Options'])
            break
        except Exception :
            pass
    return option_chains
breaker=0
while True:
    option_chains=get_option_chains(prime_client,bank_list)
    bank_lastrates=bank_LTPs(bank_list,bank_scripcodes)
    projections=bank_proj(option_chains,bank_list)
    re=[{"Exch":"N","ExchType":"C","Symbol":"BANKNIFTY","Scripcode":"999920005","OptionType":"EQ"}]          
    aa=prime_client['login'].fetch_market_feed(re)
    banknifty_lastrate=aa['Data'][0]['LastRate']
    ind2=indicator2(banknifty_lastrate,bank_lastrates,bank_weights,projections)
    while True:
        try :
            expiry_timestamps=prime_client['login'].get_expiry("N","BANKNIFTY").copy()
            current_expiry_time_stamp_weekly=int(expiry_timestamps['Expiry'][0]['ExpiryDate'][6:19])
            option_chain=pd.DataFrame(prime_client['login'].get_option_chain("N","BANKNIFTY",current_expiry_time_stamp_weekly)['Options'])
            break
        except Exception :
            pass
    project_k=banknifty_lastrate-projected(option_chain=option_chain)
    proj=projected(option_chain)
    simple=simple_trend()
    complex=complex_trend()
    print('banks:         ',ind2)
    print('Niftybank:  ',project_k)
    print('oi:               ',simple)
    print('oi_change:  ',complex)
    x=banknifty_lastrate
    ind_time = datetime.now(timezone("Asia/Kolkata")).strftime('%Y-%m-%d %H:%M:%S.%f')
    trend_indicator['timestamp']=trend_indicator['timestamp']+[ind_time]
    trend_indicator['simple']=trend_indicator['simple']+[simple]
    trend_indicator['complex']=trend_indicator['complex']+[complex]
    trend_indicator['projected']=trend_indicator['projected']+[project_k]
    trend_indicator['spotprice']=trend_indicator['spotprice']+[x]
    c_data=option_chain[option_chain['CPType']=='CE']
    p_data=option_chain[option_chain['CPType']=='PE']
    #strategy
    c1=int(c_data[c_data['StrikeRate']==int(np.floor(x/100)*100)]['LastRate'])
    c2=int(c_data[c_data['StrikeRate']==int(np.ceil(x/100)*100)]['LastRate'])
    p1=int(p_data[p_data['StrikeRate']==int(np.floor(x/100)*100)]['LastRate'])
    p2=int(p_data[p_data['StrikeRate']==int(np.ceil(x/100)*100)]['LastRate'])
    dynamic_crossover=(c1+c2+p1+p2)/10
    if proj-x>dynamic_crossover and control==0 and ind2<0:
        strike = int(np.ceil(proj/100)*100)
        scrip=int(c_data[c_data['StrikeRate']==strike]['ScripCode'])
        c_lastrate=float(c_data[c_data['StrikeRate']==strike]['LastRate'])
        test_order = Order(order_type='S',exchange='N',exchange_segment='D', scrip_code =scrip , quantity=25*prime_client['lots'], price=0 ,is_intraday=False,remote_order_id="tag")
        at_strike=round(x/100)*100
        list_of_strikes=strike_list(strike,at_strike)
        total_oi_towards_CE=0
        total_oi_towards_PE=0
        for element in list_of_strikes:
            total_oi_towards_CE = total_oi_towards_CE+int(c_data[c_data['StrikeRate']==element]['OpenInterest'])
        required_total_oi_towards_PE=total_oi_towards_CE*1.5
        vinay=0
        while True:
            total_oi_towards_PE = total_oi_towards_PE+int(p_data[p_data['StrikeRate']==at_strike+vinay]['OpenInterest'])
            vinay=vinay-100
            if total_oi_towards_PE>required_total_oi_towards_PE:
                put_strike=at_strike+vinay
                break
        put_scrip=int(p_data[p_data['StrikeRate']==put_strike]['ScripCode'])
        p_lastrate=float(p_data[p_data['StrikeRate']==put_strike]['LastRate'])
        test_order_put = Order(order_type='B',exchange='N',exchange_segment='D', scrip_code =put_scrip , quantity=25*prime_client['lots'], price=0 ,is_intraday=False,remote_order_id="tag")
        status = prime_client['login'].place_order(test_order)
        status_put = prime_client['login'].place_order(test_order_put)
        if status['Message']=='Success' and status_put['Message']=='Success':
            orders_track=orders(orders_track=orders_track,scrip_name=str(strike)+'_CE_S',lots=prime_client['lots'],price=c_lastrate)
            orders_track=orders(orders_track=orders_track,scrip_name=str(put_strike)+'_PE_B',lots=prime_client['lots'],price=p_lastrate)
            put_trade_taken=1
            control=1
            proj1=strike
        elif status['Message']=='Success' and status_put['Message']!='Success':
            orders_track=orders(orders_track=orders_track,scrip_name=str(strike)+'_CE_S',lots=prime_client['lots'],price=c_lastrate)
            put_trade_taken=0
            control=1
            proj1=strike
        elif status['Message']!='Success' and status_put['Message']=='Success':
            final_trade = Order(order_type='S',exchange='N',exchange_segment='D', scrip_code =put_scrip , quantity=25*prime_client['lots'], price=0 ,is_intraday=False,remote_order_id="tag")
            prime_client['login'].place_order(final_trade)
            breaker=1
    if control==1 and x>proj1:
        test_order = Order(order_type='B',exchange='N',exchange_segment='D', scrip_code =scrip , quantity=25*prime_client['lots'], price=0 ,is_intraday=False,remote_order_id="ta")
        status = prime_client['login'].place_order(test_order)
        c_lastrate=float(c_data[c_data['StrikeRate']==proj1]['LastRate'])
        orders_track=orders(orders_track=orders_track,scrip_name=str(proj1)+'_CE_B',lots=prime_client['lots'],price=c_lastrate)
        if put_trade_taken==1:
            test_order_put = Order(order_type='S',exchange='N',exchange_segment='D', scrip_code =put_scrip , quantity=25*prime_client['lots'], price=0 ,is_intraday=False,remote_order_id="tag")
            status_put = prime_client['login'].place_order(test_order_put)
            p_lastrate=float(p_data[p_data['StrikeRate']==put_strike]['LastRate'])
            orders_track=orders(orders_track=orders_track,scrip_name=str(put_strike)+'_PE_S',lots=prime_client['lots'],price=p_lastrate)
            put_trade_taken=0
        control=0
    if control==1 and proj-x<-dynamic_crossover/4:
        #exit call
        test_order = Order(order_type='B',exchange='N',exchange_segment='D', scrip_code =scrip , quantity=25*prime_client['lots'], price=0 ,is_intraday=False,remote_order_id="ta")
        status = prime_client['login'].place_order(test_order)
        c_lastrate=float(c_data[c_data['StrikeRate']==proj1]['LastRate'])
        orders_track=orders(orders_track=orders_track,scrip_name=str(proj1)+'_CE_B',lots=prime_client['lots'],price=c_lastrate)
        if put_trade_taken==1:
            test_order_put = Order(order_type='S',exchange='N',exchange_segment='D', scrip_code =put_scrip , quantity=25*prime_client['lots'], price=0 ,is_intraday=False,remote_order_id="tag")
            status_put = prime_client['login'].place_order(test_order_put)
            p_lastrate=float(p_data[p_data['StrikeRate']==put_strike]['LastRate'])
            orders_track=orders(orders_track=orders_track,scrip_name=str(put_strike)+'_PE_S',lots=prime_client['lots'],price=p_lastrate)
            put_trade_taken=0
        control=0
    if proj-x<-dynamic_crossover and control==0 and ind2>0:
        strike = int(np.floor(proj/100)*100)
        scrip=int(p_data[p_data['StrikeRate']==strike]['ScripCode'])
        p_lastrate=float(p_data[p_data['StrikeRate']==strike]['LastRate'])
        test_order = Order(order_type='S',exchange='N',exchange_segment='D', scrip_code =scrip , quantity=25*prime_client['lots'], price=0 ,is_intraday=False,remote_order_id="tag1")
        at_strike=round(x/100)*100
        list_of_strikes=strike_list(strike,at_strike)
        total_oi_towards_CE=0
        total_oi_towards_PE=0
        for element in list_of_strikes:
            total_oi_towards_PE = total_oi_towards_PE+int(p_data[p_data['StrikeRate']==element]['OpenInterest'])
        required_total_oi_towards_CE=total_oi_towards_PE*1.5
        vinay=0 
        while True:
            total_oi_towards_CE = total_oi_towards_CE+int(c_data[c_data['StrikeRate']==at_strike+vinay]['OpenInterest'])
            vinay=vinay+100
            if total_oi_towards_CE>required_total_oi_towards_CE:
                call_strike=at_strike+vinay
                break
        call_scrip=int(c_data[c_data['StrikeRate']==call_strike]['ScripCode'])
        c_lastrate=float(c_data[c_data['StrikeRate']==call_strike]['LastRate'])
        test_order_call = Order(order_type='B',exchange='N',exchange_segment='D', scrip_code =call_scrip , quantity=25*prime_client['lots'], price=0 ,is_intraday=False,remote_order_id="tag")
        status = prime_client['login'].place_order(test_order)
        status_call = prime_client['login'].place_order(test_order_call)
        if status['Message']=='Success' and status_call['Message']=='Success':
            orders_track=orders(orders_track=orders_track,scrip_name=str(strike)+'_PE_S',lots=prime_client['lots'],price=p_lastrate)
            orders_track=orders(orders_track=orders_track,scrip_name=str(call_strike)+'_CE_B',lots=prime_client['lots'],price=c_lastrate)
            call_trade_taken=1
            control=2
            proj2=strike
        elif status['Message']=='Success' and status_call['Message']!='Success':
            orders_track=orders(orders_track=orders_track,scrip_name=str(strike)+'_PE_S',lots=prime_client['lots'],price=p_lastrate)
            call_trade_taken=0
            control=2
            proj2=strike
        elif status['Message']!='Success' and status_call['Message']=='Success':
            final_order = Order(order_type='S',exchange='N',exchange_segment='D', scrip_code =call_scrip , quantity=25*prime_client['lots'], price=0 ,is_intraday=False,remote_order_id="tag")
            prime_client['login'].place_order(final_order)
            breaker=1
    if control==2 and x<proj2:
        test_order = Order(order_type='B',exchange='N',exchange_segment='D', scrip_code =scrip , quantity=25*prime_client['lots'], price=0 ,is_intraday=False,remote_order_id="ta1")
        status = prime_client['login'].place_order(test_order)
        p_lastrate=float(p_data[p_data['StrikeRate']==proj2]['LastRate'])
        orders_track=orders(orders_track=orders_track,scrip_name=str(proj2)+'_PE_B',lots=prime_client['lots'],price=p_lastrate)
        if call_trade_taken==1:
            test_order_call = Order(order_type='S',exchange='N',exchange_segment='D', scrip_code =call_scrip , quantity=25*prime_client['lots'], price=0 ,is_intraday=False,remote_order_id="tag")
            status_call = prime_client['login'].place_order(test_order_call)
            c_lastrate=float(c_data[c_data['StrikeRate']==call_strike]['LastRate'])
            orders_track=orders(orders_track=orders_track,scrip_name=str(call_strike)+'_CE_S',lots=prime_client['lots'],price=c_lastrate)
            call_trade_taken=0
        if status['Message']=='Success':
            control=0 
    if control==2 and proj-x>dynamic_crossover/4:
        #exit put
        test_order = Order(order_type='B',exchange='N',exchange_segment='D', scrip_code =scrip , quantity=25*prime_client['lots'], price=0 ,is_intraday=False,remote_order_id="ta1")
        status = prime_client['login'].place_order(test_order)
        p_lastrate=float(p_data[p_data['StrikeRate']==proj2]['LastRate'])
        orders_track=orders(orders_track=orders_track,scrip_name=str(proj2)+'_PE_B',lots=prime_client['lots'],price=p_lastrate)
        if call_trade_taken==1:
            test_order_call = Order(order_type='S',exchange='N',exchange_segment='D', scrip_code =call_scrip , quantity=25*prime_client['lots'], price=0 ,is_intraday=False,remote_order_id="tag")
            status_call = prime_client['login'].place_order(test_order_call)
            c_lastrate=float(c_data[c_data['StrikeRate']==call_strike]['LastRate'])
            orders_track=orders(orders_track=orders_track,scrip_name=str(call_strike)+'_CE_S',lots=prime_client['lots'],price=c_lastrate)
            call_trade_taken=0
        if status['Message']=='Success':
            control=0 
    ind_time = datetime.now(timezone("Asia/Kolkata")).strftime('%Y-%m-%d %H:%M:%S.%f')
    if int(ind_time[11:13])==15 and int(ind_time[14:16])>=25 :
        break
    live_orders_track=orders_track.copy()
    for amar in list(orders_track.keys()):
        temp_scrip=amar.split('_')
        lot_size=0
        for k in range(0,len(orders_track[amar])):
            lot_size=lot_size+orders_track[amar][k]['lots']
        if temp_scrip[2]=='B':
            strike = int(temp_scrip[0])
            c_lastrate=float(c_data[c_data['StrikeRate']==strike]['LastRate'])
            p_lastrate=float(p_data[p_data['StrikeRate']==strike]['LastRate'])
            live_orders_track=orders(orders_track=live_orders_track,scrip_name=amar[:-1]+'S',lots=lot_size,price=p_lastrate*(temp_scrip[1]=='PE')+c_lastrate*(temp_scrip[1]=='CE'))
        else :
            strike = int(temp_scrip[0])
            c_lastrate=float(c_data[c_data['StrikeRate']==strike]['LastRate'])
            p_lastrate=float(p_data[p_data['StrikeRate']==strike]['LastRate'])
            live_orders_track=orders(orders_track=live_orders_track,scrip_name=amar[:-1]+'B',lots=lot_size,price=p_lastrate*(temp_scrip[1]=='PE')+c_lastrate*(temp_scrip[1]=='CE'))
    
    ammu=net_profit(orders_track=live_orders_track)
    print('profit: ',ammu)
    if (tim-ammu)!=0:
        print(orders_track)
        print(live_orders_track)
        tim=ammu
    if ammu>100*prime_client['lots']:
        break
    if breaker==1:
        break
    import json
    data = json.dumps(orders_track)
    with open(client_name+".json","w") as f:
        f.write(data)

sleep(11)
if control==1 and breaker==0:
    test_order = Order(order_type='B',exchange='N',exchange_segment='D', scrip_code =scrip , quantity=25*prime_client['lots'], price=0 ,is_intraday=False,remote_order_id="ta")
    status = prime_client['login'].place_order(test_order)
    if put_trade_taken==1:
        test_order_put = Order(order_type='S',exchange='N',exchange_segment='D', scrip_code =put_scrip , quantity=25*prime_client['lots'], price=0 ,is_intraday=False,remote_order_id="tag")
        status_put = prime_client['login'].place_order(test_order_put)
elif control==2 and breaker==0:
    test_order = Order(order_type='B',exchange='N',exchange_segment='D', scrip_code =scrip , quantity=25*prime_client['lots'], price=0 ,is_intraday=False,remote_order_id="ta1")
    status = prime_client['login'].place_order(test_order)
    if call_trade_taken==1:
        test_order_call = Order(order_type='S',exchange='N',exchange_segment='D', scrip_code =call_scrip , quantity=25*prime_client['lots'], price=0 ,is_intraday=False,remote_order_id="tag")
        status_call = prime_client['login'].place_order(test_order_call)

sleep(5)
proj=projected(option_chain)
req_list_=[{"Exch":"N","ExchType":"C","Symbol":"BANKNIFTY","Scripcode":"999920005","OptionType":"EQ"}]          
a=prime_client['login'].fetch_market_feed(req_list_)
x=a['Data'][0]['LastRate']
if proj-x>0 :
    c_data=option_chain[option_chain['CPType']=='CE']
    strike = int(np.ceil(proj/100)*100)+800
    scrip=int(c_data[c_data['StrikeRate']==strike]['ScripCode'])
    test_order = Order(order_type='S',exchange='N',exchange_segment='D', scrip_code =scrip , quantity=25*prime_client['lots'], price=0 ,is_intraday=False,remote_order_id="tag")
    status = prime_client['login'].place_order(test_order)

if proj-x<0 :
    p_data=option_chain[option_chain['CPType']=='PE']
    strike = int(np.floor(proj/100)*100)-800
    scrip=int(p_data[p_data['StrikeRate']==strike]['ScripCode'])
    test_order = Order(order_type='S',exchange='N',exchange_segment='D', scrip_code =scrip , quantity=25*prime_client['lots'], price=0 ,is_intraday=False,remote_order_id="tag1")
    status = prime_client['login'].place_order(test_order)

indicator_data=pd.DataFrame(trend_indicator)
indicator_data.to_pickle('./oi_indicator.pkl')
