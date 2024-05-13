import pandas as pd
from kite_trade import *
from datetime import datetime,timedelta
import ast
import requests
import json


path_main="D:/ashu/Finance/algo_trading/Zerodha_GUI/Kite_Zerodha-main/Kite_Zerodha-main/"
path="D:/ashu/Finance/algo_trading/Option_chain_data/"
path_closing_price="H:/My Drive/Daily_F_O_data/Daily_closing_price_data/"

################################  Values in the data #############################

df=pd.read_csv(path_main+"Enctoke_Expiry_month_end_info.csv")
content_enctoken=df.iloc[0,0]
enctoken = content_enctoken
kite = KiteApp(enctoken=enctoken)

filter_time="15:30"

list_1_min=["NIFTY 50", "NIFTY BANK","NIFTY FIN SERVICE","NIFTY MID SELECT","SENSEX"]
Sectors_list=["IT","FMCG","HEALTHCARE","PHARMA","AUTO","REALTY","METAL","MEDIA","OIL AND GAS","CONSR DURBL","PSU BANK","INDIA VIX"]


for sector in Sectors_list:
    if sector!="INDIA VIX":
        quote="NIFTY "+str(sector)
    elif sector=="INDIA VIX":
        quote=str(sector)
    else:
        pass
    print(sector)
    df=pd.read_csv(path_closing_price+quote+".csv")
    df['Time'] = pd.to_datetime(df['Time'])
    df = df[df['Time'] <= pd.to_datetime(filter_time)]
    df['Time'] = df['Time'].dt.strftime('%H:%M')
    df.to_csv(path_closing_price+quote+".csv",index=False)