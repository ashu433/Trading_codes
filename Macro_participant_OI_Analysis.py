import flie_sorting_option_chain
import senitment_estimator
import csv

# date="10"
# month_file="Oct"
# month_in_words="Oct"
# month_in_numbers="10"
# year=2023
# closing_price=19664.70
# number_of_rows=75


# # flie_sorting_option_chain.file_sorting_of_Option_chain(date,month_in_words,month_in_numbers,year,number_of_rows,closing_price)

# senitment_estimator.sentiment_participants(date,month_in_words,month_in_numbers,year,closing_price,month_file)




########################### CSV File Saving #########################

import requests
import pandas as pd
import time
import matplotlib.pyplot as plt
import json


    

# sesi=requests.Session()
# headers={}
# headers['user-agent']='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
# a=sesi.get("https://www.nseindia.com/",headers=headers,timeout=20)

# url="https://nsearchives.nseindia.com/content/historical/DERIVATIVES/2024/FEB/fo14FEB2024bhav.csv.zip"


# file_path = "D:/ashu/Finance/algo_trading/Option_chain_data/data.txt"


# a=sesi.get(url,headers=headers)

# print(a)

# with open(file_path, 'wb') as file:
#     file.write(a.content)

sesi = requests.Session()
headers = {}
headers['user-agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'

# Request to the URL
a = sesi.get("https://www.nseindia.com/", headers=headers, timeout=20)

url = "https://nsearchives.nseindia.com/content/historical/DERIVATIVES/2024/FEB/fo14FEB2024bhav.csv.zip"

# Make a request to the CSV URL
response = sesi.get(url, headers=headers)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Specify the file path for the CSV file
    file_path = "D:/ashu/Finance/algo_trading/Option_chain_data/fo14FEB2024bhav.csv"

    # Write the content of the response to the CSV file
    with open(file_path, 'wb') as file:
        file.write(response.content)

    # Read the CSV file into a DataFrame
    df = pd.read_csv(file_path, encoding='ISO-8859-1')

    # Now you can work with the DataFrame 'df'
    print(df.head())
else:
    print("Failed to retrieve data. Status code:", response.status_code)
