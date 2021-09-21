import numpy as np
import pandas as pd
from time import sleep, strftime
from py5paisa import FivePaisaClient
from py5paisa.strategy import *
from datetime import datetime 
import json
now=datetime.now()

cred={
    "APP_NAME":"5P59470899",
    "APP_SOURCE":"6176",
    "USER_ID":"1v73mtvQk3L",
    "PASSWORD":"8DASLLALpZH",
    "USER_KEY":"nNaWVqHIXsgi6FEPnjBknpPPjK1LOHQL",
    "ENCRYPTION_KEY":"HSE2AS6SIEH0UgwfpmwiymkdiRId7eZU"
}
Client = FivePaisaClient(email="p.amareswar20@dmsiitd.org", passwd="Amarreddy@123456", dob="19930714", cred=cred)
Client.login()

#Add all the instruments tokens and corresponding symbols to thi list
strategy2Tickers = {}
ticker_symbol_token= {3045: "SBIN",2263:"BANDHANBNK"}

correlated_pairs = [{"tickers":[3045 ,2263]}]

for element in correlated_pairs:
     #Place to store variables
    element["doesPositionExists"] = "no";
    element["movingStopLoss"] = 0;
    element["positiontype"] = 'none';
    element["tradePrice"] = 0
    element['tradedStock'] = 0
    #Creating an empty dict to hold data for different tickers
    for tickerTemp in element["tickers"]:
        strategy2Tickers[tickerTemp] = {'tick_data':[], 'high':0, 'low':0, 'last_price':0}
        
def placeOrder(transact_type, price, tradingsymbol, order_type="MARKET"):
    print("Transact Type is "+ transact_type+"@ "+ str(price)+ "for Stock "+ tradingsymbol)
    
req_list=[
            { "Exch":"N","ExchType":"C","ScripCode":3045}, 
        { "Exch":"N","ExchType":"C","ScripCode":2263}     
            ]

def on_message(ws, message):
        for element in json.loads(message):
            #print(element)
            
            strategy2Tickers[int(element['Token'])]['tick_data'].append(element['LastRate'])
            #print(strategy2Tickers)
            if(len(strategy2Tickers[int(element['Token'])]['tick_data']) >20):
                strategy2Tickers[int(element['Token'])]['tick_data'].pop(0)

            strategy2Tickers[int(element['Token'])]['last_price'] = element['LastRate']
            strategy2Tickers[int(element['Token'])]['high'] = max(strategy2Tickers[int(element['Token'])]['tick_data'])
            strategy2Tickers[int(element['Token'])]['low'] = min(strategy2Tickers[int(element['Token'])]['tick_data'])
            #print(strategy2Tickers) 
            for pair in correlated_pairs:
            #SBI Stock low & high percentage difference with respect to last traded price 
                symbol1 = pair["tickers"][0] #returns instrument token
                symbol2 = pair["tickers"][1]
                low_percent_diff_sbi = abs(((strategy2Tickers[symbol1]['last_price'] - strategy2Tickers[symbol1]['low'])/ strategy2Tickers[symbol1]['low'])*100)
                high_percent_diff_sbi = abs(((strategy2Tickers[symbol1]['last_price'] - strategy2Tickers[symbol1]['high'])/ strategy2Tickers[symbol1]['high'])*100)
                
                                
                #Canara Bank low & high percentage difference with repect to last trade price
                low_percent_diff_canara = abs(((strategy2Tickers[symbol2]['last_price'] - strategy2Tickers[symbol2]['low'])/ strategy2Tickers[symbol2]['low'])*100)
                high_percent_diff_canara = abs(((strategy2Tickers[symbol2]['last_price'] - strategy2Tickers[symbol2]['high'])/ strategy2Tickers[symbol2]['high'])*100)
                
                doesPositionExists = pair['doesPositionExists']
                movingStopLoss = pair['movingStopLoss']
                positiontype = pair['positiontype']
                tradePrice = pair['tradePrice']
                
                
                 #Update Moving Stop loss. This is to benefit from the profit booking after price moves certain distance in the favourable direction
                if doesPositionExists == 'yes':
                    if movingStopLoss == 0 :
                        if positiontype == 'long':
                            percent_diff_temp = ((strategy2Tickers[pair['tradedStock']]['last_price'] - tradePrice)/tradePrice)*100
                            if percent_diff_temp > 0.3:
                                pair['movingStopLoss'] = strategy2Tickers[pair['tradedStock']]['last_price']
                            
                        
                        elif positiontype == 'short':
                            percent_diff_temp = ((tradePrice-strategy2Tickers[pair['tradedStock']]['last_price'])/tradePrice)*100
                            if percent_diff_temp > 0.3:
                                pair['movingStopLoss'] = strategy2Tickers[pair['tradedStock']]['last_price']

                    #Already moving stop is updated once
                    else :
                        if positiontype == 'long' :
                            percent_diff_temp = ((strategy2Tickers[pair['tradedStock']]['last_price'] - movingStopLoss)/movingStopLoss)*100
                            if percent_diff_temp > 0.2 :
                                pair['movingStopLoss'] = strategy2Tickers[pair['tradedStock']]['last_price']
        
                        elif positiontype == 'short' :
                            percent_diff_temp = ((movingStopLoss-strategy2Tickers[pair['tradedStock']]['last_price'])/movingStopLoss)*100
                            if percent_diff_temp > 0.2 :
                                pair['movingStopLoss'] = strategy2Tickers[pair['tradedStock']]['last_price']
                                
                
                #Profit Booking based on Stop Loss updation
                if doesPositionExists == 'yes':
                    if movingStopLoss != 0 :
                        if positiontype == 'long' :
                            temp_diff = ((movingStopLoss - strategy2Tickers[pair['tradedStock']]['last_price'])/movingStopLoss)*100
                            if temp_diff > 0.15 :
                                print("Sell the stock. Its moving down after hitting an updated stop loss" + ticker_symbol_token[pair['tradedStock']])
                                placeOrder('SELL', strategy2Tickers[pair['tradedStock']]['last_price'], ticker_symbol_token[pair['tradedStock']])
                                pair['tradePrice'] = 0
                                pair['doesPositionExists'] = 'no'
                                pair['positiontype'] = 'none'
                                pair['movingStopLoss'] = 0
                        elif positiontype == 'short':
                            temp_diff = ((strategy2Tickers[pair['tradedStock']]['last_price'] - movingStopLoss)/movingStopLoss)*100
                            if temp_diff > 0.15 :
                                print("Buy the stock. Its moving up after hitting an updated stop loss" + ticker_symbol_token[pair['tradedStock']])
                                placeOrder('BUY', strategy2Tickers[pair['tradedStock']]['last_price'], ticker_symbol_token[pair['tradedStock']])
                                pair['tradePrice'] = 0
                                pair['doesPositionExists'] = 'no'
                                pair['positiontype'] = 'none'
                                pair['movingStopLoss'] = 0
                can_initiate_trade = False
                trade_action = 'none'
                #Trade Symbol 2
                if low_percent_diff_sbi > 0.1 or high_percent_diff_sbi > 0.1:
                    if low_percent_diff_canara < 0.1 or high_percent_diff_canara < 0.1 : 
                        can_initiate_trade = True
                        if high_percent_diff_sbi == 0:
                            trade_action = 'Buy'
                        elif low_percent_diff_sbi == 0:
                            trade_action = "Sell"
                        if pair['doesPositionExists'] == 'no':
                            pair['tradedStock'] = symbol2

                if low_percent_diff_canara > 0.1 or high_percent_diff_canara > 0.1:
                    if low_percent_diff_sbi < 0.1 or high_percent_diff_sbi < 0.1:
                        can_initiate_trade = True
                        if high_percent_diff_canara == 0:
                            trade_action = 'Buy'
                        elif low_percent_diff_canara == 0:
                            trade_action = "Sell"   
                        if pair['doesPositionExists'] == 'no':
                            pair['tradedStock'] = symbol1
                        


                if can_initiate_trade:
                        print("Percentage difference is > 0.2" + ticker_symbol_token[pair['tradedStock']])
                    # Initiate trade action only if Canara Bank hasn't moved yet
                    #Check if Buy or Sell position has been taken
                        if doesPositionExists == 'no':
                            #Check whether the signal is to Buy or Sell
                            if trade_action == 'Buy' :
                                #Buy;  SBI is moving up. Since the latest price is the highest and percent difference with low > 0.2
                                print("Buy:"+ticker_symbol_token[pair['tradedStock']]+ " @" + str(strategy2Tickers[pair['tradedStock']]['last_price']))
                                placeOrder('BUY', strategy2Tickers[pair['tradedStock']]['last_price'], ticker_symbol_token[pair['tradedStock']])
                                pair['tradePrice'] = strategy2Tickers[pair['tradedStock']]['last_price']
                                pair['doesPositionExists'] = 'yes'
                                pair['positiontype'] = 'long'
                                pair['movingStopLoss'] = 0
                                #Used after entering position
                                pair.position_token = pair['tradedStock'] 
                            
                            elif trade_action == 'Sell':
                                #Sell ; SBI is moving down. Since the latest price is the lowest and percent difference with high > 0.2
                                print("Sell:"+ ticker_symbol_token[pair['tradedStock']] + " @" + str(strategy2Tickers[pair['tradedStock']]['last_price']))
                                placeOrder('SELL', strategy2Tickers[pair['tradedStock']]['last_price'], ticker_symbol_token[pair['tradedStock']])
                                pair['tradePrice'] = strategy2Tickers[pair['tradedStock']]['last_price']
                                pair['doesPositionExists'] = 'yes'
                                pair['positiontype'] = 'short'
                                pair['movingStopLoss'] = 0
                                #Used after entering position
                                pair.position_token = pair['tradedStock'] 
                            
                        

                        #Re ckeck for the conditon in the above loop
                        elif doesPositionExists == 'yes':
                            #Since a position exists, do the reverse of above
                            if (positiontype == 'short' and ((high_percent_diff_sbi == 0 and pair['tradedStock'] == pair.position_token) or (high_percent_diff_canara == 0 and pair['tradedStock'] == pair.position_token))) : 
                                #Buy;  SBI is moving up. 
                                print("Buy the Canara bank Stock from position")
                                placeOrder('BUY', strategy2Tickers[pair['tradedStock']]['last_price'],ticker_symbol_token[pair['tradedStock']], 'LIMIT')
                                pair['tradePrice'] = 0
                                pair['doesPositionExists'] = 'no'
                                pair['positiontype'] = 'none'
                                pair['movingStopLoss'] = 0
                                
                            elif (positiontype == 'long'  and ((low_percent_diff_sbi == 0 and pair['tradedStock'] == pair.position_token) or (low_percent_diff_canara == 0 and pair['tradedStock'] == pair.position_token))): 
                                #Sell ; SBI is moving down.
                                print("Sell Canara Bank Stock position")
                                placeOrder('SELL', strategy2Tickers[pair['tradedStock']]['last_price'],ticker_symbol_token[pair['tradedStock']], 'LIMIT')
                                pair['tradePrice'] = 0
                                pair['doesPositionExists'] = 'no'
                                pair['positiontype'] = 'none'
                                pair['movingStopLoss'] = 0
                                
                if(doesPositionExists == 'yes'):
                    # precent_diff_canara_on_position;
                    if(positiontype == 'long'):
                        if(tradePrice != 0):
                            # Want to exit position, i.e. sell if current price is less than trade price by 0.2 %
                            #Here we are subtracting trade price with current price, so taking +ve sign in if loop
                            precent_diff_canara_on_position =  ((tradePrice - strategy2Tickers[pair['tradedStock']]['last_price'])/tradePrice)*100
                            if(precent_diff_canara_on_position > 0.3):
                                print("Sell"+ticker_symbol_token[pair['tradedStock']]+"; Hit Stop Loss")
                                placeOrder('SELL', strategy2Tickers[pair['tradedStock']]['last_price'],ticker_symbol_token[pair['tradedStock']], 'LIMIT')
                                pair['tradePrice'] = 0
                                pair['doesPositionExists'] = 'no'
                                pair['positiontype'] = 'none'
                                pair['movingStopLoss'] = 0
                            
                    elif positiontype == 'short':
                        if(tradePrice != 0):
                            # Want to exit position, i.e. Buy if current price is greater than trade price by 0.2 %
                            precent_diff_canara_on_position =  ((strategy2Tickers[pair['tradedStock']]['last_price'] - tradePrice)/tradePrice)*100
                            if(precent_diff_canara_on_position > 0.3):
                                print("Buy "+ticker_symbol_token[pair['tradedStock']]+"; Hit Stop Loss")
                                placeOrder('BUY', strategy2Tickers[pair['tradedStock']]['last_price'],ticker_symbol_token[pair['tradedStock']], 'LIMIT')
                                pair['tradePrice'] = 0
                                pair['doesPositionExists'] = 'no'
                                pair['positiontype'] = 'none'
                                pair['movingStopLoss'] = 0
    
# END of the fuction        
        

        
dict1=Client.Request_Feed('mf','s',req_list)
Client.Streming_data(dict1, on_message)
