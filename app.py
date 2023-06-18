from flask import Flask, render_template
import pandas as pd
import plotly.graph_objects as go
import plotly
import json
from datetime import datetime

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
        df.iloc[i,0] = datetime.utcfromtimestamp(int(df.iloc[i,0])/1000)
    fig = go.Figure(data=[go.Candlestick(x=df['Open time'],
                                       open=df['Open'],
                                       high=df['High'],low=df['Low'],close=df['Close'])])
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return render_template('candlestick.html',graphJSON=graphJSON)


if __name__ == '__main__':
    app.run()
