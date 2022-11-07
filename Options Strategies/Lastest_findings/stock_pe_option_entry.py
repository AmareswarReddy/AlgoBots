#%%
from math import ceil, floor
import numpy as np
import pandas as pd
import json
from time import sleep, strftime
from py5paisa import FivePaisaClient

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
    client_list[client]['login']=FivePaisaClient(email=user, passwd=passw, dob=dob,cred=vinathi_cred)
    client_list[client]['login'].login()
    client_list[client]['lots']=round((client_list[client]['login'].margin()[0]['AvailableMargin']-200000)/180000)
    return client_list[client]

client_name   = 'vinathi'
prime_client=client_login(client=client_name)

def download_scrip_csv():
    import requests
    url = "https://images.5paisa.com/website/scripmaster-csv-format.csv"
    r = requests.get(url)
    if(r.status_code == 200):
        from io import StringIO
        s=str(r.content,'utf-8')
        data = StringIO(s) 
        df=pd.read_csv(data)
        return df
    else :
        return None
data =  download_scrip_csv()


#Gets all the Stocks 
a= data[(data['Exch'] == 'N') & (data['Series'] == 'EQ')]['Root'].unique()
#Gets all scripts with Derivatives
b= data[(data['Exch'] == 'N') & (data['Series'] == 'XX')]['Root'].unique()

#List of Stocks which has options
stocks_with_options = list(set(a) & set(b))

df_with_stock_options = data[(data['Exch'] == 'N') & (data['Series'] =='EQ') & (data['Root'].isin(stocks_with_options))]

scrip_code_dict = pd.Series(df_with_stock_options['Scripcode'].values, index = df_with_stock_options['Name']).to_dict()

# %%
def check_PE_option_sell(scrip_code, last_week_date, today_date):
    hist_data = prime_client['login'].historical_data('N', 'C', scrip_code, '1d', last_week_date, today_date)
    latest_close = hist_data['Close'].iloc[-1]
    open_5_day_earlier  = hist_data['Open'].iloc[0]
    open_4_day_earlier  = hist_data['Open'].iloc[1]
    try:
        check1 = math.floor(((latest_close - open_5_day_earlier)/latest_close)*100)
        check2 = math.floor(((latest_close - open_4_day_earlier)/latest_close)*100)
        if(check2 <= -10 or check1 <= -10):
            print(check2)
            print(check1)
            return True
        else:
            return False
    except:
        print("Eorro with this guy")
        return False
    

#%%
from datetime import date, timedelta
for i in range(0,30):
    today_date = date.today()-timedelta(days= i)
    last_week_date = today_date-timedelta(days= 7)
    print(today_date, last_week_date)
    import math
    for scrip in scrip_code_dict:
        can_sell_PE = check_PE_option_sell(scrip_code_dict[scrip],last_week_date, today_date)
        if can_sell_PE:
            print(scrip)
# %%
