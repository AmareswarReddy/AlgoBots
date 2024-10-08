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
client_name=input('enter the client name Eg: vinathi,bhaskar ')
lots=int(input('lots (Eg:3):'))
#%%
ind_time = datetime.now(timezone("Asia/Kolkata")).strftime('%Y-%m-%d %H:%M:%S.%f')
while int(ind_time[11:13])*60+int(ind_time[14:16])<561 or int(ind_time[11:13])*60+int(ind_time[14:16])>885 :
    ind_time = datetime.now(timezone("Asia/Kolkata")).strftime('%Y-%m-%d %H:%M:%S.%f')
#%%
prime_client=client_login(client=client_name,lots=lots)
expiry_timestamps=prime_client['login'].get_expiry("N","BANKNIFTY")
current_expiry_time_stamp=int(expiry_timestamps['Expiry'][0]['ExpiryDate'][6:19])
option_chain=pd.DataFrame(prime_client['login'].get_option_chain("N","BANKNIFTY",current_expiry_time_stamp)['Options'])
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

def projected():
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
while True:
    while True:
        try :
            expiry_timestamps=prime_client['login'].get_expiry("N","BANKNIFTY")
            current_expiry_time_stamp=int(expiry_timestamps['Expiry'][0]['ExpiryDate'][6:19])
            option_chain=pd.DataFrame(prime_client['login'].get_option_chain("N","BANKNIFTY",current_expiry_time_stamp)['Options'])
            break
        except Exception :
            pass
    req_list_=[{"Exch":"N","ExchType":"C","Symbol":"BANKNIFTY","Scripcode":"999920005","OptionType":"EQ"}]      
    a=prime_client['login'].fetch_market_feed(req_list_)
    x=a['Data'][0]['LastRate']
    simple=simple_trend()
    complex=complex_trend()
    proj=projected()
    ind_time = datetime.now(timezone("Asia/Kolkata")).strftime('%Y-%m-%d %H:%M:%S.%f')
    trend_indicator['timestamp']=trend_indicator['timestamp']+[ind_time]
    trend_indicator['simple']=trend_indicator['simple']+[simple]
    trend_indicator['complex']=trend_indicator['complex']+[complex]
    trend_indicator['projected']=trend_indicator['projected']+[proj]
    trend_indicator['spotprice']=trend_indicator['spotprice']+[x]
    print(simple)
    print(complex)
    print(proj)
    c_data=option_chain[option_chain['CPType']=='CE']
    p_data=option_chain[option_chain['CPType']=='PE']
    #strategy
    c1=int(c_data[c_data['StrikeRate']==int(np.floor(x/100)*100)]['LastRate'])
    c2=int(c_data[c_data['StrikeRate']==int(np.ceil(x/100)*100)]['LastRate'])
    p1=int(p_data[p_data['StrikeRate']==int(np.floor(x/100)*100)]['LastRate'])
    p2=int(p_data[p_data['StrikeRate']==int(np.ceil(x/100)*100)]['LastRate'])
    dynamic_crossover=(c1+c2+p1+p2)/20
    if proj-x>dynamic_crossover and control==0:
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
        required_total_oi_towards_PE=total_oi_towards_CE*2
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
    if proj-x<-dynamic_crossover and control==0:
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
        required_total_oi_towards_CE=total_oi_towards_PE*2
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
    print(ammu)
    if (tim-ammu)!=0:
        print(orders_track)
        print(live_orders_track)
        tim=ammu
    if ammu>100*prime_client['lots']:
        break


sleep(11)
if control==1:
    test_order = Order(order_type='B',exchange='N',exchange_segment='D', scrip_code =scrip , quantity=25*prime_client['lots'], price=0 ,is_intraday=False,remote_order_id="ta")
    status = prime_client['login'].place_order(test_order)
    if put_trade_taken==1:
        test_order_put = Order(order_type='S',exchange='N',exchange_segment='D', scrip_code =put_scrip , quantity=25*prime_client['lots'], price=0 ,is_intraday=False,remote_order_id="tag")
        status_put = prime_client['login'].place_order(test_order_put)
elif control==2:
    test_order = Order(order_type='B',exchange='N',exchange_segment='D', scrip_code =scrip , quantity=25*prime_client['lots'], price=0 ,is_intraday=False,remote_order_id="ta1")
    status = prime_client['login'].place_order(test_order)
    if call_trade_taken==1:
        test_order_call = Order(order_type='S',exchange='N',exchange_segment='D', scrip_code =call_scrip , quantity=25*prime_client['lots'], price=0 ,is_intraday=False,remote_order_id="tag")
        status_call = prime_client['login'].place_order(test_order_call)

sleep(5)
proj=projected()
req_list_=[{"Exch":"N","ExchType":"C","Symbol":"BANKNIFTY","Scripcode":"999920005","OptionType":"EQ"}]          
a=prime_client['login'].fetch_market_feed(req_list_)
x=a['Data'][0]['LastRate']
if proj-x>0 :
    c_data=option_chain[option_chain['CPType']=='CE']
    strike = int(np.ceil(proj/100)*100)+500
    scrip=int(c_data[c_data['StrikeRate']==strike]['ScripCode'])
    test_order = Order(order_type='S',exchange='N',exchange_segment='D', scrip_code =scrip , quantity=25*prime_client['lots'], price=0 ,is_intraday=False,remote_order_id="tag")
    status = prime_client['login'].place_order(test_order)

if proj-x<0 :
    p_data=option_chain[option_chain['CPType']=='PE']
    strike = int(np.floor(proj/100)*100)-500
    scrip=int(p_data[p_data['StrikeRate']==strike]['ScripCode'])
    test_order = Order(order_type='S',exchange='N',exchange_segment='D', scrip_code =scrip , quantity=25*prime_client['lots'], price=0 ,is_intraday=False,remote_order_id="tag1")
    status = prime_client['login'].place_order(test_order)

indicator_data=pd.DataFrame(trend_indicator)
indicator_data.to_pickle('./oi_indicator.pkl')
plt.plot(trend_indicator['timestamp'],trend_indicator['spotprice'])
plt.plot(trend_indicator['timestamp'],trend_indicator['projected'])
plt.show()
# %%
a=np.array(trend_indicator['projected'])-np.array(trend_indicator['spotprice'])