#%%
import os
import numpy as np
import json

list_of_files=os.listdir()
only_week_data=[]
for i in range(0,len(list_of_files)):
    if len(list_of_files[i])==15:
        only_week_data+=[list_of_files[i]]



dates=[]
for i in range(0,len(only_week_data)):
    dates+=[only_week_data[i][:10]]

dates_till_months=[]
for i in range(0,len(only_week_data)):
    dates_till_months+=[only_week_data[i][:7]]

dates_till_months=[*set(dates_till_months)]

week1=[]
week234=[]
week5=[]

for i in range(0,len(dates_till_months)):
    total_in_month=[]
    day_sort=[]
    for j in range(0,len(dates)):
        if dates_till_months[i] in dates[j]:
            total_in_month+=[dates[j]]
    for k in range(0,len(total_in_month)):
        day_sort+=[int(total_in_month[k][-2:])]
    if len(total_in_month)>1:
        hi=np.argmax(day_sort)
        li=np.argmin(day_sort)
        week5+=[total_in_month[hi]]
        week1+=[total_in_month[li]]
        a=total_in_month[hi]
        b=total_in_month[li]
        total_in_month.remove(a)
        total_in_month.remove(b)
        week234+=total_in_month
    if len(total_in_month)<=1:
        hi=np.max(day_sort)
        if hi>22:
            week5+=total_in_month
        if hi<8:
            week1+=total_in_month
        if hi>=8 and hi<=22:
            week234+=total_in_month
week234.remove('31-03-2021')
week1.remove('2023-03-16')

for i in range(0,len(only_week_data)):
    if only_week_data[i][:10] in week1:
        hh=json.load(open(only_week_data[i]))
        with open('week1/'+only_week_data[i][:10]+'.json', 'w') as json_file:
            json.dump(hh, json_file)

    if only_week_data[i][:10] in week234:
        hh=json.load(open(only_week_data[i]))
        with open('week234/'+only_week_data[i][:10]+'.json', 'w') as json_file:
            json.dump(hh, json_file)

    if only_week_data[i][:10] in week5:
        hh=json.load(open(only_week_data[i]))
        with open('week5/'+only_week_data[i][:10]+'.json', 'w') as json_file:
            json.dump(hh, json_file)
# %%
