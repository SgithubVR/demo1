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
    ],
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
        sg.VSeparator(),
        sg.Column(lucky_column),
        sg.VSeparator(),
        sg.Column(luckyPlus_graph_column)
    ]
]

window = sg.Window("Stock Investment Game (Name TBD)", layout)
draw_figure(window["-Canvas-"].TKCanvas, fig)

# Create an event loop
while True:
    event, values = window.read()
    # End program if user closes window or
    # presses the OK button
    if event == "Lucky":
        window["Portfolio"].update([df_lucky])
    elif event == "Not lucky" or event == sg.WIN_CLOSED:
        break

window.close()


