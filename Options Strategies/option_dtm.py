#import banknifty future data for 1 day (1min interval)
#import banknifty greeks for all strikeprices
#manual check on banknifty greeks for different strikeprices mainly gamma
# Black Scholes formula implimentation. ref:  youtube series: khan academy black scholes formula




"""
let ' f ' be black scholes function
let c be call premium.
c=f(stock,strike,volatility, varience, riskfree rate, term, div yeild)
so, we find volatility from the above eqn
volatility=g(stock,strike, c,varience,riskfreerate, term, div yeild)

at 9:15AM we find volatility at all the strikeprices. 
let the volatility is found to be 0.25
we take this as 100 % and we keep finding the volatility on every minute basis.
eg: let the time be 9:20AM and we found the volatility be 0.50
      we take 0.25 as the reference and we take 0.5 as 200 percent.
      if the volatility be 200 percent as the highest volatility for the day. we consider 200 percent as our max volatility for that perticular day.
we will do the same for all the strike prices and we take those 2 strike prices at which stragle strategy could be formed when we run the strangle code.
by taking those two strike prices. we see combined volatility and we start strangle when the volatility meets our requirements or when it hits max volatility for that perticular day.

As strangle is not a good idea to be deployed after 12 o clock. So, when the volatility meets our condition before 12 o clock, we deploy our strat. Else we stop the program and look for other possible strategies
 

"""

