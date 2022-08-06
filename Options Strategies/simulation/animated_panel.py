import panel as pn
import numpy as np
import json 
pn.extension('echarts')

k = []
lastrate = []
x_axis_array = []
with open('animation.json', 'r') as  json_file:
    j_data = json.load(json_file)
    lastrate = j_data['lastrate']
    martha = j_data['martha']
    k = j_data['k']
    niftybank=j_data['nifty_bank']
    corr2=j_data['corr2']
for i in range(0,len(k)):
    x_axis_array.append(i)

min_banknifty = min(lastrate)
max_banknifty = max(lastrate)


def refresh_chart():
    print("In Refresh Chart")
    with open('animation.json', 'r') as  json_file:
        print("Hello from inside json read")
        j_data = json.load(json_file)
        lastrate = j_data['lastrate']
        k = j_data['k']
        martha = j_data['martha']
        niftybank=j_data['nifty_bank']
        corr2=j_data['corr2']
        print(len(lastrate))
        print(len(k))
        x_axis_array = []
        for i in range(0,len(k)):
            x_axis_array.append(i)
        
    echart['series'] = [dict(echart['series'][0], data= lastrate), dict(echart['series'][1], data= k), dict(echart['series'][2], data= martha)]
    echart['xAxis'] = dict(echart['xAxis'], data = x_axis_array)
    echart['yAxis'] = [dict(echart['yAxis'][0], min = min(lastrate),max = max(lastrate))]
    echart_pane.param.trigger('object')

    echart2['series'] = [dict(echart2['series'][0], data= niftybank),dict(echart2['series'][1], data= corr2)]
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
        'data':['BANKNIFTY', 'K', 'martha']
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
      'name': 'martha',
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
        'name': 'martha',
        'type': 'line',
        'yAxisIndex': 2,
        'data': martha,
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
        'data':['nifty_bank','corr2']
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
    },
    {
      'type': 'value',
      'name': 'corr2',
      'position': 'right',
       'splitLine': {
         'show': False
      }
    },
  ],
    'series': [{
        'name': 'nifty_bank',
        'type': 'line',
        'yAxisIndex': 0,
        'data': niftybank,
        'smooth': True
    },
    {
    'name': 'K',
    'type': 'line',
    'yAxisIndex': 1,
    'data': k,
    'smooth': True
    }
    ]
}



echart_pane = pn.pane.ECharts(echart, height=400, width=1200)
echart_pane
echart_pane2 = pn.pane.ECharts(echart2, height=400, width=1200)

button = pn.widgets.Button(name='Click me', button_type='primary')
def cb_button(event):
    print("Hello")
    #refresh_chart()
button.on_click(cb_button)
cb = pn.state.add_periodic_callback(refresh_chart, 500)

pn.template.FastListTemplate(
    site="Echarts", 
    title="Assy",
    main=[
       echart_pane, echart_pane2
    ]
).servable()



