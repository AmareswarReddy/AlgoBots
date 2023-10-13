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
from datetime import datetime, timedelta
import yfinance as yf


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


def historical_data(days, interval):
    pastdate = datetime.now() - timedelta(days)
    from_ = datetime.strftime(pastdate, '%Y-%m-%d')
    # df = prime_client['login'].historical_data('N', 'C', 999920005, '1m', from_, str(datetime.today()).split()[0])
    df = yf.download('^NSEBANK', start=from_,
                     end=str(datetime.today()).split()[0], interval=interval)
    return df


def EMA(data, a):
    data['SMAC'] = 0
    close = data['Close'].copy()
    sma = data['SMAC'].copy()
    for i in range(a, sma.size):
        sma.iloc[i] = close.iloc[i-a:i].sum()/a
    del data['SMAC']
    return sma


def marketmove(data_):
    return (EMA(data_, 15)-EMA(data_, 5))[-1]


def max_steel_strategy(indicator, lots, ces, pes, ceb, peb, x, option_chain, intrade):
    exclusive_strike = int(np.round((x)/100)*100)
    ce_data = option_chain[(option_chain['CPType'] == 'CE') & (
        option_chain['StrikeRate'] >= exclusive_strike)]
    pe_data = option_chain[(option_chain['CPType'] == 'PE') & (
        option_chain['StrikeRate'] <= exclusive_strike)]
    if indicator < -30 and intrade == 0:
        c_lastrate = float(
            ce_data[ce_data['StrikeRate'] == exclusive_strike]['LastRate'])
        ces = exclusive_strike
        ceb = exclusive_strike+((int(2*c_lastrate)/100)+1)*100
        order_button(ceb, 'CE_B', lots)
        order_button(ces, 'CE_S', lots)
        intrade = -1

    if indicator > 30 and intrade == 0:
        p_lastrate = float(
            pe_data[pe_data['StrikeRate'] == exclusive_strike]['LastRate'])
        pes = exclusive_strike
        peb = exclusive_strike-((int(2*p_lastrate)/100)+1)*100
        order_button(peb, 'PE_B', lots)
        order_button(pes, 'PE_S', lots)
        intrade = 1

    if indicator > 30 and intrade < 0:
        order_button(ces, 'CE_B', lots)
        order_button(ceb, 'CE_S', lots)
        intrade = 0

    if indicator < -30 and intrade > 0:
        order_button(pes, 'PE_B', lots)
        order_button(peb, 'PE_S', lots)
        intrade = 0

    if intrade > 0 and x < peb-115:
        order_button(pes, 'PE_B', lots)
        order_button(pes-100, 'PE_S', lots)
        pes -= 100
        if pes == peb:
            intrade = 0

    if intrade < 0 and x > ceb+115:
        order_button(ces, 'CE_B', lots)
        order_button(ces+100, 'CE_S', lots)
        ces += 100
        if ces == ceb:
            intrade = 0
    return ces, pes, ceb, peb, intrade


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
    intrade = 0
    p_strike_b, p_strike_s, c_strike_b, c_strike_s = 0, 0, 0, 0
    while int(ind_time[11:13])*60+int(ind_time[14:16]) < 568:
        ind_time = datetime.now(timezone("Asia/Kolkata")
                                ).strftime('%Y-%m-%d %H:%M:%S.%f')
    option_chain, x = data(week)


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
    indicator = marketmove(historical_data(5))
    c_strike_s, p_strike_s, c_strike_b, p_strike_b, intrade = max_steel_strategy(indicator, max_lots_tracker, c_strike_s,
                                                                                 p_strike_s, c_strike_b, p_strike_b, x, option_chain, intrade)
positions_json = {'show': {'c_strike_b': c_strike_b, 'p_strike_b': p_strike_b, 'c_sell_tron': c_sell_tron, 'p_sell_tron': p_sell_tron, 'c_strike_s': c_strike_s, 'p_strike_s': p_strike_s,
                           'c_buy_tron': c_buy_tron_json, 'p_buy_tron': p_buy_tron_json}, 'ranger': {'ceb_strike': ceb_strike, 'peb_strike': peb_strike, 'lots_tracker': lots_tracker, 'lots_diff': lots_diff}}

print(positions_json)
with open(client_name+'_ultimateshow_positions.pkl', "wb") as f:
    pickle.dump(positions_json, f)

order_button(c_strike_s, 'CE_B', c_sell_tron)
order_button(p_strike_s, 'PE_B', p_sell_tron)
order_button(c_strike_b, 'CE_S', c_buy_tron_json)
order_button(p_strike_b, 'PE_S', p_buy_tron_json)
if ceb_strike != 0:
    order_button(ceb_strike, 'CE_S', lots_tracker)
elif peb_strike != 0:
    order_button(peb_strike, 'PE_S', lots_tracker)


# %%
# research
data_ = historical_data(7)
close = np.array(data_['Close'].copy())[50:]
ema15 = np.array(EMA(data_, 50))[50:]
ema5 = np.array(EMA(data_, 15))[50:]


def ind(minutes):
    u = []
    for i in range(minutes, len(ema15)):
        u += [np.sum((ema15-ema5)[i-minutes:i])]
    return u


# plt.plot(close[:250])
# plt.plot((ema15-ema5)[:250])
# plt.show()
# dual axes
fig, ax = plt.subplots(figsize=(40, 5))
ax.set_title('Banknifty')
ax2 = ax.twinx()
ax.plot(close, alpha=1, color='white')
# ax2.plot(ind(15), color='pink')
ax2.plot(ema15-ema5, color='pink')
ax2.plot(np.multiply(ema15, 0), color='green')
ax2.plot(np.multiply(ema15, 0), color='green')
ax.set_ylabel('lastrate')
ax2.set_ylabel('indicator')
plt.tight_layout()
plt.show()

# %%
data_1h = historical_data(7, '1m')
# %%


def similarity(samples, data_1h):

    similarity_index = []
    check = np.reshape(np.array(data_1h.iloc[len(
        data_1h)-samples:][['Open', 'High', 'Low', 'Close']]), (samples*4))
    check = ((check/check[0])-1)*10000

    check1 = np.reshape(np.array(data_1h.iloc[len(
        data_1h)-samples:]['Volume']), (samples))
    check1 = ((check1/np.average(check1))-1)
    for i in range(samples, len(data_1h)):
        to_check = np.reshape(
            np.array(data_1h.iloc[i-samples:i][['Open', 'High', 'Low', 'Close']]), (samples*4))
        to_check = ((to_check/to_check[0])-1)*10000

        to_check1 = np.reshape(
            np.array(data_1h.iloc[i-samples:i]['Volume']), (samples))
        to_check1 = ((to_check1/np.average(to_check1))-1)
        similarity_index += [np.sum(np.power(check-to_check, 2)/len(check)) +
                             np.sum(np.power(check1-to_check1, 2)/len(check1))]
    history_index = [np.argmin(similarity_index)]
    for i in range(0, len(similarity_index)):
        similarity_index[np.argmin(similarity_index)] += 100
        if history_index[0] == np.argmin(similarity_index):
            break
        history_index += [np.argmin(similarity_index)]
    match_ = np.min(similarity_index)
    a = data_1h.iloc[np.array(history_index)+samples]
    temp1 = np.sign(np.sum(np.array(a.Close-a.Open))/len(a))
    # temp2 = np.sign(np.sum(np.sign(np.array(a.Close-a.Open))/len(a)))
    return temp1, match_

# %%


def pnl(data_1h, test_samples):
    sh = data_1h.copy()
    profits = 0
    losses = 0
    net_profit = 0
    for i in range(len(data_1h)-test_samples, len(data_1h)):
        indicator, match_ = similarity(4, sh.iloc[:i])
        live_move = sh.iloc[i].Close-sh.iloc[i].Open
        if abs(indicator) > 0.1 and match_ > 0:
            max_move = sh.iloc[i].Close-sh.iloc[i].Open
            print([indicator, live_move, match_])
            eplorer_pnl = np.sign(live_move) == np.sign(indicator)
            net_profit += live_move*(eplorer_pnl-0.5)*2
            if eplorer_pnl:
                profits += 1

            else:
                losses += 1

    return profits, losses, net_profit


# %%
