import panel as pn
import numpy as np
import json 
pn.extension('echarts')

k = []
lastrate = []
x_axis_array = []
with open('variables_data.json', 'r') as  json_file:
    j_data = json.load(json_file)
    lastrate = j_data['lastrate']
    corr = j_data['corr']
    k = j_data['k']
    niftybank=j_data['nifty_bank']
for i in range(0,len(k)):
    x_axis_array.append(i)

min_banknifty = min(lastrate)
max_banknifty = max(lastrate)


def refresh_chart():
    print("In Refresh Chart")
    with open('variables_data.json', 'r') as  json_file:
        print("Hello from inside json read")
        j_data = json.load(json_file)
        lastrate = j_data['lastrate']
        k = j_data['k']
        corr = j_data['corr']
        niftybank=j_data['nifty_bank']
        print(len(lastrate))
        print(len(k))
        x_axis_array = []
        for i in range(0,len(k)):
            x_axis_array.append(i)
        
    echart['series'] = [dict(echart['series'][0], data= lastrate), dict(echart['series'][1], data= k), dict(echart['series'][2], data= corr)]
    echart['xAxis'] = dict(echart['xAxis'], data = x_axis_array)
    echart['yAxis'] = [dict(echart['yAxis'][0], min = min(lastrate),max = max(lastrate))]
    echart_pane.param.trigger('object')

    echart2['series'] = [dict(echart2['series'][0], data= niftybank)]
    echart2['xAxis'] = dict(echart2['xAxis'], data = x_axis_array)
    echart_pane2.param.trigger('object')

    # min_banknifty = min(lastrate)
    # max_banknifty = max(lastrate)
    
echart = {
    'title': {
        #'text': 'ECharts entry example'
    },
    'tooltip': {},
    'legend': {
        'data':['BANKNIFTY', 'K', 'corr']
    },
    'xAxis': {
        'data': x_axis_array,
         'splitLine': {
         'show': False
      }
    },

    'yAxis': [
    {
      'type': 'value',
      'name': 'BANKNIFTY',
      'min': min_banknifty,
      'max': max_banknifty,
      'position': 'right',
       'splitLine': {
         'show': False
      }
    },
    {
      'type': 'value',
      'name': 'K',
      'position': 'right',
       'splitLine': {
         'show': False
      }
    },
    {
      'type': 'value',
      'name': 'corr',
      'position': 'left',
       'splitLine': {
         'show': False
      }
    }
  ],

    'series': [{
        'name': 'BANKNIFTY',
        'type': 'line',
        'yAxisIndex': 0,
        'data': lastrate,
        'smooth': True
    }
    ,
    {
        'name': 'K',
        'type': 'line',
        'yAxisIndex': 1,
        'data': k,
        'smooth': True
    },

    {
        'name': 'corr',
        'type': 'line',
        'yAxisIndex': 2,
        'data': corr,
        'smooth': True
    }
    
    ],
}

echart2= {
    'title': {
        #'text': 'ECharts entry example'
    },
    'tooltip': {},
    'legend': {
        'data':['nifty_bank',]
    },
    'xAxis': {
        'data': x_axis_array,
         'splitLine': {
         'show': False
      }
    },
    'yAxis': [
    {
      'type': 'value',
      'name': 'nifty_bank',
      'position': 'left',
       'splitLine': {
         'show': False
      }
    }
  ],
    'series': [{
        'name': 'nifty_bank',
        'type': 'line',
        'yAxisIndex': 0,
        'data': niftybank,
        'smooth': True
    }
    ]
}



echart_pane = pn.pane.ECharts(echart, height=420, width=1200)
echart_pane
echart_pane2 = pn.pane.ECharts(echart2, height=420, width=1200)

button = pn.widgets.Button(name='Click me', button_type='primary')
def cb_button(event):
    print("Hello")
    #refresh_chart()
button.on_click(cb_button)
cb = pn.state.add_periodic_callback(refresh_chart, 2000)

pn.template.FastListTemplate(
    site="Echarts", 
    title="Assy",
    main=[
       echart_pane, echart_pane2
    ]
).servable()


#%%
def client_login(client):
    import json
    f = open ('credentials.json', "r")
    creds = json.loads(f.read())
    client_list={}
    client_list[client]={'strategy':{},'login':{},'lots':{}}
    vinathi_cred = creds[client]["keys"]
    user = creds[client]["user"]
    passw = creds[client]["passw"]
    dob = creds[client]["dob"]
    client_list[client]['strategy']=strategies(user=user, passw=passw, dob=dob,cred=vinathi_cred)
    client_list[client]['login']=FivePaisaClient(email=user, passwd=passw, dob=dob,cred=vinathi_cred)
    client_list[client]['login'].login()
    client_list[client]['lots']=round((client_list[client]['login'].margin()[0]['AvailableMargin']-200000)/180000)
    return client_list[client]
def order_button(exclusive_strike,type,lots):
    if lots>=48:
          lots=48
    prime_client=client_login('vinathi')
    while True:
        try:
            re=[{"Exch":"N","ExchType":"C","Symbol":"BANKNIFTY","Scripcode":"999920005","OptionType":"EQ"}]          
            aa=prime_client['login'].fetch_market_feed(re)
            x=aa['Data'][0]['LastRate']
            break
        except Exception:
            pass
    while True:
        try :
            expiry_timestamps=prime_client['login'].get_expiry("N","BANKNIFTY").copy()
            current_expiry_time_stamp_weekly=int(expiry_timestamps['Expiry'][0]['ExpiryDate'][6:19])
            option_chain=pd.DataFrame(prime_client['login'].get_option_chain("N","BANKNIFTY",current_expiry_time_stamp_weekly)['Options'])
            break
        except Exception :
            pass
    if exclusive_strike==0:
        exclusive_strike=int(np.round(x/100)*100)
    if type=='CE_B':
        c_data=option_chain[option_chain['CPType']=='CE']
        c_scrip=int(c_data[c_data['StrikeRate']==exclusive_strike]['ScripCode'])
        test_order = Order(order_type='B',exchange='N',exchange_segment='D', scrip_code =c_scrip, quantity=25*lots, price=0 ,is_intraday=False,remote_order_id="tag")
        prime_client['login'].place_order(test_order) 
    if type=='PE_B':
        p_data=option_chain[option_chain['CPType']=='PE']
        p_scrip=int(p_data[p_data['StrikeRate']==exclusive_strike]['ScripCode'])
        test_order = Order(order_type='B',exchange='N',exchange_segment='D', scrip_code =p_scrip, quantity=25*lots, price=0 ,is_intraday=False,remote_order_id="tag")
        prime_client['login'].place_order(test_order) 
    if type=='CE_S':
        c_data=option_chain[option_chain['CPType']=='CE']
        c_scrip=int(c_data[c_data['StrikeRate']==exclusive_strike]['ScripCode'])
        test_order = Order(order_type='S',exchange='N',exchange_segment='D', scrip_code =c_scrip, quantity=25*lots, price=0 ,is_intraday=False,remote_order_id="tag")
        prime_client['login'].place_order(test_order) 
    if type=='PE_S':
        p_data=option_chain[option_chain['CPType']=='PE']
        p_scrip=int(p_data[p_data['StrikeRate']==exclusive_strike]['ScripCode'])
        test_order = Order(order_type='S',exchange='N',exchange_segment='D', scrip_code =p_scrip, quantity=25*lots, price=0 ,is_intraday=False,remote_order_id="tag")
        prime_client['login'].place_order(test_order) 
