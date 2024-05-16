import requests

def fetch_stock_data(symbol):
    ALPHA_VANTAGE_API_KEY = 'JBN8YV6NR69F94UC'
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={symbol}&interval=5min&apikey={ALPHA_VANTAGE_API_KEY}'
    response = requests.get(url)
    data = response.json()
    return data['Time Series (5min)']