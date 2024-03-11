import datetime
from kite_trade import *
import pandas as pd
import ast
import Intraday_live_data
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np
import time
import os
import date_time_format


def data_saving():
    final_new=Intraday_live_data.getoptionchain(name,expiry_date)

    x=final_new["strikePrice"]
    strikes=x.tolist()

    formatted_date=date_time_format.date_time_format(expiry_date)

    for i in range(len(strikes)):
        quote_CE=name+formatted_date+str(strikes[i])+"CE"
        quote_PE=name+formatted_date+str(strikes[i])+"PE"

        atm_token_ce=kite.ltp("NFO:"+quote_CE)
        atm_token_pe=kite.ltp("NFO:"+quote_PE)
        ATM_Token_CE=atm_token_ce["NFO:"+quote_CE]['instrument_token']
        ATM_Token_PE=atm_token_pe["NFO:"+quote_PE]['instrument_token']

        import datetime

        from_datetime = datetime.datetime.now() - datetime.timedelta(days=Days)     # From last & days
        to_datetime = datetime.datetime.now()
        interval = "minute"
        content_CE=kite.historical_data(ATM_Token_CE, from_datetime, to_datetime, interval, continuous=False, oi=True)
        content_PE=kite.historical_data(ATM_Token_PE, from_datetime, to_datetime, interval, continuous=False, oi=True)

        Content_CE=str(content_CE)
        Content_PE=str(content_PE)

        cleaned_contents_CE = Content_CE.replace("datetime.datetime", "").replace(", tzinfo=tzoffset(None, 19800)", "")
        cleaned_contents_PE = Content_PE.replace("datetime.datetime", "").replace(", tzinfo=tzoffset(None, 19800)", "")

        data_CE = ast.literal_eval(cleaned_contents_CE)
        data_PE = ast.literal_eval(cleaned_contents_PE)

        df_CE = pd.DataFrame(data_CE)
        df_PE = pd.DataFrame(data_PE)

        if 'date' in df_CE.columns:
            df_CE['date'] = df_CE['date'].apply(lambda x: pd.Timestamp(year=x[0], month=x[1], day=x[2], hour=x[3], minute=x[4]))
            df_CE['Date'] = df_CE['date'].dt.strftime('%Y-%m-%d')
            df_CE['Time'] = df_CE['date'].dt.strftime('%H:%M')
            df_CE = df_CE.drop(columns=['date'])
            df_CE = df_CE[['Date', 'Time', 'open', 'high', 'low', 'close','volume','oi']]

            new_column_names_CE = {
            'Date': 'Date',
            "Time": "Time",
            "open": "open CE",
            "high": "high CE",
            "low": "low CE",
            "close": "close CE",
            "volume": "volume CE",
            "oi": "oi CE",
            # Add more columns as needed
            }

            df_CE.rename(columns=new_column_names_CE, inplace=True)
            df_CE.to_csv(path_option_cain_data_saving+name+str(strikes[i])+"_CE.csv",index=False)

        if 'date' in df_PE.columns:
            df_PE['date'] = df_PE['date'].apply(lambda x: pd.Timestamp(year=x[0], month=x[1], day=x[2], hour=x[3], minute=x[4]))
            df_PE['Date'] = df_PE['date'].dt.strftime('%Y-%m-%d')
            df_PE['Time'] = df_PE['date'].dt.strftime('%H:%M')
            df_PE = df_PE.drop(columns=['date'])

            
            df_PE = df_PE[['Date', 'Time', 'open', 'high', 'low', 'close','volume','oi']]


            new_column_names_PE = {
            'Date': 'Date',
            "Time": "Time",
            "open": "open PE",
            "high": "high PE",
            "low": "low PE",
            "close": "close PE",
            "volume": "volume PE",
            "oi": "oi PE",
                # Add more columns as needed
            }

            df_PE.rename(columns=new_column_names_PE, inplace=True)
            df_PE.to_csv(path_option_cain_data_saving+name+str(strikes[i])+"_PE.csv",index=False)





path_main="D:/ashu/Finance/algo_trading/Zerodha_GUI/Kite_Zerodha-main/Kite_Zerodha-main/"

with open(path_main+"expiry_date.txt",'r') as file:
    content_expiry_date=file.read()

name="NIFTY"

expiry_date=content_expiry_date

path="D:/ashu/Finance/algo_trading/Zerodha_GUI/OI_Raw_Data_Collected/"

## Please update the date in the path_option_cain_data_saving at every week #################

# path_option_cain_data_saving="D:/ashu/Finance/Option_chain_data/Feb_2024/15_02_2024/"

df=pd.read_csv(path_main+"Enctoke_Expiry_month_end_info.csv")

content_enctoken=df.iloc[0,0]

enctoken = content_enctoken
kite = KiteApp(enctoken=enctoken)
Days=7
data_saving()