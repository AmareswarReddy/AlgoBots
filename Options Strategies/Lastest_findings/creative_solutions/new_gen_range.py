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
import pickle
from pytz import timezone
# from cred import *
from py5paisa.order import Basket_order


class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return super(NpEncoder, self).default(obj)


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


def finalise_tron(p_strike, c_strike, tron):
    p_strike, p_yet_to_place = order_button(p_strike, 'PE_S', tron)
    c_strike, c_yet_to_place = order_button(c_strike, 'CE_S', tron)
    if p_yet_to_place == 0 and c_yet_to_place == 0:
        return tron
    if p_yet_to_place != 0 and c_yet_to_place == 0:
        while True:
            tron = tron-1
            p_yet_to_place -= 1
            order_button(c_strike, 'CE_B', 1)
            kkk, y_place = order_button(p_strike, 'PE_S', p_yet_to_place)
            if y_place == 0:
                break
        return tron
    if p_yet_to_place == 0 and c_yet_to_place != 0:
        while True:
            tron = tron-1
            c_yet_to_place -= 1
            order_button(p_strike, 'PE_B', 1)
            kkk, y_place = order_button(c_strike, 'CE_S', c_yet_to_place)
            if y_place == 0:
                break
        return tron
    if p_yet_to_place == tron and c_yet_to_place == tron:
        return finalise_tron(p_strike=p_strike, c_strike=c_strike, tron=tron-1)


def data(week):
    exchange = 'BANKNIFTY'
    while True:
        expiry_timestamps = prime_client['login'].get_expiry(
            "N", exchange).copy()
        current_expiry_time_stamp_weekly = int(
            expiry_timestamps['Expiry'][week]['ExpiryDate'][6:19])
        try:
            expiry_timestamps = prime_client['login'].get_expiry(
                "N", exchange).copy()
            option_chain = pd.DataFrame(prime_client['login'].get_option_chain(
                "N", exchange, current_expiry_time_stamp_weekly)['Options'])
            x = expiry_timestamps['lastrate'][0]['LTP']
            break
        except Exception:
            pass
    return option_chain, x


def strikes_decider(x, option_chain):
    exclusive_strike = int(np.round((x)/100)*100)
    ce_data = option_chain[(option_chain['CPType'] == 'CE') & (
        option_chain['StrikeRate'] >= exclusive_strike)]
    pe_data = option_chain[(option_chain['CPType'] == 'PE') & (
        option_chain['StrikeRate'] <= exclusive_strike)]
    if x % 100 > 85 or x % 100 < 15:
        p_factor = (max(pe_data['LastRate'])+50)/max(pe_data['LastRate'])
        c_factor = (max(ce_data['LastRate'])+50)/max(ce_data['LastRate'])
        plastrate_sort = np.array(pe_data['LastRate'])
        clastrate_sort = np.array(ce_data['LastRate'])
        pstrikes = np.array(pe_data['StrikeRate'])
        cstrikes = np.array(ce_data['StrikeRate'])
        if clastrate_sort[-1] > clastrate_sort[0]:
            clastrate_sort = clastrate_sort[::-1]
            cstrikes = cstrikes[::-1]
        if plastrate_sort[-1] > plastrate_sort[0]:
            plastrate_sort = plastrate_sort[::-1]
            pstrikes = pstrikes[::-1]
        final_p_strike_b = 0
        prev_fact = 0
        for i in range(0, 20):
            fact = (plastrate_sort[0]-plastrate_sort[i]
                    * 1.5)/(np.power(p_factor, i))
            if fact > prev_fact:
                final_p_strike_b = pstrikes[i]
                prev_fact = fact
                capital_to_deploy1 = 1/(np.power(p_factor, i))
        final_c_strike_b = 0
        prev_fact = 0
        for i in range(0, 20):
            fact = (clastrate_sort[0]-clastrate_sort[i]
                    * 1.5)/(np.power(c_factor, i))
            if fact > prev_fact:
                final_c_strike_b = cstrikes[i]
                prev_fact = fact
                capital_to_deploy2 = 1/(np.power(p_factor, i))
        capital_to_deploy = (capital_to_deploy1+capital_to_deploy2)/2
        return final_c_strike_b, final_p_strike_b, cstrikes[0], pstrikes[0], capital_to_deploy
    else:
        return 0, 0, 0, 0


def strikes_in_strategy(option_chain, exclusive_strike):
    ce_data = option_chain[(option_chain['CPType'] == 'CE') & (
        option_chain['StrikeRate'] > exclusive_strike)]
    pe_data = option_chain[(option_chain['CPType'] == 'PE') & (
        option_chain['StrikeRate'] < exclusive_strike)]
    p_factor = (max(pe_data['LastRate'])+50)/max(pe_data['LastRate'])
    c_factor = (max(ce_data['LastRate'])+50)/max(ce_data['LastRate'])
    plastrate_sort = np.array(pe_data['LastRate'])
    clastrate_sort = np.array(ce_data['LastRate'])
    pstrikes = np.array(pe_data['StrikeRate'])
    cstrikes = np.array(ce_data['StrikeRate'])
    if clastrate_sort[-1] > clastrate_sort[0]:
        clastrate_sort = clastrate_sort[::-1]
        cstrikes = cstrikes[::-1]
    if plastrate_sort[-1] > plastrate_sort[0]:
        plastrate_sort = plastrate_sort[::-1]
        pstrikes = pstrikes[::-1]
    final_p_strike_b = 0
    prev_fact = 0
    for i in range(0, 20):
        fact = (plastrate_sort[0]-plastrate_sort[i]
                * 1.5)/(np.power(p_factor, i))
        if fact > prev_fact:
            final_p_strike_b = pstrikes[i]
            prev_fact = fact
    final_c_strike_b = 0
    prev_fact = 0
    for i in range(0, 20):
        fact = (clastrate_sort[0]-clastrate_sort[i]
                * 1.5)/(np.power(c_factor, i))
        if fact > prev_fact:
            final_c_strike_b = cstrikes[i]
            prev_fact = fact
    return final_c_strike_b, final_p_strike_b, cstrikes[0], pstrikes[0]


def initial_leg_trades(x, option_chain):
    exclusive_strike = int(np.round((x)/100)*100)
    ce_data = option_chain[(option_chain['CPType'] == 'CE') & (
        option_chain['StrikeRate'] >= exclusive_strike)]
    pe_data = option_chain[(option_chain['CPType'] == 'PE') & (
        option_chain['StrikeRate'] <= exclusive_strike)]
    global max_lots_tracker
    p_strike_s = exclusive_strike
    c_strike_s = exclusive_strike
    c_lastrate = float(ce_data[ce_data['StrikeRate']
                       == exclusive_strike]['LastRate'])
    p_lastrate = float(pe_data[pe_data['StrikeRate']
                       == exclusive_strike]['LastRate'])
    p_strike_b = p_strike_s-100*(int((c_lastrate+p_lastrate)/100)+1)
    c_strike_b = c_strike_s+100*(int((c_lastrate+p_lastrate)/100)+1)
    c_strike = c_strike_b
    p_strike = p_strike_b
    c_lastrate_b = float(
        ce_data[ce_data['StrikeRate'] == c_strike_b]['LastRate'])
    p_lastrate_b = float(
        pe_data[pe_data['StrikeRate'] == p_strike_b]['LastRate'])

    ctron = 2*max_lots_tracker
    ptron = 2*max_lots_tracker
    k, y1 = order_button(p_strike, 'PE_B', ptron)
    p_buy_tron_json = ptron

    k, y1 = order_button(c_strike, 'CE_B', ctron)
    c_buy_tron_json = ctron

    final_tron = finalise_tron(
        c_strike=c_strike_s, p_strike=p_strike_s, tron=max_lots_tracker)
    if final_tron != max_lots_tracker:
        order_button(p_strike, 'PE_S', max_lots_tracker-final_tron)
        order_button(c_strike, 'CE_S', max_lots_tracker-final_tron)

    final_tron2 = finalise_tron(
        c_strike=2*c_strike_b-c_strike_s, p_strike=2*p_strike_b-p_strike_s, tron=max_lots_tracker)
    return final_tron, c_buy_tron_json, p_buy_tron_json, c_strike_s, p_strike_s, c_strike_b, p_strike_b, max_lots_tracker


def ranger(c_strike_s, p_strike_s, x, lots_tracker, ceb_strike, peb_strike):
    centre = (c_strike_s+p_strike_s)/2
    global lots_diff
    global initial_leg_buy_tron
    if peb_strike == 0:
        if x > centre+85:
            peb_strike = int(np.round(x/100)*100)
            order_button(peb_strike, 'PE_B', lots_tracker)

    if ceb_strike == 0:
        if x < centre-85:
            ceb_strike = int(np.round(x/100)*100)
            order_button(ceb_strike, 'CE_B', lots_tracker)

    if peb_strike != 0:
        if x > centre and x > peb_strike+85:
            order_button(peb_strike, 'PE_S', lots_tracker)
            lots_tracker *= 1.5
            lots_tracker = min(initial_leg_buy_tron, int(lots_tracker))
            order_button(peb_strike+100, 'PE_B', lots_tracker)

            peb_strike += 100

        if x < centre:
            order_button(peb_strike, 'PE_S', lots_tracker)
            lots_tracker = lots_diff
            peb_strike = 0

    if ceb_strike != 0:
        if x < centre and x < ceb_strike-85:
            order_button(ceb_strike, 'CE_S', lots_tracker)
            lots_tracker *= 1.5
            lots_tracker = min(initial_leg_buy_tron, int(lots_tracker))
            order_button(ceb_strike-100, 'CE_B', lots_tracker)
            ceb_strike -= 100

        if x > centre:
            order_button(ceb_strike, 'CE_S', lots_tracker)
            lots_tracker = lots_diff
            ceb_strike = 0

    return lots_tracker, ceb_strike, peb_strike


# %%
client_name = input('enter the client name: ')
prime_client = client_login(client=client_name)
week = int(input('enter the week: '))
option_chain, x = data(week)
start = int(
    input('enter 0 if starting the strategy for the first time, else 1 :  '))
from_json = input(
    'to take positions from existing positions json file (y/n): ')
if start == 0:
    ind_time = datetime.now(timezone("Asia/Kolkata")
                            ).strftime('%Y-%m-%d %H:%M:%S.%f')
    max_lots_tracker = int(input('enter the number of initial lots: '))

    while int(ind_time[11:13])*60+int(ind_time[14:16]) < 568:
        ind_time = datetime.now(timezone("Asia/Kolkata")
                                ).strftime('%Y-%m-%d %H:%M:%S.%f')
    option_chain, x = data(week)
    c_sell_tron, c_buy_tron_json, p_buy_tron_json, c_strike_s, p_strike_s, c_strike_b, p_strike_b, initial_leg_buy_tron = initial_leg_trades(
        x, option_chain)
    p_sell_tron, ceb_strike, peb_strike = c_sell_tron, 0, 0
    lots_diff = int(max_lots_tracker/4)
    lots_tracker = lots_diff

elif start == 1 and from_json == 'y':
    with open(client_name+'_ultimateshow_positions.pkl', 'rb') as f:
        positions_record = pickle.load(f)
    c_sell_tron = positions_record['show']['c_sell_tron']
    p_sell_tron = positions_record['show']['p_sell_tron']
    c_strike_b = positions_record['show']['c_strike_b']
    p_strike_b = positions_record['show']['p_strike_b']
    c_strike_s = positions_record['show']['c_strike_s']
    p_strike_s = positions_record['show']['p_strike_s']
    c_buy_tron_json = positions_record['show']['c_buy_tron']
    p_buy_tron_json = positions_record['show']['p_buy_tron']
    ceb_strike = positions_record['ranger']['ceb_strike']
    peb_strike = positions_record['ranger']['peb_strike']
    lots_tracker = positions_record['ranger']['lots_tracker']
    lots_diff = positions_record['ranger']['lots_diff']

ind_time = datetime.now(timezone("Asia/Kolkata")
                        ).strftime('%Y-%m-%d %H:%M:%S.%f')
while int(ind_time[11:13])*60+int(ind_time[14:16]) < 556:
    ind_time = datetime.now(timezone("Asia/Kolkata")
                            ).strftime('%Y-%m-%d %H:%M:%S.%f')
# %%
while int(ind_time[11:13])*60+int(ind_time[14:16]) < 927:
    option_chain, x = data(week=week)
    # x=int(input('enter x'))
    sleep(1)
    ind_time = datetime.now(timezone("Asia/Kolkata")
                            ).strftime('%Y-%m-%d %H:%M:%S.%f')
    lots_tracker, ceb_strike, peb_strike = ranger(
        c_strike_s, p_strike_s, x, lots_tracker, ceb_strike, peb_strike)
positions_json = {'show': {'c_strike_b': c_strike_b, 'p_strike_b': p_strike_b, 'c_sell_tron': c_sell_tron, 'p_sell_tron': p_sell_tron, 'c_strike_s': c_strike_s, 'p_strike_s': p_strike_s,
                           'c_buy_tron': c_buy_tron_json, 'p_buy_tron': p_buy_tron_json}, 'ranger': {'ceb_strike': ceb_strike, 'peb_strike': peb_strike, 'lots_tracker': lots_tracker, 'lots_diff': lots_diff}}

print(positions_json)
with open(client_name+'_ultimateshow_positions.pkl', "wb") as f:
    pickle.dump(positions_json, f)
