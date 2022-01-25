#%%
# Update scripmaster file every week
import numpy as np
import pandas as pd
from time import sleep, strftime
from py5paisa import FivePaisaClient
from py5paisa.strategy import *
from cred import *
from datetime import datetime 
import requests
from pytz import timezone 
# Client login credentials
cred={
    "APP_NAME":"5P53784053",
    "APP_SOURCE":"8023",
    "USER_ID":"y4JUrjToSOR",
    "PASSWORD":"y0tc7unqQAV",
    "USER_KEY":"DrmeltLdZo82SKaxWJoeMALor1Xaiqk5",
    "ENCRYPTION_KEY":"ANb7Y0ouVD5iX0jcPGwPMIEyQnwPjxuI"
    }
Client = FivePaisaClient(email='chandinimadduru123@gmail.com', passwd='amar@0987',dob='19950820', cred=cred)
Client.login()
# %%
# get data from opstra
#data1: open interest
#data2: FII data and DII data (cash market and derivatives market)
def overall_trend():

    return trend