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
    client_list[client]['login'] = FivePaisaClient(cred=vinathi_cred)
    client_list[client]['login'].get_totp_session('', '', '')
    return client_list[client]
# client_name=input('enter the client name Eg: vinathi,bhaskar '


def order_button(exclusive_strike, type, lots, week):
    exchange = 'NIFTY'
    lot_size = 25
    max_lots_per_order = 20
    strike_difference = 50
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
    exchange = 'NIFTY'
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


def data(week):
    exchange = 'NIFTY'
    while True:
        try:
            expiry_timestamps = prime_client['login'].get_expiry(
                "N", exchange).copy()
            current_expiry_time_stamp_weekly = int(
                expiry_timestamps['Expiry'][week]['ExpiryDate'][6:19])
            option_chain = pd.DataFrame(prime_client['login'].get_option_chain(
                "N", exchange, current_expiry_time_stamp_weekly)['Options'])
            option_chain = option_chain[option_chain.StrikeRate % 50 == 0]
            ce_data = option_chain[option_chain['CPType'] == 'CE']
            pe_data = option_chain[option_chain['CPType'] == 'PE']
            a = 50
            strike = 0
            for i in ce_data['StrikeRate']:

                if abs(float(ce_data[ce_data['StrikeRate'] == i]['LastRate'])-float(pe_data[pe_data['StrikeRate'] == i]['LastRate'])) < a and float(ce_data[ce_data['StrikeRate'] == i]['LastRate']) > 5 and float(pe_data[pe_data['StrikeRate'] == i]['LastRate']) > 5:
                    a = float(ce_data[ce_data['StrikeRate'] == i]['LastRate']) - \
                        float(pe_data[pe_data['StrikeRate'] == i]['LastRate'])
                    strike = i
            x = strike+a
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


def initial_trades(week0, max_lots, decider):
    option_chain_week0, x = data(week0)
    exclusive_strike = int(np.round(x/100)*100)
    pe_data = option_chain_week0[option_chain_week0['CPType'] == 'PE']
    ce_data = option_chain_week0[option_chain_week0['CPType'] == 'CE']
    p_sumB = float(pe_data[pe_data['StrikeRate'] ==
                   exclusive_strike]['LastRate'])
    c_sumB = float(ce_data[ce_data['StrikeRate'] ==
                   exclusive_strike]['LastRate'])
    net_sum = p_sumB+c_sumB
    final_strike = exclusive_strike + \
        (decider > 0.5)*int(np.round(net_sum/100)*100)
    order_button(final_strike, 'PE_B', max_lots, week0)
    order_button(final_strike, 'CE_B', max_lots, week0)
    max_move = abs(exclusive_strike-final_strike)
    return final_strike, max_move


def strategy(orders_tracker, x):
    init_x = orders_tracker['init_x']
    final_strike = orders_tracker['final_strike']
    max_lots = orders_tracker['max_lots']
    week0 = orders_tracker['week0']
    max_move = orders_tracker['max_move']
    losses = orders_tracker['losses']
    if abs(init_x-x) > max_move:
        order_button(final_strike, 'PE_S', max_lots, week0)
        order_button(final_strike, 'CE_S', max_lots, week0)
        if final_strike != int(np.round(x/100)*100):
            orders_tracker = {'final_strike': 0,
                              'max_lots': max_lots,  'week0': week0, 'init_x': x, 'max_move': 0, 'losses': 0}
        else:
            orders_tracker = {'final_strike': 0,
                              'max_lots': max_lots,  'week0': week0, 'init_x': x, 'max_move': 0, 'losses': losses+1}
    return orders_tracker


def premium_decay(premium_sum):
    option_chain_week0, x = data(week0)
    exclusive_strike = int(np.round(x/100)*100)
    pe_data = option_chain_week0[option_chain_week0['CPType'] == 'PE']
    ce_data = option_chain_week0[option_chain_week0['CPType'] == 'CE']
    p_sumB = float(pe_data[pe_data['StrikeRate'] ==
                   exclusive_strike]['LastRate'])
    c_sumB = float(ce_data[ce_data['StrikeRate'] ==
                   exclusive_strike]['LastRate'])
    net_sum = p_sumB+c_sumB
    return premium_sum-net_sum


# %%
client_name = input('enter the client name: ')
prime_client = client_login(client=client_name)

max_lots = int(input('max lots : '))
week0 = int(input('enter the buying week'))
ind_time = datetime.now(timezone("Asia/Kolkata")
                        ).strftime('%Y-%m-%d %H:%M:%S.%f')
while int(ind_time[11:13])*60+int(ind_time[14:16]) < 600 or int(ind_time[11:13])*60+int(ind_time[14:16]) > 1085:
    ind_time = datetime.now(timezone("Asia/Kolkata")
                            ).strftime('%Y-%m-%d %H:%M:%S.%f')
# %%
option_chain, x = data(week0)
decider = np.random.rand()

# option_chain_week0, x = data(week0)
# exclusive_strike = int(np.round(x/100)*100)
# pe_data = option_chain_week0[option_chain_week0['CPType'] == 'PE']
# ce_data = option_chain_week0[option_chain_week0['CPType'] == 'CE']
# p_sumB = float(pe_data[pe_data['StrikeRate'] ==
#               exclusive_strike]['LastRate'])
# c_sumB = float(ce_data[ce_data['StrikeRate'] ==
#               exclusive_strike]['LastRate'])
# premium_sum = p_sumB+c_sumB
while True:
    option_chain_week0, x = data(week0)
    new_strike = int(np.round(x/100)*100)
    # if premium_decay(premium_sum) > 80 and new_strike == exclusive_strike:
    #    break
    break
final_strike, max_move = initial_trades(week0, max_lots, decider)
orders_tracker = {'final_strike': final_strike,
                  'max_lots': max_lots,  'week0': week0, 'init_x': x, 'max_move': max_move, 'losses': 0}

# %%
while int(ind_time[11:13])*60+int(ind_time[14:16]) < 899:
    ind_time = datetime.now(timezone("Asia/Kolkata")
                            ).strftime('%Y-%m-%d %H:%M:%S.%f')
    option_chain, x = data(week0)
    # x = int(input('x= '))
    orders_tracker = strategy(orders_tracker, x)
    if orders_tracker['final_strike'] == 0:
        decider = np.random.rand()
        losses = orders_tracker['losses']
        max_lots += losses
        final_strike, max_move = initial_trades(week0, max_lots, decider)
        orders_tracker['final_strike'] = final_strike
        orders_tracker['max_move'] = max_move
        orders_tracker['max_lots'] = max_lots

orders_tracker = strategy(orders_tracker, 0)

# %%
