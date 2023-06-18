import requests
from celery import Celery
import csv

app=Celery("tasks", broker='redis://localhost/0', backend='db+postgresql://postgres:marzipan@localhost/crypto')
@app.on_after_configure.connect
def schedule_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(20.0, dataCollection.s("BTCUSDT","1h"))

@app.task
def dataCollection(symbol, interval):
    if interval != "1d" and interval != "4h" and interval != "1h":
        print("Entered interval is incorrect.")
    else:
        url = f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval={interval}"

        payload = {}
        headers = {}

        response = requests.request("GET", url, headers=headers, data=payload)

        responseText = eval(response.text)
        if response.status_code != 200:
             if responseText["code"] == -1100 or responseText["code"] == -1121:
                print("Entered symbol is incorrect.")
        else:
            with open("crypto.csv","a", newline="") as f:
                write=csv.writer(f)
                write.writerows(responseText)
        print(responseText)
        return responseText


if __name__=="__main__":
    symbol = (input("Enter the symbol: ")).upper()
    interval = input("Enter the interval (1d, 4h, 1h): ")
    dataCollection(symbol,interval)

#celery -A tasks worker -l info -P eventlet
#celery -A tasks beat --loglevel=INFO


