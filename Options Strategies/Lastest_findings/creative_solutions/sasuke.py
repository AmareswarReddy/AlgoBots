# %%
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
    f = open('credentials.json', "r")
    creds = json.loads(f.read())
    client_list = {}
    client_list[client] = {'strategy': {}, 'login': {}, 'lots': {}}
    vinathi_cred = creds[client]["keys"]
    user = creds[client]["user"]
    passw = creds[client]["passw"]
    dob = creds[client]["dob"]
    client_list[client]['strategy'] = strategies(
        user=user, passw=passw, dob=dob, cred=vinathi_cred)
    client_list[client]['login'] = FivePaisaClient(
        email=user, passwd=passw, dob=dob, cred=vinathi_cred)
    client_list[client]['login'].login()
    return client_list[client]
# client_name=input('enter the client name Eg: vinathi,bhaskar '


def order_button(exclusive_strike, type, lots, week):
    exchange = 'BANKNIFTY'
    lot_size = 15
    max_lots_per_order = 50
    strike_difference = 100
    if exclusive_strike == 0:
        while True:
            try:
                expiry_timestamps = prime_client['login'].get_expiry(
                    "N", exchange).copy()
                current_expiry_time_stamp_weekly = int(
                    expiry_timestamps['Expiry'][week]['ExpiryDate'][6:19])
                option_chain = pd.DataFrame(prime_client['login'].get_option_chain(
                    "N", exchange, current_expiry_time_stamp_weekly)['Options'])
                x = expiry_timestamps['lastrate'][0]['LTP']
                break
            except Exception:
                pass
        exclusive_strike = int(np.round(x/strike_difference)*strike_difference)
    else:
        while True:
            try:
                expiry_timestamps = prime_client['login'].get_expiry(
                    "N", exchange).copy()
                current_expiry_time_stamp_weekly = int(
                    expiry_timestamps['Expiry'][week]['ExpiryDate'][6:19])
                option_chain = pd.DataFrame(prime_client['login'].get_option_chain(
                    "N", exchange, current_expiry_time_stamp_weekly)['Options'])
                x = expiry_timestamps['lastrate'][0]['LTP']
                break
            except Exception:
                pass
    if type == 'CE_B':
        already_placed = 0
        c_data = option_chain[option_chain['CPType'] == 'CE']
        c_scrip = int(c_data[c_data['StrikeRate'] ==
                      exclusive_strike]['ScripCode'].iloc[0])
        temp2 = lots
        temp = int(temp2/max_lots_per_order)
        end = temp2-temp*max_lots_per_order
        test_order = Order(order_type='B', exchange='N', exchange_segment='D', scrip_code=c_scrip,
                           quantity=lot_size*max_lots_per_order, price=0, is_intraday=False, remote_order_id="tag")
        while temp > 0:
            status = prime_client['login'].place_order(test_order)
            temp = temp-1
            if status['Message'] == 'Success':
                already_placed += max_lots_per_order
        if temp == 0 and end != 0:
            test_order = Order(order_type='B', exchange='N', exchange_segment='D', scrip_code=c_scrip,
                               quantity=lot_size*end, price=0, is_intraday=False, remote_order_id="tag")
            status = prime_client['login'].place_order(test_order)
            if status['Message'] == 'Success':
                already_placed += end
        yet_to_place = lots-already_placed
    if type == 'PE_B':
        already_placed = 0
        p_data = option_chain[option_chain['CPType'] == 'PE']
        p_scrip = int(p_data[p_data['StrikeRate'] ==
                      exclusive_strike]['ScripCode'].iloc[0])
        temp2 = lots
        temp = int(temp2/max_lots_per_order)
        end = temp2-temp*max_lots_per_order
        test_order = Order(order_type='B', exchange='N', exchange_segment='D', scrip_code=p_scrip,
                           quantity=lot_size*max_lots_per_order, price=0, is_intraday=False, remote_order_id="tag")
        while temp > 0:
            status = prime_client['login'].place_order(test_order)
            temp = temp-1
            if status['Message'] == 'Success':
                already_placed += max_lots_per_order
        if temp == 0 and end != 0:
            test_order = Order(order_type='B', exchange='N', exchange_segment='D', scrip_code=p_scrip,
                               quantity=lot_size*end, price=0, is_intraday=False, remote_order_id="tag")
            status = prime_client['login'].place_order(test_order)
            if status['Message'] == 'Success':
                already_placed += end
        yet_to_place = lots-already_placed
    if type == 'CE_S':
        already_placed = 0
        c_data = option_chain[option_chain['CPType'] == 'CE']
        c_scrip = int(c_data[c_data['StrikeRate'] ==
                      exclusive_strike]['ScripCode'].iloc[0])
        temp2 = lots
        temp = int(temp2/max_lots_per_order)
        end = temp2-temp*max_lots_per_order
        test_order = Order(order_type='S', exchange='N', exchange_segment='D', scrip_code=c_scrip,
                           quantity=lot_size*max_lots_per_order, price=0, is_intraday=False, remote_order_id="tag")
        while temp > 0:
            status = prime_client['login'].place_order(test_order)
            temp = temp-1
            if status['Message'] == 'Success':
                already_placed += max_lots_per_order
        if temp == 0 and end != 0:
            test_order = Order(order_type='S', exchange='N', exchange_segment='D', scrip_code=c_scrip,
                               quantity=lot_size*end, price=0, is_intraday=False, remote_order_id="tag")
            status = prime_client['login'].place_order(test_order)
            if status['Message'] == 'Success':
                already_placed += end
        yet_to_place = lots-already_placed
    if type == 'PE_S':
        already_placed = 0
        p_data = option_chain[option_chain['CPType'] == 'PE']
        p_scrip = int(p_data[p_data['StrikeRate'] ==
                      exclusive_strike]['ScripCode'].iloc[0])
        temp2 = lots
        temp = int(temp2/max_lots_per_order)
        end = temp2-temp*max_lots_per_order
        test_order = Order(order_type='S', exchange='N', exchange_segment='D', scrip_code=p_scrip,
                           quantity=lot_size*max_lots_per_order, price=0, is_intraday=False, remote_order_id="tag")
        while temp > 0:
            status = prime_client['login'].place_order(test_order)
            temp = temp-1
            if status['Message'] == 'Success':
                already_placed += max_lots_per_order
        if temp == 0 and end != 0:
            test_order = Order(order_type='S', exchange='N', exchange_segment='D', scrip_code=p_scrip,
                               quantity=lot_size*end, price=0, is_intraday=False, remote_order_id="tag")
            status = prime_client['login'].place_order(test_order)
            if status['Message'] == 'Success':
                already_placed += end
        yet_to_place = lots-already_placed
    return exclusive_strike, yet_to_place

def data(week):
    exchange = 'BANKNIFTY'
    while True:
        try:
            expiry_timestamps = prime_client['login'].get_expiry(
                "N", exchange).copy()
            current_expiry_time_stamp_weekly = int(
                expiry_timestamps['Expiry'][week]['ExpiryDate'][6:19])
            option_chain = pd.DataFrame(prime_client['login'].get_option_chain(
                "N", exchange, current_expiry_time_stamp_weekly)['Options'])
            x = expiry_timestamps['lastrate'][0]['LTP']
            break
        except Exception:
            pass
    return option_chain, x

def initial_trades(week0,week1,exclusive_strike,max_lots):
    order_button(exclusive_strike,'PE_B',2*max_lots,week1)
    order_button(exclusive_strike,'CE_B',2*max_lots,week1)
    order_button(exclusive_strike,'PE_S',max_lots,week0)
    order_button(exclusive_strike,'CE_S',max_lots,week0)




#orders_tracker={'exclusive_strike':43000,'sold_strikes':[43100,43200,43300]}
def strategy(x, orders_tracker, max_lots, lots_per_strike, week):
    exclusive_strike=orders_tracker['exclusive_strike']
    length=len(orders_tracker['sold_strikes'])
    if length==0:
        if x>exclusive_strike+100:
            order_button(new_strike, 'CE_S', lots_per_strike, week)
            orders_tracker['sold_strikes']+=[new_strike]
        elif x<exclusive_strike-100:
            order_button(new_strike, 'PE_S', lots_per_strike, week)
            orders_tracker['sold_strikes']+=[new_strike]
    else:
        if x > max(orders_tracker['sold_strikes'])+100 and x>exclusive_strike and len(orders_tracker['sold_strikes'])*(lots_per_strike+1)<=max_lots :
            for i in range(0,length):
                if orders_tracker['sold_strikes'][i]<exclusive_strike:
                    order_button(orders_tracker['sold_strikes'][i], 'PE_B', lots_per_strike, week)
                    orders_tracker['sold_strikes'].remove(orders_tracker['sold_strikes'][i])

            new_strike=max(orders_tracker['sold_strikes'])+100
            order_button(new_strike, 'CE_S', lots_per_strike, week)
            orders_tracker['sold_strikes']+=[new_strike]

        if x < min(orders_tracker['sold_strikes'])-100 and x<exclusive_strike and len(orders_tracker['sold_strikes'])*(lots_per_strike+1)<=max_lots :
            for i in range(0,length):
                if orders_tracker['sold_strikes'][i]>exclusive_strike:
                    order_button(orders_tracker['sold_strikes'][i], 'CE_B', lots_per_strike, week)
                    orders_tracker['sold_strikes'].remove(orders_tracker['sold_strikes'][i])

            new_strike=min(orders_tracker['sold_strikes'])-100
            order_button(new_strike, 'PE_S', lots_per_strike, week)
            orders_tracker['sold_strikes']+=[new_strike]





# %%
client_name = input('enter the client name: ')
max_lots = int(input('max lots : '))
lots_per_strike=1
week0=int(input('enter the selling week'))
week1=int(input('enter the buying week'))
prime_client = client_login(client=client_name)
option_chain, x = data(0)
start=int(input('enter 0 if starting the strategy for the first time'))
if start==0:
    ind_time = datetime.now(timezone("Asia/Kolkata")
                            ).strftime('%Y-%m-%d %H:%M:%S.%f')
    while int(ind_time[11:13])*60+int(ind_time[14:16]) < 556 or int(ind_time[11:13])*60+int(ind_time[14:16]) > 1085:
        ind_time = datetime.now(timezone("Asia/Kolkata")
                                ).strftime('%Y-%m-%d %H:%M:%S.%f')
    exclusive_strike = int(np.round(x/100)*100)
    initial_trades(week0,week1,exclusive_strike,max_lots)
    orders_tracker={'exclusive_strike':exclusive_strike,'sold_strikes':[]}
else:
    orders_tracker=json.load(open(client_name+'_positions.json'))


while int(ind_time[11:13])*60+int(ind_time[14:16]) < 931:
    ind_time = datetime.now(timezone("Asia/Kolkata")
                            ).strftime('%Y-%m-%d %H:%M:%S.%f')
    option_chain, x = data(0)
    strategy(x,orders_tracker,max_lots,lots_per_strike,week0)

out_file = open(client_name+'_positions.json', "w")
json.dump(orders_tracker, out_file, indent = 6)
out_file.close()

# %%
