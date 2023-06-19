# Test task with Binance API usage.
## Task 1.
The script to collect data from Binance API for 1h interval and BTCUSDT symbol is provided in file ['tasks.py'](tasks.py).
There are **two** options for you to run the script.
### Option 1. One-time execution.
To collect data once, you have to run the file ['tasks.py'](tasks.py). The collected data will be shown in the console and will be added to file ['crypto.csv'](crypto.csv).
The data format - 500 rows with lists of OHLCV values for the last 500 hours (Open time, Open, High, Low, Close, Volume, Close time, 
Quote asset volume, Number of trades, Taker buy base asset volume, Taker buy quote asset volume, Ignore).
So the freshest data will be stored in the last 500 rows of the file.

![image](https://github.com/expresoviter/test-task-crypto/assets/89355159/22b3906e-7f21-4fb9-b37f-ccfd4207891f)

### Option 2. Periodical execution.
To collect relevant data with 1h interval, you have to have Redis installed and launched as a broker and Postgres RDB launched as a backend database for the scheduler.
Or you can choose and set up your own broker and backend database. Anyway, fill in the parameters of connection in the line 5 of ['tasks.py'](tasks.py):
```
# Example
app = Celery("tasks", broker='redis://localhost/0', backend='db+postgresql://postgres:marzipan@localhost/crypto')
```
Open the command line and type in the following command:
```
celery -A tasks worker -l info -P eventlet
```
Wait for the command to process. After successful launch of a worker and connection to the database, open the second terminal and type in the next command:
```
celery -A tasks beat --loglevel=INFO
```
That is it! Your scheduled is set up and the relevant data is going to be collected every hour. Or if you want to change the scheduled time, you can change it in the line 8:
```
    sender.add_periodic_task(3600.0, dataCollection.s()) 
    # 3600.0 - time of period in seconds
```
The collected data will be shown in the console and will be added to file ['crypto.csv'](crypto.csv). Also each completed task will be saved to your backend database. The needed table is **celery_taskmeta**. There are different columns with different variables after the completion of the task. The result of the execution is stored in **result** column. The result is stored in binary data format, so you need to download and decode it to make data understandable to the human eye.

![image](https://github.com/expresoviter/test-task-crypto/assets/89355159/6f909b21-6d7e-4b6b-9505-757a88963eba)

## Task 2. 
The Flask UI is provided in file ['app.py'](app.py) and a needed template is provided in file ['candlestick.html']('candlestick.html'). 
To run the script, you have to run the file ['app.py'](app.py). Then the server will be launched and you will be able to open the page. Just type the address in your browser and you will see the page. 

![image](https://github.com/expresoviter/test-task-crypto/assets/89355159/733d6226-f42e-4a41-9304-f4b2aaedc6a3)

The first graph is a candlestick chart with data from task 1. The chart is being built based on 500 freshest rows of the ['crypto.csv'](crypto.csv). 
The second graph is a piechart of top 10 symbols with biggest market caps. The information is extracted from CoinGeckoAPI. The graphs are dynamic, so you can interact with them.

I hope you will enjoy using these scripts.

