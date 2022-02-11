# Python program to read
# json file

#%%
import json

# Opening JSON file
f = open('variables.json')

# returns JSON object as
# a dictionary
data = json.load(f)
print(data)
# Iterating through the json
# list
print(data['days'])
print(data['expiry'])
print(data['money'])

# Closing file
f.close()

# %%
