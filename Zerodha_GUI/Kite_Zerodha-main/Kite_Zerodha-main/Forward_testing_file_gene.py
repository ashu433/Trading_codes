import pandas as pd
from datetime import datetime, timedelta




def formatted_dates(expiry, month_end):
    mont_dict = {"Jan": 1, "Feb": 2, "Mar": 3, "Apr": 4, "May": 5, "Jun": 6, "Jul": 7, "Aug": 8, "Sep": 9, "Oct": 10,
                 "Nov": 11, "Dec": 12}

    if month_end == 0:

        parsed_date = datetime.strptime(expiry, '%d-%b-%Y')
        formatted_date = parsed_date.strftime('%y%m%d')

        char_list = list(formatted_date)

        month = expiry.split('-')[1]

        Letter_to_insert = str(mont_dict[month])
        length = len(formatted_date)
        first = formatted_date[0:2]
        last = formatted_date[length - 2:length]

        formatted_date = first + Letter_to_insert + last

        return formatted_date
    elif month_end == 1:

        parsed_date = datetime.strptime(expiry, '%d-%b-%Y')
        formatted_date = parsed_date.strftime('%Y%b').upper()
        formatted_date = formatted_date[2:]

        return formatted_date

def data_parsing(Suffix_out):
    Orders_data=pd.read_csv(path_index+"orders.csv")
    Orders_data[['Date', 'Time']] = Orders_data['Time'].str.split(' ', expand=True)
    Orders_data.insert(0, 'Date', Orders_data.pop('Date'))
    Orders_data['Instrument'] = Orders_data['Instrument'].str.replace(f'NIFTY{Suffix_out}', '', regex=False)
    Orders_data['Right'] = Orders_data['Instrument'].str.extract('(PE|CE)$')
    Orders_data['Instrument'] = Orders_data['Instrument'].str.replace('(PE|CE)$', '', regex=True)
    Orders_data.insert(3, 'Right', Orders_data.pop('Right'))
    Orders_data = Orders_data.iloc[::-1].reset_index(drop=True)
    Orders_data.to_csv(path_index+"Order_parsed.csv",index=False)

path_main = "D:/ashu/Finance/algo_trading/Zerodha_GUI/Kite_Zerodha-main/Kite_Zerodha-main/"
path_index = "D:/ashu/Finance/algo_trading/Option_chain_data/"


Segment = "NIFTY"

index_data = pd.read_csv(path_main + "Index_Symbols_Expiry.csv")
indices = index_data.index[index_data['Symbol'] == Segment].tolist()
date_list = []
month_end_list = []

for i in indices:
    date = index_data.loc[i, "Expiry Date"]
    month_end = index_data.loc[i, "Month End"]
    date_list.append(date)
    month_end_list.append(month_end)

Expiry_date = date_list[0]
Month_End = month_end_list[0]

date_object = datetime.strptime(Expiry_date, '%d-%b-%y')
Expiry_date = date_object.strftime('%d-%b-%Y')

Suffix_out=formatted_dates(Expiry_date,Month_End)
data_parsing(Suffix_out)