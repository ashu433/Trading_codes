from maticalgos.historical import historical
import pandas as pd
import datetime
import os

ma = historical('ashud43317@gmail.com')
ma.login("642911")
path_main="D:/ashu/Finance/algo_trading/Zerodha_GUI/Kite_Zerodha-main/Kite_Zerodha-main/"
path_index="D:/ashu/Finance/Daily_F_O_data/Options/Index/"
path_stocks_path="D:/ashu/Finance/Daily_F_O_data/Options/Stocks/"

def get_data(date,end_date):
    INSTRUMENT="NIFTY"
    
    try:
        df = ma.get_data("nifty", datetime.date(date.year,date.month,date.day))
    except Exception as e:
        print(f"Unable to fetch data for {date} - {e}")
        return 0
    symbols=df['symbol'].unique().tolist()
    symbols.remove('NIFTY-I')
    symbols.remove('NIFTY')

    sym_len=len(symbols)
    

    folder_name = date.strftime("%d-%b-%Y")
   
    os.makedirs(path_index+folder_name, exist_ok=True)
    path_index_new=f'{path_index}{folder_name}/'
    x=len(symbols)

    input_date_string = end_date

    # Convert the date string to a datetime object
    date_object = datetime.datetime.strptime(input_date_string, "%Y-%m-%d").date()

    # Format the date as "day-Mon-year"
    formatted_date = date_object.strftime("%d-%b-%Y")
    formatted_date_expiry=date_object.strftime("%d%b%y")
    combined_result=f"NIFTY{formatted_date_expiry.upper()}"

    # Print the result in the desired format
    formatted_folder = f"NIFTY_{formatted_date}"

    os.makedirs(path_index_new+formatted_folder, exist_ok=True)

    xox=f"{path_index_new}{formatted_folder}/"

    for k in range(x):
        filtered_df=df[df['symbol']==symbols[k]]
        filtered_df=filtered_df.drop("symbol", axis=1)
        new_coloumn_order=["date","time","open","high","low","close","volume","oi"]
        filtered_df=filtered_df[new_coloumn_order]


        symbol_token=symbols[k]
        p=len(symbol_token)
        
        right=str(symbol_token[p-2:p])

        if right=="CE":
            new_column_names_CE = {
            'date': 'Date',
            "time": "Time",
            "open": "open CE",
            "high": "high CE",
            "low": "low CE",
            "close": "close CE",
            "volume": "volume CE",
            "oi": "oi CE",
            # Add more columns as needed
            }
            filtered_df.rename(columns=new_column_names_CE,inplace=True)
            m=symbols[k]
            pop=len(m)
            t=combined_result
            tot=len(t)
            strike=m[tot:pop-2]
            print(f"{strike}_CE")

            filtered_df.to_csv(xox+INSTRUMENT+strike+"_CE.csv",index=False)

        elif right=="PE":
            new_column_names_PE = {
            'date': 'Date',
            "time": "Time",
            "open": "open PE",
            "high": "high PE",
            "low": "low PE",
            "close": "close PE",
            "volume": "volume PE",
            "oi": "oi PE",
                # Add more columns as needed
            }
            filtered_df.rename(columns=new_column_names_PE,inplace=True)

            m=symbols[k]
            pop=len(m)
            t=combined_result
            tot=len(t)
            strike=m[tot:pop-2]
            print(f"{strike}_PE")

            filtered_df.to_csv(xox+INSTRUMENT+strike+"_PE.csv",index=False)

    return sym_len




new_df=pd.read_excel(path_main+"Startjee.xlsx", sheet_name="Past_Backtesting")
rows=new_df.shape[0]

for jj in range(rows):
    data = {'Date of Initiation': [pd.Timestamp(new_df.loc[jj,"Date of Initiation"]), pd.Timestamp(new_df.loc[jj,"Expiry"])]}
    df = pd.DataFrame(data)

    # Convert the Timestamp column to a string with the desired format
    df['Date of Initiation'] = df['Date of Initiation'].dt.strftime('%Y-%m-%d')

    start_date = pd.to_datetime(df.loc[0,"Date of Initiation"])
    end_date = pd.to_datetime(df.loc[1,"Date of Initiation"])

    date_range = pd.date_range(start=start_date, end=end_date)

    filtered_dates = [date.strftime('%Y-%m-%d') for date in date_range if date.weekday() < 5]
    length_date=len(filtered_dates)
    print(length_date)
    end_date_new=filtered_dates[length_date-1]
    symbol_length_1=[]
    for date_string in filtered_dates:
        # Convert each date string to a datetime.date object
        print(date_string)
        date_object = datetime.datetime.strptime(date_string, "%Y-%m-%d").date()
        lenght=get_data(date_object,end_date_new)
        symbol_length_1.append(lenght)

    expiry_date=end_date_new
    formatted_data = f"Expiry {expiry_date}: {symbol_length_1}\n"

    file_path = 'Expiry_vs_Strike_Len.txt'

    with open(path_index+file_path, 'a') as file:
        file.write(formatted_data)

    print(symbol_length_1)