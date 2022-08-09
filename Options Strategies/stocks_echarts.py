import panel as pn
import numpy as np
import json 
pn.extension('echarts')

gauge_data = {}
gauge_pane = {}
root_col = pn.Column(background='WhiteSmoke')
row = pn.Row(background='WhiteSmoke')
root_col.append(row)
i = 0


with open('stocks_manual.json', 'r') as  json_file:
    j_data = json.load(json_file)
    for stock in j_data:
        #print(stock)
        gauge_data[stock] = {
            'tooltip': {
            },
            'series': [
                {
                    'startAngle': 180,
                    'endAngle': 0,
                    'min':-100,
                    'max':100,
                    'name': stock,
                    'type': 'gauge',
                    'detail': {
                        'formatter': '{value}%'
                    },
                    'data': [{'value': int(j_data[stock]*100), 'name': stock}]
                }
            ]
        }
        gauge_pane[stock] = pn.pane.ECharts(gauge_data[stock], width=300, height=300)
        row.append(gauge_pane[stock])
        i = i+1
        if i%4 == 0:
            row = pn.Row(background='WhiteSmoke')
            root_col.append(row)


def refresh_chart():
    print("in refresh chart")
    with open('stocks_manual.json', 'r') as  json_file:
        j_data = json.load(json_file)
        print(j_data)
        for stock in j_data:
            gauge_data[stock]['series'][0]['data'][0]['value'] =   int(j_data[stock]*100)
            #print(gauge_data[stock]['series'][0]['data'][0]['value'])
            #gauge_pane[stock].param.trigger('object')
        for stock in j_data:
            print(stock)
            gauge_pane[stock].properties.data.change.emit()
            #gauge_pane[stock].param.trigger('object')

#cb = pn.state.add_periodic_callback(refresh_chart, 15000)

pn.template.FastListTemplate(
    site="Echarts", 
    title="Assy",
    main=[
       root_col
    ]
).servable()