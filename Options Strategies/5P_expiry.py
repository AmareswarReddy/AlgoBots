#%%

# works only when you don't have positions of banknifty other than strategy based banknifty positions 
# if you take banknifty positions anyway. Please look at the lines from 72 in the code 
import numpy as np
import pandas as pd
from time import sleep
from py5paisa import FivePaisaClient
from py5paisa.strategy import *
from cred import *
main_str="BANKNIFTY 09 SEP 2021 "
main_str_format = "BANKNIFTY 09 Sep 2021 "
expiry = "20210909"
expiry_format= expiry[:4]+'-'+expiry[4:6]+'-'+expiry[6:]
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
req_list_=[{"Exch":"N","ExchType":"C","Symbol":"BANKNIFTY","Scripcode":"999920005","OptionType":"EQ"}]
a=Client.fetch_market_feed(req_list_)
x=a['Data'][0]['LastRate']
floor_strikeprice=str(int(np.floor(x/100)*100))
ceil_strikeprice=str(int(np.ceil(x/100)*100))
req_list_PE=[{"Exch":"N","ExchType":"D","Symbol":main_str+'PE '+floor_strikeprice+".00","Expiry":expiry,"StrikePrice":floor_strikeprice,"OptionType":"PE"},
                      {"Exch":"N","ExchType":"D","Symbol":main_str+'PE '+ceil_strikeprice+".00","Expiry":expiry,"StrikePrice":ceil_strikeprice,"OptionType":"PE"}]
req_list_CE=[{"Exch":"N","ExchType":"D","Symbol":main_str+'CE '+floor_strikeprice+".00","Expiry":expiry,"StrikePrice":floor_strikeprice,"OptionType":"CE"},
                       {"Exch":"N","ExchType":"D","Symbol":main_str+'CE '+ceil_strikeprice+".00","Expiry":expiry,"StrikePrice":ceil_strikeprice,"OptionType":"CE"}]
live_PE = Client.fetch_market_feed(req_list_PE)
live_CE = Client.fetch_market_feed(req_list_CE)
live_PE_lastrate = [live_PE['Data'][0]['LastRate']]+[live_PE['Data'][1]['LastRate']]
live_CE_lastrate = [live_CE['Data'][0]['LastRate']]+[live_CE['Data'][1]['LastRate']]
strategy_sell_value=np.max(live_PE_lastrate+live_CE_lastrate)
temp=np.argmax(live_PE_lastrate+live_CE_lastrate)
if temp<=1:
    strategy_on='PE '
    hole=0
else :
    strategy_on='CE '
    hole=1
if temp%2==0:
    strategy_strikeprice=int(floor_strikeprice)
else :
    strategy_strikeprice=int(ceil_strikeprice)

temp2=np.ceil(strategy_sell_value/100)*100
strategy_lower_strikeprice=str(int(strategy_strikeprice-temp2))
strategy_upper_strikeprice=str(int(strategy_strikeprice+temp2))
strategy_on_strikeprice=str(int(strategy_strikeprice))
main_str_name = main_str+strategy_on
main_str_name_format=main_str_format+strategy_on

#%%
lower_sripcode=str(int(script[script['FullName']==main_str_name_format+strategy_lower_strikeprice+'.00']['Scripcode']))
upper_scripcode=str(int(script[script['FullName']==main_str_name_format+strategy_upper_strikeprice+'.00']['Scripcode']))
on_scripcode=str(int(script[script['FullName']==main_str_name_format+strategy_on_strikeprice+'.00']['Scripcode']))
test_order = Order(order_type='B',exchange='N',exchange_segment='D', scrip_code=lower_sripcode, quantity=25,price=0,is_intraday=False,atmarket=True)
Client.place_order(test_order)
test_order = Order(order_type='B',exchange='N',exchange_segment='D', scrip_code=upper_scripcode, quantity=25,price=0,is_intraday=False,atmarket=True)
Client.place_order(test_order)
test_order = Order(order_type='S',exchange='N',exchange_segment='D', scrip_code=on_scripcode, quantity=50,price=0,is_intraday=False,atmarket=True)
Client.place_order(test_order)
sleep(5)
awesome=Client.positions()
potential_profit=0
for i in range(0,len(awesome)):
    if awesome[i]['ScripName'][:22] == main_str_format :
        buy_avg=awesome[i]['BuyAvgRate']
        sell_avg=awesome[i]['SellAvgRate']
        buy_qty=awesome[i]['BuyQty']
        sell_qty = awesome[i]['SellQty']
        potential_profit = potential_profit + (buy_avg+sell_avg)*(sell_qty-buy_qty)
for i in range(0,len(awesome)):
    if awesome[i]['ScripCode'] == int(lower_sripcode):
        lower_lastrate=awesome[i]['LTP']
    elif awesome[i]['ScripCode'] == int(upper_scripcode):
        upper_lastrate=awesome[i]['LTP']
    elif awesome[i]['ScripCode'] == int(on_scripcode):
        on_lastrate=awesome[i]['LTP']
# if all orders are placed we should not get error in the next 2 lines
lower_breakeven = int(strategy_lower_strikeprice)+(lower_lastrate+upper_lastrate-2*on_lastrate)
upper_breakeven = int(strategy_upper_strikeprice)-(lower_lastrate+upper_lastrate-2*on_lastrate)
SL_criteria_lower = (lower_breakeven+int(strategy_on_strikeprice))/2
SL_criteria_upper = (upper_breakeven+int(strategy_on_strikeprice))/2
#%%
if hole==0:
    scripcode_ce = str(int(script[script['FullName']==main_str_format+'CE '+strategy_on_strikeprice+'.00']['Scripcode']))
    while True:
        req_list_=[{"Exch":"N","ExchType":"C","Symbol":"BANKNIFTY","Scripcode":"999920005","OptionType":"EQ"}]
        a=Client.fetch_market_feed(req_list_)
        x=a['Data'][0]['LastRate']
        profit=0
        for i in range(0,len(awesome)):
            if awesome[i]['ScripName'][:22] == main_str_format :
                buy_avg=awesome[i]['BuyAvgRate']
                sell_avg=awesome[i]['SellAvgRate']
                buy_qty=awesome[i]['BuyQty']
                sell_qty = awesome[i]['SellQty']
                LTP=awesome[i]['LTP']
                profit = profit + (buy_avg+sell_avg)*(sell_qty-buy_qty)+(buy_qty-sell_qty)*LTP
        if profit>=potential_profit*0.75:
            #square off all the positions
            brk=1
            test_order = Order(order_type='S',exchange='N',exchange_segment='D', scrip_code=lower_sripcode, quantity=25,price=0,is_intraday=False,atmarket=True)
            Client.place_order(test_order)
            test_order = Order(order_type='S',exchange='N',exchange_segment='D', scrip_code=upper_scripcode, quantity=25,price=0,is_intraday=False,atmarket=True)
            Client.place_order(test_order)
            test_order = Order(order_type='B',exchange='N',exchange_segment='D', scrip_code=on_scripcode, quantity=50,price=0,is_intraday=False,atmarket=True)
            Client.place_order(test_order)
            test_order = Order(order_type='B',exchange='N',exchange_segment='D', scrip_code=on_scripcode, quantity=25,price=0,is_intraday=False,atmarket=True)
            Client.place_order(test_order)
            break

        if x >= upper_breakeven-5:
            #adjustment begins with a sell order at (on_strikeprice pe)
            test_order = Order(order_type='S',exchange='N',exchange_segment='D', scrip_code=on_scripcode, quantity=25,price=0,is_intraday=False,atmarket=True)
            Client.place_order(test_order)
            while True:
                req_list_=[{"Exch":"N","ExchType":"C","Symbol":"BANKNIFTY","Scripcode":"999920005","OptionType":"EQ"}]
                a=Client.fetch_market_feed(req_list_)
                x=a['Data'][0]['LastRate']
                profit=0
                for i in range(0,len(awesome)):
                    if awesome[i]['ScripName'][:22] == main_str_format :
                        buy_avg=awesome[i]['BuyAvgRate']
                        sell_avg=awesome[i]['SellAvgRate']
                        buy_qty=awesome[i]['BuyQty']
                        sell_qty = awesome[i]['SellQty']
                        LTP=awesome[i]['LTP']
                        profit = profit + (buy_avg+sell_avg)*(sell_qty-buy_qty)+(buy_qty-sell_qty)*LTP
                if profit>=potential_profit*0.75:
                    #square off all the positions
                    brk=1
                    test_order = Order(order_type='S',exchange='N',exchange_segment='D', scrip_code=lower_sripcode, quantity=25,price=0,is_intraday=False,atmarket=True)
                    Client.place_order(test_order)
                    test_order = Order(order_type='S',exchange='N',exchange_segment='D', scrip_code=upper_scripcode, quantity=25,price=0,is_intraday=False,atmarket=True)
                    Client.place_order(test_order)
                    test_order = Order(order_type='B',exchange='N',exchange_segment='D', scrip_code=on_scripcode, quantity=50,price=0,is_intraday=False,atmarket=True)
                    Client.place_order(test_order)
                    test_order = Order(order_type='B',exchange='N',exchange_segment='D', scrip_code=on_scripcode, quantity=25,price=0,is_intraday=False,atmarket=True)
                    Client.place_order(test_order)
                    break
                elif x<=SL_criteria_lower:
                    brk=1
                    #square off all the positions
                    test_order = Order(order_type='S',exchange='N',exchange_segment='D', scrip_code=lower_sripcode, quantity=25,price=0,is_intraday=False,atmarket=True)
                    Client.place_order(test_order)
                    test_order = Order(order_type='S',exchange='N',exchange_segment='D', scrip_code=upper_scripcode, quantity=25,price=0,is_intraday=False,atmarket=True)
                    Client.place_order(test_order)
                    test_order = Order(order_type='B',exchange='N',exchange_segment='D', scrip_code=on_scripcode, quantity=50,price=0,is_intraday=False,atmarket=True)
                    Client.place_order(test_order)
                    test_order = Order(order_type='B',exchange='N',exchange_segment='D', scrip_code=on_scripcode, quantity=25,price=0,is_intraday=False,atmarket=True)
                    Client.place_order(test_order)
                    break
        if brk==1:
            break

        elif x<=lower_breakeven+5:
            #adjustment begins with a sell order at (on_strikeprice ce)
            test_order = Order(order_type='S',exchange='N',exchange_segment='D', scrip_code=scripcode_ce, quantity=25,price=0,is_intraday=False,atmarket=True)
            Client.place_order(test_order)
            while True:
                req_list_=[{"Exch":"N","ExchType":"C","Symbol":"BANKNIFTY","Scripcode":"999920005","OptionType":"EQ"}]
                a=Client.fetch_market_feed(req_list_)
                x=a['Data'][0]['LastRate']
                profit=0
                for i in range(0,len(awesome)):
                    if awesome[i]['ScripName'][:22] == main_str_format :
                        buy_avg=awesome[i]['BuyAvgRate']
                        sell_avg=awesome[i]['SellAvgRate']
                        buy_qty=awesome[i]['BuyQty']
                        sell_qty = awesome[i]['SellQty']
                        LTP=awesome[i]['LTP']
                        profit = profit + (buy_avg+sell_avg)*(sell_qty-buy_qty)+(buy_qty-sell_qty)*LTP
                if profit>=potential_profit*0.75:
                    #square off all the positions
                    brk=1
                    test_order = Order(order_type='S',exchange='N',exchange_segment='D', scrip_code=lower_sripcode, quantity=25,price=0,is_intraday=False,atmarket=True)
                    Client.place_order(test_order)
                    test_order = Order(order_type='S',exchange='N',exchange_segment='D', scrip_code=upper_scripcode, quantity=25,price=0,is_intraday=False,atmarket=True)
                    Client.place_order(test_order)
                    test_order = Order(order_type='B',exchange='N',exchange_segment='D', scrip_code=on_scripcode, quantity=50,price=0,is_intraday=False,atmarket=True)
                    Client.place_order(test_order)
                    test_order = Order(order_type='B',exchange='N',exchange_segment='D', scrip_code=on_scripcode, quantity=25,price=0,is_intraday=False,atmarket=True)
                    Client.place_order(test_order)
                    break
                elif x>=SL_criteria_upper:
                    brk=1
                    #square off all the positions
                    test_order = Order(order_type='S',exchange='N',exchange_segment='D', scrip_code=lower_sripcode, quantity=25,price=0,is_intraday=False,atmarket=True)
                    Client.place_order(test_order)
                    test_order = Order(order_type='S',exchange='N',exchange_segment='D', scrip_code=upper_scripcode, quantity=25,price=0,is_intraday=False,atmarket=True)
                    Client.place_order(test_order)
                    test_order = Order(order_type='B',exchange='N',exchange_segment='D', scrip_code=on_scripcode, quantity=50,price=0,is_intraday=False,atmarket=True)
                    Client.place_order(test_order)
                    test_order = Order(order_type='B',exchange='N',exchange_segment='D', scrip_code=scripcode_ce, quantity=25,price=0,is_intraday=False,atmarket=True)
                    Client.place_order(test_order)
                    break
        if brk==1:
            break
elif hole==1:
    scripcode_pe = str(int(script[script['FullName']==main_str_format+'PE '+strategy_on_strikeprice+'.00']['Scripcode']))
    while True:
        req_list_=[{"Exch":"N","ExchType":"C","Symbol":"BANKNIFTY","Scripcode":"999920005","OptionType":"EQ"}]
        a=Client.fetch_market_feed(req_list_)
        x=a['Data'][0]['LastRate']
        if x >=upper_breakeven-5:
            #adjustment begins with a sell order at (on_strikeprice pe)
            test_order = Order(order_type='S',exchange='N',exchange_segment='D', scrip_code=scripcode_pe, quantity=25,price=0,is_intraday=False,atmarket=True)
            Client.place_order(test_order)
            while True:
                req_list_=[{"Exch":"N","ExchType":"C","Symbol":"BANKNIFTY","Scripcode":"999920005","OptionType":"EQ"}]
                a=Client.fetch_market_feed(req_list_)
                x=a['Data'][0]['LastRate']
                profit=0
                for i in range(0,len(awesome)):
                    if awesome[i]['ScripName'][:22] == main_str_format :
                        buy_avg=awesome[i]['BuyAvgRate']
                        sell_avg=awesome[i]['SellAvgRate']
                        buy_qty=awesome[i]['BuyQty']
                        sell_qty = awesome[i]['SellQty']
                        LTP=awesome[i]['LTP']
                        profit = profit + (buy_avg+sell_avg)*(sell_qty-buy_qty)+(buy_qty-sell_qty)*LTP
                if profit>=potential_profit*0.75:
                    #square off all the positions
                    brk=1
                    test_order = Order(order_type='S',exchange='N',exchange_segment='D', scrip_code=lower_sripcode, quantity=25,price=0,is_intraday=False,atmarket=True)
                    Client.place_order(test_order)
                    test_order = Order(order_type='S',exchange='N',exchange_segment='D', scrip_code=upper_scripcode, quantity=25,price=0,is_intraday=False,atmarket=True)
                    Client.place_order(test_order)
                    test_order = Order(order_type='B',exchange='N',exchange_segment='D', scrip_code=on_scripcode, quantity=50,price=0,is_intraday=False,atmarket=True)
                    Client.place_order(test_order)
                    test_order = Order(order_type='B',exchange='N',exchange_segment='D', scrip_code=on_scripcode, quantity=25,price=0,is_intraday=False,atmarket=True)
                    Client.place_order(test_order)
                    break
                elif x<=SL_criteria_lower:
                    brk=1
                    #square off all the positions
                    test_order = Order(order_type='S',exchange='N',exchange_segment='D', scrip_code=lower_sripcode, quantity=25,price=0,is_intraday=False,atmarket=True)
                    Client.place_order(test_order)
                    test_order = Order(order_type='S',exchange='N',exchange_segment='D', scrip_code=upper_scripcode, quantity=25,price=0,is_intraday=False,atmarket=True)
                    Client.place_order(test_order)
                    test_order = Order(order_type='B',exchange='N',exchange_segment='D', scrip_code=on_scripcode, quantity=50,price=0,is_intraday=False,atmarket=True)
                    Client.place_order(test_order)
                    test_order = Order(order_type='B',exchange='N',exchange_segment='D', scrip_code=scripcode_pe, quantity=25,price=0,is_intraday=False,atmarket=True)
                    Client.place_order(test_order)
                    break
        if brk==1:
            break

        elif x<=lower_breakeven+5:
            #adjustment begins with a sell order at (on_strikeprice ce)
            test_order = Order(order_type='S',exchange='N',exchange_segment='D', scrip_code=on_scripcode, quantity=25,price=0,is_intraday=False,atmarket=True)
            Client.place_order(test_order)
            while True:
                req_list_=[{"Exch":"N","ExchType":"C","Symbol":"BANKNIFTY","Scripcode":"999920005","OptionType":"EQ"}]
                a=Client.fetch_market_feed(req_list_)
                x=a['Data'][0]['LastRate']
                profit=0
                for i in range(0,len(awesome)):
                    if awesome[i]['ScripName'][:22] == main_str_format :
                        buy_avg=awesome[i]['BuyAvgRate']
                        sell_avg=awesome[i]['SellAvgRate']
                        buy_qty=awesome[i]['BuyQty']
                        sell_qty = awesome[i]['SellQty']
                        LTP=awesome[i]['LTP']
                        profit = profit + (buy_avg+sell_avg)*(sell_qty-buy_qty)+(buy_qty-sell_qty)*LTP
                if profit>=potential_profit*0.75:
                    #square off all the positions
                    brk=1
                    test_order = Order(order_type='S',exchange='N',exchange_segment='D', scrip_code=lower_sripcode, quantity=25,price=0,is_intraday=False,atmarket=True)
                    Client.place_order(test_order)
                    test_order = Order(order_type='S',exchange='N',exchange_segment='D', scrip_code=upper_scripcode, quantity=25,price=0,is_intraday=False,atmarket=True)
                    Client.place_order(test_order)
                    test_order = Order(order_type='B',exchange='N',exchange_segment='D', scrip_code=on_scripcode, quantity=50,price=0,is_intraday=False,atmarket=True)
                    Client.place_order(test_order)
                    test_order = Order(order_type='B',exchange='N',exchange_segment='D', scrip_code=on_scripcode, quantity=25,price=0,is_intraday=False,atmarket=True)
                    Client.place_order(test_order)
                    break
                elif x>=SL_criteria_upper:
                    brk=1
                    #square off all the positions
                    test_order = Order(order_type='S',exchange='N',exchange_segment='D', scrip_code=lower_sripcode, quantity=25,price=0,is_intraday=False,atmarket=True)
                    Client.place_order(test_order)
                    test_order = Order(order_type='S',exchange='N',exchange_segment='D', scrip_code=upper_scripcode, quantity=25,price=0,is_intraday=False,atmarket=True)
                    Client.place_order(test_order)
                    test_order = Order(order_type='B',exchange='N',exchange_segment='D', scrip_code=on_scripcode, quantity=50,price=0,is_intraday=False,atmarket=True)
                    Client.place_order(test_order)
                    test_order = Order(order_type='B',exchange='N',exchange_segment='D', scrip_code=on_scripcode, quantity=25,price=0,is_intraday=False,atmarket=True)
                    Client.place_order(test_order)
                    break
        if brk==1:
            break