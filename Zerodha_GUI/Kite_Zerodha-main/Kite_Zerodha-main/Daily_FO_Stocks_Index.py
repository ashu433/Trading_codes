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

    atm_token_ce=kite.ltp("BFO:"+quote_CE)
    atm_token_pe=kite.ltp("BFO:"+quote_PE)
    if len(atm_token_ce)==0 or len(atm_token_pe)==0:
        token_not_present_in_data.append(quote_CE)
        token_not_present_in_data.append(quote_PE)
    else:
        ATM_Token_CE=atm_token_ce["BFO:"+quote_CE]['instrument_token']
        ATM_Token_PE=atm_token_pe["BFO:"+quote_PE]['instrument_token']

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
                atm_token_ce=kite.ltp("NFO:"+quote_CE)
                atm_token_pe=kite.ltp("NFO:"+quote_PE)
                if len(atm_token_ce)==0 or len(atm_token_pe)==0:
                    token_not_present_in_data.append(quote_CE)
                    token_not_present_in_data.append(quote_PE)
                else:
                    ATM_Token_CE=atm_token_ce["NFO:"+quote_CE]['instrument_token']
                    ATM_Token_PE=atm_token_pe["NFO:"+quote_PE]['instrument_token']

                    print(ATM_Token_CE)
                    print(ATM_Token_PE)
                    print(quote_CE)
                    print(quote_PE)

                    import datetime

                    from_datetime = datetime.datetime.now() - datetime.timedelta(days=3)     # From last & days
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

            atm_token_ce=kite.ltp("NFO:"+quote_CE)
            atm_token_pe=kite.ltp("NFO:"+quote_PE)

            if len(atm_token_ce)==0 or len(atm_token_pe)==0:
                token_not_present_in_data.append(quote_CE)
                token_not_present_in_data.append(quote_PE)
            else:
                ATM_Token_CE=atm_token_ce["NFO:"+quote_CE]['instrument_token']
                ATM_Token_PE=atm_token_pe["NFO:"+quote_PE]['instrument_token']

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

        token=kite.ltp("NFO:"+Instrument_list[k])
        token_id=token["NFO:"+Instrument_list[k]]['instrument_token']

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

        token=kite.ltp("NFO:"+Instrument_list[k])
        token_id=token["NFO:"+Instrument_list[k]]['instrument_token']

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







path_main="D:/ashu/Finance/algo_trading/Zerodha_GUI/Kite_Zerodha-main/Kite_Zerodha-main/"
path_index="D:/ashu/Finance/Daily_F_O_data/Options/Index/"
path_stocks_path="D:/ashu/Finance/Daily_F_O_data/Options/Stocks/"



df=pd.read_csv(path_main+"Enctoke_Expiry_month_end_info.csv")
content_enctoken=df.iloc[0,0]
enctoken = content_enctoken
kite = KiteApp(enctoken=enctoken)


Options_index() 
# stock_Options()
# Future_index()
# Futures_stock() 