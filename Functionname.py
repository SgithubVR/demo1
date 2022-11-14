##In this file we want to randomly select 7 'Lucky' Tickers for the lucky coinflip.

##install packages
import pandas as pd
import requests
import numpy as np
import math

##import data
ticker = pd.read_csv('nasdaq_screener_1668088408246.csv')
#print(ticker)

##select the tickers
ticker_symbol = ticker['Symbol']
##print(ticker_symbol)

##make dataframe
df = pd.DataFrame(data=ticker_symbol)

##remove unlucky numbers
df = df.drop([13, 666])

##select the random lucky companies
df_lucky = df.sample(n = 7)

#drop tickers with ^
df_lucky.astype(str)
df_lucky = df_lucky[df_lucky['Symbol'].str.contains('\^')==False]

#coinflip the random sample
df_lucky = df_lucky.sample(frac=0.50)

#drop of more than 5 entries because we use the basic fucntion
number = len(df_lucky)

# remove lines if more than 7
while number > 5:
    df_lucky = df_lucky[:-1]
    number -= 1

#df_lucky = df.sample(n = 5)
#df_lucky = df_lucky[df_lucky['Symbol'].str.contains('\^')==False]

API="P6ZDKCUUUUKTQLSW"

#print(url)
df3=pd.DataFrame()

for i in df_lucky['Symbol']:
    #url=f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={i}&apikey={API}"
    url=f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={i}&apikey={API}"
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
    #df2[['Date', 'Time']] = df2['index'].str.split(' ', 1, expand=True)
    df2['symbol']=f"{i}"
    df3 = pd.concat([df3,df2], axis=0)

df3['profit']=df3['close']-df3['open']
print(df3)

df_all=pd.pivot_table(df3, values=['profit','open','close'], index=['index'],
                    columns=['symbol'], aggfunc=np.sum).reset_index()
#df_profit=pd.pivot_table(df3, values='profit', index=['index'],
                    #columns=['symbol'], aggfunc=np.sum)
#df_cost=pd.pivot_table(df3, values='open', index=['index'],
                    #columns=['symbol'], aggfunc=np.sum)
#df_revenue=pd.pivot_table(df3, values='close', index=['index'],
                    #columns=['symbol'], aggfunc=np.sum)


# ## pick day 7-7
# def timeline(index):
#     profit=
#
new_portfolio_balance=30000
wallet=30000
today='2022-07-07'
df_all.rename(columns = {'index':'Date'}, inplace = True)
indexvalue=df_all.index[df_all['Date']==f'{today}'].tolist()
index_start=indexvalue[0]
df_all=df_all.sort_values(by='Date', ascending=True)
index_end=len(df_all)
index=index_start
df_buy=df_all['open'].iloc[index]
df_buy=df_buy.reset_index()
df_buy.rename(columns = {index:'Buy'}, inplace = True)
df_sell = df_all['close'].iloc[index]
df_sell = df_sell.reset_index()
df_sell.rename(columns = {index:'Sell'}, inplace = True)
print(df_buy)
print(df_sell)
# create dataframe to see how many stocks we can buy on the allocated date
# available in wallet (NEEDS TO BE UPDATED!)

# in case of evenly distributed ( "you feel lucky")

# new part for looping

df_complete=pd.DataFrame()

am = new_portfolio_balance / len(df_lucky)  # available money per stock if wallet is evenly distributed over available stocks
df_complete['symbol'] = df3['symbol'].unique()
df_complete['Available_Money'] = am
df_complete = df_complete.merge(df_buy, how="inner", on='symbol')
df_complete = df_complete.merge(df_sell, how="inner", on='symbol')
df_complete['Amount_bought'] = df_complete['Available_Money'] / df_complete['Buy']
df_complete['Amount_bought'] = df_complete['Amount_bought'].astype(int)
df_complete['Profit'] = (df_complete['Sell'] - df_complete['Buy']) * df_complete['Amount_bought']
df_complete['Actually_spend'] = df_complete['Buy'] * df_complete['Amount_bought']
profit = df_complete['Profit'].sum()
spent = df_complete['Actually_spend'].sum()
new_portfolio= profit + spent
new_portfolio_balance=new_portfolio_balance+new_portfolio
print(df_complete)
#print(df_complete[df_complete['Date'].isin([f'{today}'])].index)