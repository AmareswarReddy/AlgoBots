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
def data(exchange):
    while True:
        try :
            expiry_timestamps=prime_client['login'].get_expiry("N",exchange).copy()
            option_chain=pd.DataFrame(prime_client['login'].get_option_chain("N",exchange,current_expiry_time_stamp_weekly)['Options'])
            x=expiry_timestamps['lastrate'][0]['LTP']
            break
        except Exception :
            pass
    return option_chain,x

def add_position(positions,strike,type,lots):
    positions[len(positions)]=[strike,type,lots]
    return positions

def y_axis(x,single_position,option_chain):
    if single_position[1]=='CE_B':
        k=x-single_position[0]
        k[k<0]=0
        lastrate=float(option_chain[(option_chain['StrikeRate']==single_position[0]) & (option_chain['CPType']=='CE')]['LastRate'])
        y=single_position[2]*(k-lastrate)

    if single_position[1]=='CE_S':
        k=single_position[0]-x
        k[k>0]=0
        lastrate=float(option_chain[(option_chain['StrikeRate']==single_position[0]) & (option_chain['CPType']=='CE')]['LastRate'])
        y=single_position[2]*(k+lastrate)

    if single_position[1]=='PE_B':
        k=single_position[0]-x
        k[k<0]=0
        lastrate=float(option_chain[(option_chain['StrikeRate']==single_position[0]) & (option_chain['CPType']=='PE')]['LastRate'])
        y=single_position[2]*(k-lastrate)
    if single_position[1]=='PE_S':
        k=x-single_position[0]
        k[k>0]=0
        lastrate=float(option_chain[(option_chain['StrikeRate']==single_position[0]) & (option_chain['CPType']=='PE')]['LastRate'])
        y=single_position[2]*(k+lastrate)
    return y

def pnl_graph(positions,option_chain,lastrate):
    try:
        k=pd.DataFrame(positions)
        a=np.array(k.iloc[0])
        x=np.linspace(min(a)-500,max(a)+500,int((max(a)-min(a)+1000)/100)+1)
        y1=np.zeros(len(x))
        for i in range(0,len(positions)):
            y1+=np.array(y_axis(x,positions[i],option_chain))  
    except Exception:
        x=[0]
        y1=[0]
    return x,y1


#%%
#variables to be initialised
client_name = 'rohit'
prime_client=client_login(client=client_name)
expiry_timestamps=prime_client['login'].get_expiry("N","BANKNIFTY").copy()
current_expiry_time_stamp_weekly=int(expiry_timestamps['Expiry'][0]['ExpiryDate'][6:19])
option_chain=pd.DataFrame(prime_client['login'].get_option_chain("N","BANKNIFTY",current_expiry_time_stamp_weekly)['Options'])
prev_x=expiry_timestamps['lastrate'][0]['LTP']
#%%
def get_strike_from_scrip(scripcode,exchange):
    option_chain,a1=data(exchange)
    k1=option_chain[option_chain['ScripCode']==scripcode]
    return int(k1['StrikeRate'])
while True:
    Noption_chain,Nx=data('NIFTY') 
    Boption_chain,Bx=data('BANKNIFTY') 
    S=pd.DataFrame(prime_client['login'].positions())
    nifty_positions={}
    banknifty_positions={}
    for i in range(0,len(S)):
        if ('NIFTY' in S['ScripName'].iloc[i]) and S['NetQty'].iloc[i]!=0:
            if S['NetQty'].iloc[i]<0 and ('PE' in S['ScripName'].iloc[i]):
                type_='PE_S'
            elif S['NetQty'].iloc[i]<0 and ('CE' in S['ScripName'].iloc[i]):
                type_='CE_S'
            elif S['NetQty'].iloc[i]>0 and ('CE' in S['ScripName'].iloc[i]):
                type_='CE_B'
            elif S['NetQty'].iloc[i]>0 and ('PE' in S['ScripName'].iloc[i]):
                type_='PE_B'
            nifty_positions=add_position(nifty_positions,get_strike_from_scrip(S['ScripCode'].iloc[i],'NIFTY'),type_,abs(S['NetQty'].iloc[i]))
        elif ('BANKNIFTY' in S['ScripName'].iloc[i]) and S['NetQty'].iloc[i]!=0:
            if S['NetQty'].iloc[i]<0 and ('PE' in S['ScripName'].iloc[i]):
                type_='PE_S'
            elif S['NetQty'].iloc[i]<0 and ('CE' in S['ScripName'].iloc[i]):
                type_='CE_S'
            elif S['NetQty'].iloc[i]>0 and ('CE' in S['ScripName'].iloc[i]):
                type_='CE_B'
            elif S['NetQty'].iloc[i]>0 and ('PE' in S['ScripName'].iloc[i]):
                type_='PE_B'
            banknifty_positions=add_position(banknifty_positions,get_strike_from_scrip(S['ScripCode'].iloc[i],'BANKNIFTY'),type_,abs(S['NetQty'].iloc[i]))
    x1,y1=pnl_graph(nifty_positions,Noption_chain,Nx)
    x2,y2=pnl_graph(banknifty_positions,Boption_chain,Bx)
    plt.plot(x1,y1)
    plt.show()
    plt.plot(x2,y2)
    plt.show()

# %%
