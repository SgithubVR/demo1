import pandas as pd

import PySimpleGUI as sg
import os.path
import numpy as np
import matplotlib as mt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

fig = mt.figure.Figure(figsize=(5, 4), dpi=100)
t = np.arange(0, 3, .01)
fig.add_subplot(111).plot(t, 2 * np.sin(2 * np.pi * t))

mt.use("TkAgg")

def draw_figure(canvas, figure):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side="top", fill="both", expand=1)
    return figure_canvas_agg

df_lucky = ["IBM", "APPL", "Stock1", "Stock2"]


from io import BytesIO
from PIL import Image
import PySimpleGUI as sg

def array_to_data(array):
    im = Image.fromarray(array)
    with BytesIO() as output:
        im.save(output, format="PNG")
        data = output.getvalue()
    return data

font = ("Courier New", 11)
sg.theme("DarkBlue3")
sg.set_options(font=font)

im = Image.open("C:/Users/arucabado-gordo/OneDrive - Deloitte (O365D)/Documents")
array = np.array(im, dtype=np.uint8)
data = array_to_data(array)



#sg.Window(title = "Hello World", layout=[[]], margins = (100, 50)).read()

#layout = [[sg.Text("Do you want to get lucky?")], [sg.Button("I want to get lucky!")]]

#window = sg.Window("Stock Investment", layout)

# Create an event loop
#while True:
    #event, values = window.read()
    # End program if user closes window or
    # presses the OK button
    #if event == "I want to get lucky!" or event == sg.WIN_CLOSED:
        #break

#window.close()

#First column with not lucky button and portfolio list
header = sg.Text("How lucky are you feeling?")
list_column = [
    [
        sg.Button("Not lucky")

    ],
    [
        sg.Listbox(
            values=[], enable_events=True, size=(40, 20), key="Portfolio" # This will enable the user to see which stocks they have bought
        )
    ]
]

#Second column with lucky button and eventually coin GIF
lucky_column = [
    [
        sg.Button("Lucky")

    ]
]

#Third column with lucky+ button and time series graph
luckyPlus_graph_column = [
    [
        sg.Button("Lucky +")

    ],
    [
        sg.Canvas(key="-Canvas-")
    ]

]

#Full Layout
layout = [
    [
        sg.Column(list_column),
        sg.Column(lucky_column),
        sg.Column(luckyPlus_graph_column),
        sg.Graph(canvas_size=(640,480),
                 graph_bottom_left=(0,0),
                 graph_top_right=(640,480),
                 key="-GRAPH-",
                 change_submits=True,
                 background_color='lightblue',
                 drag_submits=True),
    ]
]

window = sg.Window("Stock Investment Game (Name TBD)", layout)
graph = window["-GRAPH-"]
graph.draw_figure(data=t, location=(0, 480))

# Create an event loop
while True:
    event, values, graph = window.read()
    # End program if user closes window or
    # presses the OK button
    if event == "Lucky":
        window["Portfolio"].update(df_lucky)
    elif event == "Lucky +":
        window["Portfolio"].update(df_lucky)
    elif event == "Not lucky" or event == sg.WIN_CLOSED:
        break

window.close()


