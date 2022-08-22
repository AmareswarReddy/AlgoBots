#%%
import requests
import json
import pandas as pd
import csv
from io import StringIO
def download_tickers(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; Rigor/1.0.0; http://rigor.com)",
        "Accept": "*/*",
        "authorization": "enctoken nL7CMcUPQ/xHPbd2xguSce3i1XC5QqdwpMAWbn3CH9+L8RT2VkxFs8WPwink48EWUXxjBGSDbwtqbyAg4/BhPLpbeud+HSl6pu/5ZbmvDUv8lbStYq/sqQ==",
        "cookie": "public_token=1ekFsAD5dQpaRJ30BYfIPQMdkU0ZkLNF; enctoken=nL7CMcUPQ/xHPbd2xguSce3i1XC5QqdwpMAWbn3CH9+L8RT2VkxFs8WPwink48EWUXxjBGSDbwtqbyAg4/BhPLpbeud+HSl6pu/5ZbmvDUv8lbStYq/sqQ==; user_id=UW1001; kf_session=ASE75ZSJHhD9V63oDtKopnrPsYwZ3ltN; _ga=GA1.2.796226098.1661082037; _gid=GA1.2.815124478.1661082037"
    }
    url = url
    r = requests.get(url, headers=headers)
    
    if(r.status_code == 200):
        #print(r.content)
        #df = pd.read_csv(r.content)
        # json_data = json.loads(r.content)
        # print(json_data)
    
        #print(pd.DataFrame(r.content))
            #json.dump(json_data, json_file)
        s=str(r.content,'utf-8')
        data = StringIO(s) 
        df=pd.read_csv(data)
        return df
    else:
        return None

def downloaddata(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; Rigor/1.0.0; http://rigor.com)",
        "Accept": "*/*",
        "authorization": "enctoken nL7CMcUPQ/xHPbd2xguSce3i1XC5QqdwpMAWbn3CH9+L8RT2VkxFs8WPwink48EWUXxjBGSDbwtqbyAg4/BhPLpbeud+HSl6pu/5ZbmvDUv8lbStYq/sqQ==",
        "cookie": "public_token=1ekFsAD5dQpaRJ30BYfIPQMdkU0ZkLNF; enctoken=nL7CMcUPQ/xHPbd2xguSce3i1XC5QqdwpMAWbn3CH9+L8RT2VkxFs8WPwink48EWUXxjBGSDbwtqbyAg4/BhPLpbeud+HSl6pu/5ZbmvDUv8lbStYq/sqQ==; user_id=UW1001; kf_session=ASE75ZSJHhD9V63oDtKopnrPsYwZ3ltN; _ga=GA1.2.796226098.1661082037; _gid=GA1.2.815124478.1661082037"
    }
    url = url
    r = requests.get(url, headers=headers)
    
    if(r.status_code == 200):
        json_data = json.loads(r.content)
        return pd.DataFrame(json_data['data']['candles'])
    else:
        return None
url3 = "https://kite.zerodha.com/oms/instruments/historical/21048578/minute?user_id=UW1001&oi=1&from=2022-07-22&to=2022-08-21"
url = "https://api.kite.trade/instruments"
df=download_tickers(url)
df2=downloaddata(url3)
df2[7]=0
indicator=list(df2[7])
# %%
import numpy as np
index=list(df2[0])
day=index[0][:10]
def pearsonr(x, y):
    n = len(x)
    x = np.asarray(x)
    y = np.asarray(y)
    dtype = type(1.0 + x[0] + y[0])
    if n == 2:
        return dtype(np.sign(x[1] - x[0])*np.sign(y[1] - y[0])), 1.0
    xmean = x.mean(dtype=dtype)
    ymean = y.mean(dtype=dtype)
    xm = x.astype(dtype) - xmean
    ym = y.astype(dtype) - ymean
    normxm = np.linalg.norm(xm)
    normym = np.linalg.norm(ym)
    r = np.dot(xm/normxm, ym/normym)
    r = max(min(r, 1.0), -1.0)
    return r,0
def tester(df2,day,indicator):
    close=list(df2[4])
    volume=list(df2[5])
    oi=list(df2[6])
    c=[]
    o=[]
    v=0
    for i in range(0,len(df2)):
        if index[i][:10]==day:
            c=c+[close[i]]
            o=o+[oi[i]]
            v=v+volume[i]
            if len(o)>1:
                corr=pearsonr(c, o)[0]
                indicator[i]=corr*(((o[-1]-o[0])/v)+1)/2
    return indicator


# %%
days=[]
for a in index:
    days=days+[a[:10]]
[*set(days)]
for day in days:
    indicator=tester(df2,day,indicator)
df2[7]=indicator
# %%
p1=[]
temp=0
profit=0
for i in range(0,len(df2)):
    if df2[7].iloc[i]>0 and temp==0:
        p1=p1+[df2[4].iloc[i]]
        temp=1
    if df2[7].iloc[i]<=0 and len(p1)!=0:
        p1=p1+[df2[4].iloc[i]]
        print(p1)
        print('profit: ',p1[1]-p1[0])
        profit=profit+p1[1]-p1[0]
        p1=[]
        temp=0
    if df2[7].iloc[i]==0 and len(p1)!=0:
        p1=p1+[df2[4].iloc[i-1]]
        print(p1)
        print('profit: ',p1[1]-p1[0])
        profit=profit+p1[1]-p1[0]
        p1=[]
        temp=0
print('total profit: ',profit)
# %%
p1=[]
temp=0
profit=0
for i in range(0,len(df2)):
    if df2[7].iloc[i]<0 and temp==0:
        p1=p1+[df2[4].iloc[i]]
        temp=1
    if df2[7].iloc[i]>0 and len(p1)!=0:
        p1=p1+[df2[4].iloc[i]]
        print(p1)
        print('profit: ',-p1[1]+p1[0])
        profit=profit-p1[1]+p1[0]
        p1=[]
        temp=0
    if df2[7].iloc[i]==0 and len(p1)!=0:
        p1=p1+[df2[4].iloc[i-1]]
        print(p1)
        print('profit: ',-p1[1]+p1[0])
        profit=profit-p1[1]+p1[0]
        p1=[]
        temp=0
print('total profit: ',profit)
# %%
