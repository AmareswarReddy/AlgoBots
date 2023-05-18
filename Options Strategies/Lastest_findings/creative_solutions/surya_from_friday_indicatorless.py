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
# client_name=input('enter the client name Eg: vinathi,bhaskar '


def order_button(exclusive_strike, type, lots):
    sleep(0.5)
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


def initial_strangle_trades(option_chain, x, tron):
    exclusive_strike = int(np.round((x)/100)*100)
    if tron == 0:
        tron = int(prime_client['login'].margin()[0]['AvailableMargin']/170000)
    f = np.sum(option_chain[option_chain['StrikeRate']
               == int(np.round(x/100)*100)]['LastRate'])
    factor = float(1.8+1.5*np.random.rand(1)/2)*int(np.ceil(f/100)*100)
    factor = int(np.round((factor)/100)*100)
    c_strike = exclusive_strike+factor
    p_strike = exclusive_strike-factor
    tron = finalise_tron(p_strike=p_strike, c_strike=c_strike, tron=tron)
    return tron, c_strike, p_strike


def margin_utilizer(c_strike, p_strike):
    k = prime_client['login'].margin()[0]['AvailableMargin']
    tron = int(k/180000)
    tron = finalise_tron(p_strike, c_strike, tron)
    return tron


def re_adjust_strangle(strangle_lastrate_sum,option_chain,x):
    exclusive_strike=int(np.round((x)/100)*100)
    f=np.sum(option_chain[option_chain['StrikeRate']==int(np.round(x/100)*100)]['LastRate'])
    factor=float(1.9)*int(np.ceil(f/100)*100)
    factor=int(np.round((factor)/100)*100)
    c_strike=exclusive_strike+factor
    p_strike=exclusive_strike-factor
    ce_data=option_chain[option_chain['CPType']=='CE']
    pe_data=option_chain[option_chain['CPType']=='PE']
    c_lastrate=float(ce_data[ce_data['StrikeRate']==c_strike]['LastRate'])
    p_lastrate=float(pe_data[pe_data['StrikeRate']==p_strike]['LastRate'])
    cp_sum=c_lastrate+p_lastrate
    if 2*strangle_lastrate_sum<cp_sum:
        return True
    else:
        return False

def new_strangle_adjustment_trades(option_chain,x,tron,sell_value,c_strike,p_strike):
    def strangle_sum(c_strike,p_strike):
        ce_data=option_chain[option_chain['CPType']=='CE']
        pe_data=option_chain[option_chain['CPType']=='PE']
        c_lastrate=float(ce_data[ce_data['StrikeRate']==c_strike]['LastRate'])
        p_lastrate=float(pe_data[pe_data['StrikeRate']==p_strike]['LastRate'])
        return c_lastrate+p_lastrate
    exclusive_strike=int(np.round((x)/100)*100)
    f=np.sum(option_chain[option_chain['StrikeRate']==int(np.round(x/100)*100)]['LastRate'])
    factor=float(2+np.random.rand(1)/2)*int(np.ceil(f/100)*100)
    factor=int(np.round((factor)/100)*100)
    old_c_strike=c_strike
    old_p_strike=p_strike
    while True:
        factor-=100
        c_strike=exclusive_strike+factor
        p_strike=exclusive_strike-factor
        new_sell_value=strangle_sum(c_strike,p_strike)
        if new_sell_value>sell_value or factor==0:
            if c_strike==old_c_strike:
                to_take_c_strike=0
            elif c_strike!=old_c_strike:
                order_button(old_c_strike,'CE_B',tron)
                to_take_c_strike=1
            if p_strike==old_p_strike:
                to_take_p_strike=0
            elif p_strike!=old_p_strike:
                order_button(old_p_strike,'PE_B',tron)
                to_take_p_strike=1
            tron=finalise_tron(p_strike=p_strike,c_strike=c_strike,tron=tron,to_take_c_strike=to_take_c_strike,to_take_p_strike=to_take_p_strike)
            break
    return tron,c_strike,p_strike



def strangle_adjustments(x,exclusive_strike,c_strike,p_strike,tron):
    if c_strike!=p_strike:
        ce_data=option_chain[option_chain['CPType']=='CE']
        pe_data=option_chain[option_chain['CPType']=='PE']
        c_lastrate=float(ce_data[ce_data['StrikeRate']==c_strike]['LastRate'])
        p_lastrate=float(pe_data[pe_data['StrikeRate']==p_strike]['LastRate'])
        if re_adjust_strangle(c_lastrate+p_lastrate,option_chain,x):
            while True:
                strike,yet_to_place=order_button(p_strike,'PE_B',tron)
                if yet_to_place==0:
                    break
            while True:
                strike,yet_to_place=order_button(c_strike,'CE_B',tron)
                if yet_to_place==0:
                    break
            tron,c_strike,p_strike=initial_strangle_trades(option_chain,x,tron)
        at_strike=int(np.round((x)/100)*100)
        at_strike_premium_sum=float(ce_data[ce_data['StrikeRate']==at_strike]['LastRate'])+float(pe_data[pe_data['StrikeRate']==at_strike]['LastRate'])
        if (c_lastrate/p_lastrate>(1+at_strike_premium_sum/(c_lastrate+p_lastrate)) or p_lastrate/c_lastrate>(1+at_strike_premium_sum/(c_lastrate+p_lastrate)) ) :
            tron,c_strike,p_strike=new_strangle_adjustment_trades(option_chain,x,tron,c_lastrate+p_lastrate,c_strike,p_strike)
            exclusive_strike=(c_strike==p_strike)*c_strike
        if x>=c_strike or x<=p_strike:
            at_strike=int(np.round((x)/100)*100)
            if at_strike==p_strike and at_strike==c_strike:
                pass
            elif at_strike==p_strike and at_strike!=c_strike:
                while True:
                    strike,yet_to_place=order_button(c_strike,'CE_B',tron)
                    if yet_to_place==0:
                        break
                c_strike,yet_to_place=order_button(at_strike,'CE_S',tron)
                while True:
                    if yet_to_place!=0:
                        tron=tron-1
                        while True:
                            strike,y=order_button(p_strike,'PE_B',1)
                            if y==0:
                                break
                        sleep(1)
                        c_strike,yet_to_place=order_button(at_strike,'CE_S',tron)
                    if yet_to_place==0:
                        break
                exclusive_strike,c_strike,p_strike=at_strike,at_strike,at_strike
            elif at_strike!=p_strike and at_strike==c_strike:
                while True:
                    strike,yet_to_place=order_button(p_strike,'PE_B',tron)
                    if yet_to_place==0:
                        break
                p_strike,yet_to_place=order_button(at_strike,'PE_S',tron)
                while True:
                    if yet_to_place!=0:
                        tron=tron-1
                        while True:
                            strike,y=order_button(c_strike,'CE_B',1)
                            if y==0:
                                break
                        sleep(1)
                        p_strike,yet_to_place=order_button(at_strike,'PE_S',tron)
                    if yet_to_place==0:
                        break
                exclusive_strike,c_strike,p_strike=at_strike,at_strike,at_strike
            elif at_strike!=p_strike and at_strike!=c_strike:
                k,y1=order_button(p_strike,'PE_B',tron)
                while True:
                    if y1!=0:
                        k,y1=order_button(p_strike,'PE_B',tron)
                    if y1==0:
                        break
                k,y1=order_button(p_strike,'CE_B',tron)
                while True:
                    if y1!=0:
                        k,y1=order_button(p_strike,'CE_B',tron)
                    if y1==0:
                        break
                tron=finalise_tron(c_strike=at_strike,p_strike=at_strike,tron=tron,to_take_c_strike=1,to_take_p_strike=1)
                exclusive_strike,c_strike,p_strike=at_strike,at_strike,at_strike
        tron=tron+margin_utilizer(c_strike,p_strike)
    return exclusive_strike,c_strike,p_strike,tron




def initial_leg_trades(x, option_chain, tron):
    exclusive_strike = int(np.round((x)/100)*100)
    ce_data = option_chain[option_chain['CPType'] == 'CE']
    pe_data = option_chain[option_chain['CPType'] == 'PE']
    c_lastrate = float(ce_data[ce_data['StrikeRate']
                       == exclusive_strike]['LastRate'])
    p_lastrate = float(pe_data[pe_data['StrikeRate']
                       == exclusive_strike]['LastRate'])
    f = (p_lastrate+c_lastrate)/2
    factor = max(100, int(np.floor((f)/100)*100))
    c_strike = exclusive_strike+factor
    p_strike = exclusive_strike-factor
    k, y1 = order_button(p_strike, 'PE_B', tron+1)
    while True:
        if y1 != 0:
            k, y1 = order_button(p_strike, 'PE_B', tron+1)
        if y1 == 0:
            break
    k, y1 = order_button(c_strike, 'CE_B', tron+1)
    while True:
        if y1 != 0:
            k, y1 = order_button(c_strike, 'CE_B', tron+1)
        if y1 == 0:
            break
    final_tron = finalise_tron(
        c_strike=exclusive_strike, p_strike=exclusive_strike, tron=tron)
    if final_tron != tron:
        order_button(p_strike, 'PE_S', tron-final_tron)
        order_button(c_strike, 'CE_S', tron-final_tron)
    return final_tron, final_tron, c_strike, p_strike, exclusive_strike, exclusive_strike


def extra_lots_decider():
    a = datetime.today().weekday()
    if a == 4:
        return 2
    if a != 4:
        return a+2


def surya(x, option_chain, c_strike_b, p_strike_b, c_leg_tron, p_leg_tron, exclusive_strike, strangle_c_strike, strangle_p_strike, strangle_tron):
    if strangle_tron > 0:
        strangle_c_strike = (exclusive_strike == 0) * \
            strangle_c_strike+exclusive_strike
        strangle_p_strike = (exclusive_strike == 0) * \
            strangle_p_strike+exclusive_strike
        ce_data = option_chain[option_chain['CPType'] == 'CE']
        pe_data = option_chain[option_chain['CPType'] == 'PE']
        c_lastrate = float(
            ce_data[ce_data['StrikeRate'] == c_strike_b]['LastRate'])
        p_lastrate = float(
            pe_data[pe_data['StrikeRate'] == p_strike_b]['LastRate'])
        call_factor = max(100, int(np.ceil((c_lastrate)/100)*100))
        put_factor = max(100, int(np.ceil((p_lastrate)/100)*100))
        new_p_strike_b, new_c_strike_b = 0, 0
        extra_lots = extra_lots_decider()
        if x > c_strike_b and c_lastrate > 100:
            new_c_strike_b, y = order_button(
                c_strike_b+call_factor, 'CE_B', c_leg_tron+extra_lots)
            while y != 0:
                if strangle_tron == 0:
                    break
                order_button(strangle_c_strike, 'CE_B', 1)
                order_button(strangle_p_strike, 'PE_B', 1)
                strangle_tron -= 1
                new_c_strike_b, y = order_button(
                    c_strike_b+call_factor, 'CE_B', c_leg_tron+extra_lots)

            o, y = order_button(c_strike_b, 'CE_S', c_leg_tron+extra_lots)
            while y != 0:
                if strangle_tron == 0:
                    break
                order_button(strangle_c_strike, 'CE_B', 1)
                order_button(strangle_p_strike, 'PE_B', 1)
                strangle_tron -= 1
                o, y = order_button(c_strike_b, 'CE_S', c_leg_tron+extra_lots)
            c_leg_tron += extra_lots
        elif x < p_strike_b and p_lastrate > 100:
            new_p_strike_b, y = order_button(
                p_strike_b-put_factor, 'PE_B', p_leg_tron+extra_lots)
            while y != 0:
                if strangle_tron == 0:
                    break
                order_button(strangle_c_strike, 'CE_B', 1)
                order_button(strangle_p_strike, 'PE_B', 1)
                strangle_tron -= 1
                new_p_strike_b, y = order_button(
                    p_strike_b-put_factor, 'PE_B', p_leg_tron+extra_lots)
            o, y = order_button(p_strike_b, 'PE_S', p_leg_tron+extra_lots)
            while y != 0:
                if strangle_tron == 0:
                    break
                order_button(strangle_c_strike, 'CE_B', 1)
                order_button(strangle_p_strike, 'PE_B', 1)
                strangle_tron -= 1
                o, y = order_button(p_strike_b, 'PE_S', p_leg_tron+extra_lots)
            p_leg_tron += extra_lots
        new_c_strike_b, new_p_strike_b = c_strike_b * \
            (new_c_strike_b == 0)+new_c_strike_b, p_strike_b * \
            (new_p_strike_b == 0)+new_p_strike_b
    if strangle_tron == 0:
        new_c_strike_b, new_p_strike_b = c_strike_b, p_strike_b
    return new_c_strike_b, new_p_strike_b, c_leg_tron, p_leg_tron, strangle_tron


def intel_strike_mover(x, c_strike_intel, p_strike_intel, tron_intel, strangle_c_strike, strangle_p_strike, strangle_tron):
    at_strike = int(np.round((x)/100)*100)
    new_c_strike_intel = c_strike_intel
    new_p_strike_intel = p_strike_intel
    if c_strike_intel-x > 53:
        order_button(c_strike_intel, 'CE_B', tron_intel)
        new_c_strike_intel, y = order_button(at_strike, 'CE_S', tron_intel)
        while y != 0:
            if strangle_tron == 0:
                break
            order_button(strangle_c_strike, 'CE_B', 1)
            order_button(strangle_p_strike, 'PE_B', 1)
            strangle_tron -= 1
            o, y = order_button(at_strike, 'CE_S', tron_intel)
    if x-p_strike_intel > 53:
        order_button(p_strike_intel, 'PE_B', tron_intel)
        new_p_strike_intel, y = order_button(at_strike, 'PE_S', tron_intel)
        while y != 0:
            if strangle_tron == 0:
                break
            order_button(strangle_c_strike, 'CE_B', 1)
            order_button(strangle_p_strike, 'PE_B', 1)
            strangle_tron -= 1
            o, y = order_button(at_strike, 'PE_S', tron_intel)
    return new_c_strike_intel, new_p_strike_intel


def exclusive_strike_change_trades(exclusive_strike, x, tron):
    k, y1 = order_button(exclusive_strike, 'PE_B', tron)
    while True:
        if y1 != 0:
            k, y1 = order_button(exclusive_strike, 'PE_B', tron)
        if y1 == 0:
            break
    k, y1 = order_button(exclusive_strike, 'CE_B', tron)
    while True:
        if y1 != 0:
            k, y1 = order_button(exclusive_strike, 'CE_B', tron)
        if y1 == 0:
            break
    exclusive_strike = int(np.round((x)/100)*100)
    tron = finalise_tron(c_strike=exclusive_strike,
                         p_strike=exclusive_strike, tron=tron)
    return exclusive_strike, tron


def exit_signal(option_chain, exclusive_strike):
    ind_time = datetime.now(timezone("Asia/Kolkata")
                            ).strftime('%Y-%m-%d %H:%M:%S.%f')
    temp = np.sum(
        option_chain[option_chain['StrikeRate'] == exclusive_strike]['LastRate'])
    if temp < 66 or int(ind_time[11:13])*60+int(ind_time[14:16]) > 929:
        return 1
    else:
        return 0


def exit_trades(exclusive_strike, tron):
    order_button(exclusive_strike, 'PE_B', tron)
    order_button(exclusive_strike, 'CE_B', tron)


def straddle_special_adjustment(exclusive_strike, x, tron):
    if exclusive_strike != 0 and tron != 0:
        def exclusive_strike_change_signal(earlier_x, x):
            a = (x-earlier_x)/66
            return abs(a)
        if exclusive_strike_change_signal(earlier_x=exclusive_strike, x=x) > 1:
            exclusive_strike, tron = exclusive_strike_change_trades(
                exclusive_strike, x, tron)
        if exit_signal(option_chain, exclusive_strike) == 1 and exclusive_strike != 0:
            exit_trades(exclusive_strike, tron)
            tron = 0
    return exclusive_strike, tron


# %%
client_name = input('enter the client name: ')
prime_client = client_login(client=client_name)
option_chain, x = data(week=0)
start = int(
    input('enter 0 if starting the strategy for the first time, else 1 :  '))
from_json = input(
    'to take positions from existing positions json file (y/n): ')
if start == 0:
    leg_tron = int(input('leg_tron'))
    tron_intel = leg_tron
    ind_time = datetime.now(timezone("Asia/Kolkata")
                            ).strftime('%Y-%m-%d %H:%M:%S.%f')
    while int(ind_time[11:13])*60+int(ind_time[14:16]) < 556:
        ind_time = datetime.now(timezone("Asia/Kolkata")
                                ).strftime('%Y-%m-%d %H:%M:%S.%f')
    c_leg_tron, p_leg_tron, c_strike_b, p_strike_b, c_strike_intel, p_strike_intel = initial_leg_trades(
        x, option_chain, leg_tron)
    tron = int(prime_client['login'].margin()[0]['AvailableMargin']/140000)
    strangle_tron, strangle_c_strike, strangle_p_strike = initial_strangle_trades(
        option_chain, x, 0)
    exclusive_strike = 0
elif start == 1 and from_json == 'n':
    c_leg_tron = int(input('enter number of existing lots on call side buy: '))
    p_leg_tron = int(input('enter number of existing lots on put side buy: '))
    c_strike_b = int(input('enter the call bought strike: '))
    p_strike_b = int(input('enter the put bought strike: '))
    strangle_tron = int(input('strangle tron:  '))
    strangle_c_strike = int(input('enter strangle call strike: '))
    strangle_p_strike = int(input('enter strangle put strike: '))
    tron_intel = int(input(' tron_intel:  '))
    c_strike_intel = int(input('enter call_strike_intel: '))
    p_strike_intel = int(input('enter put_strike_intel: '))
    exclusive_strike = int(
        (strangle_c_strike == strangle_p_strike)*strangle_p_strike)
elif start == 1 and from_json == 'y':
    positions_record = json.load(open(client_name+'_suryabhai_positions.json'))
    c_leg_tron = positions_record['surya']['c_leg_tron']
    p_leg_tron = positions_record['surya']['p_leg_tron']
    c_strike_b = positions_record['surya']['c_strike_b']
    p_strike_b = positions_record['surya']['p_strike_b']
    strangle_tron = positions_record['strangle']['tron']
    strangle_c_strike = positions_record['strangle']['c_strike']
    strangle_p_strike = positions_record['strangle']['p_strike']
    tron_intel = positions_record['intel']['tron_intel']
    c_strike_intel = positions_record['intel']['c_strike_intel']
    p_strike_intel = positions_record['intel']['p_strike_intel']
    exclusive_strike = int(
        (strangle_c_strike == strangle_p_strike)*strangle_p_strike)

ind_time = datetime.now(timezone("Asia/Kolkata")
                        ).strftime('%Y-%m-%d %H:%M:%S.%f')
while int(ind_time[11:13])*60+int(ind_time[14:16]) < 556:
    ind_time = datetime.now(timezone("Asia/Kolkata")
                            ).strftime('%Y-%m-%d %H:%M:%S.%f')
while int(ind_time[11:13])*60+int(ind_time[14:16]) < 931:
    option_chain, x = data(week=0)
    ind_time = datetime.now(timezone("Asia/Kolkata")
                            ).strftime('%Y-%m-%d %H:%M:%S.%f')
    exclusive_strike, strangle_c_strike, strangle_p_strike, strangle_tron = strangle_adjustments(
        x, exclusive_strike, strangle_c_strike, strangle_p_strike, strangle_tron)
    exclusive_strike, strangle_tron = straddle_special_adjustment(
        exclusive_strike, x, strangle_tron)
    c_strike_b, p_strike_b, c_leg_tron, p_leg_tron, strangle_tron = surya(
        x, option_chain, c_strike_b, p_strike_b, c_leg_tron, p_leg_tron, exclusive_strike, strangle_c_strike, strangle_p_strike, strangle_tron)
    # c_strike_intel, p_strike_intel = intel_strike_mover(x, c_strike_intel, p_strike_intel, tron_intel, strangle_c_strike, strangle_p_strike, strangle_tron)
    if strangle_tron == 0:
        if exclusive_strike != 0:
            temp = np.sum(
                option_chain[option_chain['StrikeRate'] == exclusive_strike]['LastRate'])
            if temp > 66:
                exclusive_strike = 0
                strangle_tron, strangle_c_strike, strangle_p_strike = initial_strangle_trades(
                    option_chain, x, 0)
        elif exclusive_strike == 0:
            strangle_tron, strangle_c_strike, strangle_p_strike = initial_strangle_trades(
                option_chain, x, 0)
positions_json = {'strangle': {'c_strike': strangle_c_strike, 'p_strike': strangle_p_strike, 'tron': strangle_tron},
                  'surya': {'c_strike_b': c_strike_b, 'p_strike_b': p_strike_b, 'c_leg_tron': c_leg_tron, 'p_leg_tron': p_leg_tron},
                  'intel': {'c_strike_intel': c_strike_intel, 'p_strike_intel': p_strike_intel, 'tron_intel': tron_intel}}

print(positions_json)
out_file = open(client_name+'_suryabhai_positions.json', "w")
json.dump(positions_json, out_file, indent=6)
out_file.close()
# %%
