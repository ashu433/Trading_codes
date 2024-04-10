# import requests

# Path_backtest_Report="D:/ashu/Finance/algo_trading/Zerodha_GUI/Kite_Zerodha-main/Kite_Zerodha-main/Back_Test_Files_Report/"

# def get_website_content(url):
#     try:
#         # Send a GET request to the URL
#         response = requests.get(url)

#         # Check if the request was successful (status code 200)
#         if response.status_code == 200:
#             # Return the content of the webpage
#             return response.json()
#         else:
#             print("Failed to fetch the URL:", response.status_code)
#             return None
#     except Exception as e:
#         print("An error occurred:", str(e))
#         return None

# # URL of the website
# url = "https://oxide.sensibull.com/v1/compute/cache/live_derivative_prices/256265"

# # Call the function to get the content of the website
# website_content = get_website_content(url)

# # Print the content (you can process it further as needed)
# if website_content:
#     print(website_content['data']['per_expiry_data']['2024-04-04']['options'][0])
#     # with open(Path_backtest_Report+"website_content.txt", "w") as file:
#     #     file.write(str(website_content))



from kite_trade import *
import pandas as pd
from datetime import datetime,timedelta
import time
import ast

path_main="D:/ashu/Finance/algo_trading/Zerodha_GUI/Kite_Zerodha-main/Kite_Zerodha-main/"
Path_backtest_Report="D:/ashu/Finance/algo_trading/Zerodha_GUI/Kite_Zerodha-main/Kite_Zerodha-main/Back_Test_Files_Report/"


# content_CE=str(content_CE)
# cleaned_contents_CE = content_CE.replace("datetime.datetime", "").replace(", tzinfo=tzoffset(None, 19800)", "")
# data_CE = ast.literal_eval(cleaned_contents_CE)
# df_CE = pd.DataFrame(data_CE)
# df_CE['date'] = df_CE['date'].apply(lambda x: pd.Timestamp(year=x[0], month=x[1], day=x[2], hour=x[3], minute=x[4]))
# df_CE['Date'] = df_CE['date'].dt.strftime('%Y-%m-%d')
# df_CE['Time'] = df_CE['date'].dt.strftime('%H:%M')
# df_CE = df_CE.drop(columns=['date'])
# df_CE = df_CE[['Date', 'Time', 'open', 'high', 'low', 'close','volume','oi']]

# df_CE.to_csv(Path_backtest_Report+"Output.csv",index=False)


def limit_order_Sell(Quote,Size,price,Strike,Right):
    global enctoken
    kite = KiteApp(enctoken=enctoken)
    global order_info

    Initial_DF=pd.read_csv(Path_backtest_Report+"Running_Status_of_trade.csv")

    Trigger_price=price-0.05

    order = kite.place_order(variety=kite.VARIETY_REGULAR,
                         exchange=kite.EXCHANGE_NFO,
                         tradingsymbol=Quote,
                         transaction_type=kite.TRANSACTION_TYPE_SELL,
                         quantity=Size,
                         product=kite.PRODUCT_NRML,
                         order_type=kite.ORDER_TYPE_SL,
                         price=price,
                         validity=kite.VALIDITY_DAY,
                         disclosed_quantity=None,
                         trigger_price=Trigger_price,
                         squareoff=None,
                         stoploss=None,
                         trailing_stoploss=None,
                         tag="TradeViaPython")
    

df=pd.read_csv(path_main+"Enctoke_Expiry_month_end_info.csv")
content_enctoken=df.iloc[0,0]
enctoken = content_enctoken
kite = KiteApp(enctoken=enctoken)

ATM_Token_CE=10010882







def console_output_log_recording(content):
    global Path_backtest_Report
    current_time = datetime.now()

    current_time_str = current_time.strftime("%H:%M:%S")

    with open(Path_backtest_Report+'Console_output_log_file.txt', 'a') as file:
        file.write(f"{current_time_str}: {content}.\n")


with open(Path_backtest_Report+'Console_output_log_file.txt', 'w') as file:
    pass
        
Path_backtest_Report="D:/ashu/Finance/algo_trading/Zerodha_GUI/Kite_Zerodha-main/Kite_Zerodha-main/Back_Test_Files_Report/"


console_output_log_recording("All the Orders are succesfully complete")