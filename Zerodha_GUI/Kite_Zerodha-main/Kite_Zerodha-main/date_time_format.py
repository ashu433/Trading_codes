from datetime import datetime
import pandas as pd



def date_time_format(expiry):
    # global expiry

    if month_end==0:

        parsed_date = datetime.strptime(expiry, '%d-%b-%Y')
        formatted_date = parsed_date.strftime('%y%m%d')

        char_list = list(formatted_date)

        Letter_to_insert="2"
        length=len(formatted_date)
        first=formatted_date[0:2]
        last=formatted_date[length-2:length]

        formatted_date=first+Letter_to_insert+last

        return formatted_date
    elif month_end==1:

        parsed_date = datetime.strptime(expiry, '%d-%b-%Y')
        formatted_date = parsed_date.strftime('%Y%b').upper()
        formatted_date=formatted_date[2:]

        return formatted_date




path_main="D:/ashu/Finance/algo_trading/Zerodha_GUI/Kite_Zerodha-main/Kite_Zerodha-main/"

df=pd.read_csv(path_main+"Enctoke_Expiry_month_end_info.csv")

# with open(path_main+"expiry_date.txt",'r') as file:
#     content_expiry_date=file.read()

# expiry=content_expiry_date

month_end=df.iloc[0,2]