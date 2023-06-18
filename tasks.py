import requests
from celery import Celery

app=Celery("tasks", broker='redis://localhost')
@app.on_after_configure.connect
def schedule_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(3600.0, dataCollection.s("BTCUSDT","1h"))

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
        print(responseText)


if __name__=="__main__":
    symbol = (input("Enter the symbol: ")).upper()
    interval = input("Enter the interval (1d, 4h, 1h): ")
    dataCollection(symbol,interval)

#celery -A tasks worker -l info -P eventlet
#celery -A tasks beat --loglevel=INFO


