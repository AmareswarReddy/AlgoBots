#%%
import numpy as np
import pandas as pd
from time import sleep, strftime
from py5paisa import FivePaisaClient
from py5paisa.strategy import *
from py5paisa.logging import log_response
from datetime import datetime 
from datetime import date
import requests
from pytz import timezone 
from cred import *
import os
today=date.today()
d=today.strftime("20%y%m%d")
def new_short_straddle(main_str_format_pe,main_str_format_ce,main_str_pe,main_str_ce,pe_mem,ce_mem):  #do not try running this function seperately. this is just an add on to strangle. 
    
    while True:
        brk=0                
        #square off all positions
        if check(main_str_format_pe,main_str_format_ce) =='q':
            quit()
        pe_memory=pe_mem
        ce_memory=ce_mem
        req_list_=[{"Exch":"N","ExchType":"C","Symbol":"BANKNIFTY","Scripcode":"999920005","OptionType":"EQ"}]          
        a=strategy.fetch_market_feed(req_list_)
        x=a['Data'][0]['LastRate']
        req_list_PE={"Exch":"N","ExchType":"D","Symbol":main_str_pe+str(round(x/100)*100)+".00","Expiry":expiry,"StrikePrice":str(round(x/100)*100),"OptionType":"PE"}
        req_list_CE={"Exch":"N","ExchType":"D","Symbol":main_str_ce+str(round(x/100)*100)+".00","Expiry":expiry,"StrikePrice":str(round(x/100)*100),"OptionType":"CE"}
        req_list2=[req_list_CE,req_list_PE]
        req_list_PE_strikeprice=round(x/100)*100
        req_list_CE_strikeprice=round(x/100)*100
        strategy.adjustment_ce('banknifty',[str(ce_memory)],[str(req_list_CE_strikeprice)],str(lots),expiry,'D')
        strategy.adjustment_pe('banknifty',[str(pe_memory)],[str(req_list_PE_strikeprice)],str(lots),expiry,'D')
        ce_mem=str(req_list_CE_strikeprice)
        pe_mem=str(req_list_PE_strikeprice)
        b=strategy.fetch_market_feed(req_list2)
        ce_lastrate=b['Data'][0]['LastRate']
        pe_lastrate=b['Data'][1]['LastRate']
        Total_value_old=ce_lastrate+pe_lastrate
        Stop_loss=Total_value_old*1.2
        test=0
        while True :
            if Total_value_old>200 and test==0: # value 150 is anticipated optimised parameter
                b=strategy.fetch_market_feed(req_list2)
                ce_lastrate=b['Data'][0]['LastRate']
                pe_lastrate=b['Data'][1]['LastRate']
                Total_value_new=ce_lastrate+pe_lastrate
                if Total_value_new<Total_value_old:
                    Stop_loss=Total_value_new*1.2
                    Total_value_old=Total_value_new
                if Total_value_new>Stop_loss :
                    brk=1
            if brk==1:
                ind_time = datetime.now(timezone("Asia/Kolkata")).strftime('%Y-%m-%d %H:%M:%S.%f')
                print(ind_time)
                print('#########                                         stoplosshit                                         #########')
                break
            elif Total_value_old<=200: # value 150 is anticipated
                # individual stoploss shall be implimented and we will square off this time unlike taking new positions so that we don't lose more money
                control1=0
                control2=0
                test=1
                b=strategy.fetch_market_feed(req_list2)
                ce_lastrate=b['Data'][0]['LastRate']
                pe_lastrate=b['Data'][1]['LastRate']
                ce_lastrate_old=ce_lastrate
                pe_lastrate_old=pe_lastrate
                Stop_loss1=ce_lastrate*1.2
                Stop_loss2=pe_lastrate*1.2
                while True:
                    b=strategy.fetch_market_feed(req_list2)
                    ce_lastrate=b['Data'][0]['LastRate']
                    pe_lastrate=b['Data'][1]['LastRate']
                    if ce_lastrate<ce_lastrate_old and control1==0:
                        Stop_loss1=ce_lastrate*1.2
                        ce_lastrate_old=ce_lastrate
                    if ce_lastrate>Stop_loss1 and control1==0:
                        control1=1
                        print('square off call option')
                        strategy.square_off_ce('banknifty',[str(req_list_CE_strikeprice)],str(lots),expiry,'D')
                    if pe_lastrate<pe_lastrate_old and control2==0:
                        Stop_loss2=pe_lastrate*1.2
                        pe_lastrate_old=pe_lastrate
                    if pe_lastrate>Stop_loss2 and control2==0:
                        control2=1
                        print('square off put option')
                        strategy.square_off_pe('banknifty',[str(req_list_PE_strikeprice)],str(lots),expiry,'D')

#inputs to the code
expiry = str(input('enter the current expiry(Eg: "20210916" ) : '))
expiry2=0
if expiry==d:
    expiry2=str(input('enter the next expiry (Eg: "20210916" ) : '))
lots = int(input('enter the amount of lots(Eg: 25) :'))
day=int(input('enter the no. of days ellapsed since strategy implimentation :'))
while True:
    now=datetime.now(timezone("Asia/Kolkata"))
    if int(now.strftime('%H'))==9 and int(now.strftime('%M'))>=17:
        break
    elif int(now.strftime('%H'))>7:
        break
# formatting the input data 
temp={1:'JAN',
            2:'FEB',
            3:'MAR',
            4:'APR',
            5:'MAY',
            6:'JUN',
            7:'JUL',
            8:'AUG',
            9:'SEP',
            10:'OCT',
            11:'NOV',
            12:'DEC'}
main_str="BANKNIFTY "+expiry[-2:]+" "+temp[int(expiry[4:6])]+" "+expiry[:4]+" "
main_str_format = main_str[:14]+main_str[14:16].lower()+main_str[16:] 
main_str_pe = main_str+"PE "
main_str_ce = main_str+"CE "
main_str_format_pe=main_str_format+"PE "
main_str_format_ce=main_str_format+"CE "
expiry_format= expiry[:4]+'-'+expiry[4:6]+'-'+expiry[6:]
#%%
# Client login credentials
'''
cred={
    "APP_NAME":"5P56936208",
    "APP_SOURCE":"2179",
    "USER_ID":"w6MJ1dw5Yd0",
    "PASSWORD":"V7JkGTUudjt",
    "USER_KEY":"8Q4SSCEo0bOgroVMFcNB0nTTB6CGPQuE",
    "ENCRYPTION_KEY":"zeoxSiZ1pbQsOJ2vaMlOllCeJwNzRQeFlcjc0WGYyl5nLzoCRtWZI5Z2xwChp6Ip"
    }
strategy=strategies(user="vinaykumar7295@gmail.com", passw="vinay1@A", dob="19700701",cred=cred)
'''

cred={
    "APP_NAME":"5P53784053",
    "APP_SOURCE":"8023",
    "USER_ID":"y4JUrjToSOR",
    "PASSWORD":"y0tc7unqQAV",
    "USER_KEY":"DrmeltLdZo82SKaxWJoeMALor1Xaiqk5",
    "ENCRYPTION_KEY":"ANb7Y0ouVD5iX0jcPGwPMIEyQnwPjxuI"
    }
strategy=strategies(user="chandinimadduru123@gmail.com", passw="amar@0987", dob="19950820",cred=cred)

#%%
cred={
    "APP_NAME":"5P55115625",
    "APP_SOURCE":"8899",
    "USER_ID":"qZS8Qd5THYc",
    "PASSWORD":"O4X41D47h1g",
    "USER_KEY":"BDYHVFfDodmHw3RXeWzuc2acdOwczZ64",
    "ENCRYPTION_KEY":"ymueoJS7gS0bljQMYBTKStoWquugglDV"
    }
#%%
strategy=strategies(user="vinathi.bujji@gmail.com", passw="vinay1@A", dob="19940830",cred=cred)
#%%
Client=FivePaisaClient(email='vinathi.bujji@gmail.com', passwd='vinay1@A', dob='19940830',cred=cred)
Client.login()
#%%

# if the 
if day!=0:
    pos=strategy.positions()
    for i in range(0, len(pos)):
        if pos[i]['ScripName'][:25] == main_str_format_pe and  pos[i]['SellQty']-pos[i]['BuyQty']-pos[i]['NetQty']>0 :
            Current_PE_strikeprice=pos[i]['ScripName'][25:30]
            pe_mem=Current_PE_strikeprice
        elif pos[i]['ScripName'][:25] == main_str_format_ce and  pos[i]['SellQty']-pos[i]['BuyQty']-pos[i]['NetQty']>0:
            Current_CE_strikeprice=pos[i]['ScripName'][25:30]
            ce_mem=Current_CE_strikeprice

req_list_=[{"Exch":"N","ExchType":"C","Symbol":"BANKNIFTY","Scripcode":"999920005","OptionType":"EQ"}]          
a=strategy.fetch_market_feed(req_list_)
x=a['Data'][0]['LastRate']
req_list_PE=[{"Exch":"N","ExchType":"D","Symbol":main_str_pe+str(round(x/100)*100)+".00","Expiry":expiry,"StrikePrice":str(round(x/100)*100),"OptionType":"PE"}]
req_list_CE=[{"Exch":"N","ExchType":"D","Symbol":main_str_ce+str(round(x/100)*100)+".00","Expiry":expiry,"StrikePrice":str(round(x/100)*100),"OptionType":"CE"}]
req_list_PE_strikeprice=[round(x/100)*100]
req_list_CE_strikeprice=[round(x/100)*100]
for i in range(1,25):
    req_list_PE=req_list_PE+[{"Exch":"N","ExchType":"D","Symbol": main_str_pe+str(round(x/100)*100-i*100-2400)+".00","Expiry":expiry,"StrikePrice":str(round(x/100)*100-i*100-2400),"OptionType":"PE"}] 
    req_list_PE=[{"Exch":"N","ExchType":"D","Symbol": main_str_pe+str(round(x/100)*100+i*100-2400)+".00","Expiry":expiry,"StrikePrice":str(round(x/100)*100+i*100-2400),"OptionType":"PE"}]+req_list_PE
    req_list_PE_strikeprice=[round(x/100)*100+i*100-2400]+req_list_PE_strikeprice+[round(x/100)*100-i*100-2400]
    req_list_CE=req_list_CE+[{"Exch":"N","ExchType":"D","Symbol":main_str_ce+str(round(x/100)*100+i*100+2400)+".00","Expiry":expiry,"StrikePrice":str(round(x/100)*100+i*100+2400),"OptionType":"CE"}] 
    req_list_CE=[{"Exch":"N","ExchType":"D","Symbol":main_str_ce+str(round(x/100)*100-i*100+2400)+".00","Expiry":expiry,"StrikePrice":str(round(x/100)*100-i*100+2400),"OptionType":"CE"}]+req_list_CE
    req_list_CE_strikeprice=[round(x/100)*100-i*100+2400]+req_list_CE_strikeprice+[round(x/100)*100+i*100+2400]
live_PE=strategy.fetch_market_feed(req_list_PE)
live_PE_lastrate=[]
live_CE_lastrate=[]
live_CE = strategy.fetch_market_feed(req_list_CE)
for j in range(0,49):
    live_PE_lastrate=live_PE_lastrate+[live_PE['Data'][j]['LastRate']]
    live_CE_lastrate = live_CE_lastrate+[live_CE['Data'][j]['LastRate']]
live_PE_lastrate=[np.inf if x==0 else x for x in live_PE_lastrate]
live_CE_lastrate=[np.inf if x==0 else x for x in live_CE_lastrate]
CE_index_strikeprice=np.argmin(np.abs(np.array(live_CE_lastrate)-115))
CE_hedge_index_strikeprice = np.argmin(np.abs(np.array(live_CE_lastrate)-10))
PE_index_strikeprice=np.argmin(np.abs(np.array(live_PE_lastrate)-115))
PE_hedge_index_strikeprice = np.argmin(np.abs(np.array(live_PE_lastrate)-10))
CE_upper=req_list_CE_strikeprice[CE_index_strikeprice]
CE_hedge=req_list_CE_strikeprice[CE_hedge_index_strikeprice]
PE_lower=req_list_PE_strikeprice[PE_index_strikeprice]
PE_hedge=req_list_PE_strikeprice[PE_hedge_index_strikeprice]
if day==0:
    strategy.iron_condor("banknifty",[str(CE_hedge),str(PE_hedge)],[str(PE_lower),str(CE_upper)],str(lots),expiry,'D')
    sleep(3)
    pe_mem=PE_lower
    ce_mem=CE_upper
    CE_req={'Exch': 'N',
                'ExchType': 'D',
                'Symbol': main_str_ce+str(ce_mem)+'.00',
                'Expiry': expiry,
                'StrikePrice': str(ce_mem),
                'OptionType': 'CE'}

    PE_req={'Exch': 'N',
                'ExchType': 'D',
                'Symbol': main_str_pe+str(pe_mem)+'.00',
                'Expiry': expiry,
                'StrikePrice': str(pe_mem),
                'OptionType': 'PE'}
if day!=0:
    for i in range(0,len(req_list_CE)):
        if req_list_CE[i]['StrikePrice']==Current_CE_strikeprice:
            CE_req=req_list_CE[i]
            break
    for j in range(0,len(req_list_PE)):
        if req_list_PE[j]['StrikePrice']==Current_PE_strikeprice:
            PE_req=req_list_PE[j]
            break
Total_value_old=float('inf')
PE_req_old = ' '
CE_req_old = ' '
loop_control=0
brk=0
#%%
turn=0
money_heist=0
def check(main_str_format_pe,main_str_format_ce):
    Current_PE_strikeprice=0
    Current_CE_strikeprice=0
    positions = strategy.positions()
    for i in range(0, len(positions)):
        if positions[i]['ScripName'][:25] == main_str_format_pe and  positions[i]['SellQty']-positions[i]['BuyQty']-positions[i]['NetQty']>0 :
            Current_PE_strikeprice=positions[i]['ScripName'][25:30]
        elif positions[i]['ScripName'][:25] == main_str_format_ce and  positions[i]['SellQty']-positions[i]['BuyQty']-positions[i]['NetQty']>0 :
            Current_CE_strikeprice = positions[i]['ScripName'][25:30]
    if Current_PE_strikeprice==0 and Current_CE_strikeprice==0:
        print('quiting the program since no positions are active')
        return 'q'
    else :
        return 'dq'

def day_end_trades(ce_mem,pe_mem,lots,expiry,expiry2):
    #square off all active positions
    strategy.long_strangle("banknifty",[str(pe_mem),str(ce_mem)],lots,expiry,'D')
    while True:
        now=datetime.now(timezone("Asia/Kolkata"))
        if int(now.strftime('%H'))==15 and int(now.strftime('%M'))>=29:
            break
    sleep(33)
    if expiry2==0:
        strategy.short_strangle("banknifty",[str(pe_mem),str(ce_mem)],lots,expiry,'D')
    else :
        expiry=expiry2
        main_str="BANKNIFTY "+expiry[-2:]+" "+temp[int(expiry[4:6])]+" "+expiry[:4]+" "
        main_str_pe = main_str+"PE "
        main_str_ce = main_str+"CE "
        req_list_=[{"Exch":"N","ExchType":"C","Symbol":"BANKNIFTY","Scripcode":"999920005","OptionType":"EQ"}]          
        a=strategy.fetch_market_feed(req_list_)
        x=a['Data'][0]['LastRate']
        req_list_PE=[{"Exch":"N","ExchType":"D","Symbol":main_str_pe+str(round(x/100)*100)+".00","Expiry":expiry,"StrikePrice":str(round(x/100)*100),"OptionType":"PE"}]
        req_list_CE=[{"Exch":"N","ExchType":"D","Symbol":main_str_ce+str(round(x/100)*100)+".00","Expiry":expiry,"StrikePrice":str(round(x/100)*100),"OptionType":"CE"}]
        req_list_PE_strikeprice=[round(x/100)*100]
        req_list_CE_strikeprice=[round(x/100)*100]
        for i in range(1,25):
            req_list_PE=req_list_PE+[{"Exch":"N","ExchType":"D","Symbol": main_str_pe+str(round(x/100)*100-i*100-2400)+".00","Expiry":expiry,"StrikePrice":str(round(x/100)*100-i*100-2400),"OptionType":"PE"}] 
            req_list_PE=[{"Exch":"N","ExchType":"D","Symbol": main_str_pe+str(round(x/100)*100+i*100-2400)+".00","Expiry":expiry,"StrikePrice":str(round(x/100)*100+i*100-2400),"OptionType":"PE"}]+req_list_PE
            req_list_PE_strikeprice=[round(x/100)*100+i*100-2400]+req_list_PE_strikeprice+[round(x/100)*100-i*100-2400]
            req_list_CE=req_list_CE+[{"Exch":"N","ExchType":"D","Symbol":main_str_ce+str(round(x/100)*100+i*100+2400)+".00","Expiry":expiry,"StrikePrice":str(round(x/100)*100+i*100+2400),"OptionType":"CE"}] 
            req_list_CE=[{"Exch":"N","ExchType":"D","Symbol":main_str_ce+str(round(x/100)*100-i*100+2400)+".00","Expiry":expiry,"StrikePrice":str(round(x/100)*100-i*100+2400),"OptionType":"CE"}]+req_list_CE
            req_list_CE_strikeprice=[round(x/100)*100-i*100+2400]+req_list_CE_strikeprice+[round(x/100)*100+i*100+2400]
        live_PE=strategy.fetch_market_feed(req_list_PE)
        live_PE_lastrate=[]
        live_CE_lastrate=[]
        live_CE = strategy.fetch_market_feed(req_list_CE)
        for j in range(0,49):
            live_PE_lastrate=live_PE_lastrate+[live_PE['Data'][j]['LastRate']]
            live_CE_lastrate = live_CE_lastrate+[live_CE['Data'][j]['LastRate']]
        live_PE_lastrate=[np.inf if x==0 else x for x in live_PE_lastrate]
        live_CE_lastrate=[np.inf if x==0 else x for x in live_CE_lastrate]
        CE_index_strikeprice=np.argmin(np.abs(np.array(live_CE_lastrate)-115))
        CE_hedge_index_strikeprice = np.argmin(np.abs(np.array(live_CE_lastrate)-10))
        PE_index_strikeprice=np.argmin(np.abs(np.array(live_PE_lastrate)-115))
        PE_hedge_index_strikeprice = np.argmin(np.abs(np.array(live_PE_lastrate)-10))
        CE_upper=req_list_CE_strikeprice[CE_index_strikeprice]
        CE_hedge=req_list_CE_strikeprice[CE_hedge_index_strikeprice]
        PE_lower=req_list_PE_strikeprice[PE_index_strikeprice]
        PE_hedge=req_list_PE_strikeprice[PE_hedge_index_strikeprice]
        strategy.iron_condor("banknifty",[str(CE_hedge),str(PE_hedge)],[str(PE_lower),str(CE_upper)],str(lots),expiry,'D')


while True:
    req=[{"Exch":"N","ExchType":"C","Symbol":"BANKNIFTY","Scripcode":"999920005","OptionType":"EQ"}]          
    a=strategy.fetch_market_feed(req)
    x=a['Data'][0]['LastRate']     #int
    if check(main_str_format_pe,main_str_format_ce) =='q':
        quit()
    CE_req={'Exch': 'N',
                    'ExchType': 'D',
                    'Symbol': main_str_ce+str(ce_mem)+'.00',
                    'Expiry': expiry,
                    'StrikePrice': str(ce_mem),
                    'OptionType': 'CE'}

    PE_req={'Exch': 'N',
                    'ExchType': 'D',
                    'Symbol': main_str_pe+str(pe_mem)+'.00',
                    'Expiry': expiry,
                    'StrikePrice': str(pe_mem),
                    'OptionType': 'PE'}
    req_list_=[CE_req,PE_req]
    b=strategy.fetch_market_feed(req_list_)
    ce_lastrate=b['Data'][0]['LastRate']
    pe_lastrate=b['Data'][1]['LastRate']

    now=datetime.now(timezone("Asia/Kolkata"))
    if int(now.strftime('%H'))==15 and int(now.strftime('%M'))>=16 and int(now.strftime('%M'))<=20:
        day_end_trades(ce_mem,pe_mem,lots,expiry,expiry2)
        break

    if x<int(pe_mem) and money_heist==0 and (int(ce_mem)-int(pe_mem))>0:
        ind_time = datetime.now(timezone("Asia/Kolkata")).strftime('%Y-%m-%d %H:%M:%S.%f')
        positions=strategy.positions()
        log_response(ind_time)
        log_response(positions)
        log_response('Current CE Strikeprice: '+str(ce_mem))
        log_response('ce_lastrate: '+str(ce_lastrate))
        log_response('Current PE Strikeprice: '+str(pe_mem))
        log_response('pe_lastrate: '+str(pe_lastrate))
        strategy.adjustment_ce('banknifty',[str(ce_mem)],[str(pe_mem)],str(lots),expiry,'D')
        ind_time = datetime.now(timezone("Asia/Kolkata")).strftime('%Y-%m-%d %H:%M:%S.%f')
        log_response('re entry(Sold) ce at strikeprice: '+str(pe_mem))
        ce_mem=str(pe_mem)
        money_heist=1
    
    elif x>int(ce_mem) and money_heist==0 and (int(ce_mem)-int(pe_mem))>0:
        ind_time = datetime.now(timezone("Asia/Kolkata")).strftime('%Y-%m-%d %H:%M:%S.%f')
        positions=strategy.positions()
        log_response(ind_time)
        log_response(positions)
        log_response('Current CE Strikeprice: '+str(ce_mem))
        log_response('ce_lastrate: '+str(ce_lastrate))
        log_response('Current PE Strikeprice: '+str(pe_mem))
        log_response('pe_lastrate: '+str(pe_lastrate))
        strategy.adjustment_pe('banknifty',[str(pe_mem)],[str(ce_mem)],str(lots),expiry,'D')
        ind_time = datetime.now(timezone("Asia/Kolkata")).strftime('%Y-%m-%d %H:%M:%S.%f')
        log_response('re entry(Sold) pe at strikeprice: '+str(ce_mem))
        pe_mem=str(ce_mem)
        money_heist=1

    if ce_lastrate>2*pe_lastrate and int(CE_req['StrikePrice'])-int(PE_req['StrikePrice'])>0:
        ind_time = datetime.now(timezone("Asia/Kolkata")).strftime('%Y-%m-%d %H:%M:%S.%f')
        positions=strategy.positions()
        log_response(ind_time)
        log_response(positions)
        log_response('Current CE Strikeprice: '+str(ce_mem))
        log_response('ce_lastrate: '+str(ce_lastrate))
        log_response('Current PE Strikeprice: '+str(pe_mem))
        log_response('pe_lastrate: '+str(pe_lastrate))
        #the above step is taken because the delta(change in option price per unit change in stock price) will become so low that the further decrease in pe_lastrate will be far lower than the increase in ce_lastrate when stock price increases from the price it is now trading
        PE_req_old = PE_req['StrikePrice']   
        a=strategy.fetch_market_feed(req)
        x=a['Data'][0]['LastRate']
        req_list_PE=[{"Exch":"N","ExchType":"D","Symbol":main_str_pe+str(round(x/100)*100-2400)+".00","Expiry":expiry,"StrikePrice":str(round(x/100)*100-2400),"OptionType":"PE"}]
        req_list_PE_strikeprice=[round(x/100)*100-2400]
        for i in range(1,25):
            req_list_PE=req_list_PE+[{"Exch":"N","ExchType":"D","Symbol":main_str_pe+str(round(x/100)*100-i*100-2400)+".00","Expiry":expiry,"StrikePrice":str(round(x/100)*100-i*100-2400),"OptionType":"PE"}] 
            req_list_PE=[{"Exch":"N","ExchType":"D","Symbol": main_str_pe+str(round(x/100)*100+i*100-2400)+".00","Expiry":expiry,"StrikePrice":str(round(x/100)*100+i*100-2400),"OptionType":"PE"}]+req_list_PE
            req_list_PE_strikeprice=[round(x/100)*100+i*100-2400]+req_list_PE_strikeprice+[round(x/100)*100-i*100-2400]
        live_PE=strategy.fetch_market_feed(req_list_PE)
        live_PE_lastrate=[]
        for j in range(0,49):
            live_PE_lastrate=live_PE_lastrate+[live_PE['Data'][j]['LastRate']]
            live_PE_lastrate=[np.inf if x==0 else x for x in live_PE_lastrate]
        PE_index_strikeprice=np.argmin(np.abs(np.array(live_PE_lastrate)-0.85*ce_lastrate))
        #exit pe
        ind_time = datetime.now(timezone("Asia/Kolkata")).strftime('%Y-%m-%d %H:%M:%S.%f')
        log_response(ind_time)
        log_response('exit(bought) pe at srikeprice:  '+str(PE_req_old))
        strategy.adjustment_pe('banknifty',[str(pe_mem)],[str(req_list_PE_strikeprice[PE_index_strikeprice])],str(lots),expiry,'D')
        ind_time = datetime.now(timezone("Asia/Kolkata")).strftime('%Y-%m-%d %H:%M:%S.%f')
        log_response(ind_time)
        log_response('re entry(Sold) pe at strikeprice: '+str(req_list_PE_strikeprice[PE_index_strikeprice]))
        PE_req = req_list_PE[PE_index_strikeprice]
        log_response('New PE_req is : '+str(PE_req))
        pe_mem=str(req_list_PE_strikeprice[PE_index_strikeprice])


    elif pe_lastrate>=2*ce_lastrate and int(CE_req['StrikePrice'])-int(PE_req['StrikePrice'])>0:
        ind_time = datetime.now(timezone("Asia/Kolkata")).strftime('%Y-%m-%d %H:%M:%S.%f')
        positions=strategy.positions()
        log_response(ind_time)
        log_response(positions)
        log_response('Current CE Strikeprice: '+str(ce_mem))
        log_response('ce_lastrate: '+str(ce_lastrate))
        log_response('Current PE Strikeprice: '+str(pe_mem))
        log_response('pe_lastrate: '+str(pe_lastrate))
        #the above step is taken because the delta(change in option price per unit change in stock price) will become so low that the further decrease in ce_lastrate will be far lower than the increase in pe_lastrate when stock price decreases from the price it is now trading
        CE_req_old = CE_req['StrikePrice']
        a=strategy.fetch_market_feed(req)
        x=a['Data'][0]['LastRate']
        req_list_CE=[{"Exch":"N","ExchType":"D","Symbol":main_str_ce+str(round(x/100)*100+2400)+".00","Expiry":expiry,"StrikePrice":str(round(x/100)*100+2400),"OptionType":"CE"}]
        req_list_CE_strikeprice=[round(x/100)*100+2400]
        for i in range(1,25):
            req_list_CE=req_list_CE+[{"Exch":"N","ExchType":"D","Symbol":main_str_ce+str(round(x/100)*100+i*100+2400)+".00","Expiry":expiry,"StrikePrice":str(round(x/100)*100+i*100+2400),"OptionType":"CE"}] 
            req_list_CE=[{"Exch":"N","ExchType":"D","Symbol":main_str_ce+str(round(x/100)*100-i*100+2400)+".00","Expiry":expiry,"StrikePrice":str(round(x/100)*100-i*100+2400),"OptionType":"CE"}]+req_list_CE
            req_list_CE_strikeprice=[round(x/100)*100-i*100+2400]+req_list_CE_strikeprice+[round(x/100)*100+i*100+2400]
        live_CE=strategy.fetch_market_feed(req_list_CE)
        live_CE_lastrate=[]
        for j in range(0,49):
            live_CE_lastrate=live_CE_lastrate+[live_CE['Data'][j]['LastRate']]
        live_CE_lastrate=[np.inf if x==0 else x for x in live_CE_lastrate]
        CE_index_strikeprice=np.argmin(np.abs(np.array(live_CE_lastrate)-0.85*pe_lastrate))
        ind_time = datetime.now(timezone("Asia/Kolkata")).strftime('%Y-%m-%d %H:%M:%S.%f')
        log_response(ind_time)
        log_response('exit(bought) ce at srikeprice:  '+str(CE_req_old))
        strategy.adjustment_ce('banknifty',[str(ce_mem)],[str(req_list_CE_strikeprice[CE_index_strikeprice])],str(lots),expiry,'D')
        ind_time = datetime.now(timezone("Asia/Kolkata")).strftime('%Y-%m-%d %H:%M:%S.%f')
        log_response(ind_time)
        log_response('re entry(Sold) ce at strikeprice: '+str(req_list_CE_strikeprice[CE_index_strikeprice]))
        CE_req = req_list_CE[CE_index_strikeprice]
        log_response('New CE_req is : '+str(CE_req))
        ce_mem=str(req_list_CE_strikeprice[CE_index_strikeprice])
    now=datetime.now()
    if (int(CE_req['StrikePrice'])-int(PE_req['StrikePrice'] ))<=0 :   #or now.strftime('%H %M')=='15 15'
        if turn==0:
            turn=1
        elif turn==1:
            Total_value_new=ce_lastrate+pe_lastrate
            if Total_value_new<Total_value_old:
                Stop_loss=Total_value_new*1.12
                Total_value_old=Total_value_new
            if Total_value_new>Stop_loss :
                brk=1
                print('stoplosshit')
                new_short_straddle(main_str_format_pe, main_str_format_ce,main_str_pe,main_str_ce,pe_mem,ce_mem)           
    if brk==1:
        break
# %%
