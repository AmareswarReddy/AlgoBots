from bokeh.plotting import figure
import panel as pn
pn.extension()
from orders_at_hands_class import OrdersAtHands


def b(event):
    print(event)
    #text.value = format(event.what)
    print(event.obj.name)
    #text.value = 'Clicked {0} times'.format(button.clicks)

# p1 = figure(height=250, sizing_mode='stretch_width', margin=5)
# p2 = figure(height=250, sizing_mode='stretch_width', margin=5)

# p1.line([1, 2, 3], [1, 2, 3])
# p2.circle([1, 2, 3], [1, 2, 3])

# text = pn.widgets.TextInput(value='Ready')
root_card =  pn.Card(title="Positions by Client", sizing_mode='stretch_width')

row = pn.Row(background='WhiteSmoke')
root_card.append(row)

import json
f = open ('credentials2.json', "r")
i = 1
creds = json.loads(f.read())
clients = []



def setPositionsInLayout(position):
    rows = ''
    for p in position:
        #print(p)
        scrip_name = p['ScripName']
        qnt = p['NetQty']
        sell_avg = p['SellAvgRate']
        row = """
                 <tr>
                    <td>{scrip_name}</td>
                    <td style="text-align: end; font-weight: bold;">{qnt}</td> 
                    <td>{sell_avg}</td>
                </tr>
        """.format(scrip_name = scrip_name, qnt = qnt, sell_avg = sell_avg)

        rows = rows+'\n'+row
    str_table = """
                 <table>
                <tr>
                    <th>ScripName</th>
                    <th>Quantity</th> 
                    <th>Sell Avg</th>
                </tr>
                {rows}
                </table>

                <h1>{netpl}</h1>

    """.format(rows = rows)
    html_pane = pn.pane.HTML(("""
                {str_table}
                """).format(str_table = str_table), style={'background-color': '#F6F6F6', 'padding': '10px'})
    return html_pane

client_sessions = []

def update_ui():
    print("Updating UI")
    i =0
    for row in root_card:
        for inner_card in row:
            client = client_sessions[i]
            #Call Html Pane and replace with existing Pane
            positions = client.getLivePositions2()
            html_pane = setPositionsInLayout(positions)
            inner_card[0] = html_pane
            i = i+1
cb = pn.state.add_periodic_callback(update_ui, 30000) 

def on_click_exit(event):
    print(event)

for cred in creds:
    client = OrdersAtHands(cred)
    client_sessions.append(client)
    #Elements specific to card
    wtemp = pn.widgets.Button(name=str(cred), button_type='primary',  margin=(5, 10, 10, 10))
    wtemp.on_click(on_click_exit)
    positions = client.getLivePositions()
    html_pane = setPositionsInLayout(positions)
    card_temp = pn.Card(html_pane,wtemp, title=str(cred), sizing_mode='stretch_width')
    #end
    row.append(card_temp)

    if i%4 == 0:
        row = pn.Row(background='WhiteSmoke')
        root_card.append(row)
    i = i+ 1
print(root_card)
root_card.show()