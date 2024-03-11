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

path_main="D:/ashu/Finance/algo_trading/Zerodha_GUI/Kite_Zerodha-main/Kite_Zerodha-main/"

with open(path_main+"expiry_date.txt",'r') as file:
    content_expiry_date=file.read()

expiry_date=content_expiry_date

def find_closest_index(numbers, target):
    closest_index = None
    min_difference = float('inf')  # Set to positive infinity initially

    for i, number in enumerate(numbers):
        difference = abs(number - target)

        if difference < min_difference:
            min_difference = difference
            closest_index = i

    return closest_index


def quote_token_computation(strike_price_list_new,name,expiry):
    global Month_end
    global kite

    Strike_Prices=strike_price_list_new

    if Month_end==0:
        call_list=[]
        put_list=[]
        token_CE=[]
        token_PE=[]
        call_put_dict={}

        from datetime import datetime

        # parsed_date = datetime.strptime(expiry, '%d-%b-%Y')
        # formatted_date = parsed_date.strftime('%y%m%d')

        # char_list = list(formatted_date)

        # if char_list[2]=='0':
        #     char_list.pop(2)

        formatted_date=date_time_format.date_time_format(expiry)

        if name=="SENSEX":
            
            for i in range(len(Strike_Prices)):
                quote_CE=name+formatted_date+str(Strike_Prices[i])+"CE"
                quote_PE=name+formatted_date+str(Strike_Prices[i])+"PE"
                call_list.append(quote_CE)
                put_list.append(quote_PE)

            for j in range(len(Strike_Prices)):
                atm_token_ce=kite.ltp("BFO:"+call_list[j])
                atm_token_pe=kite.ltp("BFO:"+put_list[j])
                ATM_Token_CE=atm_token_ce["BFO:"+call_list[j]]['instrument_token']
                ATM_Token_PE=atm_token_pe["BFO:"+put_list[j]]['instrument_token']
                token_CE.append(ATM_Token_CE)
                token_PE.append(ATM_Token_PE)

            call_put_dict["quote_call"]=call_list
            call_put_dict["quote_put"]=put_list
            call_put_dict["token_call"]=token_CE
            call_put_dict["token_put"]=token_PE
            call_put_dict["Strike Prices"]=Strike_Prices

            print(call_put_dict)

            with open(path+"Call_put_quote_token.txt",'w') as file:
                file.write(str(call_put_dict))

        else:

            for i in range(len(Strike_Prices)):
                quote_CE=name+formatted_date+str(Strike_Prices[i])+"CE"
                quote_PE=name+formatted_date+str(Strike_Prices[i])+"PE"
                call_list.append(quote_CE)
                put_list.append(quote_PE)

            for j in range(len(Strike_Prices)):
                atm_token_ce=kite.ltp("NFO:"+call_list[j])
                atm_token_pe=kite.ltp("NFO:"+put_list[j])
                ATM_Token_CE=atm_token_ce["NFO:"+call_list[j]]['instrument_token']
                ATM_Token_PE=atm_token_pe["NFO:"+put_list[j]]['instrument_token']
                token_CE.append(ATM_Token_CE)
                token_PE.append(ATM_Token_PE)

            call_put_dict["quote_call"]=call_list
            call_put_dict["quote_put"]=put_list
            call_put_dict["token_call"]=token_CE
            call_put_dict["token_put"]=token_PE
            call_put_dict["Strike Prices"]=Strike_Prices

            print(call_put_dict)

            with open(path+"Call_put_quote_token.txt",'w') as file:
                file.write(str(call_put_dict))

    elif Month_end==1:

        from datetime import datetime

        call_list=[]
        put_list=[]
        token_CE=[]
        token_PE=[]
        call_put_dict={}
        # parsed_date = datetime.strptime(expiry, '%d-%b-%Y')
        # formatted_date = parsed_date.strftime('%Y%b').upper()


        formatted_date=date_time_format.date_time_format(expiry)

        if name=="SENSEX":
            for i in range(len(Strike_Prices)):
                quote_CE=name+formatted_date+str(Strike_Prices[i])+"CE"
                quote_PE=name+formatted_date+str(Strike_Prices[i])+"PE"
                call_list.append(quote_CE)
                put_list.append(quote_PE)


            for j in range(len(Strike_Prices)):
                atm_token_ce=kite.ltp("BFO:"+call_list[j])
                atm_token_pe=kite.ltp("BFO:"+put_list[j])
                ATM_Token_CE=atm_token_ce["BFO:"+call_list[j]]['instrument_token']
                ATM_Token_PE=atm_token_pe["BFO:"+put_list[j]]['instrument_token']
                token_CE.append(ATM_Token_CE)
                token_PE.append(ATM_Token_PE)


            call_put_dict["quote_call"]=call_list
            call_put_dict["quote_put"]=put_list
            call_put_dict["token_call"]=token_CE
            call_put_dict["token_put"]=token_PE
            call_put_dict["Strike Prices"]=Strike_Prices

            print(call_put_dict)

            with open(path+"Call_put_quote_token.txt",'w') as file:
                file.write(str(call_put_dict))

        else:
            for i in range(len(Strike_Prices)):
                quote_CE=name+formatted_date+str(Strike_Prices[i])+"CE"
                quote_PE=name+formatted_date+str(Strike_Prices[i])+"PE"
                call_list.append(quote_CE)
                put_list.append(quote_PE)


            for j in range(len(Strike_Prices)):
                atm_token_ce=kite.ltp("NFO:"+call_list[j])
                atm_token_pe=kite.ltp("NFO:"+put_list[j])
                ATM_Token_CE=atm_token_ce["NFO:"+call_list[j]]['instrument_token']
                ATM_Token_PE=atm_token_pe["NFO:"+put_list[j]]['instrument_token']
                token_CE.append(ATM_Token_CE)
                token_PE.append(ATM_Token_PE)


            call_put_dict["quote_call"]=call_list
            call_put_dict["quote_put"]=put_list
            call_put_dict["token_call"]=token_CE
            call_put_dict["token_put"]=token_PE
            call_put_dict["Strike Prices"]=Strike_Prices

            print(call_put_dict)

            with open(path+"Call_put_quote_token.txt",'w') as file:
                file.write(str(call_put_dict))            

    else:
        pass

    # historical_OI_computation()

def strike_update(expiry,name):
    global path
    global content_enctoken

    instrument=["NIFTY 50","NIFTY BANK","NIFTY FIN SERVICE","NIFTY MID SELECT","SENSEX"]
    Strike_interval=[50,100,50,25,100]

    enctoken = content_enctoken

    kite = KiteApp(enctoken=enctoken)

    if name=="NIFTY":
        final_new=Intraday_live_data.getoptionchain(name,expiry)
        final_new.reset_index(drop=True, inplace=True)

        nifty_current_price=kite.ltp([f"NSE:{instrument[0]}"])
        Nifty_current_price=nifty_current_price[f'NSE:{instrument[0]}']['last_price']

        index = (final_new['strikePrice'] - Nifty_current_price).abs().idxmin()
        ATM_strike_price=final_new['strikePrice'].iloc[index]

        ATM_Plus_one=ATM_strike_price+Strike_interval[0]
        ATM_Minus_one=ATM_strike_price-Strike_interval[0]

        strike_price_list_new=[ATM_strike_price,ATM_Plus_one,ATM_Minus_one]

    elif name=="BANKNIFTY":
        final_new=Intraday_live_data.getoptionchain(name,expiry)
        final_new.reset_index(drop=True, inplace=True)

        Bank_nifty_current_price=kite.ltp([f"NSE:{instrument[1]}"])
        BankNifty_current_price=Bank_nifty_current_price[f'NSE:{instrument[1]}']['last_price']

        index = (final_new['strikePrice'] - BankNifty_current_price).abs().idxmin()
        ATM_strike_price=final_new['strikePrice'].iloc[index]

        ATM_Plus_one=ATM_strike_price+Strike_interval[1]
        ATM_Minus_one=ATM_strike_price-Strike_interval[1]

        strike_price_list_new=[ATM_strike_price,ATM_Plus_one,ATM_Minus_one]

    elif name=="FINNIFTY":
        final_new=Intraday_live_data.getoptionchain(name,expiry)
        final_new.reset_index(drop=True, inplace=True)

        Fin_nifty_current_price=kite.ltp([f"NSE:{instrument[2]}"])
        FinNifty_current_price=Fin_nifty_current_price[f'NSE:{instrument[2]}']['last_price']

        index = (final_new['strikePrice'] - FinNifty_current_price).abs().idxmin()
        ATM_strike_price=final_new['strikePrice'].iloc[index]

        ATM_Plus_one=ATM_strike_price+Strike_interval[2]
        ATM_Minus_one=ATM_strike_price-Strike_interval[2]

        strike_price_list_new=[ATM_strike_price,ATM_Plus_one,ATM_Minus_one]   

    elif name=="MIDCPNIFTY":

        start=8700
        end=12100

        itteration=(end-start)/Strike_interval[3]

        strike_list=[]

        for i in range(int(itteration)):
            strike=start+Strike_interval[3]*i
            strike_list.append(strike)

        MIDCP_nifty_current_price=kite.ltp([f"NSE:{instrument[3]}"])
        MIDCPNifty_current_price=MIDCP_nifty_current_price[f'NSE:{instrument[3]}']['last_price']

        index=find_closest_index(strike_list,int(MIDCPNifty_current_price))
        ATM_strike_price=strike_list[index]

        ATM_Plus_one=ATM_strike_price+Strike_interval[3]
        ATM_Minus_one=ATM_strike_price-Strike_interval[3]

        strike_price_list_new=[ATM_strike_price,ATM_Plus_one,ATM_Minus_one]   

    elif name=="SENSEX":

        start=63700
        end=75400

        itteration=(end-start)/Strike_interval[4]

        strike_list=[]

        for i in range(int(itteration)):
            strike=start+Strike_interval[4]*i
            strike_list.append(strike)

        Sensex_current_price=kite.ltp([f"BSE:{instrument[4]}"])
        Sensexcurrent_price=Sensex_current_price[f'BSE:{instrument[4]}']['last_price']

        index=find_closest_index(strike_list,int(Sensexcurrent_price))
        ATM_strike_price=strike_list[index]

        ATM_Plus_one=ATM_strike_price+Strike_interval[4]
        ATM_Minus_one=ATM_strike_price-Strike_interval[4]

        strike_price_list_new=[ATM_strike_price,ATM_Plus_one,ATM_Minus_one]   
    else:
        pass

    with open(path+"strike_price_list.txt",'r') as file:
        content=file.read()


    if str(strike_price_list_new) in content:
        pass
    else:
        if os.path.getsize(path+"strike_price_list.txt") == 0:
            strike_price_to_add=strike_price_list_new
            strike_price_to_remove=None
            with open(path+"strike_price_list.txt",'w') as file:
                file.write(str(strike_price_list_new))
        else:
            with open(path+"strike_price_list.txt",'w') as file:
                file.write(str(strike_price_list_new))
            old_stk_price = ast.literal_eval(content)
            set1 = set(old_stk_price)
            set2 = set(strike_price_list_new)
            strike_price_to_add = list(set2 - set1)
            strike_price_to_remove = list(set1 - set2)

        print(strike_price_list_new)
        print(strike_price_to_add)
        print(strike_price_to_remove)

        quote_token_computation(strike_price_list_new,name,expiry)

    schedule_next_execution(expiry,name)



def schedule_next_execution(expiry,name):
    import time
    global time_list
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
        time.sleep(int(time_difference))
        strike_update(expiry,name)
        
    else:
        # No more times in the list for today, you can handle this case as needed
        print("No more times to execute today")


############# 1 means month end and 0 means not month end ####################

def quote_token_computation_main(name="NIFTY",expiry=expiry_date):
    

    import datetime


    today = datetime.datetime.now().date()
    formatted_date = today.strftime('%Y-%m-%d')
    specific_date = formatted_date


    files = os.listdir(path)

    # Filter the list to keep only CSV files
    csv_files = [file for file in files if file.endswith(".csv")]

    # Check if there are any CSV files to remove
    if csv_files:
        # Iterate through the list of CSV files and remove each one
        for csv_file in csv_files:
            file_path = os.path.join(path, csv_file)
            os.remove(file_path)
        print("CSV files removed successfully.")
    else:
        pass



    # final_new=Intraday_live_data.getoptionchain(name,expiry)
    # final_new.reset_index(drop=True, inplace=True)

    # final_new.to_csv(path+"Nifty_option_chain.csv",index=False)


    with open(path+"Strike_price_list.txt",'w') as file:
        pass


    strike_update(expiry,name)

global name
global expiry

run=0
path="D:/ashu/Finance/algo_trading/Zerodha_GUI/OI_Raw_Data_Collected/"

df=pd.read_csv(path_main+"Enctoke_Expiry_month_end_info.csv")

content_enctoken=df.iloc[0,0]

enctoken = content_enctoken
kite = KiteApp(enctoken=enctoken)
Month_end=df.iloc[0,2]



#######################################################  Time List Computation #################################################
from datetime import datetime, timedelta

# Define the start and end times
start_time = datetime.strptime("9:15:00", "%H:%M:%S")
end_time = datetime.strptime("15:30:00", "%H:%M:%S")

# Define the interval (3 minutes)
interval = timedelta(minutes=1)

# Initialize an empty list to store the generated times
time_list = []

# Generate the times
current_time = start_time
while current_time <= end_time:
    time_list.append(current_time.strftime("%H:%M:%S"))
    current_time += interval

#######################################################  Time List Computation #################################################

segment=["NIFTY","FINNIFTY","BANKNIFTY","MIDCPNIFTY","SENSEX"]
expiry_days=["15-Feb-2024","09-Jan-2024","03-Jan-2024","08-Jan-2024","05-Jan-2024"]


quote_token_computation_main(segment[0],expiry_days[0])