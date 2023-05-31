#%%
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
    client_list[client]['strategy']=strategies(user=user, passw=passw, dob=dob,cred=vinathi_cred)
    client_list[client]['login']=FivePaisaClient(email=user, passwd=passw, dob=dob,cred=vinathi_cred)
    client_list[client]['login'].login()
    client_list[client]['lots']=round((client_list[client]['login'].margin()[0]['AvailableMargin']-200000)/180000)
    return client_list[client]
#client_name=input('enter the client name Eg: vinathi,bhaskar ')
import sys
client_name   = 'digambar'
prime_client=client_login(client=client_name)

#%%
from datetime import date, timedelta
import pandas as pd
import requests

#Read Scrip Master
url = "https://images.5paisa.com/website/scripmaster-csv-format.csv"
r = requests.get(url)
open('scripmaster-csv-format.csv', 'wb').write(r.content)
filename = 'scripmaster-csv-format.csv'
scrips = pd.read_csv(filename)

# %%

k=pd.read_csv('scripmaster-csv-format.csv')
root=list(k[(k.Root=='BANKNIFTY') & (k.CpType=='XX')]['Scripcode'])
req_list=[]
for i in root:
    req_list=req_list+[
                { "Exch":"N","ExchType":"D","ScripCode":int(i)},
                ]
req_data=prime_client['login'].Request_Feed('oi','s',req_list)
def on_message(ws, message):
    for k in root:
        df=prime_client['login'].historical_data('N','D',str(k),'1m','2022-08-19','2022-08-25')
    print(message)
    a=json.loads(message)
    print(a)

prime_client['login'].connect(req_data)
prime_client['login'].receive_data(on_message)

# %%
