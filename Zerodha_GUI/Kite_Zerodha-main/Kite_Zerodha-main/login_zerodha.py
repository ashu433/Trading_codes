from kiteconnect import KiteConnect
from pyotp import TOTP
from kiteconnect import KiteTicker
import pandas as pd
import ast
import logging
from kiteconnect import KiteConnect
import time
import json
from datetime import datetime, timedelta

path_main="D:/ashu/Finance/algo_trading/Zerodha_GUI/Kite_Zerodha-main/Kite_Zerodha-main/"

with open(path_main+'kite_api_login_credentials.txt', 'r') as file:
    data_str = file.read()


data_dict=json.loads(data_str)
logging.basicConfig(level=logging.DEBUG)
kite = KiteConnect(api_key=data_dict['API_Key'])
print(kite.login_url())

############################# WRITING THE ACCESS TOKEN #############################################

request_token="mvIvWQWNctTWDglE7NJfKoAF3c7pq5bB"


data = kite.generate_session(request_token, api_secret=data_dict["API_Secret_Key"])
print(data['access_token'])
data_dict["Acess_token"]=data['access_token']

data_str = json.dumps(data_dict, indent=4)

with open(path_main+'kite_api_login_credentials.txt','w') as file:
    file.write(data_str)


############################# WRITING THE ACCESS TOKEN #############################################

############################# READING THE ACESS TOKEN ##############################################


# date, time = Date_time.split()

# instrument_dump=kite.instruments("NSE")
# print(instrument_dump)
# instrument_df=pd.DataFrame(instrument_dump)
# print(instrument_df)

############################# READING THE ACESS TOKEN ##############################################