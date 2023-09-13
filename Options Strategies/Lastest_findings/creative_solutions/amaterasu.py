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
    if "S" in type:
        type = type[:-1]+"B"
    elif "B" in type:
        type = type[:-1]+"S"
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


def options_vwap_json(option_chain, calloptions_vwap, putoptions_vwap, primary_oi, x, prev_final_c_shape, prev_final_p_shape):
    stoploss = 30
    ce_data = option_chain[option_chain['CPType'] == 'CE']
    pe_data = option_chain[option_chain['CPType'] == 'PE']
    ce_data_prime = primary_oi[primary_oi['CPType'] == 'CE']
    pe_data_prime = primary_oi[primary_oi['CPType'] == 'PE']
    a = json.load(open('Volume_indicator.json'))['volume_indicator']
    if a > 0:
        taken_c = np.multiply(
            (np.array(ce_data['StrikeRate']) > x-30), (np.array(ce_data['StrikeRate']) < x+400))
        taken_p = np.multiply(
            (np.array(pe_data['StrikeRate']) > x-100), (np.array(pe_data['StrikeRate']) < x+30))
    elif a < 0:
        taken_c = np.multiply(
            (np.array(ce_data['StrikeRate']) > x-30), (np.array(ce_data['StrikeRate']) < x+100))
        taken_p = np.multiply(
            (np.array(pe_data['StrikeRate']) > x-400), (np.array(pe_data['StrikeRate']) < x+30))
    elif a == 0:
        taken_c = np.multiply(
            (np.array(ce_data['StrikeRate']) > x-30), (np.array(ce_data['StrikeRate']) < x+200))
        taken_p = np.multiply(
            (np.array(pe_data['StrikeRate']) > x-200), (np.array(pe_data['StrikeRate']) < x+30))

    ind_time = datetime.now(timezone("Asia/Kolkata")
                            ).strftime('%Y-%m-%d %H:%M:%S.%f')
    t = (int(ind_time[11:13])*60+int(ind_time[14:16])-555)/15
    c_lastrate = np.array(ce_data['LastRate'])+t
    p_lastrate = np.array(pe_data['LastRate'])+t
    c_volumes = np.array(ce_data['Volume'])
    p_volumes = np.array(pe_data['Volume'])
    c_oi = np.array(ce_data['OpenInterest'])
    p_oi = np.array(pe_data['OpenInterest'])
    prev_c_lastrate = np.array(calloptions_vwap['LastRate'])
    prev_p_lastrate = np.array(putoptions_vwap['LastRate'])
    prev_c_volumes = np.array(calloptions_vwap['Volume'])
    prev_p_volumes = np.array(putoptions_vwap['Volume'])
    primary_c_oi = np.array(ce_data_prime['OpenInterest'])
    primary_p_oi = np.array(pe_data_prime['OpenInterest'])
    c_shape = np.multiply((c_oi-primary_c_oi) > 0, taken_c)
    p_shape = np.multiply((p_oi-primary_p_oi) > 0, taken_p)
    c_net = np.multiply(c_volumes-prev_c_volumes, c_lastrate)
    p_net = np.multiply(p_volumes-prev_p_volumes, p_lastrate)
    c_volumes[c_volumes == 0] = 1
    p_volumes[p_volumes == 0] = 1
    call_vwap = np.multiply(
        (c_net+np.multiply(prev_c_lastrate, prev_c_volumes)), 1/c_volumes)
    put_vwap = np.multiply(
        (p_net+np.multiply(prev_p_lastrate, prev_p_volumes)), 1/p_volumes)
    calloptions_vwap = ce_data[['StrikeRate', 'LastRate', 'Volume']].copy()
    putoptions_vwap = pe_data[['StrikeRate', 'LastRate', 'Volume']].copy()
    calloptions_vwap['LastRate'] = call_vwap
    calloptions_vwap['Volume'] = ce_data['Volume']
    putoptions_vwap['LastRate'] = put_vwap
    putoptions_vwap['Volume'] = pe_data['Volume']
    final_c_shape = np.multiply(
        np.sign(((c_lastrate-call_vwap) < -stoploss)*-1), c_shape)
    final_p_shape = np.multiply(
        np.sign(((p_lastrate-put_vwap) < -stoploss)*-1), p_shape)
    to_correct_c_shape = np.multiply(
        np.sign(((c_lastrate-call_vwap) < 0)*-1), c_shape)
    to_correct_p_shape = np.multiply(
        np.sign(((p_lastrate-put_vwap) < 0)*-1), p_shape)
    if len(prev_final_p_shape) == 0:
        prev_final_c_shape = final_c_shape
        prev_final_p_shape = final_p_shape
    final_c_shape = final_c_shape - \
        np.multiply(to_correct_c_shape-final_c_shape, prev_final_c_shape)
    final_p_shape = final_p_shape - \
        np.multiply(to_correct_p_shape-final_p_shape, prev_final_p_shape)
    call_seller = ce_data[['StrikeRate']].copy()
    call_seller['indicator'] = final_c_shape
    put_seller = pe_data[['StrikeRate']].copy()
    put_seller['indicator'] = final_p_shape
    return calloptions_vwap, putoptions_vwap, put_seller, call_seller, final_c_shape, final_p_shape


def get_strike_from_scrip(scripcode, exchange):
    global week
    if exchange == 'BANKNIFTY':
        option_chain, a1 = data(week)
    k1 = option_chain[option_chain['ScripCode'] == scripcode]
    return int(k1['StrikeRate'])


def finalise_tron(p_strike, c_strike, tron):
    p_strike, p_yet_to_place = order_button(p_strike, 'PE_S', tron)
    c_strike, c_yet_to_place = order_button(c_strike, 'CE_S', tron)
    if p_yet_to_place == 0 and c_yet_to_place == 0:
        return tron
    if p_yet_to_place != 0 and c_yet_to_place == 0:
        while True:
            tron = tron-1
            order_button(c_strike, 'CE_B', 1)
            kkk, y_place = order_button(p_strike, 'PE_S', tron)
            if y_place == 0:
                break
        return tron
    if p_yet_to_place == 0 and c_yet_to_place != 0:
        while True:
            tron = tron-1
            order_button(p_strike, 'PE_B', 1)
            kkk, y_place = order_button(c_strike, 'CE_S', tron)
            if y_place == 0:
                break
        return tron
    if p_yet_to_place != 0 and c_yet_to_place != 0:
        return finalise_tron(p_strike=p_strike, c_strike=c_strike, tron=tron-1)


def initial_leg_trades(x, tron):
    exclusive_strike = int(np.round(x/100)*100)
    finalise_tron(c_strike=exclusive_strike+200,
                  p_strike=exclusive_strike-200, tron=tron)
    return exclusive_strike+200, exclusive_strike-200


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
        order_button(exclusive_strike, 'PE_S', tron)
        order_button(exclusive_strike, 'CE_S', tron)
        tron *= 2
        initial_premium_sum = (initial_premium_sum + premium_sum)/2
    if exclusive_strike != 0 and tron != 0:
        def exclusive_strike_change_signal(earlier_x, x):
            a = (x-earlier_x)/(initial_premium_sum)
            return abs(a)
        if exclusive_strike_change_signal(earlier_x=exclusive_strike, x=x) > 2 and premium_sum > initial_premium_sum+40:
            exclusive_strike, tron = exclusive_strike_change_trades(
                exclusive_strike, x, tron, initial_tron)
            initial_premium_sum = (float(ce_data[ce_data['StrikeRate'] == exclusive_strike]['LastRate']) +
                                   float(pe_data[pe_data['StrikeRate'] == exclusive_strike]['LastRate']))
    return exclusive_strike, tron, initial_premium_sum, total_decay


def initial_straddle_trades(exclusive_strike, tron):
    order_button(exclusive_strike, 'PE_S', tron)
    order_button(exclusive_strike, 'CE_S', tron)


def dismantle(exclusive_strike, tron):
    order_button(exclusive_strike, 'PE_B', tron)
    order_button(exclusive_strike, 'CE_B', tron)


# %%
client_name = input('enter the client name: ')
week = int(input('enter the week'))
hedge_tron = 0
tron = int(input('enter the range tron : '))
btron = int(tron*3)


initial_tron = btron

prime_client = client_login(client=client_name)
a = 0
option_chain, x = data(week)
exclusive_strike = int(np.round(x/100)*100)


if a == 4:
    main_cv, main_pv, c_oi, p_oi = 0, 0, 0, 0
else:
    indicator_json = json.load(open('indicator_variables.json'))
    main_cv, main_pv, c_oi, p_oi = indicator_json['main_cv'], indicator_json[
        'main_pv'], indicator_json['c_oi'], indicator_json['p_oi']


# start=int(input('enter 0 if starting the strategy for the first time, else 1 :  '))
# %%
ind_time = datetime.now(timezone("Asia/Kolkata")
                        ).strftime('%Y-%m-%d %H:%M:%S.%f')
while int(ind_time[11:13])*60+int(ind_time[14:16]) < 568:
    ind_time = datetime.now(timezone("Asia/Kolkata")
                            ).strftime('%Y-%m-%d %H:%M:%S.%f')

option_chain, x = data(week)
exclusive_strike = int(np.round(x/100)*100)
initial_straddle_trades(exclusive_strike, btron)
ce_data = option_chain[option_chain['CPType'] == 'CE']
pe_data = option_chain[option_chain['CPType'] == 'PE']
initial_premium_sum = (float(ce_data[ce_data['StrikeRate'] == exclusive_strike]['LastRate']) +
                       float(pe_data[pe_data['StrikeRate'] == exclusive_strike]['LastRate']))

primary_oi = option_chain
ce_data = option_chain[option_chain['CPType'] == 'CE']
pe_data = option_chain[option_chain['CPType'] == 'PE']
calloptions_vwap = ce_data[['StrikeRate', 'LastRate', 'Volume']].copy()
putoptions_vwap = pe_data[['StrikeRate', 'LastRate', 'Volume']].copy()
cv, pv, day_coi, day_poi = 0, 0, 0, 0
calloptions_vwap, putoptions_vwap, put_seller, call_seller, prev_final_c_shape, prev_final_p_shape = options_vwap_json(
    option_chain, calloptions_vwap, putoptions_vwap, primary_oi, x, [], [])
e_put_seller = put_seller['indicator']*0
e_call_seller = call_seller['indicator']*0
x_prime = x
ce_data = option_chain[option_chain['CPType'] == 'CE']
pe_data = option_chain[option_chain['CPType'] == 'PE']
earlier_pv = np.array(list(pe_data['Volume']))
earlier_cv = np.array(list(ce_data['Volume']))
cv, pv = 0, 0
start = 0
if a == 4:
    initial_c_strike, initial_p_strike = initial_leg_trades(x, hedge_tron)
    hedgetrades = 1
else:
    hedgetrades = 0
while int(ind_time[11:13])*60+int(ind_time[14:16]) < 922:
    ind_time = datetime.now(timezone("Asia/Kolkata")
                            ).strftime('%Y-%m-%d %H:%M:%S.%f')
    option_chain, x = data(week)
    # B,cv,pv,earlier_cv,earlier_pv,main_cv,main_pv,day_coi,day_poi,c_oi,p_oi=options_indicator(option_chain,x,cv,pv,earlier_cv,earlier_pv,main_cv,main_pv,day_coi,day_poi,c_oi,p_oi)
    # exclusive_strike,betatron,start,earlier_indicator=buy_kickoff(start,B,earlier_indicator,exclusive_strike,betatron)
    calloptions_vwap, putoptions_vwap, put_seller, call_seller, prev_final_c_shape, prev_final_p_shape = options_vwap_json(
        option_chain, calloptions_vwap, putoptions_vwap, primary_oi, x_prime, prev_final_c_shape, prev_final_p_shape)
    final_put_seller = np.array(put_seller['indicator']-e_put_seller)
    final_call_seller = np.array(call_seller['indicator']-e_call_seller)
    shine_c_strike = np.array(call_seller['StrikeRate'])
    shine_p_strike = np.array(put_seller['StrikeRate'])

    for i in range(len(final_call_seller)):
        if final_call_seller[i] < 0:
            a, b = order_button(shine_c_strike[i], 'CE_S', tron)
            c = 0
            while b != 0:
                c += 1
                sleep(5)
                a, b = order_button(shine_c_strike[i], 'CE_S', tron)
                if c > 5:
                    if b != 0:
                        final_call_seller[i] = 0
                    break
        elif final_call_seller[i] > 0:
            order_button(shine_c_strike[i], 'CE_B', tron)
    for i in range(len(final_put_seller)):
        if final_put_seller[i] < 0:
            a, b = order_button(shine_p_strike[i], 'PE_S', tron)
            c = 0
            while b != 0:
                c += 1
                sleep(5)
                a, b = order_button(shine_p_strike[i], 'PE_S', tron)
                if c > 5:
                    if b != 0:
                        final_put_seller[i] = 0
                    break
        elif final_put_seller[i] > 0:
            order_button(shine_p_strike[i], 'PE_B', tron)
    e_put_seller = put_seller['indicator']
    e_call_seller = call_seller['indicator']
    if abs(x_prime-x) > 99:
        x_prime = x
    exclusive_strike, btron, initial_premium_sum, total_decay = straddle_special_adjustment(
        exclusive_strike, x, btron, initial_tron, option_chain, initial_premium_sum)
    if int(ind_time[11:13])*60+int(ind_time[14:16]) > 900 and total_decay < 0:
        break
dismantle(exclusive_strike, btron)
