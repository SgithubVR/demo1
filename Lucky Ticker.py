##In this file we want to randomly select 7 'Lucky' Tickers for the lucky coinflip.

##install packages
import pandas as pd

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
print(df_lucky['Symbol'])

API="P6ZDKCUUUUKTQLSW"

#print(url)

for i in df_lucky['Symbol']:
    url=f"https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={i}&interval=5min&outputsize=full&apikey={API}"
    print(url)