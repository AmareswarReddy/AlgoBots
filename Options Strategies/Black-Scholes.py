# Steps to install the library to implement Black-Scholes

# Step 1 : Open Anaconda (Anaconda is not required. It is working fine with normal python interpretor. 'pip install py_vollib' is good to go  )
# Step 2 : If multiple versions of Python or mutiple Virtual Python Environments are installed, activate the one you are using

#Info : Suppose Python Virtual Env name is "py38", then run (conda activate py38); 

# Step 3: Install the SWIG Dependency; Run (conda install swig)
# Step 4: Install the Library; Run (pip install py_vollib)

#%%
from py_vollib import black_scholes
from py_vollib.black_scholes import implied_volatility
from datetime import datetime,date
holidays=int(input('enter number of holidays between expiry date and today date: '))
today=str(datetime.today()).split()[0]
expiry = "20210910"          # already defined in strangle strategy
t_day=date(int(today[:4]),int(today[5:7]),int(today[8:10]))
e_day = date(int(expiry[:4]),int(expiry[4:6]),int(expiry[6:8]))
days_left=e_day-t_day
T_zero=(int(str(days_left).split()[0])-holidays)*6.25
now=datetime.now()
time=now.strftime('%H %M')
#price (float) – the Black-Scholes option price
#S (float) – underlying asset price
#K (float) – strike price
#t (float) – time to expiration in years
#r (float) – risk-free interest rate
#flag (str) – ‘c’ or ‘p’ for call or put.

#For Futures Interest rate is 0%. So r should be Zero for Index such as BankNifty

var=15-int(time.split()[0])+(30-int(time.split()[1]))/60
#considering a day has only 6 hours 15 min (Total trading hours from 9:15am to 3:30pm)
if var>0 and var<=6.5:
    T_one= var
elif 15-int(time.split()[0])>6.5:
    T_one=6.5
else :
    T_one = 0

# Test Values
price = 115.6
S = 36700
K = 36900
t=(T_one+T_zero)/(261*6.25)
r = 0
flag = 'c'

iv = implied_volatility.implied_volatility(price=price, S=S, K=K, t=t, r=r, flag=flag)
# looking at volatility in percentage
iv = iv*100
print(iv)

# %%
