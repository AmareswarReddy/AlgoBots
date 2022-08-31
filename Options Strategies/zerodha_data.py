#%%
import requests
import json
import pandas as pd
import csv
from io import StringIO
import matplotlib.pyplot as plt
url3 = "https://kite.zerodha.com/oms/instruments/historical/9604098/minute?user_id=UW1001&oi=1&from=2022-08-01&to=2022-08-30"
headers = {
    "User-Agent": "Mozilla/5.0 (compatible; Rigor/1.0.0; http://rigor.com)",
    "Accept": "*/*",
    "authorization": "enctoken SCkcz66MSyVmOtR6WDoReMP015xsEZ71yVOECGkGsAXworRsFdyCFPq28ai+DeCRbhLIN5dJUQWOgO2h3mvmdpRO4uvnhumvHY1m5xFIXgtFq+DsgapMxw==",
    "cookie": "public_token=nkC7486t0a9TwxSKP5fxe55Vzl0Z25WZ; enctoken=SCkcz66MSyVmOtR6WDoReMP015xsEZ71yVOECGkGsAXworRsFdyCFPq28ai+DeCRbhLIN5dJUQWOgO2h3mvmdpRO4uvnhumvHY1m5xFIXgtFq+DsgapMxw==; user_id=UW1001; kf_session=myDjy7MyA7ewiBRc6rDggPyknjwWaLFn"
}
def download_tickers(url,headers):
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

def downloaddata(url,headers):
    url = url
    r = requests.get(url, headers=headers)
    #print(r.content)
    if(r.status_code == 200):
        json_data = json.loads(r.content)
        #print(r.content)
        return pd.DataFrame(json_data['data']['candles'])
    else:
        return None
url = "https://api.kite.trade/instruments"
df=download_tickers(url,headers)
df2=downloaddata(url3,headers)
#print(df2)
df2[7]=0
df2['v']=df2[1]
df2['o']=df2[1]
df2['ch_o']=0
indicator=list(df2[7])
vwap=list(df2['v'])
owap=list(df2['o'])
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
def tester(df2,day,indicator,vwap,owap):
    close=list(df2[4])
    volume=list(df2[5])
    oi=list(df2[6])
    dayy=list(df2[6])
    df2['day']=0
    c=[]
    o=[]
    v=[]
    for i in range(0,len(df2)):
        if index[i][:10]==day:
            dayy[i]=day
            c=c+[close[i]]
            o=o+[oi[i]]
            v=v+[volume[i]]
            if len(o)>1:
                corr=pearsonr(c, o)[0]
                del_o=o[-1]-o[0]
                #indicator[i]=corr*((((del_o)/np.sum(v)+1))/2)
                vwap[i]=np.dot(np.array(v),np.array(c))/np.sum(np.array(v))
                owap[i]=np.dot(np.array(o),np.array(c))/np.sum(np.array(o))
                #kratos=(np.dot(np.array(o),np.array(c))-o[0]*np.sum(np.array(c)))/(np.sum(np.array(o))-len(o)*o[0])
                #owap[i]=min(vwap[i]+100,max(vwap[i]-100,kratos))
                if owap[i]>vwap[i] and close[i]>vwap[i]:
                    indicator[i]=1
                elif owap[i]<vwap[i] and close[i]<vwap[i]:
                    indicator[i]=-1
                else:
                    indicator[i]=0
                #a=np.array([0]+list(o))
                #b=np.array(list(o)+[0])
                #ch_o=np.array([1]+list((b-a)[1:]))[:-1]
                #owap[i]=np.dot(np.array(ch_o),np.array(c))/np.sum(np.array(ch_o))
    df2['day']=dayy
    return indicator,owap,vwap

def tester2(df2,day,indicator,vwap,owap):
    close=list(df2[4])
    volume=list(df2[5])
    oi=list(df2[6])
    dayy=list(df2[6])
    df2['day']=0
    c=[]
    o=[]
    v=[]
    for i in range(0,len(df2)):
        if index[i][:10]==day:
            dayy[i]=day
            c=c+[close[i]]
            o=o+[oi[i]]
            v=v+[volume[i]]
            if len(o)>1:
                vwap[i]=np.dot(np.array(v),np.array(c))/np.sum(np.array(v))
                #owap[i]=np.dot(np.array(o),np.array(c))/np.sum(np.array(o))
                #kratos=(np.dot(np.array(o),np.array(c))-o[0]*np.sum(np.array(c)))/(np.sum(np.array(o))-len(o)*o[0])
                #owap[i]=min(vwap[i]+100,max(vwap[i]-100,kratos))
                
                a=np.array([0]+list(o))
                b=np.array(list(o)+[0])
                ch_o=np.array([1]+list((b-a)[1:]))[:-1]
                owap[i]=np.dot(np.array(ch_o),np.array(c))/np.sum(np.array(ch_o))
                if owap[i]>vwap[i]:
                    indicator[i]=1
                elif owap[i]<vwap[i]:
                    indicator[i]=-1
                else:
                    indicator[i]=0

    df2['day']=dayy
    return indicator,owap,vwap
# %%
days=[]
for a in index:
    days=days+[a[:10]]
[*set(days)]
for day in days:
    indicator,owap,vwap=tester(df2,day,indicator,vwap,owap)
df2[7]=indicator
df2['v']=vwap
df2['o']=owap
# %%
p1=[]
temp=0
profit=0
trades=0
for i in range(0,len(df2)):
    if df2[7].iloc[i]>0 and temp==0:
        p1=p1+[df2[4].iloc[i]]
        temp=1
        trades=trades+1
    elif df2[7].iloc[i]<0 and len(p1)!=0 and temp==1 and df2[4].iloc[i]<vwap[i]:
        p1=p1+[df2[4].iloc[i]]
        print(p1)
        print('profit: ',int(p1[1]-p1[0]))
        profit=profit+p1[1]-p1[0]
        p1=[]
        temp=0
    elif df2[7].iloc[i]==0 and len(p1)!=0 and temp==1:
        p1=p1+[df2[4].iloc[i-1]]
        print(p1)
        print('profit: ',int(p1[1]-p1[0]))
        profit=profit+p1[1]-p1[0]
        p1=[]
        temp=0
print('total profit: ',profit)
print('Total trades',trades)
# %%
p1=[]
temp=0
profit=0
trades=0
for i in range(0,len(df2)):
    if df2[7].iloc[i]<0 and temp==0:
        p1=p1+[df2[4].iloc[i]]
        temp=1
        trades=trades+1
    elif df2[7].iloc[i]>0 and len(p1)!=0 and temp==1 and df2[4].iloc[i]>vwap[i]:
        p1=p1+[df2[4].iloc[i]]
        print(p1)
        print('profit: ',int(-p1[1]+p1[0]))
        profit=profit-p1[1]+p1[0]
        p1=[]
        temp=0
    elif df2[7].iloc[i]==0 and len(p1)!=0 and temp==1:
        p1=p1+[df2[4].iloc[i-1]]
        print(p1)
        print('profit: ',int(-p1[1]+p1[0]))
        profit=profit-p1[1]+p1[0]
        p1=[]
        temp=0
print('total profit: ',profit)
print('Total trades',trades)
# %%
for loop in range(0,21):
    lbu=df2.iloc[loop*375:loop*375+375]
    fig, ax_left = plt.subplots()
    ax_right = ax_left.twinx()
    ax_left.plot(np.array(lbu[4]), color='blue')
    #ax_right.plot(np.array(df2[7]), color='white')
    #ax_right.plot(np.array(df2['o'])-np.array(df2['v']), color='green')
    ax_left.plot(np.array(lbu['v']), color='red')
    ax_left.plot(np.array(lbu['o']), color='yellow')
    plt.show()
    print(loop)
#%%
for day in days:
    data=df2[df2['day']==day]
    fig, ax_left = plt.subplots()
    ax_right = ax_left.twinx()
    ax_left.plot(np.array(data[4]), color='blue')
    #ax_right.plot(np.array(df2[7]), color='white')
    #ax_right.plot(np.array(df2['o'])-np.array(df2['v']), color='green')
    ax_left.plot(np.array(data['v']), color='red')
    ax_left.plot(np.array(data['o']), color='yellow')
    plt.show()


# %%
