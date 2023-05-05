#%%
import numpy as np
import re
import pandas as pd

def get_data(filename):
    print(filename)
    df = pd.read_csv(filename)
    df_banknifty = df[df['Ticker'].str.contains('BANKNIFTY')]
    df_banknifty_lastrate = df_banknifty[df_banknifty['Ticker'] == 'BANKNIFTY']
    df_banknifty_options = df_banknifty[df_banknifty['Ticker'].str.contains('BANKNIFTYWK')]
    from datetime import datetime, date, time
    df_banknifty_options['date_only'] = df_banknifty_options['Date/Time'].apply(lambda date:str(datetime.strptime(date, "%d-%m-%Y %H:%M:%S").date()))
    df_banknifty_grouped_by_time = df_banknifty_options.groupby(['date_only'])
    list_dts_str = list(df_banknifty_grouped_by_time.groups.keys())
    ##Get list of dates
    from datetime import datetime, date, time
    list_dates = list(set(map(lambda date:datetime.strptime(date, "%Y-%m-%d").date() , list_dts_str)))
    max_date = max(list_dates)
    print(max_date)
    final_df_list = []
    days_sort = []
    for group in df_banknifty_grouped_by_time.groups:
        #current_iter_datetime  = datetime.strptime(group, "%d-%m-%Y %H:%M:%S")
        current_iter_date = datetime.strptime(group, "%Y-%m-%d").date()
        start_time = datetime.combine(current_iter_date,time(9,15))
        days = max_date - current_iter_date
        #seconds = current_iter_datetime - start_time
        df = df_banknifty_grouped_by_time.get_group(group)
        df['day'] = days.days
        days_sort.append(days.days)
        df['seconds'] = df['Date/Time'].apply(lambda date : (datetime.strptime(date, "%d-%m-%Y %H:%M:%S") - start_time).seconds)
        df['CPType'] = df['Ticker'].apply(lambda x: 'CE' if 'CE' in x else 'PE')
        df['StrikeRate'] = df[['Ticker', 'CPType']].apply(lambda x:int(x[0].split("WK")[1].split(x[1])[0]), axis=1)
        df.rename(columns={'Close':'LastRate'}, inplace=True)
        #df['CurrentStrike_BN'] =  df_banknifty_lastrate[df_banknifty_lastrate['Date/Time'] == group]
        #df['CurrentStrike_BN'] = df_banknifty_lastrate[df_banknifty_lastrate['Date/Time'] == group]
        #print("Starting new")
        #print(len(df))
        df = pd.merge(df, df_banknifty_lastrate[['Date/Time', 'Close']], on = 'Date/Time', how = 'inner')
        #print(len(df))
        df['expiry'] = max_date
        df.reset_index(drop=True, inplace=True)
        df = df.drop(columns=['Ticker', 'Open', 'High', 'Low', 'date_only', 'Date/Time'])
        columns_rename = {'Close':'lastrate','Open Interest':'OpenInterest'}
        df.rename(columns=columns_rename, inplace=True)
        df.drop_duplicates()
        columns_rename_ce = {'Volume':'Volume_CE', 'OpenInterest':'OpenInterest_CE', 'LastRate':'LastRate_CE'}
        columns_rename_pe = {'Volume':'Volume_PE', 'OpenInterest':'OpenInterest_PE', 'LastRate':'LastRate_PE'}
        ce_data = df[df['CPType'] == 'CE']
        ce_data.rename(columns=columns_rename_ce, inplace=True)
        print('Starting a iteration')
        print(len(ce_data))
        pe_data = df[df['CPType'] == 'PE']
        pe_data.rename(columns=columns_rename_pe, inplace=True)
        print(len(pe_data))
        print(len(df))
        df_merged = pd.merge(ce_data,pe_data, on = ['day', 'seconds','StrikeRate', 'lastrate', 'expiry'], how='outer')
        print(len(df_merged))
        df_merged.fillna(0, inplace=True)
        final_df_list.append(df_merged)
    return final_df_list, days_sort,str(max_date)

#filename = "/Users/amareswarreddy/Documents/GitHub/AlgoBots/Options Strategies/backtester2/optionsdata/02-09--SEP-2021-weekly-expiry_data__VEGE_NF_AND_BNF_Options.csv"
#df = get_data(filename)
# %%
#return final_df_list
    #%%

# %%
# %%
