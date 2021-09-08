# Steps to install the library to implement Black-Scholes

# Step 1 : Open Anaconda
# Step 2 : If multiple versions of Python or mutiple Virtual Python Environments are installed, activate the one you are using

#Info : Suppose Python Virtual Env name is "py38", then run (conda activate py38); 

# Step 3: Install the SWIG Dependency; Run (conda install swig)
# Step 4: Install the Library; Run (pip install py_vollib)


from py_vollib import black_scholes
from py_vollib.black_scholes import implied_volatility

#price (float) – the Black-Scholes option price
#S (float) – underlying asset price
#K (float) – strike price
#t (float) – time to expiration in years
#r (float) – risk-free interest rate
#flag (str) – ‘c’ or ‘p’ for call or put.


#For Futures Interest rate is 0%. So r should be Zero for Index such as BankNifty

# Test Values
price = 115.6
S = 36700
K = 36900
t = 0.5
r = 0
flag = 'c'

iv = implied_volatility.implied_volatility(price=price, S=S, K=K, t=t, r=r, flag=flag)
print(iv)
