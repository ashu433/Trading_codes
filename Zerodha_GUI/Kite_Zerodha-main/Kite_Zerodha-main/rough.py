import pandas as pd
from kite_trade import *
from datetime import datetime, timedelta
import ast
import time
import numpy as np
import json
import requests
import Intraday_live_data
import pytz
import logging
from kiteconnect import KiteConnect
from pyotp import TOTP
from kiteconnect import KiteTicker



path_main = "D:/ashu/Finance/algo_trading/Zerodha_GUI/Kite_Zerodha-main/Kite_Zerodha-main/"

with open(path_main+'kite_api_login_credentials.txt', 'r') as file:
    data_str = file.read()

data_dict=json.loads(data_str)
logging.basicConfig(level=logging.DEBUG)
kite = KiteConnect(api_key=data_dict['API_Key'])

Access_token=data_dict["Acess_token"]
kite.set_access_token(Access_token)


instrument_dump_NSE=kite.instruments("NSE")
instrument_NSE_df=pd.DataFrame(instrument_dump_NSE)


quote="NIFTY 50"
index=instrument_NSE_df.index[instrument_NSE_df['tradingsymbol'] ==quote].tolist()
instrument_token=instrument_NSE_df.loc[index[0],"instrument_token"]

import datetime

from_datetime = datetime.datetime.now() - datetime.timedelta(days=10)     # From last & days historical limit 60 days for 1 min
to_datetime = datetime.datetime.now()

interval="day"
content=kite.historical_data(instrument_token, from_datetime, to_datetime, interval, continuous=False, oi=True)
Content=str(content)
cleaned_contents = Content.replace("datetime.datetime", "").replace(", tzinfo=tzoffset(None, 19800)", "")
data = ast.literal_eval(cleaned_contents)
df = pd.DataFrame(data)

if 'date' in df.columns:
    df['date'] = df['date'].apply(lambda x: pd.Timestamp(year=x[0], month=x[1], day=x[2], hour=x[3], minute=x[4]))
    df['Date'] = df['date'].dt.strftime('%Y-%m-%d')
    df['Time'] = df['date'].dt.strftime('%H:%M')
    df = df.drop(columns=['date'])
    df = df[['Date', 'Time', 'open', 'high', 'low', 'close','volume','oi']]

df.to_csv(path_main+"Output_file_nifty.csv",index=False)