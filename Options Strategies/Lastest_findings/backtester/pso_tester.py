#%%
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import json
import os
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
        fg_flow+=[fg]
        g_flow+=[g]
        if debug:
            print('Best after iteration {:}: {:} {:}'.format(it, g, fg))
        it += 1
    print('Stopping search: maximum iterations reached --> {:}'.format(maxiter))
    if not is_feasible(g):
        print("However, the optimization couldn't find a feasible design. Sorry")
    return g_flow, fg_flow

#data import
list_of_data=os.listdir()
train_data=[]
test_data=[]
for file_name in list_of_data:
    if 'json' in file_name:
        if np.random.rand()<0.8:
            train_data=train_data+[pd.DataFrame(json.load(open(file_name)))]
        else:
            test_data=test_data+[pd.DataFrame(json.load(open(file_name)))]
#%%
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
    A1=np.tanh(w11*np.array(data['hightime'])+c11)
    A2=np.tanh(w12*np.array(data['oi_ratio'])+c12)
    A3=np.tanh(w13*np.array(data['rosetta_ratio'])+c13)
    A4=np.tanh(w14*np.array(data['rosetta'])+c14)
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
xopt,fopt=pso(lossfunc,lb,ub,maxiter=80,swarmsize=1000)

#%%
#cross check plots
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
plt.plot(np.array(fopt)/len(train_data),'g')
plt.plot(np.array(fopt_test)/len(test_data),'r')
plt.legend(['train','test'])
plt.show()

# %%
