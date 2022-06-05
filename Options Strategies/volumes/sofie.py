#%%
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d 
from py5paisa import FivePaisaClient
from py5paisa.strategy import *
import pandas as pd
def client_login(client,lots):
    import json
    f = open ('credentials.json', "r")
    creds = json.loads(f.read())
    client_list={}
    client_list[client]={'strategy':{},'login':{},'lots':{}}
    client_list[client]['lots']=lots
    vinathi_cred = creds[client]["keys"]
    user = creds[client]["user"]
    passw = creds[client]["passw"]
    dob = creds[client]["dob"]
    client_list[client]['strategy']=strategies(user=user, passw=passw, dob=dob,cred=vinathi_cred)
    client_list[client]['login']=FivePaisaClient(email=user, passwd=passw, dob=dob,cred=vinathi_cred)
    client_list[client]['login'].login()
    return client_list[client]

def profits(trades_taken,c_premiums,p_premiums):
    strikes_taken=[int(k.split('_')[0]) for k in list(trades_taken.keys())]
    cptype=[k.split('_')[1][0]+k.split('_')[2] for k in list(trades_taken.keys())]
    prices=[trades_taken[p] for p in list(trades_taken.keys())]
    profit=0
    for i in range(0,len(strikes_taken)):
        if cptype[i]=='CS':
            profit=profit-(c_premiums[strikes_taken[i]]-prices[i])
            
        elif cptype[i]=='CB':
            profit=profit+(c_premiums[strikes_taken[i]]-prices[i])
        
        elif cptype[i]=='PB':
            profit=profit+(p_premiums[strikes_taken[i]]-prices[i])
        
        elif cptype[i]=='PS':
            profit=profit-(p_premiums[strikes_taken[i]]-prices[i])
    return profit

def line(x,strike,cptype,premium):
    if cptype=='CS':
        if x<strike:
            y=premium
        elif x>=strike:
            y=strike+premium-x
        return y    
    elif cptype=='CB':
        if x<strike:
            y=-premium
        elif x>=strike:
            y=-strike-premium+x
        return y
    elif cptype=='PS':
        if x>strike:
            y=+premium
        elif x<=strike:
            y=-strike+premium+x
        return y
    elif cptype=='PB':
        if x>strike:
            y=-premium
        elif x<=strike:
            y=strike-premium-x
        return y
    
def combined_line(x,trades_taken,c_premiums,p_premiums): 
    strikes=[int(k.split('_')[0]) for k in list(trades_taken.keys())]
    cptype=[k.split('_')[1][0]+k.split('_')[2] for k in list(trades_taken.keys())]
    q=0
    for i in range(0,len(strikes)):
        if cptype[i]=='CS' or cptype[i]=='CB': 
            q=q+line(x,strikes[i],cptype[i],c_premiums[strikes[i]])
        elif cptype[i]=='PS' or  cptype[i]=='PB': 
            q=q+line(x,strikes[i],cptype[i],p_premiums[strikes[i]])
    return q

def strike_list(strike1,strike2):
    k=[]
    if strike1>strike2:
        a=strike2
        while a<=strike1:
            k=k+[a]
            a=a+100
    else:
        a=strike1
        while a<=strike2:
            k=k+[a]
            a=a+100
    return k
    
    
def breakeven(trades_taken,c_premiums,p_premiums):
    evens=[]
    x=[int(k.split('_')[0]) for k in list(trades_taken.keys())]
    x_min=min(x)-5000
    x_max=max(x)+5000
    k=strike_list(x_min,x_max)
    possible_break_evens=[]
    trigger1=0
    trigger2=0
    for i in k:
        temp=combined_line(i,trades_taken,c_premiums,p_premiums)
        if temp>0:
            trigger1=1
            if trigger1*trigger2==-1:
                possible_break_evens=possible_break_evens+[[i-100,i]]
                trigger1=0
                trigger2=0
        elif temp<0:
            trigger2=-1
            if trigger1*trigger2==-1:
                possible_break_evens=possible_break_evens+[[i-100,i]]
                trigger1=0
                trigger2=0
    for element in possible_break_evens:
        t1=combined_line(element[0],trades_taken,c_premiums,p_premiums)
        t2=combined_line(element[1],trades_taken,c_premiums,p_premiums)
        accuracy=10
        while accuracy>=1:
            t3=combined_line((element[0]+element[1])/2,trades_taken,c_premiums,p_premiums)
            if t1*t3>0:
                element[0]=(element[0]+element[1])/2
            elif t2*t3>0:
                element[1]=(element[0]+element[1])/2
            accuracy=np.abs(element[0]-element[1])
        evens=evens+[element[0]]
    return  evens


def premium_line(premiums):
    a = list(premiums.keys())
    b=[premiums[e] for e in a]
    f = interp1d(a, b, kind='cubic') 
    return f


def blueline(current_price,trades_taken,c_premiums,p_premiums):
    c_line_func=premium_line(premiums=c_premiums)
    p_line_func=premium_line(premiums=p_premiums)
    strikes_taken=[int(k.split('_')[0]) for k in list(trades_taken.keys())]                
    cptype=[k.split('_')[1][0]+k.split('_')[2] for k in list(trades_taken.keys())]
    prices=[trades_taken[p] for p in list(trades_taken.keys())]
    xmin=-(current_price-min(strikes_taken))-1000
    xmax=-(current_price-max(strikes_taken))+1000
    def CB(x,strike,price_bought,c_line_func): return c_line_func(strike-np.array(x))-price_bought        
    def CS(x,strike,price_sold,c_line_func): return -c_line_func(strike-np.array(x))+price_sold
    def PB(x,strike,price_bought,p_line_func): return p_line_func(strike-np.array(x))-price_bought
    def PS(x,strike,price_sold,p_line_func): return -p_line_func(strike-np.array(x))+price_sold
    def combined_blue_line(current_price,x):
        sofie=current_price+np.array(x)
        bullet=0
        for i in range(0,len(strikes_taken)):
            if cptype[i]=='CS':
                bullet=bullet+np.array(CS(x,strikes_taken[i],prices[i],c_line_func))
            elif cptype[i]=='CB':
                bullet=bullet+np.array(CB(x,strikes_taken[i],prices[i],c_line_func))
            elif cptype[i]=='PB':
                bullet=bullet+np.array(PB(x,strikes_taken[i],prices[i],p_line_func))
            elif cptype[i]=='PS':
                bullet=bullet+np.array(PS(x,strikes_taken[i],prices[i],p_line_func))
        return [sofie,bullet]
    return combined_blue_line(current_price,np.linspace(xmin,xmax,xmax-xmin+1))

def graphity(current_price,trades_taken,c_premiums,p_premiums):
    x=[int(k.split('_')[0]) for k in list(trades_taken.keys())]
    x_min=min(x)-1000
    x_max=max(x)+1000
    k=np.array(strike_list(x_min,x_max))
    x=np.sort([x_min]+x+[x_max])
    y=[]
    for i in x:
        y=y+[combined_line(i,trades_taken,c_premiums,p_premiums)]  
    [A,B]=blueline(current_price,trades_taken,c_premiums=c_premiums,p_premiums=p_premiums)
    plt.plot(A,B,color='green')
    plt.plot(np.array(x),np.array(y),color='black')
    plt.scatter(k,k*0,color='skyblue', s=6)
    plt.axvline(x=current_price,color='red')
    t=breakeven(trades_taken,c_premiums,p_premiums)
    t2=profits(trades_taken,c_premiums,p_premiums)
    for i in t:
        plt.text(x=i,y=0,s=' '+str(int(i)))
    if t2<0:
        plt.title(label='Loss '+str(t2),color='red')
    elif t2>0:
        plt.title(label='profit '+str(t2),color='green')
    plt.xlabel('banknifty price')
    plt.ylabel('profit')
    return plt.show()

client_name='vinathi'
lots=3
prime_client=client_login(client=client_name,lots=lots)
while True:
        try :
            expiry_timestamps=prime_client['login'].get_expiry("N","BANKNIFTY").copy()
            current_expiry_time_stamp_weekly=int(expiry_timestamps['Expiry'][0]['ExpiryDate'][6:19])
            option_chain=pd.DataFrame(prime_client['login'].get_option_chain("N","BANKNIFTY",current_expiry_time_stamp_weekly)['Options'])
            break
        except Exception :
            pass
        
c_data=option_chain[option_chain['CPType']=='CE']
c_premiums={}
temp=c_data['LastRate'].iloc[0]
for i in range(0,len(c_data)): 
    c_premiums[c_data['StrikeRate'].iloc[i]]=(c_data['LastRate'].iloc[i]==0)*(temp-100)+c_data['LastRate'].iloc[i]
    temp=c_premiums[c_data['StrikeRate'].iloc[i]]
p_data=option_chain[option_chain['CPType']=='PE']
p_premiums={}
temp=p_data['LastRate'].iloc[0]
for i in range(0,len(p_data)):
    p_premiums[p_data['StrikeRate'].iloc[i]]=(p_data['LastRate'].iloc[i]==0)*(temp+100)+p_data['LastRate'].iloc[i]
    temp=p_premiums[p_data['StrikeRate'].iloc[i]]

trades_taken={'35100_PE_B':300}
req_list_=[{"Exch":"N","ExchType":"C","Symbol":"BANKNIFTY","Scripcode":"999920005","OptionType":"EQ"}]          
a=prime_client['login'].fetch_market_feed(req_list_)
x=int(a['Data'][0]['LastRate'])
graphity(x,trades_taken,c_premiums,p_premiums)
# %%
