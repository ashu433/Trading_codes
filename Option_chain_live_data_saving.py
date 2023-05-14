import Intraday_live_data
import pandas as pd
import matplotlib.pyplot as plt
from openpyxl import load_workbook
from openpyxl.utils.dataframe import dataframe_to_rows
import schedule
import time 
from datetime import  timedelta, datetime

i=0
# scripname="NIFTY"
# Expiry_DATE="11-May-2023"
# Option_chain=Intraday_live_data.getoptionchain(scripname,Expiry_DATE)
# Option_chain.to_excel('data.xlsx', index=False)

def loading_data(book,ws,script,expiry_date):

    #######################stocks and the index computation###############################################

    # stocks_and_index=["NIFTY","BANKNIFTY"]


    ################## Time Computation ########################

    current_time = time.strftime("%H:%M:%S")

    # Convert the 24-hour format to 12-hour format with AM/PM
    time_parts = current_time.split(":")
    hours = int(time_parts[0])
    minutes = int(time_parts[1])
    seconds = int(time_parts[2])
    if hours >= 12:
        suffix = "PM"
        hours -= 12
    else:
        suffix = "AM"
    if hours == 0:
        hours = 12
    formatted_time = "{:02d}:{:02d}:{:02d} {}".format(hours, minutes, seconds, suffix)

    print(formatted_time)


    # Print the current time in 12-hour format with AM/PM

    #########Loading Option chain data#######################
    # book = load_workbook('data.xlsx')
    # ws = book['Sheet1']


    # new_sheet_name = 'NewSheetName'
    # ws.title = new_sheet_name


    new_data = {'Name': ["OI_Data",""], 'Time': [f"{formatted_time}",""], 'Interval': ["15 Mins",""]}
    df = pd.DataFrame(new_data)
    scripname=script
    Expiry_DATE=expiry_date
    Option_chain=Intraday_live_data.getoptionchain(scripname,Expiry_DATE)
    df_1=Option_chain
    # Write the new data to the sheet
    for r in dataframe_to_rows(df, index=False, header=True):
        ws.append(r)

    for r in dataframe_to_rows(df_1, index=False, header=True):
        ws.append(r)

    # Save the Excel file
    book.save('data.xlsx')





def calling():

    global i

    index=["NIFTY","BANKNIFTY"]
    expiry="11-May-2023"

    if i<1:

        i=i+1
        book = load_workbook('data.xlsx')

        for k in range(1,(len(index)+1)):

            ws = book['Sheet{k}'.format(k=k)]
            new_sheet_name =index[-k]
            ws.title = new_sheet_name
            loading_data(book,ws,index[-k],expiry)

    else:

        for k in range(1,(len(index)+1)):

            book = load_workbook('data.xlsx')
            ws = book[index[-k]]
            loading_data(book,ws,index[-k],expiry)


schedule.every(5).minutes.until(timedelta(hours=5)).do(calling)

while True:
    schedule.run_pending()
    time.sleep(1)
