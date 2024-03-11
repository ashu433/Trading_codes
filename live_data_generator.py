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
import requests
import Option_chain_live_data_saving
from multiprocessing import Process, freeze_support


path="D:/ashu/Finance/algo_trading/Option_chain_data/"
MAX_ATTEMPTS=50
DELAY_BETWEEN_ATTEMPTS = 5

def live_OI_data_computing():

    global path

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
    expiry="27-Jul-2023"

    final_new=Intraday_live_data.getoptionchain(name,expiry)
    final_new.reset_index(drop=True, inplace=True)
    final_new=final_new.fillna(0)
    COI_by_Volume_Call = 50 * final_new["CE_CHNG_IN_OI"] / final_new["CE_Volume"]
    final_new = pd.concat([final_new, pd.DataFrame(COI_by_Volume_Call)], axis=1)
    final_new = final_new.rename(columns={0: "COI_by_Volume_Call"})
    COI_by_Volume_Put = 50 * (final_new["PE_CHNG_IN_OI"] / final_new["PE_Volume"])
    final_new = pd.concat([final_new, pd.DataFrame(COI_by_Volume_Put)], axis=1)
    final_new = final_new.rename(columns={0: "COI_by_Volume_Put"})
    final_new.insert(0, "Time", formatted_time)
    final_new.iloc[:, 0] = formatted_time
    return final_new


def file_appending():
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




def make_request_again():
    global path
    attempt = 1
    while attempt <= MAX_ATTEMPTS:
        try:
            print(3)
            running()
        except (requests.exceptions.RequestException, requests.exceptions.HTTPError) as e:
            print(4)
            print(f"Attempt {attempt} failed: {e}")
            attempt += 1
            time.sleep(DELAY_BETWEEN_ATTEMPTS)


    
    # If the maximum number of attempts is reached without a successful response, raise an exception
    raise Exception("Maximum number of attempts reached without a successful response")


 
############### Please Update the K if there is any Intrupption so that Old OI data is retained for the day #####################################
def live_csv_creation():
    try:
        k=1
        if k==1:
            print(1)
            initial_data=live_OI_data_computing()
            initial_data.to_csv(path+'Option_chain_data_saving.csv', index=False)
            make_request_again()    
        else:
            make_request_again()

    except Exception as e:
        print(f"Error occurred: {e}")



def data_saving():
    Option_chain_live_data_saving.OI_data_collection()

thread_1 = threading.Thread(target=live_csv_creation)
thread_2 = threading.Thread(target=data_saving)

# Start both threads
thread_1.start()
thread_2.start()

thread_1.join()
thread_2.join() 

