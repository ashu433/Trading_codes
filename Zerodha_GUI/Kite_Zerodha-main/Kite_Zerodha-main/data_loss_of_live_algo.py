import pandas as pd
from kite_trade import *
from datetime import datetime,timedelta
import ast
import time
import numpy as np
import json

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

def writing_market_status(dict_name,text_file="Market_status.txt"):
    with open(Path_backtest_Report+text_file, 'w') as file:
        json.dump(dict_name, file)

def reading_market_status(text_file="Market_status.txt"):
    with open(Path_backtest_Report+text_file, 'r') as file:
        json_data = file.read()
        present_market_status= json.loads(json_data)

        return present_market_status

def ensure_nested_dict(main_dict, key):
    if key not in main_dict:
        main_dict[key] = {}


def Loading_in_Running_log(Strike,Right,order_type,Type):
    data=pd.read_csv(path_main+"Live_Running_Startjee.csv")
    Segment=data.loc[0,"Symbol"]
    expiry_date=data.loc[0,"Expiry Date"]
    Month_end=data.loc[0,"Month End"]
    content_enctoken=df.iloc[0,0]
    enctoken = content_enctoken
    kite = KiteApp(enctoken=enctoken)

    date_object = datetime.strptime(expiry_date, '%d-%b-%y')
    expiry_date = date_object.strftime('%d-%b-%Y')

    modified_date=formatted_dates(expiry_date,Month_end)
    if Right=="Call":
        quote=Segment+modified_date+str(Strike)+"CE"
    elif Right=="Put":
        quote=Segment+modified_date+str(Strike)+"PE"
    else:
        pass

    list_of_dicts = kite.orders()

    for i in range(len(list_of_dicts)):

        running_log=reading_market_status("Running_log.txt")
        if list_of_dicts[i]['tradingsymbol']==quote and list_of_dicts[i]['order_type']==order_type:
            Date_time=list_of_dicts[i]['order_timestamp']
            date, time = Date_time.split()
            Order_ID=list_of_dicts[i]['order_id']
            Status_present=list_of_dicts[i]['status']
            price=list_of_dicts[i]['average_price']
            Stop_loss=2*price

            if order_type=="SL":
                Strike=-Strike
                Stop_loss=price
            else:
                pass

            ensure_nested_dict(running_log, Strike)
            running_log[Strike]["Date"]=date
            running_log[Strike]["Time"]=time
            running_log[Strike]["Right"]=Right
            running_log[Strike]["Order ID"]=str(Order_ID)
            running_log[Strike]["Status"]=Status_present
            running_log[Strike]["Type"]=Type
            running_log[Strike]["Initial Price"]=price
            running_log[Strike]["Trailing SL"]=Stop_loss

            writing_market_status(running_log,"Running_log.txt")





path_main="D:/ashu/Finance/algo_trading/Zerodha_GUI/Kite_Zerodha-main/Kite_Zerodha-main/"
Path_backtest_Report="D:/ashu/Finance/algo_trading/Zerodha_GUI/Kite_Zerodha-main/Kite_Zerodha-main/Live_market_data_gathering/"
df=pd.read_csv(path_main+"Enctoke_Expiry_month_end_info.csv")
content_enctoken=df.iloc[0,0]
enctoken = content_enctoken
kite = KiteApp(enctoken=enctoken)


######################################  INITILIZATION PART ##########################################
Initilization=0
Input_strike=22700
right="Call"
# Order_type="LIMIT"
Type="Buy"

# Order_type="MARKET"
Order_type="SL"

Active_strike_list_Call=[22750,22700]
Active_strike_list_Put=[22100]
reversal_status=0
max_call_credit_spreads=2
max_put_credit_spreads=1
Market_trend="Trending Down"
######################################  INITILIZATION PART ############################################




market_status={}
market_status["Market Trend"]=Market_trend
market_status["Active Call Strikes"]=Active_strike_list_Call
market_status["Active Put Strikes"]=Active_strike_list_Put
market_status["Reversal status"]=reversal_status
market_status["Maximum call credit Spread"]=max_call_credit_spreads
market_status["Maximum put credit Spread"]=max_put_credit_spreads

with open(Path_backtest_Report+"Market_status.txt", 'w') as file:
    json.dump(market_status, file)

if Initilization==1:
    running_log={}
    writing_market_status(running_log,"Running_log.txt")
elif Initilization==0:
    Loading_in_Running_log(Input_strike,right,Order_type,Type)
else:
    pass