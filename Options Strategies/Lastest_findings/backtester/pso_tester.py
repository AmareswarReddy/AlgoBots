#%%
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import json
from pyswarm import pso
#data import
f=open('4_08.json')
f1=open('2_08.json')
f2=open('1_15.json')
f3=open('3_08.json')
f4=open('4_15.json')
f5=open('0_15.json')
f6=open('1_08.json')
f7=open('4_22.json')
f8=open('3_15.json')

day1_data=pd.DataFrame(json.load(f))
day2_data=pd.DataFrame(json.load(f1))
day3_data=pd.DataFrame(json.load(f2))
day4_data=pd.DataFrame(json.load(f3))
day5_data=pd.DataFrame(json.load(f4))
day6_data=pd.DataFrame(json.load(f5))
day7_data=pd.DataFrame(json.load(f6))
day8_data=pd.DataFrame(json.load(f7))
day9_data=pd.DataFrame(json.load(f8))

train_data=[day7_data,day5_data,day3_data,day4_data,day5_data,day6_data,day7_data,day8_data,day9_data]
#model
def pnl(data):
    b=list(data['indicator']>0)+[0]
    b[0]=0
    s=list(np.array(data['indicator']<0)*-1)+[0]
    s[0]=0
    buyer=np.array(b[1:])-np.array(b[:-1])
    seller=np.array(s[1:])-np.array(s[:-1])
    trades=np.sum(buyer>0)+np.sum(seller<0)
    net_pnl=np.dot(buyer,np.array(data['lastrate']))+np.dot(seller,np.array(data['lastrate']))-trades*5
    return net_pnl

def indicator(w11,w12,w13,w14,c11,c12,c13,c14,outw11,outw12,outw13,outw14,outc11,outw21,outw22,outw23,outw24,outc21,data):
    #layer1
    A1=np.tanh(w11*data['hightime']+c11)
    A2=np.tanh(w12*data['oi_ratio']+c12)
    A3=np.tanh(w13*data['rosetta_ratio']+c13)
    A4=np.tanh(w14*data['rosetta']+c14)
    layer11=outw11*A1+outw12*A2+outw13*A3+outw14*A4
    layer12=outw21*A1+outw22*A2+outw23*A3+outw24*A4
    output1=np.tanh(layer11+outc11)
    output2=(np.tanh(layer12+outc21)+1)/2
    final_indicator=np.multiply((np.array(output2)>0.5),(np.array(output1>0)+np.array(output1<0)*-1))
    data['indicator']=final_indicator
    return data

# loss function
def lossfunc(x):
    # define data
    net_profit=0
    global train_data
    w11,w12,w13,w14,c11,c12,c13,c14,outw11,outw12,outw13,outw14,outc11,outw21,outw22,outw23,outw24,outc21=x[0],x[1],x[2],x[3],x[4],x[5],x[6],x[7],x[8],x[9],x[10],x[11],x[12],x[13],x[14],x[15],x[16],x[17]
    for data in train_data:
        data_=indicator(w11,w12,w13,w14,c11,c12,c13,c14,outw11,outw12,outw13,outw14,outc11,outw21,outw22,outw23,outw24,outc21,data)
        net_profit+=pnl(data_)
    return -net_profit

# optimisation
lb=[-5,-5,-5,-5,-5,-5,-5,-5,-5,-5,-5,-5,-5,-5,-5,-5,-5,-5]
ub=list(np.array(lb)+10)
xopt,fopt=pso(lossfunc,lb,ub,maxiter=100,swarmsize=100)

#%%
#cross check plots
f=open('2_15.json')
data_1=pd.DataFrame(json.load(f))
test_data=[data_1]
fopt_test=[]
def lossfunc_test(x):
    net_profit=0
    # define data
    global test_data
    w11,w12,w13,w14,c11,c12,c13,c14,outw11,outw12,outw13,outw14,outc11,outw21,outw22,outw23,outw24,outc21=x[0],x[1],x[2],x[3],x[4],x[5],x[6],x[7],x[8],x[9],x[10],x[11],x[12],x[13],x[14],x[15],x[16],x[17]
    for data in test_data:
        data_=indicator(w11,w12,w13,w14,c11,c12,c13,c14,outw11,outw12,outw13,outw14,outc11,outw21,outw22,outw23,outw24,outc21,data)
        net_profit+=pnl(data_)
    return -net_profit
for item in xopt:
    fopt_test+=[lossfunc_test(item)]
plt.plot(fopt)
plt.show()
plt.plot(fopt_test)
plt.show()

# %%
