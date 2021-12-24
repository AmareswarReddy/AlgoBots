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
fromDate = '2021-11-03'
fromTime = '09:20:00'
toDate = '2021-11-11'
toTime='15:35:00'
expiry = '11NOV2021'


start=0

present_expiry = readJson(symbol, fromDate, toDate,expiry, fromTime, toTime)
p_keys=list(present_expiry.keys())
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
req_list_CE_strikeprice.remove(0)
v1=np.array(req_list_CE_strikeprice)
v1=v1[v1!=0]
v2=np.array(req_list_PE_strikeprice)
v2=v2[v2!=0]

n1=np.array(live_CE_lastrate)
n2=np.array(live_PE_lastrate)

f1spot = interpolate.interp1d(v1, n1,kind = 'cubic')
f2spot = interpolate.interp1d(v2, n2, kind = 'cubic')
def change_in_call(strikeprice=41000,f1spot=f1spot,delta=200):
    a=f1spot(strikeprice-delta)-f1spot(strikeprice)
    return a
def change_in_put(strikeprice=41000,f2spot=f2spot,delta=200):
    a=f2spot(strikeprice-delta)-f2spot(strikeprice)
    return a
change_in_call(40000,f1spot,1)

# %%
