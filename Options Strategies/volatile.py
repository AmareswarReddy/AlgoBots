#%%
from py_vollib import black_scholes
from py_vollib.black_scholes import implied_volatility
from datetime import datetime,date
expiry = "20210916"          # already defined in strangle strategy
price = 115.6
S = 36700
K = 36900
flag = 'c'
holidays=   0  #int(input('enter number of holidays between expiry date and today date: '))
def volatility(holidays,expiry,price,S,K,flag):
    r = 0
    today=str(datetime.today()).split()[0]
    t_day=date(int(today[:4]),int(today[5:7]),int(today[8:10]))
    e_day = date(int(expiry[:4]),int(expiry[4:6]),int(expiry[6:8]))
    days_left=e_day-t_day
    T_zero=(int(str(days_left).split()[0])-holidays)*6.25
    now=datetime.now()
    time=now.strftime('%H %M')
    var=15-int(time.split()[0])+(30-int(time.split()[1]))/60
    if var>0 and var<=6.5:
        T_one= var
    elif 15-int(time.split()[0])>6.5:
        T_one=6.5
    else :
        T_one = 0
    t=(T_one+T_zero)/(261*6.25)
    iv = implied_volatility.implied_volatility(price=price, S=S, K=K, t=t, r=r, flag=flag)
    return iv*100
