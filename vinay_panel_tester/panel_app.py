#%%
from bokeh.plotting import figure
import matplotlib.pyplot as plt
import panel as pn
import subprocess
import json
import os
from sofie import fig
pn.extension()
f = open ('credentials.json', "r")
creds = json.loads(f.read())

# def a(event):
#     state[event.obj.name.split(":")[1]]['lots'] = event.obj.value
#     print(state)

def callback(target, event):
    import json
    print("From Callback 1")
    print(target.value)
    print(event.obj.name)
    temp_json_data = {}
    with open('state.json', 'r') as json_file:
            data = json.load(json_file)
            if data[event.obj.name]['pid'] == -1:
                temp_p = subprocess.Popen(['python', "shakira.py", event.obj.name, str(target.value)])
                print(temp_p.pid)
                data[event.obj.name]['pid'] = temp_p.pid
            else:
                print("Active PID is", data[event.obj.name]['pid'])
                #os.kill(data[event.obj.name]['pid'], -9)
                subprocess.Popen(['taskkill', '/pid', str(data[event.obj.name]['pid']),'/F' ])
                data[event.obj.name]['pid'] = -1
            temp_json_data = data

    with open('state.json', 'w') as outfile:
            json.dump(temp_json_data, outfile)

            
    
def callback2(target, event):
    print("From Callback 2")
    print(target)
    print()
    if target.object == 'Idle':
        target.object = "Running"
    else :
        target.object = 'Idle'


def callback3(target, event):
    print("Termial Process")
    print(target)
    #print(target.running)
    

def btn_on_click(event):
    if event.obj.button_type == "primary":
        event.obj.button_type = "success"
    else:
        event.obj.button_type = "primary"
# def b(event):
#     print("From On Click")
#     #print(event)
#     print(event)
#     #text.value = format(event.what)
#     print(event.obj.name)
#     #text.value = 'Clicked {0} times'.format(button.clicks)

def stream():
    try:
        with open(".json","r") as f:
            data = f.read()
        d = json.loads(data)
        p1 = fig(trades_taken=d)
    except Exception:
        p1=plt.figure(figsize=[3.5,2.5])
        plt.plot([1,100],[0,0])
        plt.title('no_trades_yet') 
    return p1
pn.state.add_periodic_callback(stream,500)
    
text = pn.widgets.TextInput(value='Ready')
root_card =  pn.Card(text, title="Home", sizing_mode='stretch_width')

row = pn.Row(background='WhiteSmoke')
root_card.append(row)
i = 0
int_sliders = []
state = {}
for cred in creds:
    subprocess_terminal = pn.widgets.Terminal(
    "Welcome to the Panel Terminal",
    options={"cursorBlink": True},
    height=250, sizing_mode='stretch_width'
    )

    state[cred] = {"pid":-1, "state":"Idle"}
    name_temp = "Number of Lots:"+cred
    markdown = pn.pane.Markdown("Status :")
    markdown1 = pn.pane.Markdown("Idle")
    label_row = pn.Row(markdown,markdown1, background='WhiteSmoke')
    wtemp = pn.widgets.Button(name=cred, button_type='primary',  margin=(5, 10, 10, 10))
    wtemp.on_click(btn_on_click)
    int_slider = pn.widgets.IntSlider(name=name_temp, start=1, end=10, step=1, value=1)
    #int_slider.param.trigger()
    wtemp.link(int_slider, callbacks={'value': callback})
    wtemp.link(markdown1, callbacks={'value': callback2})
    #wtemp.link(subprocess_terminal,callbacks={'value': callback3})
    #int_slider.param.watch(a, ['value'], onlychanged=False)
    try:
        with open(".json","r") as f:
            data = f.read()
        d = json.loads(data)
        p1 = fig(trades_taken=d)
    except Exception:
        p1=plt.figure(figsize=[3.5,2.5])
        plt.plot([1,100],[0,0])
        plt.title('no_trades_yet')
    card_temp = pn.Card(p1, label_row, int_slider, pn.Spacer(background='WhiteSmoke', height=5), wtemp, title=cred, sizing_mode='stretch_width')
    row.append(card_temp)
    i = i+1
    if i%3 == 0:
        row = pn.Row(background='WhiteSmoke')
        root_card.append(row)

with open('state.json', 'w') as outfile:
    json.dump(state, outfile)

root_card.show()
# %%
