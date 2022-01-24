#%%

# Navigate to Below Link and obtain auth_code
#https://api.fyers.in/api/v2/generate-authcode?client_id=TTHF3EHNQM-100&redirect_uri=http%3A%2F%2Flocalhost%3A8000%2F&response_type=code&state=None&scope=&nonce=private
auth_code = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJhcGkubG9naW4uZnllcnMuaW4iLCJpYXQiOjE2NDMwNDAzMDksImV4cCI6MTY0MzA3MDMwOSwibmJmIjoxNjQzMDM5NzA5LCJhdWQiOiJbXCJ4OjBcIiwgXCJ4OjFcIiwgXCJ4OjJcIiwgXCJkOjFcIiwgXCJkOjJcIiwgXCJ4OjFcIiwgXCJ4OjBcIl0iLCJzdWIiOiJhdXRoX2NvZGUiLCJkaXNwbGF5X25hbWUiOiJYUDE1MzI3Iiwibm9uY2UiOiJwcml2YXRlIiwiYXBwX2lkIjoiVFRIRjNFSE5RTSIsInV1aWQiOiI5YTMxYjFmZDBjYjk0YzdlYTM0ZjMwNDY1OTcyN2ZhYSIsImlwQWRkciI6IjAuMC4wLjAiLCJzY29wZSI6IiJ9.0S0DK788cT-y2HaeiiL4wi8AeSjk_bFG4U2DHqiI2cw"

# Update scripmaster file every week
import numpy as np
import pandas as pd
import calendar
from time import sleep, strftime
from datetime import datetime 
import requests
from pytz import timezone 
from fyers_api import fyersModel
from fyers_api import accessToken




client_id = "TTHF3EHNQM-100"
secret_key = "SE5N0EKNVY"
redirect_uri = "http://localhost:8000/"
response_type = "code"
grant_type = "authorization_code"
state = "None"
nonce = "private"

session=accessToken.SessionModel(client_id=client_id,
secret_key=secret_key,redirect_uri=redirect_uri, 
response_type=response_type, grant_type=grant_type,
state=state,scope="",nonce=nonce)


session.set_token(auth_code)
response_token = session.generate_token()
print(response_token)

access_token = response_token['access_token']
print(access_token)
fyers = fyersModel.FyersModel(client_id=client_id, token=access_token,log_path="/Users/vinayreddy/Desktop/logs/")
#%%
month_mapping = {
    '01' : '1', 
'02' : '2' ,
'03' : '3', 
'04' : '4', 
'05' : '5' ,
'06' : '6' ,
'07' : '7' ,
'08' : '8' ,
'09' : '9' ,
'10':  'O' ,
'11' : 'N', 
'12' : 'D'
}
month_end_mapping = {
    '01' : 'JAN', 
'02' : 'FEB' ,
'03' : 'MAR', 
'04' : 'APR', 
'05' : 'MAY' ,
'06' : 'JUN' ,
'07' : 'JUL' ,
'08' : 'AUG' ,
'09' : 'SEP' ,
'10':  'OCT' ,
'11' : 'NOV', 
'12' : 'DEC'
}
expiry = str(input('enter the expiry(Eg: 20210916 ) : '))
is_last_week=str(input('is last week Eg(y or n ):'))
money_in_account = float(input('enter the amount of money in the account in lakhs(Eg: 2) :'))
lots = int(np.floor(money_in_account/1.5)*25)
day=int(input('enter the no. of days ellapsed since strategy implimentation :'))
if is_last_week=='n':
    main_str="BANKNIFTY"+expiry[2:4]+month_mapping[expiry[4:6]]+expiry[-2:]
elif is_last_week=='y':
    main_str="BANKNIFTY"+expiry[2:4]+month_end_mapping[expiry[4:6]]

#%%
def Is_last_week(is_last_week):
    a=calendar.monthcalendar(int(expiry[:4]),int(expiry[4:6]))
    return 0

#%%
def new_short_straddle():  #do not try running this function seperately. this is just an add on to strangle.  
    while True:
        brk=0                
        #square off all positions
        pos=fyers.positions()['netPositions']
        for i in range(0, len(pos)):
            if pos[i]['symbol'][4:18] == main_str and pos[i]['symbol'][23:]=='PE' and pos[i]['sellQty']-pos[i]['buyQty']-pos[i]['netQty']>0  :
                pe_index=i
            elif pos[i]['symbol'][4:18] == main_str and pos[i]['symbol'][23:]=='CE' and pos[i]['sellQty']-pos[i]['buyQty']-pos[i]['netQty']>0  :
                ce_index=i
        data = [{ "symbol":pos[pe_index]['symbol'],
                      "qty":lots,
                      "type":2,  
                      "side":1, 
                      "productType":"CNC",   
                      "limitPrice":0,
                      "stopPrice":0 ,
                      "disclosedQty":0, 
                      "validity":"DAY", 
                      "offlineOrder":"False", 
                      "stopLoss":0,  
                      "takeProfit":0
                    },
                    {
                      "symbol":pos[ce_index]['symbol'],
                      "qty":lots,
                      "type":2,  
                      "side":1, 
                      "productType":"CNC",   
                      "limitPrice":0,
                      "stopPrice":0 ,
                      "disclosedQty":0, 
                      "validity":"DAY", 
                      "offlineOrder":"False", 
                      "stopLoss":0,  
                      "takeProfit":0
                    }]
        fyers.place_basket_orders(data)

        req_list_={"symbols":"NSE:NIFTYBANK-INDEX"}        
        a=fyers.quotes(req_list_)
        x=a['d'][0]['v']['lp']
        data=[{ "symbol":'NSE:'+main_str+str(round(x/100)*100)+'CE',
           "qty":lots,
           "type":2,  
           "side":-1, 
           "productType":"CNC",   
           "limitPrice":0,
           "stopPrice":0 ,
           "disclosedQty":0, 
           "validity":"DAY", 
           "offlineOrder":"False", 
           "stopLoss":0,  
           "takeProfit":0
         },
         {
           "symbol":'NSE:'+main_str+str(round(x/100)*100)+'PE',
           "qty":lots,
           "type":2,  
           "side":-1, 
           "productType":"CNC",   
           "limitPrice":0,
           "stopPrice":0 ,
           "disclosedQty":0, 
           "validity":"DAY", 
           "offlineOrder":"False", 
           "stopLoss":0,  
           "takeProfit":0
         }]
        fyers.place_basket_orders(data) 
        Total_value_old=float('inf')

        while True :
            b=fyers.quotes({'symbol':'NSE:'+main_str+str(round(x/100)*100)+'PE'})
            c=fyers.quotes({'symbol':'NSE:'+main_str+str(round(x/100)*100)+'CE'})
            ce_lastrate=b['d'][0]['v']['lp']
            pe_lastrate=c['d'][0]['v']['lp']
            Total_value_new=ce_lastrate+pe_lastrate
            if Total_value_new<Total_value_old:
                Stop_loss=Total_value_new*1.2
                Total_value_old=Total_value_new
            if Total_value_new>Stop_loss :
                brk=1
            if brk==1:
                ind_time = datetime.now(timezone("Asia/Kolkata")).strftime('%Y-%m-%d %H:%M:%S.%f')
                print(ind_time)
                print('#########                                         stoplosshit                                         #########')
                break
#%%
if day!=0:
    pos=fyers.positions()['netPositions']
    for i in range(0, len(pos)):
        if pos[i]['symbol'][4:18] == main_str and pos[i]['symbol'][23:]=='PE' and pos[i]['sellQty']-pos[i]['buyQty']-pos[i]['netQty']>0  :
            pe_index=i
            Current_PE_strikeprice=pos[i]['symbol'][18:23]
        elif pos[i]['symbol'][4:18] == main_str and pos[i]['symbol'][23:]=='CE' and pos[i]['sellQty']-pos[i]['buyQty']-pos[i]['netQty']>0  :
            ce_index=i
            Current_CE_strikeprice=pos[i]['symbol'][18:23]
    CE_req='NSE:'+main_str+Current_CE_strikeprice+'CE'
    PE_req='NSE:'+main_str+Current_PE_strikeprice+'PE'

#%%
req_list_={"symbols":"NSE:NIFTYBANK-INDEX"}        
a=fyers.quotes(req_list_)
x=a['d'][0]['v']['lp']                                 
req_list_PE={"symbols":"NSE:"+main_str+str(round(x/100)*100)+"PE"}  
req_list_CE={'symbols':"NSE:"+main_str+str(round(x/100)*100)+"CE"}
req_list_PE_strikeprice=[round(x/100)*100]
req_list_CE_strikeprice=[round(x/100)*100]
for i in range(1,25):
    req_list_PE['symbols']="NSE:"+main_str+str(round(x/100)*100+i*100)+"PE,"+req_list_PE['symbols']+",NSE:"+main_str+str(round(x/100)*100-i*100)+"PE"
    req_list_PE_strikeprice=[round(x/100)*100+i*100]+req_list_PE_strikeprice+[round(x/100)*100-i*100]
    req_list_CE['symbols']="NSE:"+main_str+str(round(x/100)*100-i*100)+"CE,"+req_list_CE['symbols']+",NSE:"+main_str+str(round(x/100)*100+i*100)+"CE"
    req_list_CE_strikeprice=[round(x/100)*100-i*100]+req_list_CE_strikeprice+[round(x/100)*100+i*100]
live_PE=fyers.quotes(req_list_PE)
live_PE_lastrate=[]
live_CE_lastrate=[]
live_CE = fyers.quotes(req_list_CE)
for j in range(0,49):
    live_PE_lastrate=live_PE_lastrate+[live_PE['d'][j]['v']['lp']]
    live_CE_lastrate = live_CE_lastrate+[live_CE['d'][j]['v']['lp']]
CE_index_strikeprice=np.argmin(np.abs(np.array(live_CE_lastrate)-115))
CE_hedge_index_strikeprice = np.argmin(np.abs(np.array(live_CE_lastrate)-10))
PE_index_strikeprice=np.argmin(np.abs(np.array(live_PE_lastrate)-115))
PE_hedge_index_strikeprice = np.argmin(np.abs(np.array(live_PE_lastrate)-10))
CE_upper=req_list_CE_strikeprice[CE_index_strikeprice]
CE_hedge=req_list_CE_strikeprice[CE_hedge_index_strikeprice]
PE_lower=req_list_PE_strikeprice[PE_index_strikeprice]
PE_hedge=req_list_PE_strikeprice[PE_hedge_index_strikeprice]

#%%

#short_strangle(<symbol>,<List of sell strike price>,<qty>,<expiry>,<Order Type>)
#strategy.short_strangle('banknifty',[str(PE_lower),str(CE_upper)],'25','20210902','D')
#iron_condor(<symbol>,<List of buy strike prices>,<List of sell strike price>,<qty>,<expiry>,<Order Type>)
if day==0:
    #short_strangle(<symbol>,<List of sell strike price>,<qty>,<expiry>,<Order Type>)
    #strategy.short_strangle("banknifty",[str(PE_lower),str(CE_upper)],str(lots),expiry,'D')
    data = [{ "symbol":'NSE:'+main_str+str(CE_hedge)+'CE',
              "qty":lots,
              "type":2,  
              "side":1, 
              "productType":"CNC",   
              "limitPrice":0,
              "stopPrice":0 ,
              "disclosedQty":0, 
              "validity":"DAY", 
              "offlineOrder":"False", 
              "stopLoss":0,  
              "takeProfit":0
            },
            {
              "symbol":'NSE:'+main_str+str(PE_hedge)+'PE',
              "qty":lots,
              "type":2,  
              "side":1, 
              "productType":"CNC",   
              "limitPrice":0,
              "stopPrice":0 ,
              "disclosedQty":0, 
              "validity":"DAY", 
              "offlineOrder":"False", 
              "stopLoss":0,  
              "takeProfit":0
            },
            {
            "symbol":'NSE:'+main_str+str(CE_upper)+'CE',
            "qty":lots,
            "type":2,  
            "side":-1, 
            "productType":"CNC",   
            "limitPrice":0,
            "stopPrice":0 ,
            "disclosedQty":0, 
            "validity":"DAY", 
            "offlineOrder":"False", 
            "stopLoss":0,  
            "takeProfit":0
            },
            {
            "symbol":'NSE:'+main_str+str(PE_lower)+'CE',
            "qty":lots,
            "type":2,  
            "side":-1, 
            "productType":"CNC",   
            "limitPrice":0,
            "stopPrice":0 ,
            "disclosedQty":0, 
            "validity":"DAY", 
            "offlineOrder":"False", 
            "stopLoss":0,  
            "takeProfit":0
            }]
    fyers.place_basket_orders(data)
    positions = fyers.positions()['netPositions']
    CE_req = 'NSE:'+main_str+str(CE_upper)+'CE'
    PE_req = 'NSE:'+main_str+str(PE_lower)+'PE'
#%%
Total_value_old=float('inf')
PE_req_old = ' '
CE_req_old = ' '
loop_control=0
brk=0
turn=0
while True:
    req={"symbols":"NSE:NIFTYBANK-INDEX"}        
    a=fyers.quotes(req)
    x=a['d'][0]['v']['lp']     #int
    req_list_PE={"symbols":"NSE:"+main_str+str(round(x/100)*100)+"PE"}  
    req_list_CE={'symbols':"NSE:"+main_str+str(round(x/100)*100)+"CE"}
    for i in range(1,25):
        req_list_PE['symbols']="NSE:"+main_str+str(round(x/100)*100+i*100)+"PE,"+req_list_PE['symbols']+",NSE:"+main_str+str(round(x/100)*100-i*100)+"PE"
        req_list_CE['symbols']="NSE:"+main_str+str(round(x/100)*100-i*100)+"CE,"+req_list_CE['symbols']+",NSE:"+main_str+str(round(x/100)*100+i*100)+"CE"
    pos = fyers.positions()['netPositions']
    for i in range(0, len(pos)):
        if pos[i]['symbol'][4:18] == main_str and pos[i]['symbol'][23:]=='PE' and pos[i]['sellQty']-pos[i]['buyQty']-pos[i]['netQty']>0  :
            pe_index=i
            Current_PE_strikeprice=pos[i]['symbol'][18:23]
            CE_req='NSE:'+main_str+Current_CE_strikeprice+'CE'
        elif pos[i]['symbol'][4:18] == main_str and pos[i]['symbol'][23:]=='CE' and pos[i]['sellQty']-pos[i]['buyQty']-pos[i]['netQty']>0  :
            ce_index=i
            Current_CE_strikeprice=pos[i]['symbol'][18:23]
            PE_req='NSE:'+main_str+Current_PE_strikeprice+'PE'
    req_list_={'symbols':CE_req+','+PE_req}
    if loop_control==1 and CE_req[18:23]==CE_req_old and PE_req[18:23]==PE_req_old:
        print('Sorry for the inconvenience caused. Some of the orders were not executed. Please do the trades manually')
        break
    elif loop_control==1 and CE_req[18:23]!=CE_req_old and PE_req[18:23]==PE_req_old:
        loop_control=0
    elif loop_control==1 and CE_req[18:23]==CE_req_old and PE_req[18:23]!=PE_req_old:
        loop_control=0
    b=fyers.quotes(req_list_)
    ce_lastrate=b['d'][0]['v']['lp'] 
    pe_lastrate=b['d'][1]['v']['lp']

    if ce_lastrate>2*pe_lastrate and int(CE_req[18:23])-int(PE_req[18:23])>0:
        ind_time = datetime.now(timezone("Asia/Kolkata")).strftime('%Y-%m-%d %H:%M:%S.%f')
        print(ind_time)
        print('Current CE Strikeprice: ',Current_CE_strikeprice)
        print('ce_lastrate: ', ce_lastrate)
        print('Current PE Strikeprice: ',Current_PE_strikeprice)
        print('pe_lastrate: ',pe_lastrate)

        #the above step is taken because the delta(change in option price per unit change in stock price) will become so low that the further decrease in pe_lastrate will be far lower than the increase in ce_lastrate when stock price increases from the price it is now trading
        PE_req_old = PE_req[18:23]
        nice=req_list_["symbols"].split(',')
        for k in range(0,len(pos)):
            if nice[1]==pos[k]['symbol']  and loop_control==0:
                awesome_ammu=k   
                a=fyers.quotes(req)
                x=a['d'][0]['v']['lp'] 
                req_list_PE={"symbols":"NSE:"+main_str+str(round(x/100)*100)+"PE"}  
                req_list_PE_strikeprice=[round(x/100)*100]
                for i in range(1,25):
                    req_list_PE['symbols']="NSE:"+main_str+str(round(x/100)*100+i*100)+"PE,"+req_list_PE['symbols']+",NSE:"+main_str+str(round(x/100)*100-i*100)+"PE"
                    req_list_PE_strikeprice=[round(x/100)*100+i*100]+req_list_PE_strikeprice+[round(x/100)*100-i*100]
                live_PE=fyers.quotes(req_list_PE)
                live_PE_lastrate=[]
                for j in range(0,49):
                    live_PE_lastrate=live_PE_lastrate+[live_PE['d'][j]['v']['lp']]
                PE_index_strikeprice=np.argmin(np.abs(np.array(live_PE_lastrate)-0.85*ce_lastrate))
                #exit pe
                ind_time = datetime.now(timezone("Asia/Kolkata")).strftime('%Y-%m-%d %H:%M:%S.%f')
                print(ind_time)
                print('exit(bought) pe at srikeprice:  ', PE_req_old)
                data=[  { "symbol":pos[awesome_ammu]['symbol'],
                                "qty":lots,
                                "type":2,  
                                "side":1, 
                                "productType":"CNC",   
                                "limitPrice":0,
                                "stopPrice":0 ,
                                "disclosedQty":0, 
                                "validity":"DAY", 
                                "offlineOrder":"False", 
                                "stopLoss":0,  
                                "takeProfit":0
                            },
                            { "symbol":'NSE:'+main_str+str(req_list_PE_strikeprice[PE_index_strikeprice])+'PE',
                              "qty":lots,
                              "type":2,  
                              "side":-1, 
                              "productType":"CNC",   
                              "limitPrice":0,
                              "stopPrice":0 ,
                              "disclosedQty":0, 
                              "validity":"DAY", 
                              "offlineOrder":"False", 
                              "stopLoss":0,  
                              "takeProfit":0
                            }]
                #sell pe which is 80 to 95% of ce
                fyers.place_basket_orders(data)
                ind_time = datetime.now(timezone("Asia/Kolkata")).strftime('%Y-%m-%d %H:%M:%S.%f')
                print(ind_time)
                print('re entry(Sold) pe at strikeprice: ',req_list_PE_strikeprice[PE_index_strikeprice])
                PE_req = req_list_PE[PE_index_strikeprice]
                print('New PE_req is : ',PE_req)
                loop_control=1
                break
        


    elif pe_lastrate>2*ce_lastrate and int(CE_req[18:23])-int(PE_req[18:23])>0:
        ind_time = datetime.now(timezone("Asia/Kolkata")).strftime('%Y-%m-%d %H:%M:%S.%f')
        print(ind_time)
        print('Current CE Strikeprice: ',Current_CE_strikeprice)
        print('ce_lastrate: ', ce_lastrate)
        print('Current PE Strikeprice: ',Current_PE_strikeprice)
        print('pe_lastrate: ',pe_lastrate)
        #the above step is taken because the delta(change in option price per unit change in stock price) will become so low that the further decrease in ce_lastrate will be far lower than the increase in pe_lastrate when stock price decreases from the price it is now trading
        CE_req_old = CE_req[18:23]
        nice=req_list_["symbols"].split(',')
        for k in range(0,len(positions)):
            if nice[0]==pos[k]['symbol']  and loop_control==0:
                awesome_ammu=k
                a=fyers.quotes(req)
                x=a['d'][0]['v']['lp'] 
                req_list_CE={"symbols":"NSE:"+main_str+str(round(x/100)*100)+"CE"}  
                req_list_CE_strikeprice=[round(x/100)*100]
                for i in range(1,25):
                    req_list_CE['symbols']="NSE:"+main_str+str(round(x/100)*100+i*100)+"CE,"+req_list_CE['symbols']+",NSE:"+main_str+str(round(x/100)*100-i*100)+"CE"
                    req_list_CE_strikeprice=[round(x/100)*100+i*100]+req_list_CE_strikeprice+[round(x/100)*100-i*100]
                live_CE=fyers.quotes(req_list_CE)
                live_CE_lastrate=[]
                for j in range(0,49):
                    live_CE_lastrate=live_CE_lastrate+[live_CE['d'][j]['v']['lp']]
                CE_index_strikeprice=np.argmin(np.abs(np.array(live_CE_lastrate)-0.85*pe_lastrate))
                #exit ce
                ind_time = datetime.now(timezone("Asia/Kolkata")).strftime('%Y-%m-%d %H:%M:%S.%f')
                print(ind_time)
                print('exit(bought) pe at srikeprice:  ', CE_req_old)
                data=[{ "symbol":pos[awesome_ammu]['symbol'],
                                "qty":lots,
                                "type":2,  
                                "side":1, 
                                "productType":"CNC",   
                                "limitPrice":0,
                                "stopPrice":0 ,
                                "disclosedQty":0, 
                                "validity":"DAY", 
                                "offlineOrder":"False", 
                                "stopLoss":0,  
                                "takeProfit":0
                            },
                            { "symbol":'NSE:'+main_str+str(req_list_CE_strikeprice[CE_index_strikeprice])+'CE',
                              "qty":lots,
                              "type":2,  
                              "side":-1, 
                              "productType":"CNC",   
                              "limitPrice":0,
                              "stopPrice":0 ,
                              "disclosedQty":0, 
                              "validity":"DAY", 
                              "offlineOrder":"False", 
                              "stopLoss":0,  
                              "takeProfit":0
                            }]
                fyers.place_basket_orders(data)
                ind_time = datetime.now(timezone("Asia/Kolkata")).strftime('%Y-%m-%d %H:%M:%S.%f')
                print(ind_time)
                print('re entry(Sold) pe at strikeprice: ',req_list_CE_strikeprice[CE_index_strikeprice])
                nice=req_list_CE['symbols'].split(',')
                CE_req = nice[CE_index_strikeprice]
                print('New PE_req is : ',CE_req)
                loop_control=1
                break         
    #now=datetime.now()
    if int(CE_req[18:23])-int(PE_req[18:23])<=0 :   #or now.strftime('%H %M')=='15 15'
        if turn==0:
            turn=1
        elif turn==1:
            Total_value_new=ce_lastrate+pe_lastrate
            if Total_value_new<Total_value_old:
                Stop_loss=Total_value_new*1.15
                Total_value_old=Total_value_new
            if Total_value_new>Stop_loss :
                brk=1
                print('stoplosshit')
                new_short_straddle()           
    if brk==1:
        break

# %%
