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
import zipfile
import io
import requests
import json
import shutil
import logging
from kiteconnect import KiteConnect
from pyotp import TOTP
from kiteconnect import KiteTicker


def formatted_dates(expiry,month_end):
    mont_dict={"Jan":1,"Feb":2,"Mar":3,"Apr":4,"May":5,"Jun":6,"Jul":7,"Aug":8,"Sep":9,"Oct":10,"Nov":11,"Dec":12}

    if month_end==0:

        parsed_date = datetime.strptime(expiry, '%d-%b-%Y')
        formatted_date = parsed_date.strftime('%y%m%d')

        char_list = list(formatted_date)

        month=expiry.split('-')[1]

        Letter_to_insert=str(mont_dict[month])
        length=len(formatted_date)
        first=formatted_date[0:2]
        last=formatted_date[length-2:length]

        formatted_date=first+Letter_to_insert+last

        return formatted_date
    elif month_end==1:

        parsed_date = datetime.strptime(expiry, '%d-%b-%Y')
        formatted_date = parsed_date.strftime('%Y%b').upper()
        formatted_date=formatted_date[2:]

        return formatted_date

def sensex(quote_CE,quote_PE,strikes_sensex,xox):
    global token_not_present_in_data


    instrument_dump_BFO=kite.instruments("BFO")
    instrument_BFO_df=pd.DataFrame(instrument_dump_BFO)

    index_CE=instrument_BFO_df.index[instrument_BFO_df['tradingsymbol'] ==quote_CE].tolist()
    index_PE=instrument_BFO_df.index[instrument_BFO_df['tradingsymbol'] ==quote_PE].tolist()

    if len(index_CE)==0 or len(index_PE)==0:
        token_not_present_in_data.append(quote_CE)
        token_not_present_in_data.append(quote_PE)
    else:

        atm_token_ce=instrument_BFO_df.loc[index_CE[0],"instrument_token"]
        atm_token_pe=instrument_BFO_df.loc[index_PE[0],"instrument_token"]

        ATM_Token_CE=atm_token_ce
        ATM_Token_PE=atm_token_pe

        print(ATM_Token_CE)
        print(ATM_Token_PE)
        print(quote_CE)
        print(quote_PE)

        import datetime

        from_datetime = datetime.datetime.now() - datetime.timedelta(days=1)     # From last & days
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
            df_CE.to_csv(xox+"SENSEX"+str(strikes_sensex)+"_CE.csv",index=False)

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
            df_PE.to_csv(xox+"SENSEX"+str(strikes_sensex)+"_PE.csv",index=False)

    with open(xox+"Strikes_not_present.txt","w") as file:

        for item in token_not_present_in_data:
            file.write(str(item)+ "\n")
  

def MIDCPNIFTY_SENSEX(symbol):
    if symbol=="MIDCPNIFTY":
        x=kite.ltp("NSE:NIFTY MID SELECT")
        price=x['NSE:NIFTY MID SELECT']['last_price']
        closest_number = round(price/ 25) * 25
        upper_list=[]
        lower_list=[]

        for i in range(41):
            xx=closest_number+i*25
            upper_list.append(xx)

        for j in range(1,41):
            yy=closest_number-j*25
            lower_list.append(yy)

        set_upper = set(upper_list)
        set_lower = set(lower_list)

        non_common_elements = list(set_upper.symmetric_difference(set_lower))
        strike_price_list=sorted(non_common_elements)


        return strike_price_list
    
    elif symbol=="SENSEX":
        x=kite.ltp("BSE:SENSEX")
        price=x['BSE:SENSEX']['last_price']
        closest_number = round(price/ 100) * 100
        upper_list=[]
        lower_list=[]

        for i in range(41):
            xx=closest_number+i*100
            upper_list.append(xx)

        for j in range(1,41):
            yy=closest_number-j*100
            lower_list.append(yy)

        set_upper = set(upper_list)
        set_lower = set(lower_list)

        non_common_elements = list(set_upper.symmetric_difference(set_lower))
        strike_price_list=sorted(non_common_elements)

        return strike_price_list



def Options_index():

    from datetime import datetime
    global token_not_present_in_data
    

    current_date = datetime.now()

    formatted_current_date = current_date.strftime('%d-%b-%Y')
    os.makedirs(path_index+formatted_current_date, exist_ok=True)

    path_index_new=f'{path_index}{formatted_current_date}/'
    print(path_index_new)


    index_data=pd.read_csv(path_main+"Index_Symbols_Expiry.csv")

    sym=index_data["Symbol"]
    Symbol_index=sym.to_list()
    date=index_data["Expiry Date"]
    Expiry_dates=date.to_list()
    Month_End=index_data["Month End"]
    month_end_status=Month_End.to_list()

    instrument_dump_NFO=kite.instruments("NFO")
    instrument_NFO_df=pd.DataFrame(instrument_dump_NFO)

    for i in range(len(Symbol_index)):
        from datetime import datetime

        date_object = datetime.strptime(Expiry_dates[i], '%d-%b-%y')
        expiry_date = date_object.strftime('%d-%b-%Y')
        token_not_present_in_data=[]

        if Symbol_index[i]=="MIDCPNIFTY" or Symbol_index[i]=="SENSEX":
            strikes=MIDCPNIFTY_SENSEX(Symbol_index[i])
        else:
            final_new=Intraday_live_data.getoptionchain(Symbol_index[i],expiry_date)
            x=final_new["strikePrice"]
            strikes=x.tolist()

        modified_date=formatted_dates(expiry_date,month_end_status[i])

        Name_instrument=f"{Symbol_index[i]}_{expiry_date}"

        os.makedirs(path_index_new+Name_instrument, exist_ok=True)

        xox=f"{path_index_new}{Name_instrument}/"

        for j in range(len(strikes)):

            quote_CE=Symbol_index[i]+modified_date+str(strikes[j])+"CE"
            quote_PE=Symbol_index[i]+modified_date+str(strikes[j])+"PE"

            print(quote_CE)
            print(quote_PE)

            if Symbol_index[i]=="SENSEX":
                sensex(quote_CE,quote_PE,strikes[j],xox)
            else:
                index_CE=instrument_NFO_df.index[instrument_NFO_df['tradingsymbol'] ==quote_CE].tolist()
                index_PE=instrument_NFO_df.index[instrument_NFO_df['tradingsymbol'] ==quote_PE].tolist()

                if len(index_CE)==0 or len(index_PE)==0:
                    token_not_present_in_data.append(quote_CE)
                    token_not_present_in_data.append(quote_PE)
                else:

                    atm_token_ce=instrument_NFO_df.loc[index_CE[0],"instrument_token"]
                    atm_token_pe=instrument_NFO_df.loc[index_PE[0],"instrument_token"]

                    ATM_Token_CE=atm_token_ce
                    ATM_Token_PE=atm_token_pe

                    print(ATM_Token_CE)
                    print(ATM_Token_PE)
                    print(quote_CE)
                    print(quote_PE)

                    import datetime

                    from_datetime = datetime.datetime.now() - datetime.timedelta(days=1)     # From last & days
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
                        df_CE.to_csv(xox+Symbol_index[i]+str(strikes[j])+"_CE.csv",index=False)

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
                        df_PE.to_csv(xox+Symbol_index[i]+str(strikes[j])+"_PE.csv",index=False)

            with open(xox+"Strikes_not_present.txt","w") as file:

                for item in token_not_present_in_data:
                    file.write(str(item)+ "\n")
            

def stock_Options():
    from datetime import datetime

    current_date = datetime.now()

    formatted_current_date = current_date.strftime('%d-%b-%Y')
    os.makedirs(path_stocks_path+formatted_current_date, exist_ok=True)
    path_stock_new=f'{path_stocks_path}{formatted_current_date}/'



    path_stock="D:/ashu/Finance/algo_trading/Option_chain_data/"
    today_date = datetime.today().strftime('%d%b%Y')
    today_date=today_date.upper()
    final_file=f"fo{today_date}bhav.csv"
    path_new=f"{path_stock}/{final_file}/"

    stock_data=pd.read_csv(path_new+final_file)
    stock_DF=stock_data[stock_data['INSTRUMENT'] == 'FUTSTK']
    stock_DF=stock_DF.reset_index(drop=True)
    unique_symbol=stock_DF["SYMBOL"].unique().tolist()

    file_path=path_main+"Stock_Expiry.txt"

    with open(file_path, 'r') as file:
        expiry_date=file.read()

    instrument_dump_NFO=kite.instruments("NFO")
    instrument_NFO_df=pd.DataFrame(instrument_dump_NFO)

    for i in range(len(unique_symbol)):

        token_not_present_in_data=[]
        file=Intraday_live_data.getoptionchain(unique_symbol[i],expiry_date)
        x=file["strikePrice"]
        strikes=x.tolist()

        modified_date=formatted_dates(expiry_date,1)

        Name_instrument=f"{unique_symbol[i]}_{expiry_date}"

        os.makedirs(path_stock_new+Name_instrument, exist_ok=True)

        xox_stock=f"{path_stock_new}{Name_instrument}/"

        for k in range(len(strikes)):
            quote_CE=unique_symbol[i]+modified_date+str(strikes[k])+"CE"
            quote_PE=unique_symbol[i]+modified_date+str(strikes[k])+"PE"

            print(quote_CE)
            print(quote_PE)

            index_CE=instrument_NFO_df.index[instrument_NFO_df['tradingsymbol'] ==quote_CE].tolist()
            index_PE=instrument_NFO_df.index[instrument_NFO_df['tradingsymbol'] ==quote_PE].tolist()

            if len(index_CE)==0 or len(index_PE)==0:
                token_not_present_in_data.append(quote_CE)
                token_not_present_in_data.append(quote_PE)
            else:
                atm_token_ce=instrument_NFO_df.loc[index_CE[0],"instrument_token"]
                atm_token_pe=instrument_NFO_df.loc[index_PE[0],"instrument_token"]

                ATM_Token_CE=atm_token_ce
                ATM_Token_PE=atm_token_pe

                print(ATM_Token_CE)
                print(ATM_Token_PE)
                print(quote_CE)
                print(quote_PE)

                import datetime

                from_datetime = datetime.datetime.now() - datetime.timedelta(days=1)     # From last & days
                to_datetime = datetime.datetime.now()
                interval = "5minute"
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
                    df_CE.to_csv(xox_stock+unique_symbol[i]+str(strikes[k])+"_CE.csv",index=False)

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
                    df_PE.to_csv(xox_stock+unique_symbol[i]+str(strikes[k])+"_PE.csv",index=False)

        with open(xox_stock+"Strikes_not_present.txt","w") as file:

            for item in token_not_present_in_data:
                file.write(str(item)+ "\n")



def Future_index():
    from datetime import datetime
    path_futures="D:/ashu/Finance/Daily_F_O_data/Futures/Index/"
    current_date = datetime.now()

    formatted_current_date = current_date.strftime('%d-%b-%Y')
    os.makedirs(path_futures+formatted_current_date, exist_ok=True)
    path_future_new=f'{path_futures}{formatted_current_date}/'


    path_index="D:/ashu/Finance/algo_trading/Option_chain_data/"
    today_date = datetime.today().strftime('%d%b%Y')
    today_date=today_date.upper()
    final_file=f"fo{today_date}bhav.csv"
    path_new=f"{path_index}/{final_file}/"

    index_data=pd.read_csv(path_new+final_file)
    Fut_Index=index_data[index_data['INSTRUMENT'] == 'FUTIDX']

    Fut_Index=Fut_Index.reset_index(drop=True)
    unique_df = Fut_Index.drop_duplicates(subset='SYMBOL', keep='first')
    unique_df=unique_df.reset_index(drop=True)

    rows=unique_df.shape[0]

    instrument_dump_NFO=kite.instruments("NFO")
    instrument_NFO_df=pd.DataFrame(instrument_dump_NFO)

    Instrument_list=[]

    for i in range(rows):
        symbol=unique_df.iloc[i]["SYMBOL"]
        current_year = datetime.now().year
        x=str(current_year)
        year=x[2:4]

        

        input_date_str = unique_df.iloc[i]["EXPIRY_DT"]

        # Convert the input string to a datetime object
        input_date = datetime.strptime(input_date_str, "%d-%b-%Y")

        today_date = datetime.now()

        month=input_date.strftime("%b").upper()
        Instrument_id=symbol+year+month+"FUT"
        Instrument_list.append(Instrument_id)

    print(Instrument_list)


    for k in range(len(Instrument_list)):

        index_fut=instrument_NFO_df.index[instrument_NFO_df['tradingsymbol'] ==Instrument_list[k]].tolist()
        token_id=instrument_NFO_df.loc[index_fut[0],"instrument_token"]

        import datetime

        from_datetime = datetime.datetime.now() - datetime.timedelta(days=1)     # From last & days
        to_datetime = datetime.datetime.now()
        interval = "5minute"
        content_Futures=kite.historical_data(token_id, from_datetime, to_datetime, interval, continuous=False, oi=True)

        Content_Futures=str(content_Futures)

        cleaned_contents_Futures = Content_Futures.replace("datetime.datetime", "").replace(", tzinfo=tzoffset(None, 19800)", "")

        data_Futures = ast.literal_eval(cleaned_contents_Futures)

        df_Futures = pd.DataFrame(data_Futures)

        if 'date' in df_Futures.columns:
            df_Futures['date'] = df_Futures['date'].apply(lambda x: pd.Timestamp(year=x[0], month=x[1], day=x[2], hour=x[3], minute=x[4]))
            df_Futures['Date'] = df_Futures['date'].dt.strftime('%Y-%m-%d')
            df_Futures['Time'] = df_Futures['date'].dt.strftime('%H:%M')
            df_Futures = df_Futures.drop(columns=['date'])
            df_Futures = df_Futures[['Date', 'Time', 'open', 'high', 'low', 'close','volume','oi']]

            df_Futures.to_csv(path_future_new+Instrument_list[k]+".csv",index=False)


def Futures_stock():

    from datetime import datetime
    path_futures="D:/ashu/Finance/Daily_F_O_data/Futures/Stocks/"
    current_date = datetime.now()

    formatted_current_date = current_date.strftime('%d-%b-%Y')
    os.makedirs(path_futures+formatted_current_date, exist_ok=True)
    path_future_new=f'{path_futures}{formatted_current_date}/'


    path_index="D:/ashu/Finance/algo_trading/Option_chain_data/"
    today_date = datetime.today().strftime('%d%b%Y')
    today_date=today_date.upper()
    final_file=f"fo{today_date}bhav.csv"
    path_new=f"{path_index}/{final_file}/"

    index_data=pd.read_csv(path_new+final_file)
    Fut_Index=index_data[index_data['INSTRUMENT'] == 'FUTSTK']
    Fut_Index=Fut_Index.reset_index(drop=True)
    unique_df = Fut_Index.drop_duplicates(subset='SYMBOL', keep='first')
    unique_df=unique_df.reset_index(drop=True)

    instrument_dump_NFO=kite.instruments("NFO")
    instrument_NFO_df=pd.DataFrame(instrument_dump_NFO)

    rows=unique_df.shape[0]

    Instrument_list=[]

    for i in range(rows):
        symbol=unique_df.iloc[i]["SYMBOL"]
        current_year = datetime.now().year
        x=str(current_year)
        year=x[2:4]

        

        input_date_str = unique_df.iloc[i]["EXPIRY_DT"]

        # Convert the input string to a datetime object
        input_date = datetime.strptime(input_date_str, "%d-%b-%Y")

        today_date = datetime.now()

        month=input_date.strftime("%b").upper()
        Instrument_id=symbol+year+month+"FUT"
        Instrument_list.append(Instrument_id)
    
    print(Instrument_list)

    for k in range(len(Instrument_list)):

        index_fut=instrument_NFO_df.index[instrument_NFO_df['tradingsymbol'] ==Instrument_list[k]].tolist()
        token_id=instrument_NFO_df.loc[index_fut[0],"instrument_token"]

        print(Instrument_list[k])
        print(token_id)

        import datetime

        from_datetime = datetime.datetime.now() - datetime.timedelta(days=1)     # From last & days
        to_datetime = datetime.datetime.now()
        interval = "5minute"
        content_Futures=kite.historical_data(token_id, from_datetime, to_datetime, interval, continuous=False, oi=True)

        Content_Futures=str(content_Futures)

        cleaned_contents_Futures = Content_Futures.replace("datetime.datetime", "").replace(", tzinfo=tzoffset(None, 19800)", "")

        data_Futures = ast.literal_eval(cleaned_contents_Futures)

        df_Futures = pd.DataFrame(data_Futures)

        if 'date' in df_Futures.columns:
            df_Futures['date'] = df_Futures['date'].apply(lambda x: pd.Timestamp(year=x[0], month=x[1], day=x[2], hour=x[3], minute=x[4]))
            df_Futures['Date'] = df_Futures['date'].dt.strftime('%Y-%m-%d')
            df_Futures['Time'] = df_Futures['date'].dt.strftime('%H:%M')
            df_Futures = df_Futures.drop(columns=['date'])
            df_Futures = df_Futures[['Date', 'Time', 'open', 'high', 'low', 'close','volume','oi']]

            df_Futures.to_csv(path_future_new+Instrument_list[k]+".csv",index=False)


def daily_bhav_copy_download():
    from datetime import datetime

    today_date = datetime.today().strftime('%d%b%Y')
    today_date=today_date.upper()
    final_file=f"fo{today_date}bhav.csv"


    import datetime
    current_month = datetime.datetime.now().strftime('%b')
    current_month = current_month.upper()
    current_year = datetime.datetime.now().strftime('%Y')

    # URL of the zip file
    zip_file_url = f"https://nsearchives.nseindia.com/content/historical/DERIVATIVES/{current_year}/{current_month}/{final_file}.zip"

    # Directory to save the downloaded file
    save_dir = "D:/ashu/Finance/algo_trading/Option_chain_data"


    folder_name = f"fo{today_date}bhav.csv"

    # Path to the folder
    folder_path = os.path.join(save_dir, folder_name)

    # Create the folder if it doesn't exist
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    save_dir=f"{save_dir}/{final_file}/"

    # Create the directory if it doesn't exist
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
    }

    # Path to save the zip file
    zip_file_path = os.path.join(save_dir, f"fo{today_date}bhav.csv.zip")

    # Send a GET request to the URL
    response = requests.get(zip_file_url, headers=headers)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Save the zip file to the specified location
        with open(zip_file_path, "wb") as f:
            f.write(response.content)

        # Open the saved zip file
        with zipfile.ZipFile(zip_file_path, 'r') as zip_file:
            # Extract all files from the zip file to the specified directory
            # Extract only files to the folder fo26APR2024bhav.csv
            for file in zip_file.namelist():
                filename = os.path.basename(file)
                if filename:  # Ensure it's not a directory
                    with zip_file.open(file) as source, open(os.path.join(save_dir, final_file), 'wb') as target:
                        target.write(source.read())

        print("Zip file downloaded and extracted successfully.")
    else:
        print("Failed to download the zip file.")

def Holidays_dates_determination():
    url = "https://www.nseindia.com/api/holiday-master?type=trading"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    }

    response = requests.get(url, headers=headers)
    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Print the content of the response
        content_output=response.text
    else:
        print("Failed to retrieve data from the URL:", response.status_code)

    content_output = json.loads(content_output)
    Holidays_date=[]
    Description_of_holidays=[]
    Week_on_holiday=[]


    for ii in range(len(content_output["FO"])):
        holiday_date=content_output["FO"][ii]['tradingDate']
        discrip=content_output["FO"][ii]['description']
        week=content_output["FO"][ii]['weekDay']

        Holidays_date.append(holiday_date)
        Description_of_holidays.append(discrip)
        Week_on_holiday.append(week)

    ####################### COMPUTING DATES FOR SUNDAY AND SATURDAY ###################################

    import datetime

    # Get the current year
    current_year = datetime.datetime.now().year

    # Initialize lists to store Saturdays and Sundays as strings
    saturdays = []
    sundays = []

    # Iterate over all the days in the current year
    for month in range(1, 13):
        for day in range(1, 32):
            try:
                # Try to create a datetime object for the current date
                date_obj = datetime.datetime(current_year, month, day)
                # Check if the day is Saturday or Sunday
                if date_obj.weekday() == 5:  # Saturday (Monday is 0, Sunday is 6)
                    saturdays.append(date_obj.strftime("%d-%m-%Y"))  # Format as string
                elif date_obj.weekday() == 6:  # Sunday
                    sundays.append(date_obj.strftime("%d-%m-%Y"))  # Format as string
            except ValueError:
                # If the day is invalid for the current month, ignore it
                pass

    Holidays_list=saturdays+sundays

    Holidays_date=Holidays_date+Holidays_list
    ####################### COMPUTING DATES FOR SUNDAY AND SATURDAY ###################################

    return Holidays_date,Description_of_holidays,Week_on_holiday

def Chainging_expiry_days():
    from datetime import datetime,timedelta
    today_date = datetime.today()
    formatted_todays_date = today_date.strftime('%d-%m-%Y')

    input_date = datetime.strptime(formatted_todays_date, "%d-%m-%Y")
    new_date = input_date + timedelta(days=1)
    New_Initial_date = new_date.strftime("%d-%b-%Y")

    file_path=path_main+"Stock_Expiry.txt"
    with open(file_path, 'r') as file:
        expiry_date=file.read()
        path_stock="D:/ashu/Finance/algo_trading/Option_chain_data"
        today_date = datetime.today().strftime('%d%b%Y')
        today_date=today_date.upper()
        final_file=f"fo{today_date}bhav.csv"
        path_new=f"{path_stock}/{final_file}/"

        if expiry_date==New_Initial_date:
            stock_data=pd.read_csv(path_new+final_file)
            stock_DF=stock_data[stock_data['INSTRUMENT'] == 'FUTSTK']
            stock_DF=stock_DF.reset_index(drop=True)
            New_expiry_date=stock_DF.loc[1,"EXPIRY_DT"]

            with open(file_path,'w') as file:
                file.write(New_expiry_date)

        else:
            print("Not Chainging Expiry Dates")

    # shutil.rmtree(path_new)


def prompt_Stocks_CP_data_collection(DAYS,symbol):
    path_closing_price="H:/My Drive/Daily_F_O_data/Daily_closing_price_data/"
    import datetime
    quote=str(symbol)
    print(f"Collecting closing price data for {quote}")
    df_old=pd.read_csv(path_closing_price+quote+".csv")

    token=kite.ltp("NSE:"+quote)
    instrument_token=token["NSE:"+quote]["instrument_token"]
    from_datetime = datetime.datetime.now() - datetime.timedelta(days=DAYS)     # From last & days historical limit 100 days for 5 mins
    to_datetime = datetime.datetime.now()

    interval="5minute"
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

        df['Time'] = pd.to_datetime(df['Time'])
        df = df[df['Time'] <= pd.to_datetime(filter_time)]
        df['Time'] = df['Time'].dt.strftime('%H:%M')

        if DAYS==1:
            df_new=pd.concat([df_old, df], axis=0)
            df_new.to_csv(path_closing_price+quote+".csv",index=False)
        else:
            df.to_csv(path_closing_price+quote+".csv",index=False)

def F_O_Stocks_closing_price():
    from datetime import datetime

    path="D:/ashu/Finance/algo_trading/Option_chain_data/"
    path_closing_price="H:/My Drive/Daily_F_O_data/Daily_closing_price_data/"

    today_date = datetime.today().strftime('%d%b%Y')
    today_date=today_date.upper()
    final_file=f"fo{today_date}bhav.csv"
    path_new=f"{path}/{final_file}/"

    stock_data=pd.read_csv(path_new+final_file)
    stock_DF=stock_data[stock_data['INSTRUMENT'] == 'FUTSTK']
    stock_DF=stock_DF.reset_index(drop=True)
    unique_symbol=stock_DF["SYMBOL"].unique().tolist()

    stock_data_old=pd.read_csv(path_main+"Old_list_F_O_stocks.csv")
    old_symbol_list=stock_data_old["SYMBOL"].unique().tolist()

    common_symbols = [symbol for symbol in unique_symbol if symbol in old_symbol_list]
    non_common_symbols = [symbol for symbol in unique_symbol if symbol not in old_symbol_list] + [symbol for symbol in old_symbol_list if symbol not in unique_symbol]

    instrument_dump_NSE=kite.instruments("NSE")
    instrument_NSE_df=pd.DataFrame(instrument_dump_NSE)

    for symbol in common_symbols:
        import datetime
        quote=str(symbol)
        print(f"Collecting closing price data for {quote}")
        df_old=pd.read_csv(path_closing_price+quote+".csv")

        index=instrument_NSE_df.index[instrument_NSE_df['tradingsymbol'] ==quote].tolist()

        instrument_token=instrument_NSE_df.loc[index[0],"instrument_token"]
        from_datetime = datetime.datetime.now() - datetime.timedelta(days=1)     # From last & days historical limit 100 days for 5 mins
        to_datetime = datetime.datetime.now()

        interval="5minute"
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

            df['Time'] = pd.to_datetime(df['Time'])
            df = df[df['Time'] <= pd.to_datetime(filter_time)]
            df['Time'] = df['Time'].dt.strftime('%H:%M')

            df_new=pd.concat([df_old, df], axis=0)
            df_new.to_csv(path_closing_price+quote+".csv",index=False)

    for non_common_quotes in non_common_symbols:
        print(f"The Non Common Symbols: {non_common_quotes}")
        if non_common_quotes in old_symbol_list:
            today_date = datetime.today()
            formatted_todays_date = today_date.strftime('%d-%b-%Y')

            prompt_Stocks_CP_data_collection(1,non_common_quotes)

            Index = stock_data_old.index[(stock_data_old['SYMBOL'] == non_common_quotes)].tolist()
            Index = Index[0]

            stock_data_old.loc[Index,"Status"]="Removed"
            stock_data_old.loc[Index,"Date of Update"]=str(formatted_todays_date)
            stock_data_old.to_csv(path_main+"Old_list_F_O_stocks.csv",index=False)

        elif non_common_quotes in unique_symbol:
            today_date = datetime.today()
            formatted_todays_date = today_date.strftime('%d-%b-%Y')

            prompt_Stocks_CP_data_collection(100,non_common_quotes)
            
            Instrument_list=stock_data_old["INSTRUMENT"].unique().tolist()
            Status_list=stock_data_old["Status"].unique().tolist()
            Todays_Date=stock_data_old["Date of Update"].unique().tolist()

            old_symbol_list.append(non_common_quotes)
            Instrument_list.append("FUTSTK")
            Status_list.append("Newely Added")
            Todays_Date.append(str(formatted_todays_date))

            dict_old_saving={"INSTRUMENT":Instrument_list,"SYMBOL":old_symbol_list,"Status":Status_list,"Date of Update":Todays_Date}
            df_old_saving=pd.DataFrame(dict_old_saving)
            df_old_saving.to_csv(path_main+"Old_list_F_O_stocks.csv",index=False)
        else:
            pass

def Sectors_indices_closing_price():
    path_closing_price="H:/My Drive/Daily_F_O_data/Daily_closing_price_data/"
    list_1_min=["NIFTY 50", "NIFTY BANK","NIFTY FIN SERVICE","NIFTY MID SELECT","SENSEX"]
    Sectors_list=["IT","FMCG","HEALTHCARE","PHARMA","AUTO","REALTY","METAL","MEDIA","OIL AND GAS","CONSR DURBL","PSU BANK","INDIA VIX"]

    instrument_dump_NSE=kite.instruments("NSE")
    instrument_NSE_df=pd.DataFrame(instrument_dump_NSE)

    instrument_dump_BSE=kite.instruments("BSE")
    instrument_BSE_df=pd.DataFrame(instrument_dump_BSE)

    for index_1_min in list_1_min:
        import datetime
        quote=str(index_1_min)
        print(f"Collecting closing price data for {quote}")
        df_old=pd.read_csv(path_closing_price+quote+".csv")

        if quote!="SENSEX":
            index=instrument_NSE_df.index[instrument_NSE_df['tradingsymbol'] ==quote].tolist()
            instrument_token=instrument_NSE_df.loc[index[0],"instrument_token"]

        elif quote=="SENSEX":
            index=instrument_BSE_df.index[instrument_BSE_df['tradingsymbol'] ==quote].tolist()
            instrument_token=instrument_BSE_df.loc[index[0],"instrument_token"]

        from_datetime = datetime.datetime.now() - datetime.timedelta(days=1)     # From last & days historical limit 60 days for 1 min
        to_datetime = datetime.datetime.now()

        interval="minute"
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

            df['Time'] = pd.to_datetime(df['Time'])
            df = df[df['Time'] <= pd.to_datetime(filter_time)]
            df['Time'] = df['Time'].dt.strftime('%H:%M')

            df_new=pd.concat([df_old, df], axis=0)
            df_new.to_csv(path_closing_price+quote+".csv",index=False)

    for sector in Sectors_list:
        import datetime
        if sector!="INDIA VIX":
            quote="NIFTY "+str(sector)
        elif sector=="INDIA VIX":
            quote=str(sector)
        else:
            pass

        print(f"Collecting closing price data for {quote}")
        df_old=pd.read_csv(path_closing_price+quote+".csv")

        index=instrument_NSE_df.index[instrument_NSE_df['tradingsymbol'] ==quote].tolist()
        instrument_token=instrument_NSE_df.loc[index[0],"instrument_token"]

        from_datetime = datetime.datetime.now() - datetime.timedelta(days=1)     # From last & days
        to_datetime = datetime.datetime.now()

        interval="5minute"
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

            df['Time'] = pd.to_datetime(df['Time'])
            df = df[df['Time'] <= pd.to_datetime(filter_time)]
            df['Time'] = df['Time'].dt.strftime('%H:%M')

            df_new=pd.concat([df_old, df], axis=0)
            df_new.to_csv(path_closing_price+quote+".csv",index=False)


def Pre_market_data_collection(path,content_read):
    Date=[]
    Time=[]
    Advance=[]
    Decline=[]
    Unchanged=[]
    Total_traded_value_in_cr=[]
    Total_market_cap=[]
    Total_traded_volume=[]

    #################################  Values in the data #############################
    Symbol=[]
    Opening_price_today=[]
    Closing_price=[]
    Change=[]
    Percent_change=[]
    Final_setteled_qty=[]
    Total_turn_over_in_cr=[]
    Market_cap_in_cr=[]
    Year_high=[]
    Year_low=[]

    Price=[]
    Buy_Qty=[]
    Sell_Qty=[]

    ATO_Buy_Qty=[]
    ATO_Sell_Qty=[]
    Total_traded_volume_eqilibrim_qty=[]
    Total_sell_Qty=[]
    Total_Buy_Qty=[]

    max_len=[]

    for i in range(len(content_read['data'])):
        date,time=content_read['timestamp'].split()
        Date.append(date)
        Time.append(time)
        Advance.append(content_read['advances'])
        Decline.append(content_read['declines'])
        Unchanged.append(content_read['unchanged'])
        Total_traded_value_in_cr.append(content_read['totalTradedValue'])
        Total_market_cap.append(content_read['totalmarketcap'])
        Total_traded_volume.append(content_read['totalTradedVolume'])

        Symbol.append(content_read['data'][i]['metadata']['symbol'])
        print(f"Collecting Preopen market for: {content_read['data'][i]['metadata']['symbol']}")
        Opening_price_today.append(content_read['data'][i]['metadata']['lastPrice'])
        Closing_price.append(content_read['data'][i]['metadata']['previousClose'])
        Change.append(round(content_read['data'][i]['metadata']['change'],2))
        Percent_change.append((round(content_read['data'][i]['metadata']['pChange'],2)))
        Final_setteled_qty.append((content_read['data'][i]['metadata']['finalQuantity']))
        Total_turn_over_in_cr.append(content_read['data'][i]['metadata']['totalTurnover'])
        Market_cap_in_cr.append(content_read['data'][i]['metadata']['marketCap'])
        Year_high.append(content_read['data'][i]['metadata']['yearHigh'])
        Year_low.append(content_read['data'][i]['metadata']['yearLow'])

        max_len_price=len(content_read['data'][i]['detail']['preOpenMarket']['preopen'])

        max_len.append(max_len_price)

        price_lists = [[] for _ in range(max_len_price)]
        buy_qty_lists = [[] for _ in range(max_len_price)]
        sell_qty_lists = [[] for _ in range(max_len_price)]

        for j in range(max_len_price):
            price_lists[j].append(content_read['data'][i]['detail']['preOpenMarket']['preopen'][j]["price"])
            buy_qty_lists[j].append(content_read['data'][i]['detail']['preOpenMarket']['preopen'][j]['buyQty'])
            sell_qty_lists[j].append(content_read['data'][i]['detail']['preOpenMarket']['preopen'][j]['sellQty'])

        Price.append(price_lists)
        Buy_Qty.append(buy_qty_lists)
        Sell_Qty.append(sell_qty_lists)

        ATO_Buy_Qty.append(content_read['data'][i]['detail']['preOpenMarket']['ato']['totalBuyQuantity'])
        ATO_Sell_Qty.append(content_read['data'][i]['detail']['preOpenMarket']['ato']['totalSellQuantity'])
        Total_traded_volume_eqilibrim_qty.append(content_read['data'][i]['detail']['preOpenMarket']['totalTradedVolume'])
        Total_sell_Qty.append(content_read['data'][i]['detail']['preOpenMarket']['totalSellQuantity'])
        Total_Buy_Qty.append(content_read['data'][i]['detail']['preOpenMarket']['totalBuyQuantity'])

    maximum_length_overall=max(max_len)


    Price_list={}
    Buy_list={}
    Sell_list={}

    for mm in range(maximum_length_overall):
        Price_list[f"Price_{mm}"]=[]
        Buy_list[f"Buy_{mm}"]=[]
        Sell_list[f"Sell_{mm}"]=[]

    for mmm in range(len(content_read['data'])):
        slice=max_len[mmm]
        residual=maximum_length_overall-slice
        for ii in range(slice):
            Price_list[f"Price_{ii}"].append(Price[mmm][ii][0])
            Buy_list[f"Buy_{ii}"].append(Buy_Qty[mmm][ii][0])
            Sell_list[f"Sell_{ii}"].append(Sell_Qty[mmm][ii][0])

        for kk in range(residual):
            Price_list[f"Price_{slice+kk}"].append(None)
            Buy_list[f"Buy_{slice+kk}"].append(None)
            Sell_list[f"Sell_{slice+kk}"].append(None)

    Price_df=pd.DataFrame(Price_list)
    Buy_df=pd.DataFrame(Buy_list)
    Sell_df=pd.DataFrame(Sell_list)

    Pre_market_data_1={"Date":Date,"Time":Time,"Advance":Advance,"Decline":Decline,"Unchanged":Unchanged,"Total Traded Value in Crores":Total_traded_value_in_cr,"Total Market Cap":Total_market_cap,"Total traded volume":Total_traded_volume
                    ,"Symbol":Symbol,"Opening Price Today":Opening_price_today,"Closing Price Previous Day":Closing_price,"Change":Change,"Percentage Change":Percent_change,"Final Setteled Quantity":Final_setteled_qty,
                    "Total Turnover in Crore":Total_turn_over_in_cr,"Market Captilization":Market_cap_in_cr,"Year High":Year_high,"Year Low":Year_low}

    Pre_market_data_3={"ATO Buy Qty":ATO_Buy_Qty,"ATO Sell Qty":ATO_Sell_Qty,"Equilibrium Volume":Total_traded_volume_eqilibrim_qty,"Total Sell Quantity":Total_sell_Qty,"Total Buy Quantity":Total_Buy_Qty}

    Pre_market_data_1_df=pd.DataFrame(Pre_market_data_1)
    Pre_market_data_3_df=pd.DataFrame(Pre_market_data_3)

    today_date = datetime.today()
    formatted_todays_date = today_date.strftime('%d-%b-%Y')

    Pre_market_df=pd.concat([Pre_market_data_1_df, Price_df,Buy_df,Sell_df,Pre_market_data_3_df], axis=1)
    Pre_market_df.to_csv(path+"Pre_Market_Data_"+str(formatted_todays_date)+".csv",index=False)

def Pre_market():
    path="H:/My Drive/Daily_F_O_data/Pre_Market_data/"
    url = "https://www.nseindia.com/api/market-data-pre-open?key=FO"

    # Set headers with API key
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    }
    while True:
        import time
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            content=response.json()
            print("Pre Market data Extracted")
            Pre_market_data_collection(path,content)
            break
        else:
            print("Failed to retrieve data:", response.status_code)

        time.sleep(1)






path_main="D:/ashu/Finance/algo_trading/Zerodha_GUI/Kite_Zerodha-main/Kite_Zerodha-main/"
path_index="D:/ashu/Finance/Daily_F_O_data/Options/Index/"
path_stocks_path="D:/ashu/Finance/Daily_F_O_data/Options/Stocks/"


###################################### CALLING KITE API CREDITIANLS ###############################################

with open(path_main+'kite_api_login_credentials.txt', 'r') as file:
    data_str = file.read()

data_dict=json.loads(data_str)
logging.basicConfig(level=logging.DEBUG)
kite = KiteConnect(api_key=data_dict['API_Key'])

Access_token=data_dict["Acess_token"]
kite.set_access_token(Access_token)


###################################### CALLING KITE API CREDITIANLS ###############################################

filter_time="15:30"


from datetime import datetime

today_date = datetime.today()
formatted_todays_date = today_date.strftime('%d-%m-%Y')
Holidays_list,Description_of_holidays,Week_on_holiday=Holidays_dates_determination()


if formatted_todays_date in Holidays_list:
    print("Today is holiday")
else:
    print("Today is not holiday")
    daily_bhav_copy_download()
    Options_index() 
    stock_Options()
    Future_index()
    Futures_stock()  
    Chainging_expiry_days()
    F_O_Stocks_closing_price()
    Sectors_indices_closing_price()
    Pre_market()

    Path_Options="D:/ashu/Finance/Daily_F_O_data/Options/"
    Path_Futures="D:/ashu/Finance/Daily_F_O_data/Futures/"

    with open(Path_Options+"Last_update_date.txt",'w') as file:
        today_date = datetime.today()
        formatted_todays_date = today_date.strftime('%d-%m-%Y')
        file.write(str(formatted_todays_date))

    with open(Path_Futures+"Last_update_date.txt",'w') as file:
        today_date = datetime.today()
        formatted_todays_date = today_date.strftime('%d-%m-%Y')
        file.write(str(formatted_todays_date))