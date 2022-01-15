#%%
import json
from os import error
from datetime import datetime
import numpy as np
import requests
#eg: optionchain=present_expiry[p_keys[0]]['optionchaindata']
#eg: strikeprice= 35500
alpha1=2 #call_ltp>=alpha1*put_ltp
alpha2=2  #put_ltp>=alpha2*call_ltp
beta=0.85
gamma=-1000
start_cpLTP=115
modified_strangle_tracker = 0
import pandas as pd
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

def readJson(symbol, fromDate, toDate,expiry, fromTime='09:20:00', toTime='15:35:00'):
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


symbol = 'BANKNIFTY'
fromDate = '2021-11-03'
fromTime = '09:20:00'
toDate = '2021-11-25'
toTime='15:35:00'
expiry = '11NOV2021'

#dataJson = readJson(symbol, fromDate, toDate, expiry)
present_expiry = readJson(symbol, fromDate, toDate, expiry)
p_keys=list(present_expiry.keys())
'''
near_expiry = readJson(symbol, fromDate, toDate, expiry='18NOV2021')
n_keys=list(near_expiry.keys())
far_expiry = readJson(symbol, fromDate, toDate, expiry='25NOV2021')
f_keys=list(far_expiry.keys())
'''
#%%
import matplotlib.pyplot as plt
start=0
time_to_break=0
ceequalspe=0
x=present_expiry[p_keys[start]]['spotPrice']
req_list_PE_strikeprice=[round(x/100)*100]
req_list_CE_strikeprice=[round(x/100)*100]
#ce_positions{p_keys[i]:}

for i in range(1,25):
    req_list_PE_strikeprice=[round(x/100)*100+i*100]+req_list_PE_strikeprice+[round(x/100)*100-i*100]
    req_list_CE_strikeprice=[round(x/100)*100-i*100]+req_list_CE_strikeprice+[round(x/100)*100+i*100]
live_PE_lastrate=[]
live_CE_lastrate=[]
for j in range(0,49):
    try:
        live_PE_lastrate=live_PE_lastrate+[putprice(optionchain=present_expiry[p_keys[start]]['optionchaindata'],strikeprice=req_list_PE_strikeprice[j])]
    except Exception:
        live_PE_lastrate=live_PE_lastrate+[-1]
    try:
        live_CE_lastrate = live_CE_lastrate+[callprice(optionchain=present_expiry[p_keys[start]]['optionchaindata'],strikeprice=req_list_CE_strikeprice[j])]
    except Exception:
        live_CE_lastrate = live_CE_lastrate+[-1]
CE_index_strikeprice=np.argmin(np.abs(np.array(live_CE_lastrate)-start_cpLTP))
PE_index_strikeprice=np.argmin(np.abs(np.array(live_PE_lastrate)-start_cpLTP))
CE_upper=req_list_CE_strikeprice[CE_index_strikeprice]
PE_lower=req_list_PE_strikeprice[PE_index_strikeprice]

#strategy implimentation



profit=[0]
spot=[]
booked_profit=0
Total_value_old=float('inf')
call_price=callprice(optionchain=present_expiry[p_keys[start]]['optionchaindata'],strikeprice=CE_upper)
put_price=putprice(optionchain=present_expiry[p_keys[start]]['optionchaindata'],strikeprice=PE_lower)
ce_positions={p_keys[start]:[CE_upper,call_price]}
pe_positions={p_keys[start]:[PE_lower,put_price]}
for i in range(len(p_keys)):
    spot=spot+[present_expiry[p_keys[i]]['spotPrice']]
    #print(booked_profit)
    Current_CE_strikeprice=ce_positions[list(ce_positions.keys())[-1]][0]
    Current_PE_strikeprice=pe_positions[list(pe_positions.keys())[-1]][0]
    try:
        temp= callprice(optionchain=present_expiry[p_keys[i]]['optionchaindata'],strikeprice=Current_CE_strikeprice)
        call_ltp=temp
    except Exception:
        True

    try:
        temp= putprice(optionchain=present_expiry[p_keys[i]]['optionchaindata'],strikeprice=Current_PE_strikeprice)
        put_ltp=temp
    except Exception:
        True
    profit=profit+[ce_positions[list(ce_positions.keys())[-1]][1]-call_ltp+pe_positions[list(pe_positions.keys())[-1]][1]-put_ltp+booked_profit]
    if call_ltp>=alpha1*put_ltp and Current_CE_strikeprice-Current_PE_strikeprice>gamma:   #changing put position
        x=present_expiry[p_keys[i]]['spotPrice']
        req_list_PE_strikeprice=[round(x/100)*100]
        req_list_CE_strikeprice=[round(x/100)*100]
        for k in range(1,25):
            req_list_PE_strikeprice=[round(x/100)*100+k*100]+req_list_PE_strikeprice+[round(x/100)*100-k*100]
            req_list_CE_strikeprice=[round(x/100)*100-k*100]+req_list_CE_strikeprice+[round(x/100)*100+k*100]
        live_PE_lastrate=[]
        live_CE_lastrate=[]
        for j in range(0,49):
            try:
                live_PE_lastrate = live_PE_lastrate+[putprice(optionchain=present_expiry[p_keys[i]]['optionchaindata'],strikeprice=req_list_PE_strikeprice[j])]
            except Exception:
                live_PE_lastrate = live_PE_lastrate+[-1000]
            try:
                live_CE_lastrate = live_CE_lastrate+[callprice(optionchain=present_expiry[p_keys[i]]['optionchaindata'],strikeprice=req_list_CE_strikeprice[j])]
            except Exception:
                live_CE_lastrate = live_CE_lastrate+[-1000]
        if modified_strangle_tracker%2 == 0:
                    PE_index_strikeprice = np.argmin(np.abs(np.array(live_PE_lastrate)-beta*call_ltp))
                    put_price = putprice(optionchain=present_expiry[p_keys[i]]['optionchaindata'],strikeprice=req_list_PE_strikeprice[PE_index_strikeprice])
                    pe_positions[p_keys[i]] = [req_list_PE_strikeprice[PE_index_strikeprice],put_price]
                    booked_profit = booked_profit+pe_positions[list(pe_positions.keys())[-2]][1]-put_ltp
                    modified_strangle_tracker = modified_strangle_tracker + 1
        elif modified_strangle_tracker%2 == 1:
                    CE_index_strikeprice = np.argmin(np.abs(np.array(live_CE_lastrate)- put_ltp))
                    #print(CE_index_strikeprice)
                    call_price = callprice(optionchain=present_expiry[p_keys[i]]['optionchaindata'],strikeprice=req_list_CE_strikeprice[CE_index_strikeprice])
                    ce_positions[p_keys[i]] = [req_list_CE_strikeprice[CE_index_strikeprice],call_price]
                    booked_profit = booked_profit+ce_positions[list(ce_positions.keys())[-2]][1]-call_ltp
                    modified_strangle_tracker = modified_strangle_tracker + 1
    if put_ltp>=alpha2*call_ltp and Current_CE_strikeprice-Current_PE_strikeprice>gamma:   #changing call position
        x=present_expiry[p_keys[i]]['spotPrice']
        req_list_PE_strikeprice=[round(x/100)*100]
        req_list_CE_strikeprice=[round(x/100)*100]
        for k in range(1,25):
            req_list_PE_strikeprice=[round(x/100)*100+k*100]+req_list_PE_strikeprice+[round(x/100)*100-k*100]
            req_list_CE_strikeprice=[round(x/100)*100-k*100]+req_list_CE_strikeprice+[round(x/100)*100+k*100]
        live_PE_lastrate=[]
        live_CE_lastrate=[]
        for j in range(0,49):
            try:
                live_PE_lastrate = live_PE_lastrate+[putprice(optionchain=present_expiry[p_keys[i]]['optionchaindata'],strikeprice=req_list_PE_strikeprice[j])]
            except Exception:
                live_PE_lastrate = live_PE_lastrate+[-1000]
            try:
                live_CE_lastrate = live_CE_lastrate+[callprice(optionchain=present_expiry[p_keys[i]]['optionchaindata'],strikeprice=req_list_CE_strikeprice[j])]
            except Exception:
                live_CE_lastrate = live_CE_lastrate+[-1000]
                
        if modified_strangle_tracker%2 == 0:
                    CE_index_strikeprice = np.argmin(np.abs(np.array(live_CE_lastrate)-beta*put_ltp))
                    call_price = callprice(optionchain=present_expiry[p_keys[i]]['optionchaindata'],strikeprice=req_list_CE_strikeprice[CE_index_strikeprice])
                    ce_positions[p_keys[i]] = [req_list_CE_strikeprice[CE_index_strikeprice],call_price]
                    booked_profit = booked_profit+ce_positions[list(ce_positions.keys())[-2]][1]-call_ltp
                    modified_strangle_tracker = modified_strangle_tracker + 1
            
        elif modified_strangle_tracker%2 == 1:
                    PE_index_strikeprice = np.argmin(np.abs(np.array(live_PE_lastrate)-call_ltp))
                    #print(PE_index_strikeprice)
                    put_price = putprice(optionchain=present_expiry[p_keys[i]]['optionchaindata'],strikeprice=req_list_PE_strikeprice[PE_index_strikeprice])
                    pe_positions[p_keys[i]] = [req_list_PE_strikeprice[PE_index_strikeprice],put_price]
                    booked_profit = booked_profit+pe_positions[list(pe_positions.keys())[-2]][1]-put_ltp
                    modified_strangle_tracker = modified_strangle_tracker + 1
    if Current_CE_strikeprice-Current_PE_strikeprice<=0 and abs(call_ltp-put_ltp)<call_ltp/20:
        #square of all positions
        ceequalspe=ceequalspe+1
        print(p_keys[i])
        print('ce=pe')
        #break

#
    if Current_CE_strikeprice-Current_PE_strikeprice<=gamma:
        Total_value_new=call_ltp+put_ltp
        if Total_value_new<Total_value_old:
            Stop_loss=Total_value_new*1.2
            Total_value_old=Total_value_new
        if Total_value_new>Stop_loss :
            #square off all positions
            time_to_break=1
    if time_to_break==1:
        print('stoplosshit')
        break
        
plt.plot(profit)
plt.xlabel('time(scale=5min)')
plt.ylabel("profit(scale=25rs.)")
plt.show()
plt.plot(spot)
plt.xlabel('time(scale=5min)')
plt.ylabel('spotprice')
plt.show()
print('Total profit booked:',profit[-1])

# %%
