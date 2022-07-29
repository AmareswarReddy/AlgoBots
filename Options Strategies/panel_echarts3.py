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



echart_pane = pn.pane.ECharts(echart, height=480, width=1200)
echart_pane
echart_pane2 = pn.pane.ECharts(echart2, height=480, width=1200)

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



