#%%
import numpy as np
from scipy import interpolate
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime
import requests
import json

def callprice(optionchain,strikeprice):
    a=pd.DataFrame(optionchain)
    price=float(a[a['Strikes']==strikeprice]['CallLTP'])
    return price

def putprice(optionchain,strikeprice):
    a=pd.DataFrame(optionchain)
    price=float(a[a['Strikes']==strikeprice]['PutLTP'])
    return price


def getOptionData(symbol = 'NIFTY', fromDate = '2018-12-25', fromTime = '09:20:00', toDate = '2018-12-25', toTime='15:35:00', expiry='02DEC2021' ):
    baseURL = 'https://opstra.definedge.com/api/optionsimulator/optionchain/'
    currentDate = fromDate + " "+ fromTime
    datetime_object_current = datetime.strptime(currentDate, '%Y-%m-%d %X')
    timestamp_current = int(datetime.timestamp(datetime_object_current))
    #print(timestamp_current)
    fivemin_timestamp = 300
    endDate = toDate + " "+ toTime
    datetime_object_endDate = datetime.strptime(endDate, '%Y-%m-%d %X')
    timestamp_end = int(datetime.timestamp(datetime_object_endDate))
    #print(timestamp_end)
    final_data = {}
    while (timestamp_current < timestamp_end):
        dt_object = datetime.fromtimestamp(timestamp_current)
        
        only_time = dt_object.time()
        timeparts = str(only_time).split(":")
        if (9 <= int(timeparts[0]) <= 15):
            #print(only_time)
            #url = baseURL + str(timestamp_current)+"&"+symbol+"&"+(datetime.fromtimestamp(timestamp_current).strftime('%d%b%Y')).upper()
            url = baseURL + str(timestamp_current)+"&"+symbol+"&"+ expiry
            
            #print(url)
            tempData = downloaddata(url)
            if tempData is not None:
                final_data[str(dt_object)] = tempData
                #print(dt_object)
                #print(url)
        timestamp_current = timestamp_current + fivemin_timestamp    
    return final_data

def downloaddata(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; Rigor/1.0.0; http://rigor.com)",
        "Accept": "*/*"
    }
    url = url
    r = requests.get(url, headers=headers)
    
    if(r.status_code == 200):
        json_data = json.loads(r.content)
        return json_data;
    else:
        return None;
    
def jsonDump(symbol, fromDate, toDate, expiry,data):
    # the json file where the output must be stored
    fileName = symbol+"_"+str(fromDate)+"_"+str(toDate)+"_"+str(expiry)+'.json'
    out_file = open(fileName, "w")

    json.dump(data, out_file, indent = 6)

    out_file.close()

def readJson(symbol, fromDate, toDate,expiry, fromTime, toTime):
    fileName = symbol+"_"+str(fromDate)+"_"+str(toDate)+"_"+str(expiry)+'.json'
    if  not os.path.isfile(fileName):
        print("Downloading Data")
        data = getOptionData(symbol, fromDate,fromTime, toDate,toTime, expiry)
        jsonDump(symbol,  fromDate,toDate,expiry, data)
    f = open(fileName)
    # returns JSON object as
    # a dictionary
    data = json.load(f)
    f.close()
    return data

#%%
symbol = 'BANKNIFTY'
fromDate = '2021-11-18'
fromTime = '09:20:00'
toDate = '2021-12-02'
toTime='15:35:00'
expiry = '02DEC2021'


present_expiry = readJson(symbol, fromDate, toDate,expiry, fromTime, toTime)
def functions(start=0,present_expiry=present_expiry):

    p_keys=list(present_expiry.keys())
    if type(start)==str:
        start=p_keys.index(start)
    x=present_expiry[p_keys[start]]['spotPrice']
    req_list_PE_strikeprice=[round(x/100)*100]
    req_list_CE_strikeprice=[round(x/100)*100]
    for i in range(1,25):
        req_list_PE_strikeprice=[round(x/100)*100+i*100]+req_list_PE_strikeprice+[round(x/100)*100-i*100]
        req_list_CE_strikeprice=[round(x/100)*100-i*100]+req_list_CE_strikeprice+[round(x/100)*100+i*100]
    live_PE_lastrate=[]
    live_CE_lastrate=[]
    for j in range(0,49):
        try:
            live_PE_lastrate=live_PE_lastrate+[putprice(optionchain=present_expiry[p_keys[start]]['optionchaindata'],strikeprice=req_list_PE_strikeprice[j])]
        except Exception:
            req_list_PE_strikeprice[j]=0
        try:
            live_CE_lastrate = live_CE_lastrate+[callprice(optionchain=present_expiry[p_keys[start]]['optionchaindata'],strikeprice=req_list_CE_strikeprice[j])]
        except Exception:
            req_list_CE_strikeprice[j]=0
    if 0 in req_list_CE_strikeprice :
        req_list_CE_strikeprice.remove(0)
    if 0 in req_list_PE_strikeprice :
        req_list_PE_strikeprice.remove(0)
    v1=np.array(req_list_CE_strikeprice)
    v1=v1[v1!=0]
    v2=np.array(req_list_PE_strikeprice)
    v2=v2[v2!=0]
    n1=np.array(live_CE_lastrate)
    n2=np.array(live_PE_lastrate)
    f1spot = interpolate.interp1d(v1, n1,kind = 'cubic',fill_value='extrapolate')
    f2spot = interpolate.interp1d(v2, n2, kind = 'cubic',fill_value='extrapolate')
    return f1spot,f2spot
#%%
# theta visualisation by taking virtual positions at the spot price.
p_keys=list(present_expiry.keys())
call_lastrate_spot=[]
put_lastrate_spot=[]
spot=[]
for i in range(0,len(p_keys)):
    callspot,putspot=functions(start=i,present_expiry=present_expiry)
    call_lastrate_spot=call_lastrate_spot+[callspot(present_expiry[p_keys[i]]['spotPrice'])]
    put_lastrate_spot=put_lastrate_spot+[putspot(present_expiry[p_keys[i]]['spotPrice'])]
    spot=spot+[present_expiry[p_keys[i]]['spotPrice']]


fig, ax_left = plt.subplots()
ax_right = ax_left.twinx()

ax_left.plot(call_lastrate_spot, color='blue')
ax_left.plot(put_lastrate_spot, color='red')
ax_right.plot(spot,color='green')

#%%
def change_in_call(strikeprice=41000,f1spot=callspot,delta=200):
    a=f1spot(strikeprice-delta)-f1spot(strikeprice)
    return a
def change_in_put(strikeprice=41000,f2spot=putspot,delta=200):
    a=f2spot(strikeprice-delta)-f2spot(strikeprice)
    return a
# real time delta strategy
positions_taken=[{'strike':38200,
                                'type':'CE',
                                'side':1},
                            {'strike':38200,
                              'type':'PE',
                              'side':1},
                              {'strike':37500,
                                 'type':'PE',
                                 'side':-1}]
                                                  
def instant_cost(positions_taken=positions_taken,delta=100,start=5,time_lapsed=10):
    callspot,putspot=functions(start=start+time_lapsed,present_expiry=present_expiry) 
    callspot_prime,putspot_prime=functions(start=start,present_expiry=present_expiry) 
    temp=[]
    temp2=[]
    for i in range(len(positions_taken)): 
        if positions_taken[i]['type']=='CE':
            temp=temp+[positions_taken[i]['side']*callspot(positions_taken[i]['strike'])]
        elif positions_taken[i]['type']=='PE':
            temp=temp+[positions_taken[i]['side']*putspot(positions_taken[i]['strike'])]
        if positions_taken[i]['type']=='CE':
            temp2=temp2+[positions_taken[i]['side']*callspot_prime(positions_taken[i]['strike'])]
        elif positions_taken[i]['type']=='PE':
            temp2=temp2+[positions_taken[i]['side']*putspot_prime(positions_taken[i]['strike'])]

    profit=np.sum(np.array(temp)-np.array(temp2))
    a=0
    for i in range(len(positions_taken)):
        if positions_taken[i]['type']=='CE':
            a=a+positions_taken[i]['side']*change_in_call(positions_taken[i]['strike'],f1spot=callspot,delta=delta)
        elif positions_taken[i]['type']=='PE':
            a=a+positions_taken[i]['side']*change_in_put(positions_taken[i]['strike'],f2spot=putspot,delta=delta)
    return profit+a
# %%
def long_positions(present_expiry,start):
    p_keys=list(present_expiry.keys())
    x=present_expiry[p_keys[start]]['spotPrice']
    out=[]
    for i in range(1,15):
        positions_taken=[{'strike':round(x/100)*100+i*100,
                                    'type':'CE',
                                    'side':1},
                                    {'strike':round(x/100)*100+i*100,
                                      'type':'PE',
                                      'side':1},
                                    {'strike':round(x/100)*100,
                                     'type':'PE',
                                     'side':-1}]
        a=instant_cost(positions_taken=positions_taken,delta=-200,start=start,time_lapsed=0)
        b=instant_cost(positions_taken=positions_taken,delta=200,start=start,time_lapsed=0)
        out=out+[abs(b/a)]
    return  [{'strike':round(x/100)*100+(np.argmax(out)+1)*100,
                'type':'CE',
                'side':1},
                {'strike':round(x/100)*100+(np.argmax(out)+1)*100,
                  'type':'PE',
                  'side':1},
                {'strike':round(x/100)*100,
                 'type':'PE',
                 'side':-1}]

def short_positions(present_expiry,start):
    p_keys=list(present_expiry.keys())
    x=present_expiry[p_keys[start]]['spotPrice']
    out=[]
    for i in range(1,15):
        positions_taken=[{'strike':round(x/100)*100-i*100,
                                    'type':'CE',
                                    'side':1},
                                    {'strike':round(x/100)*100-i*100,
                                      'type':'PE',
                                      'side':1},
                                    {'strike':round(x/100)*100,
                                     'type':'CE',
                                     'side':-1}]
        a=instant_cost(positions_taken=positions_taken,delta=-200,start=start,time_lapsed=0)
        b=instant_cost(positions_taken=positions_taken,delta=200,start=start,time_lapsed=0)
        out=out+[abs(a/b)]
    return  [{'strike':round(x/100)*100-(np.argmax(out)+1)*100,
                'type':'CE',
                'side':1},
                {'strike':round(x/100)*100-(np.argmax(out)+1)*100,
                  'type':'PE',
                  'side':1},
                {'strike':round(x/100)*100,
                 'type':'CE',
                 'side':-1}]
#%%
best_long_positions=long_positions(present_expiry=present_expiry,start=15)
best_short_positions=short_positions(present_expiry=present_expiry,start=15)
print(best_long_positions)
print(best_short_positions)

# %%
def max_loss(present_expiry=present_expiry,positions_taken=best_long_positions,start=15,time_lapsed=10):
    ammu=[]
    for i in np.linspace(500,-500,101):
        ammu=ammu+[instant_cost(positions_taken=positions_taken,delta=i,start=start,time_lapsed=time_lapsed)]
    ammu=np.array(ammu)
    plt.plot(ammu)
    return {'maxloss':min(ammu),
                'maxloss_at':round(present_expiry[p_keys[0]]['spotPrice'])+np.argmin(ammu)-round(len(ammu)/2),
                'breakeven':round(present_expiry[p_keys[0]]['spotPrice'])+np.argmin(np.abs(ammu[round(len(ammu)/2):]))
                }
max_loss(present_expiry=present_expiry,positions_taken=best_long_positions,start=100,time_lapsed=0)
#%%
for i in range(0,len(p_keys)):
