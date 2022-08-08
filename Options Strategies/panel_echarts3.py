import panel as pn
import numpy as np
import json 
pn.extension('echarts')

k = []
lastrate = []
x_axis_array = []

k_nifty = []
lastrate_nifty = []
x_axis_array_nifty = []

with open('variables_data.json', 'r') as  json_file:
    j_data = json.load(json_file)
    
    lastrate = j_data['lastrate'][-150:]
    corr = j_data['corr'][-150:]
    k = j_data['k'][-150:]
    niftybank=j_data['nifty_bank'][-150:]
for i in range(0,len(k)):
    x_axis_array.append(i)

with open('variables_data_nifty.json', 'r') as  json_file:
    j_data_nifty = json.load(json_file)
    lastrate_nifty = j_data_nifty['lastrate']
    corr_nifty = j_data_nifty['corr']
    k_nifty = j_data_nifty['k']
    ind_nifty=j_data_nifty['nifty_bank']
for i in range(0,len(k_nifty)):
    x_axis_array_nifty.append(i)

min_banknifty = min(lastrate)
max_banknifty = max(lastrate)

min_nifty = min(lastrate_nifty)
max_nifty = max(lastrate_nifty)


def refresh_chart():
    print("In Refresh Chart")
    with open('variables_data.json', 'r') as  json_file:
        print("Hello from inside json read")
        j_data = json.load(json_file)
        lastrate = j_data['lastrate'][-150:]
        k = j_data['k'][-150:]
        corr = j_data['corr'][-150:]
        niftybank=j_data['nifty_bank'][-150:]
        print(len(lastrate))
        print(len(k))
        x_axis_array = []
        for i in range(0,len(k)):
            x_axis_array.append(i)
    with open('variables_data_nifty.json', 'r') as  json_file:
        j_data_nifty = json.load(json_file)
        lastrate_nifty = j_data_nifty['lastrate']
        corr_nifty = j_data_nifty['corr']
        k_nifty = j_data_nifty['k']
        ind_nifty=j_data_nifty['nifty_bank']
        x_axis_array_nifty = []
        for i in range(0,len(k_nifty)):
            x_axis_array_nifty.append(i)

    echart['series'] = [dict(echart['series'][0], data= lastrate), dict(echart['series'][1], data= k), dict(echart['series'][2], data= corr)]
    echart['xAxis'] = dict(echart['xAxis'], data = x_axis_array)
    echart['yAxis'] = [dict(echart['yAxis'][0], min = min(lastrate),max = max(lastrate))]
    echart_pane.param.trigger('object')

    echart2['series'] = [dict(echart2['series'][0], data= niftybank)]
    echart2['xAxis'] = dict(echart2['xAxis'], data = x_axis_array)
    echart_pane2.param.trigger('object')


    echart_nifty['series'] = [dict(echart_nifty['series'][0], data= lastrate_nifty), dict(echart_nifty['series'][1], data= k_nifty), dict(echart_nifty['series'][2], data= corr_nifty)]
    echart_nifty['xAxis'] = dict(echart_nifty['xAxis'], data = x_axis_array_nifty)
    echart_nifty['yAxis'] = [dict(echart_nifty['yAxis'][0], min = min(lastrate_nifty),max = max(lastrate_nifty))]
    echart_pane_nifty.param.trigger('object')

    echart_nifty_2['series'] = [dict(echart_nifty_2['series'][0], data= ind_nifty)]
    echart_nifty_2['xAxis'] = dict(echart_nifty_2['xAxis'], data = x_axis_array_nifty)
    echart_pane_nifty_2.param.trigger('object')

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


echart_nifty = {
    'title': {
        #'text': 'ECharts entry example'
    },
    'tooltip': {},
    'legend': {
        'data':['NIFTY', 'K', 'corr']
    },
    'xAxis': {
        'data': x_axis_array_nifty,
         'splitLine': {
         'show': False
      }
    },

    'yAxis': [
    {
      'type': 'value',
      'name': 'NIFTY',
      'min': min_nifty,
      'max': max_nifty,
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
        'name': 'NIFTY',
        'type': 'line',
        'yAxisIndex': 0,
        'data': lastrate_nifty,
        'smooth': True
    }
    ,
    {
        'name': 'K',
        'type': 'line',
        'yAxisIndex': 1,
        'data': k_nifty,
        'smooth': True
    },

    {
        'name': 'corr',
        'type': 'line',
        'yAxisIndex': 2,
        'data': corr_nifty,
        'smooth': True
    }
    
    ],
}

echart_nifty_2= {
    'title': {
        #'text': 'ECharts entry example'
    },
    'tooltip': {},
    'legend': {
        'data':['ind_nifty']
    },
    'xAxis': {
        'data': x_axis_array_nifty,
         'splitLine': {
         'show': False
      }
    },
    'yAxis': [
    {
      'type': 'value',
      'name': 'ind_nifty',
      'position': 'left',
       'splitLine': {
         'show': False
      }
    }
  ],
    'series': [{
        'name': 'ind_nifty',
        'type': 'line',
        'yAxisIndex': 0,
        'data': ind_nifty,
        'smooth': True
    }
    ]
}



echart_pane = pn.pane.ECharts(echart, height=400, width=670)
echart_pane2 = pn.pane.ECharts(echart2, height=400, width=670)


echart_pane_nifty = pn.pane.ECharts(echart_nifty, height=400, width=670)
echart_pane_nifty_2 = pn.pane.ECharts(echart_nifty_2, height=400, width=670)

# button = pn.widgets.Button(name='Click me', button_type='primary')
# def cb_button(event):
#     print("Hello")
#     #refresh_chart()
# button.on_click(cb_button)
cb = pn.state.add_periodic_callback(refresh_chart, 1000)


banknifty_col = pn.Column(echart_pane, echart_pane2 )
nifty_col  = pn.Column(echart_pane_nifty,echart_pane_nifty_2 )

display_row = pn.Row(banknifty_col, nifty_col, sizing_mode='stretch_width')

pn.template.FastListTemplate(
    site="Echarts", 
    title="Assy",
    main=[
       display_row
    ]
).servable()



