import pandas as pd
from kite_trade import *
from datetime import datetime,timedelta
import ast
import time
import numpy as np

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

def Market_order_Buy(Quote,Size,Strike,Right):
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

    Type_list.append("Buy Hedges")
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


def Market_order_Sell():
    global enctoken
    kite = KiteApp(enctoken=enctoken)
    global order_info


    order = kite.place_order(variety=kite.VARIETY_REGULAR,
                         exchange=kite.EXCHANGE_NFO,
                         tradingsymbol=order_info["Trading_symbol"],
                         transaction_type=kite.TRANSACTION_TYPE_SELL,
                         quantity=order_info["Size_Sell"],
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
    
    ## Save the order info in the log list


def Modify_SL_Order(OID,Size,Price,type_of_modification):
    global order_info
    
    global enctoken
    kite = KiteApp(enctoken=enctoken)

    Initial_DF=pd.read_csv(Path_backtest_Report+"Running_Status_of_trade.csv")

    kite.modify_order(variety=kite.VARIETY_REGULAR,
                  order_id=OID,
                  parent_order_id=None,
                  quantity=Size,
                  price=Price,
                  order_type=kite.ORDER_TYPE_LIMIT,
                  trigger_price=None,
                  validity=kite.VALIDITY_DAY,
                  disclosed_quantity=None)
    
    Index = Initial_DF.index[(Initial_DF['Order_ID'] == OID)].tolist()
    Index=Index[0]
    Initial_DF.loc[Index,type_of_modification]=Price

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
    Status_present=x[l1-1]['status']
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

    data={"Date":Date,"Time":Time,"Strike":Strike_list,"Right":Right_list,"Order_ID":order_id,"Status":Status_list,"Type":Type_list,"Initial Price":Initial_price_list,"Trailing SL":Trailing_SL_list}
    new_df=pd.DataFrame(data)
    Initial_DF=pd.concat([Initial_DF, new_df], axis=0)

    Initial_DF.to_csv(Path_backtest_Report+"Running_Status_of_trade.csv",index=False)

def cancel_order():

    global order_info
    global enctoken
    kite = KiteApp(enctoken=enctoken)

    kite.cancel_order(variety=kite.VARIETY_REGULAR,
                  order_id=str(order_info["Order_ID"]),
                  parent_order_id=None)
    
    ## Save the order info in the log list

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

def Compute_token_Closing_price(Strike,Right):
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
        interval = "5minute"
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
        interval = "5minute"
        content_PE=kite.historical_data(ATM_Token_PE, from_datetime, to_datetime, interval, continuous=False, oi=True)
        length=len(content_PE)
        Content_PE=str(content_PE[length-2])
        cleaned_contents_PE = Content_PE.replace("datetime.datetime", "").replace(", tzinfo=tzoffset(None, 19800)", "")
        data_PE = ast.literal_eval(cleaned_contents_PE)

        closing_price_PE=data_PE['close']

        return closing_price_PE, quote_PE       

def Closest_time(present_time):
    present_time_minutes = int(present_time.split(':')[0]) * 60 + int(present_time.split(':')[1])

    closest_time = None
    closest_time_difference = float('inf')

    for time in time_list:
        # Convert each time to minutes for comparison
        time_minutes = int(time.split(':')[0]) * 60 + int(time.split(':')[1])
        
        # Check if the time is less than the present time and closer to it
        if time_minutes < present_time_minutes and present_time_minutes - time_minutes < closest_time_difference:
            closest_time = time
            closest_time_difference = present_time_minutes - time_minutes

    return closest_time


def Status_compute(Order_ID_current):
    global enctoken
    kite = KiteApp(enctoken=enctoken)

    Log=kite.orders()
    order_id_to_find = Order_ID_current

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

        current_time = datetime.now().strftime("%I:%M").lstrip('0')

        Initial_time=Closest_time(current_time)
        index_time=time_list.index(Initial_time)
        New_time=time_list[index_time+1]

        while True:
            current_time = datetime.now().strftime("%I:%M").lstrip('0')

            Initial_time=Closest_time(current_time)

            Status_call=Status_compute(Order_ID_Call)
            Status_put=Status_compute(Order_ID_Put)

            if Status_call=="COMPLETE" and Status_put=="COMPLETE" and Initial_time<New_time:
                Market_order_Buy(quote_call_Hedges,size,Input_Strike_Call_Hedge,"Call")
                Market_order_Buy(quote_put_Hedges,size,Input_Strike_Put_Hedge,"Put")

                SL_Initiate_order(quote_call,size,SL_Call,SL_Call_Trig,Input_Strike_Call,"Call")
                SL_Initiate_order(quote_put,size,SL_Put,SL_Put_Trig,Input_Strike_Put,"Put")

                Initial_DF.loc[Index_call,"Status"]="COMPLETE"
                Initial_DF.loc[Index_put,"Status"]="COMPLETE"
                Initial_DF.to_csv(Path_backtest_Report+"Running_Status_of_trade.csv",index=False)

                break

            elif Initial_time>=New_time:
                Status_call=Status_compute(Order_ID_Call)
                Status_put=Status_compute(Order_ID_Put)

                if Status_call=="TRIGGER PENDING" and Status_put=="TRIGGER PENDING":
                    Call_CP,quote_CE=Compute_token_Closing_price(Input_Strike_Call,"Call")
                    Put_CP,quote_PE=Compute_token_Closing_price(Input_Strike_Put,"Put")
                    Modify_SL_Order(Order_ID_Call,size,Call_CP,"Initial Price")
                    Modify_SL_Order(Order_ID_Put,size,Put_CP,"Initial Price")

                elif Status_call=="TRIGGER PENDING":
                    Call_CP,quote_CE=Compute_token_Closing_price(Input_Strike_Call,"Call")
                    Modify_SL_Order(Order_ID_Call,size,Call_CP,"Initial Price")
                elif Status_put=="TRIGGER PENDING":
                    Put_CP,quote_PE=Compute_token_Closing_price(Input_Strike_Put,"Put")
                    Modify_SL_Order(Order_ID_Put,size,Put_CP,"Initial Price")
                else:
                    pass

                index_time=time_list.index(New_time)
                New_time=time_list[index_time+1]

            else:
                pass

            time.sleep(1)

    elif Input_Strike_Call is not None and Input_Strike_Put is None:
        Index_call = Initial_DF.index[(Initial_DF['Strike'] == Input_Strike_Call)].tolist()
        Index_call=Index_call[0]
        Order_ID_Call=Initial_DF.loc[Index_call,"Order_ID"]

        SL_Call=Initial_DF.loc[Index_call,"Trailing SL"]
        SL_Call_Trig=SL_Call-0.05

        current_time = datetime.now().strftime("%I:%M").lstrip('0')

        Initial_time=Closest_time(current_time)
        index_time=time_list.index(Initial_time)
        New_time=time_list[index_time+1]

        while True:
            current_time = datetime.now().strftime("%I:%M").lstrip('0')

            Initial_time=Closest_time(current_time)
            Status_call=Status_compute(Order_ID_Call)

            if Status_call=="COMPLETE" and Initial_time<New_time:
                Market_order_Buy(quote_call_Hedges,size,Input_Strike_Call_Hedge,"Call")
                SL_Initiate_order(quote_call,size,SL_Call,SL_Call_Trig,Input_Strike_Call,"Call")
                Initial_DF.loc[Index_call,"Status"]="COMPLETE"

                Initial_DF.to_csv(Path_backtest_Report+"Running_Status_of_trade.csv",index=False)
                break

            elif Initial_time>=New_time:
                Status_call=Status_compute(Order_ID_Call)

                if Status_call=="TRIGGER PENDING":
                    Call_CP,quote_CE=Compute_token_Closing_price(Input_Strike_Call,"Call")
                    Modify_SL_Order(Order_ID_Call,size,Call_CP,"Initial Price")
                else:
                    pass

                index_time=time_list.index(New_time)
                New_time=time_list[index_time+1]

            else:
                pass

            time.sleep(1)


    elif Input_Strike_Put is not None and Input_Strike_Call is None:
        Index_put = Initial_DF.index[(Initial_DF['Strike'] == Input_Strike_Put)].tolist()
        Index_put=Index_put[0]
        Order_ID_Put=Initial_DF.loc[Index_put,"Order_ID"]
        SL_Put=Initial_DF.loc[Index_put,"Trailing SL"]
        SL_Put_Trig=SL_Put-0.05

        current_time = datetime.now().strftime("%I:%M").lstrip('0')

        Initial_time=Closest_time(current_time)
        index_time=time_list.index(Initial_time)
        New_time=time_list[index_time+1]

        while True:
            current_time = datetime.now().strftime("%I:%M").lstrip('0')

            Initial_time=Closest_time(current_time)
            Status_put=Status_compute(Order_ID_Put)

            if Status_put=="COMPLETE" and Initial_time<New_time:
                Market_order_Buy(quote_put_Hedges,size,Input_Strike_Put_Hedge,"Put")
                SL_Initiate_order(quote_put,size,SL_Put,SL_Put_Trig,Input_Strike_Put,"Put")

                Initial_DF.loc[Index_put,"Status"]="COMPLETE"
                Initial_DF.to_csv(Path_backtest_Report+"Running_Status_of_trade.csv",index=False)

                break
            elif Initial_time>=New_time:
                Status_put=Status_compute(Order_ID_Put)

                if Status_put=="TRIGGER PENDING":
                    Put_CP,quote_PE=Compute_token_Closing_price(Input_Strike_Put,"Put")
                    Modify_SL_Order(Order_ID_Put,size,Put_CP,"Initial Price")
                else:
                    pass

                index_time=time_list.index(New_time)
                New_time=time_list[index_time+1]

            else:
                pass

            time.sleep(1) 

    else:
        pass

def Trailing_SL(Active_strike_list_Call,Active_strike_list_Put):
    global Market_Trend
    
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

            CE_CP,QE_CE=Compute_token_Closing_price(CE_stk,"Call")
            PE_CP,QE_PE=Compute_token_Closing_price(PE_stk,"Put")

            New_SL_CE=2*CE_CP
            New_SL_PE=2*PE_CP

            if New_SL_CE<SL_Call:
                Modify_SL_Order(OID_Call,size,New_SL_CE,"Trailing SL")
            elif New_SL_PE<SL_Put:
                Modify_SL_Order(OID_Put,size,New_SL_PE,"Trailing SL")
            else:
                pass

        elif Status_call=="COMPLETE":
            Initial_DF.loc[Index_call,"Status"]="COMPLETE"
            Market_Trend="Trending Up"

            with open(Path_backtest_Report+"Market_trend_file.txt", "w") as file:
                file.write(Market_Trend)
            New_order_Placement(Active_strike_list_Call,Active_strike_list_Put)

        elif Status_put=="COMPLETE":
            Initial_DF.loc[Index_put,"Status"]
            Market_Trend="Trending Down"

            with open(Path_backtest_Report+"Market_trend_file.txt", "w") as file:
                file.write(Market_Trend)
            New_order_Placement(Active_strike_list_Call,Active_strike_list_Put)

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
                PE_CP,QE_PE=Compute_token_Closing_price(PE_stk,"Put")
                New_SL_PE=2*PE_CP

                if New_SL_PE<SL_Put:
                    Modify_SL_Order(OID_Put,size,New_SL_PE,"Trailing SL")
                else:
                    pass
            elif Status_put=="COMPLETE":
                Active_strike_list_Put.remove(PE_stk)

            else:
                pass

        Index_call = Initial_DF.index[(Initial_DF['Strike'] == -CE_stk)].tolist()
        OID_Call=Initial_DF.loc[Index_call[0],"Order_ID"]
        Status_call=Status_compute(OID_Call)

        if Status_call=="TRIGGER PENDING":
            Idx_call = Initial_DF.index[(Initial_DF['Strike'] == CE_stk)].tolist()
            SL_Call=Initial_DF.loc[Idx_call[0],"Trailing SL"]
            CE_CP,QE_CE=Compute_token_Closing_price(CE_stk,"Call")
            New_SL_CE=2*CE_CP

            if New_SL_CE<SL_Call:
                Modify_SL_Order(OID_Call,size,New_SL_CE,"Trailing SL")
            else:
                pass
        
        elif Status_call=="COMPLETE":
            Length_put=len(Active_strike_list_Put)

            if Length_put>4:
                print("Maximum Credit limit reached")
            else:
                New_order_Placement(Active_strike_list_Call,Active_strike_list_Put)


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
                CE_CP,QE_CE=Compute_token_Closing_price(CE_stk,"Call")

                New_SL_CE=2*CE_CP

                if New_SL_CE<SL_Call:
                    Modify_SL_Order(OID_Call,size,New_SL_CE,"Trailing SL")
                else:
                    pass
            elif Status_call=="COMPLETE":
                Active_strike_list_Call.remove(CE_stk)

            else:
                pass

        Index_put = Initial_DF.index[(Initial_DF['Strike'] == -PE_stk)].tolist()
        OID_Put=Initial_DF.loc[Index_put[0],"Order_ID"]
        Status_put=Status_compute(OID_Put)

        if Status_put=="TRIGGER PENDING":
            Idx_put = Initial_DF.index[(Initial_DF['Strike'] == PE_stk)].tolist()
            SL_Put=Initial_DF.loc[Idx_put[0],"Trailing SL"]
            PE_CP,QE_PE=Compute_token_Closing_price(PE_stk,"Put")

            New_SL_PE=2*PE_CP

            if New_SL_PE<SL_Put:
                Modify_SL_Order(OID_Put,size,New_SL_PE,"Trailing SL")
            else:
                pass

        elif Status_call=="COMPLETE":
            Length_call=len(Active_strike_list_Call)

            if Length_call>4:
                print("Maximum Credit limit reached")
            else:
                New_order_Placement(Active_strike_list_Call,Active_strike_list_Put)

    else:
        pass

def New_order_Placement(Active_strike_list_Call,Active_strike_list_Put):
    global enctoken
    global Market_Trend
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
            limit_order_Sell(qte_put,Deployed_Size,CP_Put,New_Call_Strike,"Put")

            Order_execution_Check(New_Call_Strike,New_Put_Strike,qte_call_hedge,qte_put_hedge,qte_call,qte_put,New_Put_Strike_hedges,New_Call_Strike_hedges)

        elif length_put==3:
            Put_strike=Active_strike_list_Put[length_put-1]
            New_Put_Strike=Put_strike+50      

            Active_strike_list_Put.append(New_Put_Strike)
            New_Put_Strike_hedges=New_Put_Strike-600

            CP_Put,qte_put=Compute_token_Closing_price(New_Put_Strike,"Put")            
            CP_Put_hedge,qte_put_hedge=Compute_token_Closing_price(New_Put_Strike_hedges,"Put")

            limit_order_Sell(qte_put,Deployed_Size,CP_Put,New_Put_Strike,"Put")

            Order_execution_Check(None,New_Put_Strike,None,qte_put_hedge,None,qte_put,New_Put_Strike_hedges,None)

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
            limit_order_Sell(qte_put,Deployed_Size,CP_Put,New_Call_Strike,"Put")

            Order_execution_Check(New_Call_Strike,New_Put_Strike,qte_call_hedge,qte_put_hedge,qte_call,qte_put,New_Put_Strike_hedges,New_Call_Strike_hedges)

        elif length_call==3:
            Call_strike=Active_strike_list_Call[length_call-1]
            New_Call_Strike=Call_strike-50      

            Active_strike_list_Call.append(New_Call_Strike)
            New_Call_Strike_hedges=New_Call_Strike+600

            CP_Call,qte_call=Compute_token_Closing_price(New_Call_Strike,"Call")            
            CP_Call_hedge,qte_call_hedge=Compute_token_Closing_price(New_Call_Strike_hedges,"Call")

            limit_order_Sell(qte_call,Deployed_Size,CP_Call,New_Call_Strike,"Call")

            Order_execution_Check(New_Call_Strike,None,qte_call_hedge,None,qte_call,None,None,New_Call_Strike_hedges)
        else:
            pass


def Morning_run():
    global Active_strike_list_Call
    global Active_strike_list_Put

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
                    SL_Initiate_order(quote_call,size,CP_CALL,SL_Call_Trig,Active_strike_list_Call[0],"Call")
                    Market_Trend="Trending Up"
                    with open(Path_backtest_Report+"Market_trend_file.txt", "w") as file:
                        file.write(Market_Trend)
                    

                if CP_PUT>=SL_PE:
                    SL_Put_Trig=CP_PUT-0.05
                    SL_Initiate_order(quote_put,size,CP_PUT,SL_Put_Trig,Active_strike_list_Put[0],"Put")
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
            CP_CALL,QTE_CALL=Compute_token_Closing_price(CE_STK,"Call")

            for i in range(len(Active_strike_list_Put)):
                PE_STK=Active_strike_list_Put[i]
                CP_PUT,QTE_PUT=Compute_token_Closing_price(PE_STK,"Put")
                closing_price_put.append(CP_PUT)

            if current_time >= target_time:

                for i in range(len(Active_strike_list_Put)):
                    CP_PE=closing_price_put[i]
                    SL_PE=Stop_Loss_arr_Put[i]

                    if CP_PE>=SL_PE:
                        SL_Put_Trig=CP_PE-0.05
                        SL_Initiate_order(quote_put,size,CP_PE,SL_Put_Trig,Active_strike_list_Put[i],"Put")
                    else:
                        pass

                if CP_CALL>=SL_CE:
                    SL_Call_Trig=CP_CALL-0.05
                    SL_Initiate_order(quote_call,size,CP_CALL,SL_Call_Trig,Active_strike_list_Call[0],"Call")
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
            CP_PUT,QTE_PUT=Compute_token_Closing_price(PE_STK,"Put")

            for i in range(len(Active_strike_list_Call)):
                CE_STK=Active_strike_list_Call[i]
                CP_CALL,QTE_CALL=Compute_token_Closing_price(CE_STK,"Call")
                closing_price_put.append(CP_CALL)

            if current_time >= target_time:

                for i in range(len(Active_strike_list_Call)):
                    CP_CE=closing_price_call[i]
                    SL_CE=Stop_Loss_arr_Call[i]
                    if CP_CE>=SL_CE:
                        SL_Call_Trig=CP_PE-0.05
                        SL_Initiate_order(quote_put,size,CP_CE,SL_Call_Trig,Active_strike_list_Call[i],"Call")
                    else:
                        pass

                if CP_PUT>=SL_PE:
                    SL_Put_Trig=CP_PUT-0.05
                    SL_Initiate_order(quote_call,size,CP_PUT,SL_Put_Trig,Active_strike_list_Call[0],"Call")
                else:
                    pass

                break
            time.sleep(300)  
    else:
        pass
    


path_main="D:/ashu/Finance/algo_trading/Zerodha_GUI/Kite_Zerodha-main/Kite_Zerodha-main/"
Path_backtest_Report="D:/ashu/Finance/algo_trading/Zerodha_GUI/Kite_Zerodha-main/Kite_Zerodha-main/Back_Test_Files_Report/"

df=pd.read_csv(path_main+"Enctoke_Expiry_month_end_info.csv")
content_enctoken=df.iloc[0,0]
enctoken = content_enctoken




Initial_day=1
Input_Strike_Put=21000
Input_Strike_Call=22500
Input_Strike_Put_Hedge=Input_Strike_Put-600
Input_Strike_Call_Hedge=Input_Strike_Call+600

Initiate_time="09:20"
Desired_time="09:30"

size=1
Deployed_Size=50*size

start_time = datetime.strptime("9:15", "%H:%M")
end_time = datetime.strptime("15:30", "%H:%M")

interval = timedelta(minutes=5)
time_list = []

current_time = start_time
while current_time <= end_time:
    time_list.append(current_time.strftime("%H:%M"))
    current_time += interval


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


    # limit_order_Sell(quote_call,Deployed_Size,Call_Closing_Price,Strike,Right)
    # limit_order_Sell(quote_put,Deployed_Size,Put_Closing_Price,Strike,Right)


    Order_execution_Check(Input_Strike_Call,Input_Strike_Put,quote_call_Hedges,quote_put_Hedges,quote_call,quote_put,Input_Strike_Call_Hedge,Input_Strike_Put_Hedge)

    Trailing_SL(Active_strike_list_Call,Active_strike_list_Put)

else:
    Morning_run()
    Trailing_SL(Active_strike_list_Call,Active_strike_list_Put)