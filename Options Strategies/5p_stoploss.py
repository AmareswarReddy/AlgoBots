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
expiry = str(input('enter the current expiry(Eg: "20210916" ) : '))
lots = int(input('enter the amount of lots(Eg: 25) :'))
day=int(input('enter the no. of days ellapsed since strategy implimentation :'))
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
cred={
    "APP_NAME":"5P55115625",
    "APP_SOURCE":'8899',
    "USER_ID":"qZS8Qd5THYc",
    "PASSWORD":"O4X41D47h1g",
    "USER_KEY":"BDYHVFfDodmHw3RXeWzuc2acdOwczZ64",
    "ENCRYPTION_KEY":"jhxJH0k6BIUL6VnXYPIAcqTZLqYWhkLc"
    }
strategy=strategies(user="vinathi.bujji@gmail.com", passw="alliswell1@A", dob="19940830",cred=cred)
Client=FivePaisaClient(email='vinathi.bujji@gmail.com', passwd='alliswell1@A', dob='19940830',cred=cred)
Client.login()
#%%
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
'''
#%%
while True:
    req_list_=[{"Exch":"N","ExchType":"C","Symbol":"BANKNIFTY","Scripcode":"999920005","OptionType":"EQ"}]          
    a=strategy.fetch_market_feed(req_list_)
    x=a['Data'][0]['LastRate']
    bot=np.floor(x/100)*100
    top=np.ceil(x/100)*100
    while True:
        req_list_=[{"Exch":"N","ExchType":"C","Symbol":"BANKNIFTY","Scripcode":"999920005","OptionType":"EQ"}]          
        a=strategy.fetch_market_feed(req_list_)
        x=a['Data'][0]['LastRate']
        if x<bot:
            break
        if x>top:
            break
    control1=0
    control2=0
    req_list_=[{"Exch":"N","ExchType":"C","Symbol":"BANKNIFTY","Scripcode":"999920005","OptionType":"EQ"}]          
    a=strategy.fetch_market_feed(req_list_)
    x=a['Data'][0]['LastRate']
    req_list_PE={"Exch":"N","ExchType":"D","Symbol":main_str_pe+str(round(x/100)*100)+".00","Expiry":expiry,"StrikePrice":str(round(x/100)*100),"OptionType":"PE"}
    req_list_CE={"Exch":"N","ExchType":"D","Symbol":main_str_ce+str(round(x/100)*100)+".00","Expiry":expiry,"StrikePrice":str(round(x/100)*100),"OptionType":"CE"}
    req_list2=[req_list_CE,req_list_PE]
    req_list_PE_strikeprice=round(x/100)*100
    req_list_CE_strikeprice=round(x/100)*100
    strategy.short_strangle("banknifty",[str(req_list_CE_strikeprice),str(req_list_PE_strikeprice)],lots,expiry,'D',tag='alliswell')
    b=strategy.fetch_market_feed(req_list2)
    ce_lastrate=b['Data'][0]['LastRate']
    pe_lastrate=b['Data'][1]['LastRate']
    ce_lastrate_old=ce_lastrate
    ce_temp=ce_lastrate
    pe_lastrate_old=pe_lastrate
    pe_temp=pe_lastrate
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
            print('square off call option',ce_lastrate)
            strategy.square_off_ce('banknifty',[str(req_list_CE_strikeprice)],str(lots),expiry,'D',tag='noneiswell')
        if ce_lastrate<=ce_temp/2 and control1==0:
            control1=1
            print('square off call option',ce_lastrate)
            strategy.square_off_ce('banknifty',[str(req_list_CE_strikeprice)],str(lots),expiry,'D',tag='nothingiswell')

        if pe_lastrate<pe_lastrate_old and control2==0:
            Stop_loss2=pe_lastrate*1.2
            pe_lastrate_old=pe_lastrate
        if pe_lastrate>Stop_loss2 and control2==0:
            control2=1
            print('square off put option',pe_lastrate)
            strategy.square_off_pe('banknifty',[str(req_list_PE_strikeprice)],str(lots),expiry,'D',tag='eyd')
        if pe_lastrate<=pe_temp/2 and control2==0:
            control2=1
            print('square off put option',pe_lastrate)
            strategy.square_off_pe('banknifty',[str(req_list_PE_strikeprice)],str(lots),expiry,'D',tag='eter')

        if control1==1 and control2==1:
            break

# %%
