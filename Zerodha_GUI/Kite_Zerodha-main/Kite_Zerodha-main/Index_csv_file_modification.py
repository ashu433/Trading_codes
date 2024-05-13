import pandas as pd
import numpy as np
import requests
from kite_trade import *
import json
from datetime import datetime,timedelta


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


def get_website_content(url):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
        }
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            return response.json()
        else:
            print("Failed to fetch the URL:", response.status_code)
            return None
    except Exception as e:
        print("An error occurred:", str(e))
        return None


def Next_expiry_date_finding(Segment):

    import time

    if Segment!="SENSEX":
        url = f"https://www.nseindia.com/api/option-chain-indices?symbol={Segment}"

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
        }

        while True:
            response = requests.get(url, headers=headers)

            if response.status_code == 200:
                content_output=response.text
                content_output = json.loads(content_output)
                Expiry_date_list=content_output["records"]["expiryDates"]
                return Expiry_date_list
            
            else:
                print("Failed to retrieve data from the URL:", response.status_code)
                print("Retrying in 1 second...")
                time.sleep(1)
    
    elif Segment=="SENSEX":
        pass
    else:
        pass


def checking_month_end(entered_date,index_of_date):
    df=pd.read_csv(path_main+"Enctoke_Expiry_month_end_info.csv")
    content_enctoken=df.iloc[0,0]
    enctoken = content_enctoken
    kite = KiteApp(enctoken=enctoken)

    x=kite.ltp("BSE:SENSEX")
    price=x['BSE:SENSEX']['last_price']
    ATM_Strike = round(price/ 100) * 100

    date_No_month_end=formatted_dates(entered_date,0)
    date_with_month_end=formatted_dates(entered_date,1)

    quote_no_month_end=Segment+date_No_month_end+str(ATM_Strike)+"CE"
    quote_with_month_end=Segment+date_with_month_end+str(ATM_Strike)+"CE"

    atm_token_ce_no_month_end=kite.ltp("BFO:"+quote_no_month_end)
    atm_token_ce_with_month_end=kite.ltp("BFO:"+quote_with_month_end) 

    Modify_dates=0

    print(f"len(atm_token_ce_no_month_end)={len(atm_token_ce_no_month_end)} en(atm_token_ce_with_month_end)={len(atm_token_ce_with_month_end)}")

    if len(atm_token_ce_no_month_end)==0 and len(atm_token_ce_with_month_end)!=0:
        Modify_dates=1
        return month_end,Modify_dates
    elif len(atm_token_ce_no_month_end)!=0 and len(atm_token_ce_with_month_end)!=0:
        Month_End=0
        date_obj = datetime.strptime(entered_date, "%d-%b-%Y")
        entered_date = date_obj.strftime("%d-%b-%y")
        index_data.loc[index_of_date,"Expiry Date"]=entered_date
        index_data.loc[index_of_date,"Month End"]=Month_End
        return index_data,Modify_dates
    elif len(atm_token_ce_no_month_end)==0 and len(atm_token_ce_with_month_end)==0:
        month_end=0
        Modify_dates=1
        return month_end,Modify_dates
    else:
        pass

def is_last_week_of_month(date_str):
    present_date = datetime.strptime(date_str, "%d-%b-%Y")
    total_days_in_month = present_date.replace(day=1, month=present_date.month % 12 + 1) - timedelta(days=1)
    total_weeks_in_month = total_days_in_month.isocalendar()[1]
    current_week_number = present_date.isocalendar()[1]

    if present_date.day > total_days_in_month.day - 7 and current_week_number == total_weeks_in_month:
        print("The entered date belongs to the last week of the month.")
        Last_date_of_month=1
        return Last_date_of_month
    else:
        print("The entered date does not belong to the last week of the month.")
        Last_date_of_month=0
        return Last_date_of_month


path_main="D:/ashu/Finance/algo_trading/Zerodha_GUI/Kite_Zerodha-main/Kite_Zerodha-main/"
path_bhav_copy="D:/ashu/Finance/algo_trading/Option_chain_data/"

index_data=pd.read_csv(path_main+"Index_Symbols_Expiry.csv")

segment_dictonary={"NIFTY":["NIFTY 50",50],"BANKNIFTY":["NIFTY BANK",100],"FINNIFTY":["NIFTY FIN SERVICE",50],"MIDCPNIFTY":["NIFTY MID SELECT",25],"SENSEX":["SENSEX",100]}

Segment_N_BN=["NIFTY","BANKNIFTY"]

today_date = datetime.today()
today_date = today_date.strftime('%d-%b-%y')
print(today_date)
Expiry_date=index_data.loc[0,"Expiry Date"]
index_of_date = index_data[index_data['Expiry Date'] == today_date].index.max()
Segment=index_data.loc[index_of_date,"Symbol"]

Present_date = datetime.today().strftime('%d%b%Y')
Present_date=Present_date.upper()
final_file=f"fo{Present_date}bhav.csv"
path_new_bhav_copy=f"{path_bhav_copy}/{final_file}/"
bhav_copy_df=pd.read_csv(path_new_bhav_copy+final_file)
N_BN_dict={}

for segment in Segment_N_BN:
    filtered_df_N_BN=index_data[index_data['Symbol']==segment]
    date_list=filtered_df_N_BN["Expiry Date"].tolist()
    exp_list=Next_expiry_date_finding(segment)
    exp_list=exp_list[0:6]
    exp_list = [datetime.strptime(date_str, '%d-%b-%Y').strftime('%d-%b-%y') for date_str in exp_list]
    set_date_list = set(date_list)
    set_exp_list = set(exp_list)

    non_common_elements = set_date_list.symmetric_difference(set_exp_list)
    if not non_common_elements:
        print("Both the Index Data frame and the listed expiries is same ")
        New_expiry=None
        N_BN_dict[segment]=None
    else:
        non_common_elements=list(non_common_elements)
        print("New Expiry:", non_common_elements[0])
        New_expiry=non_common_elements[0]

    new_bhav_copy_df=bhav_copy_df[(bhav_copy_df['SYMBOL']==segment) & (bhav_copy_df['INSTRUMENT']=="FUTIDX")]
    monthly_expiry_date_list=new_bhav_copy_df['EXPIRY_DT'].tolist()


    if New_expiry is not None:
        if New_expiry in monthly_expiry_date_list:
            Month_end=1
        else:
            Month_end=0

        dictonary_to_add={"Underlying":segment_dictonary[segment][0],"Symbol":segment,"Expiry Date":New_expiry,"Month End":Month_end}
        new_dataframe = pd.DataFrame(dictonary_to_add, index=[0])
        filtered_df_N_BN = pd.concat([filtered_df_N_BN, new_dataframe], axis=0)
        print(f"New Data Frame: {filtered_df_N_BN}")
        N_BN_dict[segment]=filtered_df_N_BN
    else:
        pass

for jj in Segment_N_BN:
    if N_BN_dict[jj] is not None:
        index_data=index_data[index_data['Symbol']!=jj]
        stored_df=N_BN_dict[jj]
        index_data=pd.concat([stored_df, index_data], axis=0)
    else:
        pass

if Segment!="SENSEX" :
    expiry_list=Next_expiry_date_finding(Segment)
    print(expiry_list)
    Next_Expiry=expiry_list[1]
    date_obj = datetime.strptime(Next_Expiry, '%d-%b-%Y')
    Next_Expiry= date_obj.strftime('%d-%b-%y')
    print(Next_Expiry)
    new_bhav_copy_df=bhav_copy_df[(bhav_copy_df['SYMBOL']==Segment) & (bhav_copy_df['INSTRUMENT']=="FUTIDX")]
    
    monthly_expiry_date_list=new_bhav_copy_df['EXPIRY_DT'].tolist()

    if today_date in monthly_expiry_date_list:
        Month_end=1
    else:
        Month_end=0

    index_data.loc[index_of_date,"Expiry Date"]=Next_Expiry
    index_data.loc[index_of_date,"Month End"]=Month_end
    index_data = index_data.drop_duplicates()

elif Segment=="SENSEX":

    date_obj = datetime.strptime(today_date, "%d-%b-%y")
    new_date_obj = date_obj + timedelta(days=7)
    new_expiry_date = new_date_obj.strftime("%d-%b-%Y")
    Last_date_of_month=is_last_week_of_month(new_expiry_date)

    if Last_date_of_month==0:
        index_of_date,Modify_dates=checking_month_end(new_expiry_date,index_of_date)
        if Modify_dates==1:
            current_date = new_date_obj
            for _ in range(7):
                current_date -= timedelta(days=1)
                computed_date=current_date.strftime('%d-%b-%Y')
                index_of_date,Modify_dates=checking_month_end(computed_date)
                if Modify_dates==0:
                    break
                elif Modify_dates==1:
                    continue
                else:
                    pass
    elif Last_date_of_month==1:
        index_data.loc[index_of_date,"Expiry Date"]=new_expiry_date
        index_data.loc[index_of_date,"Month End"]=1   

    
print(index_data)
