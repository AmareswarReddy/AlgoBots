#%%
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
a=pd.read_pickle('/Users/vinayreddy/Documents/GitHub/AlgoBots/Options Strategies/oi_indicator2.pkl')
# %%
y1=np.array(a['projected'])
y2=np.array(a['spotprice'])
plt.plot(y1)
plt.plot(y2)
plt.show()

# %%
