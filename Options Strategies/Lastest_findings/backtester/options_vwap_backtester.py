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

def options_vwap_json(option_chain,options_vwap):
    c_lastrate=np.array(option_chain['LastRate_CE'])
    p_lastrate= np.array(option_chain['LastRate_PE'])
    c_volumes=  np.array(option_chain['Volume_CE'])
    p_volumes=  np.array(option_chain['Volume_PE'])
    prev_c_lastrate=    np.array(options_vwap['LastRate_CE'])
    prev_p_lastrate=    np.array(options_vwap['LastRate_PE'])
    prev_c_volumes=     np.array(options_vwap['Volume_CE'])
    prev_p_volumes=     np.array(options_vwap['Volume_PE'])
    c_net=np.multiply(c_volumes-prev_c_volumes,c_lastrate)
    p_net=np.multiply(p_volumes-prev_p_volumes,p_lastrate)
    c_volumes[c_volumes==0]=1
    p_volumes[p_volumes==0]=1
    call_vwap=np.multiply((c_net+np.multiply(prev_c_lastrate,prev_c_volumes)),1/c_volumes)
    put_vwap=np.multiply((p_net+np.multiply(prev_p_lastrate,prev_p_volumes)),1/p_volumes)
    options_vwap=option_chain[['StrikeRate','LastRate_CE','LastRate_PE','Volume_CE','Volume_PE']].copy()
    options_vwap['LastRate_CE']=call_vwap    
    options_vwap['Volume_CE']=option_chain['Volume_CE']
    options_vwap['LastRate_PE']=put_vwap    
    options_vwap['Volume_PE']=option_chain['Volume_PE']
    return options_vwap

#backtest

day_list=[[0, "'2022-09-01'"],
[1, "'2022-09-01'"],
[3, "'2022-09-01'"],
[4, "'2022-09-08'"],
[0, "'2022-09-08'"],
[1, "'2022-09-08'"],
[2, "'2022-09-08'"],
[3, "'2022-09-08'"],
[4, "'2022-09-15'"],
[0, "'2022-09-15'"],
[1, "'2022-09-15'"],
[2, "'2022-09-15'"],
[3, "'2022-09-15'"],
[4, "'2022-09-22'"],
[0, "'2022-09-22'"],
[1, "'2022-09-22'"],
[2, "'2022-09-22'"],
[0, "'2022-09-29'"],
[1, "'2022-09-29'"],
[2, "'2022-09-29'"],
[3, "'2022-09-29'"],
[4, "'2022-10-06'"],
[0, "'2022-10-06'"],
[1, "'2022-10-06'"],
[1, "'2022-10-13'"],
[2, "'2022-10-13'"],
[4, "'2022-10-20'"],
[3, "'2022-10-20'"],
[1, "'2022-11-03'"],
[1, "'2022-11-24'"],
[2, "'2022-11-24'"],
[3, "'2022-11-24'"],
[4, "'2022-12-01'"],
[0, "'2022-12-01'"],
[1, "'2022-12-01'"],
[2, "'2022-12-01'"],
[3, "'2022-12-01'"],
[4, "'2022-12-08'"],
[0, "'2022-12-08'"],
[1, "'2022-12-08'"],
[2, "'2022-12-08'"],
[3, "'2022-12-08'"],
[4, "'2022-12-15'"],
[0, "'2022-12-15'"],
[1, "'2022-12-15'"],
[2, "'2022-12-15'"],
[3, "'2022-12-15'"],
[4, "'2022-12-22'"]]
for i in range(0,len(day_list)):
    try:
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
        expiry=day_list[i][1]
        day=str(day_list[i][0])
        k="select * from option_chain_data where expiry="+expiry+" and day="+day+";"
        mycursor.execute(k)


        """
        rows=mycursor.fetchall()
        aa=pd.DataFrame(rows,columns=['Volume_CE','OpenInterest_CE','LastRate_CE','StrikeRate','LastRate_PE','OpenInterest_PE','Volume_PE','expiry','day','seconds','lastrate'])
        """


        aa=pd.read_sql(k,connection)
        k2="select seconds from option_chain_data where day="+day+" and expiry="+expiry+" group by 1;"
        list_of_seconds=list(pd.read_sql(k2,connection)['seconds'])
        lastrate=[]
        indicator=[]
        def list_of_strikes(a,b):
            a=np.linspace(int(np.floor(a/100)*100),int(np.ceil(b/100)*100),int((int(np.ceil(b/100)*100)-int(np.floor(a/100)*100))/100)+1)
            if len(a)==1:
                a=a+a[0]
            return a
        option_chain=aa[aa['seconds']==list_of_seconds[0]].copy()
        options_vwap=option_chain[['StrikeRate','LastRate_CE','LastRate_PE','Volume_PE','Volume_CE']].copy()
        options_vwap['Volume_PE']=options_vwap['Volume_PE']
        options_vwap['Volume_CE']=options_vwap['Volume_CE']
        for second in list_of_seconds[1:]:
            option_chain=aa[aa['seconds']==second].copy()
            x=float(option_chain['lastrate'].iloc[0])
            options_vwap=options_vwap_json(option_chain,options_vwap)
            call_move=sum(np.sign(np.array(option_chain['LastRate_CE']-options_vwap['LastRate_CE'])))
            put_move= sum(np.sign(np.array(options_vwap['LastRate_PE']-option_chain['LastRate_PE'])))
            total=2*len(np.array(option_chain['LastRate_CE']))
            indicator=indicator+[(call_move+put_move)/(total)]
            lastrate=lastrate+[x]
        fig, ax_left = plt.subplots()
        ax_right = ax_left.twinx()
        ax_left.plot(np.array(lastrate[:]), color='blue')
        #ax_left.plot(created_lastrate[:], color='violet')
        ax_right.plot(np.array(indicator), color='red')
        plt.show()
    except Exception:
        pass
    #json_file={'indicator':final_,'hightime':final1,'oi_ratio':final2,'rosetta_ratio':final3,'rosetta':final4,'lastrate':lastrate[:],'time':list_of_seconds}
    #import json
#
    #with open(day+'_'+expiry+".json", "w") as outfile:
    #    json.dump(json_file,outfile)
# %%
