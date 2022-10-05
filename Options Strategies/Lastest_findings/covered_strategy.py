from math import ceil, floor
from  orders_at_hands_class  import OrdersAtHands
from datetime import date
import time
import json

strikes = {"strike":0, "ATM":{"CE":{"original_strike":0, "adjusted_strike":0}, "PE":{"original_strike":0, "adjusted_strike":0}}, 
                       "OTM":{"CE":{"original_strike":0, "adjusted_strike":0}, "PE":{"original_strike":0, "adjusted_strike":0}}}

client_name = "amar"
lots = 5
std_deviation = 0
expected_points = 600


#Initalizing Orders Class
orderAtHands = OrdersAtHands(client_name)


def initiate_strategy():
    print("Initiating")
    sellATM()
    buyCovered()

def getGapToday():
    day = date.today().weekday()
    if day in [4,0,1]:
        return 400
    elif day == 2:
        return 300
    else:
        return 200

def getRosettaToday():
    day = date.today().weekday()
    if day  == 4:
        return 225, -225
    elif day == 0:
        return 200, -200
    elif day == 1:
        return 175, -175
    elif day == 2:
        return 150, -150
    else:
        return 100, -100

def sellATM():
    print("Selling ATM")
    CE_Strike =  orderAtHands.order_button(0, 'CE_S', lots)
    PE_Strike =  orderAtHands.order_button(0, 'PE_S', lots)
    strikes["ATM"]['CE']['original_strike'] = CE_Strike
    strikes["ATM"]['PE']['original_strike'] = PE_Strike
    # Can be either of CE_exclusive 

def buyCovered():
    print("Buying Protection")
    CE_Cover_Strike = strikes["ATM"]['CE']['original_strike'] + expected_points
    PE_Cover_Strike = strikes["ATM"]['PE']['original_strike'] - expected_points
    orderAtHands.order_button(CE_Cover_Strike, 'CE_B', lots)
    orderAtHands.order_button(PE_Cover_Strike, 'PE_B', lots)

def get_rounded_strike(strike, op_type):
    if op_type == 'floor':
        rounded_strike = ((floor(strike/100))*100)
        print(rounded_strike)
    elif op_type == 'ceil':
        rounded_strike = ((ceil(strike/100))*100)

def callAdjust(current_strike):
    current_strike = current_strike
    #Moving Ahead Adjustment
    if current_strike > strikes["ATM"]['CE']['original_strike'] + getGapToday()+100:
        if current_strike > strikes["ATM"]['CE']['adjusted_strike'] + getGapToday()+100 or strikes["ATM"]['CE']['adjusted_strike'] == 0:
            #Close Existing Postion
            if strikes["ATM"]['CE']['adjusted_strike'] == 0:
                orderAtHands.order_button(strikes["ATM"]['CE']['original_strike'], 'CE_B', lots)
            else:
                orderAtHands.order_button(strikes["ATM"]['CE']['adjusted_strike'], 'CE_B', lots)
            adjusted_strike = current_strike - getGapToday()
            adjusted_strike = get_rounded_strike(adjusted_strike, 'floor')
            #Open New position
            orderAtHands.order_button(adjusted_strike, 'CE_S', lots)
            strikes["ATM"]['CE']['adjusted_strike'] = adjusted_strike
    
    #Readjusting backwards
    if current_strike > strikes["ATM"]['CE']['original_strike'] + getGapToday()-100:
        if current_strike < strikes["ATM"]['CE']['adjusted_strike'] + getGapToday()-100:
            print("backtracking")
            #Close Existing Position
            orderAtHands.order_button(strikes["ATM"]['CE']['adjusted_strike'], 'CE_B', lots)
            #Open New Position
            adjusted_strike = current_strike - getGapToday()
            adjusted_strike = get_rounded_strike(adjusted_strike, 'ceil')
            orderAtHands.order_button(adjusted_strike, 'CE_S', lots)
            strikes["ATM"]['CE']['adjusted_strike'] = adjusted_strike

def putAdjust(current_strike):
    current_strike = current_strike
    #Moving Ahead Adjustment
    if current_strike < strikes["ATM"]['PE']['original_strike'] - getGapToday()-100:
        if current_strike < strikes["ATM"]['PE']['adjusted_strike'] - getGapToday()-100 or strikes["ATM"]['PE']['adjusted_strike'] == 0:
            #Close Existing Postion
            if strikes["ATM"]['PE']['adjusted_strike'] == 0:
                orderAtHands.order_button(strikes["ATM"]['PE']['original_strike'], 'PE_B', lots)
            else:
                orderAtHands.order_button(strikes["ATM"]['PE']['adjusted_strike'], 'PE_B', lots)
            adjusted_strike = current_strike + getGapToday()
            adjusted_strike = get_rounded_strike(adjusted_strike, 'ceil')
            #Open New position
            orderAtHands.order_button(adjusted_strike, 'PE_S', lots)
            strikes["ATM"]['PE']['adjusted_strike'] = adjusted_strike
    
    #Readjusting backwards
    if current_strike < strikes["ATM"]['PE']['original_strike'] - getGapToday()+100:
        if current_strike > strikes["ATM"]['PE']['adjusted_strike'] - getGapToday()+100:
            print("backtracking")
            #Close Existing Position
            orderAtHands.order_button(strikes["ATM"]['PE']['adjusted_strike'], 'PE_B', lots)
            #Open New Position
            adjusted_strike = current_strike + getGapToday()
            adjusted_strike = get_rounded_strike(adjusted_strike, 'floor')
            orderAtHands.order_button(adjusted_strike, 'PE_S', lots)
            strikes["ATM"]['PE']['adjusted_strike'] = adjusted_strike

def adjustATMSell():
    print("Adjusting ATM")
    current_strike = orderAtHands.getCurrentStrike()
    callAdjust(current_strike)
    putAdjust(current_strike)
    #Track the positions in case of program restart
    with open('positions_tracker.json', 'w') as  json_file:
        json.dump(strikes, json_file)


#Used in case of restart. 
run_type =input('Is the Execution Restart? Yes, Y or No, N')
if run_type in ['YES','Yes','Y']:
    with open('positions_tracker.json', 'r') as  json_file:
        j_data = json.load(json_file)
        strikes = j_data
elif run_type in ['NO', 'No', 'N']:
    expected_points = int(input('Enter Expected points'))
    initiate_strategy()

while (True):
    adjustATMSell()
    time.sleep(2)



