import requests
import json
import pandas as pd
import datetime as dt


# Получаем исторические данные от Binance
def get_binance_bars(symbol, interval, startTime, endTime):
        url = "https://api.binance.com/api/v3/klines"
        startTime = str(int(startTime.timestamp() * 1000))
        endTime = str(int(endTime.timestamp() * 1000))
        limit = '1000'
        req_params = {"symbol" : symbol, 'interval' : interval, 'startTime' : startTime, 'endTime' : endTime, 'limit' : limit}
        df = pd.DataFrame(json.loads(requests.get(url, params = req_params).text))
        if (len(df.index) == 0):
            return None
        df = df.iloc[:, 0:5]
        df.columns = ['Datetime', 'Open', 'High', 'Low', 'Close']
        df.Open      = df.Open.astype("float")
        df.High      = df.High.astype("float")
        df.Low       = df.Low.astype("float")
        df.Close     = df.Close.astype("float")
        df.index = [dt.datetime.fromtimestamp(x / 1000.0) for x in df.Datetime]
        return df

def pd_datas(TICKER, INTERVAL, START, END):
    df_list = []
    while True:
        new_df = get_binance_bars(TICKER, INTERVAL, START, END)
        if new_df is None:
            break
        df_list.append(new_df)
        START = max(new_df.index) + dt.timedelta(0, 1)
    return pd.concat(df_list)