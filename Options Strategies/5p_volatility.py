#%%
import numpy as np
import pandas as pd
from time import sleep, strftime
from py5paisa import FivePaisaClient
from py5paisa.strategy import *
from cred import *
from datetime import datetime 
main_str="BANKNIFTY 16 SEP 2021 "
main_str_format = "BANKNIFTY 16 Sep 2021 "
main_str_pe = main_str+"PE "
main_str_ce = main_str+"CE "
main_str_format_pe=main_str_format+"PE "
main_str_format_ce=main_str_format+"CE "
money_in_account = float(input('enter the amount of money in the account in lakhs(Eg: 2) :'))
lots = int(np.floor(money_in_account/1.65)*25)
expiry = "20210916"
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
req_list_=[{"Exch":"N","ExchType":"C","Symbol":"BANKNIFTY","Scripcode":"999920005","OptionType":"EQ"}]          
a=Client.fetch_market_feed(req_list_)
x=a['Data'][0]['LastRate']
req_list_PE=[{"Exch":"N","ExchType":"D","Symbol":main_str_pe+str(round(x/100)*100)+".00","Expiry":expiry,"StrikePrice":str(round(x/100)*100),"OptionType":"PE"}]
req_list_CE=[{"Exch":"N","ExchType":"D","Symbol":main_str_ce+str(round(x/100)*100)+".00","Expiry":expiry,"StrikePrice":str(round(x/100)*100),"OptionType":"CE"}]
req_list_PE_strikeprice=[round(x/100)*100]
req_list_CE_strikeprice=[round(x/100)*100]
for i in range(1,25):
    req_list_PE=req_list_PE+[{"Exch":"N","ExchType":"D","Symbol": main_str_pe+str(round(x/100)*100-i*100)+".00","Expiry":expiry,"StrikePrice":str(round(x/100)*100-i*100),"OptionType":"PE"}] 
    req_list_PE=[{"Exch":"N","ExchType":"D","Symbol": main_str_pe+str(round(x/100)*100+i*100)+".00","Expiry":expiry,"StrikePrice":str(round(x/100)*100+i*100),"OptionType":"PE"}] +req_list_PE
    req_list_PE_strikeprice=req_list_PE_strikeprice+[round(x/100)*100-i*100]
    req_list_PE_strikeprice=[round(x/100)*100+i*100]+req_list_PE_strikeprice
    req_list_CE=req_list_CE+[{"Exch":"N","ExchType":"D","Symbol":main_str_ce+str(round(x/100)*100+i*100)+".00","Expiry":expiry,"StrikePrice":str(round(x/100)*100+i*100),"OptionType":"CE"}] 
    req_list_CE=[{"Exch":"N","ExchType":"D","Symbol":main_str_ce+str(round(x/100)*100-i*100)+".00","Expiry":expiry,"StrikePrice":str(round(x/100)*100-i*100),"OptionType":"CE"}] +req_list_CE
    req_list_CE_strikeprice=req_list_CE_strikeprice+[round(x/100)*100+i*100]
    req_list_CE_strikeprice=[round(x/100)*100-i*100]+req_list_CE_strikeprice
live_PE=Client.fetch_market_feed(req_list_PE)
live_CE = Client.fetch_market_feed(req_list_CE)
live_PE_lastrate=[]
live_CE_lastrate=[]
for j in range(0,25):
    live_PE_lastrate=live_PE_lastrate+[live_PE['Data'][j]['LastRate']]
    live_CE_lastrate = live_CE_lastrate+[live_CE['Data'][j]['LastRate']]

# %%
