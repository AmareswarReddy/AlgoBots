#%%
import numpy as np
import pandas as pd
from indicators import indicators
from time import sleep, strftime
from py5paisa import FivePaisaClient
from py5paisa.strategy import *
from datetime import datetime 
import requests
from pytz import timezone 
from cred import *
import os
#login
cred={
    "APP_NAME":"5P53784053",
    "APP_SOURCE":"8023",
    "USER_ID":"y4JUrjToSOR",
    "PASSWORD":"y0tc7unqQAV",
    "USER_KEY":"DrmeltLdZo82SKaxWJoeMALor1Xaiqk5",
    "ENCRYPTION_KEY":"ANb7Y0ouVD5iX0jcPGwPMIEyQnwPjxuI"
    }
Client = FivePaisaClient(email='chandinimadduru123@gmail.com', passwd='amar@0987',dob='19950820', cred=cred)
Client.login()
strategy=strategies(user="vinaykumar7295@gmail.com", passw="vinay1@A", dob="19700701",cred=cred)
#historical data

#historical_data(<Exchange>,<Exchange Type>,<Scrip Code>,<Time Frame>,<From Data>,<To Date>)

df=Client.historical_data('N','C',1660,'15m','2021-05-25','2021-06-16')
# Note : TimeFrame Should be from this list ['1m','5m','10m','15m','30m','60m','1d']
# %%
#get all the indicators in the data
data=indicators(df)

#%%
#Strategy begins
# Down Thrust(low spread high volume----uptrend on the way)
def low_spread_high_volume(data):
    a=np.abs(np.array(data['Open']-data['Close']))/np.abs(np.array(data['Volume']))
    data['multiplier'] = a
            

    # get the condition for doji
    



