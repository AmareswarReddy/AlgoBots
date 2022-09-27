#%%
import pandas as pd
import mysql.connector
from mysql.connector import Error
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy.interpolate
try:
    connection  = mysql.connector.connect(
        host    = 'localhost',
        user    = 'root',
        passwd  = 'vinay1@A',
        database= "banknifty_data"
    )
except Error as e:
    print(f"The error '{e}' occurred")
print('Connected!')
mycursor = connection.cursor(buffered=True)
expiry="'2022-09-15'"
day='4'
k="select * from option_chain_data where expiry="+expiry+" and day="+day+";"
mycursor.execute(k)


"""
rows=mycursor.fetchall()
aa=pd.DataFrame(rows,columns=['Volume_CE','OpenInterest_CE','LastRate_CE','StrikeRate','LastRate_PE','OpenInterest_PE','Volume_PE','expiry','day','seconds','lastrate'])
"""


aa=pd.read_sql(k,connection)
k2="select seconds from option_chain_data where day="+day+" and expiry="+expiry+" group by 1;"
list_of_seconds=list(pd.read_sql(k2,connection)['seconds'])

#strategy
def rosetta_ratio_tester(option_chain,memory,a2,a1):
    try:
        p_openinterest2=np.array(list(memory['OpenInterest_PE']))
        c_openinterest2=np.array(list(memory['OpenInterest_CE']))
        p_openinterest=np.array(list(option_chain['OpenInterest_PE']))-p_openinterest2
        c_openinterest=np.array(list(option_chain['OpenInterest_CE']))-c_openinterest2
    except Exception:
        p_openinterest=np.array(list(option_chain['OpenInterest_PE']))
        c_openinterest=np.array(list(option_chain['OpenInterest_CE']))
    p_lastrate=np.array(list(option_chain['LastRate_PE']))
    c_lastrate=np.array(list(option_chain['LastRate_CE']))
    pp=p_lastrate[np.multiply(p_lastrate!=0, p_openinterest!=0)]
    po=p_openinterest[np.multiply(p_lastrate!=0, p_openinterest!=0)]
    cp=c_lastrate[np.multiply(c_lastrate!=0, c_openinterest!=0)]
    co=c_openinterest[np.multiply(c_lastrate!=0, c_openinterest!=0)]
    a1=a1+np.dot(1/np.array(pp),np.array(po))
    a2=a2+np.dot(1/np.array(cp),np.array(co))
    a=a2/a1
    return  np.round_(((1/np.exp(a))-(1/np.exp(1)))*158.2,2),a2,a1


def rosetta_distance_ratio_tester(option_chain,memory,b2,b1,x):
    
    try:
        p_openinterest2=np.array(list(memory['OpenInterest_PE']))
        c_openinterest2=np.array(list(memory['OpenInterest_CE']))
        p_openinterest=np.array(list(option_chain['OpenInterest_PE']))-p_openinterest2
        c_openinterest=np.array(list(option_chain['OpenInterest_CE']))-c_openinterest2
    except Exception:
        p_openinterest=np.array(list(option_chain['OpenInterest_PE']))
        c_openinterest=np.array(list(option_chain['OpenInterest_CE']))
    p_lastrate=np.array(list(option_chain['LastRate_PE']))
    c_lastrate=np.array(list(option_chain['LastRate_CE']))
    pp=p_lastrate[np.multiply(p_lastrate!=0, p_openinterest!=0)]
    po=p_openinterest[np.multiply(p_lastrate!=0, p_openinterest!=0)]
    cp=c_lastrate[np.multiply(c_lastrate!=0, c_openinterest!=0)]
    co=c_openinterest[np.multiply(c_lastrate!=0, c_openinterest!=0)]
    p_strikes=np.exp((np.array(list(option_chain['StrikeRate']))-x)/2000)[np.multiply(p_lastrate!=0, p_openinterest!=0)]
    c_strikes=np.exp((x-np.array(list(option_chain['StrikeRate'])))/2000)[np.multiply(c_lastrate!=0, c_openinterest!=0)]
    tone1=1/np.multiply(p_strikes,np.array(pp))
    tone2=1/np.multiply(c_strikes,np.array(cp))
    b1=b1+np.dot(tone1,np.array(po))
    b2=b2+np.dot(tone2,np.array(co))
    #b=b2/b1
    b=(np.sum(np.array(list(option_chain['OpenInterest_PE'])))/np.sum(np.array(list(option_chain['OpenInterest_CE']))) )
    #return  np.round_(((1/np.exp(b))-(1/np.exp(1)))*158.2,2),b2,b1
    return b,1,1


#profit n loss
def moving_average(x, w):
    return np.convolve(x, np.ones(w), 'valid') / w

def moving_average_spot(x,w):
    return np.round_(float(np.convolve(x[-w:], np.ones(w), 'valid') / w),2)

    #return np.array(list(np.zeros(w-1))+ list(np.convolve(x, np.ones(w), 'valid') / w))
#plt.plot(moving_average(capture2,99950))
plt.show()
memory=0
a1,a2=0,0
b1,b2=0,0
capture=[]
capture2=[]
lastrate=[]
memory2=0
memory3=0
w1,w2=5,200
taken_trade=0
up=[]
down=[]
total=0
profit_trades=0
loss_trades=0
max_loss=0
max_profit=0
dif=0
for second in list_of_seconds:
    option_chain=aa[aa['seconds']==second].copy()
    x=float(option_chain['lastrate'].iloc[0])
    a,a2,a1=rosetta_ratio_tester(option_chain,memory,a2,a1)
    b,b2,b1=rosetta_distance_ratio_tester(option_chain,memory,b2,b1,x)
    memory=option_chain.copy()
    capture=capture+[a]
    capture2=capture2+[b]
    lastrate=lastrate+[x]
    if len(capture)>800:
        c1=moving_average_spot(capture2,w1)
        c2=moving_average_spot(capture2,w2)
        calc_lastrate = scipy.interpolate.interp1d(capture2[:-50],lastrate[:-50],fill_value='extrapolate')
        #dif=c1-c2
        #dif=c1+c2-memory2-memory3
        dif=np.sum(calc_lastrate(capture2[-50:])-lastrate[-50:])
        memory2=c1
        memory3=c2
        
    if dif>0 and taken_trade==0:
        up=up+[lastrate[-1]]
        taken_trade=1
    if dif<0 and taken_trade==0 :
        down=down+[lastrate[-1]]
        taken_trade=-1
    if dif>0 and taken_trade==-1:
        down=down+[lastrate[-1]]
        profit=down[0]-down[-1]
        print(profit)
        if profit>0:
            profit_trades=profit_trades+1
            if profit>max_profit:
                max_profit=profit
        else:
            loss_trades=loss_trades+1
            if profit<max_loss:
                max_loss=profit
        down=[]
        total=total+profit
        taken_trade=0
    if dif<0 and taken_trade==1:
        up=up+[lastrate[-1]]
        profit=up[1]-up[0]
        print(profit)
        if profit>0:
            profit_trades=profit_trades+1
            if profit>max_profit:
                max_profit=profit
        else:
            loss_trades=loss_trades+1
            if profit<max_loss:
                max_loss=profit
        up=[]
        total=total+profit
        taken_trade=0
print('max_loss :', max_loss)
print('loss_trades',loss_trades)
print('profit_trades',profit_trades)
print('max_profit',max_profit)
print('total_profit',total)



#backtest
memory=0
a1,a2=0,0
b1,b2=0,0
capture=[]
capture2=[]
lastrate=[]
for second in list_of_seconds:
    option_chain=aa[aa['seconds']==second].copy()
    x=float(option_chain['lastrate'].iloc[0])
    a,a2,a1=rosetta_ratio_tester(option_chain,memory,a2,a1)
    b,b2,b1=rosetta_distance_ratio_tester(option_chain,memory,b2,b1,x)
    memory=option_chain.copy()
    capture=capture+[a]
    capture2=capture2+[b]
    lastrate=lastrate+[x]
fig, ax_left = plt.subplots()
ax_right = ax_left.twinx()
ax_left.plot(lastrate[:], color='blue')
#ax_right.plot(capture[:], color='red')
ax_right.plot(capture2[:], color='orange')
plt.show()




# %%
