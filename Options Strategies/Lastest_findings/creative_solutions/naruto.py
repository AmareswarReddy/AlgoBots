# %%
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import json
import time
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


def is_expiry(week0):
    exchange = 'BANKNIFTY'
    expiry_timestamps = prime_client['login'].get_expiry(
        "N", exchange).copy()
    current_time = time.time()
    week0time_stamp = int(
        expiry_timestamps['Expiry'][week0]['ExpiryDate'][6:16])
    if week0time_stamp-current_time < 55800:
        return 1
    else:
        return 0


def initial_trades(week0, week1, max_lots):
    option_chain_week1, x = data(week1)
    option_chain_week0, x = data(week0)
    exclusive_strike = int(np.round(x/100)*100)
    pe_data = option_chain_week1[option_chain_week1['CPType'] == 'PE']
    p_sumS = float(pe_data[pe_data['StrikeRate'] ==
                   exclusive_strike]['LastRate'])
    pe_data = option_chain_week0[option_chain_week0['CPType'] == 'PE']
    p_sumB = float(pe_data[pe_data['StrikeRate'] ==
                           exclusive_strike]['LastRate'])
    order_button(exclusive_strike, 'PE_B', max_lots, week0)
    order_button(exclusive_strike, 'PE_S', max_lots, week1)
    return p_sumS, p_sumB

# orders_tracker={'exclusive_strike':43000,'sold_strikes':[43100,43200,43300]}


def double_edge(week0, week1):
    option_chain0, x = data(week0)
    option_chain1, x = data(week1)
    exclusive_strike = int(np.round(x/100)*100)
    pe_data = option_chain0[option_chain0['CPType'] == 'PE']
    ce_data = option_chain0[option_chain0['CPType'] == 'CE']
    p_sum0 = float(pe_data[pe_data['StrikeRate'] == exclusive_strike]['LastRate']) + \
        float(ce_data[ce_data['StrikeRate'] == exclusive_strike]['LastRate'])

    pe_data = option_chain1[option_chain1['CPType'] == 'PE']
    ce_data = option_chain1[option_chain1['CPType'] == 'CE']
    p_sum1 = float(pe_data[pe_data['StrikeRate'] == exclusive_strike]['LastRate']) + \
        float(ce_data[ce_data['StrikeRate'] == exclusive_strike]['LastRate'])

    exchange = 'BANKNIFTY'
    expiry_timestamps = prime_client['login'].get_expiry(
        "N", exchange).copy()
    current_time = time.time()
    week0time_stamp = int(
        expiry_timestamps['Expiry'][week0]['ExpiryDate'][6:16])
    week1time_stamp = int(
        expiry_timestamps['Expiry'][week1]['ExpiryDate'][6:16])
    proportion = (week0time_stamp-current_time) / \
        (week1time_stamp-current_time-172800)
    proportion2 = (week0time_stamp-current_time) / \
        (week1time_stamp-current_time)
    if (p_sum0/p_sum1) > proportion:
        return ['sasuke', (p_sum0/p_sum1)/proportion]
    elif (p_sum0/p_sum1) < proportion2:
        return ['naruto', (p_sum0/p_sum1)/proportion2]
    else:
        ['unknown', (p_sum0/p_sum1)/proportion]


def strategy(orders_tracker):
    exclusive_strike = orders_tracker['exclusive_strike']
    max_lots = orders_tracker['max_lots']
    original_max_lots = orders_tracker['original_max_lots']
    p_sumB = orders_tracker['p_sumB']
    p_sumS = orders_tracker['p_sumS']
    week0 = orders_tracker['week0']
    week1 = orders_tracker['week1']

    option_chain_week1, x = data(week1)
    option_chain_week0, x = data(week0)
    exclusive_strike = int(np.round(x/100)*100)
    pe_data = option_chain_week1[option_chain_week1['CPType'] == 'PE']
    p_sumS_C = float(pe_data[pe_data['StrikeRate'] ==
                             exclusive_strike]['LastRate'])
    pe_data = option_chain_week0[option_chain_week0['CPType'] == 'PE']
    p_sumB_C = float(pe_data[pe_data['StrikeRate'] ==
                             exclusive_strike]['LastRate'])
    net_profit = p_sumS+p_sumB_C-p_sumB-p_sumS_C
    at_strike = int(np.round(x/100)*100)
    if net_profit > 0 and abs(x-exclusive_strike) > p_sumS+p_sumB:
        order_button(exclusive_strike, 'PE_B', max_lots, week1)
        order_button(exclusive_strike, 'PE_S', max_lots, week0)
        order_button(at_strike, 'PE_B', original_max_lots, week0)
        order_button(at_strike, 'PE_S', original_max_lots, week1)
        orders_tracker['exclusive_strike'] = at_strike
        orders_tracker['p_sumB'] = p_sumB_C
        orders_tracker['p_sumS'] = p_sumS_C
    elif net_profit/(p_sumS-p_sumB) < -0.3 and at_strike == exclusive_strike:
        order_button(exclusive_strike, 'PE_B', max_lots, week0)
        order_button(exclusive_strike, 'PE_S', max_lots, week1)
        orders_tracker['max_lots'] = max_lots*2
        orders_tracker['p_sumS'] = (p_sumS_C+p_sumS)/2
        orders_tracker['p_sumB'] = (p_sumB_C+p_sumB)/2
    return orders_tracker


# %%
client_name = input('enter the client name: ')
start = int(input('enter 0 if starting the strategy for the first time'))
prime_client = client_login(client=client_name)

if start == 0:
    max_lots = int(input('max lots : '))
    week0 = int(input('enter the buying week'))
    week1 = int(input('enter the selling week'))
    ind_time = datetime.now(timezone("Asia/Kolkata")
                            ).strftime('%Y-%m-%d %H:%M:%S.%f')
    while int(ind_time[11:13])*60+int(ind_time[14:16]) < 556 or int(ind_time[11:13])*60+int(ind_time[14:16]) > 1085:
        ind_time = datetime.now(timezone("Asia/Kolkata")
                                ).strftime('%Y-%m-%d %H:%M:%S.%f')
    option_chain, x = data(week0)
    exclusive_strike = int(np.round(x/100)*100)
    trigger = double_edge(week0, week1)[0]
    if trigger == 'naruto':
        p_sumS, p_sumB = initial_trades(
            week0, week1, max_lots)

    orders_tracker = {'exclusive_strike': exclusive_strike, 'original_max_lots': max_lots,
                      'max_lots': max_lots,  'week0': week0, 'week1': week1, 'p_sumS': p_sumS, 'p_sumB': p_sumB}
else:
    orders_tracker = json.load(open(client_name+'_positions.json'))
    ind_time = datetime.now(timezone("Asia/Kolkata")
                            ).strftime('%Y-%m-%d %H:%M:%S.%f')
    while int(ind_time[11:13])*60+int(ind_time[14:16]) < 556 or int(ind_time[11:13])*60+int(ind_time[14:16]) > 1085:
        ind_time = datetime.now(timezone("Asia/Kolkata")
                                ).strftime('%Y-%m-%d %H:%M:%S.%f')


while int(ind_time[11:13])*60+int(ind_time[14:16]) < 931 and trigger == 'naruto':
    ind_time = datetime.now(timezone("Asia/Kolkata")
                            ).strftime('%Y-%m-%d %H:%M:%S.%f')
    orders_tracker = strategy(orders_tracker)


out_file = open(client_name+'_positions.json', "w")
json.dump(orders_tracker, out_file, indent=6)
out_file.close()

# %%
