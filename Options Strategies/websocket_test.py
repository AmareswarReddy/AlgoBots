#%%
import numpy as np
import pandas as pd
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
# %%
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
req_list=[
            { "Exch":"N","ExchType":"D","Scripcode":"51839"},

            ]


dict1=Client.Request_Feed('mf','s',req_list)
# %%

def on_message(ws,message):
            print("Hello Vinay")
            print(message)
Client.Streming_data(dict1, on_message)

# Note : Pass Dictionary in Parameter Field
# %%
