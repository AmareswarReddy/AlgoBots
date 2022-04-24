#%%
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import json
from time import sleep, strftime
from py5paisa import FivePaisaClient
from py5paisa.strategy import *
from py5paisa.logging import log_response
from datetime import datetime 
from datetime import date
import requests
from pytz import timezone 
from cred import *
client='vinathi'

def client_login(client):
    client_list={}
    client_list[client]={'strategy':{},'login':{},'lots':{}}
    if client=='vinathi' :
        client_list[client]['lots']=int(input('lots for vinathi (Eg:3):'))
        vinathi_cred={
            "APP_NAME":"5P55115625",
            "APP_SOURCE":'8899',
            "USER_ID":"qZS8Qd5THYc",
            "PASSWORD":"O4X41D47h1g",
            "USER_KEY":"BDYHVFfDodmHw3RXeWzuc2acdOwczZ64",
            "ENCRYPTION_KEY":"jhxJH0k6BIUL6VnXYPIAcqTZLqYWhkLc"
            }
        client_list[client]['strategy']=strategies(user="vinathi.bujji@gmail.com", passw="kittu1@A", dob="19940830",cred=vinathi_cred)
        client_list[client]['login']=FivePaisaClient(email="vinathi.bujji@gmail.com", passwd="kittu1@A", dob="19940830",cred=vinathi_cred)
    elif client=='bhaskar':
        client_list[client]['lots']=int(input('lots for bhaskar (Eg:3):'))
        bhaskar_cred={
            "APP_NAME":"5P56936208",
            "APP_SOURCE":"2179",
            "USER_ID":"w6MJ1dw5Yd0",
            "PASSWORD":"V7JkGTUudjt",
            "USER_KEY":"8Q4SSCEo0bOgroVMFcNB0nTTB6CGPQuE",
            "ENCRYPTION_KEY":"HEgo6erh7qmqnDjRXIbaRTSNyfI6eofO"
            }
        client_list[client]['strategy']=strategies(user="vinaykumar7295@gmail.com", passw="kittu1@A", dob="19700701",cred=bhaskar_cred)
        client_list[client]['login']=FivePaisaClient(email='vinaykumar7295@gmail.com', passwd='kittu1@A', dob='19700701',cred=bhaskar_cred)
    
    else:
        print('client_name does not exist in the data')
        print('please choose one the following clients')
        print('vinathi')
        print('bhaskar')
    return client_list
prime_client=client_login(client)

# %%
