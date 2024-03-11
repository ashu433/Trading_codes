from tkinter import *
import Intraday_live_data
import pandas as pd
from kite_trade import *
import os
import math
import ast
import subprocess

#######################################################################################################################################################
#######################################################################################################################################################
#######################################################################################################################################################
#######################################################################################################################################################
###############                                                   Functions                                                           #################
#######################################################################################################################################################
#######################################################################################################################################################
#######################################################################################################################################################
#######################################################################################################################################################

##################################### Order Execution #######################################################
def Overall_size_computation():
    global order_info
    global path_kite_main
    global Buy_status
    global enctoken
    kite = KiteApp(enctoken=enctoken)

    x=kite.orders()
    l1=len(x)
    Status=x[l1-1]['status']

    if Status=="COMPLETE":
        if order_info["Order Placed Type"]=="Buy Limit":

            with open(path_kite_main+"Buy_Size.txt",'r') as file:
                read_content=file.read()

            read_content=int(read_content)

            read_content=read_content+order_info["Size_Buy"]
            

            if read_content>0:
                Buy_status=1
                order_info["Buy Status"]=Buy_status
            else:
                Buy_status=0
                order_info["Buy Status"]=Buy_status

            with open(path_kite_main+"Buy_Size.txt",'w') as file:
                file.write(str(read_content))


        elif order_info["Order Placed Type"]=="Sell Limit":

            with open(path_kite_main+"Buy_Size.txt",'r') as file:
                read_content=file.read()

            read_content=int(read_content)

            read_content=read_content-order_info["Size_Sell"]

            if read_content>0:
                Buy_status=1
                order_info["Buy Status"]=Buy_status
            else:
                Buy_status=0
                order_info["Buy Status"]=Buy_status

            with open(path_kite_main+"Buy_Size.txt",'w') as file:
                file.write(str(read_content))

    elif Status=="OPEN":
        print("Trigger pending")

    else:
        pass

    if Status =="COMPLETE":
        if order_info["Order Placed Type"]=="Stop Loss sell Limit":

            with open(path_kite_main+"Buy_Size.txt",'r') as file:
                read_content=file.read()

            read_content=int(read_content)

            
            read_content=read_content-order_info["Size_Buy"]

            if read_content>0:
                Buy_status=1
                order_info["Buy Status"]=Buy_status
            else:
                Buy_status=0
                order_info["Buy Status"]=Buy_status

            with open(path_kite_main+"Buy_Size.txt",'w') as file:
                file.write(str(read_content))

        elif order_info["Order Placed Type"]=="modify order SL":
            with open(path_kite_main+"Buy_Size.txt",'r') as file:
                read_content=file.read()

            read_content=int(read_content)
            read_content=read_content-order_info["Stop_loss_Size_sell"]

            if read_content>0:
                Buy_status=1
                order_info["Buy Status"]=Buy_status
            else:
                Buy_status=0
                order_info["Buy Status"]=Buy_status

            with open(path_kite_main+"Buy_Size.txt",'w') as file:
                file.write(str(read_content))

    elif Status == "TRIGGER PENDING":
        print("Trigger Price is still not hit")
    else:
        pass





################## LIMIT BUY ORDER ###############
def limit_order_Placement_buy():

    global enctoken
    kite = KiteApp(enctoken=enctoken)
    global order_info
    global Buy_status
    global path_kite_main
    global path_virtual
    import datetime
    global cancel
    import time


    InstrumentID=order_info["Trading_symbol"]
    
    with open(path_virtual+"Buy_Price.txt",'r') as file:
        content=file.read()

    price=ast.literal_eval(content)
    Buy_price=float(price["Buy_Price"])
    trigger_price=float(price["Trigger_Price"])

    l112.config(text=str(Buy_price)+": Pending")

    while True:
        start_time = time.time()
        x=kite.ltp(["NFO:"+InstrumentID])
        price=float(x['NFO:'+InstrumentID]['last_price'])

        if (price==Buy_price or price==trigger_price):
            print("Order Executed")
            current_datetime = datetime.datetime.now()
            formatted_time = current_datetime.strftime("%H:%M:%S")
            formatted_date = current_datetime.strftime("%d %B %Y")
            df=pd.read_csv(path_virtual+"trade_Virtual_excel.csv")
            rows=df.shape[0]
            df.iloc[rows,0]=formatted_date
            df.iloc[rows,1]=formatted_time
            df.iloc[rows,2]=Buy_price
            df.iloc[rows,3]=0
            l112.config(text=str(Buy_price)+": Executed")
            break
        elif cancel==1:
            print("Ordered Cancelled")
        else:
            pass

        elapsed_time = time.time() - start_time
        sleep_time = max(0, 0.01 - elapsed_time) 
        time.sleep(sleep_time)

    



    order_info["Trading Var"]=trading_var.get()
    order_info["Order Type Var"]=Order_type_var.get()
    order_info["Order Placed Type"]="Buy Limit"

    print(f"Buy Limit Order: {order_info}")

    with open(path_kite_main+"Order_Log_File.txt","r") as file:
        content=file.read()

    log_file = ast.literal_eval(content)

    log_file.append(order_info)

    with open(path_kite_main+"Order_Log_File.txt","w") as file:
        file.write(str(log_file))

    # order_update_func()
    order_info["Buy_Price"]=0
################## LIMIT BUY ORDER ########################

######################### LIMIT Sell ORDER ################
def limit_order_Placement_sell():

    global enctoken
    kite = KiteApp(enctoken=enctoken)
    global order_info
    global virtua_selling_start

    sell_price=order_info["Sell_Price"]
    trig_price_sell=order_info["Sell_Trigger_Price"]
    virtual_order={}
    virtual_order["Sell_Price"]=sell_price
    virtual_order["Trigger_Price_sell"]=trig_price_sell
    l115.config(text=str(sell_price)+": Pending")
    

    with open(path_virtual+"Sell_Price.txt",'w') as file:
        file.write(virtual_order)
    
    virtua_selling_start=1



    order_info["Trading Var"]=trading_var.get()
    order_info["Order Type Var"]=Order_type_var.get()
    order_info["Order Placed Type"]="Sell Limit"

    print(f"Sell Limit Order: {order_info}")

    with open(path_kite_main+"Order_Log_File.txt","r") as file:
        content=file.read()

    log_file = ast.literal_eval(content)

    log_file.append(order_info)

    with open(path_kite_main+"Order_Log_File.txt","w") as file:
        file.write(str(log_file))

    # order_update_func()
    order_info["Sell_Price"]=0
####################### LIMIT Sell ORDER ####################


########################### Stop Loss Limit ################

def Stop_loss_sell_limit():
    global enctoken
    kite = KiteApp(enctoken=enctoken)
    global order_info
    global virtua_selling_start

    # virtua_selling_start=1
    order_info["Trading Var"]=trading_var.get()
    order_info["Order Type Var"]=Order_type_var.get()
    order_info["Order Placed Type"]="Stop Loss sell Limit"

    print(f"Stop Loss Sell Limit Order: {order_info}")

    with open(path_kite_main+"Order_Log_File.txt","r") as file:
        content=file.read()

    log_file = ast.literal_eval(content)

    log_file.append(order_info)

    with open(path_kite_main+"Order_Log_File.txt","w") as file:
        file.write(str(log_file))

########################### Stop Loss Limit ################

####################### Modify ORDER ####################

def modify_order_buy_Limit():

    global order_info
    import datetime

    global enctoken
    kite = KiteApp(enctoken=enctoken)

    InstrumentID=order_info["Trading_symbol"]
    
    with open(path_virtual+"Buy_Price.txt",'r') as file:
        content=file.read()

    price=ast.literal_eval(content)
    Buy_price=float(price["Buy_Price"])
    trigger_price=float(price["Trigger_Price"])

    l112.config(text=str(Buy_price)+": Pending")

    while True:
        x=kite.ltp(["NFO:"+InstrumentID])
        price=float(x['NFO:'+InstrumentID]['last_price'])

        if (price==Buy_price | price==trigger_price):
            print("Order Executed")
            current_datetime = datetime.datetime.now()
            formatted_time = current_datetime.strftime("%H:%M:%S")
            formatted_date = current_datetime.strftime("%d %B %Y")
            df=pd.read_csv(path_virtual+"trade_Virtual_excel.csv")
            rows=df.shape[0]
            df.iloc[rows,0]=formatted_date
            df.iloc[rows,1]=formatted_time
            df.iloc[rows,2]=Buy_price
            df.iloc[rows,3]=0
            l112.config(text=str(Buy_price)+": Executed")
            break
        elif cancel==1:
            print("Ordered Cancelled")
        else:
            pass
    
    print(f"Modified Buy Order: {order_info}")

    order_info["Order Placed Type"]="modify order buy Limit"

    with open(path_kite_main+"Order_Log_File.txt","r") as file:
        content=file.read()

    log_file = ast.literal_eval(content)

    log_file.append(order_info)

    with open(path_kite_main+"Order_Log_File.txt","w") as file:
        file.write(str(log_file))


def modify_order_sell_Limit():

    global order_info
    global enctoken
    kite = KiteApp(enctoken=enctoken)

    sell_price=order_info["Sell_Price"]
    trig_price_sell=order_info["Sell_Trigger_Price"]
    virtual_order={}
    virtual_order["Sell_Price"]=sell_price
    virtual_order["Trigger_Price_sell"]=trig_price_sell
    l115.config(text=str(sell_price)+": Pending")
    

    with open(path_virtual+"Sell_Price.txt",'w') as file:
        file.write(virtual_order)
    
    virtua_selling_start=1


    order_info["Order Placed Type"]="modify order sell Limit"

    with open(path_kite_main+"Order_Log_File.txt","r") as file:
        content=file.read()

    log_file = ast.literal_eval(content)

    log_file.append(order_info)

    with open(path_kite_main+"Order_Log_File.txt","w") as file:
        file.write(str(log_file))

def modify_order_SL():
    global order_info
    global enctoken
    global path_kite_main
    global virtua_selling_start

    kite = KiteApp(enctoken=enctoken)
    # virtua_selling_start=1


    order_info["Order Placed Type"]="modify order SL"

    with open(path_kite_main+"Order_Log_File.txt","r") as file:
        content=file.read()

    log_file = ast.literal_eval(content)

    log_file.append(order_info)

    with open(path_kite_main+"Order_Log_File.txt","w") as file:
        file.write(str(log_file))

####################### Modify ORDER ####################

####################### Cancel ORDER ####################
def cancel_order_cmd():

    global order_info
    global enctoken
    global cancel
    kite = KiteApp(enctoken=enctoken)

    cancel=1


def Virtual_buy():
    global order_info
    global path_virtual

    buy_price=order_info["Buy_Price"]
    trig_price=order_info["Trigger_Price"]
    virtual_order={}
    virtual_order["Buy_Price"]=buy_price
    virtual_order["Trigger_Price"]=trig_price

    with open(path_virtual+"Buy_Price.txt",'w') as file:
        file.write(str(virtual_order))


def Virtual_sell():
    pass





####################### Cancel ORDER ####################
##################################### Order Execution #######################################################

########################################### Quick Order Processing #################################################

def Quick_order_price_computation():

    global enctoken
    global order_info
    import datetime
    global data_dict_1_min
    global data_dict_5_min


    data_dict_5_min={}
    data_dict_1_min={}

    kite = KiteApp(enctoken=enctoken)

    instrument_token = order_info["Token"]
    from_datetime = datetime.datetime.now() - datetime.timedelta(days=3)     # From last & days
    to_datetime = datetime.datetime.now()
    interval = "minute"
    x=kite.historical_data(instrument_token, from_datetime, to_datetime, interval, continuous=False, oi=False)

    l=len(x)
    p=2

    dt=x[l-p]['date']
    split_datetime_list = [(dt.strftime('%Y-%m-%d'), dt.strftime('%H:%M'))]
    date=split_datetime_list[0][0]
    time=split_datetime_list[0][1]

    data_dict_1_min = {
    'Date': date,
    'Time': time,
    'open': x[l-p]['open'],
    'high': x[l-p]['high'],
    'low': x[l-p]['low'],
    'close': x[l-p]['close']
    }

    instrument_token = order_info["Token"]
    from_datetime = datetime.datetime.now() - datetime.timedelta(days=7)     # From last & days
    to_datetime = datetime.datetime.now()
    interval = "5minute"
    x=kite.historical_data(instrument_token, from_datetime, to_datetime, interval, continuous=False, oi=False)

    l=len(x)
    p=2

    dt=x[l-p]['date']
    split_datetime_list = [(dt.strftime('%Y-%m-%d'), dt.strftime('%H:%M'))]
    date=split_datetime_list[0][0]
    time=split_datetime_list[0][1]

    data_dict_5_min = {
    'Date': date,
    'Time': time,
    'open': x[l-p]['open'],
    'high': x[l-p]['high'],
    'low': x[l-p]['low'],
    'close': x[l-p]['close']
    }

########################################### Quick Order Processing #################################################

############################ Order Type CE or PE  Function #############################################

def Call_side_Order():

    from datetime import datetime
    global ATM_Strike_Price
    global ATM_Strike_Price_Plus_1
    global ATM_Strike_Price_Minus_1
    global expiry
    global call_list
    global token

    global enctoken
    kite = KiteApp(enctoken=enctoken)

    global previous_value

    x=Order_type_var.get()

    strike_price=[ATM_Strike_Price_Plus_1,ATM_Strike_Price,ATM_Strike_Price_Minus_1]

    if x == previous_value:
        return
    
    previous_value=x

    if x==1:
        if Month_end_var.get()==40:
            call_list=[]
            token=[]
            parsed_date = datetime.strptime(expiry, '%d-%b-%Y')
            formatted_date = parsed_date.strftime('%Y%b').upper()
            name="NIFTY"


            formatted_date=formatted_date[2:]

            for i in range(len(strike_price)):
                quote=name+formatted_date+str(strike_price[i])+"CE"
                call_list.append(quote)

            print(call_list)

            for j in range(len(call_list)):
                atm_token_ce=kite.ltp("NFO:"+call_list[j])
                ATM_Token=atm_token_ce["NFO:"+call_list[j]]['instrument_token']
                token.append(ATM_Token)


            print(call_list)
            print(token)
        else:
            call_list=[]
            token=[]
            parsed_date = datetime.strptime(expiry, '%d-%b-%Y')
            formatted_date = parsed_date.strftime('%y%m%d')
            name="NIFTY"

            char_list = list(formatted_date)

            if char_list[2]=='0':
                char_list.pop(2)

            formatted_date=''.join(char_list)

            for i in range(len(strike_price)):
                quote=name+formatted_date+str(strike_price[i])+"CE"
                call_list.append(quote)

            for j in range(len(call_list)):
                atm_token_ce=kite.ltp("NFO:"+call_list[j])
                ATM_Token=atm_token_ce["NFO:"+call_list[j]]['instrument_token']
                token.append(ATM_Token)


            print(call_list)
            print(token)
    

def Put_side_Order():

    from datetime import datetime

    global ATM_Strike_Price
    global ATM_Strike_Price_Plus_1
    global ATM_Strike_Price_Minus_1
    global expiry
    global put_list
    global previous_value
    global token

    global enctoken
    kite = KiteApp(enctoken=enctoken)

    x=Order_type_var.get()

    strike_price=[ATM_Strike_Price_Plus_1,ATM_Strike_Price,ATM_Strike_Price_Minus_1]

    if x == previous_value:
        return
    
    previous_value=x

    if x==2:
        if Month_end_var.get()==40:
            put_list=[]
            token=[]
            parsed_date = datetime.strptime(expiry, '%d-%b-%Y')
            formatted_date = parsed_date.strftime('%Y%b').upper()
            name="NIFTY"
            formatted_date=formatted_date[2:]

            for i in range(len(strike_price)):
                quote=name+formatted_date+str(strike_price[i])+"PE"
                put_list.append(quote)

            for j in range(len(put_list)):
                atm_token_pe=kite.ltp("NFO:"+put_list[j])
                ATM_Token=atm_token_pe["NFO:"+put_list[j]]['instrument_token']
                token.append(ATM_Token)

            print(put_list)
            print(token)

        else:
            put_list=[]
            token=[]
            parsed_date = datetime.strptime(expiry, '%d-%b-%Y')
            formatted_date = parsed_date.strftime('%y%m%d')
            name="NIFTY"

            char_list = list(formatted_date)

            if char_list[2]=='0':
                char_list.pop(2)

            formatted_date=''.join(char_list)

            for i in range(len(strike_price)):
                quote=name+formatted_date+str(strike_price[i])+"PE"
                put_list.append(quote)

            for j in range(len(put_list)):
                atm_token_pe=kite.ltp("NFO:"+put_list[j])
                ATM_Token=atm_token_pe["NFO:"+put_list[j]]['instrument_token']
                token.append(ATM_Token)

            print(put_list)
            print(token)

############################ Order Type CE or PE  Function #############################################

################################# Buying and selling Functions #########################################


def Buy():
    global order_info
    global Moving_Average_Buying
    xox=0

    key_list=list(order_info.keys())

    if Moving_Average_Buying:
        if 'Trading_symbol' in key_list:
            xox=xox + 1
        else:
            message_label.config(text="Please Enter the Type of trade")

        if 'Size_Buy' in key_list:
            xox=xox + 1
        else:
            message_label.config(text="Please Enter the Buy Size")

        if 'Buy_Price' in key_list:
            xox=xox + 1
        else:
            message_label.config(text="Please Enter the Buy Price")

        if order_info["Buy_Price"]==0:
            message_label.config(text="Please Enter the Buy Price")
        else:
            xox=xox + 1

        if order_info["Size_Buy"]==0:
            message_label.config(text="Please Enter the Buy Size")
        else:
            xox=xox + 1

        if xox ==5:
            message_label.config(text="Good to go!")
            order_info["Buy Status"]=1
            print(order_info)
            limit_order_Placement_buy()
    else:
         message_label.config(text="Please place Buy price from the Moving Average Buy section")


    print(xox)



def Sell():
    global order_info
    global Moving_Average_Selling

    if Moving_Average_Selling:
        if order_info["Buy Status"]==1:    
            sos=0
            
            key_list=list(order_info.keys())

            if 'Trading_symbol' in key_list:
                sos=sos + 1
            else:
                message_label.config(text="Please Enter the Type of trade")

            if 'Size_Sell' in key_list:
                sos=sos + 1
            else:
                message_label.config(text="Please Enter the Sell Size")

            if 'Sell_Price' in key_list:
                sos=sos + 1
            else:
                message_label.config(text="Please Enter the Sell Price")

            if order_info["Sell_Price"]==0:
                message_label.config(text="Please Enter the Sell Price")
            else:
                sos=sos + 1

            if order_info["Size_Sell"]==0:
                message_label.config(text="Please Enter the Sell Size")
            else:
                sos=sos + 1

            if sos ==5:
                message_label.config(text="Good to go!")
                print(order_info)
                limit_order_Placement_sell()

        else:
            message_label.config(text="Please Before selling Buy first")
    else:
        message_label.config(text="Please Place Sell Order in the Moving Average sell section")



def IBuy():
    global order_info
    global Buy_status
    global Immediate_Buying
    global path
    xox=0
    
    key_list=list(order_info.keys())

    if Immediate_Buying:
        if 'Trading_symbol' in key_list:
            xox=xox + 1
        else:
            message_label.config(text="Please Enter the Type of trade")

        if 'Size_Buy' in key_list:
            xox=xox + 1
        else:
            message_label.config(text="Please Enter the Buy Size")

        if 'Buy_Price' in key_list:
            xox=xox + 1
        else:
            message_label.config(text="Please Enter the Buy Price")

        if order_info["Buy_Price"]==0:
            message_label.config(text="Please Enter the Buy Price")
        else:
            xox=xox + 1

        if order_info["Size_Buy"]==0:
            message_label.config(text="Please Enter the Buy Size")
        else:
            xox=xox + 1

        if xox ==5:
            message_label.config(text="Good to go!")
            order_info["Buy Status"]=1
            print(order_info)
            limit_order_Placement_buy()
    else:
         message_label.config(text="Please place Buy price from the Immediate section")


    print(xox)

    




def ISell():

    global order_info
    global Immediate_Selling
    global path

    if Immediate_Selling:
        if order_info["Buy Status"]==1:    
            sos=0
            
            key_list=list(order_info.keys())

            if 'Trading_symbol' in key_list:
                sos=sos + 1
            else:
                message_label.config(text="Please Enter the Type of trade")

            if 'Size_Sell' in key_list:
                sos=sos + 1
            else:
                message_label.config(text="Please Enter the Sell Size")

            if 'Sell_Price' in key_list:
                sos=sos + 1
            else:
                message_label.config(text="Please Enter the Sell Price")

            if order_info["Sell_Price"]==0:
                message_label.config(text="Please Enter the Sell Price")
            else:
                sos=sos + 1

            if order_info["Size_Sell"]==0:
                message_label.config(text="Please Enter the Sell Size")
            else:
                sos=sos + 1

            if sos ==5:
                message_label.config(text="Good to go!")
                print(order_info)
                limit_order_Placement_sell()

        else:
            message_label.config(text="Please Before selling Buy first")
    else:
        message_label.config(text="Please Place Sell Order in the Immediate section")






################################# Buying and selling Functions #########################################

############################ Type Trading ##################################################################

def Testing(): 
    global call_list
    global put_list
    global order_info
    global token

    lot_entry.config(state=DISABLED)
    lot_entry_Sell.config(state=DISABLED)

    if Order_type_var.get()==1: ########### call side ###############
        order_info["Trading_symbol"]=call_list[0]
        order_info["Token"]=token[0]
        order_info["Size_Buy"]=50
        order_info["Size_Sell"]=50
        order_info["Stop_loss_Size_sell"]=50
    elif Order_type_var.get()==2: ########### put side ###############
        order_info["Trading_symbol"]=put_list[2]
        order_info["Token"]=token[2]
        order_info["Size_Buy"]=50
        order_info["Size_Sell"]=50
        order_info["Stop_loss_Size_sell"]=50
    else:
        pass

def Real_Trading(): 

    lot_entry.config(state=NORMAL)
    lot_entry_Sell.config(state=NORMAL)



def size_computation_buy():
    global call_list
    global put_list
    global order_info

    if Order_type_var.get()==1: ########### call side ###############
        if trading_var.get()==4:  ########### Serious Trading ###############
            size=int(lot_entry.get())
            net_size=50*size
            order_info["Trading_symbol"]=call_list[2]
            order_info["Token"]=token[2]
            order_info["Size_Buy"]=net_size
            print(net_size)
        else:
            pass
    if Order_type_var.get()==2: ########### put side ###############
        if trading_var.get()==4:  ########### Serious Trading ###############
            size=int(lot_entry.get())
            net_size=50*size
            order_info["Trading_symbol"]=put_list[0]
            order_info["Token"]=token[0]
            order_info["Size_Buy"]=net_size
            print(net_size)
        else:
            pass

    if Modify_buy_var.get()==11:
        if trading_var.get()==4:
            size=int(lot_entry.get())
            net_size=50*size
            order_info["Size_Buy"]=net_size
            Buy_size.config(text=f"{net_size}")
        else:
            pass
    else:
        pass

def size_computation_sell():
    global call_list
    global put_list
    global order_info

    if Order_type_var.get()==1: ########### call side ###############
        if trading_var.get()==4:  ########### Serious Trading ###############
            size=int(lot_entry_Sell.get())
            net_size=50*size
            order_info["Trading_symbol"]=call_list[2]
            order_info["Token"]=token[2]
            order_info["Size_Sell"]=net_size
        elif trading_var.get()==3: ########### Testing Trading ###############
            net_size=50
            order_info["Trading_symbol"]=call_list[0]
            order_info["Token"]=token[0]
            order_info["Size_Sell"]=net_size
        else:
            pass
    if Order_type_var.get()==2: ########### put side ###############
        if trading_var.get()==4:  ########### Serious Trading ###############
            size=int(lot_entry_Sell.get())
            net_size=50*size
            order_info["Trading_symbol"]=put_list[0]
            order_info["Token"]=token[0]
            order_info["Size_Sell"]=net_size
        elif trading_var.get()==3:
            net_size=50
            order_info["Trading_symbol"]=call_list[2]
            order_info["Token"]=token[2]
            order_info["Size_Sell"]=net_size
        else:
            pass
    else:
        pass

    if Modify_sell_var.get()==12:
        if trading_var.get()==4:
            size=int(lot_entry_Sell.get())
            net_size=50*size
            order_info["Size_Sell"]=net_size
            size_s.config(text=f"{net_size}")
        else:
            pass
    else:
        pass





############################ Type Trading ##################################################################



################################## Constant Updating Functions #################################################################

def update_strike_price():
    global ATM_Strike_Price
    global ATM_Strike_Price_Plus_1
    global ATM_Strike_Price_Minus_1

    global enctoken
    kite = KiteApp(enctoken=enctoken)

    final_new=pd.read_csv(path+"Nifty_option_chain.csv")

    nifty_current_price=kite.ltp(["NSE:NIFTY 50"])
    Nifty_current_price=nifty_current_price['NSE:NIFTY 50']['last_price']

    index = (final_new['strikePrice'] - Nifty_current_price).abs().idxmin()
    ATM_Strike_Price=final_new['strikePrice'].iloc[index]
    ATM_Strike_Price_Plus_1=ATM_Strike_Price+50
    ATM_Strike_Price_Minus_1=ATM_Strike_Price-50

    GUI.after(60000,update_strike_price)


def Moving_average_status_update():
    global order_info
    global MA_1_min
    global MA_5_min

    key_list=list(order_info.keys())

    path_1="D:/ashu/Finance/algo_trading/Zerodha_GUI/raw_data_collected/"

    if MA_loop_var.get()==20:
        if 'Trading_symbol' in key_list:
            Trading_Symbol=order_info["Trading_symbol"]
            data_1_min=pd.read_csv(path_1+Trading_Symbol+".csv")
            data_5_min=pd.read_csv(path_1+Trading_Symbol+"_5_min.csv")

            MA_1_min=[data_1_min["EMA 9"].iloc[-1],data_1_min["EMA 21"].iloc[-1],data_1_min["EMA 50"].iloc[-1],data_1_min["EMA 200"].iloc[-1],data_1_min["Time"].iloc[-1]]
            MA_5_min=[data_5_min["EMA 9"].iloc[-1],data_5_min["EMA 21"].iloc[-1],data_5_min["EMA 50"].iloc[-1],data_5_min["EMA 200"].iloc[-1],data_5_min["Time"].iloc[-1]]
            print("Running")
            l118.config(text="Running")
            # listbox.insert(9,"MA Loop Status: Running")
        else:
            pass
    elif MA_loop_var.get()==21:
        pass
        # listbox.insert(9,"MA Loop Status: Stopped")
    else:
        pass

    GUI.after(1000,Moving_average_status_update)


def MA_code_start():
    path_MA="D:/ashu/Finance/algo_trading/Zerodha_GUI/Kite_Zerodha-main/Kite_Zerodha-main/"

    batch_file_path = path_MA+"data_processing.bat"

    try:
        subprocess.Popen(['start', 'cmd', '/k', batch_file_path], shell=True)
        print("Batch file executed successfully!")
    except subprocess.CalledProcessError:
        print("Error executing the batch file.")


################################## Constant Updating Functions #################################################################



############################################ Menue bar Functions (Immediate Orders)#########################################

############# BUY #######################

def I_High_1min():
    global data_dict_1_min
    global data_dict_5_min
    global order_info
    global Immediate_Buying

    Quick_order_price_computation()
    buy_price=data_dict_1_min["high"]
    trigger_price=data_dict_1_min["high"]-0.05

    if Modify_buy_var.get() ==11:
        order_info["Buy_Price"]=buy_price
        order_info["Trigger_Price"]=round(trigger_price,2)
        order_info["Time"]=data_dict_1_min["Time"]
        Immediate_Buying=True
        Price_buy.config(text="1 min High")
    else:
        order_info["Buy_Price"]=buy_price
        order_info["Trigger_Price"]=round(trigger_price,2)
        order_info["Time"]=data_dict_1_min["Time"]
        Immediate_Buying=True


def I_Low_1min():
    global data_dict_1_min
    global data_dict_5_min
    global order_info
    global Immediate_Buying

    Quick_order_price_computation()

    buy_price=data_dict_1_min["low"]
    trigger_price=data_dict_1_min["low"]-0.05
    if Modify_buy_var.get() ==11:
        order_info["Buy_Price"]=buy_price
        order_info["Trigger_Price"]=round(trigger_price,2)
        order_info["Time"]=data_dict_1_min["Time"]
        Immediate_Buying=True
        Price_buy.config(text="1 min Low")
    else:
        order_info["Buy_Price"]=buy_price
        order_info["Trigger_Price"]=round(trigger_price,2)
        order_info["Time"]=data_dict_1_min["Time"]
        Immediate_Buying=True

    Virtual_buy()


def I_Open_1min():
    global data_dict_1_min
    global data_dict_5_min
    global order_info
    global Immediate_Buying

    Quick_order_price_computation()

    buy_price=data_dict_1_min["open"]
    trigger_price=data_dict_1_min["open"]-0.05

    if Modify_buy_var.get() ==11:
        order_info["Buy_Price"]=buy_price
        order_info["Trigger_Price"]=round(trigger_price,2)
        order_info["Time"]=data_dict_1_min["Time"]
        Immediate_Buying=True
        Price_buy.config(text="1 min Open")
    else:
        order_info["Buy_Price"]=buy_price
        order_info["Trigger_Price"]=round(trigger_price,2)
        order_info["Time"]=data_dict_1_min["Time"]
        Immediate_Buying=True

    Virtual_buy()

def I_Close_1min():
    global data_dict_1_min
    global data_dict_5_min
    global order_info
    global Immediate_Buying

    Quick_order_price_computation()

    buy_price=data_dict_1_min["close"]
    trigger_price=data_dict_1_min["close"]-0.05

    if Modify_buy_var.get() ==11:
        order_info["Buy_Price"]=buy_price
        order_info["Trigger_Price"]=round(trigger_price,2)
        order_info["Time"]=data_dict_1_min["Time"]
        Immediate_Buying=True
        Price_buy.config(text="1 min Close")
    else:
        order_info["Buy_Price"]=buy_price
        order_info["Trigger_Price"]=round(trigger_price,2)
        order_info["Time"]=data_dict_1_min["Time"]
        Immediate_Buying=True     

    Virtual_buy()


def I_High_5min():
    global data_dict_1_min
    global data_dict_5_min
    global order_info
    global Immediate_Buying

    Quick_order_price_computation()
    buy_price=data_dict_5_min["high"]
    trigger_price=data_dict_5_min["high"]-0.05

    if Modify_buy_var.get() ==11:
        order_info["Buy_Price"]=buy_price
        order_info["Trigger_Price"]=round(trigger_price,2)
        order_info["Time"]=data_dict_5_min["Time"]
        Immediate_Buying=True
        Price_buy.config(text="5 min High")
    else:
        order_info["Buy_Price"]=buy_price
        order_info["Trigger_Price"]=round(trigger_price,2)
        order_info["Time"]=data_dict_5_min["Time"]
        Immediate_Buying=True

    Virtual_buy()



def I_Low_5min():
    global data_dict_1_min
    global data_dict_5_min
    global order_info
    global Immediate_Buying

    Quick_order_price_computation()

    buy_price=data_dict_5_min["low"]
    trigger_price=data_dict_5_min["low"]-0.05

    if Modify_buy_var.get() ==11:
        order_info["Buy_Price"]=buy_price
        order_info["Trigger_Price"]=round(trigger_price,2)
        order_info["Time"]=data_dict_5_min["Time"]
        Immediate_Buying=True
        Price_buy.config(text="5 min Low")
    else:
        order_info["Buy_Price"]=buy_price
        order_info["Trigger_Price"]=round(trigger_price,2)
        order_info["Time"]=data_dict_5_min["Time"]
        Immediate_Buying=True

    Virtual_buy()



def I_Open_5min():
    global data_dict_1_min
    global data_dict_5_min
    global order_info
    global Immediate_Buying

    Quick_order_price_computation()

    buy_price=data_dict_5_min["open"]
    trigger_price=data_dict_5_min["open"]-0.05

    if Modify_buy_var.get() ==11:
        order_info["Buy_Price"]=buy_price
        order_info["Trigger_Price"]=round(trigger_price,2)
        order_info["Time"]=data_dict_5_min["Time"]
        Immediate_Buying=True
        Price_buy.config(text="5 min Open")
    else:
        order_info["Buy_Price"]=buy_price
        order_info["Trigger_Price"]=round(trigger_price,2)
        order_info["Time"]=data_dict_5_min["Time"]
        Immediate_Buying=True

    Virtual_buy()

def I_Close_5min():
    global data_dict_1_min
    global data_dict_5_min
    global order_info
    global Immediate_Buying

    Quick_order_price_computation()

    buy_price=data_dict_5_min["close"]
    trigger_price=data_dict_5_min["close"]-0.05

    if Modify_buy_var.get() ==11:
        order_info["Buy_Price"]=buy_price
        order_info["Trigger_Price"]=round(trigger_price,2)
        order_info["Time"]=data_dict_5_min["Time"]
        Immediate_Buying=True
        Price_buy.config(text="5 min Close")
    else:
        order_info["Buy_Price"]=buy_price
        order_info["Trigger_Price"]=round(trigger_price,2)
        order_info["Time"]=data_dict_5_min["Time"]
        Immediate_Buying=True

    Virtual_buy()



############# BUY #######################



############# SELL #######################

def I_High_1min_sell():
    global data_dict_1_min
    global data_dict_5_min
    global order_info
    global Immediate_Selling

    Quick_order_price_computation()
    sell_price=data_dict_1_min["high"]
    sell_trigger_price=data_dict_1_min["high"]+0.05

    if Modify_sell_var.get() ==12:
        order_info["Sell_Price"]=sell_price
        order_info["Sell_Trigger_Price"]=round(sell_trigger_price,2)
        order_info["Time"]=data_dict_1_min["Time"]
        Immediate_Selling=True
        Price_sell.config(text="1 min High")
    else:
        order_info["Sell_Price"]=sell_price
        order_info["Sell_Trigger_Price"]=round(sell_trigger_price,2)
        order_info["Time"]=data_dict_1_min["Time"]
        Immediate_Selling=True
    


def I_Low_1min_sell():
    global data_dict_1_min
    global data_dict_5_min
    global order_info
    global Immediate_Selling

    Quick_order_price_computation()

    sell_price=data_dict_1_min["low"]
    sell_trigger_price=data_dict_1_min["low"]+0.05

    if Modify_sell_var.get() ==12:
        order_info["Sell_Price"]=sell_price
        order_info["Sell_Trigger_Price"]=round(sell_trigger_price,2)
        order_info["Time"]=data_dict_1_min["Time"]
        Immediate_Selling=True
        Price_sell.config(text="1 min Low")
    else:
        order_info["Sell_Price"]=sell_price
        order_info["Sell_Trigger_Price"]=round(sell_trigger_price,2)
        order_info["Time"]=data_dict_1_min["Time"]
        Immediate_Selling=True
    

def I_Open_1min_sell():
    global data_dict_1_min
    global data_dict_5_min
    global order_info
    global Immediate_Selling

    Quick_order_price_computation()

    sell_price=data_dict_1_min["open"]
    sell_trigger_price=data_dict_1_min["open"]+0.05

    if Modify_sell_var.get() ==12:
        order_info["Sell_Price"]=sell_price
        order_info["Sell_Trigger_Price"]=round(sell_trigger_price,2)
        order_info["Time"]=data_dict_1_min["Time"]
        Immediate_Selling=True
        Price_sell.config(text="1 min Open")
    else:
        order_info["Sell_Price"]=sell_price
        order_info["Sell_Trigger_Price"]=round(sell_trigger_price,2)
        order_info["Time"]=data_dict_1_min["Time"]
        Immediate_Selling=True


def I_Close_1min_sell():
    global data_dict_1_min
    global data_dict_5_min
    global order_info
    global Immediate_Selling

    Quick_order_price_computation()

    sell_price=data_dict_1_min["close"]
    sell_trigger_price=data_dict_1_min["close"]+0.05

    if Modify_sell_var.get() ==12:
        order_info["Sell_Price"]=sell_price
        order_info["Sell_Trigger_Price"]=round(sell_trigger_price,2)
        order_info["Time"]=data_dict_1_min["Time"]
        Immediate_Selling=True
        Price_sell.config(text="1 min Close")
    else:
        order_info["Sell_Price"]=sell_price
        order_info["Sell_Trigger_Price"]=round(sell_trigger_price,2)
        order_info["Time"]=data_dict_1_min["Time"]
        Immediate_Selling=True

    Virtual_sell()


def I_High_5min_sell():
    global data_dict_1_min
    global data_dict_5_min
    global order_info
    global Immediate_Selling

    Quick_order_price_computation()
    sell_price=data_dict_5_min["high"]
    sell_trigger_price=data_dict_5_min["high"]+0.05

    if Modify_sell_var.get() ==12:
        order_info["Sell_Price"]=sell_price
        order_info["Sell_Trigger_Price"]=round(sell_trigger_price,2)
        order_info["Time"]=data_dict_5_min["Time"]
        Immediate_Selling=True
        Price_sell.config(text="5 min High")
    else:
        order_info["Sell_Price"]=sell_price
        order_info["Sell_Trigger_Price"]=round(sell_trigger_price,2)
        order_info["Time"]=data_dict_1_min["Time"]
        Immediate_Selling=True

    Virtual_sell()



def I_Low_5min_sell():
    global data_dict_1_min
    global data_dict_5_min
    global order_info
    global Immediate_Selling

    Quick_order_price_computation()

    sell_price=data_dict_5_min["low"]
    sell_trigger_price=data_dict_5_min["low"]+0.05

    if Modify_sell_var.get() ==12:
        order_info["Sell_Price"]=sell_price
        order_info["Sell_Trigger_Price"]=round(sell_trigger_price,2)
        order_info["Time"]=data_dict_5_min["Time"]
        Immediate_Selling=True
        Price_sell.config(text="5 min Low")
    else:
        order_info["Sell_Price"]=sell_price
        order_info["Sell_Trigger_Price"]=round(sell_trigger_price,2)
        order_info["Time"]=data_dict_5_min["Time"]
        Immediate_Selling=True

    Virtual_sell()



def I_Open_5min_sell():
    global data_dict_1_min
    global data_dict_5_min
    global order_info
    global Immediate_Selling

    Quick_order_price_computation()

    sell_price=data_dict_5_min["open"]
    sell_trigger_price=data_dict_5_min["open"]+0.05

    if Modify_sell_var.get() ==12:
        order_info["Sell_Price"]=sell_price
        order_info["Sell_Trigger_Price"]=round(sell_trigger_price,2)
        order_info["Time"]=data_dict_5_min["Time"]
        Immediate_Selling=True
        Price_sell.config(text="5 min Open")
    else:
        order_info["Sell_Price"]=sell_price
        order_info["Sell_Trigger_Price"]=round(sell_trigger_price,2)
        order_info["Time"]=data_dict_5_min["Time"]
        Immediate_Selling=True

    Virtual_sell()

def I_Close_5min_sell():
    global data_dict_1_min
    global data_dict_5_min
    global order_info
    global Immediate_Selling

    Quick_order_price_computation()

    sell_price=data_dict_5_min["close"]
    sell_trigger_price=data_dict_5_min["close"]+0.05

    if Modify_sell_var.get() ==12:
        order_info["Sell_Price"]=sell_price
        order_info["Sell_Trigger_Price"]=round(sell_trigger_price,2)
        order_info["Time"]=data_dict_5_min["Time"]
        Immediate_Selling=True
        Price_sell.config(text="5 min Close")
    else:
        order_info["Sell_Price"]=sell_price
        order_info["Sell_Trigger_Price"]=round(sell_trigger_price,2)
        order_info["Time"]=data_dict_5_min["Time"]
        Immediate_Selling=True

    Virtual_sell()


############# SELL #######################


############# Immediate Stop Loss #######################
def SL_low_1_min():
    global data_dict_1_min
    global data_dict_5_min
    global order_info
    global Interrupt_value
    global path

    if Trailing_SL_var.get()==30:
        file_name="SL_low_1_min.txt"
        with open(path+file_name, "w") as file:
            pass

        
        def loop():
            if  Interrupt_value:
                Quick_order_price_computation()
                if os.path.getsize(path+"SL_low_1_min.txt") == 0:
                    order_info["Stop_Loss"]=round(data_dict_1_min["low"],2)
                    order_info["SL_Trigger_Price"]=round(data_dict_1_min["low"]+0.05,2)
                    order_info["Time"]=data_dict_1_min["Time"]
                    
                    with open(path+file_name, "w") as file:
                        file.write(str(data_dict_1_min["low"]))
                    
                    print("Modify Order")
                    modify_order_SL()
                else:
                    with open(path+file_name, "r") as file:
                        content = file.read()
                        if content==str(data_dict_1_min["low"]):
                            print("Not Modify Order")
                            # listbox.insert(4,"SL Run Status: Not Modified")
                        else:
                            order_info["Stop_Loss"]=round(data_dict_1_min["low"],2)
                            order_info["SL_Trigger_Price"]=round(data_dict_1_min["low"]+0.05,2)
                            order_info["Time"]=data_dict_1_min["Time"]
                            
                            with open(path+file_name, "w") as file:
                                file.write(str(data_dict_1_min["low"]))
                            print("Modify Order")
                            # listbox.insert(3,f'SL Price: {order_info["Stop_Loss"]}')
                            # listbox.insert(4,"SL Run Status: Modified")
                            modify_order_SL()
                
                print("SL_low_1_min Running")
                GUI.after(1000,loop)

        Interrupt_value=True
        loop()
    else:
        message_label.config(text="Place Trailing SL order first")

    


def SL_close_1_min():
    global data_dict_1_min
    global data_dict_5_min
    global order_info
    global Interrupt_value
    global path

    if Trailing_SL_var.get()==30:
        file_name="SL_close_1_min.txt"
        with open(path+file_name, "w") as file:
            pass
        def loop():
            if  Interrupt_value:
                Quick_order_price_computation()
                if os.path.getsize(path+"SL_close_1_min.txt") == 0:
                    order_info["Stop_Loss"]=round(data_dict_1_min["close"],2)
                    order_info["SL_Trigger_Price"]=round(data_dict_1_min["close"]+0.05,2)
                    order_info["Time"]=data_dict_1_min["Time"]
                    
                    with open(path+file_name, "w") as file:
                        file.write(str(data_dict_1_min["close"]))
                    
                    # listbox.insert(3,f'SL Price: {order_info["Stop_Loss"]}')
                    # listbox.insert(4,"SL Run Status: Modified")
                    print("Modify Order")
                    modify_order_SL()
                else:
                    with open(path+file_name, "r") as file:
                        content = file.read()
                        if content==str(data_dict_1_min["close"]):
                            print("Not Modify Order")
                            # listbox.insert(4,"SL Run Status: Not Modified")
                        else:
                            order_info["Stop_Loss"]=round(data_dict_1_min["close"],2)
                            order_info["SL_Trigger_Price"]=round(data_dict_1_min["close"]+0.05,2)
                            order_info["Time"]=data_dict_1_min["Time"]
                            
                            with open(path+file_name, "w") as file:
                                file.write(str(data_dict_1_min["close"]))
                            print("Modify Order")
                            # listbox.insert(3,f'SL Price: {order_info["Stop_Loss"]}')
                            # listbox.insert(4,"SL Run Status: Modified")
                            modify_order_SL()
                
                print("SL_close_1_min Running")
                GUI.after(1000,loop)

        Interrupt_value=True
        loop()
    else:
        message_label.config(text="Place Trailing SL order first")


def SL_low_5_min():
    global data_dict_1_min
    global data_dict_5_min
    global order_info
    global Interrupt_value
    global path

    if Trailing_SL_var.get()==30:
        file_name="SL_low_5_min.txt"
        with open(path+file_name, "w") as file:
            pass
        # Quick_order_price_computation()
        # order_info["Stop_Loss"]=data_dict_1_min["low"]
        def loop():
            if  Interrupt_value:
                Quick_order_price_computation()
                if os.path.getsize(path+"SL_low_5_min.txt") == 0:
                    order_info["Stop_Loss"]=round(data_dict_5_min["low"],2)
                    order_info["SL_Trigger_Price"]=round(data_dict_5_min["low"]+0.05,2)
                    order_info["Time"]=data_dict_5_min["Time"]
                    
                    with open(path+file_name, "w") as file:
                        file.write(str(data_dict_5_min["low"]))

                    # listbox.insert(3,f'SL Price: {order_info["Stop_Loss"]}')
                    # listbox.insert(4,"SL Run Status: Modified")
                    print("Modify Order")
                    modify_order_SL()
                else:
                    with open(path+file_name, "r") as file:
                        content = file.read()
                        if content==str(data_dict_5_min["low"]):
                            print("Not Modify Order")
                            # listbox.insert(4,"SL Run Status: Not Modified")
                        else:
                            order_info["Stop_Loss"]=round(data_dict_5_min["low"],2)
                            order_info["SL_Trigger_Price"]=round(data_dict_5_min["low"]+0.05,2)
                            order_info["Time"]=data_dict_5_min["Time"]
                            
                            with open(path+file_name, "w") as file:
                                file.write(str(data_dict_5_min["low"]))

                            # listbox.insert(3,f'SL Price: {order_info["Stop_Loss"]}')
                            # listbox.insert(4,"SL Run Status: Modified")
                            print("Modify Order")
                            modify_order_SL()
                
                print("SL_low_5_min Running")
                GUI.after(1000,loop)

        Interrupt_value=True
        loop()
    else:
        message_label.config(text="Place Trailing SL order first") 


def SL_close_5_min():
    global data_dict_1_min
    global data_dict_5_min
    global order_info
    global Interrupt_value
    global path

    if Trailing_SL_var.get()==30:
        file_name="SL_close_5_min.txt"
        with open(path+file_name, "w") as file:
            pass

        def loop():
            if  Interrupt_value:
                Quick_order_price_computation()
                if os.path.getsize(path+"SL_close_5_min.txt") == 0:
                    order_info["Stop_Loss"]=round(data_dict_5_min["close"],2)
                    order_info["SL_Trigger_Price"]=round(data_dict_5_min["close"]+0.05,2)
                    order_info["Time"]=data_dict_5_min["Time"]
                    
                    with open(path+file_name, "w") as file:
                        file.write(str(data_dict_5_min["close"]))

                    # listbox.insert(3,f'SL Price: {order_info["Stop_Loss"]}')
                    # listbox.insert(4,"SL Run Status: Modified")
                    print("Modify Order")
                    modify_order_SL()
                else:
                    with open(path+file_name, "r") as file:
                        content = file.read()
                        if content==str(data_dict_5_min["close"]):
                            print("Not Modify Order")
                            # listbox.insert(4,"SL Run Status: Not Modified")
                        else:
                            order_info["Stop_Loss"]=round(data_dict_5_min["close"],2)
                            order_info["SL_Trigger_Price"]=round(data_dict_5_min["close"]+0.05,2)
                            order_info["Time"]=data_dict_5_min["Time"]
                            
                            with open(path+file_name, "w") as file:
                                file.write(str(data_dict_5_min["close"]))

                            # listbox.insert(3,f'SL Price: {order_info["Stop_Loss"]}')
                            # listbox.insert(4,"SL Run Status: Modified")
                            print("Modify Order")
                            modify_order_SL()
                
                print("SL_close_5_min Running")
                GUI.after(1000,loop)

        Interrupt_value=True
        loop()
    else:
        message_label.config(text="Place Trailing SL order first")


def Interrupt_butt():
    global Interrupt_value
    global order_info
    
    Interrupt_value=False
    print("Stop Loss Update Stop")
    sell_price=order_info["Stop_Loss"]
    l114.config(text=f"{sell_price}: Interrupted")

############# Immediate Stop Loss #######################

############# Moving Average Stop Loss #######################
def SL_9_EMA_1_min():
    global order_info
    global MA_1_min
    global MA_5_min
    global Interrupt_value
    global path

    if Trailing_SL_var.get()==30:
        file_name="SL_9_EMA_1_min.txt"
        with open(path+file_name, "w") as file:
            pass

        def loop():
            if  Interrupt_value:
                if os.path.getsize(path+"SL_9_EMA_1_min.txt") == 0:
                    order_info["Stop_Loss"]=math.floor(MA_1_min[0])
                    order_info["SL_Trigger_Price"]=math.floor(MA_1_min[0])+0.05
                    order_info["Time"]=data_dict_1_min["Time"]
                    
                    with open(path+file_name, "w") as file:
                        file.write(str(math.floor(MA_1_min[0])))

                    # listbox.insert(3,f'SL Price: {order_info["Stop_Loss"]}')
                    # listbox.insert(4,"SL Run Status: Modified")
                    print("Modify Order")
                    modify_order_SL()
                else:
                    with open(path+file_name, "r") as file:
                        content = file.read()
                        if content==str(math.floor(MA_1_min[0])):
                            print("Not Modify Order")
                            # listbox.insert(4,"SL Run Status: Not Modified")
                        else:
                            order_info["Stop_Loss"]=math.floor(MA_1_min[0])
                            order_info["SL_Trigger_Price"]=math.floor(MA_1_min[0])+0.05
                            order_info["Time"]=data_dict_1_min["Time"]
                            
                            with open(path+file_name, "w") as file:
                                file.write(str(math.floor(MA_1_min[0])))
                            print("Modify Order")
                            # listbox.insert(3,f'SL Price: {order_info["Stop_Loss"]}')
                            # listbox.insert(4,"SL Run Status: Modified")
                            modify_order_SL()
                
                print("SL_9_EMA_1_min Running")
                GUI.after(1000,loop)

        Interrupt_value=True
        loop()
    else:
        message_label.config(text="Place Trailing SL order first")


def SL_21_EMA_1_min():
    global order_info
    global MA_1_min
    global MA_5_min
    global Interrupt_value
    global path

    if Trailing_SL_var.get()==30:
        file_name="SL_21_EMA_1_min.txt"
        with open(path+file_name, "w") as file:
            pass
        
        def loop():
            if  Interrupt_value:
                if os.path.getsize(path+"SL_21_EMA_1_min.txt") == 0:
                    order_info["Stop_Loss"]=math.floor(MA_1_min[1])
                    order_info["SL_Trigger_Price"]=math.floor(MA_1_min[1])+0.05
                    order_info["Time"]=data_dict_1_min["Time"]
                    
                    with open(path+file_name, "w") as file:
                        file.write(str(math.floor(MA_1_min[1])))
                    print("Modify Order")
                    # listbox.insert(3,f'SL Price: {order_info["Stop_Loss"]}')
                    # listbox.insert(4,"SL Run Status: Modified")
                    modify_order_SL()
                else:
                    with open(path+file_name, "r") as file:
                        content = file.read()
                        if content==str(math.floor(MA_1_min[1])):
                            print("Not Modify Order")
                            # listbox.insert(4,"SL Run Status: Not Modified")
                        else:
                            order_info["Stop_Loss"]=math.floor(MA_1_min[1])
                            order_info["SL_Trigger_Price"]=math.floor(MA_1_min[1])+0.05
                            order_info["Time"]=data_dict_1_min["Time"]
                            
                            with open(path+file_name, "w") as file:
                                file.write(str(math.floor(MA_1_min[1])))

                            # listbox.insert(3,f'SL Price: {order_info["Stop_Loss"]}')
                            # listbox.insert(4,"SL Run Status: Modified")
                            print("Modify Order")
                            modify_order_SL()
                
                print("SL_21_EMA_1_min Running")
                GUI.after(1000,loop)

        Interrupt_value=True
        loop()
    else:
        message_label.config(text="Place Trailing SL order first")

def SL_50_EMA_1_min():
    global order_info
    global MA_1_min
    global MA_5_min
    global Interrupt_value
    global path

    if Trailing_SL_var.get()==30:
        file_name="SL_50_EMA_1_min.txt"
        with open(path+file_name, "w") as file:
            pass
        
        def loop():
            if  Interrupt_value:
                if os.path.getsize(path+"SL_50_EMA_1_min.txt") == 0:
                    order_info["Stop_Loss"]=math.floor(MA_1_min[2])
                    order_info["SL_Trigger_Price"]=math.floor(MA_1_min[2])+0.05
                    order_info["Time"]=data_dict_1_min["Time"]
                    
                    with open(path+file_name, "w") as file:
                        file.write(str(math.floor(MA_1_min[2])))
                    print("Modify Order")
                    # listbox.insert(3,f'SL Price: {order_info["Stop_Loss"]}')
                    # listbox.insert(4,"SL Run Status: Modified")
                    modify_order_SL()
                else:
                    with open(path+file_name, "r") as file:
                        content = file.read()
                        if content==str(math.floor(MA_1_min[2])):
                            print("Not Modify Order")
                            # listbox.insert(4,"SL Run Status: Not Modified")
                        else:
                            order_info["Stop_Loss"]=math.floor(MA_1_min[2])
                            order_info["SL_Trigger_Price"]=math.floor(MA_1_min[2])+0.05
                            order_info["Time"]=data_dict_1_min["Time"]
                            
                            with open(path+file_name, "w") as file:
                                file.write(str(math.floor(MA_1_min[2])))
                            print("Modify Order")

                            # listbox.insert(3,f'SL Price: {order_info["Stop_Loss"]}')
                            # listbox.insert(4,"SL Run Status: Modified")
                            modify_order_SL()
                
                print("SL_50_EMA_1_min Running")
                GUI.after(1000,loop)

        Interrupt_value=True
        loop()
    else:
        message_label.config(text="Place Trailing SL order first")

def SL_200_EMA_1_min():
    global order_info
    global MA_1_min
    global MA_5_min
    global Interrupt_value
    global path

    if Trailing_SL_var.get()==30:
        file_name="SL_200_EMA_1_min.txt"
        with open(path+file_name, "w") as file:
            pass
        
        def loop():
            if  Interrupt_value:
                if os.path.getsize(path+"SL_200_EMA_1_min.txt") == 0:
                    order_info["Stop_Loss"]=math.floor(MA_1_min[3])
                    order_info["SL_Trigger_Price"]=math.floor(MA_1_min[3])+0.05
                    order_info["Time"]=data_dict_1_min["Time"]
                    
                    with open(path+file_name, "w") as file:
                        file.write(str(math.floor(MA_1_min[3])))
                    print("Modify Order")
                    # listbox.insert(3,f'SL Price: {order_info["Stop_Loss"]}')
                    # listbox.insert(4,"SL Run Status: Modified")
                    modify_order_SL()
                else:
                    with open(path+file_name, "r") as file:
                        content = file.read()
                        if content==str(math.floor(MA_1_min[3])):
                            print("Not Modify Order")
                            # listbox.insert(4,"SL Run Status: Not Modified")
                        else:
                            order_info["Stop_Loss"]=math.floor(MA_1_min[3])
                            order_info["SL_Trigger_Price"]=math.floor(MA_1_min[3])+0.05
                            order_info["Time"]=data_dict_1_min["Time"]
                            
                            with open(path+file_name, "w") as file:
                                file.write(str(math.floor(MA_1_min[3])))
                            
                            # listbox.insert(3,f'SL Price: {order_info["Stop_Loss"]}')
                            # listbox.insert(4,"SL Run Status: Modified")
                            print("Modify Order")
                            modify_order_SL()
                
                print("SL_200_EMA_1_min Running")
                GUI.after(1000,loop)

        Interrupt_value=True
        loop()
    else:
        message_label.config(text="Place Trailing SL order first")

def SL_9_EMA_5_min():
    global order_info
    global MA_1_min
    global MA_5_min
    global Interrupt_value
    global path

    if Trailing_SL_var.get()==30:
        file_name="SL_9_EMA_5_min.txt"
        with open(path+file_name, "w") as file:
            pass
        
        def loop():
            if  Interrupt_value:
                if os.path.getsize(path+"SL_9_EMA_5_min.txt") == 0:
                    order_info["Stop_Loss"]=math.floor(MA_5_min[0])
                    order_info["SL_Trigger_Price"]=math.floor(MA_5_min[0])+0.05
                    order_info["Time"]=data_dict_1_min["Time"]
                    
                    with open(path+file_name, "w") as file:
                        file.write(str(math.floor(MA_5_min[0])))
                    print("Modify Order")
                    # listbox.insert(3,f'SL Price: {order_info["Stop_Loss"]}')
                    # listbox.insert(4,"SL Run Status: Modified")
                    modify_order_SL()
                else:
                    with open(path+file_name, "r") as file:
                        content = file.read()
                        if content==str(math.floor(MA_5_min[0])):
                            print("Not Modify Order")
                            # listbox.insert(4,"SL Run Status: Not Modified")
                        else:
                            order_info["Stop_Loss"]=math.floor(MA_5_min[0])
                            order_info["SL_Trigger_Price"]=math.floor(MA_5_min[0])+0.05
                            order_info["Time"]=data_dict_1_min["Time"]
                            
                            with open(path+file_name, "w") as file:
                                file.write(str(math.floor(MA_5_min[0])))
                            print("Modify Order")
                            # listbox.insert(3,f'SL Price: {order_info["Stop_Loss"]}')
                            # listbox.insert(4,"SL Run Status: Modified")
                            modify_order_SL()
                
                print("SL_9_EMA_5_min Running")
                GUI.after(1000,loop)

        Interrupt_value=True
        loop()
    else:
        message_label.config(text="Place Trailing SL order first")


def SL_21_EMA_5_min():
    global order_info
    global MA_1_min
    global MA_5_min
    global Interrupt_value
    global path

    if Trailing_SL_var.get()==30:
        file_name="SL_21_EMA_5_min.txt"
        with open(path+file_name, "w") as file:
            pass
        
        def loop():
            if  Interrupt_value:
                if os.path.getsize(path+"SL_21_EMA_5_min.txt") == 0:
                    order_info["Stop_Loss"]=math.floor(MA_5_min[1])
                    order_info["SL_Trigger_Price"]=math.floor(MA_5_min[1])+0.05
                    order_info["Time"]=data_dict_1_min["Time"]
                    
                    with open(path+file_name, "w") as file:
                        file.write(str(math.floor(MA_5_min[1])))
                    print("Modify Order")
                    # listbox.insert(3,f'SL Price: {order_info["Stop_Loss"]}')
                    # listbox.insert(4,"SL Run Status: Modified")
                    modify_order_SL()
                else:
                    with open(path+file_name, "r") as file:
                        content = file.read()
                        if content==str(math.floor(MA_5_min[1])):
                            print("Not Modify Order")
                            # listbox.insert(4,"SL Run Status: Not Modified")
                        else:
                            order_info["Stop_Loss"]=math.floor(MA_5_min[1])
                            order_info["SL_Trigger_Price"]=math.floor(MA_5_min[1])+0.05
                            order_info["Time"]=data_dict_1_min["Time"]
                            
                            with open(path+file_name, "w") as file:
                                file.write(str(math.floor(MA_5_min[1])))
                            print("Modify Order")
                            # listbox.insert(3,f'SL Price: {order_info["Stop_Loss"]}')
                            # listbox.insert(4,"SL Run Status: Modified")
                            modify_order_SL()
                
                print("SL_21_EMA_5_min Running")
                GUI.after(1000,loop)

        Interrupt_value=True
        loop()
    else:
        message_label.config(text="Place Trailing SL order first")



def SL_50_EMA_5_min():
    global order_info
    global MA_1_min
    global MA_5_min
    global Interrupt_value
    global path

    if Trailing_SL_var.get()==30:
        file_name="SL_50_EMA_5_min.txt"
        with open(path+file_name, "w") as file:
            pass
        
        def loop():
            if  Interrupt_value:
                if os.path.getsize(path+"SL_50_EMA_5_min.txt") == 0:
                    order_info["Stop_Loss"]=math.floor(MA_5_min[2])
                    order_info["SL_Trigger_Price"]=math.floor(MA_5_min[2])+0.05
                    order_info["Time"]=data_dict_1_min["Time"]
                    
                    with open(path+file_name, "w") as file:
                        file.write(str(math.floor(MA_5_min[2])))
                    print("Modify Order")
                    # listbox.insert(3,f'SL Price: {order_info["Stop_Loss"]}')
                    # listbox.insert(4,"SL Run Status: Modified")
                    modify_order_SL()
                else:
                    with open(path+file_name, "r") as file:
                        content = file.read()
                        if content==str(math.floor(MA_5_min[2])):
                            print("Not Modify Order")
                            # listbox.insert(4,"SL Run Status: Not Modified")
                        else:
                            order_info["Stop_Loss"]=math.floor(MA_5_min[2])
                            order_info["SL_Trigger_Price"]=math.floor(MA_5_min[2])+0.05
                            order_info["Time"]=data_dict_1_min["Time"]
                            
                            with open(path+file_name, "w") as file:
                                file.write(str(math.floor(MA_5_min[2])))
                            # listbox.insert(3,f'SL Price: {order_info["Stop_Loss"]}')
                            # listbox.insert(4,"SL Run Status: Modified")
                            print("Modify Order")
                            modify_order_SL()
                
                print("SL_50_EMA_5_min Running")
                GUI.after(1000,loop)

        Interrupt_value=True
        loop()
    else:
        message_label.config(text="Place Trailing SL order first")



def SL_200_EMA_5_min():
    global order_info
    global MA_1_min
    global MA_5_min
    global Interrupt_value
    global path

    if Trailing_SL_var.get()==30:
        file_name="SL_200_EMA_5_min.txt"
        with open(path+file_name, "w") as file:
            pass
        
        def loop():
            if  Interrupt_value:
                if os.path.getsize(path+"SL_200_EMA_5_min.txt") == 0:
                    order_info["Stop_Loss"]=math.floor(MA_5_min[3])
                    order_info["SL_Trigger_Price"]=math.floor(MA_5_min[3])+0.05
                    order_info["Time"]=data_dict_1_min["Time"]
                    
                    with open(path+file_name, "w") as file:
                        file.write(str(math.floor(MA_5_min[3])))

                    # listbox.insert(3,f'SL Price: {order_info["Stop_Loss"]}')
                    # listbox.insert(4,"SL Run Status: Modified")
                    print("Modify Order")
                    # with open(path+"Buy_Sell_Log_File.txt",'a') as file:
                    #     file.write(f"SL_200_EMA_5_min: {str(order_info)}\n")
                else:
                    with open(path+file_name, "r") as file:
                        content = file.read()
                        if content==str(math.floor(MA_5_min[3])):
                            print("Not Modify Order")
                        else:
                            order_info["Stop_Loss"]=math.floor(MA_5_min[3])
                            order_info["SL_Trigger_Price"]=math.floor(MA_5_min[3])+0.05
                            order_info["Time"]=data_dict_1_min["Time"]
                            
                            with open(path+file_name, "w") as file:
                                file.write(str(math.floor(MA_5_min[3])))
                            
                            # listbox.insert(3,f'SL Price: {order_info["Stop_Loss"]}')
                            # listbox.insert(4,"SL Run Status: Modified")
                            print("Modify Order")
                            # with open(path+"Buy_Sell_Log_File.txt",'a') as file:
                            #     file.write(f"SL_200_EMA_5_min: {str(order_info)}\n")
                
                print("SL_200_EMA_5_min Running")
                GUI.after(1000,loop)

        Interrupt_value=True
        loop()
    else:
        message_label.config(text="Place Trailing SL order first")



############# Moving Average Stop Loss #######################

################### Moving Average Buy ###################################

def MA_9EMA_1min_buy():
    global order_info
    global MA_1_min
    global MA_5_min
    global Moving_Average_Buying

    buy_price=round(MA_1_min[0],1)-0.05
    trigger_price=round(MA_1_min[0],1)-0.1
    time=MA_1_min[4]

    order_info["Buy_Price"]=round(buy_price,2)
    order_info["Trigger_Price"]=round(trigger_price,2)
    order_info["Time"]=time
    Moving_Average_Buying=True


def MA_21EMA_1min_buy():
    global order_info
    global MA_1_min
    global MA_5_min
    global Moving_Average_Buying

    buy_price=round(MA_1_min[1],1)-0.05
    trigger_price=round(MA_1_min[1],1)-0.1
    time=MA_1_min[4]

    order_info["Buy_Price"]=round(buy_price,2)
    order_info["Trigger_Price"]=round(trigger_price,2)
    order_info["Time"]=time
    Moving_Average_Buying=True


def MA_50EMA_1min_buy():
    global order_info
    global MA_1_min
    global MA_5_min
    global Moving_Average_Buying

    buy_price=round(MA_1_min[2],1)-0.05
    trigger_price=round(MA_1_min[2],1)-0.1
    time=MA_1_min[4]

    order_info["Buy_Price"]=round(buy_price,2)
    order_info["Trigger_Price"]=round(trigger_price,2)
    order_info["Time"]=time
    Moving_Average_Buying=True

def MA_200EMA_1min_buy():
    global order_info
    global MA_1_min
    global MA_5_min
    global Moving_Average_Buying

    buy_price=round(MA_1_min[3],1)-0.05
    trigger_price=round(MA_1_min[3],1)-0.1
    time=MA_1_min[4]

    order_info["Buy_Price"]=round(buy_price,2)
    order_info["Trigger_Price"]=round(trigger_price,2)
    order_info["Time"]=time
    Moving_Average_Buying=True


def MA_9EMA_5min_buy():
    global order_info
    global MA_1_min
    global MA_5_min
    global Moving_Average_Buying

    buy_price=round(MA_5_min[0],1)-0.05
    trigger_price=round(MA_5_min[0],1)-0.1
    time=MA_5_min[4]

    order_info["Buy_Price"]=round(buy_price,2)
    order_info["Trigger_Price"]=round(trigger_price,2)
    order_info["Time"]=time
    Moving_Average_Buying=True

def MA_21EMA_5min_buy():
    global order_info
    global MA_1_min
    global MA_5_min
    global Moving_Average_Buying

    buy_price=round(MA_5_min[1],1)-0.05
    trigger_price=round(MA_5_min[1],1)-0.1
    time=MA_5_min[4]

    order_info["Buy_Price"]=round(buy_price,2)
    order_info["Trigger_Price"]=round(trigger_price,2)
    order_info["Time"]=time
    Moving_Average_Buying=True


def MA_50EMA_5min_buy():
    global order_info
    global MA_1_min
    global MA_5_min
    global Moving_Average_Buying

    buy_price=round(MA_5_min[2],1)-0.05
    trigger_price=round(MA_5_min[2],1)-0.1
    time=MA_5_min[4]

    order_info["Buy_Price"]=round(buy_price,2)
    order_info["Trigger_Price"]=round(trigger_price,2)
    order_info["Time"]=time
    Moving_Average_Buying=True



def MA_200EMA_5min_buy():
    global order_info
    global MA_1_min
    global MA_5_min
    global Moving_Average_Buying

    buy_price=round(MA_5_min[3],1)-0.05
    trigger_price=round(MA_5_min[3],1)-0.1
    time=MA_5_min[4]

    order_info["Buy_Price"]=round(buy_price,2)
    order_info["Trigger_Price"]=round(trigger_price,2)
    order_info["Time"]=time
    Moving_Average_Buying=True

################### Moving Average Buy ###################################

################### Moving Average Sell ###################################
def MA_9EMA_1min_sell():
    global order_info
    global MA_1_min
    global MA_5_min
    global Moving_Average_Selling

    sell_price=round(MA_1_min[0],1)+0.05
    trigger_price=round(MA_1_min[0],1)+0.1
    time=MA_1_min[4]

    order_info["Sell_Price"]=round(sell_price,2)
    order_info["Sell_Trigger_Price"]=round(trigger_price,2)
    order_info["Time"]=time
    Moving_Average_Selling=True


def MA_21EMA_1min_sell():
    global order_info
    global MA_1_min
    global MA_5_min
    global Moving_Average_Selling

    sell_price=round(MA_1_min[1],1)-0.05
    trigger_price=round(MA_1_min[1],1)-0.1
    time=MA_1_min[4]

    order_info["Sell_Price"]=round(sell_price,2)
    order_info["Sell_Trigger_Price"]=round(trigger_price,2)
    order_info["Time"]=time
    Moving_Average_Selling=True


def MA_50EMA_1min_sell():
    global order_info
    global MA_1_min
    global MA_5_min
    global Moving_Average_Selling

    sell_price=round(MA_1_min[2],1)+0.05
    trigger_price=round(MA_1_min[2],1)+0.1
    time=MA_1_min[4]

    order_info["Sell_Price"]=round(sell_price,2)
    order_info["Sell_Trigger_Price"]=round(trigger_price,2)
    order_info["Time"]=time
    Moving_Average_Selling=True

def MA_200EMA_1min_sell():
    global order_info
    global MA_1_min
    global MA_5_min
    global Moving_Average_Selling

    sell_price=round(MA_1_min[3],1)+0.05
    trigger_price=round(MA_1_min[3],1)+0.1
    time=MA_1_min[4]

    order_info["Sell_Price"]=round(sell_price,2)
    order_info["Sell_Trigger_Price"]=round(trigger_price,2)
    order_info["Time"]=time
    Moving_Average_Selling=True


def MA_9EMA_5min_sell():
    global order_info
    global MA_1_min
    global MA_5_min
    global Moving_Average_Selling

    sell_price=round(MA_5_min[0],1)+0.05
    trigger_price=round(MA_5_min[0],1)+0.1
    time=MA_5_min[4]

    order_info["Sell_Price"]=round(sell_price,2)
    order_info["Sell_Trigger_Price"]=round(trigger_price,2)
    order_info["Time"]=time
    Moving_Average_Selling=True

def MA_21EMA_5min_sell():
    global order_info
    global MA_1_min
    global MA_5_min
    global Moving_Average_Selling

    sell_price=round(MA_5_min[1],1)+0.05
    trigger_price=round(MA_5_min[1],1)+0.1
    time=MA_5_min[4]

    order_info["Sell_Price"]=round(sell_price,2)
    order_info["Sell_Trigger_Price"]=round(trigger_price,2)
    order_info["Time"]=time
    Moving_Average_Selling=True


def MA_50EMA_5min_sell():
    global order_info
    global MA_1_min
    global MA_5_min
    global Moving_Average_Selling

    sell_price=round(MA_5_min[2],1)+0.05
    trigger_price=round(MA_5_min[2],1)+0.1
    time=MA_5_min[4]

    order_info["Sell_Price"]=round(sell_price,2)
    order_info["Sell_Trigger_Price"]=round(trigger_price,2)
    order_info["Time"]=time
    Moving_Average_Selling=True



def MA_200EMA_5min_sell():
    global order_info
    global MA_1_min
    global MA_5_min
    global Moving_Average_Selling

    sell_price=round(MA_5_min[3],1)+0.05
    trigger_price=round(MA_5_min[3],1)+0.1
    time=MA_5_min[4]

    order_info["Sell_Price"]=round(sell_price,2)
    order_info["Sell_Trigger_Price"]=round(trigger_price,2)
    order_info["Time"]=time
    Moving_Average_Selling=True


################### Moving Average Sell ###################################

############################################ Menue bar Functions (Immediate Orders)  #########################################
def Refresh_all():
    global data_dict_1_min
    global data_dict_5_min
    global order_info
    global Buy_status
    global token
    global trading_var
    global Order_type_var
    global virtua_selling_start

    order_info={}
    token=[]
    data_dict_1_min={}
    data_dict_5_min={}
    Buy_status=0
    trading_var.set(0)
    Order_type_var.set(0)
    Modify_buy_var.set(0)
    Modify_sell_var.set(0)
    Trailing_SL_var.set(0)
    MA_loop_var.set(0)
    cancel_var_order.set(0)
    virtual_buy_loop.set(0)
    Modify_loop_Buy_sell.set(0)
    SL2_percent.set(0)
    # Stop_loss_enable_var.set(0)
    lot_entry.delete(0,END)
    lot_entry_Sell.delete(0,END)

    l112.config(text="None: None")
    l114.config(text="None: None")
    l116.config(text="None: None")
    l118.config(text="None")

    Price_buy.config(text="price")
    Price_sell.config(text="price")
    virtua_selling_start=0

    # call_button.config(command=Call_side_Order)
    # put_button.config(command=Put_side_Order)


def Modify_Buy_enable():
    global order_info

    Buy_price_Entry.config(state=NORMAL)




def Modify_Sell_enable():
    global order_info

    Sell_price_Entry.config(state=NORMAL)


def Enable_Stoploss():

    global enctoken
    global order_info
    global virtua_selling_start

    kite = KiteApp(enctoken=enctoken)

    if order_info["Buy Status"]==1:

        with open(path_virtual+"Buy_Price.txt",'r') as file:
            content=file.read()

        price=ast.literal_eval(content)
        Buy_price=float(price["Buy_Price"])

        actual_buy_price=Buy_price

        starting_SL=(actual_buy_price*0.98)

        SL_P=math.floor(starting_SL)
        T_SL_P=math.floor(starting_SL)+0.05
        order_info["Stop_Loss"]=SL_P
        order_info["SL_Trigger_Price"]=T_SL_P
        virtua_selling_start=1
        l114.config(text=str(SL_P)+": Pending")
        Stop_loss_sell_limit()
    else:
        message_label.config(text="Place Buy Order First")


def Modify_buy_limit_order():
    global order_info   

    if Buy_price_Entry.get()=="":
        #pass
        print(order_info)
    else:
        price_new_buy=float(Buy_price_Entry.get())
        order_info["Buy_Price"]=price_new_buy
        print(order_info)

    modify_order_buy_Limit()

def Modify_sell_limit_order():
    global order_info

    if Sell_price_Entry.get()=="":
        print(order_info)
    else:
        price_new=float(Sell_price_Entry.get())
        order_info["Sell_Price"]=price_new
        print(order_info)

    modify_order_sell_Limit()

def Recall_order_info():
    global order_info 
    global Buy_status

    with open(path_kite_main+"Order_Log_File.txt","r") as file:
        content=file.read()

    log_file = ast.literal_eval(content)
    Length=len(log_file)
    order_info=log_file[Length-1]
    trading_var.set(order_info["Trading Var"])
    Order_type_var.set(order_info["Order Type Var"])
    Trailing_SL_var.set(order_info["Trailing_Sl"])
    Buy_status=order_info["Buy Status"]


def Trailing_SL():
    global order_info

    order_info["Trailing_Sl"]=Trailing_SL_var.get()

    if trading_var.get()==3:
        pass
    elif trading_var.get()==4:
        Trailing_SL_Size.config(state=NORMAL)
    else:
        pass

def Placement_of_Sell_Size():
    global order_info

    if Trailing_SL_var.get()==30:
        if trading_var.get()==3:
            order_info["Stop_loss_Size_sell"]=50
            modify_order_SL()
        elif trading_var.get()==4:
            size=int(Trailing_SL_Size.get())
            net_size=50*size
            order_info["Stop_loss_Size_sell"]=net_size
            modify_order_SL()
        else:
            pass
    else:
        pass

def Market_sell():
    global order_info
    global enctoken

    kite = KiteApp(enctoken=enctoken)

    InstrumentID=order_info["Trading_symbol"]
    x=kite.ltp(["NFO:"+InstrumentID])
    Sell_price=float(x['NFO:'+InstrumentID]['last_price'])

    df=pd.read_csv(path_virtual+"trade_Virtual_excel.csv")
    rows=df.shape[0]
    df.iloc[rows,3]=Sell_price
    l114.config(text=str(Sell_price)+": Executed")

path="D:/ashu/Finance/algo_trading/Zerodha_GUI/GUI_raw_data_Collected/"

if os.path.exists(path+"Nifty_option_chain.csv"):
    os.remove(path+"Nifty_option_chain.csv")
else:
    pass




############################## Virtual Continious Loop ########################################################
def Buy_loop():
    global enctoken
    kite = KiteApp(enctoken=enctoken)
    global order_info
    global Buy_status
    global path_kite_main
    global path_virtual
    import datetime
    global cancel
    import time

    with open(path_kite_main+"Order_Log_File.txt","r") as file:
        content=file.read()

    log_file = ast.literal_eval(content)

    log_file.append(order_info)

    with open(path_kite_main+"Order_Log_File.txt","w") as file:
        file.write(str(log_file))

    key_list=list(order_info.keys())

    xox=0

    if Immediate_Buying:
        if 'Trading_symbol' in key_list:
            xox=xox + 1
        else:
            message_label.config(text="Please Enter the Type of trade")

        if 'Size_Buy' in key_list:
            xox=xox + 1
        else:
            message_label.config(text="Please Enter the Buy Size")

        if 'Buy_Price' in key_list:
            xox=xox + 1
        else:
            message_label.config(text="Please Enter the Buy Price")

        if order_info["Buy_Price"]==0:
            message_label.config(text="Please Enter the Buy Price")
        else:
            xox=xox + 1

        if order_info["Size_Buy"]==0:
            message_label.config(text="Please Enter the Buy Size")
        else:
            xox=xox + 1

        if xox ==5:
            message_label.config(text="Good to go!")
            order_info["Buy Status"]=1
            print("It's Running")
            order_info["Trading Var"]=trading_var.get()
            order_info["Order Type Var"]=Order_type_var.get()
            order_info["Order Placed Type"]="Buy Limit"

            InstrumentID=order_info["Trading_symbol"]
            Buy_price=order_info["Buy_Price"]
            trigger_price=order_info["Trigger_Price"]


            l112.config(text=str(Buy_price)+": Pending")
            x=kite.ltp(["NFO:"+InstrumentID])
            price=float(x['NFO:'+InstrumentID]['last_price'])

            print(f'buy Price {Buy_price}')
            print(f'current Price {price}')
            print(order_info)


            if cancel_var_order.get()==110:
                return
            elif (price==Buy_price or price==trigger_price):
                print("Order Executed")
                current_datetime = datetime.datetime.now()
                formatted_time = current_datetime.strftime("%H:%M:%S")
                formatted_date = current_datetime.strftime("%d %B %Y")
                df=pd.read_csv(path_virtual+"trade_Virtual_excel.csv")
                rows=df.shape[0]
                df.loc[rows,"Date"]=formatted_date
                df.loc[rows,"Time"]=formatted_time
                df.loc[rows,"Buy Price"]=Buy_price
                df.loc[rows,"Sell Price"]=0
                l112.config(text=str(Buy_price)+": Executed")
                df.to_csv(path_virtual+"trade_Virtual_excel.csv",index=False)
                return
            else:
                pass

            

            print(f"Buy Limit Order: {order_info}")

            # order_update_func()
        GUI.after(10,Buy_loop)

    else:
         message_label.config(text="Please place Buy price from the Moving Average Buy section")



def Sell_loop():
    global order_info
    global Immediate_Selling
    global path
    global enctoken
    kite = KiteApp(enctoken=enctoken)

    if Immediate_Selling:
        if order_info["Buy Status"]==1:    
            sos=0
            
            key_list=list(order_info.keys())

            if 'Trading_symbol' in key_list:
                sos=sos + 1
            else:
                message_label.config(text="Please Enter the Type of trade")

            if 'Size_Sell' in key_list:
                sos=sos + 1
            else:
                message_label.config(text="Please Enter the Sell Size")

            if 'Sell_Price' in key_list:
                sos=sos + 1
            else:
                message_label.config(text="Please Enter the Sell Price")

            if order_info["Sell_Price"]==0:
                message_label.config(text="Please Enter the Sell Price")
            else:
                sos=sos + 1

            if order_info["Size_Sell"]==0:
                message_label.config(text="Please Enter the Sell Size")
            else:
                sos=sos + 1

            if sos ==5:
                message_label.config(text="Good to go!")
                print(order_info)
                InstrumentID=order_info["Trading_symbol"]
                data=pd.read_csv(path_virtual+"trade_Virtual_excel.csv")
                rows=data.shape[0]
                buy_price=data.iloc[rows-1,2]


                
            if (order_info["Buy Status"]==1 and buy_price!=0):
                x=kite.ltp(["NFO:"+InstrumentID])
                price=float(x['NFO:'+InstrumentID]['last_price'])

                Sell_price=order_info["Sell_Price"]
                l116.config(text=str(Sell_price)+": Pending")
                trigger_price=order_info["Sell_Trigger_Price"]

                if cancel_var_order.get()==110:
                    return
                elif (price==Sell_price or price==trigger_price):
                    df=pd.read_csv(path_virtual+"trade_Virtual_excel.csv")
                    rows=df.shape[0]
                    df.loc[rows-1,"Sell Price"]=Sell_price
                    l116.config(text=f"{Sell_price}: Executed")
                    df.to_csv(path_virtual+"trade_Virtual_excel.csv",index=False)
                    return
                else:
                    pass

            GUI.after(10,Sell_loop)

        else:
            message_label.config(text="Please Before selling Buy first")
    else:
        message_label.config(text="Please Place Sell Order in the Immediate section")




def SL_2_Percent_loop():
    global enctoken
    global order_info
    global path_virtual

    kite = KiteApp(enctoken=enctoken)
    InstrumentID=order_info["Trading_symbol"]
    data=pd.read_csv(path_virtual+"trade_Virtual_excel.csv")
    rows=data.shape[0]
    buy_price=data.iloc[rows-1,2]
    print("Running")

    if (order_info["Buy Status"]==1 and buy_price!=0):
        x=kite.ltp(["NFO:"+InstrumentID])
        price=float(x['NFO:'+InstrumentID]['last_price'])

        sell_price=order_info["Stop_Loss"]
        trigger_price=order_info["SL_Trigger_Price"]

        if cancel_var_order.get()==110:
            return
        elif (price==sell_price or price==trigger_price):
            df=pd.read_csv(path_virtual+"trade_Virtual_excel.csv")
            rows=df.shape[0]
            df.loc[rows-1,"Sell Price"]=sell_price
            l114.config(text=f"{sell_price}: Executed")
            df.to_csv(path_virtual+"trade_Virtual_excel.csv",index=False)
            return
        else:
            pass

    GUI.after(10,SL_2_Percent_loop)



def V_Buy_Modify_Loop():
    global enctoken
    global order_info
    global path_virtual

    kite = KiteApp(enctoken=enctoken)
    InstrumentID=order_info["Trading_symbol"]
    data=pd.read_csv(path_virtual+"trade_Virtual_excel.csv")
    rows=data.shape[0]
    buy_price=data.iloc[rows-1,2]
    print("Running")

    if (order_info["Buy Status"]==1 and buy_price!=0):
        x=kite.ltp(["NFO:"+InstrumentID])
        price=float(x['NFO:'+InstrumentID]['last_price'])
        

        Modify_price=order_info["Buy_Price"]
        trigger_price=order_info["Trigger_Price"]  
        l112.config(text=f"{Modify_price}: Pending")

        if cancel_var_order.get()==110:
            return
        elif (price==Modify_price or price==trigger_price):
            df=pd.read_csv(path_virtual+"trade_Virtual_excel.csv")
            rows=df.shape[0]
            df.loc[rows-1,"Buy Price"]=Modify_price
            l112.config(text=f"{Modify_price}: Executed")
            df.to_csv(path_virtual+"trade_Virtual_excel.csv",index=False)
            return
        else:
            pass

    GUI.after(10,V_Buy_Modify_Loop)        

def V_Sell_Modify_Loop():
    global enctoken
    global order_info
    global path_virtual

    kite = KiteApp(enctoken=enctoken)

############################## Virtual Continious Loop ########################################################


#######################################################################################################################################################
#######################################################################################################################################################
#######################################################################################################################################################
#######################################################################################################################################################
###############                                                   GUI                                                                 #################
#######################################################################################################################################################
#######################################################################################################################################################
#######################################################################################################################################################
#######################################################################################################################################################

GUI=Tk()

width=800
height=544
GUI.geometry(f'{str(width)}x{str(height)}')
GUI.maxsize(800, 600)

GUI.title("Virtual Archu GUI")


################################## Initial Declaration ###########################
previous_value = None
order_info={}
token=[]
data_dict_1_min={}
data_dict_5_min={}
Interrupt_value=True
MA_1_min=[]
MA_5_min=[]
Immediate_Buying=False
Immediate_Selling=False
Moving_Average_Buying=False
Moving_Average_Selling=False
cancel=0
virtua_selling_start=0

path_kite_main="D:/ashu/Finance/algo_trading/Zerodha_GUI/Kite_Zerodha-main/Kite_Zerodha-main/"
path_virtual="D:/ashu/Finance/algo_trading/Zerodha_GUI/Kite_Zerodha-main/Kite_Zerodha-main/Virtual_files/"

with open(path_kite_main+"Buy_Size.txt",'r') as file:
    read_content=file.read()

read_content=int(read_content)

if read_content<=0:
    Buy_status=0
else:
    Buy_status=1


columns = ["Date", "Time", "Buy Price", "Sell Price"]
df = pd.DataFrame(columns=columns)

df.to_csv(path_virtual+"trade_Virtual_excel.csv", index=False)



BUY_SELL_Frame=Frame(GUI,bg="grey",borderwidth=6,relief=SUNKEN)
BUY_SELL_Frame.grid(row=0, column=0, padx=10, pady=20)

################################## Initial Declaration ###########################

loop_flag = [False, False, False]

############################ Order Type CE or PE #############################################

Order_type_var=IntVar()

call_button=Radiobutton(BUY_SELL_Frame,text="CE",font="comicsansms 17 bold",variable=Order_type_var,value=1,command=Call_side_Order)
put_button=Radiobutton(BUY_SELL_Frame,text="PE",font="comicsansms 17 bold",variable=Order_type_var,value=2,command=Put_side_Order)

call_button.grid()
put_button.grid(row=0,column=1)

######################################## Stop Loss ####################################

########################## Recall Button ####################################

Recall_button=Button(BUY_SELL_Frame,text="Recall",font="comicsansms 14 bold",bg="pink",command=Recall_order_info)
Recall_button.grid(row=0,column=3)


Month_end_var=IntVar()

Month_end=Radiobutton(BUY_SELL_Frame,text="Month End",font="comicsansms 14 bold",variable=Month_end_var,value=40)
Month_end.grid(row=0,column=4)
########################## Recall Button ####################################

################################ Status Message Box and Moving aV bat file running ######################################

MA_start_button=Button(BUY_SELL_Frame,text="MA code",font="comicsansms 14 bold",bg="pink",command=MA_code_start)
MA_start_button.grid(row=0,column=5,padx=10)

l111=Label(BUY_SELL_Frame,text="Buy Price: Status",font="comicsansms 12 bold",bg='yellow')
l111.grid(row=1,column=5)

l112=Label(BUY_SELL_Frame,text="None: None",font="comicsansms 12 bold",bg='pink')
l112.grid(row=2,column=5)

l113=Label(BUY_SELL_Frame,text="SL Price: SL Status",font="comicsansms 12 bold",bg='yellow')
l113.grid(row=3,column=5)

l114=Label(BUY_SELL_Frame,text="None: None",font="comicsansms 12 bold",bg='pink')
l114.grid(row=4,column=5)

l115=Label(BUY_SELL_Frame,text="Sell Price: Sell Status",font="comicsansms 12 bold",bg='yellow')
l115.grid(row=5,column=5)

l116=Label(BUY_SELL_Frame,text="None: None",font="comicsansms 12 bold",bg='pink')
l116.grid(row=6,column=5)

l117=Label(BUY_SELL_Frame,text="MA status",font="comicsansms 12 bold",bg='yellow')
l117.grid(row=7,column=5)

l118=Label(BUY_SELL_Frame,text="None",font="comicsansms 12 bold",bg='pink')
l118.grid(row=8,column=5)

Market_sell_button=Button(BUY_SELL_Frame,text="M Sell",font="comicsansms 14 bold",bg="red",command=Market_sell)
Market_sell_button.grid(row=9,column=5)
################################ Status Message Box and Moving aV bat file running ######################################

############################ Order Type CE or PE #############################################


############################ Buy and Sell Order and Immediate Buy and Sell order #############################################
virtual_buy_loop=IntVar()
Buy=Radiobutton(BUY_SELL_Frame,text="VMA Buy L",font="comicsansms 14 bold",bg='green',variable=virtual_buy_loop,value=100,command=Buy_loop)
Sell=Radiobutton(BUY_SELL_Frame,text="VMA Sell L",font="comicsansms 14 bold",bg='red',variable=virtual_buy_loop,value=101,command=Sell_loop)

Buy.grid(row=1,column=0,padx=5,pady=8)
Sell.grid(row=1,column=1)

##################################### Modify Order ##########################################################

Modify_buy_var=IntVar()

Modify_buy=Radiobutton(BUY_SELL_Frame,text="VModify Buy",font="comicsansms 14 bold",variable=Modify_buy_var,value=11,command=Modify_Buy_enable)
Modify_buy.grid(row=1,column=3)


Modify_loop_Buy_sell=IntVar()

V_Modify_buy_button=Radiobutton(BUY_SELL_Frame,text="VMB L",font="comicsansms 14 bold",bg='green',variable=Modify_loop_Buy_sell,value=106,command=V_Buy_Modify_Loop)
V_Modify_buy_button.grid(row=1,column=4)

Previous_candle_buy=Label(BUY_SELL_Frame,text="Previous candle:",font="comicsansms 14 bold",bg="grey",fg="blue")
Previous_candle_buy.grid(row=2,column=3)

Price_buy=Label(BUY_SELL_Frame,text="price",font="comicsansms 12 bold",bg="grey")
Price_buy.grid(row=2,column=4)

Size_buy=Label(BUY_SELL_Frame,text="Buy Size:",font="comicsansms 14 bold",bg="grey",fg="blue")
Size_buy.grid(row=3,column=3)

Buy_size=Label(BUY_SELL_Frame,text="Size",font="comicsansms 12 bold",bg="grey")
Buy_size.grid(row=3,column=4)

l12=Label(BUY_SELL_Frame,text="Buy Price",font="comicsansms 12 bold",bg="grey",fg="blue")
l12.grid(row=4,column=3)

Buy_price_Entry=Entry(BUY_SELL_Frame,state=DISABLED)
Buy_price_Entry.grid(row=4,column=4)


Modify_sell_var=IntVar()

Modify_Sell=Radiobutton(BUY_SELL_Frame,text="VModify Sell",font="comicsansms 14 bold",variable=Modify_sell_var,value=12,command=Modify_Sell_enable)
Modify_Sell.grid(row=5,column=3)

Modify_sell_button=Radiobutton(BUY_SELL_Frame,text="VMS L",font="comicsansms 14 bold",bg='red',variable=Modify_loop_Buy_sell,value=107,command=V_Sell_Modify_Loop)
Modify_sell_button.grid(row=5,column=4)

Previous_candle_sell=Label(BUY_SELL_Frame,text="Previous candle:",font="comicsansms 14 bold",bg="grey",fg="blue")
Previous_candle_sell.grid(row=6,column=3)

Price_sell=Label(BUY_SELL_Frame,text="price",font="comicsansms 12 bold",bg="grey")
Price_sell.grid(row=6,column=4)

Size_sell=Label(BUY_SELL_Frame,text="Sell Size:",font="comicsansms 14 bold",bg="grey",fg="blue")
Size_sell.grid(row=7,column=3)

size_s=Label(BUY_SELL_Frame,text="Size",font="comicsansms 12 bold",bg="grey")
size_s.grid(row=7,column=4)

l13=Label(BUY_SELL_Frame,text="Sell Price",font="comicsansms 12 bold",bg="grey",fg="blue")
l13.grid(row=8,column=3)

Sell_price_Entry=Entry(BUY_SELL_Frame,state=DISABLED)
Sell_price_Entry.grid(row=8,column=4)

##################################### Modify Order ##########################################################

SL2_percent=IntVar()
SL_2_percent=Radiobutton(BUY_SELL_Frame,text="VSL2",font="comicsansms 14 bold",bg='red',variable=SL2_percent,value=103,command=SL_2_Percent_loop)
SL_2_percent.grid(row=2,column=0,padx=8)

############################ Buy and Sell Order and Immediate Buy and Sell order #############################################

####################### Moving Average Loop read enable Disable ###################################

MA_loop_var=IntVar()

MA_loop_enable=Radiobutton(BUY_SELL_Frame,text="MA Loop En",font="comicsansms 12 bold",variable=MA_loop_var,value=20,command=Moving_average_status_update)
MA_loop_enable.grid(row=9,column=3)

MA_loop_disable=Radiobutton(BUY_SELL_Frame,text="MA Loop Di",font="comicsansms 12 bold",variable=MA_loop_var,value=21,command=Moving_average_status_update)
MA_loop_disable.grid(row=9,column=4)




####################### Moving Average Loop read enable Disable ###################################

############################ Type Trading ##################################################################



trading_var=IntVar()

testing_button=Radiobutton(BUY_SELL_Frame,text="Testing",font="comicsansms 12 bold",variable=trading_var,value=3,command=Testing)
Real_Trading_button=Radiobutton(BUY_SELL_Frame,text="Serious",font="comicsansms 12 bold",variable=trading_var,value=4,command=Real_Trading)
testing_button.grid(row=3,column=0,pady=5)
Real_Trading_button.grid(row=4,column=0,pady=5)

l1=Label(BUY_SELL_Frame,text="Lot Size Buy",font="comicsansms 12 bold",bg="grey")
l1.grid(row=5,column=0)

lot_entry=Entry(BUY_SELL_Frame,state=DISABLED)
lot_entry.grid(row=5,column=1)


l2=Label(BUY_SELL_Frame,text="Lot Size Sell",font="comicsansms 12 bold",bg="grey")
l2.grid(row=6,column=0)

lot_entry_Sell=Entry(BUY_SELL_Frame,state=DISABLED)
lot_entry_Sell.grid(row=6,column=1)

size_push_buy=Button(BUY_SELL_Frame,text="Place Buy size",font="comicsansms 12 bold",fg="green",command=size_computation_buy)
size_push_buy.grid(row=3,column=1)

size_push_sell=Button(BUY_SELL_Frame,text="Place Sell size",font="comicsansms 12 bold",fg="green",command=size_computation_sell)
size_push_sell.grid(row=4,column=1)

############################ Type Trading ########################################################################

################################## Cancel Order #################################################################
cancel_var_order=IntVar()
cancel_order=Radiobutton(BUY_SELL_Frame,text="Cancel Order",font="comicsansms 12 bold",bg="blue",variable=cancel_var_order,value=110)
cancel_order.grid(row=7,column=0)


################################## Cancel Order #################################################################

GUI.grid_rowconfigure(0, weight=1)


################################# Menu Bar #################################################################

############### BUY ########

menu_bar=Menu(GUI)
GUI.config(menu=menu_bar)

Immediate_Buy_sell_menue=Menu(menu_bar,tearoff=0)
menu_bar.add_cascade(label="Immediate Orders Buy",menu=Immediate_Buy_sell_menue)

min_menue=Menu(Immediate_Buy_sell_menue,tearoff=0)
Immediate_Buy_sell_menue.add_cascade(label="1 min",menu=min_menue)
min_menue.add_command(label="High",command=I_High_1min)
min_menue.add_command(label="Low",command=I_Low_1min)
min_menue.add_command(label="Open",command=I_Open_1min)
min_menue.add_command(label="Close",command=I_Close_1min)

Immediate_Buy_sell_menue.add_separator()

five_min_menue=Menu(Immediate_Buy_sell_menue,tearoff=0)
Immediate_Buy_sell_menue.add_cascade(label="5 min",menu=five_min_menue)
five_min_menue.add_command(label="High",command=I_High_5min)
five_min_menue.add_command(label="Low",command=I_Low_5min)
five_min_menue.add_command(label="Open",command=I_Open_5min)
five_min_menue.add_command(label="Close",command=I_Close_5min)


############### BUY ########

############### SELL ########


Immediate_sell_menue=Menu(menu_bar,tearoff=0)
menu_bar.add_cascade(label="Immediate Orders Sell",menu=Immediate_sell_menue)

min_menue=Menu(Immediate_sell_menue,tearoff=0)
Immediate_sell_menue.add_cascade(label="1 min",menu=min_menue)
min_menue.add_command(label="High",command=I_High_1min_sell)
min_menue.add_command(label="Low",command=I_Low_1min_sell)
min_menue.add_command(label="Open",command=I_Open_1min_sell)
min_menue.add_command(label="Close",command=I_Close_1min_sell)

Immediate_sell_menue.add_separator()

five_min_menue=Menu(Immediate_sell_menue,tearoff=0)
Immediate_sell_menue.add_cascade(label="5 min",menu=five_min_menue)
five_min_menue.add_command(label="High",command=I_High_5min_sell)
five_min_menue.add_command(label="Low",command=I_Low_5min_sell)
five_min_menue.add_command(label="Open",command=I_Open_5min_sell)
five_min_menue.add_command(label="Close",command=I_Close_5min_sell)

############### SELL ########

############### Immediate STOP Loss ########

Immediate_stoploss_menue=Menu(menu_bar,tearoff=0)
menu_bar.add_cascade(label="Immediate Stop loss",menu=Immediate_stoploss_menue)

min_menue=Menu(Immediate_stoploss_menue,tearoff=0)
Immediate_stoploss_menue.add_cascade(label="1 min Trailing",menu=min_menue)
min_menue.add_command(label="Low",command=SL_low_1_min)
min_menue.add_command(label="Close",command=SL_close_1_min)

five_min_menue=Menu(Immediate_stoploss_menue,tearoff=0)
Immediate_stoploss_menue.add_cascade(label="5 min Trailing",menu=five_min_menue)
five_min_menue.add_command(label="Low",command=SL_low_5_min)
five_min_menue.add_command(label="Close",command=SL_close_5_min)

Immediate_stoploss_menue.add_separator()

Immediate_stoploss_menue.add_command(label="2% SL",command=Enable_Stoploss)

############### Immediate STOP Loss ########

############### Moving Average STOP Loss ########

Moving_Average_stoploss_menue=Menu(menu_bar,tearoff=0)
menu_bar.add_cascade(label="MA Stop loss",menu=Moving_Average_stoploss_menue)

min_menue=Menu(Moving_Average_stoploss_menue,tearoff=0)
Moving_Average_stoploss_menue.add_cascade(label="1 min Trailing",menu=min_menue)
min_menue.add_command(label="9 EMA",command=SL_9_EMA_1_min)
min_menue.add_command(label="21 EMA",command=SL_21_EMA_1_min)
min_menue.add_command(label="50 EMA",command=SL_50_EMA_1_min)
min_menue.add_command(label="200 EMA",command=SL_200_EMA_1_min)

five_min_menue=Menu(Moving_Average_stoploss_menue,tearoff=0)
Moving_Average_stoploss_menue.add_cascade(label="5 min Trailing",menu=five_min_menue)
five_min_menue.add_command(label="9 EMA",command=SL_9_EMA_5_min)
five_min_menue.add_command(label="21 EMA",command=SL_21_EMA_5_min)
five_min_menue.add_command(label="50 EMA",command=SL_50_EMA_5_min)
five_min_menue.add_command(label="200 EMA",command=SL_200_EMA_5_min)

############### Moving Average STOP Loss ########


############### Buy at Moving Average ########
Moving_Average_Buy_menue=Menu(menu_bar,tearoff=0)
menu_bar.add_cascade(label="MA Buy",menu=Moving_Average_Buy_menue)

min_menue=Menu(Moving_Average_Buy_menue,tearoff=0)
Moving_Average_Buy_menue.add_cascade(label="1 min",menu=min_menue)
min_menue.add_command(label="9 EMA",command=MA_9EMA_1min_buy)
min_menue.add_command(label="21 EMA",command=MA_21EMA_1min_buy)
min_menue.add_command(label="50 EMA",command=MA_50EMA_1min_buy)
min_menue.add_command(label="200 EMA",command=MA_200EMA_1min_buy)

five_min_menue=Menu(Moving_Average_Buy_menue,tearoff=0)
Moving_Average_Buy_menue.add_cascade(label="5 min",menu=five_min_menue)
five_min_menue.add_command(label="9 EMA",command=MA_9EMA_5min_buy)
five_min_menue.add_command(label="21 EMA",command=MA_21EMA_5min_buy)
five_min_menue.add_command(label="50 EMA",command=MA_50EMA_5min_buy)
five_min_menue.add_command(label="200 EMA",command=MA_200EMA_5min_buy)

############### Buy at Moving Average ########

############### Sell at Moving Average ########
Moving_Average_Sell_menue=Menu(menu_bar,tearoff=0)
menu_bar.add_cascade(label="MA Sell",menu=Moving_Average_Sell_menue)

min_menue=Menu(Moving_Average_Sell_menue,tearoff=0)
Moving_Average_Sell_menue.add_cascade(label="1 min",menu=min_menue)
min_menue.add_command(label="9 EMA",command=MA_9EMA_1min_sell)
min_menue.add_command(label="21 EMA",command=MA_21EMA_1min_sell)
min_menue.add_command(label="50 EMA",command=MA_50EMA_1min_sell)
min_menue.add_command(label="200 EMA",command=MA_200EMA_1min_sell)

five_min_menue=Menu(Moving_Average_Sell_menue,tearoff=0)
Moving_Average_Sell_menue.add_cascade(label="5 min",menu=five_min_menue)
five_min_menue.add_command(label="9 EMA",command=MA_9EMA_5min_sell)
five_min_menue.add_command(label="21 EMA",command=MA_21EMA_5min_sell)
five_min_menue.add_command(label="50 EMA",command=MA_50EMA_5min_sell)
five_min_menue.add_command(label="200 EMA",command=MA_200EMA_5min_sell)

############### Sell at Moving Average ########

################################# Menu Bar #################################################################
refresh=Button(BUY_SELL_Frame,text="Refresh",font="comicsansms 12 bold",bg='pink',command=Refresh_all)
refresh.grid(row=8,column=0,pady=5)


Interrupt_Button=Button(BUY_SELL_Frame,text="Interrupt SL",font="comicsansms 12 bold",fg="red",bg="white",command=Interrupt_butt)
Interrupt_Button.grid(row=9,column=0,pady=5)

Trailing_SL_var=IntVar()

l5=Radiobutton(BUY_SELL_Frame,text="Trailing SL",font="comicsansms 12 bold",variable=Trailing_SL_var,value=30,command=Trailing_SL)
l5.grid(row=7,column=1)

Trailing_SL_Size=Entry(BUY_SELL_Frame,state=DISABLED)
Trailing_SL_Size.grid(row=8,column=1)

SL_Size_Button=Button(BUY_SELL_Frame,text="Place SL Size",font="comicsans 12 bold",bg="yellow",command=Placement_of_Sell_Size)
SL_Size_Button.grid(row=9,column=1)


################################# Error Message #################################################################

error_message_frame=Frame(GUI,bg="grey",borderwidth=6,relief=SUNKEN)
error_message_frame.grid(row=1, column=0)

error_message =Label(error_message_frame,text="Error message",font="comicsansms 12 bold",fg="red")
error_message.grid(row=0,column=0)

message_label = Label(error_message_frame, text="", font=("Helvetica", 12))
message_label.grid(row=1,column=0)


################################# Error Message #################################################################

########################################## Processing of the Data Start ##################################

ATM_Strike_Price=None
ATM_Strike_Price_Plus_1=None
ATM_Strike_Price_Minus_1=None

# log_file="Order_Log_File.txt"

# ll1=[]

# with open(path+log_file,"w") as file:
#     file.write(str(ll1))


path_main="D:/ashu/Finance/algo_trading/Zerodha_GUI/Kite_Zerodha-main/Kite_Zerodha-main/"

df=pd.read_csv(path_main+"Enctoke_Expiry_month_end_info.csv")
content_enctoken=df.iloc[0,0]

enctoken = content_enctoken


content_expiry_day=df.iloc[0,1]

name="NIFTY"
expiry=content_expiry_day
path="D:/ashu/Finance/algo_trading/Zerodha_GUI/GUI_raw_data_Collected/"

final_new=Intraday_live_data.getoptionchain(name,expiry)
final_new.reset_index(drop=True, inplace=True)

final_new.to_csv(path+"Nifty_option_chain.csv",index=False)

update_strike_price()
# order_update_func()


########################################## Processing of the Data Start ##################################

GUI.mainloop()




