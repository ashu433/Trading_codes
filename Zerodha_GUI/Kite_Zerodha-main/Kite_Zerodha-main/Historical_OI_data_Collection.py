import datetime
from kite_trade import *
import pandas as pd
import ast
import Intraday_live_data
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np




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


import datetime

path_main="D:/ashu/Finance/algo_trading/Zerodha_GUI/Kite_Zerodha-main/Kite_Zerodha-main/"

path="D:/ashu/Finance/algo_trading/Zerodha_GUI/OI_Raw_Data_Collected/"

with open(path_main+"Enctoken.txt",'r') as file:
    content_enctoken=file.read()

enctoken = content_enctoken

color_ce_list=[]
color_pe_list=[]

kite = KiteApp(enctoken=enctoken)


Closing_price=19650


with open(path_main+"Expiry_Day.txt",'r') as file:
    content_expiry_day=file.read()

name="NIFTY"
expiry=content_expiry_day

final_new=Intraday_live_data.getoptionchain(name,expiry)
final_new.reset_index(drop=True, inplace=True)

index = (final_new['strikePrice'] - Closing_price).abs().idxmin()
ATM_Strike_Price=final_new['strikePrice'].iloc[index]
ATM_Strike_Price_Plus_1=ATM_Strike_Price+50
ATM_Strike_Price_Minus_1=ATM_Strike_Price-50
ATM_Strike_Price_Plus_2=ATM_Strike_Price+100
ATM_Strike_Price_Minus_2=ATM_Strike_Price-100
ATM_Strike_Price_Plus_3=ATM_Strike_Price+150
ATM_Strike_Price_Minus_3=ATM_Strike_Price-150
ATM_Strike_Price_Plus_4=ATM_Strike_Price+200
ATM_Strike_Price_Minus_4=ATM_Strike_Price-200
ATM_Strike_Price_Plus_5=ATM_Strike_Price+250
ATM_Strike_Price_Minus_5=ATM_Strike_Price-250

Strike_Prices=[ATM_Strike_Price_Minus_5,ATM_Strike_Price_Minus_4,ATM_Strike_Price_Minus_3,ATM_Strike_Price_Minus_2,ATM_Strike_Price_Minus_1,ATM_Strike_Price,ATM_Strike_Price_Plus_1,ATM_Strike_Price_Plus_2,ATM_Strike_Price_Plus_3,ATM_Strike_Price_Plus_4,ATM_Strike_Price_Plus_5]
print(Strike_Prices)

call_list=[]
put_list=[]
token_CE=[]
token_PE=[]

from datetime import datetime

parsed_date = datetime.strptime(expiry, '%d-%b-%Y')
formatted_date = parsed_date.strftime('%Y%b').upper()
name="NIFTY"


formatted_date=formatted_date[2:]

for i in range(len(Strike_Prices)):
    quote_CE=name+formatted_date+str(Strike_Prices[i])+"CE"
    quote_PE=name+formatted_date+str(Strike_Prices[i])+"PE"
    call_list.append(quote_CE)
    put_list.append(quote_PE)

print(call_list)
print(put_list)

for i in range(len(Strike_Prices)):
    atm_token_ce=kite.ltp("NFO:"+call_list[i])
    ATM_Token_CE=atm_token_ce["NFO:"+call_list[i]]['instrument_token']

    atm_token_pe=kite.ltp("NFO:"+put_list[i])
    ATM_Token_PE=atm_token_pe["NFO:"+put_list[i]]['instrument_token']

    token_CE.append(ATM_Token_CE)
    token_PE.append(ATM_Token_PE)



print(token_CE)
print(token_PE)

import datetime

for ii in range(len(Strike_Prices)):
    instrument_token_CE = token_CE[ii]
    instrument_token_PE = token_PE[ii]

    from_datetime = datetime.datetime.now() - datetime.timedelta(days=8)     # From last & days
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


    columns_to_remove = ["open", "high", "low"]
    df_CE = df_CE.drop(columns=columns_to_remove)
    df_PE = df_PE.drop(columns=columns_to_remove)

    df_CE["Conclusion CE"]=df_CE.apply(comparision,axis=1)
    df_PE["Conclusion PE"]=df_PE.apply(comparision,axis=1)

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

    columns_to_remove = ["Date", "Time"]
    df_PE = df_PE.drop(columns=columns_to_remove)

    finial_file = pd.concat([df_CE, df_PE], axis=1)
    finial_file=finial_file[(finial_file["COI CE"] != 0) | (finial_file["COI PE"] != 0)]
    finial_file=finial_file.fillna(0)

    color_map_ce = {
    'SB': 'red',
    'LC': 'red',
    'LB': 'green',
    'SC': 'green',
    None: "black",
    0:"grey"
    }

    color_map_pe = {
        'LB': 'red',
        'SC': 'red',
        'SB': 'green',
        'LC': 'green',
        None: "black",
        0:"grey"
    }

    color_ce=[color_map_ce[conclusion] for conclusion in finial_file['Conclusion CE']]
    color_pe=[color_map_pe[conclusion] for conclusion in finial_file['Conclusion PE']]

    color_ce_list.append(color_ce)
    color_pe_list.append(color_pe)



    finial_file["Bullishness CE"]=finial_file.apply(comparision_CE,axis=1)
    finial_file["Bullishness PE"]=finial_file.apply(comparision_PE,axis=1)

    finial_file["Bullishness CE"]=finial_file["Bullishness CE"]*finial_file["COI CE"]
    finial_file["Bullishness PE"]=finial_file["Bullishness PE"]*finial_file["COI PE"]
    finial_file["Over All Bullishness"]=finial_file["Bullishness CE"]+finial_file["Bullishness PE"]
    finial_file.reset_index(drop=True, inplace=True)
    row_final=finial_file.shape[0]
    finial_file.fillna(0, inplace=True)
    finial_file["Cumulative Bullishness"]=0
    finial_file.iloc[0,17]=finial_file.iloc[0,16]
    for i in range(1,row_final):
        finial_file.iloc[i,17]=finial_file.iloc[i,16]+finial_file.iloc[(i-1),17]

    finial_file.to_csv(path+name+str(Strike_Prices[ii])+".csv",index=False)
