#%%
from lib2to3.pgen2 import driver
import requests
import json
from datetime import datetime, timedelta, time

cookies = {"JSESSIONID":"13585D82DD014EE1D8F4CB022930701B"}

#%%
def downloaddata(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; Rigor/1.0.0; http://rigor.com)",
        "Accept": "*/*"
    }
    url = url
    r = requests.get(url, headers=headers, cookies= cookies)
    #print(r.status_code)
    if(r.status_code == 200):
        json_data = json.loads(r.content)
        #print(json_data)
        return json_data
    else:
        print("Error Downloading:",r.status_code)
        return None

# %%
simulation_expiry = "https://opstra.definedge.com/api/optionsimulator/simulatorexpiries"
expiries_data = downloaddata(simulation_expiry)
# %%
def extract_dates(input):
    import re
    # Input string
    input_string = input
    # Regular expression pattern
    pattern = r"(\d{2})([A-Z]{3})(\d{4})"
    # Matching using regex
    match = re.match(pattern, input_string)
    if match:
        day = match.group(1)
        month = match.group(2)
        year = match.group(3)
    return day, month, year 
# %%
def filter_dates(expiries_data, filter=2023):
    final_list = []
    for i in range(0, len(expiries_data)):
        day, month, year  = extract_dates(expiries_data[i])
        if(int(year) == filter):
            final_list.append(expiries_data[i])
    return final_list
#expiries_data_final = extract_all_dates(expiries_data)
#%%
def get_5_working_weekdays_dates(date_object):
    #date_string = "31AUG2023"
    five_days = []
    date_format = "%d%b%Y"
    date_object = datetime.strptime(date_object, date_format).date()
    print(date_object)
    for i in range(0,7):
        dt = date_object - timedelta(days=i)
        if dt.weekday() == 5 or dt.weekday() == 6:  # Saturday
            pass
        else:  # Sunday
            five_days.append(dt)
        #date_object - timedelta(days=i)
    return five_days

# %%
expiries_data_filtered = filter_dates(expiries_data)
#%%
symbol = 'BANKNIFTY'
baseURL = 'https://opstra.definedge.com/api/optionsimulator/optionchain/'
basePath = "/Users/amareswarreddy/Documents/GitHub/AlgoBots/Options Strategies/opstra_data"

#%%
def jsonDump(data, file_name):
    # the json file where the output must be stored
    fileName = file_name
    out_file = open(fileName, "w")
    json.dump(data, out_file, indent = 6)
    out_file.close()
#%%
#Following has to be looped for all expires. Just do a tab for the whle content and a loop
for expiry_date in expiries_data_filtered:
    five_days = get_5_working_weekdays_dates(expiry_date)
    expiry = expiry_date
    time_obj = time()
    days_to_expiry = 0
    for day in five_days:
        #print(day)
        total_day_data = {}
        datetime_obj = datetime.combine(day, time_obj)
        datetime_obj = datetime_obj + timedelta(hours=9, minutes=15)
        for i in range(0,375):
            ts = int(datetime_obj.timestamp())
            url = baseURL + str(ts)+"&"+symbol+"&"+ expiry
            tempData = downloaddata(url)
            if tempData is None:
                break
            total_day_data[str(datetime_obj)] = tempData
            datetime_obj = datetime_obj + timedelta(minutes=1)
        if tempData is not None:
            file_name = symbol+"_"+expiry+"_"+str(days_to_expiry) + ".json"
            full_file_name = basePath +'/' +file_name
            print(file_name)
            jsonDump(total_day_data, full_file_name)
            days_to_expiry = days_to_expiry + 1
# %%
# import pandas as pd
# df = pd.read_json(total_day_data[0]['optionchaindata'])
# # %%
# # %%
# print(type(total_day_data))
# # %%
# for k,v in total_day_data.items():
#     print(k)
# # %%
# import pandas as pd
# df = pd.DataFrame(total_day_data['2023-08-25 15:25:00']['optionchaindata'])
# %%
