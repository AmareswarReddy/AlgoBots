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
            # if option_chain['Name'][0][10:12] == '22':
            #    print('yes')
            #    break
            # else:
            #    print(option_chain['Name'][0][10:12])
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


def initial_trades(week0, week1, exclusive_strike, max_lots):
    # exchange = 'BANKNIFTY'
    # expiry_timestamps = prime_client['login'].get_expiry(
    #    "N", exchange).copy()
    # current_time = time.time()
    # week0time_stamp = int(
    #    expiry_timestamps['Expiry'][week0]['ExpiryDate'][6:16])
    # week1time_stamp = int(
    #    expiry_timestamps['Expiry'][week1]['ExpiryDate'][6:16])
    # option_chain_week1, x = data(week1)
    # option_chain_week0, x = data(week0)
    # exclusive_strike = int(np.round(x/100)*100)
    # ce_data = option_chain_week1[option_chain_week1['CPType'] == 'CE']
    # pe_data = option_chain_week1[option_chain_week1['CPType'] == 'PE']
    # p_sum1 = float(ce_data[ce_data['StrikeRate'] == exclusive_strike]['LastRate']) + \
    #    float(pe_data[pe_data['StrikeRate'] == exclusive_strike]['LastRate'])
    # ce_data = option_chain_week0[option_chain_week0['CPType'] == 'CE']
    # pe_data = option_chain_week0[option_chain_week0['CPType'] == 'PE']
    # p_sum0 = float(ce_data[ce_data['StrikeRate'] == exclusive_strike]['LastRate']) + \
    #    float(pe_data[pe_data['StrikeRate'] == exclusive_strike]['LastRate'])
    # proportion = ((week0time_stamp-current_time) /
    #              (week1time_stamp-current_time))
    # week1lots = int(max_lots/(1-(proportion*p_sum1/p_sum0)))
    # week0lots = week1lots-max_lots
    expected_move_per_week = 1000
    week1lots = max_lots*2
    week0lots = max_lots
    order_button(exclusive_strike, 'PE_B', week1lots, week1)
    order_button(exclusive_strike, 'CE_B', week1lots, week1)
    order_button(exclusive_strike, 'PE_S', week0lots, week0)
    order_button(exclusive_strike, 'CE_S', week0lots, week0)
    lots_per_strike = max(1, int(max_lots/int(expected_move_per_week/100)))
    return lots_per_strike, week1lots, week0lots

# orders_tracker={'exclusive_strike':43000,'sold_strikes':[43100,43200,43300]}


def expiry_shift(x, Istrike, orders_tracker):
    week0 = orders_tracker['week0']
    week1 = orders_tracker['week1']
    week0lots = orders_tracker['week0lots']
    week1lots = orders_tracker['week1lots']
    max_lots = orders_tracker['max_lots']
    order_button(Istrike, 'PE_B', week0lots, week0)
    order_button(Istrike, 'CE_B', week0lots, week0)
    order_button(Istrike, 'PE_S', week1lots, week1)
    order_button(Istrike, 'CE_S', week1lots, week1)
    week0 += 1
    week1 += 1
    exclusive_strike = int(np.round(x/100)*100)+100
    lots_per_strike, week1lots, week0lots = initial_trades(
        week0, week1, exclusive_strike, max_lots)
    return week0, week1, lots_per_strike, week1lots, week0lots


def strategy(x, option_chain, orders_tracker, max_lots, lots_per_strike, week):
    exclusive_strike = orders_tracker['exclusive_strike']
    length = len(orders_tracker['sold_strikes'])
    ce_data = option_chain[option_chain['CPType'] == 'CE']
    pe_data = option_chain[option_chain['CPType'] == 'PE']
    at_strike = int(np.round(x/100)*100)
    lsm = (float(ce_data[ce_data['StrikeRate'] == at_strike]['LastRate']) +
           float(pe_data[pe_data['StrikeRate'] == at_strike]['LastRate']))
    if length == 0:
        if x > exclusive_strike+100:
            order_button(exclusive_strike+100, 'CE_S', lots_per_strike, week)
            orders_tracker['sold_strikes'] += [exclusive_strike+100]
        elif x < exclusive_strike-100:
            order_button(exclusive_strike-100, 'PE_S', lots_per_strike, week)
            orders_tracker['sold_strikes'] += [exclusive_strike-100]
    else:
        if x > max(orders_tracker['sold_strikes'])+100 and x > exclusive_strike:
            to_drop = []
            for i in range(0, length):
                if orders_tracker['sold_strikes'][i] < exclusive_strike:
                    order_button(
                        orders_tracker['sold_strikes'][i], 'PE_B', lots_per_strike, week)
                    to_drop += [(orders_tracker['sold_strikes'][i])]
            for i in to_drop:
                orders_tracker['sold_strikes'].remove(i)
            if (1+len(orders_tracker['sold_strikes']))*lots_per_strike <= max_lots and len(orders_tracker['sold_strikes']) != 0:
                new_strike = max(orders_tracker['sold_strikes'])+100
                order_button(new_strike, 'CE_S', lots_per_strike, week)
                orders_tracker['sold_strikes'] += [new_strike]

        elif x < min(orders_tracker['sold_strikes'])-100 and x < exclusive_strike:
            to_drop = []
            for i in range(0, length):
                if orders_tracker['sold_strikes'][i] > exclusive_strike:
                    order_button(
                        orders_tracker['sold_strikes'][i], 'CE_B', lots_per_strike, week)
                    to_drop += [(orders_tracker['sold_strikes'][i])]
            for i in to_drop:
                orders_tracker['sold_strikes'].remove(i)
            if (1+len(orders_tracker['sold_strikes']))*lots_per_strike <= max_lots and len(orders_tracker['sold_strikes']) != 0:
                new_strike = min(orders_tracker['sold_strikes'])-100
                order_button(new_strike, 'PE_S', lots_per_strike, week)
                orders_tracker['sold_strikes'] += [new_strike]
        else:
            to_drop = []
            for i in range(0, length):
                if orders_tracker['sold_strikes'][i] > exclusive_strike:
                    c_lastrate = float(
                        ce_data[ce_data['StrikeRate'] == orders_tracker['sold_strikes'][i]]['LastRate'])
                    if c_lastrate/lsm < 0.2:
                        order_button(
                            orders_tracker['sold_strikes'][i], 'CE_B', lots_per_strike, week)
                        to_drop += [(orders_tracker['sold_strikes'][i])]

                elif orders_tracker['sold_strikes'][i] < exclusive_strike:
                    p_lastrate = float(
                        pe_data[pe_data['StrikeRate'] == orders_tracker['sold_strikes'][i]]['LastRate'])
                    if p_lastrate/lsm < 0.2:
                        order_button(
                            orders_tracker['sold_strikes'][i], 'PE_B', lots_per_strike, week)
                        to_drop += [(orders_tracker['sold_strikes'][i])]
            for i in to_drop:
                orders_tracker['sold_strikes'].remove(i)
    return orders_tracker


# %%
client_name = input('enter the client name: ')
start = int(input('enter 0 if starting the strategy for the first time'))
prime_client = client_login(client=client_name)

if start == 0:
    max_lots = int(input('max lots : '))
    week0 = int(input('enter the selling week'))
    week1 = int(input('enter the buying week'))
    ind_time = datetime.now(timezone("Asia/Kolkata")
                            ).strftime('%Y-%m-%d %H:%M:%S.%f')
    while int(ind_time[11:13])*60+int(ind_time[14:16]) < 556 or int(ind_time[11:13])*60+int(ind_time[14:16]) > 1085:
        ind_time = datetime.now(timezone("Asia/Kolkata")
                                ).strftime('%Y-%m-%d %H:%M:%S.%f')
    option_chain, x = data(week0)
    exclusive_strike = int(np.round(x/100)*100)
    lots_per_strike, week1lots, week0lots = initial_trades(
        week0, week1, exclusive_strike, max_lots)
    orders_tracker = {'exclusive_strike': exclusive_strike, 'sold_strikes': [
    ], 'max_lots': max_lots, 'lots_per_strike': lots_per_strike, 'week0': week0, 'week1': week1, 'week0lots': week0lots, 'week1lots': week1lots}
else:
    orders_tracker = json.load(open(client_name+'_positions.json'))
    max_lots = orders_tracker['max_lots']
    lots_per_strike = orders_tracker['lots_per_strike']
    week0 = orders_tracker['week0']
    week1 = orders_tracker['week1']
    ind_time = datetime.now(timezone("Asia/Kolkata")
                            ).strftime('%Y-%m-%d %H:%M:%S.%f')
    while int(ind_time[11:13])*60+int(ind_time[14:16]) < 556 or int(ind_time[11:13])*60+int(ind_time[14:16]) > 1085:
        ind_time = datetime.now(timezone("Asia/Kolkata")
                                ).strftime('%Y-%m-%d %H:%M:%S.%f')


breaker = 0
while int(ind_time[11:13])*60+int(ind_time[14:16]) < 931:
    ind_time = datetime.now(timezone("Asia/Kolkata")
                            ).strftime('%Y-%m-%d %H:%M:%S.%f')
    option_chain, x = data(week0)
    orders_tracker = strategy(
        x, option_chain, orders_tracker, max_lots, lots_per_strike, week0)
    if is_expiry(week0) == 1 and int(ind_time[11:13])*60+int(ind_time[14:16]) > 901:
        if len(orders_tracker['sold_strikes']) == 0:
            Istrike = orders_tracker['exclusive_strike']
            week0, week1, lots_per_strike, week1lots, week0lots = expiry_shift(
                x, Istrike, week0, week1, week0lots, week1lots, max_lots)
            expiry_day = 0
        elif int(ind_time[11:13])*60+int(ind_time[14:16]) > 927:
            Istrike = orders_tracker['exclusive_strike']
            order_button(Istrike, 'PE_S', week1lots, week1)
            order_button(Istrike, 'CE_S', week1lots, week1)
            breaker = 1
    if breaker == 1:
        break


if week0 != 0 and breaker == 0:
    exchange = 'BANKNIFTY'
    expiry_timestamps = prime_client['login'].get_expiry(
        "N", exchange).copy()
    current_time = time.time()
    near_expiry_stamp = int(
        expiry_timestamps['Expiry'][0]['ExpiryDate'][6:16])
    if current_time-near_expiry_stamp > 0:
        orders_tracker['week0'] = week0-1
        orders_tracker['week1'] = week1-1
out_file = open(client_name+'_positions.json', "w")
json.dump(orders_tracker, out_file, indent=6)
out_file.close()

# %%
