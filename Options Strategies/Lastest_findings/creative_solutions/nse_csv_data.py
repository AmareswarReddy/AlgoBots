# %%
import yfinance as yf
import requests
import json
import pandas as pd
import numpy as np
import csv
from io import StringIO
import matplotlib.pyplot as plt
from datetime import date, timedelta
headers = {
    "User-Agent": "Mozilla/5.0 (compatible; Rigor/1.0.0; http://rigor.com)",
    "Accept": "*/*",
    "cookie": '_gid=GA1.2.1673706531.1679333322; _ga=GA1.1.1494217993.1679333320; _ga_PJSKY6CFJH=GS1.1.1679333320.1.1.1679333421.24.0.0; NSE-TEST-1=1910513674.20480.0000; ak_bmsc=A632A18DBFA5CBDB59314D3EB54EE169~000000000000000000000000000000~YAAQ1C/JF4kly+eGAQAA/x1eBBPmGTDMzYmxSsGvSGeAXo8u8lCD0rIbm9ysz6MTJoOIWAbJexrYmFp1aJphJsACESRI7TeJIhbj1o1Ge0DD8zAOMEgIwZPn92RmdBzFZjT/VoJdE6oTloevFp4VgkHzkjvWGawkfX7T+fA/UO1GW+hQks93QW7oHkntCTHPJ/LZ//WxtawmMJ0HmYkLIxVzABysAfbhXLBvpexsXTF0bCPbNpXOHfj4JAxRtSEk48WSeJCD/n7/DQLuj1xahVDcWXhK0YEPVGilfxEKCmWct0/U2GwwioztXKXbASXFn3HKmynJZkVCCIhJr52gI3WYZCiupviBa1w2cl8+jAbPCAoABJLyAKIHOr4dE2kG; bm_mi=C1FABE0F02D63418DFA41F7A7D368572~YAAQ1C/JF88ly+eGAQAAY3ZeBBNA9wXoAs9Ekm4+SRBA4HUyNRFXJ39qjcpyEaBtEv5709XGwcMe+O3YY5CO7nGloVACNqhL1z+Z6LLD7zYtXcvLj8Nvzi4OFKuhpbIAi+oqOE38IjpBiFAGAuBKU4V12SGCRyyp62myzOs/1l8tlBqtpM3UlY7xyKrSYfulH5ft4tLxFIhQU7zubhjH+vosjmZtv1wTJiahSbY3zlssYLpum2a6dROxY6rCREPpR6/rIGzoFNUEFQJVcCK3B004AlhQQK6JnohAHayxieYTKLAgtdU4mmsYPOzaVTkizSG8D9B2gTcxzwlXHYtOVOoL5hWD+a/ldgk9jXuYBOynPhpS1rnn65H7pkwvlt2s/2jXUg==~1; bm_sv=C3F2798D0A5C804926CB3F985DD50C6A~YAAQ1C/JF9Ily+eGAQAAKHdeBBO/BE7UQdfO/z6dRrnUB5S2dqzqFURCJUJnoYKJWwPDqNhaxtnmAx5yVK2oFnwqkLoQ7aZa9/G5GdpdS/DfxVERNET25cPtBR3RnBRZU9dEDOC7Bsa+iL3fipUjZ5Jg3KhCZqOjnFNaoNjX7+4jPoroDfB6qo6zUtVarzE2TOUVouFCouwcsWuutFHdwaRsFtk9FZ0UkSI0RvQ6L4BNoYgkQsR7DIgb6pHmYMvEgjQ=~1; RT="z=1&dm=nseindia.com&si=c4a6628f-7f71-413f-97a1-4717ed93fa92&ss=lfiaoihp&sl=1&tt=8j&bcn=//684d0d4a.akstat.io/&ld=1bq&nu=1pwpgq4y&cl=fz0"',
    "content-type": "application/x-www-form-urlencoded; charset=UTF-8"
}


def downloadfile(url):
    r = requests.get(url)
    filename = 'temp_download_data.csv'
    if (r.status_code == 200):
        open(filename, 'wb').write(r.content)
        data = pd.read_csv(filename, skiprows=[0])
        # print(data)
        # print(len(data))
        return data
    else:
        return None


def downloaddata(url, headers=None):
    url = url
    if headers == None:
        r = requests.get(url)
    else:
        r = requests.get(url, headers=headers)
    if (r.status_code == 200):
        json_data = json.loads(r.content)
        # print(r.content)
        return json_data
    else:
        return None
# %%


def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)


base_csv_url = "https://www1.nseindia.com/content/nsccl/fao_participant_oi_"
start_date = date(2023, 3, 5)
end_date = date(2023, 4, 3)
final_df = pd.DataFrame()
print("Started Download")
for single_date in daterange(start_date, end_date):
    dt = single_date.strftime("%Y-%m-%d")
    date_condense = single_date.strftime("%d%m%Y")
    url = base_csv_url+date_condense+".csv"
    data = downloadfile(url)
    if data is not None:
        data.insert(0, 'Date', dt)
        final_df = final_df.append(data, ignore_index=True)

final_file_name = 'fo_oi_positions.csv'
final_df.to_csv(final_file_name)
# url = """https://www1.nseindia.com/ArchieveSearch?h_filetype=foparticipantoi&date="""+str(single_date)+"&section=FO"
# print(url)


# %%
distinct_dates = [*set(list(final_df['Date']))]
data = yf.download('^NSEI', start=start_date.strftime(
    "%Y-%m-%d"), end=end_date.strftime("%Y-%m-%d"))
nifty = data[:]
# %%
# nifty = data[:-3]
# data creater
dates_sorted = []
sample_inputs = []
for i in range(0, len(nifty)):
    u = nifty.index[i].strftime('%Y-%m-%d')
    dates_sorted += [u]
    if u not in distinct_dates:
        print('data mismatch')
        raise IndexError


for i in range(0, len(dates_sorted)-1):
    # checks
    check1 = np.reshape(
        np.array(final_df[final_df['Date'] == distinct_dates[i]])[:, 1:2], (5,))
    to_check = ['Client', 'DII', 'FII', 'Pro', 'TOTAL']

    for j in range(0, len(check1)):
        if check1[j] != to_check[j]:
            print('difference in data')
    sample_array = np.array(final_df[final_df['Date'] == distinct_dates[i]])[
        :-1, 2:]/np.array(final_df[final_df['Date'] == distinct_dates[i]])[-1, 2:]
    # final_df[final_df['Date']==distinct_dates[i]]
    sample_inputs += [list(np.reshape(sample_array, (56,)))]
sample_outputs = (np.array(nifty['Close'])[
                  1:]-np.array(nifty['Close'])[:-1])/np.array(nifty['Close'])[1:]
# %%
# ml configurations


def pso(func, lb, ub, ieqcons=[], f_ieqcons=None, args=(), kwargs={},
        swarmsize=100, omega=0.5, phip=0.5, phig=0.5, maxiter=100,
        minstep=1e-8, minfunc=1e-8, debug=False):
    assert len(lb) == len(
        ub), 'Lower- and upper-bounds must be the same length'
    assert hasattr(func, '__call__'), 'Invalid function handle'
    lb = np.array(lb)
    ub = np.array(ub)
    assert np.all(
        ub > lb), 'All upper-bound values must be greater than lower-bound values'
    vhigh = np.abs(ub - lb)
    vlow = -vhigh
    # Check for constraint function(s) #########################################
    def obj(x): return func(x, *args, **kwargs)
    if f_ieqcons is None:
        if not len(ieqcons):
            if debug:
                print('No constraints given.')

            def cons(x): return np.array([0])
        else:
            if debug:
                print('Converting ieqcons to a single constraint function')

            def cons(x): return np.array(
                [y(x, *args, **kwargs) for y in ieqcons])
    else:
        if debug:
            print('Single constraint function given in f_ieqcons')

        def cons(x): return np.array(f_ieqcons(x, *args, **kwargs))

    def is_feasible(x):
        check = np.all(cons(x) >= 0)
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
        if i == 0:
            g = p[0, :].copy()
        # If the current particle's position is better than the swarm's,
        # update the best swarm position
        if fp[i] < fg and is_feasible(p[i, :]):
            fg = fp[i]
            g = p[i, :].copy()
        # Initialize the particle's velocity
        v[i, :] = vlow + np.random.rand(D)*(vhigh - vlow)
    # Iterate until termination criterion met ##################################
    it = 1
    fg_flow = []
    g_flow = []
    while it <= maxiter:
        rp = np.random.uniform(size=(S, D))
        rg = np.random.uniform(size=(S, D))
        for i in range(S):
            # Update the particle's velocity
            v[i, :] = omega*v[i, :] + phip*rp[i, :]*(p[i, :] - x[i, :]) + \
                phig*rg[i, :]*(g - x[i, :])
            # Update the particle's position, correcting lower and upper bound
            # violations, then update the objective function value
            x[i, :] = x[i, :] + v[i, :]
            mark1 = x[i, :] < lb
            mark2 = x[i, :] > ub
            x[i, mark1] = lb[mark1]
            x[i, mark2] = ub[mark2]
            fx = obj(x[i, :])
            # Compare particle's best position (if constraints are satisfied)
            if fx < fp[i] and is_feasible(x[i, :]):
                p[i, :] = x[i, :].copy()
                fp[i] = fx
                # Compare swarm's best position to current particle's position
                # (Can only get here if constraints are satisfied)
                if fx < fg:
                    if debug:
                        print('New best for swarm at iteration {:}: {:} {:}'.format(
                            it, x[i, :], fx))
                    tmp = x[i, :].copy()
                    stepsize = np.sqrt(np.sum((g-tmp)**2))
                    if np.abs(fg - fx) <= minfunc:
                        print(
                            'Stopping search: Swarm best objective change less than {:}'.format(minfunc))
                        return tmp, fx
                    elif stepsize <= minstep:
                        print(
                            'Stopping search: Swarm best position change less than {:}'.format(minstep))
                        return tmp, fx
                    else:
                        g = tmp.copy()
                        fg = fx
        fg_flow += [fg]
        g_flow += [g]
        if debug:
            print('Best after iteration {:}: {:} {:}'.format(it, g, fg))
        it += 1
    print(
        'Stopping search: maximum iterations reached --> {:}'.format(maxiter))
    if not is_feasible(g):
        print("However, the optimization couldn't find a feasible design. Sorry")
    return g_flow, fg_flow


def pnl(sample_input, x, sample_output):
    def node_out(input_, weights_bias):
        return np.tanh(np.dot(input_, weights_bias[:-1]+weights_bias[-1]))
    input_ = list(sample_input)
    x_ = np.reshape(x, (225, len(input_)+1))
    index = 0
    for j in range(0, 4):
        A = []
        for i in range(0, 56):
            A += [node_out(input_, x_[index])]
            index += 1
        input_ = A
    ultimatum = node_out(input_, x_[index])
    final_indicator = np.array(ultimatum > 0)+np.array(ultimatum < 0)*-1


# %%
