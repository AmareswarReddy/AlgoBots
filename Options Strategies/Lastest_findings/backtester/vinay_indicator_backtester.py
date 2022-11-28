#%%
import pandas as pd
import mysql.connector
from mysql.connector import Error
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy.interpolate
from pyswarm import pso
from scipy import interpolate
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
expiry="'2022-09-22'"
day='1'
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
def rosetta_ratio_tester(option_chain,memory,a2,a1):
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
    a=a1/a2
    return  a,a2,a1
def rosetta(option_chain):
    i=np.array(option_chain['StrikeRate'])[0]
    end=np.array(option_chain['StrikeRate'])[-1]
    ss=np.array(option_chain['StrikeRate'])
    p_lastrate=np.array(list(option_chain['LastRate_PE']))
    c_lastrate=np.array(list(option_chain['LastRate_CE']))
    p_openinterest=np.array(list(option_chain['OpenInterest_PE']))
    c_openinterest=np.array(list(option_chain['OpenInterest_CE']))
    data=[]
    data1=[]
    data2=[]
    increment=2
    while i<end:
        i=i+increment
        init_ce=0
        init_pe=0
        end_pe=0
        end_ce=0
        for k in range(0,len(ss)):
            init_pe=init_pe+p_lastrate[k]*p_openinterest[k]
            init_ce=init_ce+c_lastrate[k]*c_openinterest[k]
            end_pe=end_pe+p_openinterest[k]*max((ss[k]-i),0)
            end_ce=end_ce+c_openinterest[k]*max((i-ss[k]),0)
        data=data+[init_ce-end_ce-init_pe+end_pe]
        data1=data1+[init_ce-end_ce]
        data2=data2+[-init_pe+end_pe]
    index=np.argmin(np.abs(data))
    index1=np.argmin(np.abs(data1))
    index2=np.argmin(np.abs(data2))
    a=np.array(option_chain['StrikeRate'])[0]+index*increment
    b=np.array(option_chain['StrikeRate'])[0]+index1*increment
    c=np.array(option_chain['StrikeRate'])[0]+index2*increment
    return  a,round(b/100)*100,round(c/100)*100

def rosetta2(option_chain):
    i=np.array(option_chain['StrikeRate'])[0]
    end=np.array(option_chain['StrikeRate'])[-1]
    ss=np.array(option_chain['StrikeRate'])
    p_lastrate=np.array(list(option_chain['LastRate_PE']))
    c_lastrate=np.array(list(option_chain['LastRate_CE']))
    p_openinterest=np.array(list(option_chain['OpenInterest_PE']))
    c_openinterest=np.array(list(option_chain['OpenInterest_CE']))
    def loss_function(v):
        init_pe=np.dot(p_lastrate,p_openinterest)
        init_ce=np.dot(c_lastrate,c_openinterest)
        tmax=ss-v[0]
        tmax[tmax<0]=0
        tmin=v[0]-ss
        tmin[tmin<0]=0
        end_pe=np.dot(p_openinterest,tmax)
        end_ce=np.dot(c_openinterest,tmin)
        data=init_ce-end_ce-init_pe+end_pe
        return abs(data)
    a,b=pso(func=loss_function,lb=[i],ub=[end],minfunc=0.1)
    return  np.round_(a[0],1)

def rosetta_past(option_chain,memory,x,init_pe,init_ce):
    try:
        i=np.array(option_chain['StrikeRate'])[0]
        end=np.array(option_chain['StrikeRate'])[-1]
        ss=np.array(option_chain['StrikeRate'])
        p_lastrate=np.array(list(option_chain['LastRate_PE']))
        c_lastrate=np.array(list(option_chain['LastRate_CE']))
        mp_open=np.array(list(memory['OpenInterest_PE']))
        mc_open=np.array(list(memory['OpenInterest_CE']))
        p_openinterest=np.array(list(option_chain['OpenInterest_PE']))
        c_openinterest=np.array(list(option_chain['OpenInterest_CE']))
        p_oi_change=p_openinterest-mp_open
        c_oi_change=c_openinterest-mc_open
        def apple(v):
            init_pe=np.dot(p_lastrate,p_oi_change)+init_pe
            init_ce=np.dot(c_lastrate,c_oi_change)+init_ce
            tmax=ss-v[0]
            tmax[tmax<0]=0
            tmin=v[0]-ss
            tmin[tmin<0]=0
            end_pe=np.dot(p_openinterest,tmax)
            end_ce=np.dot(c_openinterest,tmin)
            data=init_ce-end_ce-init_pe+end_pe
            return abs(data)
        a,b=pso(func=apple,lb=[i],ub=[end],minfunc=0.1)
        return  x-np.round_(a[0],1),init_pe,init_ce
    except Exception:
        i=np.array(option_chain['StrikeRate'])[0]
        end=np.array(option_chain['StrikeRate'])[-1]
        ss=np.array(option_chain['StrikeRate'])
        p_lastrate=np.array(list(option_chain['LastRate_PE']))
        c_lastrate=np.array(list(option_chain['LastRate_CE']))
        p_openinterest=np.array(list(option_chain['OpenInterest_PE']))
        c_openinterest=np.array(list(option_chain['OpenInterest_CE']))
        def apple(v):
            init_pe=np.dot(p_lastrate,p_openinterest)
            init_ce=np.dot(c_lastrate,c_openinterest)
            tmax=ss-v[0]
            tmax[tmax<0]=0
            tmin=v[0]-ss
            tmin[tmin<0]=0
            end_pe=np.dot(p_openinterest,tmax)
            end_ce=np.dot(c_openinterest,tmin)
            data=init_ce-end_ce-init_pe+end_pe
            return abs(data)
        a,b=pso(func=apple,lb=[i],ub=[end],minfunc=0.1)
        return  np.round_(a[0],1),init_pe,init_ce

def blue_factor(option_chain,x):
    final_chain=option_chain[(option_chain['StrikeRate']>x-1000) & (option_chain['StrikeRate']<x+1000)]
    strikes=final_chain['StrikeRate']
    p_lastrates=final_chain['LastRate_PE']
    c_lastrates=final_chain['LastRate_CE']
    f_p = interpolate.interp1d(strikes, p_lastrates,kind='quadratic')
    f_c = interpolate.interp1d(strikes, c_lastrates,kind='quadratic')
    return (f_p(x)+f_c(x))/2

def triple_indicator(option_chain,x):
    p_strikerates=np.array(list(option_chain['StrikeRate']))
    c_strikerates=np.array(list(option_chain['StrikeRate']))
    p_lastrate=np.array(list(option_chain['LastRate_PE']))
    c_lastrate=np.array(list(option_chain['LastRate_CE']))
    p_openinterest=np.array(list(option_chain['OpenInterest_PE']))
    c_openinterest=np.array(list(option_chain['OpenInterest_CE']))
    average_p_strike=np.dot(p_strikerates,p_openinterest)/np.sum(p_openinterest)
    average_c_strike=np.dot(c_strikerates,c_openinterest)/np.sum(c_openinterest)
    p1=x-average_p_strike
    c1=average_c_strike-x
    i=np.array(option_chain['StrikeRate'])[0]
    end=np.array(option_chain['StrikeRate'])[-1]
    ss=np.array(option_chain['StrikeRate'])
    def loss_function(v):
        init_pe=np.dot(p_lastrate,p_openinterest)
        init_ce=np.dot(c_lastrate,c_openinterest)
        tmax=ss-v[0]
        tmax[tmax<0]=0
        tmin=v[0]-ss
        tmin[tmin<0]=0
        end_pe=np.dot(p_openinterest,tmax)
        end_ce=np.dot(c_openinterest,tmin)
        data=init_ce-end_ce-init_pe+end_pe
        return abs(data)
    a,b=pso(func=loss_function,lb=[i],ub=[end],minfunc=0.1)
    x1=x-np.round_(a[0],1)
    factor5=blue_factor(option_chain,x)
    p_open=np.sum(np.array(list(option_chain['OpenInterest_PE'])))
    c_open=np.sum(np.array(list(option_chain['OpenInterest_CE'])))
    oi_ratio=p_open/c_open
    pp=p_lastrate[np.multiply(p_lastrate!=0, p_openinterest!=0)]
    po=p_openinterest[np.multiply(p_lastrate!=0, p_openinterest!=0)]
    cp=c_lastrate[np.multiply(c_lastrate!=0, c_openinterest!=0)]
    co=c_openinterest[np.multiply(c_lastrate!=0, c_openinterest!=0)]
    a1=np.dot(np.array(pp),np.array(po))
    a2=np.dot(np.array(cp),np.array(co))
    aa=a1/a2
    hightime_indicator= ((2*(c1/p1)*(c1/p1))/(1+(c1/p1)*(c1/p1)))-1
    rosetta_indicator=x1/factor5
    rosetta_ratio_indicator=((2*aa*aa)/(1+aa*aa))-1
    oi_ratio_indicator=((2*oi_ratio*oi_ratio)/(1+oi_ratio*oi_ratio))-1
    final=rosetta_ratio_indicator+oi_ratio_indicator+hightime_indicator+rosetta_indicator
    final1=hightime_indicator
    final2=oi_ratio_indicator
    final3=rosetta_ratio_indicator
    final4=rosetta_indicator
    if (c1/p1)>1:
        indicator=1
    elif (c1/p1)<1:
        indicator=-1
    else :
        indicator=0
    return  final,final1,final2,final3,final4



def rosetta_distance_ratio_tester(option_chain,memory,b2,b1,x):
    
    #try:
    #    p_openinterest2=np.array(list(memory['OpenInterest_PE']))
    #    c_openinterest2=np.array(list(memory['OpenInterest_CE']))
    #    p_openinterest=np.array(list(option_chain['OpenInterest_PE']))-p_openinterest2
    #    c_openinterest=np.array(list(option_chain['OpenInterest_CE']))-c_openinterest2
    #except Exception:
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
def max_move(option_chain):
    #oi_chain=option_chain[(option_chain['StrikeRate']>option_chain['lastrate'].iloc[0]-1000) & (option_chain['StrikeRate']<option_chain['lastrate'].iloc[0]+1000)].copy()
    oi_chain=option_chain
    lastrate=float(oi_chain['lastrate'].iloc[0])
    strikes=np.array(list(oi_chain['StrikeRate']))
    put_lastrates=np.array(list(oi_chain['LastRate_PE']))
    call_lastrates=np.array(list(oi_chain['LastRate_CE']))
    put_open=np.array(list(oi_chain['OpenInterest_PE']))
    call_open=np.array(list(oi_chain['OpenInterest_CE']))

    put_strike_premium=strikes-put_lastrates
    put_side=np.dot(put_strike_premium,put_open)
    strikes_lastrate=strikes-lastrate
    strikes_lastrate[strikes_lastrate>0]=0
    call_side=np.dot(call_lastrates+strikes_lastrate,call_open)
    put_strike=(put_side/np.sum(put_open))-(1/np.sum(put_open))*(call_side)
    support=(put_side/np.sum(put_open))
    call_strike_premium=strikes-call_lastrates
    call_side=np.dot(call_strike_premium,call_open)
    strikes_lastrate=strikes-lastrate
    strikes_lastrate[strikes_lastrate<0]=0
    put_side=np.dot(put_lastrates-strikes_lastrate,put_open)
    call_strike=(call_side/np.sum(call_open))+(1/np.sum(call_open))*(put_side)
    resistance=(call_side/np.sum(call_open))
    
    return call_strike,resistance,put_strike,support

def max_move2(option_chain,memory,put_side1,put_side2,call_side1,call_side2):
    #oi_chain=option_chain[(option_chain['StrikeRate']>option_chain['lastrate'].iloc[0]-1000) & (option_chain['StrikeRate']<option_chain['lastrate'].iloc[0]+1000)].copy()
    try:
        mp_open=np.array(list(memory['OpenInterest_PE']))
        mc_open=np.array(list(memory['OpenInterest_CE']))
        oi_chain=option_chain
        lastrate=float(oi_chain['lastrate'].iloc[0])
        strikes=np.array(list(oi_chain['StrikeRate']))
        put_lastrates=np.array(list(oi_chain['LastRate_PE']))
        call_lastrates=np.array(list(oi_chain['LastRate_CE']))
        put_open=np.array(list(oi_chain['OpenInterest_PE']))-mp_open
        total_put_open=np.array(list(oi_chain['OpenInterest_PE']))
        total_call_open=np.array(list(oi_chain['OpenInterest_CE']))
        call_open=np.array(list(oi_chain['OpenInterest_CE']))-mc_open

        put_strike_premium=strikes-put_lastrates
        put_side1=np.dot(put_strike_premium,put_open)+put_side1
        strikes_lastrate=strikes-lastrate
        strikes_lastrate[strikes_lastrate>0]=0
        call_side1=np.dot(call_lastrates+strikes_lastrate,call_open)+call_side1
        put_strike=(put_side1/np.sum(total_put_open))-(1/np.sum(total_put_open))*(call_side1)

        call_strike_premium=strikes+call_lastrates
        call_side2=np.dot(call_strike_premium,call_open)+call_side2
        strikes_lastrate=strikes-lastrate
        strikes_lastrate[strikes_lastrate<0]=0
        put_side2=np.dot(put_lastrates-strikes_lastrate,put_open)+put_side2
        call_strike=(call_side2/np.sum(total_call_open))+(1/np.sum(total_call_open))*(put_side2)
        resistance=(call_side2/np.sum(total_call_open))
        support=(put_side1/np.sum(total_put_open))
    except Exception:
        oi_chain=option_chain
        lastrate=float(oi_chain['lastrate'].iloc[0])
        strikes=np.array(list(oi_chain['StrikeRate']))
        put_lastrates=np.array(list(oi_chain['LastRate_PE']))
        call_lastrates=np.array(list(oi_chain['LastRate_CE']))
        put_open=np.array(list(oi_chain['OpenInterest_PE']))
        call_open=np.array(list(oi_chain['OpenInterest_CE']))

        put_strike_premium=strikes-put_lastrates
        put_side1=np.dot(put_strike_premium,put_open)
        strikes_lastrate=strikes-lastrate
        strikes_lastrate[strikes_lastrate>0]=0
        call_side1=np.dot(call_lastrates+strikes_lastrate,call_open)
        put_strike=(put_side1/np.sum(put_open))-(1/np.sum(put_open))*(call_side1)

        call_strike_premium=strikes+call_lastrates
        call_side2=np.dot(call_strike_premium,call_open)
        strikes_lastrate=strikes-lastrate
        strikes_lastrate[strikes_lastrate<0]=0
        put_side2=np.dot(put_lastrates-strikes_lastrate,put_open)
        call_strike=(call_side2/np.sum(call_open))+(1/np.sum(call_open))*(put_side2)
        resistance=(call_side2/np.sum(call_open))
        support=(put_side1/np.sum(put_open))
    return call_strike,resistance,put_strike,support,put_side1,put_side2,call_side1,call_side2

def weighted_max_move2(option_chain,memory,put_side1,put_side2,call_side1,call_side2):
    #option_chain=option_chain[(option_chain['StrikeRate']>option_chain['lastrate'].iloc[0]-2000) & (option_chain['StrikeRate']<option_chain['lastrate'].iloc[0]+2000)].copy()
    oi_chain=option_chain[(option_chain['LastRate_CE']>0) & (option_chain['LastRate_PE']>0)].copy()
    try:
        #memory=memory[(option_chain['StrikeRate']>option_chain['lastrate'].iloc[0]-2000) & (option_chain['StrikeRate']<option_chain['lastrate'].iloc[0]+2000)].copy()
        memory=memory[(option_chain['LastRate_CE']>0) & (option_chain['LastRate_PE']>0)].copy()
        mp_open=np.array(list(memory['OpenInterest_PE']))
        mc_open=np.array(list(memory['OpenInterest_CE']))
        lastrate=float(oi_chain['lastrate'].iloc[0])
        strikes=np.array(list(oi_chain['StrikeRate']))
        put_lastrates=np.array(list(oi_chain['LastRate_PE']))
        call_lastrates=np.array(list(oi_chain['LastRate_CE']))
        put_open=np.array(list(oi_chain['OpenInterest_PE']))-mp_open
        total_put_open=np.array(list(oi_chain['OpenInterest_PE']))
        total_call_open=np.array(list(oi_chain['OpenInterest_CE']))
        call_open=np.array(list(oi_chain['OpenInterest_CE']))-mc_open
        c_delta=np.array(oi_chain['LastRate_CE'])/(oi_chain['LastRate_CE']+oi_chain['LastRate_PE'])
        p_delta=np.array(oi_chain['LastRate_PE'])/(oi_chain['LastRate_CE']+oi_chain['LastRate_PE'])

        put_strike_premium=np.multiply(strikes-put_lastrates,p_delta)
        put_side1=np.dot(put_strike_premium,put_open)+put_side1
        strikes_lastrate=strikes-lastrate
        strikes_lastrate[strikes_lastrate>0]=0
        call_side1=np.dot(call_lastrates+strikes_lastrate,np.multiply(call_open,c_delta))+call_side1
        weight=np.dot(total_put_open,p_delta)
        put_strike=(put_side1/weight)-(1/weight)*(call_side1)

        call_strike_premium=np.multiply(strikes+call_lastrates,c_delta)
        call_side2=np.dot(call_strike_premium,call_open)+call_side2
        strikes_lastrate=strikes-lastrate
        strikes_lastrate[strikes_lastrate<0]=0
        put_side2=np.dot(put_lastrates-strikes_lastrate,np.multiply(put_open,p_delta))+put_side2
        weight2=np.dot(total_call_open,c_delta)
        call_strike=(call_side2/weight2)+(1/weight2)*(put_side2)
        resistance=(call_side2/weight2)
        support=(put_side1/weight)
    except Exception:
        lastrate=float(oi_chain['lastrate'].iloc[0])
        strikes=np.array(list(oi_chain['StrikeRate']))
        put_lastrates=np.array(list(oi_chain['LastRate_PE']))
        call_lastrates=np.array(list(oi_chain['LastRate_CE']))
        put_open=np.array(list(oi_chain['OpenInterest_PE']))
        call_open=np.array(list(oi_chain['OpenInterest_CE']))
        c_delta=np.array(oi_chain['LastRate_CE'])/(oi_chain['LastRate_CE']+oi_chain['LastRate_PE'])
        p_delta=np.array(oi_chain['LastRate_PE'])/(oi_chain['LastRate_CE']+oi_chain['LastRate_PE'])

        put_strike_premium=np.multiply(strikes-put_lastrates,p_delta)
        put_side1=np.dot(put_strike_premium,put_open)
        strikes_lastrate=strikes-lastrate
        strikes_lastrate[strikes_lastrate>0]=0
        call_side1=np.dot(call_lastrates+strikes_lastrate,np.multiply(call_open,c_delta))
        weight=np.dot(put_open,p_delta)
        put_strike=(put_side1/weight)-(1/weight)*(call_side1)

        call_strike_premium=np.multiply(strikes+call_lastrates,c_delta)
        call_side2=np.dot(call_strike_premium,call_open)
        strikes_lastrate=strikes-lastrate
        strikes_lastrate[strikes_lastrate<0]=0
        put_side2=np.dot(put_lastrates-strikes_lastrate,np.multiply(put_open,p_delta))
        weight2=np.dot(call_open,c_delta)
        call_strike=(call_side2/weight2)+(1/weight2)*(put_side2)
        
        resistance=(call_side2/weight2)
        support=(put_side1/weight)
    return call_strike,resistance,put_strike,support,put_side1,put_side2,call_side1,call_side2
def oi_pc(option_chain):
    #lastrate=option_chain['lastrate'].iloc[0]
    #p=option_chain[option_chain['StrikeRate']>lastrate-1000]
    #c=option_chain[option_chain['StrikeRate']<lastrate+1000]
    p_openinterest=np.sum(np.array(list(option_chain['OpenInterest_PE'])))
    c_openinterest=np.sum(np.array(list(option_chain['OpenInterest_CE'])))
    return p_openinterest/c_openinterest
#backtest
memory=0
a1,a2=0,0
b1,b2=0,0
capture=[]
capture2=[]
lastrate=[]
ce_strike=[0]
pe_strike=[0]
resistance=[]
support=[]
put_side1=0
call_side1=0
put_side2=0
call_side2=0
created_lastrate=[]
final_call=[0]
final_put=[9999999999]
distance_ratio_indicator=[]
krop=[]
ind=0
rosetta_ind=[]
triple_indicator_status=[]
final=[]
final1=[]
final2=[]
final3=[]
final4=[]
init_pe,init_ce=0,0
poi_coi=[]
def list_of_strikes(a,b):
    a=np.linspace(int(np.floor(a/100)*100),int(np.ceil(b/100)*100),int((int(np.ceil(b/100)*100)-int(np.floor(a/100)*100))/100)+1)
    if len(a)==1:
        a=a+a[0]
    return a

for second in list_of_seconds:
    option_chain=aa[aa['seconds']==second].copy()
    x=float(option_chain['lastrate'].iloc[0])
    a,a2,a1=rosetta_ratio_tester(option_chain,memory,a2,a1)
    b,b2,b1=rosetta_distance_ratio_tester(option_chain,memory,b2,b1,x)
    #ind,init_pe,init_ce=rosetta_past(option_chain,memory,x,init_pe,init_ce)
    #ind=rosetta2(option_chain)
    rosetta_ind=rosetta_ind+[ind]
    #ac,r,ap,s,put_side1,put_side2,call_side1,call_side2=max_move2(option_chain,memory,put_side1,put_side2,call_side1,call_side2)
    ac,r,ap,s,put_side1,put_side2,call_side1,call_side2=weighted_max_move2(option_chain,memory,put_side1,put_side2,call_side1,call_side2)
    poi_coi=poi_coi+[oi_pc(option_chain)]
    distance_ratio_indicator=distance_ratio_indicator+[(((ac-r)/(s-ap)))]
    krop=krop+[(ac-r)]
    #ac,r,ap,s=max_move(option_chain)
    created_lastrate=created_lastrate+[(ac+ap+r+s)/4]
    memory=option_chain.copy()
    capture=capture+[a]
    capture2=capture2+[b]
    lastrate=lastrate+[x]
    ce_strike=ce_strike+[ac]
    resistance=resistance+[r]
    support=support+[s]
    pe_strike=pe_strike+[ap]
    memory=option_chain
    final_,final1_,final2_,final3_,final4_=triple_indicator(option_chain,x)
    final=final+[final_]
    final1=final1+[final1_]
    final2=final2+[final2_]
    final3=final3+[final3_]
    final4=final4+[final4_]
    if r>final_call[-1]:
        t1=list_of_strikes(r,ac)
        final_call=final_call+[t1[int(np.floor((len(t1)-1)/2))]]
    elif ac<final_call[-1]:
        t1=list_of_strikes(r,ac)
        final_call=final_call+[t1[int(np.floor((len(t1)-1)/2))]]
    else:
        final_call=final_call+[final_call[-1]]
    if s<final_put[-1]:
        t1=list_of_strikes(ap,s)
        final_put=final_put+[t1[int(np.floor((len(t1)-1)/2))]]
    elif ap>final_put[-1]:
        t1=list_of_strikes(ap,s)
        final_put=final_put+[t1[int(np.floor((len(t1)-1)/2))]]
    else:
        final_put=final_put+[final_put[-1]]
fig, ax_left = plt.subplots()
ax_right = ax_left.twinx()
ax_left.plot(lastrate[:], color='blue')
#ax_left.plot(created_lastrate[:], color='violet')
ax_right.plot(final, color='red')
ax_right.plot(final1, color='white')
ax_right.plot(final2, color='violet')
ax_right.plot(final3, color='blue')
ax_right.plot(final4, color='orange')
#ax_left.plot(final_put[1:], color='green')
#ax_left.plot(final_call[1:], color='red')
ax_right.plot(np.array(capture2[:]), color='yellow')
#ax_right.plot(distance_ratio_indicator[:], color='violet')
plt.show()
json_file={'hightime':final1,'oi_ratio':final2,'rosetta_ratio':final3,'rosetta':final4,'lastrate':lastrate[:]}
import json

with open("1_22.json", "w") as outfile:
    json.dump(json_file,outfile)
# %%