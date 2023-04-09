#%%
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import json
import os
from itertools import permutations as pts
#best_xopt=[ 1.29612133,  3.26034414, -2.22526473, -2.10365809,  2.46393221, 1.12579777,  0.80702388,  1.85194385, -1.00989509,  2.88783666,-4.18620745,  3.40181159, -1.28250369,  2.25827503,  1.08763152,1.04109902,  2.53634001, -1.12328765]
def pso(func, lb, ub, ieqcons=[], f_ieqcons=None, args=(), kwargs={}, 
        swarmsize=100, omega=0.5, phip=0.5, phig=0.5, maxiter=100, 
        minstep=1e-8, minfunc=1e-8, debug=False):
    assert len(lb)==len(ub), 'Lower- and upper-bounds must be the same length'
    assert hasattr(func, '__call__'), 'Invalid function handle'
    lb = np.array(lb)
    ub = np.array(ub)
    assert np.all(ub>lb), 'All upper-bound values must be greater than lower-bound values'
    vhigh = np.abs(ub - lb)
    vlow = -vhigh
    # Check for constraint function(s) #########################################
    obj = lambda x: func(x, *args, **kwargs)
    if f_ieqcons is None:
        if not len(ieqcons):
            if debug:
                print('No constraints given.')
            cons = lambda x: np.array([0])
        else:
            if debug:
                print('Converting ieqcons to a single constraint function')
            cons = lambda x: np.array([y(x, *args, **kwargs) for y in ieqcons])
    else:
        if debug:
            print('Single constraint function given in f_ieqcons')
        cons = lambda x: np.array(f_ieqcons(x, *args, **kwargs))
        
    def is_feasible(x):
        check = np.all(cons(x)>=0)
        return check
    # Initialize the particle swarm ############################################
    S = swarmsize
    D = len(lb)  # the number of dimensions each particle has
    x = np.random.rand(S, D)  # particle positions
    v = np.zeros_like(x)  # particle velocities
    p = np.zeros_like(x)  # best particle positions
    fp = np.zeros(S)  # best particle function values
    g = []  # best swarm position
    fg = 1e100  # artificial best swarm position starting value
    for i in range(S):
        # Initialize the particle's position
        x[i, :] = lb + x[i, :]*(ub - lb)
        # Initialize the particle's best known position
        p[i, :] = x[i, :]
        # Calculate the objective's value at the current particle's
        fp[i] = obj(p[i, :])
        # At the start, there may not be any feasible starting point, so just
        # give it a temporary "best" point since it's likely to change
        if i==0:
            g = p[0, :].copy()
        # If the current particle's position is better than the swarm's,
        # update the best swarm position
        if fp[i]<fg and is_feasible(p[i, :]):
            fg = fp[i]
            g = p[i, :].copy()
        # Initialize the particle's velocity
        v[i, :] = vlow + np.random.rand(D)*(vhigh - vlow)
    # Iterate until termination criterion met ##################################
    it = 1
    fg_flow=[]
    g_flow=[]
    while it<=maxiter:
        rp = np.random.uniform(size=(S, D))
        rg = np.random.uniform(size=(S, D))
        for i in range(S):
            # Update the particle's velocity
            v[i, :] = omega*v[i, :] + phip*rp[i, :]*(p[i, :] - x[i, :]) + \
                      phig*rg[i, :]*(g - x[i, :])
            # Update the particle's position, correcting lower and upper bound 
            # violations, then update the objective function value
            x[i, :] = x[i, :] + v[i, :]
            mark1 = x[i, :]<lb
            mark2 = x[i, :]>ub
            x[i, mark1] = lb[mark1]
            x[i, mark2] = ub[mark2]
            fx = obj(x[i, :])
            # Compare particle's best position (if constraints are satisfied)
            if fx<fp[i] and is_feasible(x[i, :]):
                p[i, :] = x[i, :].copy()
                fp[i] = fx
                # Compare swarm's best position to current particle's position
                # (Can only get here if constraints are satisfied)
                if fx<fg:
                    if debug:
                        print('New best for swarm at iteration {:}: {:} {:}'.format(it, x[i, :], fx))
                    tmp = x[i, :].copy()
                    stepsize = np.sqrt(np.sum((g-tmp)**2))
                    if np.abs(fg - fx)<=minfunc:
                        print('Stopping search: Swarm best objective change less than {:}'.format(minfunc))
                        return tmp, fx
                    elif stepsize<=minstep:
                        print('Stopping search: Swarm best position change less than {:}'.format(minstep))
                        return tmp, fx
                    else:
                        g = tmp.copy()
                        fg = fx
        fg_flow.append(fg)
        g_flow.append(g)
        if debug:
            print('Best after iteration {:}: {:} {:}'.format(it, g, fg))
        it += 1
    print('Stopping search: maximum iterations reached --> {:}'.format(maxiter))
    if not is_feasible(g):
        print("However, the optimization couldn't find a feasible design. Sorry")
    return g_flow, fg_flow
#%%
#data import
list_of_data=os.listdir()
train_data=[]
test_data=[]
for file_name in list_of_data:
    if ('json' in file_name) and ('cred' not in file_name) and '1_' in file_name[:2]:# or '4_' in file_name[:2]):
        if np.random.rand()<0.8: # "3_'2022-12-15" not in file_name:#"4_" not in file_name:#
            train_data=train_data+[pd.DataFrame(json.load(open(file_name)))]
        else:
            test_data=test_data+[pd.DataFrame(json.load(open(file_name)))]

#data processing
for i in range(0,len(train_data)):
    train_data[i]['lastrate']=(train_data[i]['lastrate']/train_data[i]['lastrate'][0])*100-100
    train_data[i]['time']=(train_data[i]['time']/22500)


for i in range(0,len(test_data)):
    test_data[i]['lastrate']=(test_data[i]['lastrate']/test_data[i]['lastrate'][0])*100-100
    train_data[i]['time']=(train_data[i]['time']/22500)

def lastrate_map(data):
    mapping_json={}
    for i in range(0,len(data)-8):
        variables=list(np.reshape(np.array(data.loc[i:i+7]),(64,)))+[1]
        t=i+8
        mapping_json[t]=[variables,float(data['lastrate'].loc[8])]
    return mapping_json
#Eg: mapping_json={time:[[variables],lastrate]}

train_data_mapping_jsons=[]
test_data_mapping_jsons=[]

for i in train_data:
    train_data_mapping_jsons+=[lastrate_map(i)]

for i in test_data:
    test_data_mapping_jsons+=[lastrate_map(i)]
#%%
#model


def polynomial(x,mapping_json):
    est_lastrate=[]
    for i in list(mapping_json.keys()):
        i=int(i)
        test_list=mapping_json[i][0]
        #res = [(a* b) for idx, a in enumerate(test_list) for b in test_list[idx + 1:]]+list(np.multiply(test_list,test_list))
        res2=np.dot(np.reshape(test_list,(len(test_list),1)),np.reshape(test_list,(1,len(test_list))))
        res2[np.tril_indices(res2.shape[0], -1)] = np.inf
        m,n=np.shape(res2)
        w=np.reshape(res2,(m*n,))
        res=w[w!=np.inf]
        est_lastrate.append(np.dot(x,res))
    return np.array(est_lastrate)

def lossfunc(x):
    deviation=0
    global train_data
    for i in range(0,len(train_data)):
        mapping_json=train_data_mapping_jsons[i]
        actual_lastrate=np.array(pd.DataFrame(mapping_json).loc[1])
        est_lastrate=polynomial(x,mapping_json)
        temp=actual_lastrate-est_lastrate
        deviation+=np.dot(temp,temp)
    return deviation



def lossfunc_test(x):
    deviation=0
    global test_data
    for data in test_data:
        mapping_json=lastrate_map(data)
        actual_lastrate=np.array(pd.DataFrame(mapping_json).loc[1])
        est_lastrate=polynomial(x,mapping_json)
        temp=actual_lastrate-est_lastrate
        deviation+=np.dot(temp,temp)
    return deviation



#%%
#finding xopt


mapping_json=lastrate_map(train_data[0])
test_list=mapping_json[8][0]
x=np.ones((len([(a* b) for idx, a in enumerate(test_list) for b in test_list[idx + 1:]]+list(np.multiply(test_list,test_list))),))
lb=x-2
ub=x
#%%
import time
a=time.time()
xopt,fopt=pso(lossfunc,lb,ub,maxiter=100,swarmsize=1000)
b=time.time()
print(b-a)
#%%
fopt_test=[]
for item in xopt:
    fopt_test+=[lossfunc_test(item)]
plt.plot(np.array(fopt)/len(train_data),'g')
plt.plot(np.array(fopt_test)/len(test_data),'r')
plt.legend(['train','test'])
plt.show()
#%%
for i in range(0,len(test_data)):
    test_data[i]['est_lastrate']=polynomial(xopt[-1],lastrate_map(test_data[i]))
    #train_data[i]=polynomial(xopt[-1],lastrate_map(train_data[i]))
    fig, ax_left = plt.subplots()
    ax_right = ax_left.twinx()
    ax_left.plot(test_data[i]['lastrate'], color='white')
    ax_right.plot(test_data[i]['est_lastrate'], color='orange')
    plt.show()

# %%
