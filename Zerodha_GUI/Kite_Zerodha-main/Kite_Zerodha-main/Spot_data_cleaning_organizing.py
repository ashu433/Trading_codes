import os
import pandas as pd

# Specify the directory path
directory_path = 'D:/ashu/Finance/algo_trading/Option_chain_data/'
path_main="D:/ashu/Finance/algo_trading/Zerodha_GUI/Kite_Zerodha-main/Kite_Zerodha-main/"

# Get all file names in the directory
file_names = os.listdir(directory_path)

# Filter out only the CSV files
csv_files = [file for file in file_names if file.endswith('.csv')]

def file_cleaning(file_name):
    df=pd.read_csv(directory_path+file_name)
    # df=df.drop(columns="MA ‌ma‌ (21,ema,0)")
    # df=df.drop(columns="MA ‌ma‌ (9,ema,0)")
    # df=df.drop(columns="MA ‌ma‌ (200,ma,0)")
    # df=df.drop(columns="MA ‌ma‌ (50,ma,0)")
    df['Date'] = df['Date'].str.replace('GMT+0530 (India Standard Time)', '', regex=False)
    tot = df['Date'].str.split(expand=True)
    df=df.drop(columns="Date")
    tot=tot.drop(columns=0)
    tot.rename(columns={4: 'Time'}, inplace=True)
    tot['Date'] = tot[2] + '-' + tot[1].str[:3] + '-' + tot[3]
    tot=tot.drop(columns=1)
    tot=tot.drop(columns=2)
    tot=tot.drop(columns=3)
    tot=tot[['Date', 'Time']]
    tot['Date'] = pd.to_datetime(tot['Date'])
    tot['Date'] = tot['Date'].dt.strftime('%d-%m-%Y')
    final_data=pd.concat([tot, df], axis=1)
    final_data['Time'] = final_data['Time'].str.replace(r':\d{2}$', '', regex=True)

    return final_data

output_file=file_cleaning(csv_files[0])
output_file.to_csv(path_main+"Nifty_daily_data.csv",index=False)


for i in range(1,len(csv_files)):
    data_new=file_cleaning(csv_files[i])
    data_old=pd.read_csv(path_main+"Nifty_daily_data.csv")
    merged = pd.merge(data_old,data_new, how='outer', indicator=False)
    merged.to_csv(path_main+"Nifty_daily_data.csv",index=False)
    print(f"Current file number {i}")