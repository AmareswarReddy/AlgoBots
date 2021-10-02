#%%
import numpy as np
import pandas as pd
from time import sleep, strftime
from py5paisa import FivePaisaClient
from py5paisa.strategy import *
from cred import *
from datetime import datetime 
def straddle(expiry,strike):  #    expiry = "20211007", strike="36500"
    cred={
    "APP_NAME":"5P56936208",
    "APP_SOURCE":"2179",
    "USER_ID":"w6MJ1dw5Yd0",
    "PASSWORD":"V7JkGTUudjt",
    "USER_KEY":"8Q4SSCEo0bOgroVMFcNB0nTTB6CGPQuE",
    "ENCRYPTION_KEY":"zeoxSiZ1pbQsOJ2vaMlOllCeJwNzRQeFlcjc0WGYyl5nLzoCRtWZI5Z2xwChp6Ip"
    }
    strategy=strategies(user="vinaykumar7295@gmail.com", passw="godofwarvinay1@A", dob="19700701",cred=cred)
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
    
    pos=Client.positions()
    for i in range(0, len(pos)):
        if pos[i]['ScripName'][:25] == main_str_format_pe and  pos[i]['NetQty']<0 :
            Current_PE_strikeprice=pos[i]['ScripName'][25:30]
            lots = -pos[i]['NetQty']
        elif pos[i]['ScripName'][:25] == main_str_format_ce and  pos[i]['NetQty']<0 :
            Current_CE_strikeprice = pos[i]['ScripName'][25:30]
                
    added_pe=0
    added_ce=0
    added_ce_manager=0
    added_pe_manager=0
    orders_to_remember=[]
    while True :
        req = [{"Exch":"N","ExchType":"C","Symbol":"BANKNIFTY","Scripcode":"999920005","OptionType":"EQ"}]          
        a = Client.fetch_market_feed(req)
        x = a['Data'][0]['LastRate']     #int
        req_list_PE = [{"Exch":"N","ExchType":"D","Symbol":main_str_pe+str(Current_PE_strikeprice)+".00","Expiry":expiry,"StrikePrice":str(Current_PE_strikeprice),"OptionType":"PE"}]
        req_list_CE = [{"Exch":"N","ExchType":"D","Symbol":main_str_ce+str(Current_CE_strikeprice)+".00","Expiry":expiry,"StrikePrice":str(Current_CE_strikeprice),"OptionType":"CE"}]
        live_PE = Client.fetch_market_feed(req_list_PE)
        live_CE = Client.fetch_market_feed(req_list_CE)
        pe_lastrate = live_PE['Data'][0]['LastRate']
        ce_lastrate = live_CE['Data'][0]['LastRate']
        net_ce=ce_lastrate+added_ce+added_ce_manager
        net_pe=pe_lastrate+added_pe+added_pe_manager
        added_ce_manager=added_ce+added_ce_manager
        added_pe_manager=added_pe+added_pe_manager
        added_pe=0
        added_ce=0
        if net_ce >= 2*net_pe:
            trigger='ce'
            #add a pe position which is 25% of ce
            req_list_=[{"Exch":"N","ExchType":"C","Symbol":"BANKNIFTY","Scripcode":"999920005","OptionType":"EQ"}]          
            a=Client.fetch_market_feed(req_list_)
            x=a['Data'][0]['LastRate']
            req_list_PE=[{"Exch":"N","ExchType":"D","Symbol":main_str_pe+str(round(x/100)*100)+".00","Expiry":expiry,"StrikePrice":str(round(x/100)*100),"OptionType":"PE"}]
            req_list_PE_strikeprice=[round(x/100)*100]
            for i in range(1,25):
                req_list_PE=req_list_PE+[{"Exch":"N","ExchType":"D","Symbol": main_str_pe+str(round(x/100)*100-i*100)+".00","Expiry":expiry,"StrikePrice":str(round(x/100)*100-i*100),"OptionType":"PE"}] 
                req_list_PE=[{"Exch":"N","ExchType":"D","Symbol": main_str_pe+str(round(x/100)*100+i*100)+".00","Expiry":expiry,"StrikePrice":str(round(x/100)*100+i*100),"OptionType":"PE"}] +req_list_PE
                req_list_PE_strikeprice=req_list_PE_strikeprice+[round(x/100)*100-i*100]
                req_list_PE_strikeprice=[round(x/100)*100+i*100]+req_list_PE_strikeprice
            live_PE=Client.fetch_market_feed(req_list_PE)
            live_PE_lastrate=[]
            for j in range(0,49):
                live_PE_lastrate=live_PE_lastrate+[live_PE['Data'][j]['LastRate']]
            PE_index_strikeprice=np.argmin(np.abs(np.array(live_PE_lastrate)-0.25*ce_lastrate))
            PE_req = req_list_PE[PE_index_strikeprice]
            scrip_code=str(int(script[script['FullName']==main_str_format_pe+PE_req['StrikePrice']+'.00']['Scripcode']))
            test_order = Order(order_type='S',exchange='N',exchange_segment='D', scrip_code=scrip_code, quantity=lots,price=0,is_intraday=False,atmarket=True)
            test_order_b = Order(order_type='B',exchange='N',exchange_segment='D', scrip_code=scrip_code, quantity=lots,price=0,is_intraday=False,atmarket=True)
            Client.place_order(test_order)
        added_pe = live_PE_lastrate[PE_index_strikeprice]

        if net_pe >= 2*net_ce:
            trigger='pe'
            #add a ce position which is 25% of pe
            req_list_=[{"Exch":"N","ExchType":"C","Symbol":"BANKNIFTY","Scripcode":"999920005","OptionType":"EQ"}]          
            a=Client.fetch_market_feed(req_list_)
            x=a['Data'][0]['LastRate']
            req_list_CE=[{"Exch":"N","ExchType":"D","Symbol":main_str_ce+str(round(x/100)*100)+".00","Expiry":expiry,"StrikePrice":str(round(x/100)*100),"OptionType":"CE"}]
            req_list_CE_strikeprice=[round(x/100)*100]
            for i in range(1,25):
                req_list_CE=req_list_CE+[{"Exch":"N","ExchType":"D","Symbol":main_str_ce+str(round(x/100)*100+i*100)+".00","Expiry":expiry,"StrikePrice":str(round(x/100)*100+i*100),"OptionType":"CE"}] 
                req_list_CE=[{"Exch":"N","ExchType":"D","Symbol":main_str_ce+str(round(x/100)*100-i*100)+".00","Expiry":expiry,"StrikePrice":str(round(x/100)*100-i*100),"OptionType":"CE"}] +req_list_CE
                req_list_CE_strikeprice=req_list_CE_strikeprice+[round(x/100)*100+i*100]
                req_list_CE_strikeprice=[round(x/100)*100-i*100]+req_list_CE_strikeprice
            live_CE = Client.fetch_market_feed(req_list_CE)
            live_CE_lastrate=[]
            for j in range(0,49):
                live_CE_lastrate = live_CE_lastrate+[live_CE['Data'][j]['LastRate']] 
            CE_index_strikeprice=np.argmin(np.abs(np.array(live_CE_lastrate)-0.25*pe_lastrate))
            CE_req = req_list_CE[CE_index_strikeprice]
            scrip_code=str(int(script[script['FullName']==main_str_format_pe+CE_req['StrikePrice']+'.00']['Scripcode']))
            test_order = Order(order_type='S',exchange='N',exchange_segment='D', scrip_code=scrip_code, quantity=lots,price=0,is_intraday=False,atmarket=True)
            test_order_b = Order(order_type='B',exchange='N',exchange_segment='D', scrip_code=scrip_code, quantity=lots,price=0,is_intraday=False,atmarket=True)
            Client.place_order(test_order)
        added_ce = live_CE_lastrate[CE_index_strikeprice]
        if trigger=='pe' or trigger=='ce':
            orders_to_remember=orders_to_remember+[test_order_b]
        if trigger=='ce' and net_ce<net_pe*0.95:
            #exit from the positions
            strategy.long_straddle("banknifty",strike,lots,expiry,'D')
            for i in range(0,len(orders_to_remember)):
                Client.place_order(orders_to_remember[i])

        elif trigger=='pe' and net_pe<net_ce*0.95:
            # exit from the positions
            strategy.long_straddle("banknifty",strike,lots,expiry,'D')
            for i in range(0,len(orders_to_remember)):
                Client.place_order(orders_to_remember[i])
# %%
