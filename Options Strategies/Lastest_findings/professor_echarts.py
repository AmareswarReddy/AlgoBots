import panel as pn
import numpy as np
import json 
pn.extension('echarts')

capture = []
lastrate = []
x_axis_array = []


with open('professor_variables.json', 'r') as  json_file:
    j_data = json.load(json_file)
    lastrate = j_data['lastrate'][-1500:]
    capture = j_data['capture'][-1500:]
for i in range(0,len(capture)):
    x_axis_array.append(i)

min_banknifty = min(lastrate)
max_banknifty = max(lastrate)


def refresh_chart():
    with open('professor_variables.json', 'r') as  json_file:
        j_data = json.load(json_file)
        lastrate = j_data['lastrate'][-1500:]
        capture = j_data['capture'][-1500:]
    x_axis_array = []
    for i in range(0,len(capture)):
        x_axis_array.append(i)


    echart['series'] = [dict(echart['series'][0], data= lastrate), dict(echart['series'][1], data= capture)]
    echart['xAxis'] = dict(echart['xAxis'], data = x_axis_array)
    echart['yAxis'] = [dict(echart['yAxis'][0], min = min(lastrate),max = max(lastrate))]
    echart_pane.param.trigger('object')

    

echart = {
    'title': {
        #'text': 'ECharts entry example'
    },
    'tooltip': {},
    'legend': {
        'data':['BANKNIFTY', 'capture']
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
      'position': 'left',
       'splitLine': {
         'show': False
      }
    },
    {
      'type': 'value',
      'name': 'capture',
      'position': 'right',
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
        'smooth': False
    }
    ,
    {
        'name': 'capture',
        'type': 'line',
        'yAxisIndex': 1,
        'data': capture,
        'smooth': False
    }
    
    ],
}

echart_pane = pn.pane.ECharts(echart, height=400, width=670)
banknifty_col = pn.Column(echart_pane)
cb = pn.state.add_periodic_callback(refresh_chart, 1000)

display_row = pn.Row(banknifty_col, sizing_mode='stretch_width')

pn.template.FastListTemplate(
    site="Echarts", 
    title="Assy",
    main=[
       display_row
    ]
).servable()