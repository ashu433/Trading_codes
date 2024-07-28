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
import warnings
import re

warnings.filterwarnings("ignore")

############################################  MARKET RELATED FUNCTION ################################################################
def ensure_nested_dict(main_dict, key):
    if key not in main_dict:
        main_dict[key] = {}


def sleep_time_compute(target_time_str):
    import datetime
    target_time = datetime.datetime.strptime(target_time_str, "%H:%M").time()
    current_time = datetime.datetime.now().time()

    time_diff_seconds = (datetime.datetime.combine(datetime.date.today(), target_time) - datetime.datetime.combine(
        datetime.date.today(), current_time)).total_seconds()
    if time_diff_seconds < 0:
        time_diff_seconds += 24 * 60 * 60

    return time_diff_seconds


def limit_order_Sell(Quote, Size, price, Strike, Right):
    global order_info
    import time

    running_log = reading_market_status("Running_log.txt")

    while True:
        try:
            order = kite.place_order(variety=kite.VARIETY_REGULAR,
                                    exchange=kite.EXCHANGE_NFO,
                                    tradingsymbol=Quote,
                                    transaction_type=kite.TRANSACTION_TYPE_SELL,
                                    quantity=Size,
                                    product=kite.PRODUCT_NRML,
                                    order_type=kite.ORDER_TYPE_LIMIT,
                                    price=price,
                                    validity=kite.VALIDITY_DAY,
                                    disclosed_quantity=None,
                                    trigger_price=None,
                                    tag="TradeViaPython")
            x = kite.orders()
            l1 = len(x)
            Order_ID = x[l1 - 1]['order_id']
            Date_time = x[l1 - 1]['order_timestamp']
            Status_present = x[l1 - 1]['status']

            date_part = Date_time.date()
            time_part = Date_time.time() 
            date = date_part.isoformat()
            Time = time_part.isoformat() 

            Stop_Loss = 2 * price

            ensure_nested_dict(running_log, Strike)

            running_log[Strike]["Date"] = date
            running_log[Strike]["Time"] = Time
            running_log[Strike]["Right"] = Right
            running_log[Strike]["Order ID"] = str(Order_ID)
            running_log[Strike]["Status"] = Status_present
            running_log[Strike]["Type"] = "Sell"
            running_log[Strike]["Initial Price"] = price
            running_log[Strike]["Trailing SL"] = Stop_Loss
            running_log[Strike]["Trailing Status"]=0

            writing_market_status(running_log, "Running_log.txt")

            with open(Path_backtest_Report + 'Running_log_file.txt', 'a') as file:
                file.write(
                    f"Date: {date} Time: {Time} Strike: {Strike} Initiation Price: {price} type of Order: Limit Order Sell.\n")
            
            break


        except Exception as e:
            # Print the error message and wait for 1 second before retrying
            Error_statement=str(e)
            if "Markets are closed right now" not in Error_statement:
                print(f"Error: {e}")
                console_output_log_recording(f"Error: {e}")
                print("Retrying after 1 second for Modify SL order")
                console_output_log_recording("Retrying after 1 second for Modify SL order")
                time.sleep(1)
            elif "Markets are closed right now" in Error_statement:
                print("Market is closed right now")
                console_output_log_recording("Market is closed right now")
                break



def limit_order_buy(Quote, Size, price):
    global order_info
    import time

    order = kite.place_order(variety=kite.VARIETY_REGULAR,
                             exchange=kite.EXCHANGE_NFO,
                             tradingsymbol=Quote,
                             transaction_type=kite.TRANSACTION_TYPE_BUY,
                             quantity=Size,
                             product=kite.PRODUCT_NRML,
                             order_type=kite.ORDER_TYPE_LIMIT,
                             price=price,
                             validity=kite.VALIDITY_DAY,
                             disclosed_quantity=None,
                             trigger_price=None,
                             tag="TradeViaPython")

    ## Save the order info in the log list


def Market_order_Buy(Quote, Size, Strike, Right, Buy_type):
    global order_info
    import time

    running_log = reading_market_status("Running_log.txt")

    while True:
        try:
            order = kite.place_order(variety=kite.VARIETY_REGULAR,
                                    exchange=kite.EXCHANGE_NFO,
                                    tradingsymbol=Quote,
                                    transaction_type=kite.TRANSACTION_TYPE_BUY,
                                    quantity=Size,
                                    product=kite.PRODUCT_NRML,
                                    order_type=kite.ORDER_TYPE_MARKET,
                                    price=None,
                                    validity=None,
                                    disclosed_quantity=None,
                                    trigger_price=None,
                                    tag="TradeViaPython")

            x = kite.orders()
            l1 = len(x)
            Order_ID = x[l1 - 1]['order_id']
            Date_time = x[l1 - 1]['order_timestamp']
            Status_present = x[l1 - 1]['status']

            date_part = Date_time.date()
            time_part = Date_time.time() 
            date = date_part.isoformat()
            Time = time_part.isoformat() 

            price = x[l1 - 1]["average_price"]
            Stop_Loss = 0

            ensure_nested_dict(running_log, Strike)

            running_log[Strike]["Date"] = date
            running_log[Strike]["Time"] = Time
            running_log[Strike]["Right"] = Right
            running_log[Strike]["Order ID"] = str(Order_ID)
            running_log[Strike]["Status"] = Status_present
            running_log[Strike]["Type"] = Buy_type
            running_log[Strike]["Initial Price"] = price
            running_log[Strike]["Trailing SL"] = Stop_Loss

            writing_market_status(running_log, "Running_log.txt")

            with open(Path_backtest_Report + 'Running_log_file.txt', 'a') as file:
                file.write(
                    f"Date: {date} Time: {Time} Strike: {Strike} Market Price: {price} type of Order: Market Order Buy.\n")
            break

        except Exception as e:
            # Print the error message and wait for 1 second before retrying
            Error_statement=str(e)
            if "Markets are closed right now" not in Error_statement:
                print(f"Error: {e}")
                console_output_log_recording(f"Error: {e}")
                print("Retrying after 1 second for Modify SL order")
                console_output_log_recording("Retrying after 1 second for Modify SL order")
                time.sleep(1)
            elif "Markets are closed right now" in Error_statement:
                print("Market is closed right now")
                console_output_log_recording("Market is closed right now")
                break


def pause(duration=10):
    """Pause execution for the specified duration in seconds."""
    time.sleep(duration)


def Market_order_Sell(Quote, Size, Strike, Right, Sell_type,Last_trailing_time_sell="Normal"):
    global order_info
    import time

    running_log = reading_market_status("Running_log.txt")

    while True:
        try:
            order = kite.place_order(variety=kite.VARIETY_REGULAR,
                                    exchange=kite.EXCHANGE_NFO,
                                    tradingsymbol=Quote,
                                    transaction_type=kite.TRANSACTION_TYPE_SELL,
                                    quantity=Size,
                                    product=kite.PRODUCT_NRML,
                                    order_type=kite.ORDER_TYPE_MARKET,
                                    price=None,
                                    validity=None,
                                    disclosed_quantity=None,
                                    trigger_price=None,
                                    tag="TradeViaPython")

            x = kite.orders()
            l1 = len(x)
            Order_ID = x[l1 - 1]['order_id']
            Date_time = x[l1 - 1]['order_timestamp']
            Status_present = x[l1 - 1]['status']

            date_part = Date_time.date()
            time_part = Date_time.time() 
            date = date_part.isoformat()
            Time = time_part.isoformat() 

            price = x[l1 - 1]["average_price"]
            Stop_Loss = 0

            if Last_trailing_time_sell=="Normal":
                Strike = -Strike
                ensure_nested_dict(running_log, Strike)
                running_log[Strike]["Date"] = date
                running_log[Strike]["Time"] = Time
                running_log[Strike]["Right"] = Right
                running_log[Strike]["Order ID"] = str(Order_ID)
                running_log[Strike]["Status"] = Status_present
                running_log[Strike]["Type"] = Sell_type
                running_log[Strike]["Initial Price"] = price
                running_log[Strike]["Trailing SL"] = Stop_Loss

                writing_market_status(running_log, "Running_log.txt")

            elif Last_trailing_time_sell=="Sell Despiration":
                ensure_nested_dict(running_log, Strike)
                running_log[Strike]["Date"] = date
                running_log[Strike]["Time"] = Time
                running_log[Strike]["Right"] = Right
                running_log[Strike]["Order ID"] = str(Order_ID)
                running_log[Strike]["Status"] = Status_present
                running_log[Strike]["Type"] = "Sell"
                running_log[Strike]["Initial Price"] = price
                running_log[Strike]["Trailing SL"] = 2*price
                running_log[Strike]["Trailing Status"]=0

                writing_market_status(running_log, "Running_log.txt")
            else:
                pass

            with open(Path_backtest_Report + 'Running_log_file.txt', 'a') as file:
                file.write(
                    f"Date: {date} Time: {Time} Strike: {Strike} Market Price: {price} type of Order: Market Order Sell.\n")
            
            break
        except Exception as e:
            # Print the error message and wait for 1 second before retrying
            Error_statement=str(e)
            if "Markets are closed right now" not in Error_statement:
                print(f"Error: {e}")
                console_output_log_recording(f"Error: {e}")
                print("Retrying after 1 second for Modify SL order")
                console_output_log_recording("Retrying after 1 second for Modify SL order")
                time.sleep(1)
            elif "Markets are closed right now" in Error_statement:
                print("Market is closed right now")
                console_output_log_recording("Market is closed right now")
                break


def Modify_SL_Order(OID, Size, Price, type_of_modification, Order_Type, Strike):
    global order_info
    import time

    running_log = reading_market_status("Running_log.txt")

    while True:
        try:
            if Order_Type == "Limit":
                type_of_order = kite.ORDER_TYPE_LIMIT
                Triggering_price = None
            elif Order_Type == "SL Limit":
                type_of_order = kite.ORDER_TYPE_SL
                Triggering_price = Price - 0.05
            else:
                pass

            kite.modify_order(variety=kite.VARIETY_REGULAR,
                            order_id=OID,
                            parent_order_id=None,
                            quantity=Size,
                            price=Price,
                            order_type=type_of_order,
                            trigger_price=Triggering_price,
                            validity=kite.VALIDITY_DAY,
                            disclosed_quantity=None)

            if type_of_modification == "Trailing SL":
                running_log[str(Strike)]["Trailing SL"] = Price
                running_log[str(-Strike)]["Trailing SL"] = Price

            elif type_of_modification == "Initial Price":
                running_log[str(Strike)]["Initial Price"] = Price
                running_log[str(Strike)]["Trailing SL"] = 2*Price
            else:
                pass

            writing_market_status(running_log, "Running_log.txt")

            x = kite.orders()
            l1 = len(x)
            Date_time = x[l1 - 1]['order_timestamp']

            date_part = Date_time.date()
            time_part = Date_time.time() 
            date = date_part.isoformat()
            Time = time_part.isoformat() 

            with open(Path_backtest_Report + 'Running_log_file.txt', 'a') as file:
                file.write(
                    f"Date: {date} Time: {Time} Strike: {Strike} Price: {Price} type of modification {type_of_modification} and order type {Order_Type}.\n")
            break

        except Exception as e:
            # Print the error message and wait for 1 second before retrying
            Error_statement=str(e)
            if "Trigger price for stoploss buy orders cannot be above the upper circuit price" in Error_statement:
                match = re.search(r"below (\d+\.\d+)", Error_statement)
                price_extracted = match.group(1)
                print(f"The error statement due to SL placement : {Error_statement}")
                console_output_log_recording(f"The error statement due to SL placement : {Error_statement}")
                Price=price_extracted
                Price=float(Price)
                Price=Price-0.05
                running_log[str(Strike)]["Error in SL placement"]=1
                writing_market_status(running_log, "Running_log.txt")

                time.sleep(1)

            elif "Markets are closed right now" not in Error_statement:
                print(f"Error: {e}")
                console_output_log_recording(f"Error: {e}")
                print("Retrying after 1 second for Modify SL order")
                console_output_log_recording("Retrying after 1 second for Modify SL order")
                time.sleep(1)
            elif "Markets are closed right now" in Error_statement:
                print("Market is closed right now")
                console_output_log_recording("Market is closed right now")
                break


def SL_Initiate_order(Quote, Size, SL_price, SL_Trig_price, Strike, Right, morning_order_state=None):
    global order_info
    import time


    while True:
        running_log = reading_market_status("Running_log.txt")
        try:
            order = kite.place_order(variety=kite.VARIETY_REGULAR,
                                    exchange=kite.EXCHANGE_NFO,
                                    tradingsymbol=Quote,
                                    transaction_type=kite.TRANSACTION_TYPE_BUY,
                                    quantity=Size,
                                    product=kite.PRODUCT_NRML,
                                    order_type=kite.ORDER_TYPE_SL,
                                    price=SL_price,
                                    validity=kite.VALIDITY_DAY,
                                    disclosed_quantity=None,
                                    trigger_price=SL_Trig_price,
                                    tag="TradeViaPython")

            x = kite.orders()
            l1 = len(x)
            Order_ID = x[l1 - 1]['order_id']
            Date_time = x[l1 - 1]['order_timestamp']
            Status_present = "TRIGGER PENDING"

            date_part = Date_time.date()
            time_part = Date_time.time() 
            date = date_part.isoformat()
            Time = time_part.isoformat() 

            if morning_order_state == None:

                Strike = -Strike
                ensure_nested_dict(running_log, Strike)

                running_log[Strike]["Date"] = date
                running_log[Strike]["Time"] = Time
                running_log[Strike]["Right"] = Right
                running_log[Strike]["Order ID"] = str(Order_ID)
                running_log[Strike]["Status"] = Status_present
                running_log[Strike]["Type"] = "Buy"
                running_log[Strike]["Initial Price"] = SL_price
                running_log[Strike]["Trailing SL"] = SL_price

                writing_market_status(running_log, "Running_log.txt")

                with open(Path_backtest_Report + 'Running_log_file.txt', 'a') as file:
                    file.write(
                        f"Date: {date} Time: {Time} Strike: {Strike} Stop Loss Price: {SL_price} type of Order: Stop Loss Order.\n")

            elif morning_order_state == 1:
                Strike = -Strike
                running_log[str(Strike)]["Order ID"] = str(Order_ID)
                running_log[str(Strike)]["Trailing SL"] = SL_price

                Strike = -Strike

                running_log[str(Strike)]["Trailing SL"] = SL_price

                writing_market_status(running_log, "Running_log.txt")

                with open(Path_backtest_Report + 'Running_log_file.txt', 'a') as file:
                    file.write(
                        f"Date: {date} Time: {Time} Strike: {Strike} Stop Loss Price: {SL_price} type of Order: Stop Loss Order Modifiying morning order.\n")

            else:
                pass

            break

        except Exception as e:
            # Print the error message and wait for 1 second before retrying
            Error_statement=str(e)
            if "Trigger price for stoploss buy orders cannot be above the upper circuit price" in Error_statement:
                match = re.search(r"below (\d+\.\d+)", Error_statement)
                price_extracted = match.group(1)
                print(f"The error statement due to SL placement : {Error_statement}")
                console_output_log_recording(f"The error statement due to SL placement : {Error_statement}")
                SL_price=price_extracted
                SL_price=float(SL_price)
                SL_price=SL_price-0.05
                SL_Trig_price=SL_price-0.05
                running_log = reading_market_status("Running_log.txt")
                Strikes_list=list(running_log.keys())
                
                if str(-Strike) in Strikes_list:
                    running_log[str(-Strike)]["Error in SL placement"]=1
                    running_log[str(Strike)]["Trailing SL"]=SL_price
                    writing_market_status(running_log, "Running_log.txt")

                else:
                    running_log[str(Strike)]["Trailing SL"]=SL_price
                    Strike=-Strike
                    ensure_nested_dict(running_log, str(Strike))
                    running_log[str(Strike)]["Error in SL placement"]=1
                    writing_market_status(running_log, "Running_log.txt")

                time.sleep(1)

            elif "Markets are closed right now" not in Error_statement:
                print(f"Error: {e}")
                console_output_log_recording(f"Error: {e}")
                print("Retrying after 1 second for Modify SL order")
                console_output_log_recording("Retrying after 1 second for Modify SL order")
                time.sleep(1)
            elif "Markets are closed right now" in Error_statement:
                print("Market is closed right now")
                console_output_log_recording("Market is closed right now")
                break



def cancel_order(Order_ID,Strike):
    global order_info
    import time

    running_log = reading_market_status("Running_log.txt")

    while True:
        try:
            kite.cancel_order(variety=kite.VARIETY_REGULAR,
                            order_id=Order_ID,
                            parent_order_id=None)

            x = kite.orders()
            l1 = len(x)
            Date_time = x[l1 - 1]['order_timestamp']
            Status_present = x[l1 - 1]['status']

            date_part = Date_time.date()
            time_part = Date_time.time() 
            date = date_part.isoformat()
            Time = time_part.isoformat() 


            print(f"Cancelling SL order for strike {Strike}")
            console_output_log_recording(f"Cancelling SL order for strike {Strike}")

            break

        except Exception as e:
            # Print the error message and wait for 1 second before retrying
            Error_statement=str(e)
            if "Markets are closed right now" not in Error_statement:
                print(f"Error: {e}")
                console_output_log_recording(f"Error: {e}")
                print("Retrying after 1 second for Modify SL order")
                console_output_log_recording("Retrying after 1 second for Modify SL order")
                time.sleep(1)
            elif "Markets are closed right now" in Error_statement:
                print("Market is closed right now")
                console_output_log_recording("Market is closed right now")
                break


def Compute_token_Closing_price(Strike, Right, Time=5):
    global path_main
    from datetime import datetime
    import time

    present_market_status = reading_market_status()
    Current_market_segment = present_market_status["Segment"]
    Current_expiry_date = present_market_status["Expiry Day"]
    Current_month_end = present_market_status["Month End"]

    Segment = Current_market_segment
    expiry_date = Current_expiry_date
    Month_end = Current_month_end

    date_object = datetime.strptime(expiry_date, '%d-%b-%y')
    expiry_date = date_object.strftime('%d-%b-%Y')

    modified_date = formatted_dates(expiry_date, Month_end)
    # instrument_dump_NFO=kite.instruments("NFO")

    while True:
        try:
            instrument_dump_NFO=kite.instruments("NFO")
            break
        except Exception as e:
            Error_statement=str(e)
            if "Markets are closed right now" not in Error_statement:
                print(f"Error: {e}")
                console_output_log_recording(f"Error: {e}")
                print("Retrying after 1 second for Closing Price")
                console_output_log_recording("Retrying after 1 second for Closing Price")
                time.sleep(1)
            elif "Markets are closed right now" in Error_statement:
                print("Market is closed right now")
                console_output_log_recording("Market is closed right now")
                break

    instrument_NFO_df=pd.DataFrame(instrument_dump_NFO)

    if Right == "Call":
        quote_CE = Segment + modified_date + str(Strike) + "CE"
        index_CE=instrument_NFO_df.index[instrument_NFO_df['tradingsymbol'] ==quote_CE].tolist()
        ATM_Token_CE=instrument_NFO_df.loc[index_CE[0],"instrument_token"]

        import datetime

        from_datetime = datetime.datetime.now() - datetime.timedelta(days=1)  # From last & days
        to_datetime = datetime.datetime.now()

        if Time == 1:
            interval = "minute"
        elif Time == 5:
            interval = "5minute"
        else:
            pass

        # content_CE = kite.historical_data(ATM_Token_CE, from_datetime, to_datetime, interval, continuous=False, oi=True)

        while True:
            try:
                content_CE = kite.historical_data(ATM_Token_CE, from_datetime, to_datetime, interval, continuous=False, oi=True)
                break
            except Exception as e:
                Error_statement=str(e)
                if "Markets are closed right now" not in Error_statement:
                    print(f"Error: {e}")
                    console_output_log_recording(f"Error: {e}")
                    print("Retrying after 1 second for Closing Price")
                    console_output_log_recording("Retrying after 1 second for Closing Price")
                    time.sleep(1)
                elif "Markets are closed right now" in Error_statement:
                    print("Market is closed right now")
                    console_output_log_recording("Market is closed right now")
                    break

        length = len(content_CE)
        Content_CE = str(content_CE[length - 2])
        cleaned_contents_CE = Content_CE.replace("datetime.datetime", "").replace(", tzinfo=tzoffset(None, 19800)", "")
        data_CE = ast.literal_eval(cleaned_contents_CE)

        closing_price_CE = data_CE['close']

        return closing_price_CE, quote_CE

    elif Right == "Put":
        quote_PE = Segment + modified_date + str(Strike) + "PE"

        index_PE=instrument_NFO_df.index[instrument_NFO_df['tradingsymbol'] ==quote_PE].tolist()
        ATM_Token_PE=instrument_NFO_df.loc[index_PE[0],"instrument_token"]


        import datetime

        from_datetime = datetime.datetime.now() - datetime.timedelta(days=1)  # From last & days
        to_datetime = datetime.datetime.now()

        if Time == 1:
            interval = "minute"
        elif Time == 5:
            interval = "5minute"
        else:
            pass

        # content_PE = kite.historical_data(ATM_Token_PE, from_datetime, to_datetime, interval, continuous=False, oi=True)

        while True:
            try:
                content_PE = kite.historical_data(ATM_Token_PE, from_datetime, to_datetime, interval, continuous=False, oi=True)
                break
            except Exception as e:
                Error_statement=str(e)
                if "Markets are closed right now" not in Error_statement:
                    print(f"Error: {e}")
                    console_output_log_recording(f"Error: {e}")
                    print("Retrying after 1 second for Closing Price")
                    console_output_log_recording("Retrying after 1 second for Closing Price")
                    time.sleep(1)
                elif "Markets are closed right now" in Error_statement:
                    print("Market is closed right now")
                    console_output_log_recording("Market is closed right now")
                    break

        length = len(content_PE)
        Content_PE = str(content_PE[length - 2])
        cleaned_contents_PE = Content_PE.replace("datetime.datetime", "").replace(", tzinfo=tzoffset(None, 19800)", "")
        data_PE = ast.literal_eval(cleaned_contents_PE)

        closing_price_PE = data_PE['close']

        return closing_price_PE, quote_PE
    ############################################  MARKET RELATED FUNCTION ################################################################


def writing_market_status(dict_name, text_file="Market_status.txt"):
    with open(Path_backtest_Report + text_file, 'w') as file:
        json.dump(dict_name, file)


def reading_market_status(text_file="Market_status.txt"):
    with open(Path_backtest_Report + text_file, 'r') as file:
        json_data = file.read()
        present_market_status = json.loads(json_data)

        return present_market_status


def formatted_dates(expiry, month_end):
    mont_dict = {"Jan": 1, "Feb": 2, "Mar": 3, "Apr": 4, "May": 5, "Jun": 6, "Jul": 7, "Aug": 8, "Sep": 9, "Oct": 10,
                 "Nov": 11, "Dec": 12}

    if month_end == 0:

        parsed_date = datetime.strptime(expiry, '%d-%b-%Y')
        formatted_date = parsed_date.strftime('%y%m%d')

        char_list = list(formatted_date)

        month = expiry.split('-')[1]

        Letter_to_insert = str(mont_dict[month])
        length = len(formatted_date)
        first = formatted_date[0:2]
        last = formatted_date[length - 2:length]

        formatted_date = first + Letter_to_insert + last

        return formatted_date
    elif month_end == 1:

        parsed_date = datetime.strptime(expiry, '%d-%b-%Y')
        formatted_date = parsed_date.strftime('%Y%b').upper()
        formatted_date = formatted_date[2:]

        return formatted_date


def console_output_log_recording(content):
    current_time = datetime.now()
    current_datetime = datetime.today()
    current_date = current_datetime.date()
    formatted_date = current_date.strftime("%d-%m-%Y")

    current_time_str = current_time.strftime("%H:%M:%S")

    with open(Path_backtest_Report + 'Console_output_log_file.txt', 'a') as file:
        file.write(f"Date: {formatted_date} Time: {current_time_str}: {content}.\n")


def closest_time(current_time_str, time_list_obs):
    current_time = datetime.strptime(current_time_str, "%H:%M:%S")
    closest_time = None
    closest_time_difference = float('inf')

    for time_str in time_list_obs:
        time = datetime.strptime(time_str, "%H:%M")
        # Only consider times that are less than the current time
        if time < current_time:
            difference = abs((current_time - time).total_seconds())

            if difference < closest_time_difference:
                closest_time = time
                closest_time_difference = difference

    return closest_time.strftime("%H:%M")


def Status_compute(Order_ID_current):

    Log = kite.orders()
    order_id_to_find = str(Order_ID_current)

    # Initialize index variable
    index = None

    # Iterate through the list and find the index of the dictionary with the given order_id
    for i, item in enumerate(Log):
        if item.get('order_id') == order_id_to_find:
            index = i
            break

    Status_present = Log[index]['status']

    return Status_present


#################################################### ALGO Code ##########################################################

def Circuit_limit_price(Strike,Right):
    global path_main
    from datetime import datetime
    import time

    API_KEY = data_dict['API_Key']
    ACCESS_TOKEN = data_dict['Acess_token']

    present_market_status = reading_market_status()
    Current_market_segment = present_market_status["Segment"]
    Current_expiry_date = present_market_status["Expiry Day"]
    Current_month_end = present_market_status["Month End"]

    Segment = Current_market_segment
    expiry_date = Current_expiry_date
    Month_end = Current_month_end

    date_object = datetime.strptime(expiry_date, '%d-%b-%y')
    expiry_date = date_object.strftime('%d-%b-%Y')

    modified_date = formatted_dates(expiry_date, Month_end)

    if Right == "Call":
        quote= Segment + modified_date + str(Strike) + "CE"
    elif Right=="Put":
        quote= Segment + modified_date + str(Strike) + "PE"
    else:
        pass

    url = f"https://api.kite.trade/quote?i=NFO:{quote}"
    headers = {
        "X-Kite-Version": "3",
        "Authorization": f"token {API_KEY}:{ACCESS_TOKEN}"
    }

    logging.debug(f"Requesting URL: {url}")
    logging.debug(f"Headers: {headers}")

    response = requests.get(url, headers=headers)
    # logging.debug(f"Response: {response.status_code}, {response.text}")

    if response.status_code == 200:
        data = response.json()
        Upper_circuit_price=data['data'][f'NFO:{quote}']['upper_circuit_limit']
        return Upper_circuit_price
    else:
        print(f"Failed to get Upper circuit price data: {response.status_code}")
        console_output_log_recording(f"Failed to get Upper circuit price data: {response.status_code}")


def Order_execution_Check(Input_Strike_Call, Input_Strike_Put, quote_call_Hedges, quote_put_Hedges, quote_call,
                          quote_put, Input_Strike_Call_Hedge, Input_Strike_Put_Hedge):
    global Deployed_Size
    running_log = reading_market_status("Running_log.txt")

    if Input_Strike_Call is not None and Input_Strike_Put is not None:

        #################################### GETTING THE STOP LOSS AND THE ORDER ID OF THE INPUT STRIKES ########################################################

        Order_ID_Call = running_log[str(Input_Strike_Call)]["Order ID"]
        Order_ID_Put = running_log[str(Input_Strike_Put)]["Order ID"]

        #################################### GETTING THE STOP LOSS AND THE ORDER ID OF THE INPUT STRIKES ########################################################

        #################################### INITIATING THE WATCH TIME FOR THE ORDER EXECUTION ###########################################################
        current_time = datetime.now()

        current_time_str = current_time.strftime("%H:%M:%S")

        Initial_time = closest_time(current_time_str, time_list_1_min)
        index_time = time_list_1_min.index(Initial_time)
        New_time = time_list_1_min[index_time + 1]
        Run = 0
        #################################### INITIATING THE WATCH TIME FOR THE ORDER EXECUTION ###########################################################

        #################################### WATCHING AND TRAILING THE MODIFIED PRICE OF THE SOLD STRIKES #################################################
        while True:
            current_time = datetime.now()
            current_time_str = current_time.strftime("%H:%M:%S")

            running_log = reading_market_status("Running_log.txt")

            SL_Call = running_log[str(Input_Strike_Call)]["Trailing SL"]
            SL_Call_Trig = SL_Call - 0.05
            SL_Put = running_log[str(Input_Strike_Put)]["Trailing SL"]
            SL_Put_Trig = SL_Put - 0.05

            Status_call = Status_compute(Order_ID_Call)
            Status_put = Status_compute(Order_ID_Put)

            print(f"The Present run is {Run}")

            if Status_call == "COMPLETE" and Status_put == "COMPLETE" and current_time_str < New_time:

                print("All the Orders are succesfully complete")

                console_output_log_recording("All the Orders are succesfully complete")

                Market_order_Buy(quote_call_Hedges, Deployed_Size, Input_Strike_Call_Hedge, "Call", "Buy Hedge")
                Market_order_Buy(quote_put_Hedges, Deployed_Size, Input_Strike_Put_Hedge, "Put", "Buy Hedge")

                SL_Initiate_order(quote_call, Deployed_Size, SL_Call, SL_Call_Trig, Input_Strike_Call, "Call")
                SL_Initiate_order(quote_put, Deployed_Size, SL_Put, SL_Put_Trig, Input_Strike_Put, "Put")

                running_log = reading_market_status("Running_log.txt")
                running_log[str(Input_Strike_Call)]["Status"] = "COMPLETE"
                running_log[str(Input_Strike_Put)]["Status"] = "COMPLETE"

                running_log[str(-Input_Strike_Call)]["Required SL"]=SL_Call
                running_log[str(-Input_Strike_Call)]["Error in SL placement"]=0

                running_log[str(-Input_Strike_Put)]["Required SL"]=SL_Put
                running_log[str(-Input_Strike_Put)]["Error in SL placement"]=0

                writing_market_status(running_log, "Running_log.txt")

                break

            elif current_time_str >= New_time:
                Status_call = Status_compute(Order_ID_Call)
                Status_put = Status_compute(Order_ID_Put)

                if Status_call == "OPEN" and Status_put == "OPEN":

                    print(
                        f"Modifiying the Call Strike {Input_Strike_Call} and Modifiying the Put Strike {Input_Strike_Put}")
                    console_output_log_recording(
                        f"Modifiying the Call Strike {Input_Strike_Call} and Modifiying the Put Strike {Input_Strike_Put}")

                    pause()

                    Call_CP, quote_CE = Compute_token_Closing_price(Input_Strike_Call, "Call", 1)
                    Put_CP, quote_PE = Compute_token_Closing_price(Input_Strike_Put, "Put", 1)

                    Modify_SL_Order(Order_ID_Call, Deployed_Size, Call_CP, "Initial Price", "Limit", Input_Strike_Call)
                    Modify_SL_Order(Order_ID_Put, Deployed_Size, Put_CP, "Initial Price", "Limit", Input_Strike_Put)


                elif Status_call == "OPEN":

                    print(f"Modifiying the Call Strike {Input_Strike_Call} ")
                    console_output_log_recording(f"Modifiying the Call Strike {Input_Strike_Call}")
                    pause()

                    Call_CP, quote_CE = Compute_token_Closing_price(Input_Strike_Call, "Call", 1)
                    Modify_SL_Order(Order_ID_Call, Deployed_Size, Call_CP, "Initial Price", "Limit", Input_Strike_Call)

                elif Status_put == "OPEN":

                    print(f"Modifiying the Put Strike {Input_Strike_Put}")
                    console_output_log_recording(f"Modifiying the Put Strike {Input_Strike_Put}")
                    pause()

                    Put_CP, quote_PE = Compute_token_Closing_price(Input_Strike_Put, "Put", 1)
                    Modify_SL_Order(Order_ID_Put, Deployed_Size, Put_CP, "Initial Price", "Limit", Input_Strike_Put)
                    
                else:
                    pass

                index_time = time_list_1_min.index(New_time)
                New_time = time_list_1_min[index_time + 1]

            else:
                pass

            time.sleep(1)

            Run = Run + 1

        #################################### WATCHING AND TRAILING THE MODIFIED PRICE OF THE SOLD STRIKES ##################################################

    elif Input_Strike_Call is not None and Input_Strike_Put is None:

        #################################### GETTING THE STOP LOSS AND THE ORDER ID OF THE INPUT STRIKES ########################################################
        Order_ID_Call = running_log[str(Input_Strike_Call)]["Order ID"]

        Run = 0
        #################################### GETTING THE STOP LOSS AND THE ORDER ID OF THE INPUT STRIKES ########################################################

        #################################### INITIATING THE WATCH TIME FOR THE ORDER EXECUTION ###########################################################
        current_time = datetime.now()

        current_time_str = current_time.strftime("%H:%M:%S")

        Initial_time = closest_time(current_time_str, time_list_1_min)
        index_time = time_list_1_min.index(Initial_time)
        New_time = time_list_1_min[index_time + 1]
        #################################### INITIATING THE WATCH TIME FOR THE ORDER EXECUTION ###########################################################

        #################################### WATCHING AND TRAILING THE MODIFIED PRICE OF THE SOLD STRIKES #################################################
        while True:
            running_log = reading_market_status("Running_log.txt")
            current_time = datetime.now()
            current_time_str = current_time.strftime("%H:%M:%S")

            SL_Call = running_log[str(Input_Strike_Call)]["Trailing SL"]
            SL_Call_Trig = SL_Call - 0.05

            Status_call = Status_compute(Order_ID_Call)

            print(f"The Present run is {Run}")

            if Status_call == "COMPLETE" and current_time_str < New_time:

                print("Call Orders Execute Succesfully")

                console_output_log_recording("Call Orders Execute Succesfully")

                Market_order_Buy(quote_call_Hedges, Deployed_Size, Input_Strike_Call_Hedge, "Call", "Buy Hedges")
                SL_Initiate_order(quote_call, Deployed_Size, SL_Call, SL_Call_Trig, Input_Strike_Call, "Call")

                running_log = reading_market_status("Running_log.txt")
                running_log[str(Input_Strike_Call)]["Status"] = "COMPLETE"

                running_log[str(-Input_Strike_Call)]["Required SL"]=SL_Call
                running_log[str(-Input_Strike_Call)]["Error in SL placement"]=0

                writing_market_status(running_log, "Running_log.txt")
                break

            elif current_time_str >= New_time:
                Status_call = Status_compute(Order_ID_Call)

                if Status_call == "OPEN":

                    print(f"Modifiying the Call Strike {Input_Strike_Call}")
                    console_output_log_recording(f"Modifiying the Call Strike {Input_Strike_Call}")

                    pause()

                    Call_CP, quote_CE = Compute_token_Closing_price(Input_Strike_Call, "Call", 1)
                    Modify_SL_Order(Order_ID_Call, Deployed_Size, Call_CP, "Initial Price", "Limit", Input_Strike_Call)


                else:
                    pass

                index_time = time_list_1_min.index(New_time)
                New_time = time_list_1_min[index_time + 1]
                #################################### WATCHING AND TRAILING THE MODIFIED PRICE OF THE SOLD STRIKES #################################################
            else:
                pass

            time.sleep(1)

            Run = Run + 1



    elif Input_Strike_Put is not None and Input_Strike_Call is None:

        Order_ID_Put = running_log[str(Input_Strike_Put)]["Order ID"]

        current_time = datetime.now()

        current_time_str = current_time.strftime("%H:%M:%S")

        Initial_time = closest_time(current_time_str, time_list_1_min)
        index_time = time_list_1_min.index(Initial_time)
        New_time = time_list_1_min[index_time + 1]

        Run = 0

        while True:
            running_log = reading_market_status("Running_log.txt")
            current_time = datetime.now()

            current_time_str = current_time.strftime("%H:%M:%S")

            SL_Put = running_log[str(Input_Strike_Put)]["Trailing SL"]
            SL_Put_Trig = SL_Put - 0.05

            Status_put = Status_compute(Order_ID_Put)

            print(f"The Present run is {Run}")

            if Status_put == "COMPLETE" and current_time_str < New_time:

                print("Put Orders Execute Succesfully")
                console_output_log_recording("Put Orders Execute Succesfully")

                Market_order_Buy(quote_put_Hedges, Deployed_Size, Input_Strike_Put_Hedge, "Put", "Buy Hedges")
                SL_Initiate_order(quote_put, Deployed_Size, SL_Put, SL_Put_Trig, Input_Strike_Put, "Put")

                running_log = reading_market_status("Running_log.txt")
                running_log[str(Input_Strike_Put)]["Status"] = "COMPLETE"

                running_log[str(-Input_Strike_Put)]["Required SL"]=SL_Put
                running_log[str(-Input_Strike_Put)]["Error in SL placement"]=0

                writing_market_status(running_log, "Running_log.txt")

                break
            elif current_time_str >= New_time:
                Status_put = Status_compute(Order_ID_Put)

                if Status_put == "OPEN":

                    print(f"Modifiying the Put Strike {Input_Strike_Put}")
                    console_output_log_recording(f"Modifiying the Put Strike {Input_Strike_Put}")

                    pause()

                    Put_CP, quote_PE = Compute_token_Closing_price(Input_Strike_Put, "Put", 1)
                    Modify_SL_Order(Order_ID_Put, Deployed_Size, Put_CP, "Initial Price", "Limit", Input_Strike_Put)

                else:
                    pass

                index_time = time_list_1_min.index(New_time)
                New_time = time_list_1_min[index_time + 1]

            else:
                pass

            time.sleep(1)

            Run = Run + 1

    else:
        pass

def Last_5_mins_update():
    global Deployed_Size

    while True:
        current_time = datetime.now().strftime("%H:%M:%S")

        if current_time<=Market_close_time:
            print(f"Running Final Evaluvation of the orders at time {current_time}")

            running_log = reading_market_status("Running_log.txt")

            present_market_status = reading_market_status()

            Market_Trend = present_market_status['Market Trend']
            Active_strike_list_Call = present_market_status["Active Call Strikes"]
            Active_strike_list_Put = present_market_status["Active Put Strikes"]

            reversal_status = present_market_status["Reversal status"]
            max_call_credit_spreads = present_market_status["Maximum call credit Spread"]
            max_put_credit_spreads = present_market_status["Maximum put credit Spread"]

            if Market_Trend == "Neutral":
                CE_stk = Active_strike_list_Call[0]
                PE_stk = Active_strike_list_Put[0]

                OID_Call = running_log[str(-CE_stk)]["Order ID"]
                OID_Put = running_log[str(-PE_stk)]["Order ID"]

                Status_call = Status_compute(OID_Call)
                Status_put = Status_compute(OID_Put)

                if Status_call == "TRIGGER PENDING" and Status_put == "TRIGGER PENDING":
                    pass
                elif Status_call == "COMPLETE":
                    print(f"SL hit on the Call Strike {CE_stk} now Market Trend is Bullish")
                    console_output_log_recording(f"SL hit on the Call Strike {CE_stk} now Market Trend is Bullish")

                    running_log[str(-CE_stk)]["Status"] = "COMPLETE"
                    writing_market_status(running_log, "Running_log.txt")

                    present_market_status['Market Trend'] = "Trending Up"
                    writing_market_status(present_market_status)

                    CE_Hedge = CE_stk + hedges_distance
                    CE_Hedge_CP, QE_CE_Hedge = Compute_token_Closing_price(CE_Hedge, "Call")
                    Market_order_Sell(QE_CE_Hedge, Deployed_Size, CE_Hedge, "Call", "Hedge Sell")

                    print("Adding new Strikes through Market orders")
                    console_output_log_recording("Adding new Strikes through Market orders")
                    Active_strike_list_Call, Active_strike_list_Put = New_order_Placement(Active_strike_list_Call,Active_strike_list_Put,"Market")

                    print(
                        f"New Strikes list for Call {Active_strike_list_Call} and New Strikes list for put {Active_strike_list_Put}")
                    console_output_log_recording(
                        f"New Strikes list for Call {Active_strike_list_Call} and New Strikes list for put {Active_strike_list_Put}")
                    
                elif Status_put == "COMPLETE":
                    print(f"SL hit on the Put Strike {PE_stk} now Market Trend is Bearish")
                    console_output_log_recording(f"SL hit on the Put Strike {PE_stk} now Market Trend is Bearish")

                    running_log[str(-PE_stk)]["Status"] = "COMPLETE"
                    writing_market_status(running_log, "Running_log.txt")

                    present_market_status['Market Trend'] = "Trending Down"
                    writing_market_status(present_market_status)

                    PE_Hedge = PE_stk - hedges_distance

                    PE_Hedge_CP, QE_PE_Hedge = Compute_token_Closing_price(PE_Hedge, "Put")
                    Market_order_Sell(QE_PE_Hedge, Deployed_Size, PE_Hedge, "Put", "Hedge Sell")

                    print("Adding new Strikes through Market orders")
                    console_output_log_recording("Adding new Strikes through Market orders")
                    Active_strike_list_Call, Active_strike_list_Put = New_order_Placement(Active_strike_list_Call,Active_strike_list_Put,"Market")

                    print(
                        f"New Strikes list for Call {Active_strike_list_Call} and New Strikes list for put {Active_strike_list_Put}")
                    console_output_log_recording(
                        f"New Strikes list for Call {Active_strike_list_Call} and New Strikes list for put {Active_strike_list_Put}")
                else:
                    pass
                
            elif Market_Trend == "Trending Up":

                print(f"Present market trend is {Market_Trend}")

                if len(Active_strike_list_Put) != 0:

                    for i in range(len(Active_strike_list_Put)):
                        PE_stk = Active_strike_list_Put[i]

                        OID_Put = running_log[str(-PE_stk)]["Order ID"]

                        print(f"OID : {OID_Put} strike: {-PE_stk}")
                        Status_put = Status_compute(OID_Put)

                        if Status_put == "TRIGGER PENDING":
                            pass

                        elif Status_put == "COMPLETE":

                            present_market_status["Reversal status"] = 1

                            print(f"SL hit for strike {PE_stk} on put side the market reverses the trend")
                            console_output_log_recording(f"SL hit for strike {PE_stk} on put side the market reverses the trend")

                            running_log[str(-PE_stk)]["Status"] = "COMPLETE"
                            writing_market_status(running_log, "Running_log.txt")

                            Active_strike_list_Put.remove(PE_stk)
                            present_market_status["Active Put Strikes"] = Active_strike_list_Put
                            writing_market_status(present_market_status)

                            print(f"The new Active strike Put list is {Active_strike_list_Put}")
                            console_output_log_recording(f"The new Active strike Put list is {Active_strike_list_Put}")
                            PE_stk_Hedges = PE_stk - hedges_distance

                            PE_Hedge_CP, QE_PE_Hedge = Compute_token_Closing_price(PE_stk_Hedges, "Put")
                            Market_order_Sell(QE_PE_Hedge, Deployed_Size, PE_stk_Hedges, "Put", "Hedge Sell")

                        else:
                            pass
                else:
                    pass

                if len(Active_strike_list_Call) != 0:
                    CE_stk = Active_strike_list_Call[0]
                    OID_Call = running_log[str(-CE_stk)]["Order ID"]
                    Status_call = Status_compute(OID_Call)

                    if Status_call == "TRIGGER PENDING":
                        pass
                    elif Status_call == "COMPLETE":
                        print(
                            f"SL hit on call Strike {CE_stk} the market continues in the same trend selling Additional Strikes")
                        console_output_log_recording(
                            f"SL hit on call Strike {CE_stk} the market continues in the same trend selling Additional Strikes")

                        running_log[str(-CE_stk)]["Status"] = "COMPLETE"
                        writing_market_status(running_log, "Running_log.txt")

                        Length_put = len(Active_strike_list_Put)
                        CE_stk_Hedges = CE_stk + hedges_distance

                        CE_Hedge_CP, QE_CE_Hedge = Compute_token_Closing_price(CE_stk_Hedges, "Call")
                        Market_order_Sell(QE_CE_Hedge, Deployed_Size, CE_stk_Hedges, "Call", "Hedge Sell")

                        if max_put_credit_spreads >= max_credit_spreads or reversal_status == 1:
                            Active_strike_list_Call.remove(CE_stk)
                            present_market_status["Active Call Strikes"] = Active_strike_list_Call
                            writing_market_status(present_market_status)

                            print("Maximum Credit limit reached can't sell more strikes")
                            console_output_log_recording("Maximum Credit limit reached can't sell more strikes")
                        elif max_put_credit_spreads < max_credit_spreads and reversal_status == 0:
                            print("Adding new Strikes through Market orders")
                            console_output_log_recording("Adding new Strikes through Market orders")
                            Active_strike_list_Call, Active_strike_list_Put = New_order_Placement(Active_strike_list_Call,Active_strike_list_Put,"Market")
                            print(
                                f"New Strikes list for Call {Active_strike_list_Call} and New Strikes list for put {Active_strike_list_Put}")
                            console_output_log_recording(
                                f"New Strikes list for Call {Active_strike_list_Call} and New Strikes list for put {Active_strike_list_Put}")
                        else:
                            pass
                    else:
                        pass

                else:
                    pass

            elif Market_Trend == "Trending Down":

                if len(Active_strike_list_Call) != 0:
                    for i in range(len(Active_strike_list_Call)):
                        CE_stk = Active_strike_list_Call[i]
                        OID_Call = running_log[str(-CE_stk)]["Order ID"]
                        Status_call = Status_compute(OID_Call)

                        if Status_call == "TRIGGER PENDING":
                            pass
                        elif Status_call == "COMPLETE":
                            present_market_status["Reversal status"] = 1

                            print(f"SL hit for strike {CE_stk} on call side the market reverses the trend")
                            console_output_log_recording(
                                f"SL hit for strike {CE_stk} on call side the market reverses the trend")

                            running_log[str(-CE_stk)]["Status"] = "COMPLETE"
                            writing_market_status(running_log, "Running_log.txt")

                            Active_strike_list_Call.remove(CE_stk)
                            present_market_status["Active Call Strikes"] = Active_strike_list_Call
                            writing_market_status(present_market_status)

                            print(f"The new Active strike Call list is {Active_strike_list_Call}")
                            console_output_log_recording(f"The new Active strike Call list is {Active_strike_list_Call}")

                            CE_stk_Hedges = CE_stk + hedges_distance

                            CE_Hedge_CP, QE_CE_Hedge = Compute_token_Closing_price(CE_stk_Hedges, "Call")
                            Market_order_Sell(QE_CE_Hedge, Deployed_Size, CE_stk_Hedges, "Call", "Hedge Sell")
                        else:
                            pass

                else:
                    pass

                if len(Active_strike_list_Put) != 0:
                    PE_stk = Active_strike_list_Put[0]
                    OID_Put = running_log[str(-PE_stk)]["Order ID"]
                    Status_put = Status_compute(OID_Put)

                    if Status_put == "TRIGGER PENDING":
                        pass

                    elif Status_put == "COMPLETE":
                        print(f"SL hit on put Strike {PE_stk} the market continues in the same trend selling Additional Strikes")
                        console_output_log_recording(f"SL hit on put Strike {PE_stk} the market continues in the same trend selling Additional Strikes")

                        running_log[str(-PE_stk)]["Status"] = "COMPLETE"
                        writing_market_status(running_log, "Running_log.txt")

                        Length_call = len(Active_strike_list_Call)
                        PE_stk_Hedges = PE_stk - hedges_distance

                        PE_Hedge_CP, QE_PE_Hedge = Compute_token_Closing_price(PE_stk_Hedges, "Put")
                        Market_order_Sell(QE_PE_Hedge, Deployed_Size, PE_stk_Hedges, "Put", "Hedge Sell")

                        if max_call_credit_spreads >= max_credit_spreads or reversal_status == 1:

                            Active_strike_list_Put.remove(PE_stk)
                            present_market_status["Active Put Strikes"] = Active_strike_list_Put
                            writing_market_status(present_market_status)

                            print("Maximum Credit limit reached can't sell more strikes")
                            console_output_log_recording("Maximum Credit limit reached can't sell more strikes")

                        elif max_call_credit_spreads < max_credit_spreads and reversal_status == 0:
                            print("Adding new Strikes")
                            console_output_log_recording("Adding new Strikes")
                            Active_strike_list_Call, Active_strike_list_Put = New_order_Placement(Active_strike_list_Call,Active_strike_list_Put,"Market")
                            print(f"New Strikes list for Call {Active_strike_list_Call} and New Strikes list for put {Active_strike_list_Put}")
                            console_output_log_recording(f"New Strikes list for Call {Active_strike_list_Call} and New Strikes list for put {Active_strike_list_Put}")
                        else:
                            pass

                    else:
                        pass
                else:
                    pass

            else:
                pass
        else:
            print("Closing for the day")
            break

        time.sleep(1)

 
def Checking_distance_from_spot():
    global Deployed_Size
    import time

    present_market_status = reading_market_status()
    Market_Trend = present_market_status['Market Trend']
    Active_strike_list_Call = present_market_status["Active Call Strikes"]
    Active_strike_list_Put = present_market_status["Active Put Strikes"]

    while True:
        try:
            Nifty = kite.ltp(["NSE:NIFTY 50"])
            Nifty_Spot_price = Nifty['NSE:NIFTY 50']['last_price']
            break
        except Exception as e:
            Error_statement=str(e)
            if "Markets are closed right now" not in Error_statement:
                print(f"Error: {e}")
                console_output_log_recording(f"Error: {e}")
                print("Retrying after 1 second for Closing Price")
                console_output_log_recording("Retrying after 1 second for Closing Price")
                time.sleep(1)
            elif "Markets are closed right now" in Error_statement:
                print("Market is closed right now")
                console_output_log_recording("Market is closed right now")
                break

    ATM_Strike=round(Nifty_Spot_price/strikes_distance)*strikes_distance

    print(f"ATM Strike is: {ATM_Strike}")

    if Market_Trend=="Neutral":

        if len(Active_strike_list_Call) != 0:
            CE_stk = Active_strike_list_Call[0]
            difference_call=abs(CE_stk-ATM_Strike)

            if difference_call<strikes_distance:

                print(f"Difference in the call strike from spot: {difference_call}")
                console_output_log_recording(f"Difference in the call strike from spot: {difference_call}")
                            
                CP_Call, qte_call_despiration = Compute_token_Closing_price(CE_stk, "Call")
                CE_stk_hedge=CE_stk+hedges_distance
                CP_Call_hedge, qte_call_hedge_despiration = Compute_token_Closing_price(CE_stk_hedge, "Call")

                Market_order_Buy(qte_call_despiration, Deployed_Size, CE_stk, "Call", "Buy Despiration")
                Active_strike_list_Call.remove(CE_stk)
                present_market_status["Active Call Strikes"] = Active_strike_list_Call
                writing_market_status(present_market_status)
                
                running_log = reading_market_status("Running_log.txt")
                running_log[str(-CE_stk)]["Status"] = "COMPLETE"
                writing_market_status(running_log, "Running_log.txt")

                Market_order_Sell(qte_call_hedge_despiration, Deployed_Size, CE_stk_hedge, "Call", "Hedge Sell Despiration")
                OID_Call = running_log[str(-CE_stk)]["Order ID"]
                pause()
                cancel_order(OID_Call,CE_stk)

            else:
                pass

        else:
            pass

        if len(Active_strike_list_Put) != 0:
            PE_stk = Active_strike_list_Put[0]
            difference_put=abs(PE_stk-ATM_Strike)

            if difference_put<strikes_distance:

                print(f"Difference in the put strike from spot: {difference_put}")
                console_output_log_recording(f"Difference in the put strike from spot: {difference_put}")

                CP_Put, qte_put_despiration = Compute_token_Closing_price(PE_stk, "Put")
                PE_stk_hedge=PE_stk-hedges_distance
                CP_Put_hedge, qte_put_hedge_despiration = Compute_token_Closing_price(PE_stk_hedge, "Put")

                Market_order_Buy(qte_put_despiration, Deployed_Size, PE_stk, "Put", "Buy Despiration")
                Active_strike_list_Put.remove(PE_stk)
                present_market_status["Active Put Strikes"] = Active_strike_list_Put
                writing_market_status(present_market_status)

                running_log = reading_market_status("Running_log.txt")
                running_log[str(-PE_stk)]["Status"] = "COMPLETE"
                writing_market_status(running_log, "Running_log.txt")

                Market_order_Sell(qte_put_hedge_despiration, Deployed_Size, PE_stk_hedge, "Put", "Hedge Sell Despiration")
                OID_Put = running_log[str(-PE_stk)]["Order ID"]
                pause()
                cancel_order(OID_Put,PE_stk)
            else:
                pass
        else:
            pass


    elif Market_Trend=="Trending Up":
        if len(Active_strike_list_Put) != 0:
            for i in range(len(Active_strike_list_Put)):
                PE_stk = Active_strike_list_Put[i]
                difference_put=abs(PE_stk-ATM_Strike)

                if difference_put<strikes_distance:
                    print(f"Difference in the put strike from spot: {difference_put}")
                    console_output_log_recording(f"Difference in the put strike from spot: {difference_put}")

                    CP_Put, qte_put_despiration = Compute_token_Closing_price(PE_stk, "Put")
                    PE_stk_hedge=PE_stk-hedges_distance
                    CP_Put_hedge, qte_put_hedge_despiration = Compute_token_Closing_price(PE_stk_hedge, "Put")

                    Market_order_Buy(qte_put_despiration, Deployed_Size, PE_stk, "Put", "Buy Despiration")
                    Active_strike_list_Put.remove(PE_stk)
                    present_market_status["Active Put Strikes"] = Active_strike_list_Put
                    writing_market_status(present_market_status)

                    running_log = reading_market_status("Running_log.txt")
                    running_log[str(-PE_stk)]["Status"] = "COMPLETE"
                    writing_market_status(running_log, "Running_log.txt")

                    Market_order_Sell(qte_put_hedge_despiration, Deployed_Size, PE_stk_hedge, "Put", "Hedge Sell Despiration")
                    OID_Put = running_log[str(-PE_stk)]["Order ID"]
                    cancel_order(OID_Put,PE_stk)

                else:
                    pass
        else:
            pass

        if len(Active_strike_list_Call) != 0:
            CE_stk = Active_strike_list_Call[0]

            difference_call=abs(CE_stk-ATM_Strike)

            if difference_call<strikes_distance:

                print(f"Difference in the call strike from spot: {difference_call}")
                console_output_log_recording(f"Difference in the call strike from spot: {difference_call}")
                            
                CP_Call, qte_call_despiration = Compute_token_Closing_price(CE_stk, "Call")
                CE_stk_hedge=CE_stk+hedges_distance
                CP_Call_hedge, qte_call_hedge_despiration = Compute_token_Closing_price(CE_stk_hedge, "Call")

                Market_order_Buy(qte_call_despiration, Deployed_Size, CE_stk, "Call", "Buy Despiration")
                Active_strike_list_Call.remove(CE_stk)
                present_market_status["Active Call Strikes"] = Active_strike_list_Call
                writing_market_status(present_market_status)
                
                running_log = reading_market_status("Running_log.txt")
                running_log[str(-CE_stk)]["Status"] = "COMPLETE"
                writing_market_status(running_log, "Running_log.txt")

                Market_order_Sell(qte_call_hedge_despiration, Deployed_Size, CE_stk_hedge, "Call", "Hedge Sell Despiration")
                OID_Call = running_log[str(-CE_stk)]["Order ID"]
                cancel_order(OID_Call,CE_stk)

            else:
                pass


    elif Market_Trend=="Trending Down":
        if len(Active_strike_list_Call) != 0:
            for i in range(len(Active_strike_list_Call)):
                CE_stk = Active_strike_list_Call[i]

                difference_call=abs(CE_stk-ATM_Strike)

                if difference_call<strikes_distance:

                    print(f"Difference in the call strike from spot: {difference_call}")
                    console_output_log_recording(f"Difference in the call strike from spot: {difference_call}")

                    CP_Call, qte_call_despiration = Compute_token_Closing_price(CE_stk, "Call")
                    CE_stk_hedge=CE_stk+hedges_distance
                    CP_Call_hedge, qte_call_hedge_despiration = Compute_token_Closing_price(CE_stk_hedge, "Call")

                    Market_order_Buy(qte_call_despiration, Deployed_Size, CE_stk, "Call", "Buy Despiration")
                    Active_strike_list_Call.remove(CE_stk)
                    present_market_status["Active Call Strikes"] = Active_strike_list_Call
                    writing_market_status(present_market_status)
                    
                    running_log = reading_market_status("Running_log.txt")
                    running_log[str(-CE_stk)]["Status"] = "COMPLETE"
                    writing_market_status(running_log, "Running_log.txt")

                    Market_order_Sell(qte_call_hedge_despiration, Deployed_Size, CE_stk_hedge, "Call", "Hedge Sell Despiration")
                    OID_Call = running_log[str(-CE_stk)]["Order ID"]
                    cancel_order(OID_Call,CE_stk)

                else:
                    pass

        else:
            pass

        if len(Active_strike_list_Put) != 0:
            PE_stk = Active_strike_list_Put[0]

            difference_put=abs(PE_stk-ATM_Strike)
            if difference_put<strikes_distance:
                CP_Put, qte_put_despiration = Compute_token_Closing_price(PE_stk, "Put")
                PE_stk_hedge=PE_stk-hedges_distance
                CP_Put_hedge, qte_put_hedge_despiration = Compute_token_Closing_price(PE_stk_hedge, "Put")

                Market_order_Buy(qte_put_despiration, Deployed_Size, PE_stk, "Put", "Buy Despiration")
                Active_strike_list_Put.remove(PE_stk)
                present_market_status["Active Put Strikes"] = Active_strike_list_Put
                writing_market_status(present_market_status)

                running_log = reading_market_status("Running_log.txt")
                running_log[str(-PE_stk)]["Status"] = "COMPLETE"
                writing_market_status(running_log, "Running_log.txt")

                Market_order_Sell(qte_put_hedge_despiration, Deployed_Size, PE_stk_hedge, "Put", "Hedge Sell Despiration")
                OID_Put = running_log[str(-PE_stk)]["Order ID"]
                cancel_order(OID_Put,PE_stk)
            else:
                pass
        
        else:
            pass

    else:
        pass


def Trailing_SL():
    global Deployed_Size

    today_date = datetime.today()
    date_str_today = today_date.strftime('%d-%b-%y')

    if date_str_today==Expiry_date:
        Checking_distance_from_spot()
    else:
        pass

    running_log = reading_market_status("Running_log.txt")

    present_market_status = reading_market_status()

    Market_Trend = present_market_status['Market Trend']
    Active_strike_list_Call = present_market_status["Active Call Strikes"]
    Active_strike_list_Put = present_market_status["Active Put Strikes"]

    reversal_status = present_market_status["Reversal status"]
    max_call_credit_spreads = present_market_status["Maximum call credit Spread"]
    max_put_credit_spreads = present_market_status["Maximum put credit Spread"]

    print(
        f"Incoming Active Put Strikes is {Active_strike_list_Put} and Incoming Active Call strikes is {Active_strike_list_Call}")
    console_output_log_recording(
        f"Incoming Active Put Strikes is {Active_strike_list_Put} and Incoming Active Call strikes is {Active_strike_list_Call}")

    if Market_Trend == "Neutral":

        ###################################### READING THE PRESENT STATUS OF THE SL ORDERS ##########################################
        if len(Active_strike_list_Call) != 0:
            CE_stk = Active_strike_list_Call[0]
            OID_Call = running_log[str(-CE_stk)]["Order ID"]
            Status_call = Status_compute(OID_Call)
            
            ###################################### READING THE PRESENT STATUS OF THE SL ORDERS ##########################################

            if Status_call == "TRIGGER PENDING":
                ####################################### READING THE PRESENT STATUS OF THE SOLD STRIKES ORDERS #######################################

                Initial_Call_price = running_log[str(CE_stk)]["Initial Price"]
                SL_Call = running_log[str(CE_stk)]["Trailing SL"]
                Trailing_SL_status_Call=running_log[str(CE_stk)]["Trailing Status"]
                
                error_in_sl_placement_call=running_log[str(-CE_stk)]["Error in SL placement"]
                
                ####################################### READING THE PRESENT STATUS OF THE SOLD STRIKES ORDERS ########################################
                pause()
                CE_CP, QE_CE = Compute_token_Closing_price(CE_stk, "Call")
                
                if error_in_sl_placement_call==1:
                    print(f"Error in SL placement found in the call Strike {CE_stk}")
                    console_output_log_recording(f"Error in SL placement found in the call Strike {CE_stk}")

                    Required_SL=running_log[str(-CE_stk)]["Required SL"]

                    Price_circuit=Circuit_limit_price(CE_stk,"Call")
                    Circuit_price=Price_circuit-0.05
                    Updated_SL=Circuit_price

                    if Required_SL>Updated_SL and Updated_SL>SL_Call:
                        print(f"Updating the SL of call strike {CE_stk} to the higher price {Updated_SL}")
                        console_output_log_recording(f"Updating the SL of call strike {CE_stk} to the higher price {Updated_SL}")

                        Modify_SL_Order(OID_Call, Deployed_Size, Updated_SL, "Trailing SL", "SL Limit", CE_stk)
                    elif Updated_SL>=Required_SL and Updated_SL>SL_Call:
                        print(f"Updating the SL of call strike {CE_stk} to the Required SL {Required_SL}")
                        console_output_log_recording(f"Updating the SL of call strike {CE_stk} to the Required SL {Required_SL}")

                        Modify_SL_Order(OID_Call, Deployed_Size, Required_SL, "Trailing SL", "SL Limit", CE_stk)

                        running_log = reading_market_status("Running_log.txt")
                        running_log[str(-CE_stk)]["Error in SL placement"]=0
                        writing_market_status(running_log, "Running_log.txt")

                    else:
                        pass
                elif error_in_sl_placement_call==0:

                    print(f"Present Closing Price CE {CE_CP} and Stored SL CE {SL_Call}")
                    console_output_log_recording(f"Present Closing Price CE {CE_CP} and Stored SL CE {SL_Call}")

                    if CE_CP < (Initial_Call_price/2) and Trailing_SL_status_Call == 0:
                        print(f"Updating the Call strike {CE_stk} SL at price {Initial_Call_price}")
                        console_output_log_recording(f"Updating the Call strike {CE_stk} SL at price {Initial_Call_price}")

                        Modify_SL_Order(OID_Call, Deployed_Size, Initial_Call_price, "Trailing SL", "SL Limit", CE_stk)

                        running_log = reading_market_status("Running_log.txt")
                        running_log[str(CE_stk)]["Trailing Status"]=1
                        running_log[str(-CE_stk)]["Required SL"]=Initial_Call_price
                        writing_market_status(running_log, "Running_log.txt")

                    elif CE_CP >= (Initial_Call_price/2) and Trailing_SL_status_Call == 0:
                        print(f"No SL Update for the Call Strike {CE_stk}")
                        console_output_log_recording(f"No SL Update for the Call Strike {CE_stk}")

                    elif Trailing_SL_status_Call == 1:
                        print(f"SL got updated for the Strike {CE_stk}")
                        console_output_log_recording(f"SL got updated for the Strike {CE_stk}")
                    else:
                        pass

                else:
                    pass

            elif Status_call == "COMPLETE":
                print(f"SL hit on the Call Strike {CE_stk} now Market Trend is Bullish")
                console_output_log_recording(f"SL hit on the Call Strike {CE_stk} now Market Trend is Bullish")

                running_log[str(-CE_stk)]["Status"] = "COMPLETE"
                writing_market_status(running_log, "Running_log.txt")

                present_market_status['Market Trend'] = "Trending Up"
                writing_market_status(present_market_status)

                CE_Hedge = CE_stk + hedges_distance

                pause()

                CE_Hedge_CP, QE_CE_Hedge = Compute_token_Closing_price(CE_Hedge, "Call")
                Market_order_Sell(QE_CE_Hedge, Deployed_Size, CE_Hedge, "Call", "Hedge Sell")

                print("Adding new Strikes")
                console_output_log_recording("Adding new Strikes")
                Active_strike_list_Call, Active_strike_list_Put = New_order_Placement(Active_strike_list_Call,Active_strike_list_Put)

                print(
                    f"New Strikes list for Call {Active_strike_list_Call} and New Strikes list for put {Active_strike_list_Put}")
                console_output_log_recording(
                    f"New Strikes list for Call {Active_strike_list_Call} and New Strikes list for put {Active_strike_list_Put}")

            else:
                pass

        if len(Active_strike_list_Put) != 0:
            PE_stk = Active_strike_list_Put[0]
            OID_Put = running_log[str(-PE_stk)]["Order ID"]
            Status_put = Status_compute(OID_Put)

            if Status_put == "TRIGGER PENDING":
                Initial_Put_price = running_log[str(PE_stk)]["Initial Price"]
                SL_Put = running_log[str(PE_stk)]["Trailing SL"]
                Trailing_SL_status_Put=running_log[str(PE_stk)]["Trailing Status"]

                error_in_sl_placement_put=running_log[str(-PE_stk)]["Error in SL placement"]

                pause()

                PE_CP, QE_PE = Compute_token_Closing_price(PE_stk, "Put")

                if error_in_sl_placement_put==1:
                    print(f"Error in SL placement found in the put Strike {PE_stk}")
                    console_output_log_recording(f"Error in SL placement found in the put Strike {PE_stk}")

                    Required_SL=running_log[str(-PE_stk)]["Required SL"]

                    Price_circuit=Circuit_limit_price(PE_stk,"Put")
                    Circuit_price=Price_circuit-0.05
                    Updated_SL=Circuit_price

                    if Required_SL>Updated_SL and Updated_SL>SL_Put:
                        print(f"Updating the SL of put strike {PE_stk} to the higher price {Updated_SL}")
                        console_output_log_recording(f"Updating the SL of put strike {PE_stk} to the higher price {Updated_SL}")

                        Modify_SL_Order(OID_Put, Deployed_Size, Updated_SL, "Trailing SL", "SL Limit", PE_stk)
                    elif Updated_SL>=Required_SL and Updated_SL>SL_Put:
                        print(f"Updating the SL of put strike {PE_stk} to the Required SL {Required_SL}")
                        console_output_log_recording(f"Updating the SL of put strike {PE_stk} to the Required SL {Required_SL}")

                        Modify_SL_Order(OID_Put, Deployed_Size, Required_SL, "Trailing SL", "SL Limit", PE_stk)

                        running_log = reading_market_status("Running_log.txt")
                        running_log[str(-PE_stk)]["Error in SL placement"]=0
                        writing_market_status(running_log, "Running_log.txt")

                    else:
                        pass
                elif error_in_sl_placement_put==0:
                    print(f"Present Closing Price {PE_CP} and Stored SL PE {SL_Put}")
                    console_output_log_recording(f"Present Closing Price {PE_CP} and Stored SL PE {SL_Put}")

                    if PE_CP < (Initial_Put_price/2) and Trailing_SL_status_Put == 0:

                        print(f"Updating the Put strike {PE_stk} SL at price {Initial_Put_price}")
                        console_output_log_recording(f"Updating the Put strike {PE_stk} SL at price {Initial_Put_price}")

                        Modify_SL_Order(OID_Put, Deployed_Size, Initial_Put_price, "Trailing SL", "SL Limit", PE_stk)

                        running_log = reading_market_status("Running_log.txt")
                        running_log[str(PE_stk)]["Trailing Status"]=1
                        running_log[str(-PE_stk)]["Required SL"]=Initial_Put_price

                        writing_market_status(running_log, "Running_log.txt")

                    elif PE_CP >= (Initial_Put_price/2) and Trailing_SL_status_Put == 0:
                        print(f"No SL Update for the Put Strike {PE_stk}")
                        console_output_log_recording(f"No SL Update for the Put Strike {PE_stk}")

                    elif Trailing_SL_status_Put == 1:
                        print(f"SL got updated for the Strike {PE_stk}")
                        console_output_log_recording(f"SL got updated for the Strike {PE_stk}")
                    else:
                        pass
                else:
                    pass


            elif Status_put == "COMPLETE":
                print(f"SL hit on the Put Strike {PE_stk} now Market Trend is Bearish")
                console_output_log_recording(f"SL hit on the Put Strike {PE_stk} now Market Trend is Bearish")

                running_log[str(-PE_stk)]["Status"] = "COMPLETE"
                writing_market_status(running_log, "Running_log.txt")

                present_market_status['Market Trend'] = "Trending Down"
                writing_market_status(present_market_status)

                PE_Hedge = PE_stk - hedges_distance

                pause()

                PE_Hedge_CP, QE_PE_Hedge = Compute_token_Closing_price(PE_Hedge, "Put")
                Market_order_Sell(QE_PE_Hedge, Deployed_Size, PE_Hedge, "Put", "Hedge Sell")

                print("Adding new Strikes")
                console_output_log_recording("Adding new Strikes")
                Active_strike_list_Call, Active_strike_list_Put = New_order_Placement(Active_strike_list_Call,
                                                                                    Active_strike_list_Put)

                print(
                    f"New Strikes list for Call {Active_strike_list_Call} and New Strikes list for put {Active_strike_list_Put}")
                console_output_log_recording(
                    f"New Strikes list for Call {Active_strike_list_Call} and New Strikes list for put {Active_strike_list_Put}")

            else:
                pass

    elif Market_Trend == "Trending Up":

        print(f"Present market trend is {Market_Trend}")

        if len(Active_strike_list_Put) != 0:

            for i in range(len(Active_strike_list_Put)):
                PE_stk = Active_strike_list_Put[i]

                OID_Put = running_log[str(-PE_stk)]["Order ID"]

                print(f"OID : {OID_Put} strike: {-PE_stk}")
                Status_put = Status_compute(OID_Put)

                if Status_put == "TRIGGER PENDING":
                    SL_Put = running_log[str(PE_stk)]["Trailing SL"]
                    Trailing_SL_status_Put=running_log[str(PE_stk)]["Trailing Status"]
                    Initial_Put_price = running_log[str(PE_stk)]["Initial Price"]
                    error_in_sl_placement_put=running_log[str(-PE_stk)]["Error in SL placement"]

                    pause()

                    PE_CP, QE_PE = Compute_token_Closing_price(PE_stk, "Put")

                    if error_in_sl_placement_put==1:
                        print(f"Error in SL placement found in the put Strike {PE_stk}")
                        console_output_log_recording(f"Error in SL placement found in the put Strike {PE_stk}")

                        Required_SL=running_log[str(-PE_stk)]["Required SL"]

                        Price_circuit=Circuit_limit_price(PE_stk,"Put")
                        Circuit_price=Price_circuit-0.05
                        Updated_SL=Circuit_price

                        if Required_SL>Updated_SL and Updated_SL>SL_Put:
                            print(f"Updating the SL of put strike {PE_stk} to the higher price {Updated_SL}")
                            console_output_log_recording(f"Updating the SL of put strike {PE_stk} to the higher price {Updated_SL}")

                            Modify_SL_Order(OID_Put, Deployed_Size, Updated_SL, "Trailing SL", "SL Limit", PE_stk)
                        elif Updated_SL>=Required_SL and Updated_SL>SL_Put:
                            print(f"Updating the SL of put strike {PE_stk} to the Required SL {Required_SL}")
                            console_output_log_recording(f"Updating the SL of put strike {PE_stk} to the Required SL {Required_SL}")

                            Modify_SL_Order(OID_Put, Deployed_Size, Required_SL, "Trailing SL", "SL Limit", PE_stk)

                            running_log = reading_market_status("Running_log.txt")
                            running_log[str(-PE_stk)]["Error in SL placement"]=0
                            writing_market_status(running_log, "Running_log.txt")

                        else:
                            pass

                    elif error_in_sl_placement_put==0:
                        print(f"Present Closing Price {PE_CP} and Stored SL PE {SL_Put}")
                        console_output_log_recording(f"Present Closing Price {PE_CP} and Stored SL PE {SL_Put}")

                        if PE_CP < (Initial_Put_price/2) and Trailing_SL_status_Put == 0:
                            print(f"Updating the Put strike {PE_stk} SL at price {Initial_Put_price}")
                            console_output_log_recording(f"Updating the Put strike {PE_stk} SL at price {Initial_Put_price}")

                            Modify_SL_Order(OID_Put, Deployed_Size, Initial_Put_price, "Trailing SL", "SL Limit", PE_stk)

                            running_log = reading_market_status("Running_log.txt")
                            running_log[str(PE_stk)]["Trailing Status"]=1
                            running_log[str(-PE_stk)]["Required SL"]=Initial_Put_price
                            writing_market_status(running_log, "Running_log.txt")

                        elif PE_CP >= (Initial_Put_price/2) and Trailing_SL_status_Put == 0:
                            print(f"No SL Update for the Put Strike {PE_stk}")
                            console_output_log_recording(f"No SL Update for the Put Strike {PE_stk}")

                        elif Trailing_SL_status_Put == 1:
                            print(f"SL got updated for the Strike {PE_stk}")
                            console_output_log_recording(f"SL got updated for the Strike {PE_stk}")
                        else:
                            pass

                    else:
                        pass

                elif Status_put == "COMPLETE":

                    present_market_status["Reversal status"] = 1

                    print(f"SL hit for strike {PE_stk} on put side the market reverses the trend")
                    console_output_log_recording(
                        f"SL hit for strike {PE_stk} on put side the market reverses the trend")

                    running_log[str(-PE_stk)]["Status"] = "COMPLETE"
                    writing_market_status(running_log, "Running_log.txt")

                    Active_strike_list_Put.remove(PE_stk)
                    present_market_status["Active Put Strikes"] = Active_strike_list_Put
                    writing_market_status(present_market_status)

                    print(f"The new Active strike Put list is {Active_strike_list_Put}")
                    console_output_log_recording(f"The new Active strike Put list is {Active_strike_list_Put}")
                    PE_stk_Hedges = PE_stk - hedges_distance

                    pause()

                    PE_Hedge_CP, QE_PE_Hedge = Compute_token_Closing_price(PE_stk_Hedges, "Put")
                    Market_order_Sell(QE_PE_Hedge, Deployed_Size, PE_stk_Hedges, "Put", "Hedge Sell")

                else:
                    pass

        else:
            pass

        if len(Active_strike_list_Call) != 0:
            CE_stk = Active_strike_list_Call[0]
            OID_Call = running_log[str(-CE_stk)]["Order ID"]
            Status_call = Status_compute(OID_Call)

            if Status_call == "TRIGGER PENDING":
                SL_Call = running_log[str(CE_stk)]["Trailing SL"]
                Trailing_SL_status_Call=running_log[str(CE_stk)]["Trailing Status"]
                Initial_Call_price = running_log[str(CE_stk)]["Initial Price"]
                error_in_sl_placement_call=running_log[str(-CE_stk)]["Error in SL placement"]

                pause()

                CE_CP, QE_CE = Compute_token_Closing_price(CE_stk, "Call")

                if error_in_sl_placement_call==1:
                    print(f"Error in SL placement found in the call Strike {CE_stk}")
                    console_output_log_recording(f"Error in SL placement found in the call Strike {CE_stk}")

                    Required_SL=running_log[str(-CE_stk)]["Required SL"]

                    Price_circuit=Circuit_limit_price(CE_stk,"Call")
                    Circuit_price=Price_circuit-0.05
                    Updated_SL=Circuit_price

                    if Required_SL>Updated_SL and Updated_SL>SL_Call:
                        print(f"Updating the SL of call strike {CE_stk} to the higher price {Updated_SL}")
                        console_output_log_recording(f"Updating the SL of call strike {CE_stk} to the higher price {Updated_SL}")

                        Modify_SL_Order(OID_Call, Deployed_Size, Updated_SL, "Trailing SL", "SL Limit", CE_stk)
                    elif Updated_SL>=Required_SL and Updated_SL>SL_Call:
                        print(f"Updating the SL of call strike {CE_stk} to the Required SL {Required_SL}")
                        console_output_log_recording(f"Updating the SL of call strike {CE_stk} to the Required SL {Required_SL}")

                        Modify_SL_Order(OID_Call, Deployed_Size, Required_SL, "Trailing SL", "SL Limit", CE_stk)

                        running_log = reading_market_status("Running_log.txt")
                        running_log[str(-CE_stk)]["Error in SL placement"]=0
                        writing_market_status(running_log, "Running_log.txt")

                    else:
                        pass

                elif error_in_sl_placement_call==0:
                    print(f"Present Closing Price CE {CE_CP} and Stored SL CE {SL_Call}")
                    console_output_log_recording(f"Present Closing Price CE {CE_CP} and Stored SL CE {SL_Call}")

                    if CE_CP < (Initial_Call_price/2) and Trailing_SL_status_Call == 0:

                        print(f"Updating the Call strike {CE_stk} SL at price {Initial_Call_price}")
                        console_output_log_recording(f"Updating the Call strike {CE_stk} SL at price {Initial_Call_price}")

                        Modify_SL_Order(OID_Call, Deployed_Size, Initial_Call_price, "Trailing SL", "SL Limit", CE_stk)

                        running_log = reading_market_status("Running_log.txt")
                        running_log[str(CE_stk)]["Trailing Status"]=1
                        running_log[str(-CE_stk)]["Required SL"]=Initial_Call_price
                        writing_market_status(running_log, "Running_log.txt")

                    elif CE_CP >= (Initial_Call_price/2) and Trailing_SL_status_Call == 0:
                        print(f"No SL update for Call Strike {CE_stk}")
                        console_output_log_recording(f"No SL update for Call Strike {CE_stk}")

                    elif Trailing_SL_status_Call == 1:
                        print(f"SL got updated for the Strike {CE_stk}")
                        console_output_log_recording(f"SL got updated for the Strike {CE_stk}")
                    else:
                        pass

                else:
                    pass


            elif Status_call == "COMPLETE":
                print(
                    f"SL hit on call Strike {CE_stk} the market continues in the same trend selling Additional Strikes")
                console_output_log_recording(
                    f"SL hit on call Strike {CE_stk} the market continues in the same trend selling Additional Strikes")

                running_log[str(-CE_stk)]["Status"] = "COMPLETE"
                writing_market_status(running_log, "Running_log.txt")

                Length_put = len(Active_strike_list_Put)
                CE_stk_Hedges = CE_stk + hedges_distance

                pause()

                CE_Hedge_CP, QE_CE_Hedge = Compute_token_Closing_price(CE_stk_Hedges, "Call")
                Market_order_Sell(QE_CE_Hedge, Deployed_Size, CE_stk_Hedges, "Call", "Hedge Sell")

                if max_put_credit_spreads >= max_credit_spreads or reversal_status == 1:
                    Active_strike_list_Call.remove(CE_stk)
                    present_market_status["Active Call Strikes"] = Active_strike_list_Call
                    writing_market_status(present_market_status)

                    print("Maximum Credit limit reached can't sell more strikes or market reverses")
                    console_output_log_recording("Maximum Credit limit reached can't sell more strikes or market reverses")
                elif max_put_credit_spreads < max_credit_spreads and reversal_status == 0:
                    print("Adding new Strikes")
                    console_output_log_recording("Adding new Strikes")
                    Active_strike_list_Call, Active_strike_list_Put = New_order_Placement(Active_strike_list_Call,
                                                                                          Active_strike_list_Put)
                    print(
                        f"New Strikes list for Call {Active_strike_list_Call} and New Strikes list for put {Active_strike_list_Put}")
                    console_output_log_recording(
                        f"New Strikes list for Call {Active_strike_list_Call} and New Strikes list for put {Active_strike_list_Put}")
                else:
                    pass
            else:
                pass

        else:
            pass

    elif Market_Trend == "Trending Down":

        if len(Active_strike_list_Call) != 0:
            for i in range(len(Active_strike_list_Call)):
                CE_stk = Active_strike_list_Call[i]
                OID_Call = running_log[str(-CE_stk)]["Order ID"]
                Status_call = Status_compute(OID_Call)

                if Status_call == "TRIGGER PENDING":
                    SL_Call = running_log[str(CE_stk)]["Trailing SL"]
                    Trailing_SL_status_Call=running_log[str(CE_stk)]["Trailing Status"]
                    Initial_Call_price = running_log[str(CE_stk)]["Initial Price"]
                    error_in_sl_placement_call=running_log[str(-CE_stk)]["Error in SL placement"]

                    pause()

                    CE_CP, QE_CE = Compute_token_Closing_price(CE_stk, "Call")

                    if error_in_sl_placement_call==1:
                        print(f"Error in SL placement found in the call Strike {CE_stk}")
                        console_output_log_recording(f"Error in SL placement found in the call Strike {CE_stk}")

                        Required_SL=running_log[str(-CE_stk)]["Required SL"]

                        Price_circuit=Circuit_limit_price(CE_stk,"Call")
                        Circuit_price=Price_circuit-0.05
                        Updated_SL=Circuit_price

                        if Required_SL>Updated_SL and Updated_SL>SL_Call:
                            print(f"Updating the SL of call strike {CE_stk} to the higher price {Updated_SL}")
                            console_output_log_recording(f"Updating the SL of call strike {CE_stk} to the higher price {Updated_SL}")

                            Modify_SL_Order(OID_Call, Deployed_Size, Updated_SL, "Trailing SL", "SL Limit", CE_stk)
                        elif Updated_SL>=Required_SL and Updated_SL>SL_Call:
                            print(f"Updating the SL of call strike {CE_stk} to the Required SL {Required_SL}")
                            console_output_log_recording(f"Updating the SL of call strike {CE_stk} to the Required SL {Required_SL}")

                            Modify_SL_Order(OID_Call, Deployed_Size, Required_SL, "Trailing SL", "SL Limit", CE_stk)

                            running_log = reading_market_status("Running_log.txt")
                            running_log[str(-CE_stk)]["Error in SL placement"]=0
                            writing_market_status(running_log, "Running_log.txt")

                        else:
                            pass

                    elif error_in_sl_placement_call==0:
                        print(f"Present Closing Price CE {CE_CP} and Stored SL CE {SL_Call}")
                        console_output_log_recording(f"Present Closing Price CE {CE_CP} and Stored SL CE {SL_Call}")

                        if CE_CP < (Initial_Call_price/2) and Trailing_SL_status_Call == 0:

                            print(f"Updating the Call strike {CE_stk} SL at price {Initial_Call_price}")
                            console_output_log_recording(f"Updating the Call strike {CE_stk} SL at price {Initial_Call_price}")
                            Modify_SL_Order(OID_Call, Deployed_Size, Initial_Call_price, "Trailing SL", "SL Limit", CE_stk)

                            running_log = reading_market_status("Running_log.txt")
                            running_log[str(CE_stk)]["Trailing Status"]=1
                            running_log[str(-CE_stk)]["Required SL"]=Initial_Call_price
                            writing_market_status(running_log, "Running_log.txt")

                        elif CE_CP >= (Initial_Call_price/2) and Trailing_SL_status_Call == 0:
                            print(f"No SL Update for the Call Strike {CE_stk}")
                            console_output_log_recording(f"No SL Update for the Call Strike {CE_stk}")

                        elif Trailing_SL_status_Call == 1:
                            print(f"SL got updated for the Strike {CE_stk}")
                            console_output_log_recording(f"SL got updated for the Strike {CE_stk}")
                        else:
                            pass

                    else:
                        pass

                elif Status_call == "COMPLETE":
                    present_market_status["Reversal status"] = 1

                    print(f"SL hit for strike {CE_stk} on call side the market reverses the trend")
                    console_output_log_recording(
                        f"SL hit for strike {CE_stk} on call side the market reverses the trend")

                    running_log[str(-CE_stk)]["Status"] = "COMPLETE"
                    writing_market_status(running_log, "Running_log.txt")

                    Active_strike_list_Call.remove(CE_stk)
                    present_market_status["Active Call Strikes"] = Active_strike_list_Call
                    writing_market_status(present_market_status)

                    print(f"The new Active strike Call list is {Active_strike_list_Call}")
                    console_output_log_recording(f"The new Active strike Call list is {Active_strike_list_Call}")

                    CE_stk_Hedges = CE_stk + hedges_distance

                    pause()

                    CE_Hedge_CP, QE_CE_Hedge = Compute_token_Closing_price(CE_stk_Hedges, "Call")
                    Market_order_Sell(QE_CE_Hedge, Deployed_Size, CE_stk_Hedges, "Call", "Hedge Sell")
                else:
                    pass

        else:
            pass

        if len(Active_strike_list_Put) != 0:
            PE_stk = Active_strike_list_Put[0]
            OID_Put = running_log[str(-PE_stk)]["Order ID"]
            Status_put = Status_compute(OID_Put)

            if Status_put == "TRIGGER PENDING":
                SL_Put = running_log[str(PE_stk)]["Trailing SL"]
                Initial_Put_price = running_log[str(PE_stk)]["Initial Price"]
                Trailing_SL_status_Put=running_log[str(PE_stk)]["Trailing Status"]
                error_in_sl_placement_put=running_log[str(-PE_stk)]["Error in SL placement"]

                pause()

                PE_CP, QE_PE = Compute_token_Closing_price(PE_stk, "Put")

                if error_in_sl_placement_put==1:
                    print(f"Error in SL placement found in the put Strike {PE_stk}")
                    console_output_log_recording(f"Error in SL placement found in the put Strike {PE_stk}")

                    Required_SL=running_log[str(-PE_stk)]["Required SL"]

                    Price_circuit=Circuit_limit_price(PE_stk,"Put")
                    Circuit_price=Price_circuit-0.05
                    Updated_SL=Circuit_price

                    if Required_SL>Updated_SL and Updated_SL>SL_Put:
                        print(f"Updating the SL of put strike {PE_stk} to the higher price {Updated_SL}")
                        console_output_log_recording(f"Updating the SL of put strike {PE_stk} to the higher price {Updated_SL}")

                        Modify_SL_Order(OID_Put, Deployed_Size, Updated_SL, "Trailing SL", "SL Limit", PE_stk)
                    elif Updated_SL>=Required_SL and Updated_SL>SL_Put:
                        print(f"Updating the SL of put strike {PE_stk} to the Required SL {Required_SL}")
                        console_output_log_recording(f"Updating the SL of put strike {PE_stk} to the Required SL {Required_SL}")

                        Modify_SL_Order(OID_Put, Deployed_Size, Required_SL, "Trailing SL", "SL Limit", PE_stk)

                        running_log = reading_market_status("Running_log.txt")
                        running_log[str(-PE_stk)]["Error in SL placement"]=0
                        writing_market_status(running_log, "Running_log.txt")

                    else:
                        pass

                elif error_in_sl_placement_put==0:
                    print(f"Present Closing Price {PE_CP} and Stored SL PE {SL_Put}")
                    console_output_log_recording(f"Present Closing Price {PE_CP} and Stored SL PE {SL_Put}")

                    if PE_CP < (Initial_Put_price/2) and Trailing_SL_status_Put == 0:

                        print(f"Updating the Put strike {PE_stk} SL at price {Initial_Put_price}")
                        console_output_log_recording(f"Updating the Put strike {PE_stk} SL at price {Initial_Put_price}")
                        
                        Modify_SL_Order(OID_Put, Deployed_Size, Initial_Put_price, "Trailing SL", "SL Limit", PE_stk)

                        running_log = reading_market_status("Running_log.txt")
                        running_log[str(PE_stk)]["Trailing Status"]=1
                        running_log[str(-PE_stk)]["Required SL"]=Initial_Put_price
                        writing_market_status(running_log, "Running_log.txt")

                    elif PE_CP >= (Initial_Put_price/2) and Trailing_SL_status_Put == 0:
                        print(f"No SL Update for the Put Strike {PE_stk}")
                        console_output_log_recording(f"No SL Update for the Put Strike {PE_stk}")

                    elif Trailing_SL_status_Put == 1:
                        print(f"SL got updated for the Strike {PE_stk}")
                        console_output_log_recording(f"SL got updated for the Strike {PE_stk}")
                    else:
                        pass

                else:
                    pass

            elif Status_put == "COMPLETE":
                print(
                    f"SL hit on put Strike {PE_stk} the market continues in the same trend selling Additional Strikes")
                console_output_log_recording(
                    f"SL hit on put Strike {PE_stk} the market continues in the same trend selling Additional Strikes")

                running_log[str(-PE_stk)]["Status"] = "COMPLETE"
                writing_market_status(running_log, "Running_log.txt")

                Length_call = len(Active_strike_list_Call)
                PE_stk_Hedges = PE_stk - hedges_distance

                pause()

                PE_Hedge_CP, QE_PE_Hedge = Compute_token_Closing_price(PE_stk_Hedges, "Put")
                Market_order_Sell(QE_PE_Hedge, Deployed_Size, PE_stk_Hedges, "Put", "Hedge Sell")

                if max_call_credit_spreads >= max_credit_spreads or reversal_status == 1:

                    Active_strike_list_Put.remove(PE_stk)
                    present_market_status["Active Put Strikes"] = Active_strike_list_Put
                    writing_market_status(present_market_status)
                
                    print("Maximum Credit limit reached can't sell more strikes or market reverses")
                    console_output_log_recording("Maximum Credit limit reached can't sell more strikes or market reverses")

                elif max_call_credit_spreads < max_credit_spreads and reversal_status == 0:
                    print("Adding new Strikes")
                    console_output_log_recording("Adding new Strikes")
                    Active_strike_list_Call, Active_strike_list_Put = New_order_Placement(Active_strike_list_Call,
                                                                                          Active_strike_list_Put)
                    print(
                        f"New Strikes list for Call {Active_strike_list_Call} and New Strikes list for put {Active_strike_list_Put}")
                    console_output_log_recording(
                        f"New Strikes list for Call {Active_strike_list_Call} and New Strikes list for put {Active_strike_list_Put}")
                else:
                    pass

            else:
                pass
        else:
            pass

    else:
        pass

    current_time = datetime.now().strftime("%H:%M")
    if current_time >= last_trailing_time:
        Last_5_mins_update()
    else:
        schedule_next_execution()


def schedule_next_execution():
    import time
    global time_list_5_min
    global run

    times_to_execute = time_list_5_min

    # Get the current time
    current_time = datetime.now().strftime("%H:%M:%S")

    print(f"Trailing SL run {run} and current time is {current_time}")
    console_output_log_recording(f"Trailing SL run {run} and current time is {current_time}")

    run = run + 1
    # Find the next time in the list that is greater than the current time
    next_time = None
    for t in times_to_execute:
        if t > current_time:
            next_time = t
            break

    if next_time:
        # Calculate the time difference in seconds
        time_difference = (datetime.strptime(next_time, "%H:%M:%S") - datetime.strptime(current_time,"%H:%M:%S")).total_seconds()
        time.sleep(int(time_difference))
        Trailing_SL()

    else:
        # No more times in the list for today, you can handle this case as needed
        print("No more times to execute today")


def New_order_Placement(Active_strike_list_Call, Active_strike_list_Put,Type="Normal"):
    global Market_Trend
    global Deployed_Size
    import time

    present_market_status = reading_market_status()

    Market_Trend = present_market_status['Market Trend']

    reversal_status = present_market_status["Reversal status"]
    max_call_credit_spreads = present_market_status["Maximum call credit Spread"]
    max_put_credit_spreads = present_market_status["Maximum put credit Spread"]

    while True:
        try:
            Nifty = kite.ltp(["NSE:NIFTY 50"])
            Nifty_Spot_price = Nifty['NSE:NIFTY 50']['last_price']

            Vix = kite.ltp(["NSE:INDIA VIX"])
            Present_vol = Vix['NSE:INDIA VIX']['last_price']

            break
        except Exception as e:
            Error_statement=str(e)
            if "Markets are closed right now" not in Error_statement:
                print(f"Error: {e}")
                console_output_log_recording(f"Error: {e}")
                print("Retrying after 1 second for Closing Price")
                console_output_log_recording("Retrying after 1 second for Closing Price")
                time.sleep(1)
            elif "Markets are closed right now" in Error_statement:
                print("Market is closed right now")
                console_output_log_recording("Market is closed right now")
                break


    range = ((Present_vol / np.sqrt(252)) * Nifty_Spot_price) / 100

    offset = round(range, 2)
    offset = round(offset / strikes_distance) * strikes_distance
    offset = int(offset)

    print(f"The Offset computed is {offset}")
    console_output_log_recording(f"The Offset computed is {offset}")


    if Market_Trend == "Trending Up":
        Call_strike = Active_strike_list_Call[0]
        length_put = len(Active_strike_list_Put)
        if length_put < (max_credit_spreads-1):

            ############################## COMPUTING NEW STRIKES ###############################################
            Put_strike = Active_strike_list_Put[length_put - 1]
            New_Put_Strike = Put_strike + strikes_distance

            New_Call_Strike = Call_strike + offset

            Active_strike_list_Call = []

            Active_strike_list_Call.append(New_Call_Strike)
            Active_strike_list_Put.append(New_Put_Strike)

            max_put_credit_spreads = len(Active_strike_list_Put)

            present_market_status["Maximum put credit Spread"] = max_put_credit_spreads
            present_market_status["Active Call Strikes"] = Active_strike_list_Call
            present_market_status["Active Put Strikes"] = Active_strike_list_Put

            writing_market_status(present_market_status)

            New_Put_Strike_hedges = New_Put_Strike - hedges_distance
            New_Call_Strike_hedges = New_Call_Strike + hedges_distance
            ############################## COMPUTING NEW STRIKES ###############################################

            ############################## SENDING THE ORDER TO THE MARKET #####################################
            CP_Call, qte_call = Compute_token_Closing_price(New_Call_Strike, "Call")
            CP_Put, qte_put = Compute_token_Closing_price(New_Put_Strike, "Put")
            CP_Call_hedge, qte_call_hedge = Compute_token_Closing_price(New_Call_Strike_hedges, "Call")
            CP_Put_hedge, qte_put_hedge = Compute_token_Closing_price(New_Put_Strike_hedges, "Put")

            if Type=="Normal":
                limit_order_Sell(qte_call, Deployed_Size, CP_Call, New_Call_Strike, "Call")
                limit_order_Sell(qte_put, Deployed_Size, CP_Put, New_Put_Strike, "Put")

                Order_execution_Check(New_Call_Strike, New_Put_Strike, qte_call_hedge, qte_put_hedge, qte_call, qte_put,New_Call_Strike_hedges, New_Put_Strike_hedges)
            
            elif Type=="Market":
                Market_order_Sell(qte_call,Deployed_Size,New_Call_Strike,"Call","Sell","Sell Despiration")
                running_log = reading_market_status("Running_log.txt")
                price_call=running_log[str(New_Call_Strike)]["Initial Price"]
                SL_Call=2*price_call
                SL_Call_Trig = SL_Call - 0.05
                SL_Initiate_order(qte_call, Deployed_Size, SL_Call, SL_Call_Trig, New_Call_Strike, "Call")
                Market_order_Buy(qte_call_hedge,Deployed_Size,New_Call_Strike_hedges,"Call","Buy Hedge")

                Market_order_Sell(qte_put,Deployed_Size,New_Put_Strike,"Put","Sell","Sell Despiration")
                running_log = reading_market_status("Running_log.txt")
                price_put=running_log[str(New_Put_Strike)]["Initial Price"]
                SL_Put=2*price_put
                SL_Put_Trig = SL_Put - 0.05
                SL_Initiate_order(qte_put, Deployed_Size, SL_Put, SL_Put_Trig, New_Put_Strike, "Put")
                Market_order_Buy(qte_put_hedge,Deployed_Size,New_Put_Strike_hedges,"Put","Buy Hedge")   
            else:
                pass
            ############################## SENDING THE ORDER TO THE MARKET #####################################

            return Active_strike_list_Call, Active_strike_list_Put

        elif length_put == (max_credit_spreads-1):

            ############################## COMPUTING NEW STRIKES ###############################################
            Active_strike_list_Call = []

            Put_strike = Active_strike_list_Put[length_put - 1]
            New_Put_Strike = Put_strike + strikes_distance

            Active_strike_list_Put.append(New_Put_Strike)
            New_Put_Strike_hedges = New_Put_Strike - hedges_distance

            max_put_credit_spreads = len(Active_strike_list_Put)

            present_market_status["Maximum put credit Spread"] = max_put_credit_spreads
            present_market_status["Active Call Strikes"] = Active_strike_list_Call
            present_market_status["Active Put Strikes"] = Active_strike_list_Put

            writing_market_status(present_market_status)

            ############################## COMPUTING NEW STRIKES ###############################################

            ############################## SENDING THE ORDER TO THE MARKET #####################################
            CP_Put, qte_put = Compute_token_Closing_price(New_Put_Strike, "Put")
            CP_Put_hedge, qte_put_hedge = Compute_token_Closing_price(New_Put_Strike_hedges, "Put")

            if Type=="Normal":
                limit_order_Sell(qte_put, Deployed_Size, CP_Put, New_Put_Strike, "Put")
                Order_execution_Check(None, New_Put_Strike, None, qte_put_hedge, None, qte_put, None, New_Put_Strike_hedges)
            elif Type=="Market":
                Market_order_Sell(qte_put,Deployed_Size,New_Put_Strike,"Put","Sell","Sell Despiration")
                running_log = reading_market_status("Running_log.txt")
                price_put=running_log[str(New_Put_Strike)]["Initial Price"]
                SL_Put=2*price_put
                SL_Put_Trig = SL_Put - 0.05
                SL_Initiate_order(qte_put, Deployed_Size, SL_Put, SL_Put_Trig, New_Put_Strike, "Put")
                Market_order_Buy(qte_put_hedge,Deployed_Size,New_Put_Strike_hedges,"Put","Buy Hedge")   
            else:
                pass
            ############################## SENDING THE ORDER TO THE MARKET #####################################

            return Active_strike_list_Call, Active_strike_list_Put


        else:
            pass

    elif Market_Trend == "Trending Down":
        Put_strike = Active_strike_list_Put[0]
        length_call = len(Active_strike_list_Call)

        if length_call < (max_credit_spreads-1):
            ############################## COMPUTING NEW STRIKES ###############################################
            Call_strike = Active_strike_list_Call[length_call - 1]
            New_Call_Strike = Call_strike - strikes_distance

            New_Put_Strike = Put_strike - offset

            Active_strike_list_Put = []

            Active_strike_list_Call.append(New_Call_Strike)
            Active_strike_list_Put.append(New_Put_Strike)

            New_Put_Strike_hedges = New_Put_Strike - hedges_distance
            New_Call_Strike_hedges = New_Call_Strike + hedges_distance

            max_call_credit_spreads = len(Active_strike_list_Call)

            present_market_status["Maximum call credit Spread"] = max_call_credit_spreads
            present_market_status["Active Call Strikes"] = Active_strike_list_Call
            present_market_status["Active Put Strikes"] = Active_strike_list_Put

            writing_market_status(present_market_status)
            ############################## COMPUTING NEW STRIKES ###############################################

            ############################## SENDING THE ORDER TO THE MARKET #####################################
            CP_Call, qte_call = Compute_token_Closing_price(New_Call_Strike, "Call")
            CP_Put, qte_put = Compute_token_Closing_price(New_Put_Strike, "Put")
            CP_Call_hedge, qte_call_hedge = Compute_token_Closing_price(New_Call_Strike_hedges, "Call")
            CP_Put_hedge, qte_put_hedge = Compute_token_Closing_price(New_Put_Strike_hedges, "Put")

            if Type=="Normal":
                limit_order_Sell(qte_call, Deployed_Size, CP_Call, New_Call_Strike, "Call")
                limit_order_Sell(qte_put, Deployed_Size, CP_Put, New_Put_Strike, "Put")

                Order_execution_Check(New_Call_Strike, New_Put_Strike, qte_call_hedge, qte_put_hedge, qte_call, qte_put,New_Call_Strike_hedges, New_Put_Strike_hedges)
            elif Type=="Market":
                Market_order_Sell(qte_call,Deployed_Size,New_Call_Strike,"Call","Sell","Sell Despiration")
                running_log = reading_market_status("Running_log.txt")
                price_call=running_log[str(New_Call_Strike)]["Initial Price"]

                SL_Call=2*price_call
                SL_Call_Trig = SL_Call - 0.05
                SL_Initiate_order(qte_call, Deployed_Size, SL_Call, SL_Call_Trig, New_Call_Strike, "Call")
                Market_order_Buy(qte_call_hedge,Deployed_Size,New_Call_Strike_hedges,"Call","Buy Hedge")

                Market_order_Sell(qte_put,Deployed_Size,New_Put_Strike,"Put","Sell","Sell Despiration")
                running_log = reading_market_status("Running_log.txt")
                price_put=running_log[str(New_Put_Strike)]["Initial Price"]

                SL_Put=2*price_put
                SL_Put_Trig = SL_Put - 0.05
                SL_Initiate_order(qte_put, Deployed_Size, SL_Put, SL_Put_Trig, New_Put_Strike, "Put")
                Market_order_Buy(qte_put_hedge,Deployed_Size,New_Put_Strike_hedges,"Put","Buy Hedge")   
            else:
                pass
            ############################## SENDING THE ORDER TO THE MARKET #####################################

            return Active_strike_list_Call, Active_strike_list_Put

        elif length_call == (max_credit_spreads-1):

            ############################## COMPUTING NEW STRIKES ###############################################
            Active_strike_list_Put = []

            Call_strike = Active_strike_list_Call[length_call - 1]
            New_Call_Strike = Call_strike - strikes_distance

            Active_strike_list_Call.append(New_Call_Strike)
            New_Call_Strike_hedges = New_Call_Strike + hedges_distance

            max_call_credit_spreads = len(Active_strike_list_Call)

            present_market_status["Maximum call credit Spread"] = max_call_credit_spreads
            present_market_status["Active Call Strikes"] = Active_strike_list_Call
            present_market_status["Active Put Strikes"] = Active_strike_list_Put

            writing_market_status(present_market_status)
            ############################## COMPUTING NEW STRIKES ###############################################

            ############################## SENDING THE ORDER TO THE MARKET #####################################
            CP_Call, qte_call = Compute_token_Closing_price(New_Call_Strike, "Call")
            CP_Call_hedge, qte_call_hedge = Compute_token_Closing_price(New_Call_Strike_hedges, "Call")

            if Type=="Normal":
                limit_order_Sell(qte_call, Deployed_Size, CP_Call, New_Call_Strike, "Call")
                Order_execution_Check(New_Call_Strike, None, qte_call_hedge, None, qte_call, None, New_Call_Strike_hedges,None)
            elif Type=="Market":
                Market_order_Sell(qte_call,Deployed_Size,New_Call_Strike,"Call","Sell","Sell Despiration")
                running_log = reading_market_status("Running_log.txt")
                price_call=running_log[str(New_Call_Strike)]["Initial Price"]

                SL_Call=2*price_call
                SL_Call_Trig = SL_Call - 0.05
                SL_Initiate_order(qte_call, Deployed_Size, SL_Call, SL_Call_Trig, New_Call_Strike, "Call")
                Market_order_Buy(qte_call_hedge,Deployed_Size,New_Call_Strike_hedges,"Call","Buy Hedge")
            else:
                pass
            ############################## SENDING THE ORDER TO THE MARKET #####################################

            return Active_strike_list_Call, Active_strike_list_Put
        else:
            pass


def Morning_run():
    present_market_status = reading_market_status()
    running_log = reading_market_status("Running_log.txt")

    Market_Trend = present_market_status['Market Trend']
    Active_strike_list_Call = present_market_status["Active Call Strikes"]
    Active_strike_list_Put = present_market_status["Active Put Strikes"]
    ################################# EXTRACTION OF THE ACTIVE CALL AND PUT STRIKES ################################

    if Market_Trend == "Neutral":
        CE_STK = Active_strike_list_Call[0]
        PE_STK = Active_strike_list_Put[0]

        SL_CE = running_log[str(-CE_STK)]["Required SL"]
        SL_PE = running_log[str(-PE_STK)]["Required SL"]

        while True:
            current_time = datetime.now()
            current_time = current_time.strftime("%H:%M:%S")

            print(f"Running the morning code {current_time} and Market Trend Neutral")
            console_output_log_recording(f"Running the morning code {current_time} and Market Trend Neutral")

            CP_CALL, QTE_CALL = Compute_token_Closing_price(CE_STK, "Call")
            CP_PUT, QTE_PUT = Compute_token_Closing_price(PE_STK, "Put")

            print(
                f"Current time: {current_time} Strike Call: {CE_STK} Old stop loss Call: {SL_CE} Current Price Call: {CP_CALL}")
            console_output_log_recording(
                f"Current time: {current_time} Strike Call: {CE_STK} Old stop loss Call: {SL_CE} Current Price Call: {CP_CALL}")
            print(
                f"Current time: {current_time} Strike Put: {PE_STK} Old stop loss Put: {SL_PE} Current Price Put: {CP_PUT}")
            console_output_log_recording(
                f"Current time: {current_time} Strike Put: {PE_STK} Old stop loss Put: {SL_PE} Current Price Put: {CP_PUT}")

            if current_time >= Desired_time:
                if CP_CALL >= SL_CE:
                    print(f"Modifiying the Call Morning SL to {CP_CALL} for strike {CE_STK} at time {current_time}")
                    console_output_log_recording(
                        f"Modifiying the Call Morning SL to {CP_CALL} for strike {CE_STK} at time {current_time}")

                    SL_Call_Trig = CP_CALL - 0.05
                    SL_Initiate_order(QTE_CALL, Deployed_Size, CP_CALL, SL_Call_Trig, Active_strike_list_Call[0],
                                      "Call", 1)
                    present_market_status['Market Trend'] = "Trending Up"
                    writing_market_status(present_market_status)

                else:
                    print(
                        f"Not Modifiying the Stoploss for strike {CE_STK} at time {current_time} and Restoring the old SL {SL_CE}")
                    console_output_log_recording(
                        f"Not Modifiying the Stoploss for strike {CE_STK} at time {current_time} and Restoring the old SL {SL_CE}")

                    SL_Call_Trig = SL_CE - 0.05
                    SL_Initiate_order(QTE_CALL, Deployed_Size, SL_CE, SL_Call_Trig, Active_strike_list_Call[0],
                                        "Call", 1)

                if CP_PUT >= SL_PE:
                    print(f"Modifiying the Put Morning SL to {CP_PUT} for strike {PE_STK} at time {current_time}")
                    console_output_log_recording(
                        f"Modifiying the Put Morning SL to {CP_PUT} for strike {PE_STK} at time {current_time}")

                    SL_Put_Trig = CP_PUT - 0.05
                    SL_Initiate_order(QTE_PUT, Deployed_Size, CP_PUT, SL_Put_Trig, Active_strike_list_Put[0], "Put", 1)
                    present_market_status['Market Trend'] = "Trending Down"
                    writing_market_status(present_market_status)
                else:
                    print(
                        f"Not Modifiying the Stoploss for strike {PE_STK} at time {current_time} and Restoring the old SL {SL_PE}")
                    console_output_log_recording(
                        f"Not Modifiying the Stoploss for strike {PE_STK} at time {current_time} and Restoring the old SL {SL_PE}")
                    SL_Put_Trig = SL_PE - 0.05
                    SL_Initiate_order(QTE_PUT, Deployed_Size, SL_PE, SL_Put_Trig, Active_strike_list_Put[0], "Put",
                                        1)

                break
            time.sleep(300)

    elif Market_Trend == "Trending Up":
        print(
            f"Incoming Active  call strikes {Active_strike_list_Call} and incoming Active put strikes {Active_strike_list_Put}")

        if len(Active_strike_list_Call) != 0:
            CE_STK = Active_strike_list_Call[0]
            SL_CE = running_log[str(-CE_STK)]["Required SL"]
        else:
            pass

        Stop_Loss_arr_Put = []

        for i in range(len(Active_strike_list_Put)):
            PE_STK = Active_strike_list_Put[i]
            SL_PE = running_log[str(-PE_STK)]["Required SL"]
            Stop_Loss_arr_Put.append(SL_PE)

        print(f"Stop loss array Put: {Stop_Loss_arr_Put}")

        while True:
            current_time = datetime.now()
            current_time = current_time.strftime("%H:%M:%S")
            print(f"Running the morning code {current_time} and Market Trend Trending Up")
            console_output_log_recording(f"Running the morning code {current_time} and Market Trend Trending Up")

            closing_price_put = []
            Qte_Put = []

            for i in range(len(Active_strike_list_Put)):
                PE_STK = Active_strike_list_Put[i]
                CP_PUT, QTE_PUT = Compute_token_Closing_price(PE_STK, "Put")
                closing_price_put.append(CP_PUT)
                Qte_Put.append(QTE_PUT)

            print(f"Closing Price Put: {closing_price_put}")

            if current_time >= Desired_time:

                for i in range(len(Active_strike_list_Put)):
                    CP_PE = closing_price_put[i]
                    SL_PE = Stop_Loss_arr_Put[i]
                    Quote_put = Qte_Put[i]

                    if CP_PE >= SL_PE:
                        print(
                            f"Modifiying the Put Morning SL to {CP_PE} for strike {Active_strike_list_Put[i]} at time {current_time}")
                        console_output_log_recording(
                            f"Modifiying the Put Morning SL to {CP_PE} for strike {Active_strike_list_Put[i]} at time {current_time}")

                        SL_Put_Trig = CP_PE - 0.05
                        SL_Initiate_order(Quote_put, Deployed_Size, CP_PE, SL_Put_Trig, Active_strike_list_Put[i],
                                          "Put", 1)
                    else:
                        print(
                            f"Not Modifiying the Morning Stoploss for strike {Active_strike_list_Put[i]} at time {current_time} and Restoring to {SL_PE}")
                        console_output_log_recording(
                            f"Not Modifiying the Morning Stoploss for strike {Active_strike_list_Put[i]} at time {current_time} and Restoring to {SL_PE}")

                        SL_Put_Trig = SL_PE - 0.05

                        SL_Initiate_order(Quote_put, Deployed_Size, SL_PE, SL_Put_Trig, Active_strike_list_Put[i],
                                            "Put", 1)

                if len(Active_strike_list_Call) != 0:
                    CP_CALL, QTE_CALL = Compute_token_Closing_price(CE_STK, "Call")
                    if CP_CALL >= SL_CE:
                        print(
                            f"Modifiying the Call Morning SL to {CP_CALL} for strike {Active_strike_list_Call[0]} at time {current_time}")
                        console_output_log_recording(
                            f"Modifiying the Call Morning SL to {CP_CALL} for strike {Active_strike_list_Call[0]} at time {current_time}")

                        SL_Call_Trig = CP_CALL - 0.05
                        SL_Initiate_order(QTE_CALL, Deployed_Size, CP_CALL, SL_Call_Trig, Active_strike_list_Call[0],
                                          "Call", 1)
                    else:
                        print(
                            f"Not Modifiying the Morning Stoploss for strike {Active_strike_list_Call[0]} at time {current_time} and Restoring to {SL_CE}")
                        console_output_log_recording(
                            f"Not Modifiying the Morning Stoploss for strike {Active_strike_list_Call[0]} at time {current_time} and Restoring to {SL_CE}")

                        SL_Call_Trig = SL_CE - 0.05
                        SL_Initiate_order(QTE_CALL, Deployed_Size, SL_CE, SL_Call_Trig, Active_strike_list_Call[0],
                                            "Call", 1)
                else:
                    pass

                break

            time.sleep(300)

    elif Market_Trend == "Trending Down":
        if len(Active_strike_list_Put) != 0:
            PE_STK = Active_strike_list_Put[0]
            SL_PE = running_log[str(-PE_STK)]["Required SL"]

        Stop_Loss_arr_Call = []

        for i in range(len(Active_strike_list_Call)):
            CE_STK = Active_strike_list_Call[i]
            SL_CE = running_log[str(-CE_STK)]["Required SL"]
            Stop_Loss_arr_Call.append(SL_CE)

        while True:
            current_time = datetime.now()
            current_time = current_time.strftime("%H:%M:%S")
            print(f"Running the morning code {current_time} and Market Trend is Trending Down")
            console_output_log_recording(f"Running the morning code {current_time} and Market Trend is Trending Down")

            closing_price_call = []
            Qte_Call = []

            for i in range(len(Active_strike_list_Call)):
                CE_STK = Active_strike_list_Call[i]
                CP_CALL, QTE_CALL = Compute_token_Closing_price(CE_STK, "Call")
                closing_price_call.append(CP_CALL)
                Qte_Call.append(QTE_CALL)

            if current_time >= Desired_time:

                for i in range(len(Active_strike_list_Call)):
                    CP_CE = closing_price_call[i]
                    SL_CE = Stop_Loss_arr_Call[i]
                    Quote_call = Qte_Call[i]

                    if CP_CE >= SL_CE:
                        print(
                            f"Modifiying the Call Morning SL to {CP_CE} for strike {Active_strike_list_Call[i]} at time {current_time}")
                        console_output_log_recording(
                            f"Modifiying the Call Morning SL to {CP_CE} for strike {Active_strike_list_Call[i]} at time {current_time}")

                        SL_Call_Trig = CP_CE - 0.05
                        SL_Initiate_order(Quote_call, Deployed_Size, CP_CE, SL_Call_Trig, Active_strike_list_Call[i],
                                          "Call", 1)
                    else:
                        print(
                            f"Not Modifiying the Morning Stoploss for strike {Active_strike_list_Call[i]} at time {current_time} and Restoring to {SL_CE}")
                        console_output_log_recording(
                            f"Not Modifiying the Morning Stoploss for strike {Active_strike_list_Call[i]} at time {current_time} and Restoring to {SL_CE}")

                        SL_Call_Trig = SL_CE - 0.05
                        SL_Initiate_order(Quote_call, Deployed_Size, SL_CE, SL_Call_Trig,
                                            Active_strike_list_Call[i], "Call", 1)

                if len(Active_strike_list_Put) != 0:
                    CP_PUT, QTE_PUT = Compute_token_Closing_price(PE_STK, "Put")
                    if CP_PUT >= SL_PE:
                        print(
                            f"Modifiying the Put Morning SL to {CP_PUT} for strike {Active_strike_list_Put[0]} at time {current_time}")
                        console_output_log_recording(
                            f"Modifiying the Put Morning SL to {CP_PUT} for strike {Active_strike_list_Put[0]} at time {current_time}")

                        SL_Put_Trig = CP_PUT - 0.05
                        SL_Initiate_order(QTE_PUT, Deployed_Size, CP_PUT, SL_Put_Trig, Active_strike_list_Put[0], "Put",
                                          1)
                    else:
                        print(
                            f"Not Modifiying the Morning Stoploss for strike {Active_strike_list_Put[0]} at time {current_time} and Restoring to {SL_PE}")
                        console_output_log_recording(
                            f"Not Modifiying the Morning Stoploss for strike {Active_strike_list_Put[0]} at time {current_time} and Restoring to {SL_PE}")

                        SL_Put_Trig = SL_PE - 0.05
                        SL_Initiate_order(QTE_PUT, Deployed_Size, SL_PE, SL_Put_Trig, Active_strike_list_Put[0],
                                            "Put", 1)
                else:
                    pass
                break
            time.sleep(300)
    else:
        pass


############################################# INITIAL DATE SELECTION ####################################################
def date_to_week(date):
    date_object = datetime.strptime(date, "%d-%b-%Y")
    day_of_week = date_object.strftime('%A')
    return day_of_week


def holiday_dates_scrape():
    import time

    url = "https://www.nseindia.com/api/holiday-master?type=trading"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    }

    while True:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            # Print the content of the response
            content_output = response.text
            content_output = json.loads(content_output)
            return content_output
        else:
            print("Failed to retrieve data from the URL:", response.status_code)
            print("Retrying in 1 second...")
            time.sleep(1)


def Holidays_dates_determination():
    content_output = holiday_dates_scrape()
    Holidays_date = []
    Description_of_holidays = []
    Week_on_holiday = []

    for ii in range(len(content_output["FO"])):
        holiday_date = content_output["FO"][ii]['tradingDate']
        discrip = content_output["FO"][ii]['description']
        week = content_output["FO"][ii]['weekDay']

        Holidays_date.append(holiday_date)
        Description_of_holidays.append(discrip)
        Week_on_holiday.append(week)

    import datetime

    current_year = datetime.datetime.now().year
    saturdays = []
    sundays = []

    descrip_saturday = []
    descrip_sunday = []

    # Iterate over all the days in the current year
    for month in range(1, 13):
        for day in range(1, 32):
            try:
                # Try to create a datetime object for the current date
                date_obj = datetime.datetime(current_year, month, day)
                # Check if the day is Saturday or Sunday
                if date_obj.weekday() == 5:  # Saturday (Monday is 0, Sunday is 6)
                    saturdays.append(date_obj.strftime("%d-%b-%Y"))  # Format as string
                elif date_obj.weekday() == 6:  # Sunday
                    sundays.append(date_obj.strftime("%d-%b-%Y"))  # Format as string
            except ValueError:
                # If the day is invalid for the current month, ignore it
                pass

    for i in range(len(saturdays)):
        descrip_saturday.append("Saturday")

    for i in range(len(sundays)):
        descrip_sunday.append("Sunday")

    Holidays_list = saturdays + sundays
    Discrip_list = descrip_saturday + descrip_sunday
    week_list = descrip_saturday + descrip_sunday

    Holidays_date = Holidays_date + Holidays_list
    Description_of_holidays = Description_of_holidays + Discrip_list
    Week_on_holiday = Week_on_holiday + week_list

    return Holidays_date, Description_of_holidays, Week_on_holiday


def Initial_date_compute(Current_expiry_date):
    global path_main

    date_object = datetime.strptime(Current_expiry_date, "%d-%b-%y")
    Expiry_date = date_object.strftime("%d-%b-%Y")

    today_date = datetime.today()
    formatted_todays_date = today_date.strftime('%d-%b-%Y')

    holiday_date, discription_holiday, week = Holidays_dates_determination()

    present_market_status = reading_market_status()
    Initial_date = present_market_status["Initial Date"]
    formatted_todays_date = str(formatted_todays_date)

    if formatted_todays_date == Initial_date:
        Initial_day = 1

    elif formatted_todays_date == Expiry_date:
        Initial_day = 0
        input_date = datetime.strptime(formatted_todays_date, "%d-%b-%Y")
        new_date = input_date + timedelta(days=1)
        New_Initial_date = new_date.strftime("%d-%b-%Y")
        Week_next_date = date_to_week(New_Initial_date)

        if New_Initial_date in holiday_date:
            if Week_next_date == "Friday":
                print("Sell the Next expiry Contracts Today only")
            else:
                while True:
                    if New_Initial_date in holiday_date:
                        input_date = datetime.strptime(New_Initial_date, "%d-%b-%Y")
                        new_date = input_date + timedelta(days=1)
                        New_Initial_date = new_date.strftime("%d-%b-%Y")
                        Week_next_date = date_to_week(New_Initial_date)
                    else:
                        break

                present_market_status["Initial Date"] = New_Initial_date
                writing_market_status(present_market_status)

        else:
            present_market_status["Initial Date"] = New_Initial_date
            writing_market_status(present_market_status)

    else:
        Initial_day = 0

    print(f"Today Initial status is {Initial_day}")

    return Initial_day


############################################# INITIAL DATE SELECTION ####################################################
 
#################################################### ALGO Code ##########################################################

path_main = "D:/ashu/Finance/algo_trading/Zerodha_GUI/Kite_Zerodha-main/Kite_Zerodha-main/"
Path_backtest_Report = "D:/ashu/Finance/algo_trading/Zerodha_GUI/Kite_Zerodha-main/Kite_Zerodha-main/Live_market_data_gathering/"

with open(path_main+'kite_api_login_credentials.txt', 'r') as file:
    data_str = file.read()

data_dict=json.loads(data_str)
logging.basicConfig(level=logging.DEBUG)
kite = KiteConnect(api_key=data_dict['API_Key'])

Access_token=data_dict["Acess_token"]
kite.set_access_token(Access_token)

####################### Global Declared Variables ##############################

###################################### INITIAL DAY SETTINGS #####################################

Interrupt = 1
call_strike=24850
put_strike=24000

###################################### INITIAL DAY SETTINGS #####################################


Segment = "NIFTY"

index_data = pd.read_csv(path_main + "Index_Symbols_Expiry.csv")
indices = index_data.index[index_data['Symbol'] == Segment].tolist()
date_list = []
month_end_list = []

for i in indices:
    date = index_data.loc[i, "Expiry Date"]
    month_end = index_data.loc[i, "Month End"]
    date_list.append(date)
    month_end_list.append(month_end)

Expiry_date = date_list[0]
Month_End = month_end_list[0]
Initial_day = Initial_date_compute(Expiry_date)
####################################### CONSTANTS OF TRADING #####################################

Initiate_time = "09:20"
Desired_time = "09:30"
Start_time="09:15"
Market_close_time="15:30:00"
last_trailing_time="15:24:00"

desired_delta = 0.15

Threshold_price = 1

size = 1
Lot_size = 25
strikes_distance = 50
hedges_distance = 600
Deployed_Size = Lot_size * size
max_credit_spreads = 4
####################################### CONSTANTS OF TRADING #####################################

global reversal_status
global max_call_credit_spreads
global max_put_credit_spreads

run = 0

start_time_5_min = datetime.strptime("9:15:00", "%H:%M:%S")
end_time_5_min = datetime.strptime("15:30:00", "%H:%M:%S")

start_time = datetime.strptime("9:15", "%H:%M")
end_time = datetime.strptime("15:30", "%H:%M")

interval = timedelta(minutes=5)
time_list_5_min = []

current_time = start_time_5_min
while current_time <= end_time_5_min:
    time_list_5_min.append(current_time.strftime("%H:%M:%S"))
    current_time += interval

interval_1_min = timedelta(minutes=1)
time_list_1_min = []

current_time = start_time
while current_time <= end_time:
    time_list_1_min.append(current_time.strftime("%H:%M"))
    current_time += interval_1_min

# ####################### Global Declared Variables ##############################

if Initial_day == 1 and Interrupt == 0:

    Input_Strike_Call = call_strike
    Input_Strike_Put = put_strike

    Input_Strike_Put_Hedge = Input_Strike_Put - hedges_distance
    Input_Strike_Call_Hedge = Input_Strike_Call + hedges_distance

    ######################## INITILIZATION OF LOGS FILE AND DATA FRAME AND MARKET TREND ########################################

    with open(Path_backtest_Report + 'Running_log_file.txt', 'w') as file:
        pass

    with open(Path_backtest_Report + 'Console_output_log_file.txt', 'w') as file:
        pass

    reversal_status = 0
    max_call_credit_spreads = 1
    max_put_credit_spreads = 1

    Active_strike_list_Call = [Input_Strike_Call]
    Active_strike_list_Put = [Input_Strike_Put]

    today_date = datetime.today()
    formatted_todays_date = today_date.strftime('%d-%b-%Y')
    formatted_todays_date = str(formatted_todays_date)

    market_status = {}
    market_status["Market Trend"] = "Neutral"
    market_status["Active Call Strikes"] = Active_strike_list_Call
    market_status["Active Put Strikes"] = Active_strike_list_Put
    market_status["Reversal status"] = reversal_status
    market_status["Maximum call credit Spread"] = max_call_credit_spreads
    market_status["Maximum put credit Spread"] = max_put_credit_spreads
    market_status["Segment"] = Segment
    market_status["Expiry Day"] = Expiry_date
    market_status["Month End"] = int(Month_End)
    market_status["Initial Date"] = formatted_todays_date

    with open(Path_backtest_Report + "Market_status.txt", 'w') as file:
        json.dump(market_status, file)

    ####################### INITILIZATION OF LOGS FILE AND DATA FRAME AND MARKET TREND ########################################

    ################################ SENDING FIRST SELL ORDER ##################################################################
    Call_Closing_Price, quote_call = Compute_token_Closing_price(Input_Strike_Call, "Call")
    Put_Closing_Price, quote_put = Compute_token_Closing_price(Input_Strike_Put, "Put")

    Call_Closing_Price_Hedges, quote_call_Hedges = Compute_token_Closing_price(Input_Strike_Call_Hedge, "Call")
    Put_Closing_Price_Hedges, quote_put_Hedges = Compute_token_Closing_price(Input_Strike_Put_Hedge, "Put")

    #################################  Writing the market status in the text file  ##############################################

    running_log = {}
    writing_market_status(running_log, "Running_log.txt")

    ##################################  Writing the market status in the text file  ###############################################

    limit_order_Sell(quote_call, Deployed_Size, Call_Closing_Price, Input_Strike_Call, "Call")
    limit_order_Sell(quote_put, Deployed_Size, Put_Closing_Price, Input_Strike_Put, "Put")

    ################################# SENDING FIRST SELL ORDER ##################################################################

    Order_execution_Check(Input_Strike_Call, Input_Strike_Put, quote_call_Hedges, quote_put_Hedges, quote_call,
                          quote_put, Input_Strike_Call_Hedge, Input_Strike_Put_Hedge)

    Trailing_SL()

elif Initial_day == 0 and Interrupt == 0:
    current_time = datetime.now()
    Present_time = current_time.strftime("%H:%M:%S")

    if Present_time<Start_time:
        time_diff_seconds = sleep_time_compute(Start_time)
        print(f"Waiting until {Start_time}...")
        time.sleep(time_diff_seconds)
        print("Starting Morning Code.....")

        pause()
        Morning_run()
        Trailing_SL()
    else:
        print("Starting Morning Code.....")
        Morning_run()
        Trailing_SL()

elif Interrupt == 1:
    print(f"Interrupt")
    console_output_log_recording(f"Interrupt")
    Trailing_SL()
else:
    pass