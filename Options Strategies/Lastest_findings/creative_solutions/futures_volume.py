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
from py5paisa.order import Basket_order
from pyswarm import pso
from itertools import permutations
def client_login(client):
    import json
    f = open ('credentials.json', "r")
    creds = json.loads(f.read())
    client_list={}
    client_list[client]={'strategy':{},'login':{},'lots':{}}
    vinathi_cred = creds[client]["keys"]
    user = creds[client]["user"]
    passw = creds[client]["passw"]
    dob = creds[client]["dob"]
    client_list[client]['strategy']=0
    client_list[client]['login']=FivePaisaClient(email=user, passwd=passw, dob=dob,cred=vinathi_cred)
    client_list[client]['login'].login()
    client_list[client]['lots']=round((client_list[client]['login'].margin()[0]['AvailableMargin']-200000)/180000)
    return client_list[client]


client_name   = 'bhaskar'


prime_client=client_login(client=client_name)

req_list_=[{"Exch":"N","ExchType":"D","Symbol":"NIFTY 25 Aug 2022","Scripcode":"82222"}]          
a=prime_client['login'].fetch_market_feed(req_list_)
x=a['Data'][0]['LastRate']

df=prime_client['login'].historical_data('N','D',82221,'5m','2022-08-10','2022-08-25')
# %%
