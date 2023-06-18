import requests
from celery import Celery
import csv

app = Celery("tasks", broker='redis://localhost/0', backend='db+postgresql://postgres:marzipan@localhost/crypto')
@app.on_after_configure.connect
def schedule_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(60.0, dataCollection.s())

@app.task
def dataCollection():
        url = f"https://api.binance.com/api/v3/uiKlines?symbol=BTCUSDT&interval=1h"

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
        print("The data for BTCUSDT and 1h interval:")
        print(responseText)
        return responseText


if __name__ == "__main__":
    dataCollection()

#celery -A tasks worker -l info -P eventlet
#celery -A tasks beat --loglevel=INFO


