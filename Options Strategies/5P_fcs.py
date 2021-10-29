#%%
# Update scripmaster file every week
import numpy as np
import pandas as pd
from time import sleep, strftime
from py5paisa import FivePaisaClient
from py5paisa.strategy import *
from cred import *
from datetime import datetime 
from straddle import straddle
expiry = str(input('enter the expiry(Eg: "20210916" ) : '))
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
money_in_account = float(input('enter the amount of money in the account in lakhs(Eg: 2) :'))
lots = int(np.floor(money_in_account/1.65)*25)
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
# data candles are in days or 4hours
def start_fc(data):
    #get rsi from the data
    if rsi<35:
        a=True
    else :
        a=False
    return a
if day==0 and start_fc(data)==True:
    #buy fut and sell call  
while True:
    if live_price<breakeven and days_left_in_the_month>10:
        # change call option
        #update call strikeprice
    if live_price<breakeven and days_left_in_the_month<10:
        # squareoff current positions and take next month fut and call with call being at the same strike price
    if live_price>max_profit_price:
        #staircase adjustment
        #define min_profit_price and max_profit_price
        a=1
    if live_price<min_profit_price and a==1:
        #change the call towards live_price
    if can_exit(data)=='yes':
        #square off positions


        


