import requests
import Intraday_live_data
import pandas as pd
from datetime import datetime
from kite_trade import *
import pytz

Path_backtest_Report="D:/ashu/Finance/algo_trading/Zerodha_GUI/Kite_Zerodha-main/Kite_Zerodha-main/Back_Test_Files_Report/"
path_main="D:/ashu/Finance/algo_trading/Zerodha_GUI/Kite_Zerodha-main/Kite_Zerodha-main/"
Desired_delta=0.15

df=pd.read_csv(path_main+"Enctoke_Expiry_month_end_info.csv")
content_enctoken=df.iloc[0,0]
enctoken = content_enctoken
kite = KiteApp(enctoken=enctoken)


data=pd.read_csv(path_main+"Live_Running_Startjee.csv")
Segment_name=data.loc[0,"Symbol"]
expiry_date=data.loc[0,"Expiry Date"]
Month_end=data.loc[0,"Month End"]


def get_website_content(url):
    try:
        response = requests.get(url)

        if response.status_code == 200:
            return response.json()
        else:
            print("Failed to fetch the URL:", response.status_code)
            return None
    except Exception as e:
        print("An error occurred:", str(e))
        return None

def formatted_dates(expiry,month_end):
    mont_dict={"Jan":1,"Feb":2,"Mar":3,"Apr":4,"May":5,"Jun":6,"Jul":7,"Aug":8,"Sep":9,"Oct":10,"Nov":11,"Dec":12}

    if month_end==0:

        parsed_date = datetime.strptime(expiry, '%d-%b-%Y')
        formatted_date = parsed_date.strftime('%y%m%d')

        char_list = list(formatted_date)

        month=expiry.split('-')[1]

        Letter_to_insert=str(mont_dict[month])
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

# URL of the website
url = "https://oxide.sensibull.com/v1/compute/cache/live_derivative_prices/256265"

# Call the function to get the content of the website
website_content = get_website_content(url)

date_obj = datetime.strptime(expiry_date, "%d-%b-%y")
expiry_date = date_obj.strftime("%d-%b-%Y")

final_new=Intraday_live_data.getoptionchain(Segment_name,expiry_date)
final_new.reset_index(drop=True, inplace=True)
Strikes_option_chain=final_new['strikePrice'].tolist()

modified_date=formatted_dates(expiry_date,Month_end)

Date_CE=[]
Date_PE=[]
Time_CE=[]
Time_PE=[]
Strikes_CE=[]
Strikes_PE=[]
Price_CE=[]
Price_PE=[]
Theta_CE=[]
Theta_PE=[]
delta_CE=[]
delta_PE=[]
gamma_CE=[]
gamma_PE=[]
Vega_CE=[]
Vega_PE=[]
IV_CE=[]
IV_PE=[]

for i in range(len(Strikes_option_chain)):
    quote_CE=Segment_name+modified_date+str(Strikes_option_chain[i])+"CE"
    atm_token_ce=kite.ltp("NFO:"+quote_CE)
    ATM_Token_CE=atm_token_ce["NFO:"+quote_CE]['instrument_token']

    quote_PE=Segment_name+modified_date+str(Strikes_option_chain[i])+"PE"
    atm_token_pe=kite.ltp("NFO:"+quote_PE)
    ATM_Token_PE=atm_token_pe["NFO:"+quote_PE]['instrument_token']  

    expiry_date_obj = datetime.strptime(expiry_date, "%d-%b-%Y")
    new_expiry_date = expiry_date_obj.strftime("%Y-%m-%d")

    if website_content:
        content_length=len(website_content['data']['per_expiry_data'][new_expiry_date]['options'])

        for j in range(content_length):

            if website_content['data']['per_expiry_data'][new_expiry_date]['options'][j]['token']==ATM_Token_CE:
                datetime_str=website_content['data']['per_expiry_data'][new_expiry_date]['options'][j]['last_trade_time']
                datetime_obj_utc = datetime.strptime(datetime_str, '%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=pytz.UTC)
                ist_timezone = pytz.timezone('Asia/Kolkata')
                datetime_obj_ist = datetime_obj_utc.astimezone(ist_timezone)
                date = datetime_obj_ist.strftime('%d-%m-%Y')
                time_ist = datetime_obj_ist.strftime('%H:%M:%S')

                Date_CE.append(date)
                Time_CE.append(time_ist)
                Strikes_CE.append(Strikes_option_chain[i])
                Price_CE.append(website_content['data']['per_expiry_data'][new_expiry_date]['options'][j]['last_price'])
                Theta_CE.append(website_content['data']['per_expiry_data'][new_expiry_date]['options'][j]['greeks_with_iv']["theta"])
                delta_CE.append(website_content['data']['per_expiry_data'][new_expiry_date]['options'][j]['greeks_with_iv']["delta"])
                gamma_CE.append(website_content['data']['per_expiry_data'][new_expiry_date]['options'][j]['greeks_with_iv']["gamma"])
                Vega_CE.append(website_content['data']['per_expiry_data'][new_expiry_date]['options'][j]['greeks_with_iv']["vega"])
                IV_CE.append(website_content['data']['per_expiry_data'][new_expiry_date]['options'][j]['greeks_with_iv']["iv"])
            else:
                pass

            if website_content['data']['per_expiry_data'][new_expiry_date]['options'][j]['token']==ATM_Token_PE:
                datetime_str=website_content['data']['per_expiry_data'][new_expiry_date]['options'][j]['last_trade_time']
                datetime_obj_utc = datetime.strptime(datetime_str, '%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=pytz.UTC)
                ist_timezone = pytz.timezone('Asia/Kolkata')
                datetime_obj_ist = datetime_obj_utc.astimezone(ist_timezone)
                date = datetime_obj_ist.strftime('%d-%m-%Y')
                time_ist = datetime_obj_ist.strftime('%H:%M:%S')

                Date_PE.append(date)
                Time_PE.append(time_ist)
                Strikes_PE.append(Strikes_option_chain[i])
                Price_PE.append(website_content['data']['per_expiry_data'][new_expiry_date]['options'][j]['last_price'])
                Theta_PE.append(website_content['data']['per_expiry_data'][new_expiry_date]['options'][j]['greeks_with_iv']["theta"])
                delta_PE.append(website_content['data']['per_expiry_data'][new_expiry_date]['options'][j]['greeks_with_iv']["delta"])
                gamma_PE.append(website_content['data']['per_expiry_data'][new_expiry_date]['options'][j]['greeks_with_iv']["gamma"])
                Vega_PE.append(website_content['data']['per_expiry_data'][new_expiry_date]['options'][j]['greeks_with_iv']["vega"])
                IV_PE.append(website_content['data']['per_expiry_data'][new_expiry_date]['options'][j]['greeks_with_iv']["iv"])
            else:
                pass


final_file_CE={"Date":Date_CE,"Time":Time_CE,"Strike":Strikes_CE,"Price CE":Price_CE,"Theta CE":Theta_CE,"Delta CE":delta_CE,"Gamma CE":gamma_CE,"Vega CE":Vega_CE,"IV CE":IV_CE}
final_file_PE={"Date":Date_PE,"Time":Time_PE,"Strike":Strikes_PE,"Price PE":Price_PE,"Theta PE":Theta_PE,"Delta PE":delta_PE,"Gamma PE":gamma_PE,"Vega PE":Vega_PE,"IV PE":IV_PE}


final_df_CE=pd.DataFrame(final_file_CE)
final_df_PE=pd.DataFrame(final_file_PE)

closest_index_CE = (final_df_CE['Delta CE'] < Desired_delta).idxmax()
Desired_Strike_CE=final_df_CE.loc[closest_index_CE,"Strike"]

# closest_index_PE = (final_df_PE['Delta PE'] < Desired_delta).idxmax()
# Desired_Strike_PE=final_df_PE.loc[closest_index_PE,"Strike"]

final_df_PE['Delta PE'] = -1*final_df_PE['Delta PE']
index_Put = (final_df_PE['Delta PE'] - 0.15)
closest_to_zero_index = index_Put.abs().idxmin()
Desired_Strike_PE=final_df_PE.loc[closest_to_zero_index, "Strike"]

print(f"Desired Strike for call: {Desired_Strike_CE} Desired Strike for put: {Desired_Strike_PE}")