#%%
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import json
import os
import statistics
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
#%%
#data import
list_of_data=os.listdir()
train_data=[]
test_data=[]
for file_name in list_of_data:
    if len(file_name)==15:
        if np.random.rand()<1.1:# and "2023-03-23.json"  in file_name:#"4_" not in file_name:#
            train_data=train_data+[pd.DataFrame(json.load(open(file_name)))]
            #break
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
    net_pnl=-np.dot(buyer,np.array(data['lastrate']))-np.dot(seller,np.array(data['lastrate']))-trades*12
    if net_pnl<0:
        net_pnl*=1
    return net_pnl

def pnl2(data):
    #oi_chains=data['option_chains']
    lastrates=list(data['lastrate'])
    #b_strike=0
    #s_strike=0
    #n_strike=0
    b=list(data['indicator']>0)+[0]
    b[0]=0
    s=list(np.array(data['indicator']<0)*-1)+[0]
    s[0]=0
    n=list(np.array(data['indicator']==0)*1)+[0]
    n[0]=0
    buyer=np.array(b[1:])-np.array(b[:-1])
    seller=np.array(s[1:])-np.array(s[:-1])
    neutral=np.array(n[1:])-np.array(n[:-1])
    trades=np.sum(buyer>0)+np.sum(seller<0)+np.sum(neutral>0)
    net_pnl=-np.dot(buyer,np.array(data['lastrate']))-np.dot(seller,np.array(data['lastrate']))-trades*5
    k=np.multiply(neutral,np.array(data['lastrate']))
    r=0
    def h_range_profit(lastrates_list):
        a=lastrates_list[0]
        good=0
        for i in range(0,len(lastrates_list)-1):
            if lastrates_list[i]>a and a>lastrates_list[i+1]:
                good+=1
            if lastrates_list[i]<a and a<lastrates_list[i+1]:
                good+=1
        mean = sum(lastrates_list) / len(lastrates_list)
        variance = sum([((x - mean) ** 2) for x in lastrates_list]) / len(lastrates_list)
        res = variance ** 0.5
        return good*res
    for i in range(0,len(k)):
        if k[i]!=0 and r==0:
            l=lastrates[i]
            index=i
            r=1
        elif k[i]!=0 and r==1:
            m=lastrates[i]
            net_pnl+=-(0.7)*(i-index)-abs(m-l)-abs(np.mean(lastrates[index:i])-m)-abs(np.mean(lastrates[index:i])-l)+h_range_profit(lastrates[index:i])
            r=0
    if net_pnl<0:
        net_pnl*=2
    return net_pnl-trades*6

def indicator(x,data):
    def node_out(input_,weights_bias):
        return np.tanh(weights_bias[0]*input_[0]+weights_bias[1]*input_[1]+weights_bias[2]*input_[2]+weights_bias[3]*input_[3]+weights_bias[4]*input_[4]+weights_bias[5]*input_[5]+weights_bias[6]*input_[6]+weights_bias[7]*input_[7]+weights_bias[8]*input_[8]+weights_bias[9])
    input_=[np.array(data['market_ripper']),np.array(data['day_volume_indicator']),np.array(data['day_market_ripper']),np.array(data['hightime']),np.array(data['oi_ratio']),np.array(data['rosetta_ratio']),np.array(data['rosetta']),np.array(data['time']/22440),np.array(data['volume_ind'])]
    x_=np.reshape(x,(82,len(input_)+1))
    index=0
    for j in range(0,9):
        A=[]
        for i in range(0,9):
            A+=[node_out(input_,x_[index])]
            index+=1
        input_=A
    ultimatum=node_out(input_,x_[index])
    final_indicator=np.array(ultimatum>0)+np.array(ultimatum<0)*-1
    data['indicator']=final_indicator
    return data
    #return ultimatum

def indicator2(x,data):
    def node_out(input_,weights_bias):
        return np.tanh(weights_bias[0]*input_[0]+weights_bias[1]*input_[1]+weights_bias[2]*input_[2]+weights_bias[3]*input_[3]+weights_bias[4]*input_[4]+weights_bias[5]*input_[5]+weights_bias[6]*input_[6]+weights_bias[7]*input_[7]+weights_bias[8]*input_[8]+weights_bias[9])
    input_=[np.array(data['market_ripper']),np.array(data['day_volume_indicator']),np.array(data['day_market_ripper']),np.array(data['hightime']),np.array(data['oi_ratio']),np.array(data['rosetta_ratio']),np.array(data['rosetta']),np.array(data['time']/22440),np.array(data['volume_ind'])]
    x_=np.reshape(x,(83,len(input_)+1))
    index=0
    for j in range(0,9):
        A=[]
        for i in range(0,9):
            A+=[node_out(input_,x_[index])]
            index+=1
        input_=A
    ultimatum=node_out(input_,x_[index])
    ultimatum2=node_out(input_,x_[index+1])
    final_indicator1=np.array(ultimatum>0)+np.array(ultimatum<0)*-1
    final_indicator2=np.array(ultimatum2>0)+np.array(ultimatum2<0)*0
    data['indicator']=final_indicator1*final_indicator2
    #data['indicator']=final_indicator
    return data
    #return ultimatum




# loss function
def lossfunc(x):
    # define data
    net_profit=0
    global train_data
    for data in train_data:
        #try:
        data_=indicator(x,data)
        net_profit+=pnl(data_)
        #except Exception:
        #    pass
    return -net_profit
#%%
# optimisation
lb=[]
for i in range(0,830):
    lb+=[-10]
ub=list(np.array(lb)+20)
xopt,fopt=pso(lossfunc,lb,ub,maxiter=25,swarmsize=5000)

#%%
#cross check plots
fopt_test=[]
def lossfunc_test(x):
    net_profit=0
    # define data
    global test_data
    for data in test_data:
        try:
            data_=indicator(x,data)
            net_profit+=pnl(data_)
        except Exception:
            pass
    return -net_profit
for item in xopt:
    fopt_test+=[lossfunc_test(item)]
plt.plot(np.array(fopt)/len(train_data),'g')
plt.plot(np.array(fopt_test)/len(test_data),'r')
plt.legend(['train','test'])
plt.show()
#%%
for i in range(0,len(test_data)):
    test_data[i]=indicator(xopt,test_data[i])
    fig, ax_left = plt.subplots()
    ax_right = ax_left.twinx()
    ax_left.plot(test_data[i]['lastrate'], color='white')
    ax_right.plot(test_data[i]['indicator'], color='orange')

    plt.show()


#%%
def max_loss(x):
    loss=1000
    global train_data
    for data in train_data:
        try:
            data_=indicator(x,data)
            if pnl(data_)<loss:
                loss=pnl(data_)
        except Exception:
            pass
    global test_data
    for data in test_data:
        try:
            data_=indicator(x,data)
            if pnl(data_)<loss:
                loss=pnl(data_)
        except Exception:
            pass
    return loss
def success_ratio(x):
    profit_days=0
    net_profit=0
    loss_days=0
    net_loss=0
    pnl_plot=[]
    global train_data
    for data in train_data:
        try:
            data_=indicator(x,data)
            shear_will=pnl(data_)
            if shear_will>0:
                profit_days+=1
                net_profit+=shear_will
                pnl_plot+=[shear_will]
            else:
                loss_days+=1
                net_loss+=shear_will
                pnl_plot+=[shear_will]
        except Exception:
            pass
    global test_data
    for data in test_data:
        try:
            data_=indicator(x,data)
            shear_will=pnl(data_)
            if shear_will>0:
                profit_days+=1
                net_profit+=shear_will
                pnl_plot+=[shear_will]
            else:
                loss_days+=1
                net_loss+=shear_will
                pnl_plot+=[shear_will]
        except Exception:
            pass
    success_ratio=profit_days/loss_days
    avg_profit=net_profit/profit_days
    avg_loss=-net_loss/loss_days
    risk_to_reward=(avg_loss/avg_profit)
    plt.plot(pnl_plot)
    return success_ratio,risk_to_reward,avg_profit,avg_loss,pnl_plot
#%%
xopt_json={}
for i in range(0,len(xopt)):
    xopt_json[i]=xopt[i].tolist()

out_file = open('xopt_backtester2.json', "w")
json.dump(xopt_json, out_file)
out_file.close()


#%%


# %%
xopt=[ 1.83470370e+01,  1.45728705e+01,  1.41472216e+01, -6.88230338e+00,
   -8.75698332e+00, -2.06859319e+01, -1.18086614e+01,  1.39622014e+01,
   -5.75393989e+00,  4.73370187e+00,  2.48271771e+01, -1.11266281e+01,
   -9.20013764e+00,  1.37846619e+01, -1.92582248e+01, -2.34012332e+01,
    9.61221910e+00,  1.03919993e+01, -3.48786893e+00,  2.12263036e+01,
    1.43668658e+01, -2.01223757e+01, -2.92780384e+01, -4.36814770e+00,
    1.88358468e+01,  9.80858384e+00,  2.85297812e+01, -3.86630553e+00,
   -1.46802026e+01, -3.00000000e+01,  2.29923601e+00, -8.22205952e+00,
    1.51065500e+01, -1.97383607e+01, -2.11078725e-02, -3.00000000e+01,
    1.67016251e+01,  1.35856612e+01, -1.10747763e+01, -6.40618409e+00,
    6.08068368e+00,  1.00231352e+01,  1.21616648e+01, -1.24424641e+01,
   -9.18686595e+00, -1.50132096e+01,  1.89310064e+01, -1.01666771e+00,
    4.64600937e-01,  2.11663819e+01,  1.94336698e+01, -4.09104894e+00,
    1.10963430e+00, -2.39419175e+01,  2.83035181e+01,  7.24378220e+00,
    2.29126589e+00,  7.01194816e+00, -2.49591398e+01, -1.66721431e+01,
    5.10303950e+00, -2.39198189e+01, -2.42762850e+01,  2.87040165e+01,
    1.70968196e+01,  2.96541493e+01,  1.37816069e+01, -3.55672188e+00,
   -5.62280851e+00, -1.62093867e+01, -5.32768067e+00,  2.20327409e+00,
    8.98977519e+00,  9.52593374e+00,  7.63361582e-02, -2.23340529e+01,
   -6.85167183e+00,  1.91426134e+01,  2.34463289e+01, -2.70711941e+01,
   -1.29688855e+01,  5.62758599e+00,  1.91451240e+00, -2.67592467e+01,
    1.89595664e+01, -3.46547357e+00, -3.00000000e+01, -5.65046053e+00,
    4.62151554e+00, -9.26513016e-01, -1.18956969e+01, -1.14880137e+01,
    1.67321031e+01,  2.16781388e+01, -6.77749242e+00, -6.17643292e+00,
    1.33628813e+01, -5.58527286e+00,  5.21577736e+00, -2.59235409e+01,
   -3.43396094e+00,  1.13038600e+01, -2.95142304e+00, -1.98564894e+01,
   -2.68934843e+01, -3.67507736e+00, -6.30856684e+00, -8.57027929e+00,
    8.52857414e+00,  7.28818577e+00, -3.68080635e+00, -1.06888580e+01,
    3.67433451e+00,  9.08843641e+00, -8.78509939e+00,  1.36408310e+01,
   -1.72001894e+01,  2.87315006e+00, -2.00643525e+01,  2.34675406e+01,
   -1.43116305e+00, -6.07203957e+00,  4.79124490e-01, -1.81128338e+01,
   -1.84252055e+01, -1.60252249e+01,  2.07295221e+00,  2.96458600e+01,
   -1.23775800e+01,  2.55807935e+01, -4.84929811e+00,  1.25657552e+01,
   -2.04851817e+01, -1.74978558e+01,  1.58041535e+01,  2.27540734e+01,
    1.92577604e+01,  7.74395614e-01, -2.58280100e+01, -4.79056848e+00,
   -1.15375373e+01,  5.68246453e+00, -1.65025062e+01, -1.91208771e+01,
   -2.72862773e+01, -1.64710603e+01, -1.28148676e+01, -5.18744239e+00,
   -5.40964725e+00, -1.17708198e+01,  5.85225734e+00,  2.46051951e+01,
    1.11464446e+01, -3.24666944e+00, -2.54832266e+01, -1.16593123e+01,
   -4.24061349e+00, -4.33543882e+00, -2.12931276e-01,  5.33841483e+00,
   -1.71679469e+01, -4.66474235e+00, -1.20721823e+01, -1.81359121e+01,
    3.16593465e+00, -2.28100234e+00,  1.27507981e+01, -1.69475628e+01,
    1.25143598e+01, -1.03902498e+01,  2.25861816e+00,  1.85445654e+00,
    1.22651143e+01,  2.96868018e+00,  1.51202655e+01,  2.45601485e+01,
   -6.47109955e+00,  1.18274274e+01,  1.76322340e+01, -1.47131295e+01,
    2.49236830e+01, -2.75229008e+01, -1.25792537e+00,  1.84466703e+01,
   -2.08613120e+01, -7.10574799e-01,  1.55689891e+01, -5.14042339e-01,
   -1.65827680e+01, -7.38615206e+00, -2.37436860e+01, -5.21631342e+00,
   -1.28292910e+01, -2.00526304e+01, -1.64976777e+01,  4.53889264e-01,
   -9.36039754e-01, -1.88234259e+01, -1.00436184e+01, -9.98277260e+00,
    5.64951420e+00, -2.28866826e+01, -5.36005318e+00,  1.28602123e+01,
    3.87781939e+00, -2.52151091e+01,  5.45969310e+00, -1.30783108e+01,
    1.29529589e+01,  1.27107714e+00, -3.26528469e+00,  2.92667839e+00,
    1.79410779e+01,  9.02835517e-01,  5.08809498e-01, -2.47336474e+00,
   -1.85937733e+01, -9.14033269e+00, -6.55242669e+00,  1.50856310e+01,
   -3.63214494e+00, -1.70461735e+01, -2.23662312e-01,  2.72651363e+00,
    3.00250627e+00, -1.03040419e+01,  6.76130934e+00,  8.10814997e+00,
    1.48325848e+01,  8.20296765e+00,  1.52680900e+01,  1.49065556e+00,
   -2.09173582e+01,  1.27290974e+01,  1.87980032e+01, -2.87349606e+01,
    1.05223440e+01,  2.61867780e+01, -5.55174954e+00, -4.99270110e+00,
   -1.00653469e+01,  2.25519604e+01, -1.13700720e+01, -1.17423350e+00,
   -1.87099320e+00,  7.46502765e+00, -2.67369059e+01,  1.88474464e+01,
   -4.44463013e+00, -6.01820606e+00, -1.87348720e+00, -7.02443843e+00,
   -7.85910430e+00, -1.69627428e+01, -1.57506185e+01, -2.10005143e+01,
    6.52347854e+00,  1.43595507e+01, -1.44610907e+01, -5.08982955e+00,
    6.14063665e+00,  1.60008830e+01,  2.64130742e+01,  1.39064292e+01,
   -5.41684585e+00,  2.82075500e+00,  1.12788112e+01, -5.07919357e-01,
    6.41463736e+00,  1.70462151e+00,  2.13742248e+01, -1.74868698e+00,
    4.93957211e+00, -1.61020059e+01,  2.02320102e+01,  3.14638576e+00,
    1.80004330e+00, -3.10229425e+00, -2.48334390e+01, -2.48882337e+01,
   -7.81376728e+00, -2.49527338e+01,  1.93986518e+01,  1.92887763e+01,
   -8.41620551e+00,  1.65374785e+01,  7.80214694e+00,  1.18196790e+01,
    1.25140320e+01,  1.65136196e+01,  1.95613602e+01,  6.50630372e+00,
    4.55048564e+00,  1.04071300e+01,  1.81345181e+01, -9.77205818e+00,
   -6.33343339e+00,  1.66763899e+01, -7.78457275e+00,  9.41761730e+00,
    1.01776546e+01,  6.68203344e+00,  2.32057810e+01,  9.12378722e+00,
    2.67661699e+00, -1.97550662e+01,  1.02593090e+01, -1.18382915e+01,
   -6.98399899e+00,  1.52654918e+01, -2.27301831e+01, -2.45850783e+01,
    8.03622702e+00, -2.01945947e+00, -8.16504049e+00,  3.81581978e+00,
   -3.96023276e-01,  5.02865552e+00,  1.88032683e+01, -2.78783987e+01,
   -8.54653646e+00, -1.12595728e+00, -1.16211955e+01,  3.38045519e+00,
    9.47166326e+00,  1.23495019e+01, -3.13689481e+00, -6.36458165e+00,
    1.07820415e+01,  1.90361413e+00,  1.40395873e+01, -3.34411759e+00,
    8.38648889e+00,  2.38942068e+01,  2.67700292e+01,  1.66147195e+01,
    4.68114575e+00,  8.61673145e+00, -2.46970786e+00,  3.38054841e+00,
   -7.53296750e-01,  9.18714213e+00,  7.38544797e+00, -6.72502466e+00,
   -8.86050099e+00, -1.70117131e+00,  1.41547592e+01, -2.01349911e+01,
    2.50262235e+00, -1.07698788e+01,  2.16695817e+01,  1.55273509e+01,
    6.62017712e+00, -5.45605889e+00, -4.93735428e+00, -8.77898540e+00,
    1.40297850e+01, -8.85927919e+00, -6.14513004e+00,  1.40151128e+01,
    3.29179154e+00, -1.48204362e+01, -1.62090327e+01, -2.21136974e+01,
    1.45317502e+01,  1.59894481e+01, -3.01737140e+00, -1.21649464e+01,
    9.79158195e-01,  2.77181337e+01, -1.56618836e+01,  7.32993408e+00,
    1.54911660e+01,  7.58169967e+00,  5.54334777e+00, -1.23333115e+01,
   -1.27906187e+00, -9.97004066e+00,  1.62923977e+01, -2.13503570e-01,
   -8.68758476e-01,  2.07496226e+01, -3.18243475e+00, -7.46262352e+00,
   -7.81876663e+00, -1.16142374e+01,  2.20456986e+01, -1.19061926e+00,
   -9.92263676e+00,  2.44191796e+01, -2.45854192e+01,  2.26484430e+01,
    9.46034345e+00, -2.28228337e+00,  1.30846369e+01,  1.12475326e+01,
   -4.33064542e+00,  1.03879293e+01,  1.49007996e+01,  4.48159071e-01,
   -7.39785932e+00, -2.20444170e+00, -5.27180976e+00, -8.72522562e+00,
   -6.15349521e+00, -2.09506774e+00,  3.41134806e+00,  2.72244488e+01,
    4.51808479e+00,  1.13927909e+01, -8.09934037e+00, -1.67283246e+00,
    8.17723870e-01, -9.51795387e+00,  7.12363892e+00,  1.40538274e+01,
   -9.88751139e+00, -1.23842944e+01, -2.07932361e+01,  1.70854693e+01,
   -8.10197684e+00,  1.49190047e+01, -9.36949885e-01, -1.74572890e+00,
    6.22625735e-01,  1.72367239e+01, -6.70163424e+00, -4.72214064e+00,
   -1.03793235e+00,  1.28289314e+01, -9.67403223e+00, -2.51423933e+01,
   -1.08649616e+01,  3.00000000e+01, -2.36148766e+01,  1.25021964e+01,
   -1.93988930e+00,  3.16043771e+00, -2.21950349e+01,  9.98995892e+00,
   -1.69643624e+01, -2.45989294e+01,  2.48141358e+01, -2.76572568e+00,
   -1.56170852e+01,  1.25279647e+01,  2.07662831e+00,  1.03141571e+01,
   -9.45040454e+00, -3.02101559e+00, -1.57019351e+01, -1.36078747e+01,
   -1.92301804e+01,  2.12571749e+01,  1.47847193e+01, -2.95973752e+00,
   -1.91716652e+01, -4.92077664e-01,  1.14839866e+01,  1.17975640e+00,
    2.41749706e+01,  4.49943967e+00, -1.79775154e+01,  3.97449971e+00,
   -7.97483880e+00,  9.99411053e+00, -1.04109197e+01, -1.00519112e+01,
    1.67393003e+01, -1.74175380e+01, -1.11127808e+01, -2.03425498e+00,
    2.94816732e-01,  9.30765399e+00, -1.59220826e+01, -1.38557705e+01,
    2.29571208e+00,  5.64840922e+00, -5.93326924e+00, -9.88087851e+00,
    4.52711912e+00,  2.06418479e+01,  4.29062216e+00, -1.00552613e+01,
    1.01678339e+01,  9.08533507e+00,  1.94053295e+01, -1.59222772e+01,
    5.11640314e+00, -2.97451005e+01,  1.08763776e+01,  1.06929629e+00,
    9.46177099e+00, -1.98891183e+00, -9.77466866e+00, -3.62536238e+00,
    2.77064145e+00,  1.54450822e+01,  2.12674618e+01, -7.46519721e+00,
    3.96122510e+00, -5.34778751e-01, -1.53627217e+01, -2.98060985e+01,
   -6.60382121e+00,  7.90737872e+00,  2.58165566e+01,  5.80123601e+00,
   -1.41547404e+01,  1.04595326e+01,  1.32736379e+00,  1.22214581e+01,
    2.69362918e+01, -7.02744379e-01, -2.26912074e+01, -4.76310820e+00,
   -1.28806442e+00, -5.31249684e+00, -7.33419815e+00, -2.09105485e+01,
   -8.08748774e+00,  1.79220159e+01, -2.10510940e+01, -5.96544400e+00,
    1.61184968e+01, -8.45430620e+00,  2.59233639e+01,  1.66649531e+01,
    2.41719599e+01,  1.21442943e-01, -1.10133024e+01,  2.28837733e+01,
    3.00000000e+01,  1.14550063e+01, -8.74314222e+00,  6.74193693e+00,
    5.02717483e+00,  9.47970027e+00, -1.11193940e+00,  9.50541989e+00,
   -3.29255964e+00, -7.07756543e+00,  9.73738647e+00, -3.21280985e-01,
   -3.16731149e+00,  1.16429211e+01, -1.68520720e+01, -4.64876612e+00,
   -4.27813383e+00, -2.83519765e+01,  3.97856671e+00,  2.64947743e+01,
    3.29230801e+00, -7.31948324e+00,  4.85919738e+00, -9.09089113e+00,
    1.97156710e+01,  1.36428237e+01,  8.55950812e+00, -5.19954602e+00,
   -1.85450510e+01, -5.83929971e+00, -1.07830852e+01, -1.40244548e+01,
   -1.36206659e+01, -1.40469537e+01, -2.18673459e+01,  2.52131995e+01,
    1.23040721e+01, -1.78176636e+01, -9.40547352e+00, -2.18073125e+01,
   -1.29022276e+01, -1.41593286e+01, -1.01127956e+00, -2.16203232e+01,
    1.67804755e+01, -7.51942691e+00, -1.47451839e+01, -1.28557143e+01,
   -1.79878107e+01,  2.81292011e+01,  1.93544188e+01, -1.05496741e+01,
   -7.92964879e+00,  2.46408677e+01,  6.22675295e+00,  2.20151234e+01,
    4.11000765e+00, -2.33007218e+00, -8.33148768e+00,  1.46385398e+01,
   -1.76191519e+01,  1.98130752e+01,  8.72366081e+00, -1.93637012e+01,
   -1.66403229e+01,  2.42661579e+01,  1.18733056e+01,  6.44950633e+00,
   -3.03017789e-01, -1.46782995e+01,  1.67803654e+01, -6.54356269e+00,
    3.18601657e+00,  7.22178432e+00, -1.83666643e+01, -1.00768265e+01,
    1.80335235e+01, -1.01952069e+01, -6.59579329e+00,  3.14553973e+00,
   -5.42215699e+00,  9.64644893e-01, -2.01813224e+01,  9.29732575e+00,
   -4.55492551e+00, -2.44674105e+01, -1.99763283e+01,  6.59423014e+00,
   -5.38276973e+00,  9.94294400e+00,  1.32011676e+01, -1.34240850e+01,
    9.35200012e+00, -1.82526498e+01, -4.33682828e+00,  1.72890326e+01,
    2.05463954e+01, -1.08753688e+01, -3.10791821e+00, -5.38255110e+00,
    7.89501082e-02,  4.50851955e+00,  1.48288498e+01, -1.67401809e+01,
   -9.06420519e+00,  2.48691430e+01,  1.17402037e+01, -2.21761440e+01,
   -2.01362649e+01, -2.36296314e+01,  1.53262159e+01,  1.11075962e+01,
    2.05491235e+01, -1.79991938e+01,  1.97358876e+01,  8.14074478e+00,
    5.84496912e+00, -1.46318881e+01,  7.55350513e+00, -4.57499008e+00,
   -1.79988019e+01, -1.97149242e+01,  1.15758797e+01,  1.56382627e+01,
    5.40615411e+00,  1.19752930e+00, -1.56233899e+01,  1.63099721e+01,
    8.96440227e+00,  2.85838972e+01,  1.96123987e+00, -1.44663331e+01,
    4.64670037e+00,  2.88927851e-01,  1.54145158e+01,  2.24342736e+01,
   -1.16615566e+01,  2.15826028e+01,  1.23176891e+01, -1.92752350e+01,
   -1.03993969e+01,  1.12469941e+01, -1.23222782e+01, -1.15402490e+01,
   -2.88233883e+01, -1.10414942e+01,  1.64426004e+01,  1.50227810e-01,
   -2.42919146e+01,  9.41393304e+00, -8.63257917e+00,  1.79313537e+01,
   -1.36480830e+01,  1.45123445e+01,  2.77446395e+00, -4.01682429e-01,
   -1.53738919e+01,  5.72396337e-01, -3.54972784e+00, -1.99930788e+01,
   -9.22333369e+00,  2.31191373e+01, -1.26699045e+01, -6.94377426e+00,
   -2.06914393e+01,  1.65227673e+01, -1.76781535e+01,  2.80885549e+00,
   -2.83942205e+01,  3.91149205e+00, -1.88794403e+01,  2.06415836e+01,
    2.62890807e+01,  1.48338951e+01,  3.94217445e+00, -2.11299673e+01,
    8.67763672e+00,  1.42254526e+01, -1.18800287e+01, -5.33825838e+00,
   -1.76999624e+01, -1.49246519e+01, -1.06980697e+00,  1.21975990e+01,
    1.29526903e+01,  1.57076698e+01,  6.83138034e+00,  3.27725302e+00,
    8.09869165e+00, -2.13334757e+01, -7.04527961e+00,  1.77731125e-01,
    6.17487068e+00, -5.58259684e+00,  2.68876105e+01,  5.62638530e+00,
   -2.72422137e+01, -4.77613018e+00, -1.19607440e+00, -1.05468645e+01,
   -2.29271193e+01, -2.31078595e+01, -1.07597988e+01, -8.04839018e+00,
   -9.84791403e+00,  2.39485158e+01,  8.14301430e+00, -2.08460202e+01,
    7.94696760e+00, -1.13300943e+01,  1.90334639e+01,  5.12037049e+00,
    5.26524656e+00, -3.91680597e-01,  9.50011138e-01, -1.77724947e+01,
    3.32069273e+00, -9.19633883e+00, -5.87311072e+00, -9.48478904e+00,
    1.65976247e+00, -3.25571553e+00, -2.35897448e+01,  7.47045363e+00,
    1.03688999e+01, -6.41868587e+00, -1.39662297e+01,  2.33805281e+00,
    3.69727527e+00,  2.00680835e+01,  1.04719995e+01, -6.19538373e+00,
    7.38632583e+00,  1.53710533e+01, -1.31427089e+01,  4.13455160e+00,
   -2.52205330e+01,  7.52673608e+00, -1.74031251e+01, -1.98772329e+01,
   -8.34391071e+00, -5.91201069e+00, -3.52697811e+00,  8.03928154e+00,
    1.69169571e+01,  1.33765145e+01,  3.10552751e+00,  3.34352973e+00,
    1.28299911e+00,  1.18133115e+01, -2.06998514e+01,  1.89190421e+01,
    1.75352137e+01, -1.27644292e+01, -1.63356223e+01, -1.33512609e+01,
   -2.25823874e+00, -1.80188192e+01,  7.90608958e-01, -1.73910180e+01,
   -3.80538985e+00,  5.07047268e+00,  2.26795356e+01,  1.11935863e+01,
   -4.50283150e+00,  1.00752711e+01, -7.02204793e+00,  1.86882737e+01,
    2.82441159e+01,  1.12244540e+01, -9.90088403e+00, -2.62243897e+01,
   -9.99865447e+00,  2.16729651e+01,  1.73336877e+01, -1.20438898e+01,
   -1.98962367e+01, -9.87347183e-01,  9.04527577e+00,  1.41345948e+00,
   -1.43600967e+01, -2.12974356e+01,  1.87448244e+01,  5.04432340e+00,
    3.69295422e+00,  1.25410184e+01, -1.50000229e+01,  1.74943443e+00]
# %%
#Eg: if 10 rupees deployed and the profit be 3 rupees, avg_profit=1.3
def capital_to_deploy(success_ratio,avg_profit):
    import random
    prob_success=(success_ratio/(success_ratio+1))
    # x is percentage of capital deployed
    def profit_for_capital_deployed(x,prob_success):
        pnl_samples=[]
        for j in range(1,100):
            capital=100
            for i in range(0,100):
                y=x*capital/100
                if i<96 and i>4:
                    capital+=-y+y*((random.random()<prob_success)*avg_profit+(random.random()>prob_success)*0)
                else:
                    capital-=y
            pnl_samples+=[capital]
        return min(pnl_samples)
    best_capital_to_deploy=[]
    for x in range(0,100):
        best_capital_to_deploy+=[profit_for_capital_deployed(x,prob_success)]
    plt.plot(best_capital_to_deploy)
    print(max(best_capital_to_deploy))
    return np.argmax(best_capital_to_deploy)



# %%
