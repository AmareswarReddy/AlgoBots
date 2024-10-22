#%%
import json
import os
from os import error
import numpy as np
from datetime import datetime, timedelta
os.chdir('/Users/vinayreddy/Desktop/strangle better comparision')
#eg: optionchain=present_expiry[p_keys[0]]['optionchaindata']
#eg: strikeprice= 35500
alpha1=2 #call_ltp>=alpha1*put_ltp
alpha2=2  #put_ltp>=alpha2*call_ltp
beta=0.85
gamma=50
start_cpLTP=75
days_in_strategy=6
import pandas as pd
import requests
import json
def getexpires():
    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; Rigor/1.0.0; http://rigor.com)",
        "Accept": "*/*"
    }
    url = 'https://opstra.definedge.com/api/optionsimulator/simulatorexpiries'
    r = requests.get(url, headers=headers)
    
    if(r.status_code == 200):
        json_data = json.loads(r.content)
        return json_data;
expires_list = getexpires()

def callprice(optionchain,strikeprice):
    a=pd.DataFrame(optionchain)
    price=float(a[a['Strikes']==strikeprice]['CallLTP'])
    return price

def putprice(optionchain,strikeprice):
    a=pd.DataFrame(optionchain)
    price=float(a[a['Strikes']==strikeprice]['PutLTP'])
    return price


df_writeData = pd.DataFrame(columns=['Expiry', 'Total Profit Booked 75', 'Total Profit Booked 115'])
start_cpLTP_list= [75, 115]
for i in range(0, len(expires_list)):
    expiry = expires_list[i]
    if '2021' in expires_list[i]:
        profit_75 = 0
        profit_115 = 0
        for price in start_cpLTP_list:
            start_cpLTP = price
            print("Start Price:"+str(start_cpLTP))
            if start_cpLTP == 75:
                gamma = 0
            elif start_cpLTP == 115:
                gamma = 0
            #print(expires_list[i])
            enddate = datetime.strptime(expiry, '%d%b%Y')
            print(enddate.date())
            startdate = enddate - timedelta(days=days_in_strategy)
            print(startdate.date())
            symbol = 'BANKNIFTY'
            fromDate = startdate.strftime('%Y-%m-%d')
            fromTime = '09:20:00'
            toDate = enddate.strftime('%Y-%m-%d')
            toTime='15:35:00'

            #dataJson = readJson(symbol, fromDate, toDate, expiry)
            #data = getOptionData(symbol, fromDate,fromTime, toDate,toTime, expiry)
            #jsonDump(symbol,  fromDate,toDate,expiry, data)
            present_expiry = readJson(symbol, fromDate, toDate,expiry, fromTime, toTime)
            p_keys=list(present_expiry.keys())
            '''
            near_expiry = readJson(symbol, fromDate, toDate, expiry='18NOV2021')
            n_keys=list(near_expiry.keys())
            far_expiry = readJson(symbol, fromDate, toDate, expiry='25NOV2021')
            f_keys=list(far_expiry.keys())
            '''
            import matplotlib.pyplot as plt
            start=0
            time_to_break=0
            ceequalspe=0
            try:
                x=present_expiry[p_keys[start]]['spotPrice']
                if x==0:
                    raise Exception("")
            except Exception:
                x=present_expiry[p_keys[start]]['futuresPrice']
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
            ce_positions={p_keys[start]:[CE_upper,call_price,start]}
            pe_positions={p_keys[start]:[PE_lower,put_price,start]}
            after_gamma_adjustments={}
            stoplosshit=0
            for i in range(len(p_keys)):
                if present_expiry[p_keys[i]]['spotPrice']==0:
                    spot=spot+[present_expiry[p_keys[i]]['futuresPrice']]
                else:
                    spot=spot+[present_expiry[p_keys[i]]['spotPrice']]
                #print(booked_profit)
                if stoplosshit>0:
                    Current_CE_strikeprice=after_gamma_adjustments[list(after_gamma_adjustments.keys())[-1]][0]
                    Current_PE_strikeprice=after_gamma_adjustments[list(after_gamma_adjustments.keys())[-1]][0]
                    try :
                        call_ltp=callprice(optionchain=present_expiry[p_keys[i]]['optionchaindata'],strikeprice=Current_CE_strikeprice)
                    except Exception:
                        try:
                            t1=callprice(optionchain=present_expiry[p_keys[i]]['optionchaindata'],strikeprice=Current_CE_strikeprice+100)
                            t2=callprice(optionchain=present_expiry[p_keys[i]]['optionchaindata'],strikeprice=Current_CE_strikeprice-100)
                            call_ltp=-(2.6*(t1+t2))/100+(t1+t2)/2
                        except Exception:
                            try:
                                call_ltp=callprice(optionchain=present_expiry[p_keys[i-2]]['optionchaindata'],strikeprice=Current_CE_strikeprice)
                            except Exception:
                                call_ltp=callprice(optionchain=present_expiry[p_keys[i-3]]['optionchaindata'],strikeprice=Current_CE_strikeprice)
                    try:
                        put_ltp=putprice(optionchain=present_expiry[p_keys[i]]['optionchaindata'],strikeprice=Current_PE_strikeprice)
                    except Exception:
                        try:
                            t1==putprice(optionchain=present_expiry[p_keys[i]]['optionchaindata'],strikeprice=Current_PE_strikeprice+100)
                            t2==putprice(optionchain=present_expiry[p_keys[i]]['optionchaindata'],strikeprice=Current_PE_strikeprice-100) 
                            put_ltp=-(2.6*(t1+t2))/100+(t1+t2)/2
                        except Exception:
                            try:
                                put_ltp=putprice(optionchain=present_expiry[p_keys[i-2]]['optionchaindata'],strikeprice=Current_PE_strikeprice)
                            except Exception:
                                put_ltp=putprice(optionchain=present_expiry[p_keys[i-3]]['optionchaindata'],strikeprice=Current_PE_strikeprice)
                    #print('booked', booked_profit)
                    profit=profit+[booked_profit+after_gamma_adjustments[list(after_gamma_adjustments.keys())[-1]][1]-call_ltp+after_gamma_adjustments[list(after_gamma_adjustments.keys())[-1]][2]-put_ltp]
                elif stoplosshit==0:
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
                    try:
                        x=present_expiry[p_keys[i]]['spotPrice']
                        if x==0:
                            raise Exception("")
                    except Exception:
                        x=present_expiry[p_keys[i]]['futuresPrice']
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
                            live_PE_lastrate = live_PE_lastrate+[-1]
                        try:
                            live_CE_lastrate = live_CE_lastrate+[callprice(optionchain=present_expiry[p_keys[i]]['optionchaindata'],strikeprice=req_list_CE_strikeprice[j])]
                        except Exception:
                            live_CE_lastrate = live_CE_lastrate+[-1]
                    PE_index_strikeprice = np.argmin(np.abs(np.array(live_PE_lastrate)-beta*call_ltp))
                    put_price = putprice(optionchain=present_expiry[p_keys[i]]['optionchaindata'],strikeprice=req_list_PE_strikeprice[PE_index_strikeprice])
                    pe_positions[p_keys[i]] = [req_list_PE_strikeprice[PE_index_strikeprice],put_price,i]
                    booked_profit = booked_profit+pe_positions[list(pe_positions.keys())[-2]][1]-put_ltp
                if put_ltp>=alpha2*call_ltp and Current_CE_strikeprice-Current_PE_strikeprice>gamma:   #changing call position
                    try:
                        x=present_expiry[p_keys[i]]['spotPrice']
                        if x==0:
                            raise Exception("")
                    except Exception:
                        x=present_expiry[p_keys[i]]['futuresPrice']
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
                            live_PE_lastrate = live_PE_lastrate+[-1]
                        try:
                            live_CE_lastrate = live_CE_lastrate+[callprice(optionchain=present_expiry[p_keys[i]]['optionchaindata'],strikeprice=req_list_CE_strikeprice[j])]
                        except Exception:
                            live_CE_lastrate = live_CE_lastrate+[-1]
                    CE_index_strikeprice = np.argmin(np.abs(np.array(live_CE_lastrate)-beta*put_ltp))
                    call_price = callprice(optionchain=present_expiry[p_keys[i]]['optionchaindata'],strikeprice=req_list_CE_strikeprice[CE_index_strikeprice])
                    ce_positions[p_keys[i]] = [req_list_CE_strikeprice[CE_index_strikeprice],call_price,i]
                    booked_profit = booked_profit+ce_positions[list(ce_positions.keys())[-2]][1]-call_ltp
            #
                if Current_CE_strikeprice-Current_PE_strikeprice<=0 and abs(call_ltp-put_ltp)<call_ltp/20:
                    #square of all positions
                    ceequalspe=ceequalspe+1
                    #print('ce=pe')
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

                    stoplosshit=stoplosshit+1
                    Total_value_old=float('inf')
                    try:
                        x=present_expiry[p_keys[i]]['spotPrice']
                        if x==0:
                            raise Exception("")
                    except Exception:
                        x=present_expiry[p_keys[i]]['futuresPrice']
                    req_list_PE_strikeprice=[round(x/100)*100]
                    req_list_CE_strikeprice=[round(x/100)*100]
                    try :
                        call_ltp=callprice(optionchain=present_expiry[p_keys[i]]['optionchaindata'],strikeprice=req_list_CE_strikeprice[0])
                    except Exception:
                        try:
                            t1=callprice(optionchain=present_expiry[p_keys[i]]['optionchaindata'],strikeprice=req_list_CE_strikeprice[0]+100)
                            t2=callprice(optionchain=present_expiry[p_keys[i]]['optionchaindata'],strikeprice=req_list_CE_strikeprice[0]-100)
                            call_ltp=-(2.6*(t1+t2))/100+(t1+t2)/2
                        except Exception:
                            try:
                                call_ltp=callprice(optionchain=present_expiry[p_keys[i-1]]['optionchaindata'],strikeprice=req_list_CE_strikeprice[0])
                            except Exception:
                                call_ltp=callprice(optionchain=present_expiry[p_keys[i-2]]['optionchaindata'],strikeprice=req_list_CE_strikeprice[0])
                    try:
                        put_ltp=putprice(optionchain=present_expiry[p_keys[i]]['optionchaindata'],strikeprice=req_list_PE_strikeprice[0])
                    except Exception:
                        try:
                            t1==putprice(optionchain=present_expiry[p_keys[i]]['optionchaindata'],strikeprice=req_list_PE_strikeprice[0]+100)
                            t2==putprice(optionchain=present_expiry[p_keys[i]]['optionchaindata'],strikeprice=req_list_PE_strikeprice[0]-100) 
                            put_ltp=-(2.6*(t1+t2))/100+(t1+t2)/2
                        except Exception:
                            try:
                                put_ltp=putprice(optionchain=present_expiry[p_keys[i-1]]['optionchaindata'],strikeprice=req_list_PE_strikeprice[0])
                            except Exception:
                                put_ltp=putprice(optionchain=present_expiry[p_keys[i-2]]['optionchaindata'],strikeprice=req_list_PE_strikeprice[0])                    
                    live_PE_lastrate = [put_ltp]
                    live_CE_lastrate = [call_ltp]
                    call_price = live_CE_lastrate[0]
                    put_price = live_PE_lastrate[0]

                    after_gamma_adjustments[p_keys[i]]=[req_list_CE_strikeprice[0],call_price,put_price,i]
                    booked_profit = profit[-1]
                    #print('stoplosshits = ', stoplosshit)
                    #print(after_gamma_adjustments)
                    #print(profit[-1])
                    time_to_break=0
            
            fig, ax = plt.subplots(2, 1)
            ax[0].plot(profit,'k')
            ax[0].set_xlabel('time(scale=5min)')
            ax[0].set_ylabel("profit(scale=25rs.)")
            
            ax[1].plot(spot,'k')
            for hun in range(0,len(ce_positions)):
                try:
                    ax[1].plot([ce_positions[list(ce_positions.keys())[hun]][-1],ce_positions[list(ce_positions.keys())[hun+1]][-1]],[ce_positions[list(ce_positions.keys())[hun]][0],ce_positions[list(ce_positions.keys())[hun]][0]],'b')
                except Exception:
                    try:
                        ax[1].plot([ce_positions[list(ce_positions.keys())[hun]][-1],after_gamma_adjustments[list(after_gamma_adjustments.keys())[0]][-1]],[ce_positions[list(ce_positions.keys())[hun]][0],ce_positions[list(ce_positions.keys())[hun]][0]],'b')
                    except Exception:
                        ax[1].plot([ce_positions[list(ce_positions.keys())[hun]][-1],len(profit)],[ce_positions[list(ce_positions.keys())[hun]][0],ce_positions[list(ce_positions.keys())[hun]][0]],'b')

            for hun in range(0,len(pe_positions)):
                try:
                    ax[1].plot([pe_positions[list(pe_positions.keys())[hun]][-1],pe_positions[list(pe_positions.keys())[hun+1]][-1]],[pe_positions[list(pe_positions.keys())[hun]][0],pe_positions[list(pe_positions.keys())[hun]][0]],'r')
                except Exception:
                    try:
                        ax[1].plot([pe_positions[list(pe_positions.keys())[hun]][-1],after_gamma_adjustments[list(after_gamma_adjustments.keys())[0]][-1]],[pe_positions[list(pe_positions.keys())[hun]][0],pe_positions[list(pe_positions.keys())[hun]][0]],'r')
                    except Exception:
                        ax[1].plot([pe_positions[list(pe_positions.keys())[hun]][-1],len(profit)],[pe_positions[list(pe_positions.keys())[hun]][0],pe_positions[list(pe_positions.keys())[hun]][0]],'r')




            for hun in range(0,len(after_gamma_adjustments)):
                try:
                    ax[1].plot([after_gamma_adjustments[list(after_gamma_adjustments.keys())[hun]][-1],after_gamma_adjustments[list(after_gamma_adjustments.keys())[hun+1]][-1]],[after_gamma_adjustments[list(after_gamma_adjustments.keys())[hun]][0],after_gamma_adjustments[list(after_gamma_adjustments.keys())[hun]][0]],'y')
                except Exception:
                    ax[1].plot([after_gamma_adjustments[list(after_gamma_adjustments.keys())[hun]][-1],len(profit)],[after_gamma_adjustments[list(after_gamma_adjustments.keys())[hun]][0],after_gamma_adjustments[list(after_gamma_adjustments.keys())[hun]][0]],'y')                        
            
            ax[1].set_xlabel('time(scale=5min)')
            ax[1].set_ylabel('spotprice')
            filename = 'images/'+expiry+"_"+str(start_cpLTP)+".png"
            plt.savefig(filename, transparent=True)
            
            #print('Total profit booked:',profit[-1])
            if start_cpLTP == 75:
                profit_75 = profit[-1]
            elif start_cpLTP == 115:
                profit_115 = profit[-1]
        df_writeData.loc[0 if pd.isnull(df_writeData.index.max()) else df_writeData.index.max() + 1] = [expiry,profit_75, profit_115 ]
        df_writeData.to_excel('report.xlsx')





# %%


from datetime import datetime

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

import requests
import json
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

# %%
