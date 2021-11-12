#%%
import yfinance as yf
import matplotlib.pyplot as plt
data= yf.download('^NSEBANK',start="2020-01-01", end="2021-04-30")
#%%
def charges(opt_value,lots):
    return 40+50*(opt_value/1000)*lots

def upside_profit(open,high,low,close,sl,target,opt_value,lots):
    executed_trade=0
    ud=1
    '''
    if (open-low)>= sl:
        profit=-sl-charges(opt_value,lots)
        executed_trade=-1
    elif (high-open)>=target:
        profit=lots*target-charges(opt_value,lots)
        executed_trade=1
    else:
        profit=lots*(close-open)-charges(opt_value,lots)
    '''
    profit=lots*(close-open)-charges(opt_value,lots) #remove later
    if profit>=0:
        executed_trade=1
    elif profit<0:
        executed_trade=-1
    return profit,executed_trade,ud

def downside_profit(open,high,low,close,sl,target,opt_value,lots):
    ud=-1
    '''
    if (high-open)>=sl:
        profit=-lots*sl-charges(opt_value,lots)
        executed_trade=-1
    elif (open-low)>=target:
        profit=lots*target-charges(opt_value,lots)
        executed_trade=1
    else:
        profit=lots*(open-close)-charges(opt_value,lots)
    '''
    profit=lots*(open-close)-charges(opt_value,lots) #remove later
    if profit>=0:
        executed_trade=1
    elif profit<0:
        executed_trade=-1
    return profit,executed_trade,ud

a=1
sl=200
target=3*sl
executed_trade=1
close=data['Close']
open=data['Open']
high=data['High']
low=data['Low']
profit=0
i=0
ud=1
portfolio=[]
while True:
    if executed_trade==-1:
        i=i+1
        if i==len(close):
            break
        a=3*a
        if a>9*a:
            a=10
        ud= ud*(-1)
        if ud==1:
            pro,executed_trade,ud=upside_profit(open[i],high[i],low[i],close[i],sl*a,target*a,1000,a)
            
            if pro>0:
                profit=profit+min([pro,target])
            elif pro<0:
                profit=profit+max([pro,-sl])
            portfolio=portfolio+[profit]
        elif ud==-1:
            pro,executed_trade,ud=downside_profit(open[i],high[i],low[i],close[i],sl*a,target*a,1000,a)
            if pro>0:
                profit=profit+min([pro,target])
            elif pro<0:
                profit=profit+max([pro,-sl])
            portfolio=portfolio+[profit]
    if executed_trade==1:
        i=i+1
        a=1
        if ud==1:
            pro,executed_trade,ud=upside_profit(open[i],high[i],low[i],close[i],sl*a,target*a,1000,a)
            if pro>0:
                profit=profit+min([pro,target])
            elif pro<0:
                profit=profit+max([pro,-sl])
            portfolio=portfolio+[profit]
        elif ud==-1:
            pro,executed_trade,ud=downside_profit(open[i],high[i],low[i],close[i],sl*a,target*a,1000,a)
            if pro>0:
                profit=profit+min([pro,target])
            elif pro<0:
                profit=profit+max([pro,-sl])
            portfolio=portfolio+[profit]
        
    if executed_trade==0:
        if pro>0:
            a=1       
        i=i+1
        if i==len(close):
            break
        if ud==1:
            pro,executed_trade,ud=upside_profit(open[i],high[i],low[i],close[i],sl*a,target*a,1000,a)
            if pro>0:
                profit=profit+min([pro,target])
            elif pro<0:
                profit=profit+max([pro,-sl])
            portfolio=portfolio+[profit]
        elif ud==-1:
            pro,executed_trade,ud=downside_profit(open[i],high[i],low[i],close[i],sl*a,target*a,1000,a)
            if pro>0:
                profit=profit+min([pro,target])
            elif pro<0:
                profit=profit+max([pro,-sl])
            portfolio=portfolio+[profit]
print('profit is ',profit)
print('required capital',10*25*500)
plt.plot(portfolio)
# %%
