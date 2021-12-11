#%%
import json
import pandas as pd
import matplotlib.pyplot as plt
def calliv(optionchain,strikeprice):
    a=pd.DataFrame(optionchain)
    price=float(a[a['Strikes']==strikeprice]['CallIV'])
    return price

def putiv(optionchain,strikeprice):
    a=pd.DataFrame(optionchain)
    price=float(a[a['Strikes']==strikeprice]['PutIV'])
    return price

def readJson(symbol, fromDate, toDate,expiry):
    fileName = symbol+"_"+str(fromDate)+"_"+str(toDate)+"_"+str(expiry)+'.json'
    f = open(fileName)
    # returns JSON object as
    # a dictionary
    data = json.load(f)
    f.close()
    return data

symbol = 'BANKNIFTY'
fromDate = '2021-11-03'
fromTime = '09:20:00'
toDate = '2021-11-03'
toTime='15:35:00'
expiry = '11NOV2021'
present_expiry = readJson(symbol, fromDate, toDate, expiry='11NOV2021')
p_keys=list(present_expiry.keys())


for i in range(len(p_keys)):
    a=present_expiry[p_keys[i]]['optionchaindata']
    x=present_expiry[p_keys[i]]['spotPrice']
    req_list_PE_strikeprice=[round(x/100)*100]
    req_list_CE_strikeprice=[round(x/100)*100]
    call_IV=[]
    put_IV=[]
    for k in range(1,25):
        req_list_PE_strikeprice=req_list_PE_strikeprice+[round(x/100)*100-k*100]
        req_list_CE_strikeprice=req_list_CE_strikeprice+[round(x/100)*100+k*100]
    for i in range(0,25):
        try:
            call_IV=call_IV+[calliv(a,req_list_CE_strikeprice[i])]
        except Exception:
            call_IV=call_IV+[0]
        try:
            put_IV=put_IV+[putiv(a,req_list_PE_strikeprice[i])]
        except Exception:
            put_IV=put_IV+[0]
    plt.plot(req_list_CE_strikeprice,call_IV)
    plt.plot(req_list_PE_strikeprice,put_IV)
    plt.show()
    plt.pause(0.1)

# %%
