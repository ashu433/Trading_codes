import pandas as pd
from datetime import datetime
import requests
import time
import json

def date_to_time_stamp(date):
    time_tuple=date.timetuple()
    timestamp=round(time.mktime(time_tuple))
    return timestamp

def time_stamp_to_date(timestamp):
    return datetime.fromtimestamp(timestamp)


def Historical_data_collection_for_1_year(Symbol_of_stock,start_date,end_date,interval):
    path_index = "D:/ashu/Finance/algo_trading/Option_chain_data/"

    start_date_str = start_date
    end_date_str = end_date
    count=2100000

    # Convert string dates to datetime objects
    start_date = datetime.strptime(start_date_str, "%d-%m-%Y")
    end_date = datetime.strptime(end_date_str, "%d-%m-%Y")

    # Convert datetime objects to Unix timestamps
    Start_date = date_to_time_stamp(start_date)
    End_date = date_to_time_stamp(end_date)

    Stock_name=Symbol_of_stock

    url = f"https://priceapi.moneycontrol.com/techCharts/indianMarket/stock/history?symbol={Stock_name}&resolution={interval}&from=1722009251&to=1722157682&countback={count}&currencyCode=INR"

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
    }

    response = requests.get(url, headers=headers)

    # Print status code and response text for debugging
    print(f"Status code: {response.status_code}")
    # print(f"Response text: {response.text}")

    try:
        resp = response.json()
        df=pd.DataFrame(resp)
        date=[]
        for dt1 in df['t']:
            date.append({'Date':time_stamp_to_date(dt1)})

        dt1=pd.DataFrame(date)
        intraday_data=pd.concat([dt1,df['o'],df['h'],df['l'],df['c'],df['v']],axis=1)
        print(type(intraday_data.loc[0,"Date"]))
        intraday_data["date"]=intraday_data["Date"].dt.date.astype(str)
        intraday_data["time"]=intraday_data["Date"].dt.time.astype(str)
        intraday_data = intraday_data.drop(columns=['Date'])
        date_column = intraday_data.pop('date')
        time_column = intraday_data.pop('time')
        intraday_data.insert(0, 'date', date_column)
        intraday_data.insert(1, 'time', time_column)
        intraday_data = intraday_data.rename(columns={
            'date': 'Date',
            'time': 'Time',
            'o': 'open',
            'h': 'high',
            'l':"low",
            'c':"close",
            'v':"volume"
        })

        # print(intraday_data)
        intraday_data["oi"]=0
        intraday_data.to_csv(path_index+Stock_name+".csv",index=False)

    except json.JSONDecodeError as e:
        print(f"JSON decode error: {e}")



if __name__=='__main__':  
    pass
