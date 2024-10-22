import panel as pn
import numpy as np
import json 
from martha_charts import marta_init
pn.extension('echarts')

k = []
lastrate = []
x_axis_array = []
try:
    j_data,indicator,b_lastrate,corr,to_deal= marta_init(indicator,b_lastrate,corr,to_deal)
    print('hi')
except Exception:
    j_data,indicator,b_lastrate,corr,to_deal= marta_init()
lastrate = j_data['lastrate']
k = j_data['k']
corr = j_data['corr']
for i in range(0,len(k)):
    x_axis_array.append(i)
print(j_data)
try:
    min_banknifty = min(lastrate)
    max_banknifty = max(lastrate)
except Exception:
    min_banknifty=33000
    max_banknifty=37000

def refresh_chart():
    print("Hello from inside json read")
    lastrate = j_data['lastrate']
    k = j_data['k']
    corr = j_data['corr']
    print(len(lastrate))
    print(len(k))
    x_axis_array = []
    for i in range(0,len(k)):
        x_axis_array.append(i)
        
    echart['series'] = [dict(echart['series'][0], data= lastrate), dict(echart['series'][1], data= k), dict(echart['series'][2], data= corr)]
    echart['xAxis'] = dict(echart['xAxis'], data = x_axis_array)
    echart['yAxis'] = [dict(echart['yAxis'][0], min = min(lastrate),max = max(lastrate))]
    echart_pane.param.trigger('object')

    # min_banknifty = min(lastrate)
    # max_banknifty = max(lastrate)
    
echart = {
    'title': {
        #'text': 'ECharts entry example'
    },
    'tooltip': {},
    'legend': {
        'data':['BANKNIFTY', 'K', 'L']
    },
    'xAxis': {
        'data': x_axis_array
    },

    'yAxis': [
    {
      'type': 'value',
      'name': 'BANKNIFTY',
      'min': min_banknifty,
      'max': max_banknifty,
      'position': 'left',
    },
    {
      'type': 'value',
      'name': 'K',
      'position': 'right',
    },
    {
      'type': 'value',
      'name': 'corr',
      'position': 'right',
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
    }, {
        'name': 'corr',
        'type': 'line',
        'yAxisIndex': 1,
        'data': corr,
        'smooth': True
    }
    ],
}


echart_pane = pn.pane.ECharts(echart, height=480, width=720)
echart_pane

button = pn.widgets.Button(name='Click me', button_type='primary')
def cb_button(event):
    print("Hello")
    #refresh_chart()
button.on_click(cb_button)
cb = pn.state.add_periodic_callback(refresh_chart, 2000)

pn.template.FastListTemplate(
    site="Echarts", 
    title="Assy", 
    theme="dark",
    sidebar=[button], 
    main=[
       echart_pane
    ]
).servable()



