import Intraday_live_data
import pandas as pd
import time
from datetime import  timedelta, datetime
import schedule
import matplotlib.pyplot as plt
from tkinter import Tk
import threading
from matplotlib.animation import FuncAnimation
from itertools import count


path="D:/ashu/Finance/algo_trading/Option_chain_data/"

def live_OI_data_computing():

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

    name="NIFTY"
    expiry="22-Jun-2023"

    Option_chain=Intraday_live_data.getoptionchain(name,expiry)
    Option_chain.reset_index(drop=True, inplace=True)
    Nifty_current_price=Option_chain["Nifty Current Price"].iloc[1]

    index = (Option_chain['strikePrice'] - Nifty_current_price).abs().idxmin()
    near_option_ATM=Option_chain.iloc[index]
    near_option_ATM_1_Plus=Option_chain.iloc[index+1]
    near_option_ATM_1_minus=Option_chain.iloc[index-1]
    near_option_ATM_2_Plus=Option_chain.iloc[index+2]
    near_option_ATM_2_minus=Option_chain.iloc[index-2]
    near_option_ATM_3_Plus=Option_chain.iloc[index+3]
    near_option_ATM_3_minus=Option_chain.iloc[index-3]
    new=pd.concat([near_option_ATM_3_minus,near_option_ATM_2_minus,near_option_ATM_1_minus,near_option_ATM,near_option_ATM_1_Plus,near_option_ATM_2_Plus,near_option_ATM_3_Plus],axis=1)
    final_new=new.T
    COI_by_Volume_Call = 50 * final_new["CE_CHNG_IN_OI"] / final_new["CE_Volume"]
    final_new = pd.concat([final_new, pd.DataFrame(COI_by_Volume_Call)], axis=1)
    final_new = final_new.rename(columns={0: "COI_by_Volume_Call"})
    COI_by_Volume_Put = 50 * (final_new["PE_CHNG_IN_OI"] / final_new["PE_Volume"])
    final_new = pd.concat([final_new, pd.DataFrame(COI_by_Volume_Put)], axis=1)
    final_new = final_new.rename(columns={0: "COI_by_Volume_Put"})
    final_new.insert(0, "Time", formatted_time)
    final_new.iloc[0:7, 0] = formatted_time
    return final_new

def file_appending():
    # path="D:/ashu/Finance/algo_trading/Option_chain_data/"
    global path
    present_data=live_OI_data_computing()
    old_data=pd.read_csv(path+'Option_chain_data_saving.csv')
    finial_file = pd.concat([old_data, present_data], axis=0)
    finial_file.to_csv(path+'Option_chain_data_saving.csv', index=False)




def running():
    print(5)
    schedule.every(5).minutes.until(timedelta(hours=6)).do(file_appending)

    while True:
        schedule.run_pending()
        time.sleep(1)


initial_data=live_OI_data_computing()

initial_data.to_csv(path+'Option_chain_data_saving.csv', index=False)

running()


