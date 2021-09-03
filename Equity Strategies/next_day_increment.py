#%%
import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt
#%%
data = yf.download('ONGC.BO', period='301d', interval='1d')
def CLOSE_OPEN_DIFFERANCE(data):
    close = data['Close'].iloc[:-1].copy()
    close = close.to_numpy()
    open = data['Open'].iloc[1:].copy()
    open = open.to_numpy()
    open_close=open-close
    return open_close
y1=CLOSE_OPEN_DIFFERANCE(data)
y2=np.zeros((data['Close'].size-1,))
x=np.zeros((data['Close'].size-1,))
for i in range(0,data['Close'].size-1):
    x[i] =i 
plt.plot(x,y1)
plt.plot(x,y2)
plt.show
# %%
y3 = np.zeros((data['Close'].size-1))
y3[0]=y1[0]
for j in range(1,data['Close'].size-1):
    y3[j] = y3[j-1]+y1[j]
plt.plot(x,y3)
# %%
