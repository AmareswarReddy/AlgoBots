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
lots=int(input('enter the number of lots (Eg:3):'))
#expiry=input('enter the expiry Eg:"07-Apr-2022"')
cred={
    "APP_NAME":"5P55115625",
    "APP_SOURCE":'8899',
    "USER_ID":"qZS8Qd5THYc",
    "PASSWORD":"O4X41D47h1g",
    "USER_KEY":"BDYHVFfDodmHw3RXeWzuc2acdOwczZ64",
    "ENCRYPTION_KEY":"jhxJH0k6BIUL6VnXYPIAcqTZLqYWhkLc"
    }
vinathi_strategy=strategies(user="vinathi.bujji@gmail.com", passw="kittu1@A", dob="19940830",cred=cred)
vinathi=FivePaisaClient(email="vinathi.bujji@gmail.com", passwd="kittu1@A", dob="19940830",cred=cred)
vinathi.login()

while True:
    ind_time = datetime.now(timezone("Asia/Kolkata")).strftime('%Y-%m-%d %H:%M:%S.%f')
    if int(ind_time[11:13])==9 and int(ind_time[14:16])>21:
        break
expiry_timestamps=vinathi.get_expiry("N","BANKNIFTY")
current_expiry_time_stamp=int(expiry_timestamps['Expiry'][0]['ExpiryDate'][6:19])
option_chain=pd.DataFrame(vinathi.get_option_chain("N","BANKNIFTY",current_expiry_time_stamp)['Options'])
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
    a=vinathi_strategy.fetch_market_feed(req_list_)
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
    a=vinathi_strategy.fetch_market_feed(req_list_)
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


trend_indicator={
            'timestamp':[],
            'simple':[],
            'complex':[],
            'projected':[],
            'spotprice':[]
            }
control=0
while True:
    expiry_timestamps=vinathi.get_expiry("N","BANKNIFTY")
    current_expiry_time_stamp=int(expiry_timestamps['Expiry'][0]['ExpiryDate'][6:19])
    option_chain=pd.DataFrame(vinathi.get_option_chain("N","BANKNIFTY",current_expiry_time_stamp)['Options'])
    req_list_=[{"Exch":"N","ExchType":"C","Symbol":"BANKNIFTY","Scripcode":"999920005","OptionType":"EQ"}]          
    a=vinathi_strategy.fetch_market_feed(req_list_)
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
    #strategy
    if proj-x>0 and control==0:
        c_data=option_chain[option_chain['CPType']=='CE']
        strike = int(np.ceil(proj/100)*100)
        scrip=int(c_data[c_data['StrikeRate']==strike]['ScripCode'])
        test_order = Order(order_type='S',exchange='N',exchange_segment='D', scrip_code =scrip , quantity=25*lots, price=0 ,is_intraday=False,remote_order_id="tag")
        status = vinathi.place_order(test_order)
        if status['Message']=='Success':
            control=1
            proj1=strike
    if control==1 and x>proj1:
        test_order = Order(order_type='B',exchange='N',exchange_segment='D', scrip_code =scrip , quantity=25*lots, price=0 ,is_intraday=False,remote_order_id="ta")
        status = vinathi.place_order(test_order)
        if status['Message']=='Success':
            control=0
    if control==1 and proj-x<0:
        #exit call
        test_order = Order(order_type='B',exchange='N',exchange_segment='D', scrip_code =scrip , quantity=25*lots, price=0 ,is_intraday=False,remote_order_id="ta")
        status = vinathi.place_order(test_order)
        if status['Message']=='Success':
            control=0
    if proj-x<0 and control==0:
        p_data=option_chain[option_chain['CPType']=='PE']
        strike = int(np.floor(proj/100)*100)
        scrip=int(p_data[p_data['StrikeRate']==strike]['ScripCode'])
        test_order = Order(order_type='S',exchange='N',exchange_segment='D', scrip_code =scrip , quantity=25*lots, price=0 ,is_intraday=False,remote_order_id="tag1")
        status = vinathi.place_order(test_order)
        if status['Message']=='Success':
            control=2
            proj2=strike
    if control==2 and x<proj2:
        test_order = Order(order_type='B',exchange='N',exchange_segment='D', scrip_code =scrip , quantity=25*lots, price=0 ,is_intraday=False,remote_order_id="ta1")
        status = vinathi.place_order(test_order)
        if status['Message']=='Success':
            control=0 
    if control==2 and proj-x>0:
        #exit put
        test_order = Order(order_type='B',exchange='N',exchange_segment='D', scrip_code =scrip , quantity=25*lots, price=0 ,is_intraday=False,remote_order_id="ta1")
        status = vinathi.place_order(test_order)
        if status['Message']=='Success':
            control=0 
    ind_time = datetime.now(timezone("Asia/Kolkata")).strftime('%Y-%m-%d %H:%M:%S.%f')
    if int(ind_time[11:13])==15:
        break


sleep(69)
if control==1:
    test_order = Order(order_type='B',exchange='N',exchange_segment='D', scrip_code =scrip , quantity=25*lots, price=0 ,is_intraday=False,remote_order_id="ta")
    status = vinathi.place_order(test_order)
elif control==2:
    test_order = Order(order_type='B',exchange='N',exchange_segment='D', scrip_code =scrip , quantity=25*lots, price=0 ,is_intraday=False,remote_order_id="ta1")
    status = vinathi.place_order(test_order)
sleep(60*26)
proj=projected()
req_list_=[{"Exch":"N","ExchType":"C","Symbol":"BANKNIFTY","Scripcode":"999920005","OptionType":"EQ"}]          
a=vinathi_strategy.fetch_market_feed(req_list_)
x=a['Data'][0]['LastRate']
if proj-x>0 :
    c_data=option_chain[option_chain['CPType']=='CE']
    strike = int(np.ceil(proj/100)*100)+500
    scrip=int(c_data[c_data['StrikeRate']==strike]['ScripCode'])
    test_order = Order(order_type='S',exchange='N',exchange_segment='D', scrip_code =scrip , quantity=25*lots, price=0 ,is_intraday=False,remote_order_id="tag")
    status = vinathi.place_order(test_order)

if proj-x<0 :
    p_data=option_chain[option_chain['CPType']=='PE']
    strike = int(np.floor(proj/100)*100)-500
    scrip=int(p_data[p_data['StrikeRate']==strike]['ScripCode'])
    test_order = Order(order_type='S',exchange='N',exchange_segment='D', scrip_code =scrip , quantity=25*lots, price=0 ,is_intraday=False,remote_order_id="tag1")
    status = vinathi.place_order(test_order)

pd.DataFrame(trend_indicator)
plt.plot(trend_indicator['timestamp'],trend_indicator['spotprice'])
plt.plot(trend_indicator['timestamp'],trend_indicator['projected'])
plt.show()
# %%
a=np.array(trend_indicator['projected'])-np.array(trend_indicator['spotprice'])
# %%
