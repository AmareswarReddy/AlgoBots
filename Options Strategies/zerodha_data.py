#%%
import requests
import json
import pandas as pd
import csv

def downloaddata(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; Rigor/1.0.0; http://rigor.com)",
        "Accept": "*/*",
        "authorization": "enctoken K9Hf9cDX0MM6V6yIRspL6ilFwWey68Ny0ypULzqAmxS7YHOC6yz0Cwz8F8nB8PbsWFDTbX/vVp7BDFRW2HIzFqLS4T9tuNXsXLN6ygGIt6E1YQqq2QKA6w==",
        "cookie": "_ga=GA1.2.1703186891.1660024373; kf_session=ZSj2lCYLSbQGTbedDlLGJV8gx23ubmM2; user_id=UW1001; public_token=1ekFsAD5dQpaRJ30BYfIPQMdkU0ZkLNF; enctoken=K9Hf9cDX0MM6V6yIRspL6ilFwWey68Ny0ypULzqAmxS7YHOC6yz0Cwz8F8nB8PbsWFDTbX/vVp7BDFRW2HIzFqLS4T9tuNXsXLN6ygGIt6E1YQqq2QKA6w=="
    }
    url = url
    r = requests.get(url, headers=headers)
    
    if(r.status_code == 200):
        #print(r.content)
        #df = pd.read_csv(r.content)
        # json_data = json.loads(r.content)
        # print(json_data)
    
        print(pd.DataFrame(r.content))
            #json.dump(json_data, json_file)
        return r.content
    else:
        return None

#url = "https://kite.zerodha.com/oms/instruments/historical/9604098/minute?user_id=UW1001&oi=1&from=2022-07-22&to=2022-08-21"
url = "https://api.kite.trade/instruments"
downloaddata(url)


# %%
