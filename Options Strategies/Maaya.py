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
    client_list[client]['login'] = FivePaisaClient(cred=vinathi_cred)
    client_list[client]['login'].get_totp_session(
        '56936208', '653249', '001273')
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
        while temp > 0:
            status = prime_client['login'].place_order(
                OrderType='B', Exchange='N', ExchangeType='D', ScripCode=c_scrip, Qty=lot_size*max_lots_per_order, Price=0)
            temp = temp-1
            if status['Message'] == 'Success':
                already_placed += max_lots_per_order
        if temp == 0 and end != 0:
            status = prime_client['login'].place_order(
                OrderType='B', Exchange='N', ExchangeType='D', ScripCode=c_scrip, Qty=lot_size*end, Price=0)
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
        while temp > 0:
            status = prime_client['login'].place_order(
                OrderType='B', Exchange='N', ExchangeType='D', ScripCode=p_scrip, Qty=lot_size*max_lots_per_order, Price=0)
            temp = temp-1
            if status['Message'] == 'Success':
                already_placed += max_lots_per_order
        if temp == 0 and end != 0:
            status = prime_client['login'].place_order(
                OrderType='B', Exchange='N', ExchangeType='D', ScripCode=p_scrip, Qty=lot_size*end, Price=0)
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
        while temp > 0:
            status = prime_client['login'].place_order(
                OrderType='S', Exchange='N', ExchangeType='D', ScripCode=c_scrip, Qty=lot_size*max_lots_per_order, Price=0)
            temp = temp-1
            if status['Message'] == 'Success':
                already_placed += max_lots_per_order
        if temp == 0 and end != 0:
            status = prime_client['login'].place_order(
                OrderType='S', Exchange='N', ExchangeType='D', ScripCode=c_scrip, Qty=lot_size*end, Price=0)
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
        while temp > 0:
            status = prime_client['login'].place_order(
                OrderType='S', Exchange='N', ExchangeType='D', ScripCode=p_scrip, Qty=lot_size*max_lots_per_order, Price=0)
            temp = temp-1
            if status['Message'] == 'Success':
                already_placed += max_lots_per_order
        if temp == 0 and end != 0:
            status = prime_client['login'].place_order(
                OrderType='S', Exchange='N', ExchangeType='D', ScripCode=p_scrip, Qty=lot_size*end, Price=0)
            if status['Message'] == 'Success':
                already_placed += end
        yet_to_place = lots-already_placed
    return exclusive_strike, yet_to_place


def rosetta(option_chain):
    ce_data = option_chain[option_chain['CPType'] == 'CE']
    pe_data = option_chain[option_chain['CPType'] == 'PE']
    i = np.array(pe_data['StrikeRate'])[0]
    end = np.array(pe_data['StrikeRate'])[-1]
    ss = np.array(pe_data['StrikeRate'])
    p_lastrate = np.array(list(pe_data['LastRate']))
    c_lastrate = np.array(list(ce_data['LastRate']))
    p_openinterest = np.array(list(pe_data['OpenInterest']))
    c_openinterest = np.array(list(ce_data['OpenInterest']))

    def loss_function(v):
        init_pe = np.dot(p_lastrate, p_openinterest)
        init_ce = np.dot(c_lastrate, c_openinterest)
        tmax = ss-v[0]
        tmax[tmax < 0] = 0
        tmin = v[0]-ss
        tmin[tmin < 0] = 0
        end_pe = np.dot(p_openinterest, tmax)
        end_ce = np.dot(c_openinterest, tmin)
        data = init_ce-end_ce-init_pe+end_pe
        return abs(data)
    a, b = pso(func=loss_function, lb=[i], ub=[end], minfunc=0.1)
    return np.round_(a[0], 1)


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


# %%
client_name = "bhaskar"
prime_client = client_login(client=client_name)
# %%

d0 = data(0)

# %%

# initial trades


def initial_trades(option_chain, x, tron_s, week):
    exclusive_strike = int(np.round((x)/100)*100)
    f = np.sum(option_chain[option_chain['StrikeRate']
               == int(np.round(x/100)*100)]['LastRate'])
    c_strike_s = exclusive_strike+int(np.ceil(f/200)*100)
    c_strike_b = exclusive_strike+int(np.ceil(f/100)*100)
    ce_data = option_chain[option_chain['CPType'] == 'CE']
    price_b = ce_data[ce_data['StrikeRate'] == int(
        np.round(c_strike_b/100)*100)]['LastRate'].iloc[0]
    price_s = ce_data[ce_data['StrikeRate'] == int(
        np.round(c_strike_s/100)*100)]['LastRate'].iloc[0]
    tron_b = int(tron_s*(price_s/price_b))
    order_button(c_strike_b, 'CE_B', tron_b, week)
    order_button(c_strike_s, 'CE_S', tron_s, week)
    return tron_s, tron_b, c_strike_s, c_strike_b

# %%


def strategy(d, tron_s, tron_b, c_strike_s, c_strike_b, week):
    option_chain, x = d[0], d[1]
    exclusive_strike = int(np.round((x)/100)*100)
    f = np.sum(option_chain[option_chain['StrikeRate']
               == int(np.round(x/100)*100)]['LastRate'])
    c_strike_s_new = exclusive_strike+int(np.ceil(f/200)*100)
    c_strike_b_new = exclusive_strike+int(np.ceil(f/100)*100)
    if c_strike_b_new != c_strike_b and c_strike_s_new != c_strike_s and x > c_strike_b:
        order_button(c_strike_s, 'CE_B', tron_s, week)
        order_button(c_strike_b, 'CE_S', tron_b, week)
        ce_data = option_chain[option_chain['CPType'] == 'CE']
        cs_ltp = ce_data[ce_data['StrikeRate'] == int(
            np.round(c_strike_s/100)*100)]['LastRate'].iloc[0]
        cb_ltp = ce_data[ce_data['StrikeRate'] == int(
            np.round(c_strike_b/100)*100)]['LastRate'].iloc[0]
        tron_b = int(tron_s*(cs_ltp/cb_ltp))
        order_button(c_strike_b_new, 'CE_B', tron_b, week)
        order_button(c_strike_s_new, 'CE_S', tron_s, week)
        c_strike_s = c_strike_s_new
        c_strike_b = c_strike_b_new
    if c_strike_b_new != c_strike_b and c_strike_s_new == c_strike_s:
        tron_b1 = tron_b
        ce_data = option_chain[option_chain['CPType'] == 'CE']
        cs_ltp = ce_data[ce_data['StrikeRate'] == int(
            np.round(c_strike_s/100)*100)]['LastRate'].iloc[0]
        cb_ltp = ce_data[ce_data['StrikeRate'] == int(
            np.round(c_strike_b/100)*100)]['LastRate'].iloc[0]
        tron_b = int(tron_s*(cs_ltp/cb_ltp))
        order_button(c_strike_b_new, 'CE_B', tron_b, week)
        order_button(c_strike_b, 'CE_S', tron_b1, week)
        c_strike_s = c_strike_s_new
        c_strike_b = c_strike_b_new
    return tron_s, tron_b, c_strike_s, c_strike_b


week = 0
tron_s = 3
d = data(week)
tron_s, tron_b, c_strike_s, c_strike_b = initial_trades(
    d[0], d[1], tron_s, week)
while True:
    d = data(0)
    tron_s, tron_b, c_strike_s, c_strike_b = strategy(
        d, tron_s, tron_b, c_strike_s, c_strike_b, week)
