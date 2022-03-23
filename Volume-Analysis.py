#%%
import numpy as np
import pandas as pd
import json
from time import sleep, strftime
from py5paisa import FivePaisaClient
from py5paisa.strategy import strategies
from py5paisa.logging import log_response
from datetime import datetime 
from datetime import date
import requests
from pytz import timezone 
from cred import *
import os

cred={
    "APP_NAME":"5P56936208",
    "APP_SOURCE":"2179",
    "USER_ID":"w6MJ1dw5Yd0",
    "PASSWORD":"V7JkGTUudjt",
    "USER_KEY":"8Q4SSCEo0bOgroVMFcNB0nTTB6CGPQuE",
    "ENCRYPTION_KEY":"zeoxSiZ1pbQsOJ2vaMlOllCeJwNzRQeFlcjc0WGYyl5nLzoCRtWZI5Z2xwChp6Ip"
        }
Client = FivePaisaClient(email='vinaykumar7295@gmail.com', passwd='vinay1@A',dob='19700701', cred=cred)
Client.login()

#%%
#historical_data(exchange,exchange type,scrip code,time frame,from data,to date)
from datetime import datetime, timedelta

currentdate = datetime.today().strftime('%Y-%m-%d')
startdate = datetime.today() - timedelta(days=40)
df=Client.historical_data('N','C',1660,'1d',startdate.strftime('%Y-%m-%d'),currentdate)
print(df)

# Note : TimeFrame Should be from this list ['1m','5m','10m','15m','30m','60m','1d']
# %%
df20 = df.iloc[:-20]
print(df20)
#def get20Average(volumes):

# %%

# %%
