#%%
import numpy as np
import pandas as pd
from time import sleep
from py5paisa import FivePaisaClient
from py5paisa.strategy import *
from cred import *
main_str="BANKNIFTY 02 SEP 2021 "
main_str_format = "BANKNIFTY 02 Sep 2021 "
main_str_pe = main_str+"PE "
main_str_ce = main_str+"CE "
main_str_format_pe=main_str_format+"PE "
main_str_format_ce=main_str_format+"CE "
expiry = "20210902"
expiry_format= expiry[:4]+'-'+expiry[4:6]+'-'+expiry[6:]
script=pd.read_csv('scripmaster-csv-format.csv')
cred={
            "APP_NAME":,
            "APP_SOURCE":,
            "USER_ID":,
            "PASSWORD":,
            "USER_KEY":,
            "ENCRYPTION_KEY":
        }
Client = FivePaisaClient(email='@gmail.com', passwd='password',dob='yyyymmdd', cred=cred)
Client.login()
#%%
req_list_=[{"Exch":"N","ExchType":"C","Symbol":"BANKNIFTY","Scripcode":"999920005","OptionType":"EQ"}]          
a=Client.fetch_market_feed(req_list_)
x=a['Data'][0]['LastRate']

#%%
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
PE_index_strikeprice=np.argmin(np.abs(np.array(live_PE_lastrate)-115))
CE_upper=req_list_CE_strikeprice[CE_index_strikeprice]
PE_lower=req_list_PE_strikeprice[PE_index_strikeprice]
strategy=strategies(user="@gmail.com", passw="PASSWORD", dob="YYYYMMDD",cred=cred)
strategy.iron_fly("NIFTY",["15000","15200"],"15100","75","20210610","I")