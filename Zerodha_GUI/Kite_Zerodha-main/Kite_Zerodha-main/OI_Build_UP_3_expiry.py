import datetime
from kite_trade import *
import pandas as pd
import ast
import Intraday_live_data
import matplotlib.pyplot as plt
import numpy as np
from tkinter import *
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import date_time_format

def create_toolbar(fig_canvas, frame):
    toolbar = NavigationToolbar2Tk(fig_canvas, frame)
    toolbar.update()
    return toolbar

def comparision(row):
        if ((row['COI'] > 0 and row['COP'] > 0)):
            return 'LB'
        elif ((row['COI'] < 0 and row['COP'] < 0)):
            return 'LC'
        elif ((row['COI'] > 0 and row['COP'] < 0)):
            return 'SB'
        elif ((row['COI'] < 0 and row['COP'] > 0)):
            return 'SC'
        else:
            pass

def date_time_computation():
    from datetime import datetime, timedelta

    today = datetime.today()
    # Calculate the difference in days to go back to the previous Thursday
    days_until_previous_thursday = (today.weekday() - 3) % 7

    # Calculate the dates for the previous 3 Thursdays
    previous_thursdays = [today - timedelta(days=days_until_previous_thursday)]
    for _ in range(2):
        previous_thursdays.append(previous_thursdays[-1] - timedelta(weeks=1))

    x=[]
    # Print the previous 3 Thursdays
    for thursday in previous_thursdays:
        date=thursday.strftime('%Y-%m-%d')
        x.append(str(date))


    l=len(x)
    DATE=x[l-2]
    start_date_str = DATE
    start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
    today = datetime.today()

    result_dates = []

    # Loop through the dates, excluding Saturdays and Sundays, until today's date
    while start_date <= today:
        # Check if the current date is not a Saturday (5) or Sunday (6)
        if start_date.weekday() not in [5, 6]:
            result_dates.append(start_date.strftime('%Y-%m-%d'))
        
        # Increment the current date by one day
        start_date += timedelta(days=1)

    date_list=[]
    # Print the list of dates excluding weekends up to today's date
    for date in result_dates:
        date_list.append(str(date))

    date_list.pop(0)

    return date_list

################################    Segment Selection and token Generation  #####################################

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

    enctoken = content_enctoken

    kite = KiteApp(enctoken=enctoken)

    if Month_end==0:
        call_list=[]
        put_list=[]
        token_CE=[]
        token_PE=[]
        call_put_dict={}

        from datetime import datetime


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


        formatted_date=date_time_format.date_time_format()

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

def strike_update(expiry,name,closing_price):
    global path
    global content_enctoken

    instrument=["NIFTY 50","NIFTY BANK","NIFTY FIN SERVICE","NIFTY MID SELECT","SENSEX"]
    Strike_interval=[50,100,50,25,100]

    enctoken = content_enctoken

    kite = KiteApp(enctoken=enctoken)

    if name=="NIFTY":
        final_new=Intraday_live_data.getoptionchain(name,expiry)
        final_new.reset_index(drop=True, inplace=True)

        Nifty_current_price=closing_price

        index = (final_new['strikePrice'] - Nifty_current_price).abs().idxmin()
        ATM_strike_price=final_new['strikePrice'].iloc[index]

        ATM_Plus_one=ATM_strike_price+Strike_interval[0]
        ATM_Minus_one=ATM_strike_price-Strike_interval[0]

        strike_price_list_new=[ATM_strike_price,ATM_Plus_one,ATM_Minus_one]

        quote_token_computation(strike_price_list_new,name,expiry)

    elif name=="BANKNIFTY":
        final_new=Intraday_live_data.getoptionchain(name,expiry)
        final_new.reset_index(drop=True, inplace=True)

        BankNifty_current_price=closing_price

        index = (final_new['strikePrice'] - BankNifty_current_price).abs().idxmin()
        ATM_strike_price=final_new['strikePrice'].iloc[index]

        ATM_Plus_one=ATM_strike_price+Strike_interval[1]
        ATM_Minus_one=ATM_strike_price-Strike_interval[1]

        strike_price_list_new=[ATM_strike_price,ATM_Plus_one,ATM_Minus_one]
        quote_token_computation(strike_price_list_new,name,expiry)

    elif name=="FINNIFTY":
        final_new=Intraday_live_data.getoptionchain(name,expiry)
        final_new.reset_index(drop=True, inplace=True)

        FinNifty_current_price=closing_price

        index = (final_new['strikePrice'] - FinNifty_current_price).abs().idxmin()
        ATM_strike_price=final_new['strikePrice'].iloc[index]

        ATM_Plus_one=ATM_strike_price+Strike_interval[2]
        ATM_Minus_one=ATM_strike_price-Strike_interval[2]

        strike_price_list_new=[ATM_strike_price,ATM_Plus_one,ATM_Minus_one]   
        quote_token_computation(strike_price_list_new,name,expiry)

    elif name=="MIDCPNIFTY":

        start=8700
        end=12100

        itteration=(end-start)/Strike_interval[3]

        strike_list=[]

        for i in range(int(itteration)):
            strike=start+Strike_interval[3]*i
            strike_list.append(strike)

        MIDCPNifty_current_price=closing_price

        index=find_closest_index(strike_list,int(MIDCPNifty_current_price))
        ATM_strike_price=strike_list[index]

        ATM_Plus_one=ATM_strike_price+Strike_interval[3]
        ATM_Minus_one=ATM_strike_price-Strike_interval[3]

        strike_price_list_new=[ATM_strike_price,ATM_Plus_one,ATM_Minus_one]   
        quote_token_computation(strike_price_list_new,name,expiry)

    elif name=="SENSEX":

        start=63700
        end=75400

        itteration=(end-start)/Strike_interval[4]

        strike_list=[]

        for i in range(int(itteration)):
            strike=start+Strike_interval[4]*i
            strike_list.append(strike)

        Sensexcurrent_price=closing_price

        index=find_closest_index(strike_list,int(Sensexcurrent_price))
        ATM_strike_price=strike_list[index]

        ATM_Plus_one=ATM_strike_price+Strike_interval[4]
        ATM_Minus_one=ATM_strike_price-Strike_interval[4]

        strike_price_list_new=[ATM_strike_price,ATM_Plus_one,ATM_Minus_one]   
        quote_token_computation(strike_price_list_new,name,expiry)
    else:
        pass

################################    Segment Selection and token Generation  #####################################


def comparision_CE(row):
        if (row['Conclusion CE'] =="LB"):
            return 0
        elif (row['Conclusion CE'] =="LC"):
            return 0
        elif (row['Conclusion CE'] =="SB"):
            return -1
        elif (row['Conclusion CE'] =="SC"):
            return -1
        else:
            pass

def comparision_PE(row):
        if (row['Conclusion PE'] =="LB"):
            return 0
        elif (row['Conclusion PE'] =="LC"):
            return 0
        elif (row['Conclusion PE'] =="SB"):
            return 1
        elif (row['Conclusion PE'] =="SC"):
            return 1
        else:
            pass

def data_frame_list_generation(Strike_Prices):
    df=[]

    for i in range(len(Strike_Prices)):
        df_i=pd.read_csv(path+name+str(Strike_Prices[i])+".csv")
        new_df=df_i[["Datetime","Cumulative Bullishness","Cumulative SB call","Cumulative SB put"]]

        new_column_names = {
                "Datetime":"Datetime",
                "Cumulative Bullishness":f'"Cumulative Bullishness "{Strike_Prices[i]}',
                "Cumulative SB call":f'"Cumulative SB call "{Strike_Prices[i]}',
                "Cumulative SB put":f'"Cumulative SB put "{Strike_Prices[i]}',
            # Add more columns as needed
            }
        
        new_df.rename(columns=new_column_names, inplace=True)

        df.append(new_df)

    merged_df = df[0]

    # Loop through the remaining dataframes and merge on 'Datetime'
    for df in df[1:]:
        merged_df = merged_df.merge(df, on='Datetime', how='inner')

    final_df=[]

    for i in range(len(Strike_Prices)):
        df_i = merged_df[["Datetime",f'"Cumulative Bullishness "{Strike_Prices[i]}',f'"Cumulative SB call "{Strike_Prices[i]}',f'"Cumulative SB put "{Strike_Prices[i]}']]

        new_column_names = {
                "Datetime":"Datetime",
                f'"Cumulative Bullishness "{Strike_Prices[i]}':"Cumulative Bullishness",
                f'"Cumulative SB call "{Strike_Prices[i]}':"Cumulative SB call",
                f'"Cumulative SB put "{Strike_Prices[i]}':"Cumulative SB put",
            # Add more columns as needed
            }
        
        df_i.rename(columns=new_column_names, inplace=True)

        final_df.append(df_i)

    return final_df



def comparision_build_up_CE(row):
        if ((row['COI CE'] > 0 and row['COP CE'] > 0)):
            return 'LB'
        elif ((row['COI CE'] < 0 and row['COP CE'] < 0)):
            return 'LC'
        elif ((row['COI CE'] > 0 and row['COP CE'] < 0)):
            return 'SB'
        elif ((row['COI CE'] < 0 and row['COP CE'] > 0)):
            return 'SC'
        else:
            pass


def comparision_build_up_PE(row):
        if ((row['COI PE'] > 0 and row['COP PE'] > 0)):
            return 'LB'
        elif ((row['COI PE'] < 0 and row['COP PE'] < 0)):
            return 'LC'
        elif ((row['COI PE'] > 0 and row['COP PE'] < 0)):
            return 'SB'
        elif ((row['COI PE'] < 0 and row['COP PE'] > 0)):
            return 'SC'
        else:
            pass



def update_figures(closing_price):
    global name
    # global axs1, axs2
    global specific_date
    global Strike_Prices

    # axs1[0].clear()
    # axs1[1].clear()
    # axs1[2].clear()
    axs2.clear()

    with open(path+"Call_put_quote_token.txt",'r') as file:
        content_strike_price=file.read()

    content_read=ast.literal_eval(content_strike_price)

    Strike_Prices=content_read['Strike Prices']
    token_CE=content_read['token_call']
    token_PE=content_read['token_put']




    import datetime


    for ii in range(len(Strike_Prices)):
        instrument_token_CE = token_CE[ii]
        instrument_token_PE = token_PE[ii]

        from_datetime = datetime.datetime.now() - datetime.timedelta(days=20)     # From last & days
        to_datetime = datetime.datetime.now()
        interval = "minute"
        content_CE=kite.historical_data(instrument_token_CE, from_datetime, to_datetime, interval, continuous=False, oi=True)
        content_PE=kite.historical_data(instrument_token_PE, from_datetime, to_datetime, interval, continuous=False, oi=True)

        Content_CE=str(content_CE)
        Content_PE=str(content_PE)

        cleaned_contents_CE = Content_CE.replace("datetime.datetime", "").replace(", tzinfo=tzoffset(None, 19800)", "")
        cleaned_contents_PE = Content_PE.replace("datetime.datetime", "").replace(", tzinfo=tzoffset(None, 19800)", "")

        data_CE = ast.literal_eval(cleaned_contents_CE)
        data_PE = ast.literal_eval(cleaned_contents_PE)

        df_CE = pd.DataFrame(data_CE)
        df_PE = pd.DataFrame(data_PE)

        df_CE['date'] = df_CE['date'].apply(lambda x: pd.Timestamp(year=x[0], month=x[1], day=x[2], hour=x[3], minute=x[4]))
        df_CE['Date'] = df_CE['date'].dt.strftime('%Y-%m-%d')
        df_CE['Time'] = df_CE['date'].dt.strftime('%H:%M')
        df_CE = df_CE.drop(columns=['date'])

        df_PE['date'] = df_PE['date'].apply(lambda x: pd.Timestamp(year=x[0], month=x[1], day=x[2], hour=x[3], minute=x[4]))
        df_PE['Date'] = df_PE['date'].dt.strftime('%Y-%m-%d')
        df_PE['Time'] = df_PE['date'].dt.strftime('%H:%M')
        df_PE = df_PE.drop(columns=['date'])

        df_CE = df_CE[['Date', 'Time', 'open', 'high', 'low', 'close','volume','oi']]
        df_PE = df_PE[['Date', 'Time', 'open', 'high', 'low', 'close','volume','oi']]

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

        df_CE.rename(columns=new_column_names_CE, inplace=True)
        df_PE.rename(columns=new_column_names_PE, inplace=True)


        merged_df = pd.merge(df_CE, df_PE, on=['Date', 'Time'], how='outer')
        merged_df['Time'] = pd.to_datetime(merged_df['Time'], format='%H:%M').dt.time
        merged_df.sort_values(by=['Date', 'Time'], inplace=True)
        merged_df.fillna(method='ffill', inplace=True)

        df_CE = merged_df[['Date', 'Time', 'open CE', 'high CE', 'low CE', 'close CE','volume CE','oi CE']]
        df_PE = merged_df[['Date', 'Time', 'open PE', 'high PE', 'low PE', 'close PE','volume PE','oi PE']]

        df_CE.loc[:,'Time'] = df_CE['Time'].astype(str).str[:5]
        df_PE.loc[:,'Time'] = df_PE['Time'].astype(str).str[:5]



        # print(type(df_CE.iloc[0,1]))

        # df_CE.to_csv(path+name+str(Strike_Prices[ii])+"_CE.csv",index=False)
        # df_PE.to_csv(path+name+str(Strike_Prices[ii])+"_PE.csv",index=False)

        rows_CE=df_CE.shape[0]
        rows_PE=df_PE.shape[0]

        df_CE["COI"]=0
        df_PE["COI"]=0

        df_CE["COP"]=0
        df_PE["COP"]=0

        for i in range(1,rows_CE):
            df_CE.iloc[i,8]=df_CE.iloc[i,7]-df_CE.iloc[(i-1),7]
            df_CE.iloc[i,9]=df_CE.iloc[i,5]-df_CE.iloc[(i-1),5]

        for i in range(1,rows_PE):
            df_PE.iloc[i,8]=df_PE.iloc[i,7]-df_PE.iloc[(i-1),7]
            df_PE.iloc[i,9]=df_PE.iloc[i,5]-df_PE.iloc[(i-1),5]

        date_list=date_time_computation()


        df_CE["Date"] = pd.to_datetime(df_CE["Date"])
        df_CE = df_CE[df_CE['Date'].dt.strftime('%Y-%m-%d').isin(date_list)]
        df_CE.reset_index(drop=True, inplace=True)

        df_PE["Date"] = pd.to_datetime(df_PE["Date"])
        df_PE = df_PE[df_PE['Date'].dt.strftime('%Y-%m-%d').isin(date_list)]
        df_PE.reset_index(drop=True, inplace=True)


        columns_to_remove_CE = ["open CE", "high CE", "low CE"]
        columns_to_remove_PE = ["open PE", "high PE", "low PE"]
        df_CE = df_CE.drop(columns=columns_to_remove_CE)
        df_PE = df_PE.drop(columns=columns_to_remove_PE)


        df_CE["Conclusion CE"]=0
        df_PE["Conclusion PE"]=0


        new_column_names_CE = {
        'COI': 'COI CE',
        "close": "close CE",
        "volume": "volume CE",
        "oi": "oi CE",
        "COP": "COP CE",
        # Add more columns as needed
        }
        new_column_names_PE = {
            'COI': 'COI PE',
            "close": "close PE",
            "volume": "volume PE",
            "oi": "oi PE",
            "COP": "COP PE",
            # Add more columns as needed
        }

        df_CE.rename(columns=new_column_names_CE, inplace=True)
        df_PE.rename(columns=new_column_names_PE, inplace=True)

    #     # df_CE.to_csv(path+name+str(Strike_Prices[ii])+"_CE.csv",index=False)
    #     # df_PE.to_csv(path+name+str(Strike_Prices[ii])+"_PE.csv",index=False)

        columns_to_remove = ["Date", "Time"]
        df_PE = df_PE.drop(columns=columns_to_remove)



        finial_file = pd.concat([df_CE, df_PE], axis=1)
        finial_file=finial_file[(finial_file["COI CE"] != 0) | (finial_file["COI PE"] != 0)]
        finial_file.fillna(0,inplace=True)

        finial_file.reset_index(drop=True, inplace=True)

        rows_total=finial_file.shape[0]

        for j in range(1,rows_total):
            finial_file.iloc[j,6]=finial_file.iloc[j,2]-finial_file.iloc[(j-1),2]
            finial_file.iloc[j,12]=finial_file.iloc[j,8]-finial_file.iloc[(j-1),8]

        finial_file["Conclusion CE"]=finial_file.apply(comparision_build_up_CE,axis=1)
        finial_file["Conclusion PE"]=finial_file.apply(comparision_build_up_PE,axis=1)



        finial_file["Bullishness CE"]=finial_file.apply(comparision_CE,axis=1)
        finial_file["Bullishness PE"]=finial_file.apply(comparision_PE,axis=1)

        finial_file["Bullishness CE"]=finial_file["Bullishness CE"]*finial_file["COI CE"]
        finial_file["Bullishness PE"]=finial_file["Bullishness PE"]*finial_file["COI PE"]
        finial_file["Over All Bullishness"]=finial_file["Bullishness CE"]+finial_file["Bullishness PE"]

        
        row_final=finial_file.shape[0]
        
        finial_file.fillna(0, inplace=True)
        finial_file["Cumulative Bullishness"]=0
        finial_file.iloc[0,17]=finial_file.iloc[0,16]
        for i in range(1,row_final):
            finial_file.iloc[i,17]=finial_file.iloc[i,16]+finial_file.iloc[(i-1),17]


        finial_file['LB CE'] = finial_file.apply(lambda row: row['COI CE'] if row['Conclusion CE'] == 'LB' else None, axis=1)
        finial_file['SB CE'] = finial_file.apply(lambda row: row['COI CE'] if row['Conclusion CE'] == 'SB' else None, axis=1)
        finial_file['LC CE'] = finial_file.apply(lambda row: row['COI CE'] if row['Conclusion CE'] == 'LC' else None, axis=1)
        finial_file['SC CE'] = finial_file.apply(lambda row: row['COI CE'] if row['Conclusion CE'] == 'SC' else None, axis=1)

        finial_file['LB PE'] = finial_file.apply(lambda row: row['COI PE'] if row['Conclusion PE'] == 'LB' else None, axis=1)
        finial_file['SB PE'] = finial_file.apply(lambda row: row['COI PE'] if row['Conclusion PE'] == 'SB' else None, axis=1)
        finial_file['LC PE'] = finial_file.apply(lambda row: row['COI PE'] if row['Conclusion PE'] == 'LC' else None, axis=1)
        finial_file['SC PE'] = finial_file.apply(lambda row: row['COI PE'] if row['Conclusion PE'] == 'SC' else None, axis=1)

        finial_file = finial_file.fillna(0)

        finial_file["Net_SB_call"]=finial_file['SB CE']+finial_file['SC CE']
        finial_file["Net_SB_put"]=finial_file['SB PE']+finial_file['SC PE']

        finial_file["Cumulative SB call"]=0
        rows1=finial_file.shape[0]
        finial_file.iloc[0,28]=finial_file.iloc[0,26]
        for i in range(1,rows1):
            finial_file.iloc[i,28]=finial_file.iloc[i,26]+finial_file.iloc[(i-1),28]


        finial_file["Cumulative SB put"]=0
        rows2=finial_file.shape[0]
        finial_file.iloc[0,29]=finial_file.iloc[0,27]
        for i in range(1,rows2):
            finial_file.iloc[i,29]=finial_file.iloc[i,27]+finial_file.iloc[(i-1),29]



        finial_file.to_csv(path+name+str(Strike_Prices[ii])+".csv",index=False)


    for mm in range(len(Strike_Prices)):

        finial_file=pd.read_csv(path+name+str(Strike_Prices[mm])+".csv")
        index_with_zero = finial_file[finial_file['Over All Bullishness'] == 0].index.tolist()
        for kk in index_with_zero:
            if (finial_file.iloc[kk,14]==0 and finial_file.iloc[kk,15]==0):
                pass
            else:
                finial_file.iloc[kk,16]=finial_file.iloc[kk,14]+finial_file.iloc[kk,15]

        row_final=finial_file.shape[0]
        
        finial_file.fillna(0, inplace=True)
        finial_file["Cumulative Bullishness"]=0
        finial_file.iloc[0,17]=finial_file.iloc[0,16]
        for i in range(1,row_final):
            finial_file.iloc[i,17]=finial_file.iloc[i,16]+finial_file.iloc[(i-1),17]


        date_list=date_time_computation()
        finial_file['Date'] = pd.to_datetime(finial_file['Date'])
        finial_file = finial_file[finial_file['Date'].dt.strftime('%Y-%m-%d').isin(date_list)]
        finial_file.reset_index(drop=True, inplace=True)

        finial_file['Date'] = pd.to_datetime(finial_file['Date']).dt.strftime('%d-%m')
        finial_file['Datetime'] = finial_file['Date'] + ': ' + finial_file['Time']
        finial_file.drop(['Date', 'Time'], axis=1, inplace=True)
        cols = list(finial_file.columns)
        cols = ['Datetime'] + [col for col in cols if col != 'Datetime']
        finial_file = finial_file[cols]

        finial_file.to_csv(path+name+str(Strike_Prices[mm])+".csv",index=False)


    final_df=data_frame_list_generation(Strike_Prices)

    xox=0
    for data_frame in final_df:
        data_frame['Cumulative Bullishness'] /= 100000
        axs2.plot(data_frame['Datetime'], data_frame['Cumulative Bullishness'], marker='o', label=str(Strike_Prices[xox]))
        xox=xox+1

    axs2.set_xlabel('Datetime')
    axs2.set_ylabel('Cumulative Bullishness by sellers (in Lakhs)')
    axs2.set_title('Bulleshness Contracts by sellers in Lakhs')
    axs2.grid(True)

    axs2.legend()
    plt.xticks(rotation=90)
    plt.tight_layout()

    canvas1.draw()

def Plot():

    nifty_price=float(entry.get())
    strike_update(expiry_date,name,nifty_price)

    update_figures(nifty_price)


def on_mousewheel(event):
    canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

def zoom_in(event):
    global axs2
    xmin, xmax = axs2.get_xlim()
    ymin, ymax = axs2.get_ylim()
    x_center = (xmin + xmax) / 2
    y_center = (ymin + ymax) / 2
    axs2.set_xlim(xmin + (xmax - xmin) * 0.1, xmax - (xmax - xmin) * 0.1)
    axs2.set_ylim(ymin + (ymax - ymin) * 0.1, ymax - (ymax - ymin) * 0.1)
    canvas1.draw()

def zoom_out(event):
    global axs2
    xmin, xmax = axs2.get_xlim()
    ymin, ymax = axs2.get_ylim()
    x_center = (xmin + xmax) / 2
    y_center = (ymin + ymax) / 2
    axs2.set_xlim(xmin - (xmax - xmin) * 0.1, xmax + (xmax - xmin) * 0.1)
    axs2.set_ylim(ymin - (ymax - ymin) * 0.1, ymax + (ymax - ymin) * 0.1)
    canvas1.draw()


def move_left(event):
    global axs2
    xmin, xmax = axs2.get_xlim()
    x_range = xmax - xmin
    axs2.set_xlim(xmin - x_range * 0.1, xmax - x_range * 0.1)
    canvas1.draw()

def move_right(event):
    xmin, xmax = axs2.get_xlim()
    x_range = xmax - xmin
    axs2.set_xlim(xmin + x_range * 0.1, xmax + x_range * 0.1)
    canvas1.draw()

def create_plot(frame3):
    global canvas2, axes
    
    fig, axes = plt.subplots(3, 1, figsize=(100, 10))

    canvas2 = FigureCanvasTkAgg(fig, master=frame3)
    canvas2.draw()
    canvas2.get_tk_widget().pack()

    return canvas2, axes

def update_figure_2(new_Window2):
    
    global canvas2
    global axes
    global Strike_Prices


    df=data_frame_list_generation(Strike_Prices)


    for i, df in enumerate(df):
        ax = axes[i]
        ax.plot(df['Datetime'], df['Cumulative SB call']/100000, marker='o', linestyle='-', color='red', label=f'Call SB: {Strike_Prices[i]}')
        ax.plot(df['Datetime'], df['Cumulative SB put']/100000, marker='o', linestyle='-', color='green', label=f'Put SB: {Strike_Prices[i]}')
        ax.set_xlabel('Datetime')
        ax.set_ylabel('Cumulative SB call(in Lakhs)')
        ax.legend()
        ax.tick_params(axis='x', rotation=90)

    plt.tight_layout()

    canvas2.draw()

    print("Updated new window")


def Open_window_1_over_all():
    global Strike_Prices

    new_Window=Toplevel(root)
    new_Window.title("Over All Bullishness")

    scrollable_frame = ttk.Frame(new_Window)
    scrollable_frame.pack(fill="both", expand=True)

    canvas = Canvas(scrollable_frame)
    canvas.pack(side="left", fill="both", expand=True)

    scrollbar_y = ttk.Scrollbar(scrollable_frame, orient="vertical", command=canvas.yview)
    scrollbar_y.pack(side="right", fill="y")
    canvas.configure(yscrollcommand=scrollbar_y.set)

    scrollbar_x = ttk.Scrollbar(new_Window, orient="horizontal", command=canvas.xview)
    scrollbar_x.pack(fill="x")
    canvas.configure(xscrollcommand=scrollbar_x.set)

    canvas.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    scrollable_content = ttk.Frame(canvas)
    canvas.create_window((0, 0), window=scrollable_content, anchor="nw")

    frame3 = ttk.Frame(scrollable_content)
    frame3.pack(fill="both", expand=True)

    canvas2, axes = create_plot(frame3)


    update_figure_2(new_Window)


    menubar = Menu(new_Window)
    new_Window.config(menu=menubar)
    menubar.add_command(label="Back to Main Window", command=new_Window.destroy)

    frame4=Frame(new_Window)
    frame4.pack(anchor='nw')



    toolbar_frame4 = ttk.Frame(frame4)  # New frame for toolbar
    toolbar_frame4.pack(anchor="nw")   # Place it at top right corner

    toolbar2 = create_toolbar(canvas2, toolbar_frame4)

global specific_date
global weekday_dates
global Strike_Prices

path="D:/ashu/Finance/algo_trading/Zerodha_GUI/Non_Intraday_OI_Data_Collected/"


path_main="D:/ashu/Finance/algo_trading/Zerodha_GUI/Kite_Zerodha-main/Kite_Zerodha-main/"

df=pd.read_csv(path_main+"Enctoke_Expiry_month_end_info.csv")
content_enctoken=df.iloc[0,0]

enctoken = content_enctoken

kite = KiteApp(enctoken=enctoken)

import datetime

with open(path_main+"expiry_date.txt",'r') as file:
    content_expiry_date=file.read()


########################################################## All Update Here #############################################################
    
segment=["NIFTY","FINNIFTY","BANKNIFTY","MIDCPNIFTY","SENSEX"]
instrument=["NIFTY 50","NIFTY BANK","NIFTY FIN SERVICE","NIFTY MID SELECT","SENSEX"]

expiry_days=["15-Feb-2024","09-Jan-2024","10-Jan-2024","08-Jan-2024","12-Jan-2024"]

expiry_date=expiry_days[0]
name=segment[0]
instrument_name=instrument[0]
# expiry=df.iloc[0,1]
expiry=content_expiry_date
Month_end=df.iloc[0,2]
# nifty_current_price=kite.ltp(["NSE:NIFTY 50"])
# Nifty_current_price=nifty_current_price['NSE:NIFTY 50']['last_price']
# closing_price=Nifty_current_price

if instrument=="SENSEX":
    Sensex_current_price=kite.ltp([f"BSE:{instrument_name}"])
    closing_price=Sensex_current_price[f'BSE:{instrument_name}']['last_price']
else:
    nse_current_price=kite.ltp([f"NSE:{instrument_name}"])
    closing_price=nse_current_price[f'NSE:{instrument_name}']['last_price']

strike_update(expiry_date,name,closing_price)

############################################## Tkinter GUI ########################################


root = Tk()
root.title("Matplotlib in Tkinter with Scrollbars")

scrollable_frame = ttk.Frame(root)
scrollable_frame.pack(fill="both", expand=True)

canvas = Canvas(scrollable_frame)
canvas.pack(side="left", fill="both", expand=True)

scrollbar_y = ttk.Scrollbar(scrollable_frame, orient="vertical", command=canvas.yview)
scrollbar_y.pack(side="right", fill="y")
canvas.configure(yscrollcommand=scrollbar_y.set)

scrollbar_x = ttk.Scrollbar(root, orient="horizontal", command=canvas.xview)
scrollbar_x.pack(fill="x")
canvas.configure(xscrollcommand=scrollbar_x.set)

canvas.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

scrollable_content = ttk.Frame(canvas)
canvas.create_window((0, 0), window=scrollable_content, anchor="nw")

frame1 = ttk.Frame(scrollable_content)
frame1.pack(fill="both", expand=True)

fig1, axs2 = plt.subplots(nrows=1, ncols=1, figsize=(100, 9))

canvas1 = FigureCanvasTkAgg(fig1, master=frame1)
canvas1.draw()
canvas1.get_tk_widget().pack()


frame2=Frame(root)
frame2.pack(anchor='nw')

l1=Label(frame2,text="Enter Nifty Price")
l1.pack()

entry = Entry(frame2)
entry.pack()

plotting_button=Button(frame2,text='Plot',command=Plot)
plotting_button.pack()

toolbar_frame1 = ttk.Frame(frame2)  # New frame for toolbar
toolbar_frame1.pack(anchor="ne")   # Place it at top right corner

toolbar1 = create_toolbar(canvas1, toolbar_frame1)

update_figures(closing_price)


menubar = Menu(root)

# Create a "File" menu
file_menu = Menu(menubar, tearoff=0)

menubar.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="Overall Buildup Intraday", command=Open_window_1_over_all)

root.config(menu=menubar)


root.bind("<KeyPress-z>", zoom_in)  # Press "z" to zoom in
root.bind("<KeyPress-x>", zoom_out)  # Press "x" to zoom out
root.bind("<Left>", move_left)  # Press the left arrow key to move left
root.bind("<Right>", move_right)

root.bind("<MouseWheel>", on_mousewheel)

root.mainloop()