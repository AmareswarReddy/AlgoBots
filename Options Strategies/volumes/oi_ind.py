#%%
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
a=pd.read_pickle('/Users/Vinay Reddy/Documents/GitHub/AlgoBots/Options Strategies/oi_indicator.pkl')
# %%
y1=np.array(a['projected']+34200)
y2=np.array(a['spotprice'])
plt.plot(y1)
plt.plot(y2)
plt.show()

# %%
