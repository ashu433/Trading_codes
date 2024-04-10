import pandas as pd
from kite_trade import *
from datetime import datetime,timedelta
import ast
import time
import numpy as np

def console_output_log_recording(content):
    current_time = datetime.now()

    current_time_str = current_time.strftime("%H:%M:%S")

    with open(Path_backtest_Report+'Console_output_log_file.txt', 'a') as file:
        file.write(f"{current_time_str}: {content}.\n")



def limit_order_Sell(Quote,Size,price,Strike,Right):
    global enctoken
    kite = KiteApp(enctoken=enctoken)
    global order_info

    Initial_DF=pd.read_csv(Path_backtest_Report+"Running_Status_of_trade.csv")


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
                         squareoff=None,
                         stoploss=None,
                         trailing_stoploss=None,
                         tag="TradeViaPython")
    x=kite.orders()
    l1=len(x)
    Order_ID=x[l1-1]['order_id']
    Date_time=x[l1-1]['order_timestamp']
    Status_present=x[l1-1]['status']
    date, time = Date_time.split()
    Stop_Loss=2*price

    Cleaning_lists()

    Type_list.append("Sell")
    Initial_price_list.append(price)
    order_id.append(Order_ID)
    Date.append(date)
    Time.append(time)
    Status_list.append(Status_present)
    Strike_list.append(Strike)
    Trailing_SL_list.append(Stop_Loss)

    if Right=="Call":
        Right_list.append("Call")
    elif Right=="Put":
        Right_list.append("Put")

    with open(Path_backtest_Report+'Running_log_file.txt', 'a') as file:
        file.write(f"Date: {date} Time: {time} Strike: {Strike} Initiation Price: {price} type of Order: Limit Order Sell.\n")

    data={"Date":Date,"Time":Time,"Strike":Strike_list,"Right":Right_list,"Order_ID":order_id,"Status":Status_list,"Type":Type_list,"Initial Price":Initial_price_list,"Trailing SL":Trailing_SL_list}
    new_df=pd.DataFrame(data)
    Initial_DF=pd.concat([Initial_DF, new_df], axis=0)

    Initial_DF.to_csv(Path_backtest_Report+"Running_Status_of_trade.csv",index=False)

def limit_order_buy(Quote,Size,price):
    global enctoken
    kite = KiteApp(enctoken=enctoken)
    global order_info


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
                         squareoff=None,
                         stoploss=None,
                         trailing_stoploss=None,
                         tag="TradeViaPython")

    ## Save the order info in the log list

def Market_order_Buy(Quote,Size,Strike,Right,Buy_type):
    global enctoken
    kite = KiteApp(enctoken=enctoken)
    global order_info

    Initial_DF=pd.read_csv(Path_backtest_Report+"Running_Status_of_trade.csv")


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
                         squareoff=None,
                         stoploss=None,
                         trailing_stoploss=None,
                         tag="TradeViaPython")
    
    x=kite.orders()
    l1=len(x)
    Order_ID=x[l1-1]['order_id']
    Date_time=x[l1-1]['order_timestamp']
    Status_present=x[l1-1]['status']
    date, time = Date_time.split()
    price=x[l1-1]["average_price"]
    Stop_Loss=0

    Cleaning_lists()

    Type_list.append(Buy_type)
    Initial_price_list.append(price)
    order_id.append(Order_ID)
    Date.append(date)
    Time.append(time)
    Status_list.append(Status_present)
    Strike_list.append(Strike)
    Trailing_SL_list.append(Stop_Loss)

    if Right=="Call":
        Right_list.append("Call")
    elif Right=="Put":
        Right_list.append("Put")

    with open(Path_backtest_Report+'Running_log_file.txt', 'a') as file:
        file.write(f"Date: {date} Time: {time} Strike: {Strike} Market Price: {price} type of Order: Market Order Buy.\n")

    data={"Date":Date,"Time":Time,"Strike":Strike_list,"Right":Right_list,"Order_ID":order_id,"Status":Status_list,"Type":Type_list,"Initial Price":Initial_price_list,"Trailing SL":Trailing_SL_list}
    new_df=pd.DataFrame(data)
    Initial_DF=pd.concat([Initial_DF, new_df], axis=0)

    Initial_DF.to_csv(Path_backtest_Report+"Running_Status_of_trade.csv",index=False)

def Cleaning_lists():
    global Date,Time,Strike_list,Right_list,order_id,Status_list,Type_list,Initial_price_list,Trailing_SL_list

    Date=[]
    Time=[]
    Strike_list=[]
    Right_list=[]
    order_id=[]
    Status_list=[]
    Type_list=[]
    Initial_price_list=[]
    Trailing_SL_list=[]

def pause(duration=10):
    """Pause execution for the specified duration in seconds."""
    time.sleep(duration)

def Market_order_Sell(Quote,Size,Strike,Right,Sell_type):
    global enctoken
    kite = KiteApp(enctoken=enctoken)
    global order_info

    Initial_DF=pd.read_csv(Path_backtest_Report+"Running_Status_of_trade.csv")

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
                         squareoff=None,
                         stoploss=None,
                         trailing_stoploss=None,
                         tag="TradeViaPython")
    
    x=kite.orders()
    l1=len(x)
    Order_ID=x[l1-1]['order_id']
    Date_time=x[l1-1]['order_timestamp']
    Status_present=x[l1-1]['status']
    date, time = Date_time.split()
    price=x[l1-1]["average_price"]
    Stop_Loss=0

    Cleaning_lists()

    Type_list.append(Sell_type)
    Initial_price_list.append(price)
    order_id.append(Order_ID)
    Date.append(date)
    Time.append(time)
    Status_list.append(Status_present)
    Strike_list.append(-Strike)
    Trailing_SL_list.append(Stop_Loss)

    if Right=="Call":
        Right_list.append("Call")
    elif Right=="Put":
        Right_list.append("Put")

    with open(Path_backtest_Report+'Running_log_file.txt', 'a') as file:
        file.write(f"Date: {date} Time: {time} Strike: {Strike} Market Price: {price} type of Order: Market Order Sell.\n")

    data={"Date":Date,"Time":Time,"Strike":Strike_list,"Right":Right_list,"Order_ID":order_id,"Status":Status_list,"Type":Type_list,"Initial Price":Initial_price_list,"Trailing SL":Trailing_SL_list}
    new_df=pd.DataFrame(data)
    Initial_DF=pd.concat([Initial_DF, new_df], axis=0)

    Initial_DF.to_csv(Path_backtest_Report+"Running_Status_of_trade.csv",index=False)


def Modify_SL_Order(OID,Size,Price,type_of_modification,Order_Type):
    global order_info
    
    global enctoken
    kite = KiteApp(enctoken=enctoken)

    Initial_DF=pd.read_csv(Path_backtest_Report+"Running_Status_of_trade.csv")

    if Order_Type=="Limit":
        type_of_order=kite.ORDER_TYPE_LIMIT
        Triggering_price=None
    elif Order_Type=="SL Limit":
        type_of_order=kite.ORDER_TYPE_SL
        Triggering_price=Price-0.05
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
    
    Index = Initial_DF.index[(Initial_DF['Order_ID'] == OID)].tolist()
    Index=Index[0]
    Initial_DF.loc[Index,type_of_modification]=Price
    Strike_at_present=Initial_DF.loc[Index,"Strike"]

    if type_of_modification=="Trailing SL":
        Index_new = Initial_DF.index[(Initial_DF['Strike'] == -Strike_at_present)].tolist()
        Index_new=Index_new[0]
        Initial_DF.loc[Index_new,type_of_modification]=Price
    else:
        pass

    x=kite.orders()
    l1=len(x)
    Date_time=x[l1-1]['order_timestamp']
    date, time = Date_time.split()

    with open(Path_backtest_Report+'Running_log_file.txt', 'a') as file:
        file.write(f"Date: {date} Time: {time} Strike: {Strike_at_present} Price: {Price} type of modification {type_of_modification} and order type {Order_Type}.\n")

    Initial_DF.to_csv(Path_backtest_Report+"Running_Status_of_trade.csv",index=False)


def SL_Initiate_order(Quote,Size,SL_price,SL_Trig_price,Strike,Right):
    global enctoken
    kite = KiteApp(enctoken=enctoken)
    global order_info
    
    Initial_DF=pd.read_csv(Path_backtest_Report+"Running_Status_of_trade.csv")

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
                         squareoff=None,
                         stoploss=None,
                         trailing_stoploss=None,
                         tag="TradeViaPython")
    
    x=kite.orders()
    l1=len(x)
    Order_ID=x[l1-1]['order_id']
    Date_time=x[l1-1]['order_timestamp']
    Status_present="TRIGGER PENDING"
    date, time = Date_time.split()

    Cleaning_lists()

    Type_list.append("Buy")
    Initial_price_list.append(SL_price)
    order_id.append(Order_ID)
    Date.append(date)
    Time.append(time)
    Status_list.append(Status_present)
    Strike_list.append(-Strike)
    Trailing_SL_list.append(SL_price)

    if Right=="Call":
        Right_list.append("Call")
    elif Right=="Put":
        Right_list.append("Put")

    with open(Path_backtest_Report+'Running_log_file.txt', 'a') as file:
        file.write(f"Date: {date} Time: {time} Strike: {Strike} Stop Loss Price: {SL_price} type of Order: Stop Loss Order.\n")

    data={"Date":Date,"Time":Time,"Strike":Strike_list,"Right":Right_list,"Order_ID":order_id,"Status":Status_list,"Type":Type_list,"Initial Price":Initial_price_list,"Trailing SL":Trailing_SL_list}
    new_df=pd.DataFrame(data)
    Initial_DF=pd.concat([Initial_DF, new_df], axis=0)

    Initial_DF.to_csv(Path_backtest_Report+"Running_Status_of_trade.csv",index=False)

def cancel_order(Order_ID):

    global order_info
    global enctoken
    kite = KiteApp(enctoken=enctoken)

    Initial_DF=pd.read_csv(Path_backtest_Report+"Running_Status_of_trade.csv")

    kite.cancel_order(variety=kite.VARIETY_REGULAR,
                  order_id=Order_ID,
                  parent_order_id=None)
    
    Index = Initial_DF.index[(Initial_DF['Order_ID'] == Order_ID)].tolist()
    Index=Index[0]
    Strike=Initial_DF.loc[Index,"Strike"]
    Initial_DF.loc[Index,"Status"]="CANCELLED"

    x=kite.orders()
    l1=len(x)
    Date_time=x[l1-1]['order_timestamp']
    date, time = Date_time.split()

    with open(Path_backtest_Report+'Running_log_file.txt', 'a') as file:
        file.write(f"Date: {date} Time: {time} Strike: {Strike} type of Order: Cancelled Order.\n")


    Initial_DF.to_csv(Path_backtest_Report+"Running_Status_of_trade.csv",index=False)

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

def Compute_token_Closing_price(Strike,Right,time=5):
    global path_main
    from datetime import datetime


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
        quote_CE=Segment+modified_date+str(Strike)+"CE"
        atm_token_ce=kite.ltp("NFO:"+quote_CE)
        ATM_Token_CE=atm_token_ce["NFO:"+quote_CE]['instrument_token']




        import datetime

        from_datetime = datetime.datetime.now() - datetime.timedelta(days=1)     # From last & days
        to_datetime = datetime.datetime.now()

        if time==1:
            interval = "minute"
        elif time==5:
            interval="5minute"
        else:
            pass

        content_CE=kite.historical_data(ATM_Token_CE, from_datetime, to_datetime, interval, continuous=False, oi=True)
        length=len(content_CE)
        Content_CE=str(content_CE[length-2])
        cleaned_contents_CE = Content_CE.replace("datetime.datetime", "").replace(", tzinfo=tzoffset(None, 19800)", "")
        data_CE = ast.literal_eval(cleaned_contents_CE)

        closing_price_CE=data_CE['close']

        return closing_price_CE, quote_CE
    
    elif Right=="Put":
        quote_PE=Segment+modified_date+str(Strike)+"PE"
        atm_token_pe=kite.ltp("NFO:"+quote_PE)
        ATM_Token_PE=atm_token_pe["NFO:"+quote_PE]['instrument_token']

        Strike_list.append(Strike)
        Right_list.append(Right)        

        import datetime

        from_datetime = datetime.datetime.now() - datetime.timedelta(days=1)     # From last & days
        to_datetime = datetime.datetime.now()

        if time==1:
            interval = "minute"
        elif time==5:
            interval="5minute"
        else:
            pass
        content_PE=kite.historical_data(ATM_Token_PE, from_datetime, to_datetime, interval, continuous=False, oi=True)
        length=len(content_PE)
        Content_PE=str(content_PE[length-2])
        cleaned_contents_PE = Content_PE.replace("datetime.datetime", "").replace(", tzinfo=tzoffset(None, 19800)", "")
        data_PE = ast.literal_eval(cleaned_contents_PE)

        closing_price_PE=data_PE['close']

        return closing_price_PE, quote_PE       


def closest_time(current_time_str,time_list_obs):
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
    global enctoken
    kite = KiteApp(enctoken=enctoken)

    Log=kite.orders()
    order_id_to_find = str(Order_ID_current)

    # Initialize index variable
    index = None

    # Iterate through the list and find the index of the dictionary with the given order_id
    for i, item in enumerate(Log):
        if item.get('order_id') == order_id_to_find:
            index = i
            break

    Status_present=Log[index]['status']

    return Status_present

def Order_execution_Check(Input_Strike_Call,Input_Strike_Put,quote_call_Hedges,quote_put_Hedges,quote_call,quote_put,Input_Strike_Call_Hedge,Input_Strike_Put_Hedge):

    global Deployed_Size
    Initial_DF=pd.read_csv(Path_backtest_Report+"Running_Status_of_trade.csv")
    
    if Input_Strike_Call is not None and Input_Strike_Put is not None :
        Index_call = Initial_DF.index[(Initial_DF['Strike'] == Input_Strike_Call)].tolist()
        Index_put = Initial_DF.index[(Initial_DF['Strike'] == Input_Strike_Put)].tolist()

        Index_call=Index_call[0]
        Index_put=Index_put[0]

        Order_ID_Call=Initial_DF.loc[Index_call,"Order_ID"]
        Order_ID_Put=Initial_DF.loc[Index_put,"Order_ID"]

        SL_Call=Initial_DF.loc[Index_call,"Trailing SL"]
        SL_Call_Trig=SL_Call-0.05
        SL_Put=Initial_DF.loc[Index_put,"Trailing SL"]
        SL_Put_Trig=SL_Put-0.05

        current_time = datetime.now()

        current_time_str = current_time.strftime("%H:%M:%S")

        Initial_time=closest_time(current_time_str,time_list_1_min)
        index_time=time_list_1_min.index(Initial_time)
        New_time=time_list_1_min[index_time+1]
        Run=0

        while True:
            current_time = datetime.now()
            current_time_str = current_time.strftime("%H:%M:%S")

            Status_call=Status_compute(Order_ID_Call)
            Status_put=Status_compute(Order_ID_Put)

            print(f"The Present run is {Run}")

            if Status_call=="COMPLETE" and Status_put=="COMPLETE" and current_time_str<New_time:

                print("All the Orders are succesfully complete")

                console_output_log_recording("All the Orders are succesfully complete")

                Market_order_Buy(quote_call_Hedges,Deployed_Size,Input_Strike_Call_Hedge,"Call","Buy Hedge")
                Market_order_Buy(quote_put_Hedges,Deployed_Size,Input_Strike_Put_Hedge,"Put","Buy Hedge")

                SL_Initiate_order(quote_call,Deployed_Size,SL_Call,SL_Call_Trig,Input_Strike_Call,"Call")
                SL_Initiate_order(quote_put,Deployed_Size,SL_Put,SL_Put_Trig,Input_Strike_Put,"Put")

                Initial_DF=pd.read_csv(Path_backtest_Report+"Running_Status_of_trade.csv")
                Initial_DF.loc[Index_call,"Status"]="COMPLETE"
                Initial_DF.loc[Index_put,"Status"]="COMPLETE"
                Initial_DF.to_csv(Path_backtest_Report+"Running_Status_of_trade.csv",index=False)

                break

            elif current_time_str>=New_time:
                Status_call=Status_compute(Order_ID_Call)
                Status_put=Status_compute(Order_ID_Put)

                if Status_call=="OPEN" and Status_put=="OPEN":

                    print(f"Modifiying the Call Strike {Input_Strike_Call} and Modifiying the Put Strike {Input_Strike_Put}")
                    console_output_log_recording(f"Modifiying the Call Strike {Input_Strike_Call} and Modifiying the Put Strike {Input_Strike_Put}")

                    pause()

                    Call_CP,quote_CE=Compute_token_Closing_price(Input_Strike_Call,"Call",1)
                    Put_CP,quote_PE=Compute_token_Closing_price(Input_Strike_Put,"Put",1)

                    Modify_SL_Order(Order_ID_Call,Deployed_Size,Call_CP,"Initial Price","Limit")
                    Modify_SL_Order(Order_ID_Put,Deployed_Size,Put_CP,"Initial Price","Limit")

                    strikes_list_modified=Initial_DF["Strike"].to_list()

                    if -Input_Strike_Call in strikes_list_modified and -Input_Strike_Put in strikes_list_modified:

                        print(f"Modifiying the Call Strike SL {Input_Strike_Call} and Modifiying the Put Strike SL {Input_Strike_Put}")
                        console_output_log_recording(f"Modifiying the Call Strike SL {Input_Strike_Call} and Modifiying the Put Strike SL {Input_Strike_Put}")

                        Index_call_SL = Initial_DF.index[(Initial_DF['Strike'] == -Input_Strike_Call)].tolist()
                        Index_put_SL = Initial_DF.index[(Initial_DF['Strike'] == -Input_Strike_Put)].tolist()

                        OID_SL_CE=Initial_DF.loc[Index_call_SL[0],"Order_ID"]
                        OID_SL_PE=Initial_DF.loc[Index_put_SL[0],"Order_ID"]

                        SL_CE=2*Call_CP
                        SL_PE=2*Put_CP

                        Modify_SL_Order(OID_SL_CE,Deployed_Size,SL_CE,"Trailing SL","SL Limit")
                        Modify_SL_Order(OID_SL_PE,Deployed_Size,SL_PE,"Trailing SL","SL Limit")
                    else:
                        pass

                elif Status_call=="OPEN":

                    print(f"Modifiying the Call Strike {Input_Strike_Call} ")
                    console_output_log_recording(f"Modifiying the Call Strike {Input_Strike_Call}")
                    pause()

                    Call_CP,quote_CE=Compute_token_Closing_price(Input_Strike_Call,"Call",1)
                    Modify_SL_Order(Order_ID_Call,Deployed_Size,Call_CP,"Initial Price","Limit")

                    strikes_list_modified=Initial_DF["Strike"].to_list()

                    if -Input_Strike_Call in strikes_list_modified:

                        print(f"Modifiying the Call Strike SL {Input_Strike_Call} ")
                        console_output_log_recording(f"Modifiying the Call Strike SL {Input_Strike_Call}")

                        Index_call_SL = Initial_DF.index[(Initial_DF['Strike'] == -Input_Strike_Call)].tolist()
                        OID_SL_CE=Initial_DF.loc[Index_call_SL[0],"Order_ID"]
                        SL_CE=2*Call_CP
                        Modify_SL_Order(OID_SL_CE,Deployed_Size,SL_CE,"Trailing SL","SL Limit")
                    else:
                        pass

                elif Status_put=="OPEN":

                    print(f"Modifiying the Put Strike {Input_Strike_Put}")
                    console_output_log_recording(f"Modifiying the Put Strike {Input_Strike_Put}")
                    pause()

                    Put_CP,quote_PE=Compute_token_Closing_price(Input_Strike_Put,"Put",1)
                    Modify_SL_Order(Order_ID_Put,Deployed_Size,Put_CP,"Initial Price","Limit")

                    strikes_list_modified=Initial_DF["Strike"].to_list()

                    if -Input_Strike_Put in strikes_list_modified:

                        print(f"Modifiying the Put Strike SL {Input_Strike_Put}")
                        console_output_log_recording(f"Modifiying the Put Strike SL {Input_Strike_Put}")

                        Index_put_SL = Initial_DF.index[(Initial_DF['Strike'] == -Input_Strike_Put)].tolist()
                        OID_SL_PE=Initial_DF.loc[Index_put_SL[0],"Order_ID"]
                        SL_PE=2*Put_CP
                        Modify_SL_Order(OID_SL_PE,Deployed_Size,SL_PE,"Trailing SL","SL Limit")
                    else:
                        pass

                else:
                    pass

                index_time=time_list_1_min.index(New_time)
                New_time=time_list_1_min[index_time+1]

            else:
                pass

            time.sleep(1)

            Run=Run+1

    elif Input_Strike_Call is not None and Input_Strike_Put is None:
        Index_call = Initial_DF.index[(Initial_DF['Strike'] == Input_Strike_Call)].tolist()
        Index_call=Index_call[0]
        Order_ID_Call=Initial_DF.loc[Index_call,"Order_ID"]

        SL_Call=Initial_DF.loc[Index_call,"Trailing SL"]
        SL_Call_Trig=SL_Call-0.05

        current_time = datetime.now()

        current_time_str = current_time.strftime("%H:%M:%S")

        Initial_time=closest_time(current_time_str,time_list_1_min)
        index_time=time_list_1_min.index(Initial_time)
        New_time=time_list_1_min[index_time+1]

        while True:
            current_time = datetime.now()
            current_time_str = current_time.strftime("%H:%M:%S")

            Status_call=Status_compute(Order_ID_Call)

            if Status_call=="COMPLETE" and current_time_str<New_time:

                print("Call Orders Execute Succesfully")

                console_output_log_recording("Call Orders Execute Succesfully")

                Market_order_Buy(quote_call_Hedges,Deployed_Size,Input_Strike_Call_Hedge,"Call","Buy Hedges")
                SL_Initiate_order(quote_call,Deployed_Size,SL_Call,SL_Call_Trig,Input_Strike_Call,"Call")

                Initial_DF=pd.read_csv(Path_backtest_Report+"Running_Status_of_trade.csv")
                Initial_DF.loc[Index_call,"Status"]="COMPLETE"
                Initial_DF.to_csv(Path_backtest_Report+"Running_Status_of_trade.csv",index=False)
                break

            elif current_time_str>=New_time:
                Status_call=Status_compute(Order_ID_Call)

                if Status_call=="OPEN":

                    print(f"Modifiying the Call Strike {Input_Strike_Call}")
                    console_output_log_recording(f"Modifiying the Call Strike {Input_Strike_Call}")

                    pause()

                    Call_CP,quote_CE=Compute_token_Closing_price(Input_Strike_Call,"Call",1)
                    Modify_SL_Order(Order_ID_Call,size,Call_CP,"Initial Price","Limit")

                    strikes_list_modified=Initial_DF["Strike"].to_list()

                    if -Input_Strike_Call in strikes_list_modified:

                        print(f"Modifiying the Call Strike SL {Input_Strike_Call}")
                        console_output_log_recording(f"Modifiying the Call Strike SL {Input_Strike_Call}")

                        Index_call_SL = Initial_DF.index[(Initial_DF['Strike'] == -Input_Strike_Call)].tolist()
                        OID_SL_CE=Initial_DF.loc[Index_call_SL[0],"Order_ID"]
                        SL_CE=2*Call_CP
                        Modify_SL_Order(OID_SL_CE,Deployed_Size,SL_CE,"Trailing SL","SL Limit")
                    else:
                        pass

                else:
                    pass

                index_time=time_list_1_min.index(New_time)
                New_time=time_list_1_min[index_time+1]

            else:
                pass

            time.sleep(1)


    elif Input_Strike_Put is not None and Input_Strike_Call is None:
        Index_put = Initial_DF.index[(Initial_DF['Strike'] == Input_Strike_Put)].tolist()
        Index_put=Index_put[0]
        Order_ID_Put=Initial_DF.loc[Index_put,"Order_ID"]
        SL_Put=Initial_DF.loc[Index_put,"Trailing SL"]
        SL_Put_Trig=SL_Put-0.05

        current_time = datetime.now()

        current_time_str = current_time.strftime("%H:%M:%S")

        Initial_time=closest_time(current_time_str,time_list_1_min)
        index_time=time_list_1_min.index(Initial_time)
        New_time=time_list_1_min[index_time+1]

        while True:
            current_time = datetime.now()

            current_time_str = current_time.strftime("%H:%M:%S")

            Status_put=Status_compute(Order_ID_Put)

            if Status_put=="COMPLETE" and current_time_str<New_time:

                print("Put Orders Execute Succesfully")
                console_output_log_recording("Put Orders Execute Succesfully")

                Market_order_Buy(quote_put_Hedges,Deployed_Size,Input_Strike_Put_Hedge,"Put","Buy Hedges")
                SL_Initiate_order(quote_put,Deployed_Size,SL_Put,SL_Put_Trig,Input_Strike_Put,"Put")

                Initial_DF=pd.read_csv(Path_backtest_Report+"Running_Status_of_trade.csv")
                Initial_DF.loc[Index_put,"Status"]="COMPLETE"
                Initial_DF.to_csv(Path_backtest_Report+"Running_Status_of_trade.csv",index=False)

                break
            elif current_time_str>=New_time:
                Status_put=Status_compute(Order_ID_Put)

                if Status_put=="OPEN":

                    print(f"Modifiying the Put Strike {Input_Strike_Put}")
                    console_output_log_recording(f"Modifiying the Put Strike {Input_Strike_Put}")

                    pause()

                    Put_CP,quote_PE=Compute_token_Closing_price(Input_Strike_Put,"Put",1)
                    Modify_SL_Order(Order_ID_Put,size,Put_CP,"Initial Price","Limit")

                    strikes_list_modified=Initial_DF["Strike"].to_list()

                    if -Input_Strike_Put in strikes_list_modified:

                        print(f"Modifiying the Put Strike SL {Input_Strike_Put}")
                        console_output_log_recording(f"Modifiying the Put Strike SL {Input_Strike_Put}")

                        Index_put_SL = Initial_DF.index[(Initial_DF['Strike'] == -Input_Strike_Put)].tolist()
                        OID_SL_PE=Initial_DF.loc[Index_put_SL[0],"Order_ID"]
                        SL_PE=2*Put_CP
                        Modify_SL_Order(OID_SL_PE,Deployed_Size,SL_PE,"Trailing SL","SL Limit")
                    else:
                        pass

                else:
                    pass

                index_time=time_list_1_min.index(New_time)
                New_time=time_list_1_min[index_time+1]

            else:
                pass

            time.sleep(1) 

    else:
        pass

def Trailing_SL(Active_strike_list_Call,Active_strike_list_Put):
    global Market_Trend
    global Deployed_Size
    
    Initial_DF=pd.read_csv(Path_backtest_Report+"Running_Status_of_trade.csv")
    
    if Market_Trend=="Neutral":
        CE_stk=Active_strike_list_Call[0]
        PE_stk=Active_strike_list_Put[0]

        Index_call = Initial_DF.index[(Initial_DF['Strike'] == -CE_stk)].tolist()
        Index_put = Initial_DF.index[(Initial_DF['Strike'] == -PE_stk)].tolist()

        OID_Call=Initial_DF.loc[Index_call[0],"Order_ID"]
        OID_Put=Initial_DF.loc[Index_put[0],"Order_ID"]

        Status_call=Status_compute(OID_Call)
        Status_put=Status_compute(OID_Put)

        if Status_call=="TRIGGER PENDING" and Status_put=="TRIGGER PENDING":
            Idx_call = Initial_DF.index[(Initial_DF['Strike'] == CE_stk)].tolist()
            Idx_put = Initial_DF.index[(Initial_DF['Strike'] == PE_stk)].tolist()

            SL_Call=Initial_DF.loc[Idx_call[0],"Trailing SL"]
            SL_Put=Initial_DF.loc[Idx_put[0],"Trailing SL"]

            pause()

            CE_CP,QE_CE=Compute_token_Closing_price(CE_stk,"Call")
            PE_CP,QE_PE=Compute_token_Closing_price(PE_stk,"Put")

            New_SL_CE=2*CE_CP
            New_SL_PE=2*PE_CP

            print(f"Present SL CE {New_SL_CE} and Stored SL CE {SL_Call}")
            console_output_log_recording(f"Present SL CE {New_SL_CE} and Stored SL CE {SL_Call}")

            if New_SL_CE<SL_Call and New_SL_CE>=Threshold_price:
                print(f"Updating the Call strike {CE_stk} SL at price {New_SL_CE}")
                console_output_log_recording(f"Updating the Call strike {CE_stk} SL at price {New_SL_CE}")

                Modify_SL_Order(OID_Call,Deployed_Size,New_SL_CE,"Trailing SL","SL Limit")
            elif New_SL_CE>=SL_Call and New_SL_CE>=Threshold_price:
                print(f"No SL Update for the Call Strike {CE_stk}")
                console_output_log_recording(f"No SL Update for the Call Strike {CE_stk}")
            else:
                print(f"No SL Update for the Call Strike {CE_stk}")
                console_output_log_recording(f"No SL Update for the Call Strike {CE_stk}")


            print(f"Present SL CE {New_SL_PE} and Stored SL CE {SL_Put}")
            console_output_log_recording(f"Present SL CE {New_SL_PE} and Stored SL CE {SL_Put}")

            if New_SL_PE<SL_Put and New_SL_PE>=Threshold_price:
                print(f"Updating the Put strike {PE_stk} SL at price {New_SL_PE}")
                console_output_log_recording(f"Updating the Put strike {PE_stk} SL at price {New_SL_PE}")
                Modify_SL_Order(OID_Put,Deployed_Size,New_SL_PE,"Trailing SL","SL Limit")
            elif New_SL_PE>=SL_Put and New_SL_PE>=Threshold_price:
                print(f"No SL Update for the Put Strike {PE_stk}")
                console_output_log_recording(f"No SL Update for the Put Strike {PE_stk}")
            else:
                print(f"No SL Update for the Put Strike {PE_stk}")
                console_output_log_recording(f"No SL Update for the Put Strike {PE_stk}")

        elif Status_call=="COMPLETE":
            print(f"SL hit on the Call Strike {CE_stk} now Market Trend is Bullish")
            console_output_log_recording(f"SL hit on the Call Strike {CE_stk} now Market Trend is Bullish")

            Initial_DF.loc[Index_call[0],"Status"]="COMPLETE"
            Market_Trend="Trending Up"
            Initial_DF.to_csv(Path_backtest_Report+"Running_Status_of_trade.csv",index=False)

            CE_Hedge=CE_stk+600

            pause()

            CE_Hedge_CP,QE_CE_Hedge=Compute_token_Closing_price(CE_Hedge,"Call")
            Market_order_Sell(QE_CE_Hedge,Deployed_Size,CE_Hedge_CP,"Call","Hedge Sell")

            with open(Path_backtest_Report+"Market_trend_file.txt", "w") as file:
                file.write(Market_Trend)

            print("Adding new Strikes")
            console_output_log_recording("Adding new Strikes")
            Active_strike_list_Call,Active_strike_list_Put=New_order_Placement(Active_strike_list_Call,Active_strike_list_Put)

            print(f"New Strikes list for Call {Active_strike_list_Call} and New Strikes list for put {Active_strike_list_Put}")
            console_output_log_recording(f"New Strikes list for Call {Active_strike_list_Call} and New Strikes list for put {Active_strike_list_Put}")

        elif Status_put=="COMPLETE":
            print(f"SL hit on the Put Strike {PE_stk} now Market Trend is Bearish")
            console_output_log_recording(f"SL hit on the Put Strike {PE_stk} now Market Trend is Bearish")

            Initial_DF.loc[Index_put[0],"Status"]="COMPLETE"
            Market_Trend="Trending Down"
            Initial_DF.to_csv(Path_backtest_Report+"Running_Status_of_trade.csv",index=False)

            PE_Hedge=PE_stk-600

            pause()

            PE_Hedge_CP,QE_PE_Hedge=Compute_token_Closing_price(PE_Hedge,"Put")
            Market_order_Sell(QE_PE_Hedge,Deployed_Size,PE_Hedge_CP,"Put","Hedge Sell")

            with open(Path_backtest_Report+"Market_trend_file.txt", "w") as file:
                file.write(Market_Trend)

            print("Adding new Strikes")
            console_output_log_recording("Adding new Strikes")
            Active_strike_list_Call,Active_strike_list_Put=New_order_Placement(Active_strike_list_Call,Active_strike_list_Put)

            print(f"New Strikes list for Call {Active_strike_list_Call} and New Strikes list for put {Active_strike_list_Put}")
            console_output_log_recording(f"New Strikes list for Call {Active_strike_list_Call} and New Strikes list for put {Active_strike_list_Put}")

        else:
            pass


    elif Market_Trend=="Trending Up":
        CE_stk=Active_strike_list_Call[0]
        
        for i in range(len(Active_strike_list_Put)):
            PE_stk=Active_strike_list_Put[i]
            Index_put = Initial_DF.index[(Initial_DF['Strike'] == -PE_stk)].tolist()
            OID_Put=Initial_DF.loc[Index_put[0],"Order_ID"]
            Status_put=Status_compute(OID_Put)

            if Status_put=="TRIGGER PENDING":
                Idx_put = Initial_DF.index[(Initial_DF['Strike'] == PE_stk)].tolist()
                SL_Put=Initial_DF.loc[Idx_put[0],"Trailing SL"]

                pause()

                PE_CP,QE_PE=Compute_token_Closing_price(PE_stk,"Put")
                New_SL_PE=2*PE_CP

                print(f"Present SL PE {New_SL_PE} and Stored SL PE {SL_Put}")
                console_output_log_recording(f"Present SL PE {New_SL_PE} and Stored SL PE {SL_Put}")

                if New_SL_PE<SL_Put and New_SL_PE>=Threshold_price:
                    print(f"Updating the Put strike {PE_stk} SL at price {New_SL_PE}")
                    console_output_log_recording(f"Updating the Put strike {PE_stk} SL at price {New_SL_PE}")

                    Modify_SL_Order(OID_Put,Deployed_Size,New_SL_PE,"Trailing SL","SL Limit")
                elif New_SL_PE>=SL_Put and New_SL_PE>=Threshold_price:
                    print(f"No SL Update for the Put Strike {PE_stk}")
                    console_output_log_recording(f"No SL Update for the Put Strike {PE_stk}")
                else:
                    print(f"No SL Update for the Put Strike {PE_stk}")
                    console_output_log_recording(f"No SL Update for the Put Strike {PE_stk}")

            elif Status_put=="COMPLETE":

                print(f"SL hit for strike {PE_stk} on put side the market reverses the trend")
                console_output_log_recording(f"SL hit for strike {PE_stk} on put side the market reverses the trend")
                Initial_DF.loc[Index_put[0],"Status"]="COMPLETE"
                Initial_DF.to_csv(Path_backtest_Report+"Running_Status_of_trade.csv",index=False)

                Active_strike_list_Put.remove(PE_stk)
                PE_stk_Hedges=PE_stk-600

                pause()

                PE_Hedge_CP,QE_PE_Hedge=Compute_token_Closing_price(PE_stk_Hedges,"Put")
                Market_order_Sell(QE_PE_Hedge,Deployed_Size,PE_Hedge_CP,"Put","Hedge Sell")

            else:
                pass

        Index_call = Initial_DF.index[(Initial_DF['Strike'] == -CE_stk)].tolist()
        OID_Call=Initial_DF.loc[Index_call[0],"Order_ID"]
        Status_call=Status_compute(OID_Call)

        if Status_call=="TRIGGER PENDING":
            Idx_call = Initial_DF.index[(Initial_DF['Strike'] == CE_stk)].tolist()
            SL_Call=Initial_DF.loc[Idx_call[0],"Trailing SL"]

            pause()

            CE_CP,QE_CE=Compute_token_Closing_price(CE_stk,"Call")
            New_SL_CE=2*CE_CP

            print(f"Present SL CE {New_SL_CE} and Stored SL CE {SL_Call}")
            console_output_log_recording(f"Present SL CE {New_SL_CE} and Stored SL CE {SL_Call}")

            if New_SL_CE<SL_Call and New_SL_CE>=Threshold_price:
                print(f"Updating the Call strike {CE_stk} SL at price {New_SL_CE}")
                console_output_log_recording(f"Updating the Call strike {CE_stk} SL at price {New_SL_CE}")
                Modify_SL_Order(OID_Call,size,New_SL_CE,"Trailing SL","SL Limit")
            elif New_SL_CE>=SL_Call and New_SL_CE>=Threshold_price:
                print(f"No SL update for Call Strike {CE_stk}")
                console_output_log_recording(f"No SL update for Call Strike {CE_stk}")
            else:
                print(f"No SL update for Call Strike {CE_stk}")
                console_output_log_recording(f"No SL update for Call Strike {CE_stk}")
        
        elif Status_call=="COMPLETE":
            print(f"SL hit on call Strike {CE_stk} the market continues in the same trend selling Additional Strikes")
            console_output_log_recording(f"SL hit on call Strike {CE_stk} the market continues in the same trend selling Additional Strikes")
            Initial_DF.loc[Index_call[0],"Status"]="COMPLETE"
            Initial_DF.to_csv(Path_backtest_Report+"Running_Status_of_trade.csv",index=False)

            Length_put=len(Active_strike_list_Put)
            CE_stk_Hedges=CE_stk+600

            pause()

            CE_Hedge_CP,QE_CE_Hedge=Compute_token_Closing_price(CE_stk_Hedges,"Call")
            Market_order_Sell(QE_CE_Hedge,Deployed_Size,CE_Hedge_CP,"Call","Hedge Sell")

            if Length_put>4:
                print("Maximum Credit limit reached can't sell more strikes")
                console_output_log_recording("Maximum Credit limit reached can't sell more strikes")
            else:
                print("Adding new Strikes")
                console_output_log_recording("Adding new Strikes")
                Active_strike_list_Call,Active_strike_list_Put=New_order_Placement(Active_strike_list_Call,Active_strike_list_Put)
                print(f"New Strikes list for Call {Active_strike_list_Call} and New Strikes list for put {Active_strike_list_Put}")
                console_output_log_recording(f"New Strikes list for Call {Active_strike_list_Call} and New Strikes list for put {Active_strike_list_Put}")


    elif Market_Trend=="Trending Down":
        PE_stk=Active_strike_list_Put[0]

        for i in range(len(Active_strike_list_Call)):
            CE_stk=Active_strike_list_Call[i]
            Index_call = Initial_DF.index[(Initial_DF['Strike'] == -CE_stk)].tolist()
            OID_Call=Initial_DF.loc[Index_call[0],"Order_ID"]
            Status_call=Status_compute(OID_Call)

            if Status_call=="TRIGGER PENDING":
                Idx_call = Initial_DF.index[(Initial_DF['Strike'] == CE_stk)].tolist()
                SL_Call=Initial_DF.loc[Idx_call[0],"Trailing SL"]

                pause()

                CE_CP,QE_CE=Compute_token_Closing_price(CE_stk,"Call")

                New_SL_CE=2*CE_CP

                print(f"Present SL CE {New_SL_CE} and Stored SL CE {SL_Call}")
                console_output_log_recording(f"Present SL CE {New_SL_CE} and Stored SL CE {SL_Call}")

                if New_SL_CE<SL_Call and New_SL_CE>=Threshold_price:
                    print(f"Updating the Call strike {CE_stk} SL at price {New_SL_CE}")
                    console_output_log_recording(f"Updating the Call strike {CE_stk} SL at price {New_SL_CE}")
                    Modify_SL_Order(OID_Call,size,New_SL_CE,"Trailing SL","SL Limit")
                elif New_SL_CE>=SL_Call and New_SL_CE>=Threshold_price:
                    print(f"No SL update for Call Strike {CE_stk}")
                    console_output_log_recording(f"No SL update for Call Strike {CE_stk}")
                else:
                    print(f"No SL update for Call Strike {CE_stk}")
                    console_output_log_recording(f"No SL update for Call Strike {CE_stk}")

            elif Status_call=="COMPLETE":
                print(f"SL hit for strike {CE_stk} on call side the market reverses the trend")
                console_output_log_recording(f"SL hit for strike {CE_stk} on call side the market reverses the trend")

                Initial_DF.loc[Index_call[0],"Status"]="COMPLETE"
                Initial_DF.to_csv(Path_backtest_Report+"Running_Status_of_trade.csv",index=False)

                Active_strike_list_Call.remove(CE_stk)
                CE_stk_Hedges=CE_stk+600

                pause()

                CE_Hedge_CP,QE_CE_Hedge=Compute_token_Closing_price(CE_stk_Hedges,"Call")
                Market_order_Sell(QE_CE_Hedge,Deployed_Size,CE_Hedge_CP,"Call","Hedge Sell")
            else:
                pass

        Index_put = Initial_DF.index[(Initial_DF['Strike'] == -PE_stk)].tolist()
        OID_Put=Initial_DF.loc[Index_put[0],"Order_ID"]
        Status_put=Status_compute(OID_Put)

        if Status_put=="TRIGGER PENDING":
            Idx_put = Initial_DF.index[(Initial_DF['Strike'] == PE_stk)].tolist()
            SL_Put=Initial_DF.loc[Idx_put[0],"Trailing SL"]

            print(f"Present SL PE {New_SL_PE} and Stored SL PE {SL_Put}")
            console_output_log_recording(f"Present SL PE {New_SL_PE} and Stored SL PE {SL_Put}")
            
            pause()

            PE_CP,QE_PE=Compute_token_Closing_price(PE_stk,"Put")

            New_SL_PE=2*PE_CP

            if New_SL_PE<SL_Put and New_SL_PE>=Threshold_price:
                print(f"Updating the Put strike {PE_stk} SL at price {New_SL_PE}")
                console_output_log_recording(f"Updating the Put strike {PE_stk} SL at price {New_SL_PE}")
                Modify_SL_Order(OID_Put,size,New_SL_PE,"Trailing SL","SL Limit")
            elif New_SL_PE>=SL_Put and New_SL_PE>=Threshold_price:
                print(f"No SL update for Put Strike {PE_stk}")
                console_output_log_recording(f"No SL update for Put Strike {PE_stk}")
            else:
                print(f"No SL update for Put Strike {PE_stk}")
                console_output_log_recording(f"No SL update for Put Strike {PE_stk}")

        elif Status_put=="COMPLETE":
            print(f"SL hit on put Strike {PE_stk} the market continues in the same trend selling Additional Strikes")
            console_output_log_recording(f"SL hit on put Strike {PE_stk} the market continues in the same trend selling Additional Strikes")

            Initial_DF.loc[Index_put[0],"Status"]="COMPLETE"
            Initial_DF.to_csv(Path_backtest_Report+"Running_Status_of_trade.csv",index=False)

            Length_call=len(Active_strike_list_Call)
            PE_stk_Hedges=PE_stk-600

            pause()

            PE_Hedge_CP,QE_PE_Hedge=Compute_token_Closing_price(PE_stk_Hedges,"Put")
            Market_order_Sell(QE_PE_Hedge,Deployed_Size,PE_Hedge_CP,"Put","Hedge Sell")
            
            if Length_call>4:
                print("Maximum Credit limit reached can't sell more strikes")
                console_output_log_recording("Maximum Credit limit reached can't sell more strikes")
            else:
                print("Adding new Strikes")
                console_output_log_recording("Adding new Strikes")
                Active_strike_list_Call,Active_strike_list_Put=New_order_Placement(Active_strike_list_Call,Active_strike_list_Put)
                print(f"New Strikes list for Call {Active_strike_list_Call} and New Strikes list for put {Active_strike_list_Put}")
                console_output_log_recording(f"New Strikes list for Call {Active_strike_list_Call} and New Strikes list for put {Active_strike_list_Put}")

    else:
        pass


    current_time = datetime.now().strftime("%H:%M")
    if current_time >= "15:30":
        Day_end()
    else:
        schedule_next_execution()

def schedule_next_execution():
    import time
    global time_list_5_min
    global Active_strike_list_Call
    global Active_strike_list_Put
    global run

    times_to_execute=time_list_5_min

    # Get the current time
    current_time = datetime.now().strftime("%H:%M:%S")

    print(f"Trailing SL run {run} and current time is {current_time}")
    console_output_log_recording(f"Trailing SL run {run} and current time is {current_time}")

    run=run+1
    # Find the next time in the list that is greater than the current time
    next_time = None
    for t in times_to_execute:
        if t > current_time:
            next_time = t
            break

    if next_time:
        # Calculate the time difference in seconds
        time_difference = (datetime.strptime(next_time, "%H:%M:%S") - datetime.strptime(current_time, "%H:%M:%S")).total_seconds()

        time.sleep(int(time_difference))
        Trailing_SL(Active_strike_list_Call,Active_strike_list_Put)
        
    else:
        # No more times in the list for today, you can handle this case as needed
        print("No more times to execute today")


def New_order_Placement(Active_strike_list_Call,Active_strike_list_Put):
    global enctoken
    global Market_Trend
    global Deployed_Size

    kite = KiteApp(enctoken=enctoken)

    Nifty=kite.ltp(["NSE:NIFTY 50"])
    Nifty_Spot_price=Nifty['NSE:NIFTY 50']['last_price']

    Vix=kite.ltp(["NSE:INDIA VIX"])
    Present_vol=Vix['NSE:INDIA VIX']['last_price']

    range=((Present_vol/np.sqrt(252))*Nifty_Spot_price)/100

    offset=round(range,2)
    offset = round(offset / 50) * 50
    offset=int(offset)

    if Market_Trend=="Trending Up":
        Call_strike=Active_strike_list_Call[0]
        length_put=len(Active_strike_list_Put)
        if length_put<3:
            Put_strike=Active_strike_list_Put[length_put-1]
            New_Put_Strike=Put_strike+50

            New_Call_Strike=Call_strike+offset

            Active_strike_list_Call.append(New_Call_Strike)
            Active_strike_list_Put.append(New_Put_Strike)

            New_Put_Strike_hedges=New_Put_Strike-600
            New_Call_Strike_hedges=New_Call_Strike+600

            CP_Call,qte_call=Compute_token_Closing_price(New_Call_Strike,"Call")
            CP_Put,qte_put=Compute_token_Closing_price(New_Put_Strike,"Put")
            CP_Call_hedge,qte_call_hedge=Compute_token_Closing_price(New_Call_Strike_hedges,"Call")
            CP_Put_hedge,qte_put_hedge=Compute_token_Closing_price(New_Put_Strike_hedges,"Put")

            limit_order_Sell(qte_call,Deployed_Size,CP_Call,New_Call_Strike,"Call")
            limit_order_Sell(qte_put,Deployed_Size,CP_Put,New_Put_Strike,"Put")

            Order_execution_Check(New_Call_Strike,New_Put_Strike,qte_call_hedge,qte_put_hedge,qte_call,qte_put,New_Put_Strike_hedges,New_Call_Strike_hedges)

            return Active_strike_list_Call,Active_strike_list_Put

        elif length_put==3:

            Active_strike_list_Call=[]

            Put_strike=Active_strike_list_Put[length_put-1]
            New_Put_Strike=Put_strike+50      

            Active_strike_list_Put.append(New_Put_Strike)
            New_Put_Strike_hedges=New_Put_Strike-600

            CP_Put,qte_put=Compute_token_Closing_price(New_Put_Strike,"Put")            
            CP_Put_hedge,qte_put_hedge=Compute_token_Closing_price(New_Put_Strike_hedges,"Put")

            limit_order_Sell(qte_put,Deployed_Size,CP_Put,New_Put_Strike,"Put")

            Order_execution_Check(None,New_Put_Strike,None,qte_put_hedge,None,qte_put,New_Put_Strike_hedges,None)

            return Active_strike_list_Call,Active_strike_list_Put

        else:
            pass

    elif Market_Trend=="Trending Down":
        Put_strike=Active_strike_list_Put[0]
        length_call=len(Active_strike_list_Call)

        if length_call<3:
            Call_strike=Active_strike_list_Call[length_call-1]
            New_Call_Strike=Call_strike-50

            New_Put_Strike=Put_strike-offset

            Active_strike_list_Call.append(New_Call_Strike)
            Active_strike_list_Put.append(New_Put_Strike)

            New_Put_Strike_hedges=New_Put_Strike-600
            New_Call_Strike_hedges=New_Call_Strike+600

            CP_Call,qte_call=Compute_token_Closing_price(New_Call_Strike,"Call")
            CP_Put,qte_put=Compute_token_Closing_price(New_Put_Strike,"Put")
            CP_Call_hedge,qte_call_hedge=Compute_token_Closing_price(New_Call_Strike_hedges,"Call")
            CP_Put_hedge,qte_put_hedge=Compute_token_Closing_price(New_Put_Strike_hedges,"Put")

            limit_order_Sell(qte_call,Deployed_Size,CP_Call,New_Call_Strike,"Call")
            limit_order_Sell(qte_put,Deployed_Size,CP_Put,New_Put_Strike,"Put")

            Order_execution_Check(New_Call_Strike,New_Put_Strike,qte_call_hedge,qte_put_hedge,qte_call,qte_put,New_Put_Strike_hedges,New_Call_Strike_hedges)

            return Active_strike_list_Call,Active_strike_list_Put

        elif length_call==3:

            Active_strike_list_Put=[]

            Call_strike=Active_strike_list_Call[length_call-1]
            New_Call_Strike=Call_strike-50      

            Active_strike_list_Call.append(New_Call_Strike)
            New_Call_Strike_hedges=New_Call_Strike+600

            CP_Call,qte_call=Compute_token_Closing_price(New_Call_Strike,"Call")            
            CP_Call_hedge,qte_call_hedge=Compute_token_Closing_price(New_Call_Strike_hedges,"Call")

            limit_order_Sell(qte_call,Deployed_Size,CP_Call,New_Call_Strike,"Call")

            Order_execution_Check(New_Call_Strike,None,qte_call_hedge,None,qte_call,None,None,New_Call_Strike_hedges)

            return Active_strike_list_Call,Active_strike_list_Put
        else:
            pass


def Morning_run():
    global Active_strike_list_Call
    global Active_strike_list_Put
    global Deployed_Size

    Initial_DF=pd.read_csv(Path_backtest_Report+"Running_Status_of_trade.csv")
    Active_strike_list_Call=[]
    Active_strike_list_Put=[]

    dummy_strikes_call=[]
    dummy_strikes_put=[]

    with open(Path_backtest_Report+"Market_trend_file.txt", 'r') as file:
        file_content = file.read()

    Market_Trend=file_content
    sell_rows = Initial_DF[Initial_DF['Type'] == 'Sell']
    sell_indexes = sell_rows.index.tolist()

    for i in sell_indexes:
        ryt=Initial_DF.loc[i,"Right"]
        
        if ryt=="Call":
            stk_ce=Initial_DF.loc[i,"Strike"]
            dummy_strikes_call.append(stk_ce)
        elif ryt=="Put":
            stk_pe=Initial_DF.loc[i,"Strike"]
            dummy_strikes_put.append(stk_pe)

    modified_list_call = [-1 * x for x in dummy_strikes_call]
    modified_list_put = [-1 * x for x in dummy_strikes_put]

    filtered_modified_list_call = [strike for strike, status in zip(modified_list_call, Initial_DF['Status']) if status == 'TRIGGER PENDING']
    filtered_modified_list_put = [strike for strike, status in zip(modified_list_put, Initial_DF['Status']) if status == 'TRIGGER PENDING']

    for i in range(len(filtered_modified_list_call)):
        filtered_modified_list_call[i] *= -1

    for i in range(len(filtered_modified_list_put)):
        filtered_modified_list_put[i] *= -1

    Active_strike_list_Call=filtered_modified_list_call
    Active_strike_list_Put=filtered_modified_list_put

    if Market_Trend=="Neutral":
        CE_STK=Active_strike_list_Call[0]
        PE_STK=Active_strike_list_Put[0]

        Index_call = Initial_DF.index[(Initial_DF['Strike'] == CE_STK)].tolist()
        Index_put = Initial_DF.index[(Initial_DF['Strike'] == PE_STK)].tolist()

        SL_CE=Initial_DF.loc[Index_call[0],"Trailing SL"]
        SL_PE=Initial_DF.loc[Index_put[0],"Trailing SL"]

        target_time = datetime.datetime.strptime(Desired_time, "%H:%M").time()

        while True:
            current_time = datetime.datetime.now().time()
            CP_CALL,QTE_CALL=Compute_token_Closing_price(CE_STK,"Call")
            CP_PUT,QTE_PUT=Compute_token_Closing_price(PE_STK,"Put")

            if current_time >= target_time:
                if CP_CALL>=SL_CE:
                    SL_Call_Trig=CP_CALL-0.05
                    SL_Initiate_order(QTE_CALL,Deployed_Size,CP_CALL,SL_Call_Trig,Active_strike_list_Call[0],"Call")
                    Market_Trend="Trending Up"
                    with open(Path_backtest_Report+"Market_trend_file.txt", "w") as file:
                        file.write(Market_Trend)
                    

                if CP_PUT>=SL_PE:
                    SL_Put_Trig=CP_PUT-0.05
                    SL_Initiate_order(QTE_PUT,Deployed_Size,CP_PUT,SL_Put_Trig,Active_strike_list_Put[0],"Put")
                    Market_Trend="Trending Down"
                    with open(Path_backtest_Report+"Market_trend_file.txt", "w") as file:
                        file.write(Market_Trend)

                break
            time.sleep(300)  

    elif Market_Trend=="Tending Up":
        CE_STK=Active_strike_list_Call[0]
        Index_call = Initial_DF.index[(Initial_DF['Strike'] == CE_STK)].tolist()
        SL_CE=Initial_DF.loc[Index_call[0],"Trailing SL"]

        Stop_Loss_arr_Put=[]

        for i in range(len(Active_strike_list_Put)):

            PE_STK=Active_strike_list_Put[i]
            Index_put = Initial_DF.index[(Initial_DF['Strike'] == PE_STK)].tolist()
            SL_PE=Initial_DF.loc[Index_put[0],"Trailing SL"]
            Stop_Loss_arr_Put.append(SL_PE)

        target_time = datetime.datetime.strptime(Desired_time, "%H:%M").time()

        while True:
            current_time = datetime.datetime.now().time()
            closing_price_put=[]
            Qte_Put=[]
            CP_CALL,QTE_CALL=Compute_token_Closing_price(CE_STK,"Call")

            for i in range(len(Active_strike_list_Put)):
                PE_STK=Active_strike_list_Put[i]
                CP_PUT,QTE_PUT=Compute_token_Closing_price(PE_STK,"Put")
                closing_price_put.append(CP_PUT)
                Qte_Put.append(QTE_PUT)

            if current_time >= target_time:

                for i in range(len(Active_strike_list_Put)):
                    CP_PE=closing_price_put[i]
                    SL_PE=Stop_Loss_arr_Put[i]
                    Quote_put=Qte_Put[i]

                    if CP_PE>=SL_PE:
                        SL_Put_Trig=CP_PE-0.05
                        SL_Initiate_order(Quote_put,Deployed_Size,CP_PE,SL_Put_Trig,Active_strike_list_Put[i],"Put")
                    else:
                        pass

                if CP_CALL>=SL_CE:
                    SL_Call_Trig=CP_CALL-0.05
                    SL_Initiate_order(QTE_CALL,Deployed_Size,CP_CALL,SL_Call_Trig,Active_strike_list_Call[0],"Call")
                else:
                    pass

                break

            time.sleep(300)  
            
    elif Market_Trend=="Trending Down":
        PE_STK=Active_strike_list_Put[0]
        Index_put = Initial_DF.index[(Initial_DF['Strike'] == PE_STK)].tolist()
        SL_PE=Initial_DF.loc[Index_put[0],"Trailing SL"]

        Stop_Loss_arr_Call=[]

        for i in range(len(Active_strike_list_Call)):

            CE_STK=Active_strike_list_Call[i]
            Index_call = Initial_DF.index[(Initial_DF['Strike'] == CE_STK)].tolist()
            SL_CE=Initial_DF.loc[Index_call[0],"Trailing SL"]
            Stop_Loss_arr_Call.append(SL_CE)

        target_time = datetime.datetime.strptime(Desired_time, "%H:%M").time()

        while True:
            current_time = datetime.datetime.now().time()
            closing_price_call=[]
            Qte_Call=[]
            CP_PUT,QTE_PUT=Compute_token_Closing_price(PE_STK,"Put")

            for i in range(len(Active_strike_list_Call)):
                CE_STK=Active_strike_list_Call[i]
                CP_CALL,QTE_CALL=Compute_token_Closing_price(CE_STK,"Call")
                closing_price_put.append(CP_CALL)
                Qte_Call.append(QTE_CALL)

            if current_time >= target_time:

                for i in range(len(Active_strike_list_Call)):
                    CP_CE=closing_price_call[i]
                    SL_CE=Stop_Loss_arr_Call[i]
                    Quote_call=Qte_Call[i]

                    if CP_CE>=SL_CE:
                        SL_Call_Trig=CP_PE-0.05
                        SL_Initiate_order(Quote_call,Deployed_Size,CP_CE,SL_Call_Trig,Active_strike_list_Call[i],"Call")
                    else:
                        pass

                if CP_PUT>=SL_PE:
                    SL_Put_Trig=CP_PUT-0.05
                    SL_Initiate_order(QTE_PUT,Deployed_Size,CP_PUT,SL_Put_Trig,Active_strike_list_Call[0],"Put")
                else:
                    pass

                break
            time.sleep(300)  
    else:
        pass
    
def Day_end():
    Initial_DF=pd.read_csv(Path_backtest_Report+"Running_Status_of_trade.csv")

    df=Initial_DF
    filtered_rows = df[(df['Strike'] < 0) & (df['Status'] == 'Trigger Pending') & (df['Type'] == 'Buy')]
    row_indices = filtered_rows.index.tolist()

    for i in row_indices:
        order_id=Initial_DF.loc[i,"Order_ID"]

        cancel_order(order_id)


path_main="D:/ashu/Finance/algo_trading/Zerodha_GUI/Kite_Zerodha-main/Kite_Zerodha-main/"
Path_backtest_Report="D:/ashu/Finance/algo_trading/Zerodha_GUI/Kite_Zerodha-main/Kite_Zerodha-main/Back_Test_Files_Report/"

df=pd.read_csv(path_main+"Enctoke_Expiry_month_end_info.csv")
content_enctoken=df.iloc[0,0]
enctoken = content_enctoken



####################### Global Declared Variables ##############################
Initial_day=1

Input_Strike_Call=23100
Input_Strike_Put=22300

Input_Strike_Put_Hedge=Input_Strike_Put-600
Input_Strike_Call_Hedge=Input_Strike_Call+600

Initiate_time="09:20"
Desired_time="09:30"
Threshold_price=1

size=1
Lot_size=50
Deployed_Size=Lot_size*size
Interrupt=0
run=0

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

####################### Global Declared Variables ##############################
    

if Initial_day==1:
    Date=[]
    Time=[]
    Strike_list=[]
    Right_list=[]
    order_id=[]
    Status_list=[]
    Type_list=[]
    Initial_price_list=[]
    Trailing_SL_list=[]

    with open(Path_backtest_Report+'Running_log_file.txt', 'w') as file:
        pass

    with open(Path_backtest_Report+'Console_output_log_file.txt', 'w') as file:
        pass

    Initial_data={"Date":Date,"Time":Time,"Strike":Strike_list,"Right":Right_list,"Order_ID":order_id,"Status":Status_list,"Type":Type_list,"Initial Price":Initial_price_list,"Trailing SL":Trailing_SL_list}
    Initial_DF=pd.DataFrame(Initial_data)

    Initial_DF.to_csv(Path_backtest_Report+"Running_Status_of_trade.csv",index=False)

    Market_Trend="Neutral"

    with open(Path_backtest_Report+"Market_trend_file.txt", "w") as file:
        file.write(Market_Trend)

    Call_Closing_Price,quote_call=Compute_token_Closing_price(Input_Strike_Call,"Call")
    Put_Closing_Price,quote_put=Compute_token_Closing_price(Input_Strike_Put,"Put")

    Call_Closing_Price_Hedges,quote_call_Hedges=Compute_token_Closing_price(Input_Strike_Call_Hedge,"Call")
    Put_Closing_Price_Hedges,quote_put_Hedges=Compute_token_Closing_price(Input_Strike_Put_Hedge,"Put")

    Active_strike_list_Call=[Input_Strike_Call]
    Active_strike_list_Put=[Input_Strike_Put]


    limit_order_Sell(quote_call,Deployed_Size,Call_Closing_Price,Input_Strike_Call,"Call")
    limit_order_Sell(quote_put,Deployed_Size,Put_Closing_Price,Input_Strike_Put,"Put")


    Order_execution_Check(Input_Strike_Call,Input_Strike_Put,quote_call_Hedges,quote_put_Hedges,quote_call,quote_put,Input_Strike_Call_Hedge,Input_Strike_Put_Hedge)

    Trailing_SL(Active_strike_list_Call,Active_strike_list_Put)

# elif Initial_day==0 and Interrupt==0:
#     Morning_run()
#     Trailing_SL(Active_strike_list_Call,Active_strike_list_Put)

# elif Initial_day==0 and Interrupt==1:
#     Trailing_SL(Active_strike_list_Call,Active_strike_list_Put)

# else:
#     pass