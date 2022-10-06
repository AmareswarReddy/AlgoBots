#%%
import json
import matplotlib.pyplot as plt
from time import sleep
with open('variables_data_1.json', 'r') as  json_file:
    j_data = json.load(json_file)
    lastrate = j_data['lastrate']
    corr = j_data['corr']
    k = j_data['k']
    niftybank=j_data['nifty_bank']

import numpy as np
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
corr2_value=-1
for cc in range(1,20):
    corr2=[]
    corr_w=cc*100
    trades_total=0
    for i in range(corr_w,len(k)):
        corr2=corr2+[pearsonr(niftybank[i-corr_w:i],lastrate[i-corr_w:i])[0]]
    lastrate=lastrate[corr_w:]
    niftybank=niftybank[corr_w:]
    k=k[corr_w:]
    profit=0
    p1=[]
    p2=[]
    martha=np.zeros(len(k))
    tempo=20
    taken_trade=0
    for i in range(2,len(k)):
        if k[i]-k[i-1]>0.4 and k[i]<-tempo and taken_trade==0  and corr2[i]>corr2_value:
            p1=p1+[lastrate[i]]
            martha[i]=tempo
            tempo=tempo+10
            taken_trade=1

        elif k[i]-k[i-1]<-0.4 and k[i]>tempo and taken_trade==0  and corr2[i]>corr2_value :
            p1=p1+[lastrate[i]]
            martha[i]=-tempo
            tempo=tempo+10
            taken_trade=-1

        elif k[i]-k[i-1]<0 and k[i]>0 and taken_trade==1 :
            profit=profit+(lastrate[i]*len(p1)-np.sum(p1))
            print(p1)
            p1=[]
            #print('hi')
            #print('lastrate=',lastrate[i])
            trades_total=trades_total+1
            martha[i]=0
            tempo=20
            taken_trade=0
        
        elif k[i]-k[i-1]>0 and k[i]<0 and taken_trade==-1:
            profit=profit-(lastrate[i]*len(p1)-np.sum(p1))
            print(p1)
            p1=[]
            #print('hi')
            #print('lastrate=',lastrate[i])
            trades_total=trades_total+1
            martha[i]=0
            taken_trade=0
            tempo=20
        elif k[i]-k[i-1]>0 and k[i]<-tempo and taken_trade==1  and corr2[i]>corr2_value:
            p1=p1+[lastrate[i]]
            martha[i]=tempo
            tempo=tempo+10
        elif k[i]-k[i-1]<-0 and k[i]>tempo and taken_trade==-1  and corr2[i]>corr2_value:
            p1=p1+[lastrate[i]]
            martha[i]=-tempo
            tempo=tempo+10
        else:
            martha[i]=martha[i-1]
    print('corr_w:',corr_w)
    print('trades:',trades_total)
    print('profit: ',int(profit))
    print("")
    #if profit==0:
    #break
#%%
fig, ax_left = plt.subplots()
ax_right = ax_left.twinx()
ax_left.plot(lastrate, color='blue') 
ax_right.plot(np.array(corr2)*100, color='red')
ax_right.plot(niftybank, color='green')
plt.show()

# %%
for i in range(1001,len(lastrate)):
    json_data = {'lastrate': list(lastrate[i-240:i]), 'k':list(k[i-240:i]),'martha':list(martha[i-240:i])*10,'nifty_bank':list(niftybank[i-240:i]),'corr2':list(corr2[i-240:i])}
    with open('animation.json', 'w') as  json_file:
        json.dump(json_data, json_file)
    sleep(0.3)
    print(i)
# %%