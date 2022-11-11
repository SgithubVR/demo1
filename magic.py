import requests
import pandas as pd
import matplotlib as plt
response = requests.get("https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=MSFT&interval=5min&outputsize=full&apikey=demo")

# Since we are retrieving stuff from a web service, it's a good idea to check for the return status code
# See: https://en.wikipedia.org/wiki/List_of_HTTP_status_codes
if response.status_code != 200:
    raise ValueError("Could not retrieve data, code:", response.status_code)

# The service sends JSON data, we parse that into a Python datastructure
raw_data = response.json()

# So it's a dict. what are the keys?
print(raw_data.keys())

# Let's look at the first key/value.
# This is just some descriptive information
raw_data['Meta Data']

# The other key/value pair is the actual time series.
# This is a dict as well
time_series = raw_data['Time Series (5min)']
type(time_series)
print(time_series)
# How many items are in there?
print(len(time_series))

# Let's take the first few keys
first_ten_keys = list(time_series.keys())[:10]
# And see the corresponding values
first_ten_items = [f"{key}: {time_series[key]}" for key in first_ten_keys ]
print("\n".join(first_ten_items))

data = raw_data['Time Series (5min)']
df = pd.DataFrame(data).T.apply(pd.to_numeric)
df.info()

# Next we parse the index to create a datetimeindex
df.index = pd.DatetimeIndex(df.index)
# Let's fix the column names by chopping off the first 3 characters
df.rename(columns=lambda s: s[3:], inplace=True)

print(df.head())
df[['open', 'high', 'low', 'close']].plot()

df2 = df.reset_index()
print(df2)

df2 = df2.astype({'index':'string'})
df2.info()
df2[['Date', 'Time']] = df2['index'].str.split(' ', 1, expand=True)
print(df2)
