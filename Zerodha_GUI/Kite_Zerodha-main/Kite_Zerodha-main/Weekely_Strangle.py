from tkinter import *
import Intraday_live_data
import pandas as pd
from kite_trade import *
import os
import math
import ast
import subprocess
import date_time_format
import json


def limit_order_Placement_sell(Trading_symbol,Sell_Price):

    global enctoken
    kite = KiteApp(enctoken=enctoken)



    order = kite.place_order(variety=kite.VARIETY_REGULAR,
                         exchange=kite.EXCHANGE_NFO,
                         tradingsymbol=Trading_symbol,
                         transaction_type=kite.TRANSACTION_TYPE_SELL,
                         quantity=50,
                         product=kite.PRODUCT_NRML,
                         order_type=kite.ORDER_TYPE_LIMIT,
                         price=Sell_Price,
                         validity=kite.VALIDITY_DAY,
                         disclosed_quantity=None,
                         trigger_price=None,
                         squareoff=None,
                         stoploss=None,
                         trailing_stoploss=None,
                         tag="TradeViaPython")
    
    with open(path_algo_strangle+"Order_Info_Details","r") as file:
        order_id_info=json.load(file)

    if Trading_symbol[-2:]=="CE":
        order_id_info["Order_ID_CE_Sell"]=str(order)
    elif Trading_symbol[-2:]=="PE":
        order_id_info["Order_ID_PE_Sell"]=str(order)
    else:
        pass

    with open(path_algo_strangle+"Order_Info_Details", "w") as file:
        json.dump(order_id_info, file)

    print(f"Order ID: {order_id_info}")
    print(f"Placed Order price: {Sell_Price}")
    

def limit_order_Placement_buy(Trading_symbol,Buy_Price):

    global enctoken
    kite = KiteApp(enctoken=enctoken)
    global order_info
    global Buy_status
    global path_kite_main


    order = kite.place_order(variety=kite.VARIETY_REGULAR,
                         exchange=kite.EXCHANGE_NFO,
                         tradingsymbol=Trading_symbol,
                         transaction_type=kite.TRANSACTION_TYPE_BUY,
                         quantity=50,
                         product=kite.PRODUCT_NRML,
                         order_type=kite.ORDER_TYPE_LIMIT,
                         price=Buy_Price, 
                         validity=kite.VALIDITY_DAY,
                         disclosed_quantity=None,
                         trigger_price=None,
                         squareoff=None,
                         stoploss=None,
                         trailing_stoploss=None,
                         tag="TradeViaPython")
    
    with open(path_algo_strangle+"Order_Info_Details","r") as file:
        order_id_info=json.load(file)

    if Trading_symbol[-2:]=="CE":
        order_id_info["Order_ID_CE_Buy"]=str(order)
    elif Trading_symbol[-2:]=="PE":
        order_id_info["Order_ID_PE_Buy"]=str(order)
    else:
        pass

    with open(path_algo_strangle+"Order_Info_Details", "w") as file:
        json.dump(order_id_info, file)


def market_order_buy(Trading_symbol):

    global enctoken
    kite = KiteApp(enctoken=enctoken)
    global order_info
    global Buy_status
    global path_kite_main


    order = kite.place_order(variety=kite.VARIETY_REGULAR,
                         exchange=kite.EXCHANGE_NFO,
                         tradingsymbol=Trading_symbol,
                         transaction_type=kite.TRANSACTION_TYPE_BUY,
                         quantity=50,
                         product=kite.PRODUCT_NRML,
                         order_type=kite.ORDER_TYPE_MARKET,
                         price=None,
                         validity=kite.VALIDITY_DAY,
                         disclosed_quantity=None,
                         trigger_price=None,
                         squareoff=None,
                         stoploss=None,
                         trailing_stoploss=None,
                         tag="TradeViaPython")
    
def market_order_sell(Trading_symbol):

    global enctoken
    kite = KiteApp(enctoken=enctoken)
    global order_info
    global Buy_status
    global path_kite_main
    global order_id_info


    order = kite.place_order(variety=kite.VARIETY_REGULAR,
                         exchange=kite.EXCHANGE_NFO,
                         tradingsymbol=Trading_symbol,
                         transaction_type=kite.TRANSACTION_TYPE_SELL,
                         quantity=50,
                         product=kite.PRODUCT_NRML,
                         order_type=kite.ORDER_TYPE_MARKET,
                         price=None,
                         validity=kite.VALIDITY_DAY,
                         disclosed_quantity=None,
                         trigger_price=None,
                         squareoff=None,
                         stoploss=None,
                         trailing_stoploss=None,
                         tag="TradeViaPython")
    

    with open(path_algo_strangle+"Order_Info_Details","r") as file:
        order_id_info=json.load(file)

    if Trading_symbol[-2:]=="CE":
        order_id_info["Order_ID_CE_Sell"]=str(order)
    elif Trading_symbol[-2:]=="PE":
        order_id_info["Order_ID_PE_Sell"]=str(order)
    else:
        pass

    with open(path_algo_strangle+"Order_Info_Details", "w") as file:
        json.dump(order_id_info, file)

    print(f"Order ID: {order_id_info}")


def modify_order_sell_Limit(Order_ID,Price):

    global order_id_info
    global enctoken
    kite = KiteApp(enctoken=enctoken)

    kite.modify_order(variety=kite.VARIETY_REGULAR,
                    order_id=str(Order_ID),
                    parent_order_id=None,
                    quantity=50,
                    price=Price,
                    order_type=kite.ORDER_TYPE_LIMIT,
                    trigger_price=None,
                    validity=kite.VALIDITY_DAY,
                    disclosed_quantity=None)

# def market_order_buy_Straddel():
#     global token_straddel
#     global quote_straddel
#     global enctoken
#     kite = KiteApp(enctoken=enctoken)

#     buy_token=[token_straddel[2],token_straddel[3]]

#     for i in range(len(buy_token)):
#         while True:
#             market_order_buy(str(buy_token[i]))
#             x=kite.orders()
#             l1=len(x)
#             Status=x[l1-1]['status']

#             if Status=='COMPLETE':
#                 print("Buy Order Executed")
#                 break
#             else:
#                 print("Buy Order Not Executed")



def formtatted_date_calculation():
    from datetime import datetime

    expiry=expiry_date_entry.get()

    if Month_end_var.get()==0:
        parsed_date = datetime.strptime(expiry, '%d-%b-%Y')
        formatted_date = parsed_date.strftime('%y%m%d')
        char_list = list(formatted_date)
        Letter_to_insert="O"
        length=len(formatted_date)
        first=formatted_date[0:2]
        last=formatted_date[length-2:length]
        formatted_date=first+Letter_to_insert+last

        return formatted_date

    elif Month_end_var.get()==1:
        parsed_date = datetime.strptime(expiry, '%d-%b-%Y')
        formatted_date = parsed_date.strftime('%Y%b').upper()
        formatted_date=formatted_date[2:]

        return formatted_date

def Submit_Initial_Strangle():
    global expiry
    global name
    global token_straddel
    global quote_straddel
    global formatted_date
    global order_id_info


    Sell_CE_Strike_Price=int(CE_Initial_Strike_entry.get())
    Sell_PE_Strike_Price=int(PE_Initial_Strike_entry.get())

    if Sell_CE_Strike_Price>=Sell_PE_Strike_Price:
        Buy_CE_Strike_Price=Sell_CE_Strike_Price+600
        Buy_PE_Strike_Price=Sell_PE_Strike_Price-600

        formatted_date=formtatted_date_calculation()
        
        strike_price_list_CE=[Sell_CE_Strike_Price,Buy_CE_Strike_Price]
        strike_price_list_PE=[Sell_PE_Strike_Price,Buy_PE_Strike_Price]

        order_id_info["Token_Sell_CE"]=name+formatted_date+str(strike_price_list_CE[0])+"CE"
        order_id_info["Token_Sell_PE"]=name+formatted_date+str(strike_price_list_PE[0])+"PE"
        order_id_info["Token_Buy_CE"]=name+formatted_date+str(strike_price_list_CE[1])+"CE"
        order_id_info["Token_Buy_PE"]=name+formatted_date+str(strike_price_list_PE[1])+"PE"
        order_id_info["Buy_Strike_Price_CE"]=Buy_CE_Strike_Price
        order_id_info["Sell_Strike_Price_CE"]=Sell_CE_Strike_Price
        order_id_info["Sell_Strike_Price_PE"]=Sell_PE_Strike_Price
        order_id_info["Buy_Strike_Price_PE"]=Buy_PE_Strike_Price

        with open(path_algo_strangle+"Order_Info_Details","w") as file:
            json.dump(order_id_info,file)

        token_straddel=[]

        for i in range(len(strike_price_list_CE)):
            quote_CE=name+formatted_date+str(strike_price_list_CE[i])+"CE"
            quote_PE=name+formatted_date+str(strike_price_list_PE[i])+"PE"
            token_straddel.append(quote_CE)
            token_straddel.append(quote_PE)


        quote_straddel=[]

        for j in range(len(token_straddel)):
            atm_token_ce=kite.ltp("NFO:"+token_straddel[j])
            ATM_Token=atm_token_ce["NFO:"+token_straddel[j]]['instrument_token']
            quote_straddel.append(ATM_Token)

        print(token_straddel)
        print(quote_straddel)
        message_label.config(text="Correct Strike Price Entry")

    else:
        message_label.config(text="Please Enter Correct Strike Price")
    

    # limit_sell_order_update()

def Price_computation(quote):
    global enctoken
    import datetime

    kite = KiteApp(enctoken=enctoken)

    instrument_token_CE = quote

    from_datetime = datetime.datetime.now() - datetime.timedelta(days=1)     # From last & days
    to_datetime = datetime.datetime.now()
    interval = "minute"
    content_CE=kite.historical_data(instrument_token_CE, from_datetime, to_datetime, interval, continuous=False, oi=True)
    length=len(content_CE)
    closing_price=content_CE[length-2]["close"]

    print(f"Closing Price: {closing_price}")

    return closing_price

def limit_sell_order_update():
    import time
    global token_straddel
    global quote_straddel
    global enctoken
    global order_id_info

    kite = KiteApp(enctoken=enctoken)

    # price_CE=Price_computation(quote_straddel[0])
    # limit_order_Placement_sell(str(token_straddel[0]),price_CE)

    # price_PE=Price_computation(quote_straddel[1])
    # limit_order_Placement_sell(str(token_straddel[1]),price_PE)

    market_order_sell(token_straddel[0])
    market_order_sell(token_straddel[1])
    market_order_buy(token_straddel[2])
    market_order_buy(token_straddel[3])



    # while True:
    #     x=kite.orders()
    #     l1=len(x)
    #     Status_CE=x[l1-2]['status']
    #     Status_PE=x[l1-1]['status']

    #     if Status_CE=='COMPLETE' and Status_PE=='COMPLETE':
    #         print("Sell order Placed")
    #         break
    #     elif Status_CE=='OPEN' and Status_PE=='COMPLETE':
    #         price_CE=Price_computation(quote_straddel[0])
    #         order_id=order_id_info["Order_ID_CE_Sell"]
    #         modify_order_sell_Limit(price_CE,order_id)
    #         print("Call Sell order Not Placed")
    #     elif Status_PE=='OPEN' and Status_CE=='COMPLETE':
    #         price_PE=Price_computation(quote_straddel[1])
    #         order_id=order_id_info["Order_ID_PE_Sell"]
    #         modify_order_sell_Limit(price_PE,order_id)
    #         print("Put Sell order Not Placed")
    #     elif Status_PE=='OPEN' and Status_CE=='OPEN':
    #         price_CE=Price_computation(quote_straddel[0])
    #         order_id=order_id_info["Order_ID_CE_Sell"]
    #         modify_order_sell_Limit(price_CE,order_id)

    #         price_PE=Price_computation(quote_straddel[1])
    #         order_id=order_id_info["Order_ID_PE_Sell"]
    #         modify_order_sell_Limit(price_PE,order_id)
    #         print("Sell order Not Placed")
    #     else:
    #         print("It is stucked here")

    #     time.sleep(60)

    # market_order_buy_Straddel()


def refresh_command():
    Month_end_var.set(0)
    Delta_neutral_cheking.set(0)
    Delta_neutral_start_var.set(0)
    Sentiment_var.set(0)

    CE_Initial_Strike_entry.delete(0,END)
    PE_Initial_Strike_entry.delete(0,END)
    expiry_date_entry.delete(0,END)


##########################  Delta Neutral Code ################################################


def instantinious_price_computation_list(Strike_price):
    global name
    global enctoken
    import datetime

    kite = KiteApp(enctoken=enctoken)

    quote_CE=name+formatted_date+str(Strike_price)+"CE"
    quote_PE=name+formatted_date+str(Strike_price)+"PE"

    atm_token_ce=kite.ltp("NFO:"+quote_CE)
    ATM_Token_CE=atm_token_ce["NFO:"+quote_CE]['instrument_token']

    atm_token_pe=kite.ltp("NFO:"+quote_PE)
    ATM_Token_PE=atm_token_pe["NFO:"+quote_PE]['instrument_token']

    instrument_token_CE = ATM_Token_CE
    instrument_token_PE = ATM_Token_PE


    from_datetime = datetime.datetime.now() - datetime.timedelta(days=2)     # From last & days
    to_datetime = datetime.datetime.now()
    interval = "minute"
    content_CE=kite.historical_data(instrument_token_CE, from_datetime, to_datetime, interval, continuous=False, oi=True)
    content_PE=kite.historical_data(instrument_token_PE, from_datetime, to_datetime, interval, continuous=False, oi=True)

    length_ce=len(content_CE)
    length_pe=len(content_PE)

    if length_ce==0:
        closing_price_pe=content_PE[length_pe-1]["close"]
        closing_price_ce=0
    elif length_pe==0:
        closing_price_ce=content_CE[length_ce-1]["close"]
        closing_price_pe=0
    else:    
        closing_price_ce=content_CE[length_ce-1]["close"]
        closing_price_pe=content_PE[length_pe-1]["close"]


    return closing_price_ce, closing_price_pe


def find_closest_indices(input_num, num_list):
    smaller_index = None
    greater_index = None
    min_diff_smaller = float('inf')
    min_diff_greater = float('inf')
    
    for i in range(len(num_list)):
        diff = input_num - num_list[i]
        
        if diff > 0 and diff < min_diff_greater:
            min_diff_greater = diff
            greater_index = i
        elif diff < 0 and abs(diff) < min_diff_smaller:
            min_diff_smaller = abs(diff)
            smaller_index = i
    
    return smaller_index, greater_index


def Delta_Neutral_Start(token_DN,token_Square_Off):
    if Delta_neutral_start_var.get()==3:
        final_new=Intraday_live_data.getoptionchain(name,expiry)
        final_new.reset_index(drop=True, inplace=True)

        formatted_date=formtatted_date_calculation()

        Strike_Price_List=final_new['strikePrice'].tolist()

        closing_price_ce=[]
        closing_price_pe=[]

        for i in range(len(Strike_Price_List)):
            Closing_price_ce,Closing_price_pe=instantinious_price_computation_list(Strike_Price_List[i])
            closing_price_ce.append(Closing_price_ce)
            closing_price_pe.append(Closing_price_pe)

        DN_Segment=token_DN[-2:]
        DN_Sell=int(token_DN[-7:-2])
        Squr_off_sell=int(token_Square_Off[-7:-2])

        print(closing_price_ce)
        print(closing_price_pe)

        print(f"Delta neutral segment {DN_Segment}")
        print(f"Delta Neutral Strike price {DN_Sell}")
        print(f"Square off Strike price {Squr_off_sell}")

        if DN_Segment=="CE":
            DN_call_price,Put_price=instantinious_price_computation_list(DN_Sell)

            greater_idx, lesser_idx = find_closest_indices(DN_call_price,closing_price_pe)
            Strike_Directional_Sell=Strike_Price_List[greater_idx]
            Buy_Neutral=Strike_Directional_Sell-600
            Strike_neutral_sell=Strike_Price_List[lesser_idx]

            print(f"Delta Neutral for Put Strike for neutral sentiment: {Strike_neutral_sell}")
            print(f"Delta Neutral for Put Strike for directional sentiment: {Strike_Directional_Sell}")

            Buy_Directional=Strike_Directional_Sell+600

            Squre_off_Sell_pe=name+formatted_date+str(Squr_off_sell)+"PE"
            Squr_off_buy=Squr_off_sell-600
            Squre_off_Buy_pe=name+formatted_date+str(Squr_off_buy)+"PE"

            # market_order_buy(Squre_off_Sell_pe)
            # market_order_sell(Squre_off_Buy_pe)

            if Sentiment_var.get()==4:
                token_DN_sell_PE=name+formatted_date+str(Strike_neutral_sell)+"PE"
                token_DN_buy_PE=name+formatted_date+str(Buy_Neutral)+"PE"
                # market_order_buy(token_DN_sell_PE)
                # market_order_sell(token_DN_buy_PE)
                Sentiment_var.set(0)
                Delta_neutral_start_var.set(0)

            elif Sentiment_var.get()==5:
                token_DN_sell_PE=name+formatted_date+str(Strike_Directional_Sell)+"PE"
                token_DN_buy_PE=name+formatted_date+str(Buy_Directional)+"PE"
                # market_order_buy(token_DN_sell_PE)
                # market_order_sell(token_DN_buy_PE)  
                Sentiment_var.set(0)
                Delta_neutral_start_var.set(0)    
            else:
                pass          

        elif DN_Segment=="PE":
            call_price,DN_put_price=instantinious_price_computation_list(DN_Sell)



            greater_idx, lesser_idx = find_closest_indices(DN_put_price,closing_price_ce)
            Strike_neutral_sell=Strike_Price_List[lesser_idx]
            Buy_Neutral=Strike_neutral_sell+600
            Strike_Directional_sell=Strike_Price_List[greater_idx]
            Buy_Directional=Strike_Directional_sell+600      

            print(f"Delta Neutral for Put Strike for neutral sentiment: {Strike_neutral_sell}")
            print(f"Delta Neutral for Put Strike for directional sentiment: {Strike_Directional_sell}")

            Squre_off_Sell_ce=name+formatted_date+str(Squr_off_sell)+"CE"
            Squr_off_buy=Squr_off_sell+600
            Squre_off_Buy_ce=name+formatted_date+str(Squr_off_buy)+"CE"    

            # market_order_buy(Squre_off_Sell_ce)
            # market_order_sell(Squre_off_Buy_ce)  

            if Sentiment_var.get()==4:
                token_DN_sell_CE=name+formatted_date+str(Strike_neutral_sell)+"CE"
                token_DN_buy_CE=name+formatted_date+str(Buy_Neutral)+"CE"
                # market_order_buy(token_DN_sell_CE)
                # market_order_sell(token_DN_buy_CE)
                Sentiment_var.set(0)
                Delta_neutral_start_var.set(0)

            elif Sentiment_var.get()==5:
                token_DN_sell_CE=name+formatted_date+str(Strike_Directional_Sell)+"CE"
                token_DN_buy_CE=name+formatted_date+str(Buy_Directional)+"CE"
                # market_order_buy(token_DN_sell_CE)
                # market_order_sell(token_DN_buy_CE)  
                Sentiment_var.set(0)
                Delta_neutral_start_var.set(0)    
            else:
                pass   

        else:
            pass
    else:
        pass



def Delta_Neutral_Checking():
    global time_list
    global enctoken
    import datetime

    with open(path_algo_strangle+"Order_Info_Details","r") as file:
        order_id_info=json.load(file)

    token_sell_CE=order_id_info["Token_Sell_CE"]
    token_sell_PE=order_id_info["Token_Sell_PE"]
    # Buy_strike_Price_CE=order_id_info["Buy_Strike_Price_CE"]
    # Sell_strike_Price_CE=order_id_info["Sell_Strike_Price_CE"]
    # Sell_strike_Price_PE=order_id_info["Sell_Strike_Price_PE"]
    # Buy_strike_Price_PE=order_id_info["Buy_Strike_Price_PE"]


    kite = KiteApp(enctoken=enctoken)

    atm_token_ce=kite.ltp("NFO:"+token_sell_CE)
    ATM_Token_CE=atm_token_ce["NFO:"+token_sell_CE]['instrument_token']

    atm_token_pe=kite.ltp("NFO:"+token_sell_PE)
    ATM_Token_PE=atm_token_pe["NFO:"+token_sell_PE]['instrument_token']


    instrument_token_CE = ATM_Token_CE
    instrument_token_PE = ATM_Token_PE

    from_datetime = datetime.datetime.now() - datetime.timedelta(days=2)     # From last & days
    to_datetime = datetime.datetime.now()
    interval = "5minute"
    content_CE=kite.historical_data(instrument_token_CE, from_datetime, to_datetime, interval, continuous=False, oi=True)
    content_PE=kite.historical_data(instrument_token_PE, from_datetime, to_datetime, interval, continuous=False, oi=True)
    length_ce=len(content_CE)
    length_pe=len(content_PE)
    print(length_ce)
    print(length_pe)
    closing_price_ce=content_CE[length_ce-2]["close"]
    closing_price_pe=content_PE[length_pe-2]["close"]

    if closing_price_ce>closing_price_pe and closing_price_ce>=(2*closing_price_pe):
        Delta_Neutral_Start(token_sell_CE,token_sell_PE)
        print(closing_price_ce)
        print(closing_price_pe)
        print(f"DN token {token_sell_CE} Square off token {token_sell_PE}")
        Delta_Neutral_Status_message_label.config(text="Delta Neutral Required",bg='red')
        DN_Ratio_info.config(text=f"CE/PE ratio:{round(closing_price_ce/closing_price_pe,2)}")

        # return "CALL",Buy_strike_Price_CE, Sell_strike_Price_CE, ATM_Token_PE, Buy_strike_Price_PE, Sell_strike_Price_PE
    
    elif closing_price_pe>closing_price_ce and closing_price_pe>=(2*closing_price_ce):
        Delta_Neutral_Start(token_sell_PE,token_sell_CE)
        print(closing_price_ce)
        print(closing_price_pe)
        print(f"DN token {token_sell_PE} Square off token {token_sell_CE}")
        Delta_Neutral_Status_message_label.config(text="Delta Neutral Required",bg='red')
        DN_Ratio_info.config(text=f"PE/CE ratio:{round(closing_price_pe/closing_price_ce,2)}")

        # return "PUT", Buy_strike_Price_PE, Sell_strike_Price_PE, ATM_Token_CE,Buy_strike_Price_CE, Sell_strike_Price_CE
    else:
        Delta_Neutral_Status_message_label.config(text="Delta Neutral Not Required",bg='green')
        DN_Ratio_info.config(text=f"PE/CE ratio:{round(closing_price_pe/closing_price_ce,2)}")

    schedule()

def schedule():
    global time_list
    import time
    global run

    times_to_execute=time_list

    # Get the current time
    current_time = datetime.now().strftime("%H:%M:%S")

    # Find the next time in the list that is greater than the current time
    next_time = None
    for t in times_to_execute:
        if t > current_time:
            next_time = t
            break

    if next_time:
        # Calculate the time difference in seconds
        time_difference = (datetime.strptime(next_time, "%H:%M:%S") - datetime.strptime(current_time, "%H:%M:%S")).total_seconds()

        # Schedule the next execution of update_figures() at the calculated time difference
        run=run+1
        print(f"Total run completed {run}")
        GUI.after(int(time_difference * 1000), Delta_Neutral_Checking)
        # time.sleep(int(time_difference))
        # Delta_Neutral_Checking()

    else:
        # No more times in the list for today, you can handle this case as needed
        print("No more times to execute today")

######################################  Auto Hedging  ##################################################

def Auto_Hedging_start():
    Sell_CE_Strike_Price=int(Hedging_CE_Initial_Strike_entry.get())
    token_CE=name+formatted_date+str(Sell_CE_Strike_Price)+"CE"
    Sell_PE_Strike_Price=int(Hedging_PE_Initial_Strike_entry.get())
    token_PE=name+formatted_date+str(Sell_PE_Strike_Price)+"PE"

    CE_price_CE,PE_price_CE=instantinious_price_computation_list(Sell_CE_Strike_Price)
    CE_price_PE,PE_price_PE=instantinious_price_computation_list(Sell_PE_Strike_Price)

    if CE_price_CE>(1.3*PE_price_PE):
        Delta_Neutral_Start(token_CE,token_PE)
        lh3.config(text="Status: DN Required for CE")
    elif PE_price_PE>(1.3*CE_price_CE):
        Delta_Neutral_Start(token_PE,token_CE)
        lh3.config(text="Status: DN Required for PE")
    else:
        pass


def Auto_Hedging_submit():
    import time
    current_time = time.strftime('%H:%M:%S')

    if current_time < '15:25:00':
        GUI.after(1000, Auto_Hedging_submit)
    else:
        Auto_Hedging_start()

path_main="D:/ashu/Finance/algo_trading/Zerodha_GUI/Kite_Zerodha-main/Kite_Zerodha-main/"
path_algo_strangle="D:/ashu/Finance/algo_trading/Zerodha_GUI/Algo_Strangle/"

run=0

df=pd.read_csv(path_main+"Enctoke_Expiry_month_end_info.csv")
content_enctoken=df.iloc[0,0]

enctoken = content_enctoken

kite = KiteApp(enctoken=enctoken)

with open(path_main+"expiry_date.txt",'r') as file:
    content_expiry_date=file.read()

expiry=content_expiry_date

name="NIFTY"
token_straddel=[]
quote_straddel=[]
order_id_info={}
time_list = []


GUI=Tk()

width=750
height=544
GUI.geometry(f'{str(width)}x{str(height)}')
GUI.maxsize(800, 600)

GUI.title("Archu Strangle GUI")

Strangle_Frame=Frame(GUI,bg="grey",borderwidth=6,relief=SUNKEN)
Strangle_Frame.grid(row=0, column=0, padx=10, pady=20)

l0=Label(Strangle_Frame,text="Initialization",font="comicsansms 14 bold",bg="green")
l0.grid(row=0,column=0,padx=10,pady=10)

l1=Label(Strangle_Frame,text="Sell Strike CE",font="comicsansms 10 bold")
l1.grid(row=1,column=0,padx=10,pady=10)

l2=Label(Strangle_Frame,text="Sell Strike PE",font="comicsansms 10 bold")
l2.grid(row=2,column=0,padx=10,pady=10)

CE_Initial_Strike_entry=Entry(Strangle_Frame)
CE_Initial_Strike_entry.grid(row=1,column=1)

PE_Initial_Strike_entry=Entry(Strangle_Frame)
PE_Initial_Strike_entry.grid(row=2,column=1)

Initial_Strangle_submit_Button=Button(Strangle_Frame,text="Submit Order",font="comicsansms 14 bold",bg="yellow",command=Submit_Initial_Strangle)
Initial_Strangle_submit_Button.grid(row=0,column=1,padx=5,pady=10)

l3=Label(Strangle_Frame,text="Expiry day\n(dd-mm-yyyy)\nExp:19-Oct-2023",font="comicsansms 10 bold")
l3.grid(row=3,column=0,padx=10,pady=10)

expiry_date_entry=Entry(Strangle_Frame)
expiry_date_entry.grid(row=3,column=1)

Month_end_var=IntVar()


Month_button=Radiobutton(Strangle_Frame,text="Month End",font="comicsansms 14 bold",variable=Month_end_var,value=1)
Month_button.grid(row=0,column=3,padx=10,pady=10)

Delta_neutral_cheking=IntVar()

Delta_Neutral=Radiobutton(Strangle_Frame,text="DN Checking",font="comicsansms 14 bold",variable=Delta_neutral_cheking,value=2,command=Delta_Neutral_Checking)
Delta_Neutral.grid(row=0,column=4)

Refresh_Button=Button(Strangle_Frame,text="Refresh",font="comicsansms 14 bold",bg="yellow",command=refresh_command)
Refresh_Button.grid(row=1,column=3,padx=5,pady=10)


Delta_neutral_start_var=IntVar()

Delta_Neutral_enable=Radiobutton(Strangle_Frame,text="DN Start",font="comicsansms 14 bold",variable=Delta_neutral_start_var,value=3)
Delta_Neutral_enable.grid(row=1,column=4,padx=5,pady=10)


Delta_neutral_start_var=IntVar()

Delta_Neutral_enable=Radiobutton(Strangle_Frame,text="DN Start",font="comicsansms 14 bold",variable=Delta_neutral_start_var,value=3)
Delta_Neutral_enable.grid(row=1,column=4,padx=5,pady=10)

Sentiment_var=IntVar()

Delta_Neutral_Sentiment_neutral=Radiobutton(Strangle_Frame,text="Neutral\nSentiment",font="comicsansms 10 bold",variable=Sentiment_var,value=4)
Delta_Neutral_Sentiment_directional=Radiobutton(Strangle_Frame,text="Directional\nSentiment",font="comicsansms 10 bold",variable=Sentiment_var,value=5)
Delta_Neutral_Sentiment_neutral.grid(row=2,column=3,padx=5,pady=10)
Delta_Neutral_Sentiment_directional.grid(row=2,column=4,padx=5,pady=10)

Delta_Neutral_Status_message=Label(Strangle_Frame,text="Delta Neutral\n Status Message",font="comicsansms 10 bold")
Delta_Neutral_Status_message.grid(row=4,column=0,padx=10,pady=10)

Delta_Neutral_Status_message_label = Label(Strangle_Frame, text="", font="comicsansms 10 bold")
Delta_Neutral_Status_message_label.grid(row=4,column=1,padx=10,pady=10)

DN_Ratio_Running=Label(Strangle_Frame,text="Delta Neutral Ratio",font="comicsansms 10 bold")
DN_Ratio_Running.grid(row=5,column=0,padx=10,pady=10)

DN_Ratio_info= Label(Strangle_Frame, text="", font="comicsansms 10 bold")
DN_Ratio_info.grid(row=5,column=1,padx=10,pady=10)


hedging_label=Label(Strangle_Frame,text="Hedging", font="comicsansms 14 bold",bg='green')
hedging_label.grid(row=3,column=3,padx=5)


lh1=Label(Strangle_Frame,text="Sell Strike CE",font="comicsansms 10 bold")
lh1.grid(row=4,column=3,padx=5)

lh2=Label(Strangle_Frame,text="Sell Strike PE",font="comicsansms 10 bold")
lh2.grid(row=5,column=3,padx=5)

Hedging_CE_Initial_Strike_entry=Entry(Strangle_Frame)
Hedging_CE_Initial_Strike_entry.grid(row=4,column=4)

Hedging_PE_Initial_Strike_entry=Entry(Strangle_Frame)
Hedging_PE_Initial_Strike_entry.grid(row=5,column=4)

Auto_hedging_turn_on=IntVar()

lh3=Label(Strangle_Frame,text="Status: DN Not Required",font="comicsansms 10 bold")
lh3.grid(row=6,column=3)

Hedging_Submit_Button=Button(Strangle_Frame,text="Submit",font="comicsansms 12 bold",bg="yellow",command=Auto_Hedging_submit)
Hedging_Submit_Button.grid(row=6,column=4)


#############################################  Other Processing  ##############################################
from datetime import datetime, timedelta

# Define the start and end times
start_time = datetime.strptime("12:16:00", "%H:%M:%S")
end_time = datetime.strptime("18:30:00", "%H:%M:%S")

# Define the interval (3 minutes)
interval = timedelta(minutes=5)

# Initialize an empty list to store the generated times


# Generate the times
current_time = start_time
while current_time <= end_time:
    time_list.append(current_time.strftime("%H:%M:%S"))
    current_time += interval


#############################################  Other Processing  ##############################################


#################################  Error Message Dialog Box  ###############################################
error_message_frame=Frame(GUI,bg="grey",borderwidth=6,relief=SUNKEN)
error_message_frame.grid(row=1, column=0)

error_message =Label(error_message_frame,text="Error message",font="comicsansms 12 bold",fg="red")
error_message.grid(row=0,column=0)

message_label = Label(error_message_frame, text="", font=("Helvetica", 12))
message_label.grid(row=1,column=0)
#################################  Error Message Dialog Box  ###############################################


GUI.mainloop()