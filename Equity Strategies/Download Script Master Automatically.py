#%%
from datetime import date, timedelta
import pandas as pd
import requests

#Read Scrip Master
url = "https://images.5paisa.com/website/scripmaster-csv-format.csv"
r = requests.get(url)
open('scripmaster-csv-format.csv', 'wb').write(r.content)
filename = 'scripmaster-csv-format.csv'
scrips = pd.read_csv(filename)

# %%
