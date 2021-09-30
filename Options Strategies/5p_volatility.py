#%%
import numpy as np
import pandas as pd
from time import sleep, strftime
from py5paisa import FivePaisaClient
from py5paisa.strategy import *
from cred import *
from datetime import datetime,date
from py_vollib.black_scholes import implied_volatility
main_str="BANKNIFTY 30 SEP 2021 "
main_str_format = "BANKNIFTY 30 Sep 2021 "
main_str_pe = main_str+"PE "
main_str_ce = main_str+"CE "
main_str_format_pe=main_str_format+"PE "
main_str_format_ce=main_str_format+"CE "
money_in_account = 0    #float(input('enter the amount of money in the account in lakhs(Eg: 2) :'))
lots = int(np.floor(money_in_account/1.65)*25)
expiry = "20210930"
expiry_format= expiry[:4]+'-'+expiry[4:6]+'-'+expiry[6:]
day=0 #int(input('enter the no. of days ellapsed since strategy implimentation :'))
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
for j in range(0,49):
    live_PE_lastrate=live_PE_lastrate+[live_PE['Data'][j]['LastRate']]
    live_CE_lastrate = live_CE_lastrate+[live_CE['Data'][j]['LastRate']]

# %%
def volatility(holidays,expiry,price,S,K,flag):
    r = 0
    today=str(datetime.today()).split()[0]
    t_day=date(int(today[:4]),int(today[5:7]),int(today[8:10]))
    e_day = date(int(expiry[:4]),int(expiry[4:6]),int(expiry[6:8]))
    days_left=e_day-t_day
    try: 
        awesome=int(str(days_left).split()[0])
    except Exception :
        awesome=0
    T_zero=(awesome-holidays)*6.25
    now=datetime.now()
    time=now.strftime('%H %M')
    var=15-int(time.split()[0])+(30-int(time.split()[1]))/60
    if var>0 and var<=6.5:
        T_one= var
    elif 15-int(time.split()[0])>6.5:
        T_one=6.5
    else :
        T_one = 0
    t=(T_one+T_zero)/(261*6.25)
    iv = implied_volatility.implied_volatility(price=price, S=S, K=K, t=t, r=r, flag=flag)
    return iv*100
#%%
live_PE_volatility=[]
live_CE_volatility=[]
for j in range(0,49):
    try:
        live_PE_volatility = live_PE_volatility+[volatility(holidays=0,expiry=expiry,price=live_PE_lastrate[j],S=x,K=req_list_PE_strikeprice[j], flag='p')]
    except Exception:
        live_PE_volatility = live_PE_volatility+[0]
    try:
        live_CE_volatility = live_CE_volatility+[volatility(holidays=0,expiry=expiry,price=live_CE_lastrate[j],S=x,K=req_list_CE_strikeprice[j], flag='c')]
    except Exception:
        live_CE_volatility = live_CE_volatility+[0]
#%%
summary_c = np.concatenate((np.reshape(req_list_CE_strikeprice,(len(live_CE_lastrate),1)),np.reshape(live_CE_lastrate,(len(live_CE_lastrate),1)), np.reshape(live_CE_volatility,(len(live_CE_lastrate),1))),axis=1)
summary_p = np.concatenate((np.reshape(req_list_PE_strikeprice,(len(live_PE_lastrate),1)),np.reshape(live_PE_lastrate,(len(live_PE_lastrate),1)), np.reshape(live_PE_volatility,(len(live_PE_lastrate),1))),axis=1)
call_data = np.reshape(summary_c,(1,np.shape(summary_c)[0],np.shape(summary_c)[1]))
put_data = np.reshape(summary_p,(1,np.shape(summary_p)[0],np.shape(summary_p)[1]))
# %%
while True:
    sleep(5)
    live_PE=Client.fetch_market_feed(req_list_PE)
    live_CE = Client.fetch_market_feed(req_list_CE)
    live_PE_lastrate=[]
    live_CE_lastrate=[]
    for j in range(0,49):
        live_PE_lastrate=live_PE_lastrate+[live_PE['Data'][j]['LastRate']]
        live_CE_lastrate = live_CE_lastrate+[live_CE['Data'][j]['LastRate']]
    live_PE_volatility=[]
    live_CE_volatility=[]
    for j in range(0,49):
        try:
            live_PE_volatility = live_PE_volatility+[volatility(holidays=1,expiry=expiry,price=live_PE_lastrate[j],S=x,K=req_list_PE_strikeprice[j], flag='p')]
        except Exception:
            live_PE_volatility = live_PE_volatility+[0]
        try:
            live_CE_volatility = live_CE_volatility+[volatility(holidays=1,expiry=expiry,price=live_CE_lastrate[j],S=x,K=req_list_CE_strikeprice[j], flag='c')]
        except Exception:
            live_CE_volatility = live_CE_volatility+[0]
    summary_c = np.concatenate((np.reshape(req_list_CE_strikeprice,(len(live_CE_lastrate),1)),np.reshape(live_CE_lastrate,(len(live_CE_lastrate),1)), np.reshape(live_CE_volatility,(len(live_CE_lastrate),1))),axis=1)
    summary_c=np.reshape(summary_c,(1,np.shape(summary_c)[0],np.shape(summary_c)[1]))
    summary_p = np.concatenate((np.reshape(req_list_PE_strikeprice,(len(live_PE_lastrate),1)),np.reshape(live_PE_lastrate,(len(live_PE_lastrate),1)), np.reshape(live_PE_volatility,(len(live_PE_lastrate),1))),axis=1)
    summary_p=np.reshape(summary_p,(1,np.shape(summary_p)[0],np.shape(summary_p)[1]))
    call_data=np.concatenate((call_data,summary_c),axis=0)
    put_data=np.concatenate((put_data,summary_p),axis=0)
    now=datetime.now()
    


# %%
