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
from scipy import interpolate
from pyswarm import pso


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
    # client_list[client]['lots']=round((client_list[client]['login'].margin()[0]['AvailableMargin']-200000)/180000)
    return client_list[client]
# client_name=input('enter the client name Eg: vinathi,bhaskar '


def order_button(exclusive_strike, type, lots):
    sleep(0.5)
    if "S" in type:
        type = type[:-1]+"B"
    elif "B" in type:
        type = type[:-1]+"S"
    exchange = 'BANKNIFTY'
    lot_size = 25
    max_lots_per_order = 36
    strike_difference = 100
    if exclusive_strike == 0:
        while True:
            try:
                expiry_timestamps = prime_client['login'].get_expiry(
                    "N", exchange).copy()
                current_expiry_time_stamp_weekly = int(
                    expiry_timestamps['Expiry'][0]['ExpiryDate'][6:19])
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
                    expiry_timestamps['Expiry'][0]['ExpiryDate'][6:19])
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
                      exclusive_strike]['ScripCode'])
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
            sleep(0.5)
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
                      exclusive_strike]['ScripCode'])
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
            sleep(0.5)
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
                      exclusive_strike]['ScripCode'])
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
            sleep(0.5)
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
                      exclusive_strike]['ScripCode'])
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
            sleep(0.5)
        if temp == 0 and end != 0:
            test_order = Order(order_type='S', exchange='N', exchange_segment='D', scrip_code=p_scrip,
                               quantity=lot_size*end, price=0, is_intraday=False, remote_order_id="tag")
            status = prime_client['login'].place_order(test_order)
            if status['Message'] == 'Success':
                already_placed += end
        yet_to_place = lots-already_placed
    return exclusive_strike, yet_to_place


def lots_drop(strike, side, yet_to_place):
    k = yet_to_place
    while yet_to_place > 0:
        sleep(1)
        yet_to_place -= 1
        xx, pending = order_button(strike, side, yet_to_place)
        if pending == 0:
            break
    return k-yet_to_place


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


def blue_factor(option_chain, x):
    final_chain = option_chain[(
        option_chain['StrikeRate'] > x-1000) & (option_chain['StrikeRate'] < x+1000)]
    p = final_chain[final_chain['CPType'] == 'PE']
    c = final_chain[final_chain['CPType'] == 'CE']
    strikes = p['StrikeRate']
    p_lastrates = p['LastRate']
    c_lastrates = c['LastRate']
    f_p = interpolate.interp1d(strikes, p_lastrates, kind='quadratic')
    f_c = interpolate.interp1d(strikes, c_lastrates, kind='quadratic')
    return (f_p(x)+f_c(x))/2


def get_strike_from_scrip(scripcode, exchange):
    if exchange == 'BANKNIFTY':
        option_chain, a1 = data(0)
    k1 = option_chain[option_chain['ScripCode'] == scripcode]
    return int(k1['StrikeRate'])


def finalise_tron(p_strike, c_strike, tron, to_take_c_strike, to_take_p_strike):
    if tron < 0:
        return 0
    if to_take_p_strike == 1:
        p_strike, p_yet_to_place = order_button(p_strike, 'PE_B', tron)
    else:
        p_yet_to_place = 0
    if to_take_c_strike == 1:
        c_strike, c_yet_to_place = order_button(c_strike, 'CE_B', tron)
    else:
        c_yet_to_place = 0
    if p_yet_to_place == 0 and c_yet_to_place == 0:
        return tron
    if p_yet_to_place != 0 and c_yet_to_place == 0:
        while True:
            tron = tron-1
            order_button(c_strike, 'CE_S', 1)
            kkk, y_place = order_button(p_strike, 'PE_B', tron)
            if y_place == 0:
                break
        return tron
    if p_yet_to_place == 0 and c_yet_to_place != 0:
        while True:
            tron = tron-1
            order_button(p_strike, 'PE_S', 1)
            kkk, y_place = order_button(c_strike, 'CE_B', tron)
            if y_place == 0:
                break
        return tron
    if p_yet_to_place != 0 and c_yet_to_place != 0:
        return finalise_tron(p_strike=p_strike, c_strike=c_strike, tron=tron-1, to_take_c_strike=to_take_c_strike, to_take_p_strike=to_take_p_strike)


def initialisation(x, tron):
    c_strike = int(np.round(x/100)*100)
    p_strike = c_strike
    order_button(p_strike, 'CE_S', tron)
    order_button(p_strike, 'PE_S', tron)
    return p_strike, c_strike


def counter_range(c_strike, p_strike, tron, x, option_chain):
    if x > p_strike+108 and tron != 0:
        a1 = int(option_chain[(option_chain['StrikeRate'] == p_strike) & (
            option_chain['CPType'] == 'PE')]['LastRate'])
        a2 = int(option_chain[(option_chain['StrikeRate'] == p_strike+100)
                 & (option_chain['CPType'] == 'PE')]['LastRate'])
        new_tron = int(tron*a1/a2)
        if new_tron != 0:
            order_button(p_strike, 'PE_B', tron)
            order_button(p_strike+100, 'PE_S', new_tron)
            order_button(c_strike, 'CE_B', tron-new_tron)
            p_strike += 100
            tron = new_tron
        if new_tron == 0:
            order_button(p_strike, 'PE_B', tron)
            # order_button(p_strike+100, 'PE_S', new_tron)
            order_button(c_strike, 'CE_B', tron-new_tron)
            p_strike += 100
            tron = new_tron

    if x < c_strike-108 and tron != 0:
        a1 = int(option_chain[(option_chain['StrikeRate'] == c_strike) & (
            option_chain['CPType'] == 'CE')]['LastRate'])
        a2 = int(option_chain[(option_chain['StrikeRate'] == c_strike-100)
                 & (option_chain['CPType'] == 'CE')]['LastRate'])
        new_tron = int(tron*a1/a2)
        if new_tron != 0:
            order_button(c_strike, 'CE_B', tron)
            order_button(c_strike-100, 'CE_S', new_tron)
            order_button(p_strike, 'PE_B', tron-new_tron)
            c_strike -= 100
            tron = new_tron
        if new_tron == 0:
            order_button(c_strike, 'CE_B', tron)
            # order_button(c_strike-100, 'CE_S', new_tron)
            order_button(p_strike, 'PE_B', tron-new_tron)
            c_strike -= 100
            tron = new_tron
            return c_strike, p_strike, tron


def dismantle(c_strike, p_strike, tron):
    order_button(c_strike, 'CE_B', tron)
    order_button(p_strike, 'PE_B', tron)


# %%
client_name = input('enter the client name: ')
tron = int(input('enter the number of lots at each strike'))
prime_client = client_login(client=client_name)
# %%
ind_time = datetime.now(timezone("Asia/Kolkata")
                        ).strftime('%Y-%m-%d %H:%M:%S.%f')
while int(ind_time[11:13])*60+int(ind_time[14:16]) < 556:
    ind_time = datetime.now(timezone("Asia/Kolkata")
                            ).strftime('%Y-%m-%d %H:%M:%S.%f')
option_chain, x = data(week=0)
p_strike, c_strike = initialisation(x, tron)
while int(ind_time[11:13])*60+int(ind_time[14:16]) < 916:
    ind_time = datetime.now(timezone("Asia/Kolkata")
                            ).strftime('%Y-%m-%d %H:%M:%S.%f')
    option_chain, x = data(week=0)
    c_strike, p_strike, tron = counter_range(
        c_strike, p_strike, tron, x, option_chain)
dismantle(c_strike, p_strike, tron)


# %%
