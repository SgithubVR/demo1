import pandas as pd

import PySimpleGUI as sg
import os.path
import numpy as np
import matplotlib.pyplot as mt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from random import randint

month = ["June", "July", "August", "September", "October", "November"]

def create_plot(month, performance, clear=None):
    mt.plot(month, performance, color='blue', marker='o')
    mt.title("Investment performance over the last 6 months", fontsize=10)
    mt.xlabel('Month', fontsize=10)
    mt.ylabel("Rate", fontsize=10)
    mt.grid(True)
    return mt.gcf()




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
#Third column with lucky+ button and time series graph
header_row = [
    [
        sg.Text("How much do you want to invest?"),
        sg.Input(key="-IN-"),
        sg.Button("Deposit")
    ]
]

list_column = [
    [
        sg.Button("Not lucky")

    ]
]

#Second column with lucky button and eventually coin GIF
lucky_column = [
    [
        sg.Button("Lucky")

    ],
    [
        sg.Listbox(
            values=[], enable_events=False, size=(40, 20), key="Portfolio" # This will enable the user to see which stocks they have bought
        )
    ],
    [
        sg.Text("Wallet"),
        sg.Multiline(size=(10,2), key="-WALLET-")
    ]
]


luckyPlus_graph_column = [
    [
        sg.Button("Lucky +")

    ],
    [
        sg.Canvas(size=(50,50), key="-CANVAS-")
    ]

]

#Full Layout
layout = [
    [
        header_row
    ],
    [
        sg.Column(list_column),
        sg.Column(lucky_column),
        sg.Column(luckyPlus_graph_column),
    ]
]

def draw_figure(canvas, figure):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
    return figure_canvas_agg

window = sg.Window("Stock Investment Game (Name TBD)", layout, finalize=True, element_justification='center').Finalize()
# window.Element("-WALLET-")._TKOut.output.bind("<Key>", lambda e: "break") # Making output box read-only
canvas_elem = window["-CANVAS-"]
canvas = canvas_elem.TKCanvas

figure = Figure()
ax = figure.add_subplot(111)
ax.set_xlabel("X axis")
ax.set_ylabel("Y axis")
ax.grid()
fig_agg = draw_figure(canvas, figure)


# Create an event loop
while True:
    event, values = window.read()
    window['-WALLET-'].Update(values['-IN-'])

    if event == "Deposit":
        # window['-WALLET-'].Update(values['-IN-'])
        sg.popup(f"Your balance is {values['-IN-']}")

    if event == "Lucky":
        window["Portfolio"].update(df_lucky)
        ax.cla()
        ax.grid()
        performance = [randint(500, 1000) for x in range(6)]
        ax.plot(month, performance)
        fig_agg.draw()
        window.refresh()

    elif event == "Lucky +":
        window["Portfolio"].update(df_lucky)
        ax.cla()
        ax.grid()
        performance = [randint(500, 1000) for x in range(6)]
        ax.plot(month, performance)
        fig_agg.draw()
        window.refresh()
    elif event == "Not lucky" or event == sg.WIN_CLOSED:
        break


window.close()





