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

#print(url)
API="P6ZDKCUUUUKTQLSW"
for i in df_lucky['Symbol']:
    url=f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={i}&interval=5min&outputsize=full&apikey={API}"
    print(url)

