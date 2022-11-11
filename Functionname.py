##In this file we want to randomly select 7 'Lucky' Tickers for the lucky coinflip.

##install packages
import pandas as pd
import requests
import numpy as np

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
df_lucky = df.sample(n = 5)
df_lucky = df_lucky[df_lucky['Symbol'].str.contains('\^')==False]

API="P6ZDKCUUUUKTQLSW"

#print(url)
df3=pd.DataFrame()

for i in df_lucky['Symbol']:
    #url=f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={i}&apikey={API}"
    url=f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={i}&apikey={API}"
    print(url)
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
    df2.info()
    #df2[['Date', 'Time']] = df2['index'].str.split(' ', 1, expand=True)
    df2['symbol']=f"{i}"
    df3 = pd.concat([df3,df2], axis=0)
    print(df3)

df3['profit']=df3['close']-df3['open']
print(df3)

df_tryout=pd.pivot_table(df3, values='profit', index=['index'],
                    columns=['symbol'], aggfunc=np.sum)
print(df_tryout)

