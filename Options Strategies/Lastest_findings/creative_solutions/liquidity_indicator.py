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


def order_button(exclusive_strike, type, lots):
    exchange = 'BANKNIFTY'
    lot_size = 15
    max_lots_per_order = 50
    strike_difference = 100
    global week
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


def exclusive_strike_change_trades(exclusive_strike, x, tron, initial_tron):
    order_button(exclusive_strike, 'PE_S', tron)
    order_button(exclusive_strike, 'CE_S', tron)
    exclusive_strike = int(np.round((x)/100)*100)
    order_button(exclusive_strike, 'PE_B', initial_tron)
    order_button(exclusive_strike, 'CE_B', initial_tron)
    return exclusive_strike, initial_tron


def straddle_special_adjustment(exclusive_strike, x, tron, initial_tron, option_chain, initial_premium_sum):
    ce_data = option_chain[option_chain['CPType'] == 'CE']
    pe_data = option_chain[option_chain['CPType'] == 'PE']
    atcl = float(ce_data[ce_data['StrikeRate'] ==
                 exclusive_strike]['LastRate'])
    atpl = float(pe_data[pe_data['StrikeRate'] ==
                 exclusive_strike]['LastRate'])
    premium_sum = atpl+atcl
    total_decay = initial_premium_sum-(premium_sum)
    if total_decay > 30 and abs(atcl-atpl) < 10:
        order_button(exclusive_strike, 'PE_B', tron)
        order_button(exclusive_strike, 'CE_B', tron)
        tron *= 2
        initial_premium_sum = (initial_premium_sum + premium_sum)/2
    if False:  # exclusive_strike != 0 and tron != 0:
        def exclusive_strike_change_signal(earlier_x, x):
            a = (x-earlier_x)/(initial_premium_sum)
            return abs(a)
        if exclusive_strike_change_signal(earlier_x=exclusive_strike, x=x) > 2 and premium_sum > initial_premium_sum+40:
            exclusive_strike, tron = exclusive_strike_change_trades(
                exclusive_strike, x, tron, initial_tron)
            initial_premium_sum = (float(ce_data[ce_data['StrikeRate'] == exclusive_strike]['LastRate']) +
                                   float(pe_data[pe_data['StrikeRate'] == exclusive_strike]['LastRate']))
    return exclusive_strike, tron, initial_premium_sum, total_decay, atcl > atpl


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


def initial_straddle_trades(exclusive_strike, tron):
    order_button(exclusive_strike, 'PE_B', tron)
    order_button(exclusive_strike, 'CE_B', tron)


def dismantle(exclusive_strike, tron):
    order_button(exclusive_strike, 'PE_S', tron)
    order_button(exclusive_strike, 'CE_S', tron)


# %%
client_name = input('enter the client name: ')
tron = int(input('enter the number of lots on each side: '))
initial_tron = tron
c_tron = tron
p_tron = tron
week = int(input('enter the week '))
prime_client = client_login(client=client_name)
option_chain, x = data(week)
exclusive_strike = int(np.round(x/100)*100)

start = int(input('enter 0 if starting the strategy for the first time else 1: '))
if start == 1:
    exclusive_strike = int(input('enter the exclusive strike: '))
    c_tron = int(input('enter the c_tron: '))
    p_tron = int(input('enter the p_tron: '))
    initial_premium_sum = float(input('initial_premium_sum: '))
ind_time = datetime.now(timezone("Asia/Kolkata")
                        ).strftime('%Y-%m-%d %H:%M:%S.%f')
while int(ind_time[11:13])*60+int(ind_time[14:16]) < 560 or int(ind_time[11:13])*60+int(ind_time[14:16]) > 1085:
    ind_time = datetime.now(timezone("Asia/Kolkata")
                            ).strftime('%Y-%m-%d %H:%M:%S.%f')
if start == 0:
    option_chain, x = data(week)
    exclusive_strike = int(np.round(x/100)*100)
    # initial_straddle_trades(exclusive_strike, tron)
    ce_data = option_chain[option_chain['CPType'] == 'CE']
    pe_data = option_chain[option_chain['CPType'] == 'PE']
    initial_premium_sum = (float(ce_data[ce_data['StrikeRate'] == exclusive_strike]['LastRate']) +
                           float(pe_data[pe_data['StrikeRate'] == exclusive_strike]['LastRate']))


while int(ind_time[11:13])*60+int(ind_time[14:16]) < 928:
    ind_time = datetime.now(timezone("Asia/Kolkata")
                            ).strftime('%Y-%m-%d %H:%M:%S.%f')
    option_chain, x = data(week)
    ce_data = option_chain[option_chain['CPType'] == 'CE']
    pe_data = option_chain[option_chain['CPType'] == 'PE']
    # exclusive_strike, tron, initial_premium_sum, total_decay, side = straddle_special_adjustment(exclusive_strike, x, tron, initial_tron, option_chain, initial_premium_sum)
    premium_sum = (float(ce_data[ce_data['StrikeRate'] == exclusive_strike]['LastRate']) +
                   float(pe_data[pe_data['StrikeRate'] == exclusive_strike]['LastRate']))
    if premium_sum > initial_premium_sum and int(ind_time[11:13])*60+int(ind_time[14:16]) > 595:
        break
initial_straddle_trades(exclusive_strike, tron)
ce_data = option_chain[option_chain['CPType'] == 'CE']
pe_data = option_chain[option_chain['CPType'] == 'PE']
initial_premium_sum = (float(ce_data[ce_data['StrikeRate'] == exclusive_strike]['LastRate']) +
                       float(pe_data[pe_data['StrikeRate'] == exclusive_strike]['LastRate']))
while int(ind_time[11:13])*60+int(ind_time[14:16]) < 928:
    ind_time = datetime.now(timezone("Asia/Kolkata")
                            ).strftime('%Y-%m-%d %H:%M:%S.%f')
    option_chain, x = data(week)
    ce_data = option_chain[option_chain['CPType'] == 'CE']
    pe_data = option_chain[option_chain['CPType'] == 'PE']
    exclusive_strike, tron, initial_premium_sum, total_decay, side = straddle_special_adjustment(
        exclusive_strike, x, tron, initial_tron, option_chain, initial_premium_sum)
    premium_sum = (float(ce_data[ce_data['StrikeRate'] == exclusive_strike]['LastRate']) +
                   float(pe_data[pe_data['StrikeRate'] == exclusive_strike]['LastRate']))

dismantle(exclusive_strike, tron)

# %%
