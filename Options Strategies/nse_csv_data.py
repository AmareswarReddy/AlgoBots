#%%
import requests
import json
import pandas as pd
import csv
from io import StringIO
import matplotlib.pyplot as plt
from datetime import date, timedelta
#%%
headers = {
    "User-Agent": "Mozilla/5.0 (compatible; Rigor/1.0.0; http://rigor.com)",
    "Accept": "*/*",
    "cookie": '_gid=GA1.2.1673706531.1679333322; _ga=GA1.1.1494217993.1679333320; _ga_PJSKY6CFJH=GS1.1.1679333320.1.1.1679333421.24.0.0; NSE-TEST-1=1910513674.20480.0000; ak_bmsc=A632A18DBFA5CBDB59314D3EB54EE169~000000000000000000000000000000~YAAQ1C/JF4kly+eGAQAA/x1eBBPmGTDMzYmxSsGvSGeAXo8u8lCD0rIbm9ysz6MTJoOIWAbJexrYmFp1aJphJsACESRI7TeJIhbj1o1Ge0DD8zAOMEgIwZPn92RmdBzFZjT/VoJdE6oTloevFp4VgkHzkjvWGawkfX7T+fA/UO1GW+hQks93QW7oHkntCTHPJ/LZ//WxtawmMJ0HmYkLIxVzABysAfbhXLBvpexsXTF0bCPbNpXOHfj4JAxRtSEk48WSeJCD/n7/DQLuj1xahVDcWXhK0YEPVGilfxEKCmWct0/U2GwwioztXKXbASXFn3HKmynJZkVCCIhJr52gI3WYZCiupviBa1w2cl8+jAbPCAoABJLyAKIHOr4dE2kG; bm_mi=C1FABE0F02D63418DFA41F7A7D368572~YAAQ1C/JF88ly+eGAQAAY3ZeBBNA9wXoAs9Ekm4+SRBA4HUyNRFXJ39qjcpyEaBtEv5709XGwcMe+O3YY5CO7nGloVACNqhL1z+Z6LLD7zYtXcvLj8Nvzi4OFKuhpbIAi+oqOE38IjpBiFAGAuBKU4V12SGCRyyp62myzOs/1l8tlBqtpM3UlY7xyKrSYfulH5ft4tLxFIhQU7zubhjH+vosjmZtv1wTJiahSbY3zlssYLpum2a6dROxY6rCREPpR6/rIGzoFNUEFQJVcCK3B004AlhQQK6JnohAHayxieYTKLAgtdU4mmsYPOzaVTkizSG8D9B2gTcxzwlXHYtOVOoL5hWD+a/ldgk9jXuYBOynPhpS1rnn65H7pkwvlt2s/2jXUg==~1; bm_sv=C3F2798D0A5C804926CB3F985DD50C6A~YAAQ1C/JF9Ily+eGAQAAKHdeBBO/BE7UQdfO/z6dRrnUB5S2dqzqFURCJUJnoYKJWwPDqNhaxtnmAx5yVK2oFnwqkLoQ7aZa9/G5GdpdS/DfxVERNET25cPtBR3RnBRZU9dEDOC7Bsa+iL3fipUjZ5Jg3KhCZqOjnFNaoNjX7+4jPoroDfB6qo6zUtVarzE2TOUVouFCouwcsWuutFHdwaRsFtk9FZ0UkSI0RvQ6L4BNoYgkQsR7DIgb6pHmYMvEgjQ=~1; RT="z=1&dm=nseindia.com&si=c4a6628f-7f71-413f-97a1-4717ed93fa92&ss=lfiaoihp&sl=1&tt=8j&bcn=//684d0d4a.akstat.io/&ld=1bq&nu=1pwpgq4y&cl=fz0"',
    "content-type": "application/x-www-form-urlencoded; charset=UTF-8"
}


def downloadfile(url):
    r = requests.get(url)
    filename = 'temp_download_data.csv'
    if(r.status_code == 200):
        open(filename, 'wb').write(r.content)
        data = pd.read_csv(filename, skiprows=[0])
        #print(data)
        #print(len(data))
        return data 
    else:
        return None

def downloaddata(url,headers=None):
    url = url
    if headers ==None:
        r = requests.get(url)
    else:
        r = requests.get(url, headers=headers)
    if(r.status_code == 200):
        json_data = json.loads(r.content)
        #print(r.content)
        return json_data
    else:
        return None
#%%
def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)

base_csv_url = "https://www1.nseindia.com/content/nsccl/fao_participant_oi_"
start_date = date(2018, 1, 10)
end_date = date(2023, 3, 22)
final_df = pd.DataFrame()
print("Started Download")
for single_date in daterange(start_date, end_date):
    dt = single_date.strftime("%Y-%m-%d")
    date_condense = single_date.strftime("%d%m%Y")
    url = base_csv_url+date_condense+".csv"
    data = downloadfile(url)
    if data is not  None:
        data.insert(0,'Date', dt)
        final_df = final_df.append(data, ignore_index=True)

final_file_name = 'fo_oi_positions.csv'
final_df.to_csv(final_file_name)
    #url = """https://www1.nseindia.com/ArchieveSearch?h_filetype=foparticipantoi&date="""+str(single_date)+"&section=FO"
    #print(url)
# %%
# %%
print("Amar")
# %%
