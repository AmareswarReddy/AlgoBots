#%%
from audioop import avg
import glob
def get_files_matching(day=0):
    # Define the pattern to match the files
    pattern = f"BANKNIFTY_*_{day}*"
    base_path = '/Users/amareswarreddy/Documents/GitHub/AlgoBots/Options Strategies/opstra_data'
    file_path_pattern = base_path + '/' + pattern
    # Use glob to get a list of matching file paths

    matching_files = glob.glob(file_path_pattern)
    # Iterate through the matching files and process them
    # for file_path in matching_files:
    #     # Process each file as needed
    #     print("Processing file:", file_path)
    return matching_files
# %%
day = 2
files = get_files_matching(day)
# %%
# %%
import pandas as pd
def get_avg_premium(data):
    keys = ['futuresPrice',
    'spotPrice',
    'optionchaindata']
    date = []
    premium = []
    strikeprice = []
    for key, val in data.items():
        data_minute = data[key]
        if data_minute is None:
            return None, None
        spot_price = int(data_minute[keys[1]]/100)* 100
        #print(spot_price)
        option_data = data_minute['optionchaindata']
        df = pd.DataFrame(option_data)
        filtered_df = df[df['Strikes'] == spot_price]
        avg_premium = int(filtered_df['CallLTP']) + int(filtered_df['PutLTP'])
        date.append(key)
        premium.append(avg_premium)
        strikeprice.append(data_minute[keys[1]])
    # print(premium[1])
    # print(date[1])

    # print(premium[350])
    # print(date[350])
    return date, premium, strikeprice
#%%
import json
dates = []
premiums = []
strikeprice = []

for file in files:
    f= open(file)
    d = json.load(f)
    date, premium, sp = get_avg_premium(d)
    if premium is not None:
        dates.append(date)
        premiums.append(premium)
        strikeprice.append(sp)
import numpy as np
avg_premiums = np.zeros(len(premium))
for i in range(0,len(premiums)):
    avg_premiums = [x+y for x,y in zip(avg_premiums, premiums[i])]

avg_premiums = [num/len(premiums) for num in avg_premiums]
# %%
condition = lambda x : x%30 == 0
result_avg_prem = [int(element) for index, element in enumerate(avg_premiums) if condition(index)]
print(result_avg_prem)
# %%
for p in premiums:
    result_avg_prem = [element for index, element in enumerate(p) if condition(index)]
    print(result_avg_prem)
# %%
for p in strikeprice:
    result_avg_prem = [element for index, element in enumerate(p) if condition(index)]
    print(result_avg_prem)
# %%

# %%
