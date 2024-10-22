#%%
# Update scripmaster file every week
import numpy as np
import pandas as pd
from time import sleep, strftime
from py5paisa import FivePaisaClient
from py5paisa.strategy import *
from cred import *
from datetime import datetime 
import requests
from pytz import timezone 

#inputs to the code
expiry = str(input('enter the expiry(Eg: "20210916" ) : '))
money_in_account = float(input('enter the amount of money in the account in lakhs(Eg: 2) :'))
lots = int(np.floor(money_in_account/1.5)*25)
day=int(input('enter the no. of days ellapsed since strategy implimentation :'))
url = "https://images.5paisa.com/website/scripmaster-csv-format.csv"


#download and reading scriptmaster
r = requests.get(url)
open('scripmaster-csv-format.csv', 'wb').write(r.content)
filename = 'scripmaster-csv-format.csv'
script = pd.read_csv(filename)
def fix(script):
    for i in range(0,len(script)):
        script['Name'].at[i]=script['Name'][i][:25]
        script['Expiry'].at[i]=script['Expiry'][i][:10]
    return script

script=fix(script)


# formatting the input data 
temp={1:'JAN',
            2:'FEB',
            3:'MAR',
            4:'APR',
            5:'MAY',
            6:'JUN',
            7:'JUL',
            8:'AUG',
            9:'SEP',
            10:'OCT',
            11:'NOV',
            12:'DEC'}
main_str="BANKNIFTY "+expiry[-2:]+" "+temp[int(expiry[4:6])]+" "+expiry[:4]+" "
main_str_format = main_str[:14]+main_str[14:16].lower()+main_str[16:] 
main_str_pe = main_str+"PE "
main_str_ce = main_str+"CE "
main_str_format_pe=main_str_format+"PE "
main_str_format_ce=main_str_format+"CE "
expiry_format= expiry[:4]+'-'+expiry[4:6]+'-'+expiry[6:]

# Client login credentials
cred={
    "APP_NAME":"5P53784053",
    "APP_SOURCE":"8023",
    "USER_ID":"y4JUrjToSOR",
    "PASSWORD":"y0tc7unqQAV",
    "USER_KEY":"DrmeltLdZo82SKaxWJoeMALor1Xaiqk5",
    "ENCRYPTION_KEY":"ANb7Y0ouVD5iX0jcPGwPMIEyQnwPjxuI"
    }
Client = FivePaisaClient(email='chandinimadduru123@gmail.com', passwd='amar@0987',dob='19950820', cred=cred)
Client.login()
#%%

# if the 
if day!=0:
    pos=Client.positions()
    for i in range(0, len(pos)):
        if pos[i]['ScripName'][:25] == main_str_format_pe and  pos[i]['SellQty']-pos[i]['BuyQty']-pos[i]['NetQty']>0 :
            Current_PE_strikeprice=pos[i]['ScripName'][25:30]
        elif pos[i]['ScripName'][:25] == main_str_format_ce and  pos[i]['SellQty']-pos[i]['BuyQty']-pos[i]['NetQty']>0:
            Current_CE_strikeprice=pos[i]['ScripName'][25:30]
'''
# Fetches holdings
Client.holdings()
# Fetches margin
Client.margin()
# Fetches positions
Client.positions()
# Fetches the order book of the client
Client.order_book()
'''

#%%
#NOTE : Symbol has to be in the same format as specified in the example below.
#banknifty scripcode=999920005
#N	C	999920005	BANKNIFTY 	EQ	1980-01-01 00:00:00	EQ	0	Z  BANKNIFTY                                         
req_list_=[{"Exch":"N","ExchType":"C","Symbol":"BANKNIFTY","Scripcode":"999920005","OptionType":"EQ"}]          
a=Client.fetch_market_feed(req_list_)
#x = input('Bank Nifty Value on the day of taking the trades')
x=a['Data'][0]['LastRate']
req_list_PE=[{"Exch":"N","ExchType":"D","Symbol":main_str_pe+str(round(x/100)*100)+".00","Expiry":expiry,"StrikePrice":str(round(x/100)*100),"OptionType":"PE"}]
req_list_CE=[{"Exch":"N","ExchType":"D","Symbol":main_str_ce+str(round(x/100)*100)+".00","Expiry":expiry,"StrikePrice":str(round(x/100)*100),"OptionType":"CE"}]
req_list_PE_strikeprice=[round(x/100)*100]
req_list_CE_strikeprice=[round(x/100)*100]
for i in range(1,25):
    req_list_PE=req_list_PE+[{"Exch":"N","ExchType":"D","Symbol": main_str_pe+str(round(x/100)*100-i*100)+".00","Expiry":expiry,"StrikePrice":str(round(x/100)*100-i*100),"OptionType":"PE"}] 
    req_list_PE_strikeprice=req_list_PE_strikeprice+[round(x/100)*100-i*100]
    req_list_CE=req_list_CE+[{"Exch":"N","ExchType":"D","Symbol":main_str_ce+str(round(x/100)*100+i*100)+".00","Expiry":expiry,"StrikePrice":str(round(x/100)*100+i*100),"OptionType":"CE"}] 
    req_list_CE_strikeprice=req_list_CE_strikeprice+[round(x/100)*100+i*100]
live_PE=Client.fetch_market_feed(req_list_PE)
live_PE_lastrate=[]
live_CE_lastrate=[]
live_CE = Client.fetch_market_feed(req_list_CE)
for j in range(0,25):
    live_PE_lastrate=live_PE_lastrate+[live_PE['Data'][j]['LastRate']]
    live_CE_lastrate = live_CE_lastrate+[live_CE['Data'][j]['LastRate']]
CE_index_strikeprice=np.argmin(np.abs(np.array(live_CE_lastrate)-115))
CE_hedge_index_strikeprice = np.argmin(np.abs(np.array(live_CE_lastrate)-10))
PE_index_strikeprice=np.argmin(np.abs(np.array(live_PE_lastrate)-115))
PE_hedge_index_strikeprice = np.argmin(np.abs(np.array(live_PE_lastrate)-10))
CE_upper=req_list_CE_strikeprice[CE_index_strikeprice]
CE_hedge=req_list_CE_strikeprice[CE_hedge_index_strikeprice]
PE_lower=req_list_PE_strikeprice[PE_index_strikeprice]
PE_hedge=req_list_PE_strikeprice[PE_hedge_index_strikeprice]

#%%
strategy=strategies(user="chandinimadduru123@gmail.com", passw="amar@0987", dob="19950820",cred=cred)
#short_strangle(<symbol>,<List of sell strike price>,<qty>,<expiry>,<Order Type>)
#strategy.short_strangle('banknifty',[str(PE_lower),str(CE_upper)],'25','20210902','D')
#iron_condor(<symbol>,<List of buy strike prices>,<List of sell strike price>,<qty>,<expiry>,<Order Type>)
if day==0:
    #short_strangle(<symbol>,<List of sell strike price>,<qty>,<expiry>,<Order Type>)
    #strategy.short_strangle("banknifty",[str(PE_lower),str(CE_upper)],str(lots),expiry,'D')

    strategy.iron_condor("banknifty",[str(CE_hedge),str(PE_hedge)],[str(PE_lower),str(CE_upper)],str(lots),expiry,'D')
    sleep(3)
    positions = Client.positions()
    CE_req = req_list_CE[CE_index_strikeprice]
    PE_req = req_list_PE[PE_index_strikeprice]
#%%
if day!=0:
    for i in range(0,len(req_list_CE)):
        if req_list_CE[i]['StrikePrice']==Current_CE_strikeprice:
            CE_req=req_list_CE[i]
            break
    for j in range(0,len(req_list_PE)):
        if req_list_PE[j]['StrikePrice']==Current_PE_strikeprice:
            PE_req=req_list_PE[j]
            break
Total_value_old=float('inf')
PE_req_old = ' '
CE_req_old = ' '
loop_control=0
brk=0
#%%
while True:
    req=[{"Exch":"N","ExchType":"C","Symbol":"BANKNIFTY","Scripcode":"999920005","OptionType":"EQ"}]          
    a=Client.fetch_market_feed(req)
    x=a['Data'][0]['LastRate']     #int
    req_list_PE=[{"Exch":"N","ExchType":"D","Symbol":main_str_pe+str(round(x/100)*100)+".00","Expiry":expiry,"StrikePrice":str(round(x/100)*100),"OptionType":"PE"}]
    req_list_CE=[{"Exch":"N","ExchType":"D","Symbol":main_str_ce+str(round(x/100)*100)+".00","Expiry":expiry,"StrikePrice":str(round(x/100)*100),"OptionType":"CE"}]
    req_list_PE_strikeprice=[round(x/100)*100]
    req_list_CE_strikeprice=[round(x/100)*100]
    for i in range(1,25):
        req_list_PE=req_list_PE+[{"Exch":"N","ExchType":"D","Symbol": main_str_pe+str(round(x/100)*100-i*100)+".00","Expiry":expiry,"StrikePrice":str(round(x/100)*100-i*100),"OptionType":"PE"}] 
        req_list_PE_strikeprice=req_list_PE_strikeprice+[round(x/100)*100-i*100]
        req_list_CE=req_list_CE+[{"Exch":"N","ExchType":"D","Symbol":main_str_ce+str(round(x/100)*100+i*100)+".00","Expiry":expiry,"StrikePrice":str(round(x/100)*100+i*100),"OptionType":"CE"}] 
        req_list_CE_strikeprice=req_list_CE_strikeprice+[round(x/100)*100+i*100]
    live_PE=Client.fetch_market_feed(req_list_PE)
    live_PE_lastrate=[]
    live_CE_lastrate=[]
    live_CE = Client.fetch_market_feed(req_list_CE)
    positions = Client.positions()
    for i in range(0, len(positions)):
        if positions[i]['ScripName'][:25] == main_str_format_pe and  positions[i]['SellQty']-positions[i]['BuyQty']-positions[i]['NetQty']>0 :
            Current_PE_strikeprice=positions[i]['ScripName'][25:30]
        elif positions[i]['ScripName'][:25] == main_str_format_ce and  positions[i]['SellQty']-positions[i]['BuyQty']-positions[i]['NetQty']>0 :
            Current_CE_strikeprice = positions[i]['ScripName'][25:30]
    
    for i in range(0,len(req_list_CE)):
        if req_list_CE[i]['StrikePrice']==Current_CE_strikeprice:
            CE_req=req_list_CE[i]
            break
    for j in range(0,len(req_list_PE)):
        if req_list_PE[j]['StrikePrice']==Current_PE_strikeprice:
            PE_req=req_list_PE[j]
            break
    req_list_=[CE_req,PE_req]
    if loop_control==1 and CE_req['StrikePrice']==CE_req_old and PE_req['StrikePrice']==PE_req_old:
        print('Sorry for the inconvenience caused. Some of the orders were not executed. Please do the trades manually')
        break
    elif loop_control==1 and CE_req['StrikePrice']!=CE_req_old and PE_req['StrikePrice']==PE_req_old:
        loop_control=0
    elif loop_control==1 and CE_req['StrikePrice']==CE_req_old and PE_req['StrikePrice']!=PE_req_old:
        loop_control=0
    b=Client.fetch_market_feed(req_list_)
    ce_lastrate=b['Data'][0]['LastRate']
    pe_lastrate=b['Data'][1]['LastRate']

    if ce_lastrate>=2*pe_lastrate and int(CE_req['StrikePrice'])-int(PE_req['StrikePrice'])>300:
        ind_time = datetime.now(timezone("Asia/Kolkata")).strftime('%Y-%m-%d %H:%M:%S.%f')
        print(ind_time)
        print('Current CE Strikeprice: ',Current_CE_strikeprice)
        print('ce_lastrate: ', ce_lastrate)
        print('Current PE Strikeprice: ',Current_PE_strikeprice)
        print('pe_lastrate: ',pe_lastrate)

        #the above step is taken because the delta(change in option price per unit change in stock price) will become so low that the further decrease in pe_lastrate will be far lower than the increase in ce_lastrate when stock price increases from the price it is now trading
        PE_req_old = PE_req['StrikePrice']
        for k in range(0,len(positions)):
            if req_list_[1]['Symbol']==str.upper(positions[k]['ScripName']) and loop_control==0:
                awesome_ammu=k   
                req=[{"Exch":"N","ExchType":"C","Symbol":"BANKNIFTY","Scripcode":"999920005","OptionType":"EQ"}]          
                a=Client.fetch_market_feed(req)
                x=a['Data'][0]['LastRate']
                req_list_PE=[{"Exch":"N","ExchType":"D","Symbol":main_str_pe+str(round(x/100)*100)+".00","Expiry":expiry,"StrikePrice":str(round(x/100)*100),"OptionType":"PE"}]
                req_list_PE_strikeprice=[round(x/100)*100]
                for i in range(1,25):
                    req_list_PE=req_list_PE+[{"Exch":"N","ExchType":"D","Symbol":main_str_pe+str(round(x/100)*100-i*100)+".00","Expiry":expiry,"StrikePrice":str(round(x/100)*100-i*100),"OptionType":"PE"}] 
                    req_list_PE_strikeprice=req_list_PE_strikeprice+[round(x/100)*100-i*100]
                live_PE=Client.fetch_market_feed(req_list_PE)
                live_PE_lastrate=[]
                for j in range(0,25):
                    live_PE_lastrate=live_PE_lastrate+[live_PE['Data'][j]['LastRate']]
                PE_index_strikeprice=np.argmin(np.abs(np.array(live_PE_lastrate)-0.85*ce_lastrate))
                #exit pe
                test_order = Order(order_type='B',exchange='N',exchange_segment='D', scrip_code=positions[awesome_ammu]['ScripCode'], quantity=lots,price=0,is_intraday=False,atmarket=True)
                Client.place_order(test_order)
                ind_time = datetime.now(timezone("Asia/Kolkata")).strftime('%Y-%m-%d %H:%M:%S.%f')
                print(ind_time)
                print('exit(bought) pe at srikeprice:  ', PE_req_old)

                #sell pe which is 80 to 95% of ce
                atemp =  script[script['Expiry']==expiry_format]
                atemp2=atemp[np.array(atemp['StrikeRate'])==req_list_PE_strikeprice[PE_index_strikeprice]]
                scripcode_=str(int(atemp2[atemp2['Name']==main_str_format_pe]['Scripcode']))
                test_order2=Order(order_type='S',exchange='N',exchange_segment='D', scrip_code=scripcode_, quantity=lots,price=0,is_intraday=False,atmarket=True)
                Client.place_order(test_order2)
                ind_time = datetime.now(timezone("Asia/Kolkata")).strftime('%Y-%m-%d %H:%M:%S.%f')
                print(ind_time)
                print('re entry(Sold) pe at strikeprice: ',req_list_PE_strikeprice[PE_index_strikeprice])
                PE_req = req_list_PE[PE_index_strikeprice]
                print('New PE_req is : ',PE_req)
                loop_control=1
                break
        


    elif pe_lastrate>=2*ce_lastrate and int(CE_req['StrikePrice'])-int(PE_req['StrikePrice'])>300:
        ind_time = datetime.now(timezone("Asia/Kolkata")).strftime('%Y-%m-%d %H:%M:%S.%f')
        print(ind_time)
        print('Current CE Strikeprice: ',Current_CE_strikeprice)
        print('ce_lastrate: ', ce_lastrate)
        print('Current PE Strikeprice: ',Current_PE_strikeprice)
        print('pe_lastrate: ',pe_lastrate)
        #the above step is taken because the delta(change in option price per unit change in stock price) will become so low that the further decrease in ce_lastrate will be far lower than the increase in pe_lastrate when stock price decreases from the price it is now trading
        CE_req_old = CE_req['StrikePrice']
        for k in range(0,len(positions)):
            if req_list_[0]['Symbol']==str.upper(positions[k]['ScripName']) and loop_control==0:
                awesome_ammu=k
                req=[{"Exch":"N","ExchType":"C","Symbol":"BANKNIFTY","Scripcode":"999920005","OptionType":"EQ"}]          
                a=Client.fetch_market_feed(req)
                x=a['Data'][0]['LastRate']
                req_list_CE=[{"Exch":"N","ExchType":"D","Symbol":main_str_ce+str(round(x/100)*100)+".00","Expiry":expiry,"StrikePrice":str(round(x/100)*100),"OptionType":"CE"}]
                req_list_CE_strikeprice=[round(x/100)*100]
                for i in range(1,25):
                    req_list_CE=req_list_CE+[{"Exch":"N","ExchType":"D","Symbol":main_str_ce+str(round(x/100)*100+i*100)+".00","Expiry":expiry,"StrikePrice":str(round(x/100)*100+i*100),"OptionType":"CE"}] 
                    req_list_CE_strikeprice=req_list_CE_strikeprice+[round(x/100)*100+i*100]
                live_CE=Client.fetch_market_feed(req_list_CE)
                live_CE_lastrate=[]
                for j in range(0,25):
                    live_CE_lastrate=live_CE_lastrate+[live_CE['Data'][j]['LastRate']]
                CE_index_strikeprice=np.argmin(np.abs(np.array(live_CE_lastrate)-0.85*pe_lastrate))
                #exit pe
                test_order = Order(order_type='B',exchange='N',exchange_segment='D', scrip_code=positions[awesome_ammu]['ScripCode'], quantity=lots,price=0,is_intraday=False,atmarket=True)
                Client.place_order(test_order)
                ind_time = datetime.now(timezone("Asia/Kolkata")).strftime('%Y-%m-%d %H:%M:%S.%f')
                print(ind_time)
                print('exit(bought) ce at srikeprice:  ', CE_req_old)
                #sell pe which is 80 to 95% of ce
                atemp =  script[script['Expiry']==expiry_format]
                atemp2=atemp[np.array(atemp['StrikeRate'])==req_list_CE_strikeprice[CE_index_strikeprice]]
                scripcode_=str(int(atemp2[atemp2['Name']==main_str_format_ce]['Scripcode']))                
                test_order2=Order(order_type='S',exchange='N',exchange_segment='D', scrip_code=scripcode_, quantity=lots,price=0,is_intraday=False,atmarket=True)
                Client.place_order(test_order2)
                ind_time = datetime.now(timezone("Asia/Kolkata")).strftime('%Y-%m-%d %H:%M:%S.%f')
                print(ind_time)
                print('re entry(Sold) ce at strikeprice: ',req_list_CE_strikeprice[CE_index_strikeprice])
                CE_req = req_list_CE[CE_index_strikeprice]
                print('New CE_req is : ',CE_req)
                loop_control=1
                break
    now=datetime.now()
    if (int(CE_req['StrikePrice'])-int(PE_req['StrikePrice'] ))<=300 :   #or now.strftime('%H %M')=='15 15'
        try: 
            straddle(expiry=expiry,strike=CE_req['StrikePrice'])
        except Exception:
            Total_value_new=ce_lastrate+pe_lastrate
            if Total_value_new<Total_value_old:
                Stop_loss=Total_value_new*1.15
                Total_value_old=Total_value_new
            if Total_value_new>Stop_loss :
                brk=1
                #square off all positions
                pos=Client.positions()
                for i in range(0, len(pos)):
                    if pos[i]['ScripName'][:25] == main_str_format_pe and  pos[i]['SellQty']-pos[i]['BuyQty']-pos[i]['NetQty']>0  :
                        Current_PE_strikeprice=pos[i]['ScripName'][25:30]
                    elif pos[i]['ScripName'][:25] == main_str_format_ce and  pos[i]['SellQty']-pos[i]['BuyQty']-pos[i]['NetQty']>0  :
                        Current_CE_strikeprice=pos[i]['ScripName'][25:30]
                for i in range(0, len(pos)):
                    if pos[i]['ScripName'][:25] == main_str_format_pe and  int(pos[i]['ScripName'][25:30])<int(Current_PE_strikeprice) and pos[i]['SellQty']-pos[i]['BuyQty']-pos[i]['NetQty']<0   :
                        PE_Hedge = pos[i]['ScripName'][25:30]
                    elif pos[i]['ScripName'][:25] == main_str_format_ce and  int(pos[i]['ScripName'][25:30])>int(Current_CE_strikeprice) and pos[i]['SellQty']-pos[i]['BuyQty']-pos[i]['NetQty']<0   :
                        CE_Hedge=pos[i]['ScripName'][25:30]
                test_order = Order(order_type='B',exchange='N',exchange_segment='D', scrip_code=str(int(script[script['FullName']==main_str_format_pe+PE_req['StrikePrice']+'.00']['Scripcode'])), quantity=lots,price=0,is_intraday=False,atmarket=True)
                Client.place_order(test_order)
                test_order = Order(order_type='B',exchange='N',exchange_segment='D', scrip_code=str(int(script[script['FullName']==main_str_format_ce+CE_req['StrikePrice']+'.00']['Scripcode'])), quantity=lots,price=0,is_intraday=False,atmarket=True)
                Client.place_order(test_order)
                test_order = Order(order_type='S',exchange='N',exchange_segment='D', scrip_code=str(int(script[script['FullName']==main_str_format_ce+str(CE_hedge)+'.00']['Scripcode'])), quantity=lots,price=0,is_intraday=False,atmarket=True)
                Client.place_order(test_order)
                test_order = Order(order_type='S',exchange='N',exchange_segment='D', scrip_code=str(int(script[script['FullName']==main_str_format_pe+str(PE_hedge)+'.00']['Scripcode'])), quantity=lots,price=0,is_intraday=False,atmarket=True)
                Client.place_order(test_order)
                print('stoplosshit')
    if brk==1:
        break

# %%
