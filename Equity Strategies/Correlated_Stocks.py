#%%
import numpy as np
import pandas as pd
from time import sleep, strftime
from py5paisa import FivePaisaClient
from py5paisa.strategy import *
from datetime import datetime 
now=datetime.now()

cred={
    "APP_NAME":"5P59470899",
    "APP_SOURCE":"6176",
    "USER_ID":"1v73mtvQk3L",
    "PASSWORD":"8DASLLALpZH",
    "USER_KEY":"nNaWVqHIXsgi6FEPnjBknpPPjK1LOHQL",
    "ENCRYPTION_KEY":"HSE2AS6SIEH0UgwfpmwiymkdiRId7eZU"
}
Client = FivePaisaClient(email="p.amareswar20@dmsiitd.org", passwd="Amarreddy@123456", dob="19930714", cred=cred)
Client.login()


#Get only NSE listed stocks
scrip_codes = pd.read_csv("scripmaster-csv-format.csv")
scrip_codes = scrip_codes[(scrip_codes['Exch']=='N') & (scrip_codes['ExchType']=='C') & (scrip_codes['Series']=='EQ')]

#Create a Dictionary of ScripCodes to Symbol
scripcode_to_Symbol = {}
for index, row in scrip_codes.iterrows():
    scripcode_to_Symbol[row['Scripcode']] = row['Name']
    
 #Get only NIFTY200  stocks
nifty200 = pd.read_csv("ind_nifty200list (2).csv")
nifty_with_200 = scrip_codes[scrip_codes['Name'].isin(nifty200['Symbol'])]


#Download the Nifty 200 Historical Data into a dataframe
df = pd.DataFrame()
df_low = pd.DataFrame()
for scrip_code in nifty_with_200['Scripcode']:
    data = Client.historical_data('N','C',scrip_code,'1m','2021-07-21','2021-09-21')
    df[scrip_code] = data['Close']
    
# Correlation
df_withoutnan = df.dropna()
corr_matrix = df_withoutnan.corr()
print(corr_matrix)
# Greater than 95% Corelation
df_corr_matrix = corr_matrix[ (corr_matrix > 0.95) & (corr_matrix != 1)]


#Get the List of Correlated Stocks
correlated_pairs = []
for symbol in nifty_with_200['Scripcode']:
    if len(df_corr_matrix[df_corr_matrix[symbol].notna()][symbol]) > 0:
        #print(df_corr_matrix[df_corr_matrix[symbol].notna()][symbol].index.tolist())
        correlated_pairs.append({symbol : df_corr_matrix[df_corr_matrix[symbol].notna()][symbol].index.tolist()})
print(correlated_pairs)


#Get the List of Correlated Stocks as Stock Symbols
correlated_pairs_by_symbol = []
for pair in correlated_pairs:
    for key in pair:
        #print(scripcode_to_Symbol[key])
        temp = []
        for values in pair[key]:
            temp.append(scripcode_to_Symbol[values])
        correlated_pairs_by_symbol.append({scripcode_to_Symbol[key]:temp})
print(correlated_pairs_by_symbol)



# %%
