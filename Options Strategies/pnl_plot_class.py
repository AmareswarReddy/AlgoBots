#%%
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.interpolate import interp1d

#client_name=input('enter the client name Eg: vinathi,bhaskar ')
# def data(exchange, prime_client, current_expiry_time_stamp_weekly):
#     while True:
#         try :
#             expiry_timestamps=prime_client['login'].get_expiry("N",exchange).copy()
#             option_chain=pd.DataFrame(prime_client['login'].get_option_chain("N",exchange,current_expiry_time_stamp_weekly)['Options'])
#             x=expiry_timestamps['lastrate'][0]['LTP']
#             break
#         except Exception :
#             pass
#     return option_chain,x

def add_position(positions,strike,type,lots):
    positions[len(positions)]=[strike,type,lots]
    return positions

def y_axis(x,single_position,option_chain):
    if single_position[1]=='CE_B':
        k=x-single_position[0]
        k[k<0]=0
        lastrate=float(option_chain[(option_chain['StrikeRate']==single_position[0]) & (option_chain['CPType']=='CE')]['LastRate'])
        y=single_position[2]*(k-lastrate)

    if single_position[1]=='CE_S':
        k=single_position[0]-x
        k[k>0]=0
        lastrate=float(option_chain[(option_chain['StrikeRate']==single_position[0]) & (option_chain['CPType']=='CE')]['LastRate'])
        y=single_position[2]*(k+lastrate)

    if single_position[1]=='PE_B':
        k=single_position[0]-x
        k[k<0]=0
        lastrate=float(option_chain[(option_chain['StrikeRate']==single_position[0]) & (option_chain['CPType']=='PE')]['LastRate'])
        y=single_position[2]*(k-lastrate)
    if single_position[1]=='PE_S':
        k=x-single_position[0]
        k[k>0]=0
        lastrate=float(option_chain[(option_chain['StrikeRate']==single_position[0]) & (option_chain['CPType']=='PE')]['LastRate'])
        y=single_position[2]*(k+lastrate)
    return y

def pnl_graph_B(positions,option_chain,lastrate):
    try:
        k=pd.DataFrame(positions)
        a=np.array(k.iloc[0])
        x=np.linspace(min(a)-300,max(a)+300,int((max(a)-min(a)+600)/100)+1)
        y1=np.zeros(len(x))
        for i in range(0,len(positions)):
            y1+=np.array(y_axis(x,positions[i],option_chain))  
    except Exception:
        x=[0]
        y1=[0]
    return x,y1

def pnl_graph_N(positions,option_chain,lastrate):
    try:
        k=pd.DataFrame(positions)
        a=np.array(k.iloc[0])
        x=np.linspace(min(a)-150,max(a)+150,int((max(a)-min(a)+300)/50)+1)
        y1=np.zeros(len(x))
        for i in range(0,len(positions)):
            y1+=np.array(y_axis(x,positions[i],option_chain))  
    except Exception:
        x=[0]
        y1=[0]
    return x,y1

def get_strike_from_scrip(scripcode, option_chain):
    k1=option_chain[option_chain['ScripCode']==scripcode]
    return int(k1['StrikeRate'])

#%%
#variables to be initialised
def get_pnl_plot(Noption_chain,Nx, Boption_chain,Bx, S):
    
    # option_chain=pd.DataFrame(prime_client['login'].get_option_chain("N","BANKNIFTY",current_expiry_time_stamp_weekly)['Options'])
    # prev_x=expiry_timestamps['lastrate'][0]['LTP']


    # Noption_chain,Nx=data('NIFTY', prime_client, current_expiry_time_stamp_weekly) 
    # Boption_chain,Bx=data('BANKNIFTY', prime_client, current_expiry_time_stamp_weekly) 
    # S=pd.DataFrame(prime_client['login'].positions())
    nifty_positions={}
    banknifty_positions={}
    S = pd.DataFrame(S)
    for i in range(0,len(S)):
        if ('NIFTY' in S['ScripName'].iloc[i]) and S['NetQty'].iloc[i]!=0 and ('BANKNIFTY' not in S['ScripName'].iloc[i]):
            if S['NetQty'].iloc[i]<0 and ('PE' in S['ScripName'].iloc[i]):
                type_='PE_S'
            elif S['NetQty'].iloc[i]<0 and ('CE' in S['ScripName'].iloc[i]):
                type_='CE_S'
            elif S['NetQty'].iloc[i]>0 and ('CE' in S['ScripName'].iloc[i]):
                type_='CE_B'
            elif S['NetQty'].iloc[i]>0 and ('PE' in S['ScripName'].iloc[i]):
                type_='PE_B'
            nifty_positions=add_position(nifty_positions,get_strike_from_scrip(S['ScripCode'].iloc[i],Noption_chain),type_,abs(S['NetQty'].iloc[i]))
        elif ('BANKNIFTY' in S['ScripName'].iloc[i]) and S['NetQty'].iloc[i]!=0:
            if S['NetQty'].iloc[i]<0 and ('PE' in S['ScripName'].iloc[i]):
                type_='PE_S'
            elif S['NetQty'].iloc[i]<0 and ('CE' in S['ScripName'].iloc[i]):
                type_='CE_S'
            elif S['NetQty'].iloc[i]>0 and ('CE' in S['ScripName'].iloc[i]):
                type_='CE_B'
            elif S['NetQty'].iloc[i]>0 and ('PE' in S['ScripName'].iloc[i]):
                type_='PE_B'
            banknifty_positions=add_position(banknifty_positions,get_strike_from_scrip(S['ScripCode'].iloc[i],Boption_chain),type_,abs(S['NetQty'].iloc[i]))
    x1,y1=pnl_graph_N(nifty_positions,Noption_chain,Nx)
    x2,y2=pnl_graph_B(banknifty_positions,Boption_chain,Bx)
    def get_break_evens(x,y):
        k=[]
        if len(y)>2:
            for i in range(1,len(y)):
                if np.sign(y[i-1])!=np.sign(y[i]):
                    f=interp1d([y[i-1],y[i]],[x[i-1],x[i]])
                    k+=[f(0)]
        return np.array(k)
    break_even_N=get_break_evens(x1,y1)
    break_even_B=get_break_evens(x2,y2)
    plt.plot(x1,y1,'g')
    plt.plot(x1,np.array(y1)*0,'r')
    l=[]
    plt.plot([Nx,Nx],[max(y1),min(y1)],'b',linestyle='dashed')
    l+=['lastrate: '+str(Nx)]
    for i in break_even_N:
        plt.plot([i,i],[max(y1),min(y1)],'y')
        l+=['break_even: '+str(i)]
    plt.legend(['pnl_at_expiry','zero_line']+l)
    nifty_plot = plt.figure()
  

    plt.plot(x2,y2,'g')
    plt.plot(x2,np.array(y2)*0,'r')
    l=[]
    plt.plot([Bx,Bx],[max(y2),min(y2)],'b',linestyle='dashed')
    l+=['lastrate:'+str(Bx)]
    for i in break_even_B:
        plt.plot([i,i],[max(y2),min(y2)],'y')
        l+=['break_even: '+str(i)]
    plt.legend(['pnl_at_expiry','zero_line']+l)
    banknifty_plot = plt.figure()
 

    #print(pd.DataFrame(prime_client['login'].positions()))
    total_profit = sum(S['MTOM'])+sum(S['BookedPL'])
    return nifty_plot, banknifty_plot, total_profit
        #print(prime_client['login'].margin())
# %%



# %%

# %%
