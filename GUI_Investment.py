import pandas as pd

import PySimpleGUI as sg
import os.path
import numpy as np
import matplotlib.pyplot as mt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from random import randint
import requests

##import data
ticker = pd.read_csv(f'C:/Users/arucabado-gordo/PycharmProjects/demo1/nasdaq_screener_1668088408246.csv')
month =[]
[month.append(i) for i in range(9,100)]


def create_plot(month, performance, clear=None):
    mt.plot(month, performance, color='blue', marker='o')
    mt.title("Investment performance over the last 6 months", fontsize=10)
    mt.xlabel('Month', fontsize=10)
    mt.ylabel("Rate", fontsize=10)
    mt.grid(True)
    return mt.gcf()

def draw_figure(canvas, figure):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
    return figure_canvas_agg

def stock_data(ticker):
    API="P6ZDKCUUUUKTQLSW"
    df3=pd.DataFrame()
    # df_lucky =

    for i in df_lucky['Symbol']:
        # url=f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={i}&apikey={API}"
        url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={i}&apikey={API}"
        response = requests.get(url)
        # Since we are retrieving stuff from a web service, it's a good idea to check for the return status code
        # See: https://en.wikipedia.org/wiki/List_of_HTTP_status_codes
        if response.status_code != 200:
            raise ValueError("Could not retrieve data, code:", response.status_code)
        # The service sends JSON data, we parse that into a Python datastructure
        raw_data = response.json()
        data = raw_data['Time Series (Daily)']
        df = pd.DataFrame(data).T.apply(pd.to_numeric)
        # Next we parse the index to create a datetimeindex
        df.index = pd.DatetimeIndex(df.index)
        # Let's fix the column names by chopping off the first 3 characters
        df.rename(columns=lambda s: s[3:], inplace=True)
        df2 = df.reset_index()
        df2 = df2.astype({'index': 'string'})
        # df2[['Date', 'Time']] = df2['index'].str.split(' ', 1, expand=True)
        df2['symbol'] = f"{i}"
        df3 = pd.concat([df3, df2], axis=0)
    return df3


def combined_data(df3):
    df3['profit'] = df3['close'] - df3['open']
    df_all = pd.pivot_table(df3, values=['profit', 'open', 'close'], index=['index'], columns=['symbol'],
                            aggfunc=np.sum).reset_index()
    return df_all

def lucky(df, balance, date=None):
    balance = int(values["-WALLET-"])
    date = '2022-07-07'
    df3 = stock_data(df)
    df_all = combined_data(df3)
    df_all.rename(columns = {'index':'Date'}, inplace = True)
    indexvalue=df_all.index[df_all['Date']==f'{date}'].tolist()
    index_start=indexvalue[0]
    df_all=df_all.sort_values(by='Date', ascending=True)
    index_end=100 # df_all length - 100 timestamps
    list_new_portfolio_balance=[]
    for i in range(index_start, index_end):
        index=i
        ## retrieves the information on what stocks you bought at what price on that particular day
        df_buy=df_all['open'].iloc[index]
        df_buy=df_buy.reset_index()
        df_buy.rename(columns = {index:'Buy'}, inplace = True)
        ## retrieves the information on what stocks you sold at what price on that particular day
        df_sell = df_all['close'].iloc[index]
        df_sell = df_sell.reset_index()
        df_sell.rename(columns = {index:'Sell'}, inplace = True)
        ## adds a timestamp to the information list
        df_sell['Date']=df_all['Date'].iloc[index]
        # creates dataframe to combine information on prices, timestamp and available money part for looping
        df_complete=pd.DataFrame()
        am = balance / len(df_lucky)  # available money per stock if wallet is evenly distributed over available stocks
        df_complete['symbol'] = df3['symbol'].unique()
        df_complete['Available_Money'] = am
        df_complete = df_complete.merge(df_buy, how="inner", on='symbol')
        df_complete = df_complete.merge(df_sell, how="inner", on='symbol')
        df_complete['Amount_bought'] = df_complete['Available_Money'] / df_complete['Buy']
        df_complete['Amount_bought'] = df_complete['Amount_bought'].astype(int)
        df_complete['Profit'] = (df_complete['Sell'] - df_complete['Buy']) * df_complete['Amount_bought']
        df_complete['Actually_spend'] = df_complete['Buy'] * df_complete['Amount_bought']
        df_complete['Date']=df_sell['Date']
        #df_complete['Date'] =df_all['Date'].iloc[index]
        profit = df_complete['Profit'].sum()
        spent = df_complete['Actually_spend'].sum()
        balance= profit + balance
        list_new_portfolio_balance.append(balance)
    return balance, list_new_portfolio_balance


def lucky_stocks(ticker):
    ticker_symbol = ticker['Symbol']
    ##select the tickers
    ticker_symbol = ticker['Symbol']
    ##print(ticker_symbol)
    ##make dataframe
    df = pd.DataFrame(data=ticker_symbol)
    ##remove unlucky numbers
    # df = df.drop([13, 666])
    ##select the random lucky companies
    df_lucky = df.sample(n=7)
    #drop tickers with ^
    df_lucky.astype(str)
    df_lucky = df_lucky[df_lucky['Symbol'].str.contains('\^') == False]
    #coinflip the random sample
    df_lucky = df_lucky.sample(frac=0.50)
    #drop of more than 5 entries because we use the basic fucntion
    number = len(df_lucky)
    # remove lines if more than 7
    while number > 5:
        df_lucky = df_lucky[:-1]
        number -= 1
    return df_lucky

df_lucky = lucky_stocks(ticker)



# Section to deposit money
input_row = [
    [
        sg.Text("How much do you want to invest?"),
        sg.Input(key="-IN-"),
        sg.Button("Deposit")
        # Add functionality to change currencies
    ]
]

# Section for buttons
button_row = [
    [
        sg.Text("How lucky are you feeling today?")
    ],
    [
        sg.Button("Not lucky"),
        sg.Button("Lucky"),
        sg.Button("Lucky +"),
    ]
]


# First column with
lucky_column = [
    [
        sg.Text("Your Portfolio")
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
        sg.Canvas(size=(50,50), key="-CANVAS-")
    ]

]

#Full Layout
layout = [
    [
       input_row
    ],
    [
       button_row
    ],
    [
       sg.Column(lucky_column, scrollable=False, element_justification="center"),
       sg.Column(luckyPlus_graph_column),
    ],
    [
       sg.Button("Exit")
    ]
]



window = sg.Window("Stock Investment Game (Name TBD)", layout ,finalize=True, element_justification='center').Finalize()
canvas_elem = window["-CANVAS-"]
canvas = canvas_elem.TKCanvas

figure = Figure()
ax = figure.add_subplot(111)
ax.set_xlabel("Months")
ax.set_ylabel("EUR") # Make dynamic, respond to different currencies
ax.grid()
fig_agg = draw_figure(canvas, figure)


# Create an event loop to initialize the GUI
while True:
    event, values = window.read()
    window['-WALLET-'].Update(values['-IN-'])

    if event == "Deposit":
        # window['-WALLET-'].Update(values['-IN-'])
        sg.popup(f"Your balance is €{values['-IN-']}")

    if event == "Lucky":
        window["Portfolio"].update(df_lucky['Symbol'])
        ax.cla()
        ax.grid()
        ax.set_xlabel("Days")
        ax.set_ylabel("EUR") # Make dynamic, respond to different currencies
        balance = values["-WALLET-"]
        performance = lucky(df_lucky, int(balance))
        ax.plot(month, performance[1])
        fig_agg.draw()
        window["-WALLET-"].update(performance[0].astype(int))
        new_balance = performance[0]
        window.refresh()
        if new_balance >= int(values["-IN-"]):
            sg.Popup(f"After investing for 100 days, your balance is: €{new_balance}. Congrats!")
        elif new_balance <= int(values["-IN-"]):
            sg.Popup(f"After investing for 100 days, your balance is: €{new_balance}. Better luck next time!")

    elif event == "Lucky +":
        window["Portfolio"].update(df_lucky)
        ax.cla()
        ax.grid()
        ax.set_xlabel("Months")
        ax.set_ylabel("EUR") # Make dynamic, respond to different currencies
        performance = [randint(500, 1000) for x in range(6)]
        ax.plot(month, performance, "o")
        fig_agg.draw()
        window.refresh()
        if int(values["-WALLET-"]) >= 30000:
            sg.Popup(f"After investing for 100 days, your balance is: €{values['-IN-']}. Congrats!")
        elif int(values["-WALLET-"]) <= 30000:
            sg.Popup(f"After investing for 100 days, your balance is: €{values['-IN-']}. Better luck next time!")

    elif event == "Not lucky" or event == "Exit" or event == sg.WIN_CLOSED:
        break


window.close()





