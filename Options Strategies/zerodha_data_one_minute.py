#%%
##Working Code 
#variables to change
from kiteconnect import KiteConnect, KiteTicker
import datetime
import json
import pandas as pd
import glob
import os
expiry_date = datetime.date(2023,5,25)
expiry_date_str = '2023-05-25'
from_date='2023-05-01 09:15:00'
to_date='2023-05-25 15:30:00'
bank_nifty_instrument_token = 260105
index_ticker = 'BANKNIFTY'
index_ticker_wk = 'BANKNIFTYWK'
ticker_name = 'BANKNIFTY'
file_name_ticker = 'BNF'
#%%
#Initiate Kiteconnect
auth = "enctoken NaEyXjisPrAlGk0a5PqciQ7jmEaA29ZeFdN/d2XyinQgUV92E3T6DMVuUmjRCN8fR6y7qBuB0u6JuUDM0/SKV50KfxiuX02crpNwWmpLyhW7OBRRGh0onQ=="
cookie = "kf_session=Z4yTMH8eX65QJEz7w6jJ1dUk4382OitM; user_id=UW1001; public_token=7T0IhvBMTtzFJwB7kpyrocH8oNRvgh0f; enctoken=NaEyXjisPrAlGk0a5PqciQ7jmEaA29ZeFdN/d2XyinQgUV92E3T6DMVuUmjRCN8fR6y7qBuB0u6JuUDM0/SKV50KfxiuX02crpNwWmpLyhW7OBRRGh0onQ==; _cfuvid=BGDX9ma2dYksUzcuQZbZAiSqwzsk4DNQZ.a6YUpPOI0-1685010216365-0-604800000"
kite = KiteConnect(authorization_manual=auth, cookie_manual=cookie)
#%%
#Get all instrument tokens
import pandas as pd
tickers = pd.DataFrame(kite.instruments())
temp_tickers = tickers[tickers['expiry'] ==  expiry_date]
#%%
ce_pe_data = temp_tickers[(temp_tickers.name == ticker_name) &( (temp_tickers.instrument_type == 'CE') | (temp_tickers.instrument_type == 'PE'))]
ce_pe_data = ce_pe_data[['instrument_token', 'strike', 'instrument_type']]
final_instrument_list = ce_pe_data.instrument_token.tolist()
final_strike = ce_pe_data.strike.tolist()
final_instrument_type = ce_pe_data.instrument_type.tolist()
# %%
##Download data and store as json
root_folder = 'json_dump/'
files = glob.glob('json_dump/*.json')
for file in files:
    os.remove(file)
for entry in range(0, len(final_instrument_list)):
    option_data = kite.historical_data(instrument_token=final_instrument_list[entry], from_date=from_date, to_date=to_date, interval='minute',oi=True)
    option_df = pd.DataFrame(option_data)
    file_name = root_folder+str(final_strike[entry])+"_"+final_instrument_type[entry]+".json"
    option_df.to_json(file_name)

#%%
#Download BANKNIFTY data
banknifty_file = 'csv_data/banknifty.json'
os.remove(banknifty_file)
bank_nifty_data = kite.historical_data(instrument_token=bank_nifty_instrument_token, from_date=from_date, to_date=to_date, interval='minute')
bank_nifty_data_df = pd.DataFrame(bank_nifty_data)
bank_nifty_data_df.to_json(banknifty_file)
#%%
#Open the json files and read
files = glob.glob('json_dump/*.json')
df_final = pd.DataFrame()
for file in files:
    print(file)
    split_str = file.split('/')
    f = split_str[1].split('_')
    print(f)
    strike = int(float(f[0]))
    option_type = f[1].split('.')[0]
    print(strike)
    print(option_type)
    df = pd.read_json(file)
    df['Ticker'] = index_ticker_wk+str(strike)+option_type
    df_final = df_final.append(df, ignore_index=True)
#Get banknifty data
df = pd.read_json(banknifty_file)
df['Ticker'] = index_ticker
df['oi'] = 0
df_final = df_final.append(df, ignore_index=True)

df_final = df_final.rename(columns={'oi':'Open Interest', 'date':'Date/Time', 'open':'Open',
                                'close':'Close', 'high':'High', 'low':'Low', 'volume':'Volume'})
df_final['Date/Time'] = df_final['Date/Time'] + pd.Timedelta(minutes=330)
file_name = expiry_date_str+"WEEKLY-expiry_data_"+file_name_ticker+"_Options.csv"
final_path = 'csv_data/'+file_name
df_final.to_csv(final_path)
# %%
# %%
