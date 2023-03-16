#%%
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
    f = open ('credentials.json', "r")
    creds = json.loads(f.read())
    client_list={}
    client_list[client]={'strategy':{},'login':{},'lots':{}}
    vinathi_cred = creds[client]["keys"]
    user = creds[client]["user"]
    passw = creds[client]["passw"]
    dob = creds[client]["dob"]
    client_list[client]['strategy']=strategies(user=user, passw=passw, dob=dob,cred=vinathi_cred)
    client_list[client]['login']=FivePaisaClient(email=user, passwd=passw, dob=dob,cred=vinathi_cred)
    client_list[client]['login'].login()
    #client_list[client]['lots']=round((client_list[client]['login'].margin()[0]['AvailableMargin']-200000)/180000)
    return client_list[client]
#client_name=input('enter the client name Eg: vinathi,bhaskar '

def order_button(exclusive_strike,type,lots):
    sleep(0.5)
    if "S" in type:
        type=type[:-1]+"B"
    elif "B" in type:
        type=type[:-1]+"S"
    exchange='BANKNIFTY'
    lot_size=25
    max_lots_per_order=36
    strike_difference=100
    if exclusive_strike==0:
        while True:
            try :
                expiry_timestamps=prime_client['login'].get_expiry("N",exchange).copy()
                current_expiry_time_stamp_weekly=int(expiry_timestamps['Expiry'][0]['ExpiryDate'][6:19])
                option_chain=pd.DataFrame(prime_client['login'].get_option_chain("N",exchange,current_expiry_time_stamp_weekly)['Options'])
                x=expiry_timestamps['lastrate'][0]['LTP']
                break
            except Exception :
                pass
        exclusive_strike=int(np.round(x/strike_difference)*strike_difference)
    else:
        while True:
            try :
                expiry_timestamps=prime_client['login'].get_expiry("N",exchange).copy()
                current_expiry_time_stamp_weekly=int(expiry_timestamps['Expiry'][0]['ExpiryDate'][6:19])
                option_chain=pd.DataFrame(prime_client['login'].get_option_chain("N",exchange,current_expiry_time_stamp_weekly)['Options'])
                x=expiry_timestamps['lastrate'][0]['LTP']
                break
            except Exception :
                pass
    if type=='CE_B':
        already_placed=0
        c_data=option_chain[option_chain['CPType']=='CE']
        c_scrip=int(c_data[c_data['StrikeRate']==exclusive_strike]['ScripCode'])
        temp2=lots
        temp=int(temp2/max_lots_per_order)
        end=temp2-temp*max_lots_per_order
        test_order = Order(order_type='B',exchange='N',exchange_segment='D', scrip_code =c_scrip, quantity=lot_size*max_lots_per_order, price=0 ,is_intraday=False,remote_order_id="tag")
        while temp>0:
            status=prime_client['login'].place_order(test_order)
            temp=temp-1 
            if status['Message']=='Success':
                already_placed+=max_lots_per_order
            sleep(0.5)
        if temp==0 and end!=0:
            test_order = Order(order_type='B',exchange='N',exchange_segment='D', scrip_code =c_scrip, quantity=lot_size*end, price=0 ,is_intraday=False,remote_order_id="tag")
            status=prime_client['login'].place_order(test_order)
            if status['Message']=='Success':
                already_placed+=end
        yet_to_place=lots-already_placed 
    if type=='PE_B':
        already_placed=0
        p_data=option_chain[option_chain['CPType']=='PE']
        p_scrip=int(p_data[p_data['StrikeRate']==exclusive_strike]['ScripCode'])
        temp2=lots
        temp=int(temp2/max_lots_per_order)
        end=temp2-temp*max_lots_per_order
        test_order = Order(order_type='B',exchange='N',exchange_segment='D', scrip_code =p_scrip, quantity=lot_size*max_lots_per_order, price=0 ,is_intraday=False,remote_order_id="tag")
        while temp>0:
            status=prime_client['login'].place_order(test_order) 
            temp=temp-1
            if status['Message']=='Success':
                already_placed+=max_lots_per_order
            sleep(0.5)
        if temp==0 and end!=0:
            test_order = Order(order_type='B',exchange='N',exchange_segment='D', scrip_code =p_scrip, quantity=lot_size*end, price=0 ,is_intraday=False,remote_order_id="tag")
            status=prime_client['login'].place_order(test_order) 
            if status['Message']=='Success':
                already_placed+=end
        yet_to_place=lots-already_placed
    if type=='CE_S':
        already_placed=0
        c_data=option_chain[option_chain['CPType']=='CE']
        c_scrip=int(c_data[c_data['StrikeRate']==exclusive_strike]['ScripCode'])
        temp2=lots
        temp=int(temp2/max_lots_per_order)
        end=temp2-temp*max_lots_per_order
        test_order = Order(order_type='S',exchange='N',exchange_segment='D', scrip_code =c_scrip, quantity=lot_size*max_lots_per_order, price=0 ,is_intraday=False,remote_order_id="tag")
        while temp>0:
            status=prime_client['login'].place_order(test_order) 
            temp=temp-1
            if status['Message']=='Success':
                already_placed+=max_lots_per_order
            sleep(0.5)
        if temp==0 and end!=0:
            test_order = Order(order_type='S',exchange='N',exchange_segment='D', scrip_code =c_scrip, quantity=lot_size*end, price=0 ,is_intraday=False,remote_order_id="tag")
            status=prime_client['login'].place_order(test_order) 
            if status['Message']=='Success':
                already_placed+=end
        yet_to_place=lots-already_placed
    if type=='PE_S':
        already_placed=0
        p_data=option_chain[option_chain['CPType']=='PE']
        p_scrip=int(p_data[p_data['StrikeRate']==exclusive_strike]['ScripCode'])
        temp2=lots
        temp=int(temp2/max_lots_per_order)
        end=temp2-temp*max_lots_per_order
        test_order = Order(order_type='S',exchange='N',exchange_segment='D', scrip_code =p_scrip, quantity=lot_size*max_lots_per_order, price=0 ,is_intraday=False,remote_order_id="tag")
        while temp>0:
            status=prime_client['login'].place_order(test_order) 
            temp=temp-1
            if status['Message']=='Success':
                already_placed+=max_lots_per_order
            sleep(0.5)
        if temp==0 and end!=0:
            test_order = Order(order_type='S',exchange='N',exchange_segment='D', scrip_code =p_scrip, quantity=lot_size*end, price=0 ,is_intraday=False,remote_order_id="tag")
            status=prime_client['login'].place_order(test_order) 
            if status['Message']=='Success':
                already_placed+=end
        yet_to_place=lots-already_placed
    return exclusive_strike,yet_to_place

def lots_drop(strike,side,yet_to_place):
    k=yet_to_place
    while yet_to_place>0:
        sleep(1)
        yet_to_place-=1
        xx,pending=order_button(strike,side,yet_to_place)
        if pending==0:
            break
    return k-yet_to_place

def data(week):
    exchange='BANKNIFTY'
    while True:
        expiry_timestamps=prime_client['login'].get_expiry("N",exchange).copy()
        current_expiry_time_stamp_weekly=int(expiry_timestamps['Expiry'][week]['ExpiryDate'][6:19])
        try :
            expiry_timestamps=prime_client['login'].get_expiry("N",exchange).copy()
            option_chain=pd.DataFrame(prime_client['login'].get_option_chain("N",exchange,current_expiry_time_stamp_weekly)['Options'])
            x=expiry_timestamps['lastrate'][0]['LTP']
            break
        except Exception :
            pass
    return option_chain,x

def indicator_(x,market_ripper,day_volume_indicator,day_market_ripper,rosetta,rosetta_ratio,oi_ratio,hightime,time,volume_ind):
    def node_out(input_,weights_bias):
        return np.tanh(weights_bias[0]*input_[0]+weights_bias[1]*input_[1]+weights_bias[2]*input_[2]+weights_bias[3]*input_[3]+weights_bias[4]*input_[4]+weights_bias[5]*input_[5]+weights_bias[6]*input_[6]+weights_bias[7]*input_[7]+weights_bias[8]*input_[8]+weights_bias[9])
    input_=[market_ripper,day_volume_indicator,day_market_ripper,hightime,oi_ratio,rosetta_ratio,rosetta,time/22440,volume_ind]
    x_=np.reshape(x,(82,len(input_)+1))
    index=0
    for j in range(0,9):
        A=[]
        for i in range(0,9):
            A+=[node_out(input_,x_[index])]
            index+=1
        input_=A
    ultimatum=node_out(input_,x_[index])
    final_indicator=np.array(ultimatum>0)+np.array(ultimatum<0)*-1
    return final_indicator



def blue_factor(option_chain,x):
    final_chain=option_chain[(option_chain['StrikeRate']>x-1000) & (option_chain['StrikeRate']<x+1000)]
    p=final_chain[final_chain['CPType']=='PE']
    c=final_chain[final_chain['CPType']=='CE']
    strikes=p['StrikeRate']
    p_lastrates=p['LastRate']
    c_lastrates=c['LastRate']
    f_p = interpolate.interp1d(strikes, p_lastrates,kind='quadratic')
    f_c = interpolate.interp1d(strikes, c_lastrates,kind='quadratic')
    return (f_p(x)+f_c(x))/2


def options_indicator(option_chain,x,cv,pv,earlier_cv,earlier_pv,main_cv,main_pv,day_coi,day_poi,c_oi,p_oi):
    ind_time = datetime.now(timezone("Asia/Kolkata")).strftime('%Y-%m-%d %H:%M:%S.%f')
    ce_data=option_chain[option_chain['CPType']=='CE']
    pe_data=option_chain[option_chain['CPType']=='PE']
    p_strikerates=np.array(list(pe_data['StrikeRate']))
    c_strikerates=np.array(list(ce_data['StrikeRate']))
    p_lastrate=np.array(list(pe_data['LastRate']))
    c_lastrate=np.array(list(ce_data['LastRate']))
    p_openinterest=np.array(list(pe_data['OpenInterest']))
    c_openinterest=np.array(list(ce_data['OpenInterest']))
    p_volume=np.array(list(pe_data['Volume']))
    c_volume=np.array(list(ce_data['Volume']))
    p_volume_change=p_volume-earlier_pv
    c_volume_change=c_volume-earlier_cv
    cv_temp=np.sum(np.multiply(c_volume_change,c_lastrate))
    pv_temp=np.sum(np.multiply(p_volume_change,p_lastrate))
    coi_temp=np.sum(np.multiply(c_openinterest,c_lastrate))
    poi_temp=np.sum(np.multiply(p_openinterest,p_lastrate))
    day_coi+=coi_temp
    day_poi+=poi_temp
    c_oi+=coi_temp
    p_oi+=poi_temp
    uu=c_oi/p_oi
    day_uu=day_coi/day_poi
    oi_davat=((2*uu*uu)/(1+uu*uu))-1
    day_oi_davat=((2*day_uu*day_uu)/(1+day_uu*day_uu))-1
    cv=cv+cv_temp
    pv=pv+pv_temp
    cc=cv/(pv+0.1)
    v_ind=((2*cc*cc)/(1+cc*cc))-1

    main_cv=main_cv+cv_temp
    main_pv=main_pv+pv_temp
    main_cc=main_cv/(main_pv+0.1)
    main_v_ind=((2*main_cc*main_cc)/(1+main_cc*main_cc))-1


    earlier_pv=p_volume
    earlier_cv=c_volume
    average_p_strike=np.dot(p_strikerates,p_openinterest)/np.sum(p_openinterest)
    average_c_strike=np.dot(c_strikerates,c_openinterest)/np.sum(c_openinterest)
    p1=x-average_p_strike
    c1=average_c_strike-x
    oi_ratio=np.sum(p_openinterest)/np.sum(c_openinterest)
    i=np.array(pe_data['StrikeRate'])[0]
    end=np.array(pe_data['StrikeRate'])[-1]
    ss=np.array(pe_data['StrikeRate'])
    def loss_function(v):
        init_pe=np.dot(p_lastrate,p_openinterest)
        init_ce=np.dot(c_lastrate,c_openinterest)
        tmax=ss-v[0]
        tmax[tmax<0]=0
        tmin=v[0]-ss
        tmin[tmin<0]=0
        end_pe=np.dot(p_openinterest,tmax)
        end_ce=np.dot(c_openinterest,tmin)
        data=init_ce-end_ce-init_pe+end_pe
        return abs(data)
    a,b=pso(func=loss_function,lb=[i],ub=[end],minfunc=0.1)
    x1=x-np.round_(a[0],1)
    factor5=blue_factor(option_chain,x)
    pp=p_lastrate[np.multiply(p_lastrate!=0, p_openinterest!=0)]
    po=p_openinterest[np.multiply(p_lastrate!=0, p_openinterest!=0)]
    cp=c_lastrate[np.multiply(c_lastrate!=0, c_openinterest!=0)]
    co=c_openinterest[np.multiply(c_lastrate!=0, c_openinterest!=0)]

    a1=np.dot(np.array(pp),np.array(po))
    a2=np.dot(np.array(cp),np.array(co))
    aa=a1/a2
    hightime_indicator= ((2*(c1/p1)*(c1/p1))/(1+(c1/p1)*(c1/p1)))-1
    rosetta_indicator=x1/factor5
    rosetta_ratio_indicator=((2*aa*aa)/(1+aa*aa))-1
    oi_ratio_indicator=((2*oi_ratio*oi_ratio)/(1+oi_ratio*oi_ratio))-1
    xopt=[ 1.83470370e+01,  1.45728705e+01,  1.41472216e+01, -6.88230338e+00,
       -8.75698332e+00, -2.06859319e+01, -1.18086614e+01,  1.39622014e+01,
       -5.75393989e+00,  4.73370187e+00,  2.48271771e+01, -1.11266281e+01,
       -9.20013764e+00,  1.37846619e+01, -1.92582248e+01, -2.34012332e+01,
        9.61221910e+00,  1.03919993e+01, -3.48786893e+00,  2.12263036e+01,
        1.43668658e+01, -2.01223757e+01, -2.92780384e+01, -4.36814770e+00,
        1.88358468e+01,  9.80858384e+00,  2.85297812e+01, -3.86630553e+00,
       -1.46802026e+01, -3.00000000e+01,  2.29923601e+00, -8.22205952e+00,
        1.51065500e+01, -1.97383607e+01, -2.11078725e-02, -3.00000000e+01,
        1.67016251e+01,  1.35856612e+01, -1.10747763e+01, -6.40618409e+00,
        6.08068368e+00,  1.00231352e+01,  1.21616648e+01, -1.24424641e+01,
       -9.18686595e+00, -1.50132096e+01,  1.89310064e+01, -1.01666771e+00,
        4.64600937e-01,  2.11663819e+01,  1.94336698e+01, -4.09104894e+00,
        1.10963430e+00, -2.39419175e+01,  2.83035181e+01,  7.24378220e+00,
        2.29126589e+00,  7.01194816e+00, -2.49591398e+01, -1.66721431e+01,
        5.10303950e+00, -2.39198189e+01, -2.42762850e+01,  2.87040165e+01,
        1.70968196e+01,  2.96541493e+01,  1.37816069e+01, -3.55672188e+00,
       -5.62280851e+00, -1.62093867e+01, -5.32768067e+00,  2.20327409e+00,
        8.98977519e+00,  9.52593374e+00,  7.63361582e-02, -2.23340529e+01,
       -6.85167183e+00,  1.91426134e+01,  2.34463289e+01, -2.70711941e+01,
       -1.29688855e+01,  5.62758599e+00,  1.91451240e+00, -2.67592467e+01,
        1.89595664e+01, -3.46547357e+00, -3.00000000e+01, -5.65046053e+00,
        4.62151554e+00, -9.26513016e-01, -1.18956969e+01, -1.14880137e+01,
        1.67321031e+01,  2.16781388e+01, -6.77749242e+00, -6.17643292e+00,
        1.33628813e+01, -5.58527286e+00,  5.21577736e+00, -2.59235409e+01,
       -3.43396094e+00,  1.13038600e+01, -2.95142304e+00, -1.98564894e+01,
       -2.68934843e+01, -3.67507736e+00, -6.30856684e+00, -8.57027929e+00,
        8.52857414e+00,  7.28818577e+00, -3.68080635e+00, -1.06888580e+01,
        3.67433451e+00,  9.08843641e+00, -8.78509939e+00,  1.36408310e+01,
       -1.72001894e+01,  2.87315006e+00, -2.00643525e+01,  2.34675406e+01,
       -1.43116305e+00, -6.07203957e+00,  4.79124490e-01, -1.81128338e+01,
       -1.84252055e+01, -1.60252249e+01,  2.07295221e+00,  2.96458600e+01,
       -1.23775800e+01,  2.55807935e+01, -4.84929811e+00,  1.25657552e+01,
       -2.04851817e+01, -1.74978558e+01,  1.58041535e+01,  2.27540734e+01,
        1.92577604e+01,  7.74395614e-01, -2.58280100e+01, -4.79056848e+00,
       -1.15375373e+01,  5.68246453e+00, -1.65025062e+01, -1.91208771e+01,
       -2.72862773e+01, -1.64710603e+01, -1.28148676e+01, -5.18744239e+00,
       -5.40964725e+00, -1.17708198e+01,  5.85225734e+00,  2.46051951e+01,
        1.11464446e+01, -3.24666944e+00, -2.54832266e+01, -1.16593123e+01,
       -4.24061349e+00, -4.33543882e+00, -2.12931276e-01,  5.33841483e+00,
       -1.71679469e+01, -4.66474235e+00, -1.20721823e+01, -1.81359121e+01,
        3.16593465e+00, -2.28100234e+00,  1.27507981e+01, -1.69475628e+01,
        1.25143598e+01, -1.03902498e+01,  2.25861816e+00,  1.85445654e+00,
        1.22651143e+01,  2.96868018e+00,  1.51202655e+01,  2.45601485e+01,
       -6.47109955e+00,  1.18274274e+01,  1.76322340e+01, -1.47131295e+01,
        2.49236830e+01, -2.75229008e+01, -1.25792537e+00,  1.84466703e+01,
       -2.08613120e+01, -7.10574799e-01,  1.55689891e+01, -5.14042339e-01,
       -1.65827680e+01, -7.38615206e+00, -2.37436860e+01, -5.21631342e+00,
       -1.28292910e+01, -2.00526304e+01, -1.64976777e+01,  4.53889264e-01,
       -9.36039754e-01, -1.88234259e+01, -1.00436184e+01, -9.98277260e+00,
        5.64951420e+00, -2.28866826e+01, -5.36005318e+00,  1.28602123e+01,
        3.87781939e+00, -2.52151091e+01,  5.45969310e+00, -1.30783108e+01,
        1.29529589e+01,  1.27107714e+00, -3.26528469e+00,  2.92667839e+00,
        1.79410779e+01,  9.02835517e-01,  5.08809498e-01, -2.47336474e+00,
       -1.85937733e+01, -9.14033269e+00, -6.55242669e+00,  1.50856310e+01,
       -3.63214494e+00, -1.70461735e+01, -2.23662312e-01,  2.72651363e+00,
        3.00250627e+00, -1.03040419e+01,  6.76130934e+00,  8.10814997e+00,
        1.48325848e+01,  8.20296765e+00,  1.52680900e+01,  1.49065556e+00,
       -2.09173582e+01,  1.27290974e+01,  1.87980032e+01, -2.87349606e+01,
        1.05223440e+01,  2.61867780e+01, -5.55174954e+00, -4.99270110e+00,
       -1.00653469e+01,  2.25519604e+01, -1.13700720e+01, -1.17423350e+00,
       -1.87099320e+00,  7.46502765e+00, -2.67369059e+01,  1.88474464e+01,
       -4.44463013e+00, -6.01820606e+00, -1.87348720e+00, -7.02443843e+00,
       -7.85910430e+00, -1.69627428e+01, -1.57506185e+01, -2.10005143e+01,
        6.52347854e+00,  1.43595507e+01, -1.44610907e+01, -5.08982955e+00,
        6.14063665e+00,  1.60008830e+01,  2.64130742e+01,  1.39064292e+01,
       -5.41684585e+00,  2.82075500e+00,  1.12788112e+01, -5.07919357e-01,
        6.41463736e+00,  1.70462151e+00,  2.13742248e+01, -1.74868698e+00,
        4.93957211e+00, -1.61020059e+01,  2.02320102e+01,  3.14638576e+00,
        1.80004330e+00, -3.10229425e+00, -2.48334390e+01, -2.48882337e+01,
       -7.81376728e+00, -2.49527338e+01,  1.93986518e+01,  1.92887763e+01,
       -8.41620551e+00,  1.65374785e+01,  7.80214694e+00,  1.18196790e+01,
        1.25140320e+01,  1.65136196e+01,  1.95613602e+01,  6.50630372e+00,
        4.55048564e+00,  1.04071300e+01,  1.81345181e+01, -9.77205818e+00,
       -6.33343339e+00,  1.66763899e+01, -7.78457275e+00,  9.41761730e+00,
        1.01776546e+01,  6.68203344e+00,  2.32057810e+01,  9.12378722e+00,
        2.67661699e+00, -1.97550662e+01,  1.02593090e+01, -1.18382915e+01,
       -6.98399899e+00,  1.52654918e+01, -2.27301831e+01, -2.45850783e+01,
        8.03622702e+00, -2.01945947e+00, -8.16504049e+00,  3.81581978e+00,
       -3.96023276e-01,  5.02865552e+00,  1.88032683e+01, -2.78783987e+01,
       -8.54653646e+00, -1.12595728e+00, -1.16211955e+01,  3.38045519e+00,
        9.47166326e+00,  1.23495019e+01, -3.13689481e+00, -6.36458165e+00,
        1.07820415e+01,  1.90361413e+00,  1.40395873e+01, -3.34411759e+00,
        8.38648889e+00,  2.38942068e+01,  2.67700292e+01,  1.66147195e+01,
        4.68114575e+00,  8.61673145e+00, -2.46970786e+00,  3.38054841e+00,
       -7.53296750e-01,  9.18714213e+00,  7.38544797e+00, -6.72502466e+00,
       -8.86050099e+00, -1.70117131e+00,  1.41547592e+01, -2.01349911e+01,
        2.50262235e+00, -1.07698788e+01,  2.16695817e+01,  1.55273509e+01,
        6.62017712e+00, -5.45605889e+00, -4.93735428e+00, -8.77898540e+00,
        1.40297850e+01, -8.85927919e+00, -6.14513004e+00,  1.40151128e+01,
        3.29179154e+00, -1.48204362e+01, -1.62090327e+01, -2.21136974e+01,
        1.45317502e+01,  1.59894481e+01, -3.01737140e+00, -1.21649464e+01,
        9.79158195e-01,  2.77181337e+01, -1.56618836e+01,  7.32993408e+00,
        1.54911660e+01,  7.58169967e+00,  5.54334777e+00, -1.23333115e+01,
       -1.27906187e+00, -9.97004066e+00,  1.62923977e+01, -2.13503570e-01,
       -8.68758476e-01,  2.07496226e+01, -3.18243475e+00, -7.46262352e+00,
       -7.81876663e+00, -1.16142374e+01,  2.20456986e+01, -1.19061926e+00,
       -9.92263676e+00,  2.44191796e+01, -2.45854192e+01,  2.26484430e+01,
        9.46034345e+00, -2.28228337e+00,  1.30846369e+01,  1.12475326e+01,
       -4.33064542e+00,  1.03879293e+01,  1.49007996e+01,  4.48159071e-01,
       -7.39785932e+00, -2.20444170e+00, -5.27180976e+00, -8.72522562e+00,
       -6.15349521e+00, -2.09506774e+00,  3.41134806e+00,  2.72244488e+01,
        4.51808479e+00,  1.13927909e+01, -8.09934037e+00, -1.67283246e+00,
        8.17723870e-01, -9.51795387e+00,  7.12363892e+00,  1.40538274e+01,
       -9.88751139e+00, -1.23842944e+01, -2.07932361e+01,  1.70854693e+01,
       -8.10197684e+00,  1.49190047e+01, -9.36949885e-01, -1.74572890e+00,
        6.22625735e-01,  1.72367239e+01, -6.70163424e+00, -4.72214064e+00,
       -1.03793235e+00,  1.28289314e+01, -9.67403223e+00, -2.51423933e+01,
       -1.08649616e+01,  3.00000000e+01, -2.36148766e+01,  1.25021964e+01,
       -1.93988930e+00,  3.16043771e+00, -2.21950349e+01,  9.98995892e+00,
       -1.69643624e+01, -2.45989294e+01,  2.48141358e+01, -2.76572568e+00,
       -1.56170852e+01,  1.25279647e+01,  2.07662831e+00,  1.03141571e+01,
       -9.45040454e+00, -3.02101559e+00, -1.57019351e+01, -1.36078747e+01,
       -1.92301804e+01,  2.12571749e+01,  1.47847193e+01, -2.95973752e+00,
       -1.91716652e+01, -4.92077664e-01,  1.14839866e+01,  1.17975640e+00,
        2.41749706e+01,  4.49943967e+00, -1.79775154e+01,  3.97449971e+00,
       -7.97483880e+00,  9.99411053e+00, -1.04109197e+01, -1.00519112e+01,
        1.67393003e+01, -1.74175380e+01, -1.11127808e+01, -2.03425498e+00,
        2.94816732e-01,  9.30765399e+00, -1.59220826e+01, -1.38557705e+01,
        2.29571208e+00,  5.64840922e+00, -5.93326924e+00, -9.88087851e+00,
        4.52711912e+00,  2.06418479e+01,  4.29062216e+00, -1.00552613e+01,
        1.01678339e+01,  9.08533507e+00,  1.94053295e+01, -1.59222772e+01,
        5.11640314e+00, -2.97451005e+01,  1.08763776e+01,  1.06929629e+00,
        9.46177099e+00, -1.98891183e+00, -9.77466866e+00, -3.62536238e+00,
        2.77064145e+00,  1.54450822e+01,  2.12674618e+01, -7.46519721e+00,
        3.96122510e+00, -5.34778751e-01, -1.53627217e+01, -2.98060985e+01,
       -6.60382121e+00,  7.90737872e+00,  2.58165566e+01,  5.80123601e+00,
       -1.41547404e+01,  1.04595326e+01,  1.32736379e+00,  1.22214581e+01,
        2.69362918e+01, -7.02744379e-01, -2.26912074e+01, -4.76310820e+00,
       -1.28806442e+00, -5.31249684e+00, -7.33419815e+00, -2.09105485e+01,
       -8.08748774e+00,  1.79220159e+01, -2.10510940e+01, -5.96544400e+00,
        1.61184968e+01, -8.45430620e+00,  2.59233639e+01,  1.66649531e+01,
        2.41719599e+01,  1.21442943e-01, -1.10133024e+01,  2.28837733e+01,
        3.00000000e+01,  1.14550063e+01, -8.74314222e+00,  6.74193693e+00,
        5.02717483e+00,  9.47970027e+00, -1.11193940e+00,  9.50541989e+00,
       -3.29255964e+00, -7.07756543e+00,  9.73738647e+00, -3.21280985e-01,
       -3.16731149e+00,  1.16429211e+01, -1.68520720e+01, -4.64876612e+00,
       -4.27813383e+00, -2.83519765e+01,  3.97856671e+00,  2.64947743e+01,
        3.29230801e+00, -7.31948324e+00,  4.85919738e+00, -9.09089113e+00,
        1.97156710e+01,  1.36428237e+01,  8.55950812e+00, -5.19954602e+00,
       -1.85450510e+01, -5.83929971e+00, -1.07830852e+01, -1.40244548e+01,
       -1.36206659e+01, -1.40469537e+01, -2.18673459e+01,  2.52131995e+01,
        1.23040721e+01, -1.78176636e+01, -9.40547352e+00, -2.18073125e+01,
       -1.29022276e+01, -1.41593286e+01, -1.01127956e+00, -2.16203232e+01,
        1.67804755e+01, -7.51942691e+00, -1.47451839e+01, -1.28557143e+01,
       -1.79878107e+01,  2.81292011e+01,  1.93544188e+01, -1.05496741e+01,
       -7.92964879e+00,  2.46408677e+01,  6.22675295e+00,  2.20151234e+01,
        4.11000765e+00, -2.33007218e+00, -8.33148768e+00,  1.46385398e+01,
       -1.76191519e+01,  1.98130752e+01,  8.72366081e+00, -1.93637012e+01,
       -1.66403229e+01,  2.42661579e+01,  1.18733056e+01,  6.44950633e+00,
       -3.03017789e-01, -1.46782995e+01,  1.67803654e+01, -6.54356269e+00,
        3.18601657e+00,  7.22178432e+00, -1.83666643e+01, -1.00768265e+01,
        1.80335235e+01, -1.01952069e+01, -6.59579329e+00,  3.14553973e+00,
       -5.42215699e+00,  9.64644893e-01, -2.01813224e+01,  9.29732575e+00,
       -4.55492551e+00, -2.44674105e+01, -1.99763283e+01,  6.59423014e+00,
       -5.38276973e+00,  9.94294400e+00,  1.32011676e+01, -1.34240850e+01,
        9.35200012e+00, -1.82526498e+01, -4.33682828e+00,  1.72890326e+01,
        2.05463954e+01, -1.08753688e+01, -3.10791821e+00, -5.38255110e+00,
        7.89501082e-02,  4.50851955e+00,  1.48288498e+01, -1.67401809e+01,
       -9.06420519e+00,  2.48691430e+01,  1.17402037e+01, -2.21761440e+01,
       -2.01362649e+01, -2.36296314e+01,  1.53262159e+01,  1.11075962e+01,
        2.05491235e+01, -1.79991938e+01,  1.97358876e+01,  8.14074478e+00,
        5.84496912e+00, -1.46318881e+01,  7.55350513e+00, -4.57499008e+00,
       -1.79988019e+01, -1.97149242e+01,  1.15758797e+01,  1.56382627e+01,
        5.40615411e+00,  1.19752930e+00, -1.56233899e+01,  1.63099721e+01,
        8.96440227e+00,  2.85838972e+01,  1.96123987e+00, -1.44663331e+01,
        4.64670037e+00,  2.88927851e-01,  1.54145158e+01,  2.24342736e+01,
       -1.16615566e+01,  2.15826028e+01,  1.23176891e+01, -1.92752350e+01,
       -1.03993969e+01,  1.12469941e+01, -1.23222782e+01, -1.15402490e+01,
       -2.88233883e+01, -1.10414942e+01,  1.64426004e+01,  1.50227810e-01,
       -2.42919146e+01,  9.41393304e+00, -8.63257917e+00,  1.79313537e+01,
       -1.36480830e+01,  1.45123445e+01,  2.77446395e+00, -4.01682429e-01,
       -1.53738919e+01,  5.72396337e-01, -3.54972784e+00, -1.99930788e+01,
       -9.22333369e+00,  2.31191373e+01, -1.26699045e+01, -6.94377426e+00,
       -2.06914393e+01,  1.65227673e+01, -1.76781535e+01,  2.80885549e+00,
       -2.83942205e+01,  3.91149205e+00, -1.88794403e+01,  2.06415836e+01,
        2.62890807e+01,  1.48338951e+01,  3.94217445e+00, -2.11299673e+01,
        8.67763672e+00,  1.42254526e+01, -1.18800287e+01, -5.33825838e+00,
       -1.76999624e+01, -1.49246519e+01, -1.06980697e+00,  1.21975990e+01,
        1.29526903e+01,  1.57076698e+01,  6.83138034e+00,  3.27725302e+00,
        8.09869165e+00, -2.13334757e+01, -7.04527961e+00,  1.77731125e-01,
        6.17487068e+00, -5.58259684e+00,  2.68876105e+01,  5.62638530e+00,
       -2.72422137e+01, -4.77613018e+00, -1.19607440e+00, -1.05468645e+01,
       -2.29271193e+01, -2.31078595e+01, -1.07597988e+01, -8.04839018e+00,
       -9.84791403e+00,  2.39485158e+01,  8.14301430e+00, -2.08460202e+01,
        7.94696760e+00, -1.13300943e+01,  1.90334639e+01,  5.12037049e+00,
        5.26524656e+00, -3.91680597e-01,  9.50011138e-01, -1.77724947e+01,
        3.32069273e+00, -9.19633883e+00, -5.87311072e+00, -9.48478904e+00,
        1.65976247e+00, -3.25571553e+00, -2.35897448e+01,  7.47045363e+00,
        1.03688999e+01, -6.41868587e+00, -1.39662297e+01,  2.33805281e+00,
        3.69727527e+00,  2.00680835e+01,  1.04719995e+01, -6.19538373e+00,
        7.38632583e+00,  1.53710533e+01, -1.31427089e+01,  4.13455160e+00,
       -2.52205330e+01,  7.52673608e+00, -1.74031251e+01, -1.98772329e+01,
       -8.34391071e+00, -5.91201069e+00, -3.52697811e+00,  8.03928154e+00,
        1.69169571e+01,  1.33765145e+01,  3.10552751e+00,  3.34352973e+00,
        1.28299911e+00,  1.18133115e+01, -2.06998514e+01,  1.89190421e+01,
        1.75352137e+01, -1.27644292e+01, -1.63356223e+01, -1.33512609e+01,
       -2.25823874e+00, -1.80188192e+01,  7.90608958e-01, -1.73910180e+01,
       -3.80538985e+00,  5.07047268e+00,  2.26795356e+01,  1.11935863e+01,
       -4.50283150e+00,  1.00752711e+01, -7.02204793e+00,  1.86882737e+01,
        2.82441159e+01,  1.12244540e+01, -9.90088403e+00, -2.62243897e+01,
       -9.99865447e+00,  2.16729651e+01,  1.73336877e+01, -1.20438898e+01,
       -1.98962367e+01, -9.87347183e-01,  9.04527577e+00,  1.41345948e+00,
       -1.43600967e+01, -2.12974356e+01,  1.87448244e+01,  5.04432340e+00,
        3.69295422e+00,  1.25410184e+01, -1.50000229e+01,  1.74943443e+00]
    time=int(ind_time[11:13])*60*60+int(ind_time[14:16])*60-33300
    final=indicator_(xopt,oi_davat,v_ind,day_oi_davat,rosetta_indicator,rosetta_ratio_indicator,oi_ratio_indicator,hightime_indicator,time,main_v_ind)
    return  final,cv,pv,earlier_cv,earlier_pv,main_cv,main_pv,day_coi,day_poi,c_oi,p_oi


def options_vwap_json(option_chain,calloptions_vwap,putoptions_vwap,primary_oi,x,prev_final_c_shape,prev_final_p_shape):
    stoploss=19
    ce_data=option_chain[option_chain['CPType']=='CE']
    pe_data=option_chain[option_chain['CPType']=='PE']
    ce_data_prime=primary_oi[primary_oi['CPType']=='CE']
    pe_data_prime=primary_oi[primary_oi['CPType']=='PE']
    taken_c=np.multiply((np.array(ce_data['StrikeRate'])>x-50), (np.array(ce_data['StrikeRate'])<x+600))
    taken_p=np.multiply((np.array(pe_data['StrikeRate'])>x-600), (np.array(pe_data['StrikeRate'])<x+50))
    ind_time = datetime.now(timezone("Asia/Kolkata")).strftime('%Y-%m-%d %H:%M:%S.%f')
    t=(int(ind_time[11:13])*60+int(ind_time[14:16])-555)/15
    c_lastrate=np.array(ce_data['LastRate'])+t
    p_lastrate= np.array(pe_data['LastRate'])+t
    c_volumes=  np.array(ce_data['Volume'])
    p_volumes=  np.array(pe_data['Volume'])
    c_oi=  np.array(ce_data['OpenInterest'])
    p_oi=  np.array(pe_data['OpenInterest'])
    prev_c_lastrate=    np.array(calloptions_vwap['LastRate'])
    prev_p_lastrate=    np.array(putoptions_vwap['LastRate'])
    prev_c_volumes=     np.array(calloptions_vwap['Volume'])
    prev_p_volumes=     np.array(putoptions_vwap['Volume'])
    primary_c_oi=  np.array(ce_data_prime['OpenInterest'])
    primary_p_oi=  np.array(pe_data_prime['OpenInterest'])
    c_shape=np.multiply((c_oi-primary_c_oi)>0,taken_c)
    p_shape=np.multiply((p_oi-primary_p_oi)>0,taken_p)
    c_net=np.multiply(c_volumes-prev_c_volumes,c_lastrate)
    p_net=np.multiply(p_volumes-prev_p_volumes,p_lastrate)
    c_volumes[c_volumes==0]=1
    p_volumes[p_volumes==0]=1
    call_vwap=np.multiply((c_net+np.multiply(prev_c_lastrate,prev_c_volumes)),1/c_volumes)
    put_vwap=np.multiply((p_net+np.multiply(prev_p_lastrate,prev_p_volumes)),1/p_volumes)
    calloptions_vwap=ce_data[['StrikeRate','LastRate','Volume']].copy()
    putoptions_vwap=pe_data[['StrikeRate','LastRate','Volume']].copy()
    calloptions_vwap['LastRate']=call_vwap    
    calloptions_vwap['Volume']=ce_data['Volume']
    putoptions_vwap['LastRate']=put_vwap    
    putoptions_vwap['Volume']=pe_data['Volume']
    final_c_shape=np.multiply(np.sign(((c_lastrate-call_vwap)<-stoploss)*-1),c_shape)
    final_p_shape=np.multiply(np.sign(((p_lastrate-put_vwap)<-stoploss)*-1),p_shape)
    to_correct_c_shape=np.multiply(np.sign(((c_lastrate-call_vwap)<0)*-1),c_shape)
    to_correct_p_shape=np.multiply(np.sign(((p_lastrate-put_vwap)<0)*-1),p_shape)
    if len(prev_final_p_shape)==0:
        prev_final_c_shape=final_c_shape
        prev_final_p_shape=final_p_shape
    final_c_shape=final_c_shape-np.multiply(to_correct_c_shape-final_c_shape,prev_final_c_shape)
    final_p_shape=final_p_shape-np.multiply(to_correct_p_shape-final_p_shape,prev_final_p_shape)
    call_seller=ce_data[['StrikeRate']].copy()
    call_seller['indicator']=final_c_shape
    put_seller=pe_data[['StrikeRate']].copy()
    put_seller['indicator']=final_p_shape
    return calloptions_vwap,putoptions_vwap,put_seller,call_seller,final_c_shape,final_p_shape

def get_strike_from_scrip(scripcode,exchange):
    if exchange=='BANKNIFTY':
        option_chain,a1=data(0)
    k1=option_chain[option_chain['ScripCode']==scripcode]
    return int(k1['StrikeRate'])


def buy_kickoff(start,indicator,earlier_indicator,exclusive_strike,tron):
    if abs(indicator-earlier_indicator)==2:
        indicator=0
    if start==0:
        s=indicator
        if s>0:
            exclusive_strike,yet_to_place=order_button(exclusive_strike,'CE_S',tron)
            tron-=lots_drop(exclusive_strike,'CE_S',yet_to_place)
            start=1
        elif s<0:
            exclusive_strike,yet_to_place=order_button(exclusive_strike,'PE_S',tron)
            tron-=lots_drop(exclusive_strike,'PE_S',yet_to_place)
            start=1
    elif start==1:
        if earlier_indicator==0 and indicator==1:
            exclusive_strike,yet_to_place=order_button(exclusive_strike,'CE_S',tron)
            tron-=lots_drop(exclusive_strike,'CE_S',yet_to_place)

        if earlier_indicator==0 and indicator==-1:
            exclusive_strike,yet_to_place=order_button(exclusive_strike,'PE_S',tron)
            tron-=lots_drop(exclusive_strike,'PE_S',yet_to_place)
        if earlier_indicator==-1 and indicator==0:
            exclusive_strike,yet_to_place=order_button(exclusive_strike,'PE_B',tron)
        if earlier_indicator==1 and indicator==0:
            exclusive_strike,yet_to_place=order_button(exclusive_strike,'CE_B',tron)

    return exclusive_strike,tron,start,indicator


def clear_open_positions():

    S=pd.DataFrame(prime_client['login'].positions())
    if len(S)==0:
        return 0
    if len(S[S['NetQty']!=0])!=0:
        for i in range(0,len(S)):
            if ('BANKNIFTY' in S['ScripName'].iloc[i]) and S['NetQty'].iloc[i]!=0:
                if S['NetQty'].iloc[i]<0 and ('PE' in S['ScripName'].iloc[i]):
                    order_button(get_strike_from_scrip(S['ScripCode'].iloc[i],'BANKNIFTY'),'PE_S',int(abs(S['NetQty'].iloc[i])/25))
                elif S['NetQty'].iloc[i]<0 and ('CE' in S['ScripName'].iloc[i]):
                    order_button(get_strike_from_scrip(S['ScripCode'].iloc[i],'BANKNIFTY'),'CE_S',int(abs(S['NetQty'].iloc[i])/25))
                elif S['NetQty'].iloc[i]>0 and ('CE' in S['ScripName'].iloc[i]):
                    order_button(get_strike_from_scrip(S['ScripCode'].iloc[i],'BANKNIFTY'),'CE_B',int(abs(S['NetQty'].iloc[i])/25))
                elif S['NetQty'].iloc[i]>0 and ('PE' in S['ScripName'].iloc[i]):
                    order_button(get_strike_from_scrip(S['ScripCode'].iloc[i],'BANKNIFTY'),'PE_B',int(abs(S['NetQty'].iloc[i])/25))
        S=pd.DataFrame(prime_client['login'].positions())
        if len(S[S['NetQty']!=0])!=0:
            return clear_open_positions()
        elif len(S[S['NetQty']!=0])==0:
            return 0
    elif len(S[S['NetQty']!=0])==0:
        return 0


#%%
client_name = input('enter the client name: ')
tron=int(input('enter the number of lots at each strike'))
betatron=tron*4
prime_client=client_login(client=client_name)
option_chain,x=data(week=0)
primary_oi=option_chain
ce_data=option_chain[option_chain['CPType']=='CE']
pe_data=option_chain[option_chain['CPType']=='PE']
calloptions_vwap=ce_data[['StrikeRate','LastRate','Volume']].copy()
putoptions_vwap=pe_data[['StrikeRate','LastRate','Volume']].copy()
cv,pv,day_coi,day_poi=0,0,0,0
a=datetime.today().weekday()
if a==4:
    main_cv,main_pv,c_oi,p_oi=0,0,0,0
else:
    indicator_json=json.load(open('indicator_variables.json'))
    main_cv,main_pv,c_oi,p_oi=indicator_json['main_cv'],indicator_json['main_pv'],indicator_json['c_oi'],indicator_json['p_oi']


#start=int(input('enter 0 if starting the strategy for the first time, else 1 :  '))
#%%
ind_time = datetime.now(timezone("Asia/Kolkata")).strftime('%Y-%m-%d %H:%M:%S.%f')
while int(ind_time[11:13])*60+int(ind_time[14:16])<556:
    ind_time = datetime.now(timezone("Asia/Kolkata")).strftime('%Y-%m-%d %H:%M:%S.%f')
option_chain,x=data(week=0)
calloptions_vwap,putoptions_vwap,put_seller,call_seller,prev_final_c_shape,prev_final_p_shape=options_vwap_json(option_chain,calloptions_vwap,putoptions_vwap,primary_oi,x,[],[])
e_put_seller=put_seller['indicator']*0
e_call_seller=call_seller['indicator']*0
x_prime=x
ce_data=option_chain[option_chain['CPType']=='CE']
pe_data=option_chain[option_chain['CPType']=='PE']
earlier_pv=np.array(list(pe_data['Volume']))
earlier_cv=np.array(list(ce_data['Volume']))
cv,pv=0,0
earlier_indicator,cv,pv,earlier_cv,earlier_pv,main_cv,main_pv,day_coi,day_poi,c_oi,p_oi=options_indicator(option_chain,x,cv,pv,earlier_cv,earlier_pv,main_cv,main_pv,day_coi,day_poi,c_oi,p_oi)
start=0
exclusive_strike=0
while int(ind_time[11:13])*60+int(ind_time[14:16])<921:
    ind_time = datetime.now(timezone("Asia/Kolkata")).strftime('%Y-%m-%d %H:%M:%S.%f')
    option_chain,x=data(week=0)
    B,cv,pv,earlier_cv,earlier_pv,main_cv,main_pv,day_coi,day_poi,c_oi,p_oi=options_indicator(option_chain,x,cv,pv,earlier_cv,earlier_pv,main_cv,main_pv,day_coi,day_poi,c_oi,p_oi)
    exclusive_strike,betatron,start,earlier_indicator=buy_kickoff(start,B,earlier_indicator,exclusive_strike,betatron)
    calloptions_vwap,putoptions_vwap,put_seller,call_seller,prev_final_c_shape,prev_final_p_shape=options_vwap_json(option_chain,calloptions_vwap,putoptions_vwap,primary_oi,x_prime,prev_final_c_shape,prev_final_p_shape)
    final_put_seller=np.array(put_seller['indicator']-e_put_seller)
    final_call_seller=np.array(call_seller['indicator']-e_call_seller)
    shine_c_strike=np.array(call_seller['StrikeRate'])
    shine_p_strike=np.array(put_seller['StrikeRate'])
    for i in range(len(final_call_seller)):
        if final_call_seller[i]<0:
            a,b=order_button(shine_c_strike[i],'CE_S',tron)
            c=0
            while b!=0:
                c+=1
                sleep(5)
                a,b=order_button(shine_c_strike[i],'CE_S',tron)
                if c>5:
                    if b!=0:
                        final_call_seller[i]=0
                    break
        elif final_call_seller[i]>0:
            order_button(shine_c_strike[i],'CE_B',tron)
    for i in range(len(final_put_seller)):
        if final_put_seller[i]<0:
            a,b=order_button(shine_p_strike[i],'PE_S',tron)
            c=0
            while b!=0:
                c+=1
                sleep(5)
                a,b=order_button(shine_p_strike[i],'PE_S',tron)
                if c>5:
                    if b!=0:
                        final_put_seller[i]=0
                    break
        elif final_put_seller[i]>0:
            order_button(shine_p_strike[i],'PE_B',tron)
    e_put_seller=put_seller['indicator']
    e_call_seller=call_seller['indicator']
    if abs(x_prime-x)>99:
        x_prime=x

#clear_open_positions()
# %%
