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
from pyswarm import pso
from pytz import timezone
from cred import *
from py5paisa.order import Basket_order
from scipy import interpolate
from sklearn.linear_model import LinearRegression


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
    client_list[client]['lots'] = round((client_list[client]['login'].margin()[
                                        0]['AvailableMargin']-200000)/180000)
    return client_list[client]


def order_button(exclusive_strike, type, lots):
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

# %%


def indicator_(listv_ind, listv_ind_n, listv_ind_f, listx):
    if len(listx) > 50:
        net_v = -(np.array(listv_ind) +
                  np.array(listv_ind_n)+np.array(listv_ind_f))
        x = np.array(net_v)[:50].reshape((-1, 1))
        y = listx[:50]
        model = LinearRegression()
        model.fit(x, y)
        slope = model.coef_[0]
        x_pred = model.predict([[net_v[-1]]])[0]
        if slope > 0.1:
            if listx[-1] > x_pred:
                return 1
            elif listx[-1] < x_pred:
                return -1
        else:
            return 0
    else:
        return 0

# market_ripper,day_volume_indicator,day_market_ripper


def premium_sum(x):
    c_strike = int(np.round((x)/100)*100)
    p_strike = c_strike
    ce_data = option_chain[option_chain['CPType'] == 'CE']
    pe_data = option_chain[option_chain['CPType'] == 'PE']
    c_lastrate = float(
        ce_data[ce_data['StrikeRate'] == c_strike]['LastRate'])
    p_lastrate = float(
        pe_data[pe_data['StrikeRate'] == p_strike]['LastRate'])
    return c_lastrate+p_lastrate


def options_indicator(option_chain, x, dist, cv, pv, cvn, pvn, cvf, pvf, earlier_pv, earlier_cv, earlier_pvn, earlier_cvn, earlier_pvf, earlier_cvf):
    at_strike = int(np.round((x)/100)*100)
    near_option_chain = option_chain[(
        option_chain['StrikeRate'] > at_strike-dist) & (option_chain['StrikeRate'] < at_strike+dist)].copy()
    far_option_chain = pd.concat([option_chain[(option_chain['StrikeRate'] > at_strike+dist)],
                                 option_chain[(option_chain['StrikeRate'] < at_strike-dist)]]).copy()

    def rusteze(option_chain, cv, pv, earlier_cv, earlier_pv):
        ce_data = option_chain[option_chain['CPType'] == 'CE']
        pe_data = option_chain[option_chain['CPType'] == 'PE']
        p_lastrate = np.array(list(pe_data['LastRate']))
        c_lastrate = np.array(list(ce_data['LastRate']))
        p_volume = np.array(list(pe_data['Volume']))
        c_volume = np.array(list(ce_data['Volume']))
        p_volume_change = p_volume
        c_volume_change = c_volume
        cv_temp = np.sum(np.multiply(c_volume_change, c_lastrate))
        pv_temp = np.sum(np.multiply(p_volume_change, p_lastrate))
        cv = cv+cv_temp
        pv = pv+pv_temp
        cc = cv/(pv+0.1)
        v_ind = ((2*cc*cc)/(1+cc*cc))-1
        earlier_pv = p_volume
        earlier_cv = c_volume
        return v_ind, earlier_pv, earlier_cv
    v_ind, earlier_pv, earlier_cv = rusteze(
        option_chain, cv, pv, earlier_cv, earlier_pv)
    v_ind_n, earlier_pvn, earlier_cvn = rusteze(
        near_option_chain, cvn, pvn, earlier_cvn, earlier_pvn)
    v_ind_f, earlier_pvf, earlier_cvf = rusteze(
        far_option_chain, cvf, pvf, earlier_cvf, earlier_pvf)

    return v_ind, earlier_pv, earlier_cv, v_ind_n, earlier_pvn, earlier_cvn, v_ind_f, earlier_pvf, earlier_cvf

# %%


def data(week):
    exchange = 'BANKNIFTY'
    while True:
        try:
            expiry_timestamps = prime_client['login'].get_expiry(
                "N", exchange).copy()
            current_expiry_time_stamp_weekly = int(
                expiry_timestamps['Expiry'][week]['ExpiryDate'][6:19])
            expiry_timestamps = prime_client['login'].get_expiry(
                "N", exchange).copy()
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


def lots_drop(strike, side, yet_to_place):
    k = yet_to_place
    while yet_to_place > 0:
        sleep(1)
        yet_to_place -= 1
        xx, pending = order_button(strike, side, yet_to_place)
        if pending == 0:
            break
    return k-yet_to_place


def buy_kickoff(start, indicator, earlier_indicator, exclusive_strike, tron):
    if abs(indicator-earlier_indicator) == 2 and start == 0:
        indicator = 0
    if start == 0:
        s = indicator
        if s > 0:
            exclusive_strike, yet_to_place = order_button(
                exclusive_strike, 'CE_B', tron)
            tron -= lots_drop(exclusive_strike, 'CE_B', yet_to_place)
            # exclusive_strike,yet_to_place=order_button(exclusive_strike,'PE_B',tron)
            # exclusive_strike,yet_to_place=order_button(exclusive_strike-day_of_week,'PE_S',tron)
            start = 1
            indicator = 1
        elif s < 0:
            exclusive_strike, yet_to_place = order_button(
                exclusive_strike, 'PE_B', tron)
            tron -= lots_drop(exclusive_strike, 'PE_B', yet_to_place)
            # exclusive_strike,yet_to_place=order_button(exclusive_strike,'CE_B',tron)
            # exclusive_strike,yet_to_place=order_button(exclusive_strike+day_of_week,'CE_S',tron)
            start = 1
            indicator = -1
    elif start == 1:
        # if earlier_indicator==0 and indicator==1:
        #    exclusive_strike,yet_to_place=order_button(0,'CE_B',tron)
        #    tron-=lots_drop(exclusive_strike,'CE_B',yet_to_place)
        #    #exclusive_strike,yet_to_place=order_button(exclusive_strike,'PE_B',tron)
        #    #exclusive_strike,yet_to_place=order_button(exclusive_strike-day_of_week,'PE_S',tron)
        # if earlier_indicator==0 and indicator==-1:
        #    exclusive_strike,yet_to_place=order_button(0,'PE_B',tron)
        #    tron-=lots_drop(exclusive_strike,'PE_B',yet_to_place)
        #    #exclusive_strike,yet_to_place=order_button(exclusive_strike,'CE_B',tron)
        #    #exclusive_strike,yet_to_place=order_button(exclusive_strike+day_of_week,'CE_S',tron)
        # if earlier_indicator==-1 and indicator==0:
        #    exclusive_strike,yet_to_place=order_button(exclusive_strike,'PE_S',tron)
        #    #exclusive_strike,yet_to_place=order_button(exclusive_strike,'CE_S',tron)
        #    #exclusive_strike,yet_to_place=order_button(exclusive_strike+day_of_week,'CE_B',tron)
        # if earlier_indicator==1 and indicator==0:
        #    exclusive_strike,yet_to_place=order_button(exclusive_strike,'CE_S',tron)
        #    #exclusive_strike,yet_to_place=order_button(exclusive_strike,'PE_S',tron)
        #    #exclusive_strike,yet_to_place=order_button(exclusive_strike-day_of_week,'PE_B',tron)
        if earlier_indicator == -1 and indicator == 1:
            exclusive_strike, yet_to_place = order_button(
                exclusive_strike, 'PE_S', tron)
            exclusive_strike, yet_to_place = order_button(0, 'CE_B', tron)
            tron -= lots_drop(exclusive_strike, 'CE_B', yet_to_place)

        if earlier_indicator == 1 and indicator == -1:
            exclusive_strike, yet_to_place = order_button(
                exclusive_strike, 'CE_S', tron)
            exclusive_strike, yet_to_place = order_button(0, 'PE_B', tron)
            tron -= lots_drop(exclusive_strike, 'PE_B', yet_to_place)

        if indicator == 0:
            if earlier_indicator == -1:
                exclusive_strike, yet_to_place = order_button(
                    exclusive_strike, 'PE_S', tron)
            if earlier_indicator == 1:
                exclusive_strike, yet_to_place = order_button(
                    exclusive_strike, 'CE_S', tron)

    return exclusive_strike, tron, start, indicator


def sell_kickoff(x, start, indicator, earlier_indicator, exclusive_strike, d, tron):
    if abs(indicator-earlier_indicator) == 2:
        indicator = 0
    if start == 0:
        s = indicator
        if s > 0:
            exclusive_strike = int(np.round(x/100)*100)-d
            exclusive_strike, yet_to_place = order_button(
                exclusive_strike, 'PE_S', tron)
            tron -= lots_drop(exclusive_strike, 'PE_S', yet_to_place)
            start = 1
        elif s < 0:
            exclusive_strike = int(np.round(x/100)*100)+d
            exclusive_strike, yet_to_place = order_button(
                exclusive_strike, 'CE_S', tron)
            tron -= lots_drop(exclusive_strike, 'CE_S', yet_to_place)
            start = 1
    elif start == 1:
        if earlier_indicator == 0 and indicator == 1:
            exclusive_strike = int(np.round(x/100)*100)-d
            exclusive_strike, yet_to_place = order_button(
                exclusive_strike, 'PE_S', tron)
            tron -= lots_drop(exclusive_strike, 'PE_S', yet_to_place)
        if earlier_indicator == 0 and indicator == -1:
            exclusive_strike = int(np.round(x/100)*100)+d
            exclusive_strike, yet_to_place = order_button(
                exclusive_strike, 'CE_S', tron)
            tron -= lots_drop(exclusive_strike, 'CE_S', yet_to_place)
        if earlier_indicator == -1 and indicator == 0:
            exclusive_strike, yet_to_place = order_button(
                exclusive_strike, 'CE_B', tron)
        if earlier_indicator == 1 and indicator == 0:
            exclusive_strike, yet_to_place = order_button(
                exclusive_strike, 'PE_B', tron)
    return exclusive_strike, tron, start, indicator


def get_strike_from_scrip(scripcode, exchange):
    if exchange == 'BANKNIFTY':
        option_chain, a1 = data(0)
    k1 = option_chain[option_chain['ScripCode'] == scripcode]
    return int(k1['StrikeRate'])


def clear_open_positions():
    S = pd.DataFrame(prime_client['login'].positions())
    for i in range(0, len(S)):
        if ('BANKNIFTY' in S['ScripName'].iloc[i]) and S['NetQty'].iloc[i] != 0:
            if S['NetQty'].iloc[i] < 0 and ('PE' in S['ScripName'].iloc[i]):
                order_button(get_strike_from_scrip(
                    S['ScripCode'].iloc[i], 'BANKNIFTY'), 'PE_B', int(abs(S['NetQty'].iloc[i])/25))
            elif S['NetQty'].iloc[i] < 0 and ('CE' in S['ScripName'].iloc[i]):
                order_button(get_strike_from_scrip(
                    S['ScripCode'].iloc[i], 'BANKNIFTY'), 'CE_B', int(abs(S['NetQty'].iloc[i])/25))
            elif S['NetQty'].iloc[i] > 0 and ('CE' in S['ScripName'].iloc[i]):
                order_button(get_strike_from_scrip(
                    S['ScripCode'].iloc[i], 'BANKNIFTY'), 'CE_S', int(abs(S['NetQty'].iloc[i])/25))
            elif S['NetQty'].iloc[i] > 0 and ('PE' in S['ScripName'].iloc[i]):
                order_button(get_strike_from_scrip(
                    S['ScripCode'].iloc[i], 'BANKNIFTY'), 'PE_S', int(abs(S['NetQty'].iloc[i])/25))
            S = pd.DataFrame(prime_client['login'].positions())
            if len(S[S['NetQty'] != 0]) != 0:
                return clear_open_positions()
        elif len(S[S['NetQty'] != 0]) == 0:
            return 0


# %%
client_name = input('enter the client name Eg: vinathi,bhaskar ')
# client_name   = 'bhaskar'
tron = int(input('enter the number of lots to trade (Eg:3):'))
typical_tron = 1
prime_client = client_login(client=client_name)
ind_time = datetime.now(timezone("Asia/Kolkata")
                        ).strftime('%Y-%m-%d %H:%M:%S.%f')
while int(ind_time[11:13])*60+int(ind_time[14:16]) < 555 or int(ind_time[11:13])*60+int(ind_time[14:16]) > 885:
    ind_time = datetime.now(timezone("Asia/Kolkata")
                            ).strftime('%Y-%m-%d %H:%M:%S.%f')
# %%
exclusive_strike = 0
type = ''
option_chain, x = data(week=0)


def premium_sum(x):
    c_strike = int(np.round((x)/100)*100)
    p_strike = c_strike
    ce_data = option_chain[option_chain['CPType'] == 'CE']
    pe_data = option_chain[option_chain['CPType'] == 'PE']
    c_lastrate = float(
        ce_data[ce_data['StrikeRate'] == c_strike]['LastRate'])
    p_lastrate = float(
        pe_data[pe_data['StrikeRate'] == p_strike]['LastRate'])
    return c_lastrate+p_lastrate


at_strike = int(np.round((x)/100)*100)
dist = premium_sum(x)
near_option_chain = option_chain[(
    option_chain['StrikeRate'] > at_strike-dist) & (option_chain['StrikeRate'] < at_strike+dist)].copy()
far_option_chain = pd.concat([option_chain[(option_chain['StrikeRate'] > at_strike+dist)],
                             option_chain[(option_chain['StrikeRate'] < at_strike-dist)]]).copy()
ce_data = option_chain[option_chain['CPType'] == 'CE']
pe_data = option_chain[option_chain['CPType'] == 'PE']
earlier_pv = np.array(list(pe_data['Volume']))
earlier_cv = np.array(list(ce_data['Volume']))
ce_datan = near_option_chain[near_option_chain['CPType'] == 'CE']
pe_datan = near_option_chain[near_option_chain['CPType'] == 'PE']
earlier_pvn = np.array(list(pe_datan['Volume']))
earlier_cvn = np.array(list(ce_datan['Volume']))
ce_dataf = far_option_chain[far_option_chain['CPType'] == 'CE']
pe_dataf = far_option_chain[far_option_chain['CPType'] == 'PE']
earlier_pvf = np.array(list(pe_dataf['Volume']))
earlier_cvf = np.array(list(ce_dataf['Volume']))
cv, pv, cvn, pvn, cvf, pvf, day_coi, day_poi = 0, 0, 0, 0, 0, 0, 0, 0
v_ind, earlier_pv, earlier_cv, v_ind_n, earlier_pvn, earlier_cvn, v_ind_f, earlier_pvf, earlier_cvf = options_indicator(
    option_chain, x, dist, cv, pv, cvn, pvn, cvf, pvf, earlier_pv, earlier_cv, earlier_pvn, earlier_cvn, earlier_pvf, earlier_cvf)

start = 0

# %%

# start=0
# day_of_week=200#100*(int(input("enter the day from expiry(Eg:enter 1 if it's Wednesday): "))+1)

# %%
listv_ind = []
listv_ind_n = []
listv_ind_f = []
listx = []
earlier_indicator = 0
dist = premium_sum(x)
volume_check = 0
while int(ind_time[11:13])*60+int(ind_time[14:16]) < 922:
    sleep(61)
    ind_time = datetime.now(timezone("Asia/Kolkata")
                            ).strftime('%Y-%m-%d %H:%M:%S.%f')
    option_chain, x = data(week=0)
    print('volume_check', np.sum(option_chain['Volume'])-volume_check)
    volume_check = np.sum(option_chain['Volume'])
    v_ind, earlier_pv, earlier_cv, v_ind_n, earlier_pvn, earlier_cvn, v_ind_f, earlier_pvf, earlier_cvf = options_indicator(
        option_chain, x, dist, cv, pv, cvn, pvn, cvf, pvf, earlier_pv, earlier_cv, earlier_pvn, earlier_cvn, earlier_pvf, earlier_cvf)
    listv_ind += [v_ind]
    listv_ind_n += [v_ind_n]
    listv_ind_f += [v_ind_f]
    listx += [x]
    B = indicator_(listv_ind, listv_ind_n, listv_ind_f, listx)
    print(B)
    exclusive_strike, tron, start, earlier_indicator = buy_kickoff(
        start, B, earlier_indicator, exclusive_strike, tron)
    indicator_saver = {'volume_indicator': B}
    out_file = open('Volume_indicator.json', "w")
    json.dump(indicator_saver, out_file, indent=6)
    out_file.close()
# clear_open_positions()
buy_kickoff(start, 0, earlier_indicator, exclusive_strike, tron)
# %%
