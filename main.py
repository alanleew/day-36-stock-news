import requests
from twilio.rest import Client

STOCK = "AAPL"
COMPANY_NAME = "Apple"
STOCK_ENDPOINT = "https://www.alphavantage.co/query"
# STOCK_API_KEY = "QS2UJG0E1MVNRI87"
STOCK_API_KEY = "X41VAJSI09XRYUK8" # Second account created using alanleew412+test@gmail.com
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
NEWS_API_KEY = "ca34d4e6c04548acbbcd901de7d725fa"
TWILIO_SID = 'ACed14ae15072c49c76eeab625db8144fb'
TWILIO_AUTH_TOKEN = "adab9f463bb92ff14c0ab8b4cdd35804"

stock_param = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "apikey": STOCK_API_KEY,
}
stock_request = requests.get(STOCK_ENDPOINT, params=stock_param)
stock_request.raise_for_status()
### WARNING - Stock API can only request 25 times daily! ###
stock_data = stock_request.json()["Time Series (Daily)"]
dates = list(stock_data.keys())
yesterday = stock_data[dates[0]]
day_before_yesterday = stock_data[dates[1]]
yesterday_close = float(yesterday["4. close"])
day_before_close = float(day_before_yesterday["4. close"])
price_change = float(format(yesterday_close - day_before_close, ".2f"))
percentage_change = float(format(price_change / yesterday_close * 100, ".2f"))

# If percentage change > 5%, send a Whatsapp message
if abs(percentage_change) > 0.05:
    news_param = {
        "q": (STOCK, COMPANY_NAME),
        "apikey": NEWS_API_KEY,
        # "pageSize": 100,
    }
    news_request = requests.get(NEWS_ENDPOINT, params=news_param)
    news_json_data = news_request.json()
    top_articles = news_json_data["articles"][0:3]
    headline = [article["title"] for article in top_articles]
    brief = [article["content"] for article in top_articles]

    if percentage_change > 0:
        message_body = f"{STOCK} 🔺+{percentage_change}%"
    else:
        message_body = f"{STOCK} 🔻{percentage_change}%"

    client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)
    message = [client.messages.create(
        from_='whatsapp:+14155238886',
        to='whatsapp:+19178853233',
        body=f"{message_body}\n"
             f"{article["title"]}\n"
             f"{article["content"]}"
    ) for article in top_articles
    ]
