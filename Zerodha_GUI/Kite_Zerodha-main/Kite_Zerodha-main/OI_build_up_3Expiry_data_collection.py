import datetime
from kite_trade import *
import pandas as pd
import ast
import Intraday_live_data
import matplotlib.pyplot as plt
import numpy as np
import warnings


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



def update_figures():
    global name
    global specific_date
    global Strike_Prices
    global run_overall

    with open(path_strike_price+"Call_put_quote_token.txt",'r') as file:
        content_strike_price=file.read()

    content_read=ast.literal_eval(content_strike_price)

    Strike_Prices=content_read['Strike Prices']
    token_CE=content_read['token_call']
    token_PE=content_read['token_put']

    warnings.filterwarnings("ignore")

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

    current_time = datetime.datetime.now().time()
    print(f"the current time is {current_time}")

    current_datetime = datetime.datetime.now()
    delayed_datetime = current_datetime - datetime.timedelta(minutes=1)
    delayed_time = delayed_datetime.strftime('%H:%M')

    delayed_time=str(delayed_time)
    today_date = datetime.date.today()
    date_month_format = today_date.strftime('%d-%m')
    date_time=f"{date_month_format}: {delayed_time}"

    final_file1=pd.read_csv(path+name+str(Strike_Prices[0])+".csv")
    rows_delay=final_file1.shape[0]
    time_last=final_file1.iloc[rows_delay-1,1]

    print(f"Updating update figure {run_overall} times")
    run_overall=run_overall+1

    # if time_last==date_time:
    #     schedule_next_execution()
    # else:
    #     update_figures()



    schedule_next_execution()


def schedule_next_execution():
    import time
    global time_list
    global expiry
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
        print(time_difference)
        time.sleep(int(time_difference))
        update_figures()
        
    else:
        # No more times in the list for today, you can handle this case as needed
        print("No more times to execute today")

def strip_until_number(input_str):
    for i, char in enumerate(input_str):
        if char.isdigit():
            return input_str[:i]



global specific_date
global weekday_dates
global Strike_Prices

path="D:/ashu/Finance/algo_trading/Zerodha_GUI/Non_Intraday_OI_Data_Collected/"
path_strike_price="D:/ashu/Finance/algo_trading/Zerodha_GUI/OI_Raw_Data_Collected/"


path_main="D:/ashu/Finance/algo_trading/Zerodha_GUI/Kite_Zerodha-main/Kite_Zerodha-main/"


        




df=pd.read_csv(path_main+"Enctoke_Expiry_month_end_info.csv")
content_enctoken=df.iloc[0,0]

enctoken = content_enctoken

kite = KiteApp(enctoken=enctoken)

import datetime

with open(path_main+"expiry_date.txt",'r') as file:
    content_expiry_date=file.read()


content_expiry_day=content_expiry_date

########################################################## All Update Here #############################################################

with open(path_strike_price+"Call_put_quote_token.txt",'r') as file:
    content_strike_price=file.read()

content_read=ast.literal_eval(content_strike_price)

Quote=content_read['quote_call'][0]

result = strip_until_number(Quote)


name=str(result)

expiry=content_expiry_day
run=0

run_overall=0

#######################################################  Time List Computation #################################################
from datetime import datetime, timedelta

# Define the start and end times
start_time = datetime.strptime("9:15:00", "%H:%M:%S")
end_time = datetime.strptime("15:30:00", "%H:%M:%S")

# Define the interval (3 minutes)
interval = timedelta(minutes=3)

# Initialize an empty list to store the generated times
time_list = []

# Generate the times
current_time = start_time
while current_time <= end_time:
    time_list.append(current_time.strftime("%H:%M:%S"))
    current_time += interval

#######################################################  Time List Computation #################################################

update_figures()