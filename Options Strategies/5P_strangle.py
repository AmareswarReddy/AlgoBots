#%%
# Update scripmaster file every week
import numpy as np
import pandas as pd
from time import sleep, strftime
from py5paisa import FivePaisaClient
from py5paisa.strategy import *
from cred import *
from datetime import datetime 
main_str="BANKNIFTY 09 SEP 2021 "
main_str_format = "BANKNIFTY 09 Sep 2021 "
main_str_pe = main_str+"PE "
main_str_ce = main_str+"CE "
main_str_format_pe=main_str_format+"PE "
main_str_format_ce=main_str_format+"CE "
money_in_account = float(input('enter the amount of money in the account in lakhs(Eg: 2) :'))
lots = int(np.floor(money_in_account/1.65)*25)
expiry = "20210909"
expiry_format= expiry[:4]+'-'+expiry[4:6]+'-'+expiry[6:]
day=int(input('enter the no. of days ellapsed since strategy implimentation :'))
script=pd.read_csv('scripmaster-csv-format.csv')
cred={
    "APP_NAME":"5P56936208",
    "APP_SOURCE":"2179",
    "USER_ID":"w6MJ1dw5Yd0",
    "PASSWORD":"V7JkGTUudjt",
    "USER_KEY":"8Q4SSCEo0bOgroVMFcNB0nTTB6CGPQuE",
    "ENCRYPTION_KEY":"zeoxSiZ1pbQsOJ2vaMlOllCeJwNzRQeFlcjc0WGYyl5nLzoCRtWZI5Z2xwChp6Ip"
    }
Client = FivePaisaClient(email='vinaykumar7295@gmail.com', passwd='godofwarvinay1@A',dob='19700701', cred=cred)
Client.login()
#%%
#NOTE : Symbol has to be in the same format as specified in the example below.
#banknifty scripcode=999920005
#N	C	999920005	BANKNIFTY 	EQ	1980-01-01 00:00:00	EQ	0	Z  BANKNIFTY                                         
req_list_=[{"Exch":"N","ExchType":"C","Symbol":"BANKNIFTY","Scripcode":"999920005","OptionType":"EQ"}]          
a=Client.fetch_market_feed(req_list_)
#%%
if day!=0:
    pos=Client.positions()
    for i in range(0, len(pos)):
        if pos[i]['ScripName'][:25] == main_str_format_pe and  pos[i]['NetQty']<0 :
            Current_PE_strikeprice=pos[i]['ScripName'][25:30]
        elif pos[i]['ScripName'][:25] == main_str_format_ce and  pos[i]['NetQty']<0 :
            Current_CE_strikeprice=pos[i]['ScripName'][25:30]

'''
# Fetches holdings
Client.holdings()
# Fetches margin
Client.margin()
# Fetches positions
Client.positions()
# Fetches the order book of the client
Client.order_book()
'''
#%%
"""
let the nifty bank is trading at 36000
"""
#x = input('Bank Nifty Value on the day of taking the trades')
x=a['Data'][0]['LastRate']
req_list_PE=[{"Exch":"N","ExchType":"D","Symbol":main_str_pe+str(int(x/100)*100)+".00","Expiry":expiry,"StrikePrice":str(int(x/100)*100),"OptionType":"PE"}]
req_list_CE=[{"Exch":"N","ExchType":"D","Symbol":main_str_ce+str(int(x/100)*100)+".00","Expiry":expiry,"StrikePrice":str(int(x/100)*100),"OptionType":"CE"}]
req_list_PE_strikeprice=[int(x/100)*100]
req_list_CE_strikeprice=[int(x/100)*100]
for i in range(1,25):
    req_list_PE=req_list_PE+[{"Exch":"N","ExchType":"D","Symbol": main_str_pe+str(int(x/100)*100-i*100)+".00","Expiry":expiry,"StrikePrice":str(int(x/100)*100-i*100),"OptionType":"PE"}] 
    req_list_PE_strikeprice=req_list_PE_strikeprice+[int(x/100)*100-i*100]
    req_list_CE=req_list_CE+[{"Exch":"N","ExchType":"D","Symbol":main_str_ce+str(int(x/100)*100+i*100)+".00","Expiry":expiry,"StrikePrice":str(int(x/100)*100+i*100),"OptionType":"CE"}] 
    req_list_CE_strikeprice=req_list_CE_strikeprice+[int(x/100)*100+i*100]
live_PE=Client.fetch_market_feed(req_list_PE)
live_PE_lastrate=[]
live_CE_lastrate=[]
live_CE = Client.fetch_market_feed(req_list_CE)
for j in range(0,25):
    live_PE_lastrate=live_PE_lastrate+[live_PE['Data'][j]['LastRate']]
    live_CE_lastrate = live_CE_lastrate+[live_CE['Data'][j]['LastRate']]
CE_index_strikeprice=np.argmin(np.abs(np.array(live_CE_lastrate)-115))
CE_hedge_index_strikeprice = np.argmin(np.abs(np.array(live_CE_lastrate)-15))
PE_index_strikeprice=np.argmin(np.abs(np.array(live_PE_lastrate)-115))
PE_hedge_index_strikeprice = np.argmin(np.abs(np.array(live_PE_lastrate)-15))
CE_upper=req_list_CE_strikeprice[CE_index_strikeprice]
CE_hedge=req_list_CE_strikeprice[CE_hedge_index_strikeprice]
PE_lower=req_list_PE_strikeprice[PE_index_strikeprice]
PE_hedge=req_list_PE_strikeprice[PE_hedge_index_strikeprice]

#%%
strategy=strategies(user="vinaykumar7295@gmail.com", passw="godofwarvinay1@A", dob="19700701",cred=cred)
#short_strangle(<symbol>,<List of sell strike price>,<qty>,<expiry>,<Order Type>)
#strategy.short_strangle('banknifty',[str(PE_lower),str(CE_upper)],'25','20210902','D')
#iron_condor(<symbol>,<List of buy strike prices>,<List of sell strike price>,<qty>,<expiry>,<Order Type>)
if day==0:
    strategy.iron_condor("banknifty",[str(CE_hedge),str(PE_hedge)],[str(PE_lower),str(CE_upper)],str(lots),expiry,'D')
positions= Client.positions()

CE_req=req_list_CE[CE_index_strikeprice]
PE_req=req_list_PE[PE_index_strikeprice]
#%%
if day!=0:
    for i in range(0,len(req_list_CE)):
        if req_list_CE[i]['StrikePrice']==str(Current_CE_strikeprice):
            CE_req=req_list_CE[i]
            break
    for j in range(0,len(req_list_PE)):
        if req_list_PE[j]['StrikePrice']==str(Current_PE_strikeprice):
            PE_req=req_list_PE[j]
            break

Total_value_old=float('inf')
# %%
while True:
    req_list_=[CE_req,PE_req]
    b=Client.fetch_market_feed(req_list_)
    ce_lastrate=b['Data'][0]['LastRate']
    pe_lastrate=b['Data'][1]['LastRate']
    positions= Client.positions()
    if ce_lastrate>=2*pe_lastrate and int(CE_req['StrikePrice'])-int(PE_req['StrikePrice'])>100:
        for i in range(0,len(positions)):
            if req_list_[1]['Symbol']==str.upper(positions[i]['ScripName']):
                awesome_ammu=i
                req=[{"Exch":"N","ExchType":"C","Symbol":"BANKNIFTY","Scripcode":"999920005","OptionType":"EQ"}]          
                a=Client.fetch_market_feed(req)
                x=a['Data'][0]['LastRate']
                req_list_PE=[{"Exch":"N","ExchType":"D","Symbol":main_str_pe+str(int(x/100)*100)+".00","Expiry":expiry,"StrikePrice":str(int(x/100)*100),"OptionType":"PE"}]
                req_list_PE_strikeprice=[int(x/100)*100]
                for i in range(1,25):
                    req_list_PE=req_list_PE+[{"Exch":"N","ExchType":"D","Symbol":main_str_pe+str(int(x/100)*100-i*100)+".00","Expiry":expiry,"StrikePrice":str(int(x/100)*100-i*100),"OptionType":"PE"}] 
                    req_list_PE_strikeprice=req_list_PE_strikeprice+[int(x/100)*100-i*100]
                live_PE=Client.fetch_market_feed(req_list_PE)
                live_PE_lastrate=[]
                for j in range(0,25):
                    live_PE_lastrate=live_PE_lastrate+[live_PE['Data'][j]['LastRate']]
                PE_index_strikeprice=np.argmin(np.abs(np.array(live_PE_lastrate)-0.89*ce_lastrate))
                #exit pe
                test_order = Order(order_type='B',exchange='N',exchange_segment='D', scrip_code=positions[awesome_ammu]['ScripCode'], quantity=lots,price=0,is_intraday=False,atmarket=True)
                Client.place_order(test_order)
                
                #sell pe which is 80 to 95% of ce
                scripcode_=str(int(script[script['Expiry']==expiry_format+' 14:30:00'][script['StrikeRate']==req_list_PE_strikeprice[PE_index_strikeprice]][script['CpType']=='PE']['Scripcode']))
                test_order2=Order(order_type='S',exchange='N',exchange_segment='D', scrip_code=scripcode_, quantity=lots,price=0,is_intraday=False,atmarket=True)
                Client.place_order(test_order2)
                PE_req = req_list_PE[PE_index_strikeprice]
                break
        


    elif pe_lastrate>=2*ce_lastrate and int(CE_req['StrikePrice'])-int(PE_req['StrikePrice'])>100:
        for i in range(0,len(positions)):
            if req_list_[0]['Symbol']==str.upper(positions[i]['ScripName']):
                awesome_ammu=i
                req=[{"Exch":"N","ExchType":"C","Symbol":"BANKNIFTY","Scripcode":"999920005","OptionType":"EQ"}]          
                a=Client.fetch_market_feed(req)
                x=a['Data'][0]['LastRate']
                req_list_CE=[{"Exch":"N","ExchType":"D","Symbol":main_str_ce+str(int(x/100)*100)+".00","Expiry":expiry,"StrikePrice":str(int(x/100)*100),"OptionType":"CE"}]
                req_list_PE_strikeprice=[int(x/100)*100]
                for i in range(1,25):
                    req_list_CE=req_list_CE+[{"Exch":"N","ExchType":"D","Symbol":main_str_ce+str(int(x/100)*100+i*100)+".00","Expiry":expiry,"StrikePrice":str(int(x/100)*100-i*100),"OptionType":"CE"}] 
                    req_list_CE_strikeprice=req_list_CE_strikeprice+[int(x/100)*100+i*100]
                live_CE=Client.fetch_market_feed(req_list_CE)
                live_CE_lastrate=[]
                for j in range(0,25):
                    live_CE_lastrate=live_CE_lastrate+[live_CE['Data'][j]['LastRate']]
                CE_index_strikeprice=np.argmin(np.abs(np.array(live_CE_lastrate)-0.89*pe_lastrate))
                #exit pe
                test_order = Order(order_type='B',exchange='N',exchange_segment='D', scrip_code=positions[awesome_ammu]['ScripCode'], quantity=lots,price=0,is_intraday=False,atmarket=True)
                Client.place_order(test_order)
                
                #sell pe which is 80 to 95% of ce
                scripcode_=str(int(script[script['Expiry']==expiry_format+' 14:30:00'][script['StrikeRate']==req_list_CE_strikeprice[CE_index_strikeprice]][script['CpType']=='CE']['Scripcode']))
                test_order2=Order(order_type='S',exchange='N',exchange_segment='D', scrip_code=scripcode_, quantity=lots,price=0,is_intraday=False,atmarket=True)
                Client.place_order(test_order2)
                CE_req = req_list_CE[CE_index_strikeprice]
                break
    if (int(CE_req['StrikePrice'])-int(PE_req['StrikePrice'] )<=100) and now.strftime("%H:%M")=='15:15':
        now=datetime.now()
        Total_value_new=ce_lastrate+pe_lastrate
        if Total_value_new<Total_value_old:
            Stop_loss=Total_value_new*1.15
            Total_value_old=Total_value_new
        if Total_value_new>Stop_loss or now.strftime('%H %M')=='15 15':
            brk=1
            #square off all positions
            test_order = Order(order_type='B',exchange='N',exchange_segment='D', scrip_code=str(int(script[script['FullName']==main_str_format_pe+CE_req['StrikePrice']+'.00']['Scripcode'])), quantity=lots,price=0,is_intraday=False,atmarket=True)
            Client.place_order(test_order)
            test_order = Order(order_type='B',exchange='N',exchange_segment='D', scrip_code=str(int(script[script['FullName']==main_str_format_ce+CE_req['StrikePrice']+'.00']['Scripcode'])), quantity=lots,price=0,is_intraday=False,atmarket=True)
            Client.place_order(test_order)
            test_order = Order(order_type='S',exchange='N',exchange_segment='D', scrip_code=str(int(script[script['FullName']==main_str_format_ce+str(CE_hedge)+'.00']['Scripcode'])), quantity=lots,price=0,is_intraday=False,atmarket=True)
            Client.place_order(test_order)
            test_order = Order(order_type='S',exchange='N',exchange_segment='D', scrip_code=str(int(script[script['FullName']==main_str_format_pe+str(PE_hedge)+'.00']['Scripcode'])), quantity=lots,price=0,is_intraday=False,atmarket=True)
            Client.place_order(test_order)
    if brk==1:
        break
# %%
