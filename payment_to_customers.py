#%%
def f(money_invested,interest,days):
    temp=money_invested
    for i in range(0,days):
        temp = temp*(1+(interest/100))
    return temp

def g(money_invested,return_percentage):
    a = (return_percentage)/365 
    while True:
        a=a-0.0001
        if f(money_invested,a,365)<=((return_percentage/100)+1)*money_invested:
            break
    return a

def h(money_invested,return_percentage,days_with_us):
    a=g(money_invested,return_percentage)
    return f(money_invested,a,days_with_us)
invested=float(input('enter the money invested in our company : '))
return_percentage=float(input('enter the promissed returns per annum : '))
days_with_us=int(input('enter the days costumers kept the money in our account : '))
#using function h will give us how much money we need to give our customer if they want to withdraw before maturity of the funds
h(money_invested=invested,return_percentage=return_percentage,days_with_us=days_with_us)
