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
That is it! Your scheduled is set up and the relevant data is going to be collected every hour. Or if you want to change the scheduled time, you can change it in the 8:
```
    sender.add_periodic_task(3600.0, dataCollection.s()) 
    # 3600.0 - time of period in seconds
```
