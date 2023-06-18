from flask import Flask, render_template
import pandas as pd
import plotly.graph_objects as go
import plotly
import plotly.express as px
import json
from datetime import datetime
import requests

app = Flask(__name__)

@app.route('/')
def visualize():
    df = pd.read_csv('C:/Users/LEGION/Desktop/Владик/testBinance/crypto.csv',
                       names=["Open time", "Open", "High", "Low",
                              "Close", "Volume", "Close time",
                              "Quote asset volume", "Number of trades",
                              "Taker buy base asset volume",
                              "Taker buy quote asset volume", "Ignore"])
    df = df[-500:]
    for i in range(0, df.shape[0]):
        df.iloc[i,0] = datetime.utcfromtimestamp(int(df.iloc[i,0]) / 1000)
    fig = go.Figure(data=[go.Candlestick(x=df['Open time'],
                                       open=df['Open'],
                                       high=df['High'],low=df['Low'],close=df['Close'])])
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    url = 'https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=10&page=1&sparkline=false&locale=en'
    response = requests.request("GET", url)
    responseText = response.text
    responseText = eval(responseText.replace("null", "None"))
    df1=[]
    for i in responseText:
        df1.append([i["name"], i["market_cap"]])
    df1 = pd.DataFrame(df1, columns=["Name", "Market Cap"])
    fig1 = px.pie(df1, values="Market Cap", names="Name", title="Top 10 symbols with biggest market caps")
    graphJSON1 = json.dumps(fig1, cls=plotly.utils.PlotlyJSONEncoder)
    return render_template('candlestick.html', graphJSON=[graphJSON, graphJSON1])


if __name__ == '__main__':
    app.run()
