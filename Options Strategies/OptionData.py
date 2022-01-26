

#%%
import requests
import json
from datetime import datetime
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

fiidii_data_url = "https://opstra.definedge.com/api/fiidiidata"
fiidii_data = downloaddata(fiidii_data_url)
fiidii_data_daily = fiidii_data['daily']
#print(fiidii_data_daily)
fiidii_data_monthly = fiidii_data['monthly']
#print(fiidii_data_monthly)


openInterest_data_url = "https://opstra.definedge.com/api/openinterest/fiioidata/30"
openInterest_data = downloaddata(openInterest_data_url)
openInterest_latest_data =  openInterest_data['latestdata']
final_OI_data = {}
#print(openInterest_latest_data)
for oi_data in openInterest_latest_data:
    #print(oi_data['symname'])
    final_OI_data[oi_data['symname']] = oi_data
print(final_OI_data)
