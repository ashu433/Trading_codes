import pandas as pd
from datetime import datetime,timedelta
import os
import Black_scholes_model
import numpy as np

Access_path_date="H:/My Drive/Daily_F_O_data/Options/Index/"
Accesst_path_Spot_IR="H:/My Drive/Daily_F_O_data/"
path_main="D:/ashu/Finance/algo_trading/Zerodha_GUI/Kite_Zerodha-main/Kite_Zerodha-main/"
path_spot_vol="H:/My Drive/Daily_F_O_data/"
Path_backtest_Report="D:/ashu/Finance/algo_trading/Zerodha_GUI/Kite_Zerodha-main/Kite_Zerodha-main/Back_Test_Files_Report/"

Accepted_Expiry_Dates=["12-Mar-2020","09-Apr-2020","28-May-2020","19-Nov-2020","03-Dec-2020","28-Jan-2021","11-Mar-2021","01-Apr-2021","15-Apr-2021","22-Apr-2021",
                       "12-May-2021","22-Jul-2021","18-Aug-2021","03-Nov-2021","27-Jan-2022","03-Mar-2022","13-Apr-2022","05-May-2022","11-Aug-2022","18-Aug-2022","01-Sep-2022",
                       "06-Oct-2022","10-Nov-2022","26-Jan-2023","09-Mar-2023","30-Mar-2023","06-Apr-2023","04-May-2023","29-Jun-2023","17-Aug-2023","21-Sep-2023","05-Oct-2023",
                       "26-Oct-2023","16-Nov-2023","30-Nov-2023","28-Nov-2023"]
Rejected_Expiry_Dates=["27-Feb-2020","01-Apr-2020","16-Apr-2020","07-May-2020","08-Oct-2020","31-Dec-2020","08-Apr-2021","16-Apr-2021","21-Oct-2021","11-Nov-2021","25-Nov-2021",
                       "24-Mar-2022","21-Apr-2022","27-Oct-2022","13-Apr-2023","20-Apr-2023"]
holidays_date=["10-Mar-2020","06-Apr-2020","25-May-2020","16-Nov-2020","30-Nov-2020","26-Jan-2021","11-Mar-2021","29-Mar-2021","14-Apr-2021",
               "21-Apr-2021","13-May-2021","21-Jul-2021","19-Aug-2021","10-Sep-2021","15-Sep-2021","04-Nov-2021","05-Nov-2021","19-Nov-2021","26-Jan-2022","01-Mar-2022",
               "18-Mar-2022","14-Apr-2022","15-Apr-2022","03-May-2022","09-Aug-2022","15-Aug-2022","31-Aug-2022","05-Oct-2022","24-Oct-2022","26-Oct-2022","08-Nov-2022",
               "26-Jan-2023","07-Mar-2023","30-Mar-2023","04-Apr-2023","07-Apr-2023","14-Apr-2023","01-May-2023","28-Jun-2023","15-Aug-2023","19-Sep-2023","02-Oct-2023",
               "24-Oct-2023","14-Nov-2023","27-Nov-2023","25-Dec-2023","22-Jan-2024","26-Jan-2024","08-Mar-2024","25-Mar-2024","29-Mar-2024","11-Apr-2024","17-Apr-2024",
               "01-May-2024","20-May-2024","17-Jun-2024","17-Jul-2024","15-Aug-2024","02-Oct-2024","01-Nov-2024","15-Nov-2024","25-Dec-2024"]


file_startjee=pd.read_excel(path_main+"Startjee.xlsx", sheet_name="Past_Backtesting")
Date_of_Init=file_startjee["Date of Initiation"].tolist()
Date_of_Expiry=file_startjee["Expiry"].tolist()

formatted_Date_of_Init = [date.strftime('%d-%b-%Y') for date in Date_of_Init]
formatted_Date_of_Expiry = [date.strftime('%d-%b-%Y') for date in Date_of_Expiry]

###########################  Analysis  ######################################

Date_ana=[]
Time_ana=[]
Net_Profit_loss_ana=[]
Call_preimum_ana=[]
Put_premium_ana=[]
Call_CE_1_CP_ana=[]
SL_1_Call_ana=[]
Call_CE_2_CP_ana=[]
SL_2_Call_ana=[]
Call_CE_3_CP_ana=[]
SL_3_Call_ana=[]
Call_CE_4_CP_ana=[]
SL_4_Call_ana=[]

Put_PE_1_CP_ana=[]
SL_1_Put_ana=[]
Put_PE_2_CP_ana=[]
SL_2_Put_ana=[]
Put_PE_3_CP_ana=[]
SL_3_Put_ana=[]
Put_PE_4_CP_ana=[]
SL_4_Put_ana=[]

###########################  Analysis  ######################################


##### Table data Initilization #################
date_init=[]
date_exp=[]
market_sentiment=[]

Call_stk_1=[]
Call_stk_2=[]
Call_stk_3=[]
Call_stk_4=[]

Put_stk_1=[]
Put_stk_2=[]
Put_stk_3=[]
Put_stk_4=[]

sl_hit_date=[]
sl_hit_time=[]
sl_hit_week=[]

Entry_date=[]
Entry_time_call=[]
Entry_time_put=[]
Entry_week=[]

Net_premium_collected=[]
Margin=[]
ROI=[]
Net_Credit_Spread_Call=[]
Net_Credit_Spread_Put=[]
Net_Credit_Spread=[]
Day=0
previous_day=[]
Market_trend="Neutral"
run_len=0
Active_status={}
reversal_status=None
reverse=[]
profit_loss=[]
global rev
global max_historical_call_credit_spread
global max_historical_put_credit_spread

Startjee_1_dict_Call={}
Startjee_1_dict_Put={}

historical_realized_profit_loss={}

################### Variables of the startjee ##############
Desired_time_CE="09:19"
Desired_time_PE="09:19"
Checking_time="09:30"
MARGIN_DEPLOYED=92000
Startjee_1=1
Startjee_2=0
Startjee_3=0
Threshold_price=1
Net_P_L=0
Len_ce=0
Len_pe=0
Lot_size=50
max_credit_spreads=4
Hedges_distance=600
Distance_between_strikes=50
size=1
################### Variables of the startjee ##############

def console_output_log_recording(content):

    with open(Path_backtest_Report+'Back_testing_Console_output_log_file.txt', 'a') as file:
        file.write(f"{content}.\n")

def merging(df_1,df_2,Right_1,Right_2,string_1,string_2):

    if Right_1=="Call" and Right_2=="Put":
      substring_to_remove_CE = "df_CE_"
      substring_to_remove_PE = "df_PE_"

      file_num_1=string_1.replace(substring_to_remove_CE,"")
      file_num_2=string_2.replace(substring_to_remove_PE,"")
      file_num_1=int(file_num_1)
      file_num_2=int(file_num_2)

      df_1.rename(columns={'Date':'Date','Time':'Time','open CE': f'open CE {file_num_1}', 'high CE': f'high CE {file_num_1}','low CE':f'low CE {file_num_1}','close CE':f'close CE {file_num_1}','volume CE': f'volume CE {file_num_1}','oi CE': f'oi CE {file_num_1}' }, inplace=True)
      df_2.rename(columns={'Date':'Date','Time':'Time','open PE': f'open PE {file_num_2}', 'high PE': f'high PE {file_num_2}','low PE':f'low PE {file_num_2}','close PE':f'close PE {file_num_2}','volume PE': f'volume PE {file_num_2}','oi PE': f'oi PE {file_num_2}' }, inplace=True)

      df_1['Date'] = pd.to_datetime(df_1['Date'])
      df_2['Date'] = pd.to_datetime(df_2['Date'])


      df_combined = pd.merge(df_1, df_2, on=['Date', 'Time'], how='outer')
      df_combined['Date'] = pd.to_datetime(df_combined['Date'])
      df_combined['Time'] = pd.to_datetime(df_combined['Time'], format='%H:%M').dt.strftime('%H:%M')
      df_combined = df_combined.sort_values(by=['Date', 'Time'])
      df_combined = df_combined.fillna(method='ffill')
      df_1=df_combined[['Date','Time',f'open CE {file_num_1}',f'high CE {file_num_1}',f'low CE {file_num_1}',f'close CE {file_num_1}',f'volume CE {file_num_1}',f'oi CE {file_num_1}']]
      df_2=df_combined[['Date','Time',f'open PE {file_num_2}',f'high PE {file_num_2}',f'low PE {file_num_2}',f'close PE {file_num_2}',f'volume PE {file_num_2}',f'oi PE {file_num_2}']]
      return df_1,df_2
        
    elif Right_1=="Call" and Right_2=="Call":
      substring_to_remove = "df_CE_"
      file_num_1=string_1.replace(substring_to_remove,"")
      file_num_2=string_2.replace(substring_to_remove,"")
      file_num_1=int(file_num_1)
      file_num_2=int(file_num_2)

      df_1.rename(columns={'Date':'Date','Time':'Time','open CE': f'open CE {file_num_1}', 'high CE': f'high CE {file_num_1}','low CE':f'low CE {file_num_1}','close CE':f'close CE {file_num_1}','volume CE': f'volume CE {file_num_1}','oi CE': f'oi CE {file_num_1}' }, inplace=True)
      df_2.rename(columns={'Date':'Date','Time':'Time','open CE': f'open CE {file_num_2}', 'high CE': f'high CE {file_num_2}','low CE':f'low CE {file_num_2}','close CE':f'close CE {file_num_2}','volume CE': f'volume CE {file_num_2}','oi CE': f'oi CE {file_num_2}' }, inplace=True)
      
      df_1['Date'] = pd.to_datetime(df_1['Date'])
      df_2['Date'] = pd.to_datetime(df_2['Date'])

      df_combined = pd.merge(df_1, df_2, on=['Date', 'Time'], how='outer')
      df_combined['Date'] = pd.to_datetime(df_combined['Date'])
      df_combined['Time'] = pd.to_datetime(df_combined['Time'], format='%H:%M').dt.strftime('%H:%M')
      df_combined = df_combined.sort_values(by=['Date', 'Time'])
      df_combined = df_combined.fillna(method='ffill')
      df_1=df_combined[['Date','Time',f'open CE {file_num_1}',f'high CE {file_num_1}',f'low CE {file_num_1}',f'close CE {file_num_1}',f'volume CE {file_num_1}',f'oi CE {file_num_1}']]
      df_2=df_combined[['Date','Time',f'open CE {file_num_2}',f'high CE {file_num_2}',f'low CE {file_num_2}',f'close CE {file_num_2}',f'volume CE {file_num_2}',f'oi CE {file_num_2}']]
      return df_1,df_2

    elif Right_1=="Put" and Right_2=="Put":
      substring_to_remove = "df_PE_"
      file_num_1=string_1.replace(substring_to_remove,"")
      file_num_2=string_2.replace(substring_to_remove,"")
      file_num_1=int(file_num_1)
      file_num_2=int(file_num_2)

      df_1.rename(columns={'Date':'Date','Time':'Time','open PE': f'open PE {file_num_1}', 'high PE': f'high PE {file_num_1}','low PE':f'low PE {file_num_1}','close PE':f'close PE {file_num_1}','volume PE': f'volume PE {file_num_1}','oi PE': f'oi PE {file_num_1}' }, inplace=True)
      df_2.rename(columns={'Date':'Date','Time':'Time','open PE': f'open PE {file_num_2}', 'high PE': f'high PE {file_num_2}','low PE':f'low PE {file_num_2}','close PE':f'close PE {file_num_2}','volume PE': f'volume PE {file_num_2}','oi PE': f'oi PE {file_num_2}' }, inplace=True)

      df_1['Date'] = pd.to_datetime(df_1['Date'])
      df_2['Date'] = pd.to_datetime(df_2['Date'])

      df_combined = pd.merge(df_1, df_2, on=['Date', 'Time'], how='outer')
      df_combined['Date'] = pd.to_datetime(df_combined['Date'])
      df_combined['Time'] = pd.to_datetime(df_combined['Time'], format='%H:%M').dt.strftime('%H:%M')
      df_combined = df_combined.sort_values(by=['Date', 'Time'])
      df_combined = df_combined.fillna(method='ffill')
      df_1=df_combined[['Date','Time',f'open PE {file_num_1}',f'high PE {file_num_1}',f'low PE {file_num_1}',f'close PE {file_num_1}',f'volume PE {file_num_1}',f'oi PE {file_num_1}']]
      df_2=df_combined[['Date','Time',f'open PE {file_num_2}',f'high PE {file_num_2}',f'low PE {file_num_2}',f'close PE {file_num_2}',f'volume PE {file_num_2}',f'oi PE {file_num_2}']]
      return df_1,df_2

    elif Right_1=="Put" and Right_2=="Call":
      substring_to_remove_PE = "df_PE_"
      substring_to_remove_CE = "df_CE_"

      file_num_1=string_1.replace(substring_to_remove_PE,"")
      file_num_2=string_2.replace(substring_to_remove_CE,"")

      print(file_num_1)
      print(file_num_2)

      file_num_1=int(file_num_1)
      file_num_2=int(file_num_2)

      df_1.rename(columns={'Date':'Date','Time':'Time','open PE': f'open PE {file_num_1}', 'high PE': f'high PE {file_num_1}','low PE':f'low PE {file_num_1}','close PE':f'close PE {file_num_1}','volume PE': f'volume PE {file_num_1}','oi PE': f'oi PE {file_num_1}' }, inplace=True)
      df_2.rename(columns={'Date':'Date','Time':'Time','open CE': f'open CE {file_num_2}', 'high CE': f'high CE {file_num_2}','low CE':f'low CE {file_num_2}','close CE':f'close CE {file_num_2}','volume CE': f'volume CE {file_num_2}','oi CE': f'oi CE {file_num_2}' }, inplace=True)

      df_1['Date'] = pd.to_datetime(df_1['Date'])
      df_2['Date'] = pd.to_datetime(df_2['Date'])

      df_combined = pd.merge(df_1, df_2, on=['Date', 'Time'], how='outer')
      df_combined['Date'] = pd.to_datetime(df_combined['Date'])
      df_combined['Time'] = pd.to_datetime(df_combined['Time'], format='%H:%M').dt.strftime('%H:%M')
      df_combined = df_combined.sort_values(by=['Date', 'Time'])
      df_combined = df_combined.fillna(method='ffill')
      df_1=df_combined[['Date','Time',f'open PE {file_num_1}',f'high PE {file_num_1}',f'low PE {file_num_1}',f'close PE {file_num_1}',f'volume PE {file_num_1}',f'oi PE {file_num_1}']]
      df_2=df_combined[['Date','Time',f'open CE {file_num_2}',f'high CE {file_num_2}',f'low CE {file_num_2}',f'close CE {file_num_2}',f'volume CE {file_num_2}',f'oi CE {file_num_2}']]
      return df_1,df_2


def SL_update(time,Active_Initial_Sold_premium_call,Active_Initial_Sold_premium_put,CE_instantinious_pr,PE_instantinious_pr,Active_call_Strike,Active_put_Strike,Active_SL_Call,Active_SL_Put,reversal_status,Startjee_1_dict_Call,Startjee_1_dict_Put):

    if Startjee_3==1:
        len_CE=len(Active_call_Strike)
        len_PE=len(Active_put_Strike)

        if reversal_status is None:
            for ii in range(len_PE):
                if PE_instantinious_pr[ii]<=(Active_Initial_Sold_premium_put[ii]/2) and (time in time_list):
                    Active_SL_Put[ii]=Active_Initial_Sold_premium_put[ii]
                else:
                    pass
            for jj in range(len_CE):
                if CE_instantinious_pr[jj]<=(Active_Initial_Sold_premium_call[jj]/2) and (time in time_list):
                    Active_SL_Call[jj]=Active_Initial_Sold_premium_call[jj]
                else:
                    pass
        
        else:
            Active_status_read=read_Active_status()
            Active_status_read["Deactive Put Strike"]=list(set(Active_status_read["Deactive Put Strike"]))
            Active_status_read["Deactive Call Strike"]=list(set(Active_status_read["Deactive Call Strike"]))
            Active_strikes_list_Put = [strike for strike in Active_put_Strike if strike not in Active_status_read["Deactive Put Strike"]]
            Active_strikes_list_Call = [strike for strike in Active_call_Strike if strike not in Active_status_read["Deactive Call Strike"]]

            len_CE=len(Active_strikes_list_Call)
            len_PE=len(Active_strikes_list_Put)

            for ii in range(len_PE):
                if Startjee_1_dict_Put[Active_strikes_list_Put[ii]][0]<=(Startjee_1_dict_Put[Active_strikes_list_Put[ii]][1]/2) and (time in time_list):
                    Startjee_1_dict_Put[Active_strikes_list_Put[ii]][2]=Startjee_1_dict_Put[Active_strikes_list_Put[ii]][1]
                else:
                    pass
            
            for jj in range(len_CE):
                if Startjee_1_dict_Call[Active_strikes_list_Call[jj]][0]<=(Startjee_1_dict_Call[Active_strikes_list_Call[jj]][1]/2) and (time in time_list):
                    Startjee_1_dict_Call[Active_strikes_list_Call[jj]][2]=Startjee_1_dict_Call[Active_strikes_list_Call[jj]][1]
                else:
                    pass

            len_1_ce=len(Active_call_Strike)
            len_1_pe=len(Active_put_Strike)

            for kk in range(len_1_pe):
                if Active_put_Strike[kk] in Active_strikes_list_Put:
                    Active_SL_Put[kk]=Startjee_1_dict_Put[Active_put_Strike[kk]][2]
                else:
                    pass

            for kk in range(len_1_ce):
                if Active_call_Strike[kk] in Active_strikes_list_Call:
                    Active_SL_Call[kk]=Startjee_1_dict_Call[Active_call_Strike[kk]][2]
                else:
                    pass



    if Startjee_1==1:

        len_CE=len(Active_call_Strike)
        len_PE=len(Active_put_Strike)

        # print(f"Active call strikes: {Active_call_Strike} and CE Instantinious premium {CE_instantinious_pr}")




        if reversal_status is None:
            for ii in range(len_PE):
                if PE_instantinious_pr[ii]<(Threshold_price/2) and (time in time_list):
                    pass
                elif PE_instantinious_pr[ii]<(Active_SL_Put[ii]/2) and (time in time_list):
                    Active_SL_Put[ii]=2*PE_instantinious_pr[ii]
                else:
                    pass
            for jj in range(len_CE):
                if CE_instantinious_pr[jj]<(Threshold_price/2) and (time in time_list):
                    pass
                elif CE_instantinious_pr[jj]<(Active_SL_Call[jj]/2) and (time in time_list):
                    Active_SL_Call[jj]=2*CE_instantinious_pr[jj]
                else:
                    pass            
        

        else:
            Active_status_read=read_Active_status()
            Active_status_read["Deactive Put Strike"]=list(set(Active_status_read["Deactive Put Strike"]))
            Active_status_read["Deactive Call Strike"]=list(set(Active_status_read["Deactive Call Strike"]))
            Active_strikes_list_Put = [strike for strike in Active_put_Strike if strike not in Active_status_read["Deactive Put Strike"]]
            Active_strikes_list_Call = [strike for strike in Active_call_Strike if strike not in Active_status_read["Deactive Call Strike"]]

            len_CE=len(Active_strikes_list_Call)
            len_PE=len(Active_strikes_list_Put)


            for ii in range(len_PE):
                if Startjee_1_dict_Put[Active_strikes_list_Put[ii]][0]<(Threshold_price/2) and (time in time_list):
                    pass
                elif Startjee_1_dict_Put[Active_strikes_list_Put[ii]][0]<(Startjee_1_dict_Put[Active_strikes_list_Put[ii]][2]/2) and (time in time_list):
                    Startjee_1_dict_Put[Active_strikes_list_Put[ii]][2]=2*Startjee_1_dict_Put[Active_strikes_list_Put[ii]][0]
                else:
                    pass
            

            for jj in range(len_CE):
                if Startjee_1_dict_Call[Active_strikes_list_Call[jj]][0]<(Threshold_price/2) and (time in time_list):
                    pass
                elif Startjee_1_dict_Call[Active_strikes_list_Call[jj]][0]<(Startjee_1_dict_Call[Active_strikes_list_Call[jj]][2]/2) and (time in time_list):
                    Startjee_1_dict_Call[Active_strikes_list_Call[jj]][2]=2*Startjee_1_dict_Call[Active_strikes_list_Call[jj]][0]
                else:
                    pass




            len_1_ce=len(Active_call_Strike)
            len_1_pe=len(Active_put_Strike)



            for kk in range(len_1_pe):
                if Active_put_Strike[kk] in Active_strikes_list_Put:
                    Active_SL_Put[kk]=Startjee_1_dict_Put[Active_put_Strike[kk]][2]
                else:
                    pass

            for kk in range(len_1_ce):
                if Active_call_Strike[kk] in Active_strikes_list_Call:
                    Active_SL_Call[kk]=Startjee_1_dict_Call[Active_call_Strike[kk]][2]
                else:
                    pass

def date_to_week(date):
    date_object = datetime.strptime(date, "%Y-%m-%d")
    day_of_week = date_object.strftime('%A')
    return day_of_week


def equalize_lists(lists_of_lists):
    # Find the maximum length of the lists
    max_length = max(len(lst) for lst in lists_of_lists)
    
    # Iterate through each list in the list of lists
    for lst in lists_of_lists:
        # Calculate the difference in length
        length_difference = max_length - len(lst)
        
        # Append None to the end of the list to make it of equal length
        lst.extend([None] * length_difference)
    
    # Return the list of lists with equal length
    return lists_of_lists

def running_log_update(entry_exit,list_name,Strike_entry,right,time,date,week,initiation_date,expiry_date,last_pe,last_ce,alternate_strike=None):

    if entry_exit=="Entry" and right=="Call" and last_ce==0 and last_pe==0:
        update_lists_call(list_name,Strike_entry)
        print(Call_stk_1)
        Entry_time_call.append(time)
        Entry_date.append(date)
        Entry_week.append(week)

        sl_hit_date.append(None)
        sl_hit_time.append(None)
        sl_hit_week.append(None)

        date_init.append(initiation_date)
        date_exp.append(expiry_date)
        market_sentiment.append(None)
        Net_Credit_Spread_Call.append(None)
        Net_Credit_Spread_Put.append(None)
        Net_Credit_Spread.append(None)
        ROI.append(None)
        reverse.append(None)
        Margin.append(None)
        profit_loss.append(None)

    elif entry_exit=="Entry" and right=="Put" and last_ce==0 and last_pe==0:
        update_lists_put(list_name,Strike_entry)
        print(Put_stk_1)
        Entry_time_put.append(time)

    elif entry_exit=="Entry" and right=="Call" and last_ce==1 and last_pe==0:
        update_lists_call(list_name,Strike_entry)
        update_lists_put(alternate_strike,None)
        Entry_time_call.append(time)
        Entry_time_put.append(None)
        Entry_date.append(date)
        Entry_week.append(week)

        sl_hit_date.append(None)
        sl_hit_time.append(None)
        sl_hit_week.append(None)

        date_init.append(initiation_date)
        date_exp.append(expiry_date)
        market_sentiment.append(None)
        Net_Credit_Spread_Call.append(None)
        Net_Credit_Spread_Put.append(None)
        Net_Credit_Spread.append(None)
        ROI.append(None)
        reverse.append(None)
        Margin.append(None)
        profit_loss.append(None)

    elif entry_exit=="Entry" and right=="Put" and last_ce==0 and last_pe==1:
        update_lists_put(list_name,Strike_entry)
        update_lists_call(alternate_strike,None)
        Entry_time_put.append(time)
        Entry_time_call.append(None)
        Entry_date.append(date)
        Entry_week.append(week)

        sl_hit_date.append(None)
        sl_hit_time.append(None)
        sl_hit_week.append(None)

        date_init.append(initiation_date)
        date_exp.append(expiry_date)
        market_sentiment.append(None)
        Net_Credit_Spread_Call.append(None)
        Net_Credit_Spread_Put.append(None)
        Net_Credit_Spread.append(None)
        ROI.append(None)
        reverse.append(None)
        Margin.append(None)
        profit_loss.append(None)

    elif entry_exit=="SL_Hit" and right=="Call":
        update_lists_call(list_name,-Strike_entry)
        update_lists_put("Put_stk_1",None)
        sl_hit_date.append(date)
        sl_hit_time.append(time)
        sl_hit_week.append(week)

        Entry_time_put.append(None)
        Entry_time_call.append(None)
        Entry_date.append(None)
        Entry_week.append(None)

        date_init.append(initiation_date)
        date_exp.append(expiry_date)
        market_sentiment.append(None)
        Net_Credit_Spread_Call.append(None)
        Net_Credit_Spread_Put.append(None)
        Net_Credit_Spread.append(None)
        ROI.append(None)
        reverse.append(None)
        Margin.append(None)
        profit_loss.append(None)

    elif entry_exit=="SL_Hit" and right=="Put":
        update_lists_put(list_name,-Strike_entry)
        update_lists_call("Call_stk_1",None)
        sl_hit_date.append(date)
        sl_hit_time.append(time)
        sl_hit_week.append(week)

        Entry_time_put.append(None)
        Entry_time_call.append(None)
        Entry_date.append(None)
        Entry_week.append(None)

        date_init.append(initiation_date)
        date_exp.append(expiry_date)
        market_sentiment.append(None)
        Net_Credit_Spread_Call.append(None)
        Net_Credit_Spread_Put.append(None)
        Net_Credit_Spread.append(None)
        ROI.append(None)
        reverse.append(None)
        Margin.append(None)
        profit_loss.append(None)


def find_closest_time_index(time_list, input_time_str):
    input_time = datetime.strptime(input_time_str, "%H:%M")
    closest_time = min(time_list, key=lambda x: abs(datetime.strptime(x, "%H:%M") - input_time))
    closest_index = time_list.index(closest_time)
    return closest_index

def Execution_check_Code(Triggered_time,Date,index_row,Closing_price,DF,right,string_name):


    if right=="CE":
      substring_to_remove_CE = "df_CE_"
      file_num=string_name.replace(substring_to_remove_CE,"")
      file_num=int(file_num)
    elif right=="PE":
      substring_to_remove_PE = "df_PE_"
      file_num=string_name.replace(substring_to_remove_PE,"")
      file_num=int(file_num)
    else:
        pass

    while True:
        if right=="CE":
            high_max=max(DF.loc[index_row+1,f"high CE {file_num}"],DF.loc[index_row+2,f"high CE {file_num}"],DF.loc[index_row+3,f"high CE {file_num}"],DF.loc[index_row+4,f"high CE {file_num}"],DF.loc[index_row+5,f"high CE {file_num}"])
            low_min=min(DF.loc[index_row+1,f"low CE {file_num}"],DF.loc[index_row+2,f"low CE {file_num}"],DF.loc[index_row+3,f"low CE {file_num}"],DF.loc[index_row+4,f"low CE {file_num}"],DF.loc[index_row+5,f"low CE {file_num}"])
        elif right=="PE":
            high_max=max(DF.loc[index_row+1,f"high PE {file_num}"],DF.loc[index_row+2,f"high PE {file_num}"],DF.loc[index_row+3,f"high PE {file_num}"],DF.loc[index_row+4,f"high PE {file_num}"],DF.loc[index_row+5,f"high PE {file_num}"])
            low_min=min(DF.loc[index_row+1,f"low PE {file_num}"],DF.loc[index_row+2,f"low PE {file_num}"],DF.loc[index_row+3,f"low PE {file_num}"],DF.loc[index_row+4,f"low PE {file_num}"],DF.loc[index_row+5,f"low PE {file_num}"])
        else:
            pass

        if low_min<=Closing_price<=high_max:
            time_new=Triggered_time
            break
        else:
            index=find_closest_time_index(time_list,Triggered_time)
            time_new=time_list[index+1]
            index_row = DF.index[(DF['Time'] == time_new)&(DF['Date'] == Date)].tolist()
            index_row=index_row[0]
            if right=="CE":
                Closing_price=DF.loc[index_row,f"close CE {file_num}"]
            elif right=="PE":
                Closing_price=DF.loc[index_row,f"close PE {file_num}"]

    return Closing_price,index_row,time_new

def round_to_nearest_5_minutes(input_time):
    # Split the input time into hours and minutes
    hour, minute = map(int, input_time.split(':'))

    # Round the minutes up to the nearest multiple of 5
    rounded_minute = 5 * round(minute / 5)

    # If rounded_minute equals 60, increment the hour
    if rounded_minute == 60:
        hour += 1
        rounded_minute = 0

    # Format the rounded time as a string
    rounded_time = '{:02d}:{:02d}'.format(hour, rounded_minute)

    return rounded_time

def find_key(dictionary, value):
    for key, values in dictionary.items():
        if value in values:
            return key
    return None


def final_log(initiation_date,expiry_date,market_sentiment_value,profit_loss_value,margin_used,net_credit_spread_call,net_credit_spread_put,reverse_happen,alternate_strike_call,alternate_strike_put):
    date_init.append(initiation_date)
    date_exp.append(expiry_date)
    market_sentiment.append(market_sentiment_value)
    Net_Credit_Spread_Call.append(net_credit_spread_call)
    Net_Credit_Spread_Put.append(net_credit_spread_put)
    overall_credit_spread=net_credit_spread_call+net_credit_spread_put
    Net_Credit_Spread.append(overall_credit_spread)
    reverse.append(reverse_happen)
    Margin.append(margin_used)
    roi=(profit_loss_value/margin_used)*100
    ROI.append(roi)
    profit_loss.append(profit_loss_value)

    update_lists_call(alternate_strike_call,None)
    update_lists_put(alternate_strike_put,None)
    Entry_time_call.append(None)
    Entry_time_put.append(None)
    Entry_date.append(None)
    Entry_week.append(None)

    sl_hit_date.append(None)
    sl_hit_time.append(None)
    sl_hit_week.append(None)

def volatility_strike_pred(Date,Time,path_expiry_date_recurring,Startjee_1_dict_Call,Startjee_1_dict_Put):
    global run_len
    global Market_trend
    global Active_call_Strike, Active_put_Strike
    global Active_Initial_Sold_premium_call, Active_Initial_Sold_premium_put
    global Active_SL_Call, Active_SL_Put
    global max_credit_spreads

#######################################   OFFSET CALCULATION   ############################################################

    input_time_str = Time
    incoming_time=Time
    input_time = datetime.strptime(input_time_str, "%H:%M")
    time_list_dt = [datetime.strptime(time_str, "%H:%M") for time_str in time_list]
    closest_time_index = min(range(len(time_list_dt)), key=lambda i: abs(time_list_dt[i] - input_time))
    Triggered_time=time_list[closest_time_index]

    target_time_df=Triggered_time

    if target_time_df>=incoming_time:
        pass
    else:
        incoming_time_index=time_list.index(target_time_df)
        target_time_df=time_list[incoming_time_index+1]

    Triggered_time=round_to_nearest_5_minutes(Triggered_time)
    ts = pd.Timestamp(Date)
    formatted_date = ts.strftime('%d-%m-%Y')
    volatility_file=pd.read_csv(path_spot_vol+"India_Vix_Historical.csv")
    Nifty_spot_file=pd.read_csv(path_spot_vol+"Nifty_50_Historical.csv")
    row_index_vol = volatility_file.index[(volatility_file['Time'] == Triggered_time)&(volatility_file['Date'] == formatted_date)].tolist()
    row_index_spot = Nifty_spot_file.index[(Nifty_spot_file['Time'] == Triggered_time)&(Nifty_spot_file['Date'] == formatted_date)].tolist()

    volatility=volatility_file.loc[row_index_vol[0],"Close"]
    Nifty_spot_price=Nifty_spot_file.loc[row_index_spot[0],"Close"]

    range_1=((volatility/np.sqrt(252))*Nifty_spot_price)/100
    offset=round(range_1,2)
    offset = round(offset / 50) * 50
    offset=int(offset)
    PE_strikes = {}
    CE_strikes={}
    df_trending_down_dict={}
    df_trending_up_dict={}
    Strikes_dict={}

    print(f"The triggered time is {Triggered_time} and the target time for the data frame is {target_time_df}")
#######################################   OFFSET CALCULATION   ############################################################

    if Market_trend=="Trending Up":
        max_len_pe=len(Active_put_Strike)

        print(Market_trend)

        if max_len_pe<=(max_credit_spreads-1):
            triggered_strike_put=Active_put_Strike[max_len_pe-1]
            triggered_strike_call=Active_call_Strike[0]+offset
            union_strikes_list=Active_call_Strike+Active_put_Strike
            over_all_len=len(union_strikes_list)
            starting_point=0
            ending_point=over_all_len
            Strikes_dict["Call"]=Active_call_Strike
            Strikes_dict["Put"]=Active_put_Strike
            constant=0
        else:
            triggered_strike_put=Active_put_Strike[max_len_pe-1]
            union_strikes_list=Active_put_Strike
            over_all_len=len(union_strikes_list)
            triggered_strike_call=None
            starting_point=1
            ending_point=over_all_len+1
            Strikes_dict["Put"]=Active_put_Strike
            print(f"The strikes dictonary is {Strikes_dict}")
            constant=1


        for i in range(starting_point,ending_point):
            Right=find_key(Strikes_dict,union_strikes_list[i-constant])
            if Right=="Call":
                CE_strikes[f"CE_Strike_{max_len_pe}"]=union_strikes_list[i]+offset
                CE_strikes[f"file_CE_{max_len_pe}"]=f'NIFTY{str(CE_strikes[f"CE_Strike_{max_len_pe}"])}_CE.csv'
                CE_strikes[f"df_CE_{max_len_pe}"]=pd.read_csv(path_expiry_date_recurring+CE_strikes[f"file_CE_{max_len_pe}"])

                if (len(CE_strikes[f"df_CE_{max_len_pe}"].loc[4,'Time']))>5:
                    CE_strikes[f"df_CE_{max_len_pe}"]['Time'] = CE_strikes[f"df_CE_{max_len_pe}"]['Time'].apply(lambda x: x[:5])
                else:
                    pass

                df_trending_up_dict[f"df_CE_{max_len_pe}"]=[CE_strikes[f"df_CE_{max_len_pe}"],"Call",CE_strikes[f"CE_Strike_{max_len_pe}"]]

                if len(df_trending_up_dict)==1:
                    pass
                elif len(df_trending_up_dict)>1:
                    len_1=len(df_trending_up_dict)
                    keys = list(df_trending_up_dict.keys())
                    Key_1=keys[len_1-2]
                    Key_2=keys[len_1-1]
                    df_1=df_trending_up_dict[Key_1][0]
                    df_2=df_trending_up_dict[Key_2][0]
                    rt_1=df_trending_up_dict[Key_1][1]
                    rt_2=df_trending_up_dict[Key_2][1]
                    df_1,df_2=merging(df_1,df_2,rt_1,rt_2,Key_1,Key_2)
                    df_trending_up_dict[Key_1][0]=df_1
                    df_trending_up_dict[Key_2][0]=df_2
                else:
                    pass

            elif Right=="Put":
                PE_strikes[f"file_PE_{i-constant}"]=f'NIFTY{union_strikes_list[i-constant]}_PE.csv'
                PE_strikes[f"df_PE_{i-constant}"]=pd.read_csv(path_expiry_date_recurring+PE_strikes[f"file_PE_{i-constant}"])

                if (len(PE_strikes[f"df_PE_{i-constant}"].loc[4,'Time']))>5:
                    PE_strikes[f"df_PE_{i-constant}"]['Time'] = PE_strikes[f"df_PE_{i-constant}"]['Time'].apply(lambda x: x[:5])
                else:
                    pass

                df_trending_up_dict[f"df_PE_{i-constant}"]=[PE_strikes[f"df_PE_{i-constant}"],"Put",union_strikes_list[i-constant]]

                if len(df_trending_up_dict)==1:
                    pass
                elif len(df_trending_up_dict)>1:
                    len_1=len(df_trending_up_dict)
                    keys = list(df_trending_up_dict.keys())
                    Key_1=keys[len_1-2]
                    Key_2=keys[len_1-1]
                    df_1=df_trending_up_dict[Key_1][0]
                    df_2=df_trending_up_dict[Key_2][0]
                    rt_1=df_trending_up_dict[Key_1][1]
                    rt_2=df_trending_up_dict[Key_2][1]
                    df_1,df_2=merging(df_1,df_2,rt_1,rt_2,Key_1,Key_2)
                    df_trending_up_dict[Key_1][0]=df_1
                    df_trending_up_dict[Key_2][0]=df_2
                else:
                    pass

            else:
                pass

        key_list=list(df_trending_up_dict.keys())

        ts = pd.Timestamp(Date)
        formatted_date = ts.strftime('%Y-%m-%d')
        week=date_to_week(formatted_date)

        for keys_i in key_list:
            if df_trending_up_dict[keys_i][2]==triggered_strike_call and df_trending_up_dict[keys_i][1]=="Call":
                Active_call_Strike.append(df_trending_up_dict[keys_i][2])
                print(f"Newly added Call Strike is {df_trending_up_dict[keys_i][2]}")
                string_repl=str(keys_i)
                resu=string_repl.replace("df_CE_", "")
                resu=int(resu)
                index_row_CE = CE_strikes[keys_i].index[(CE_strikes[keys_i]['Time'] == target_time_df) & (CE_strikes[keys_i]['Date'] == formatted_date)].tolist()
                index_row_CE=index_row_CE[0]
                CP_CE=CE_strikes[keys_i].loc[index_row_CE,f"close CE {resu}"]
                CP_CE_2,index_row_CE,time_obs_CE=Execution_check_Code(target_time_df,formatted_date,index_row_CE,CP_CE,CE_strikes[keys_i],"CE",keys_i)

            if df_trending_up_dict[keys_i][2]==triggered_strike_put and df_trending_up_dict[keys_i][1]=="Put":
                print(f"Newly added Put Strike is {df_trending_up_dict[keys_i][2]}")
                string_repl=str(keys_i)
                resu=string_repl.replace("df_PE_", "")
                resu=int(resu)
                index_row_PE = PE_strikes[keys_i].index[(PE_strikes[keys_i]['Time'] == target_time_df) & (PE_strikes[keys_i]['Date'] == formatted_date)].tolist()
                index_row_PE=index_row_PE[0]
                CP_PE=PE_strikes[keys_i].loc[index_row_PE,f"close PE {resu}"]
                CP_PE_2,index_row_PE,time_obs_PE=Execution_check_Code(target_time_df,formatted_date,index_row_PE,CP_PE,PE_strikes[keys_i],"PE",keys_i)
            elif triggered_strike_call==None:
                pass

        CE_Strike_remove=Active_call_Strike[0]
        Initial_CE_remove=Active_Initial_Sold_premium_call[0]
        SL_CE_remove=Active_SL_Call[0]

        Startjee_1_dict_Call.pop(CE_Strike_remove)

        if max_len_pe<=(max_credit_spreads-1):
            SL_PE_2=2*CP_PE_2
            SL_CE_2=2*CP_CE_2

            print(f"New Call premium is {CP_CE_2} and SL is {SL_CE_2}")
            print(f"New Put premium is {CP_PE_2} and SL is {SL_PE_2}")

            running_log_update("Entry",f"Put_stk_{max_len_pe}",triggered_strike_put,"Put",time_obs_PE,formatted_date,week,formatted_Date_of_Init[k],formatted_Date_of_Expiry[k],0,0)
            running_log_update("Entry",f"Call_stk_{max_len_pe}",triggered_strike_call,"Call",time_obs_CE,formatted_date,week,formatted_Date_of_Init[k],formatted_Date_of_Expiry[k],0,0)

            Active_status_read=read_Active_status()
            Active_status_read["Deactive Call Strike"].append(CE_Strike_remove)
            Active_status_read["Deactive Call Strike Premium Initial"].append(str(Initial_CE_remove))

            Active_status_read["Active_call_Strike"].remove(str(CE_Strike_remove))
            Active_status_read["Active_Initial_Sold_premium_call"].remove(str(Initial_CE_remove))

            Active_status_read["Active_call_Strike"].append(triggered_strike_call)
            Active_status_read["Active_Initial_Sold_premium_call"].append(CP_CE_2)

            Active_status_read["Active_put_Strike"].append(triggered_strike_put)
            Active_status_read["Active_Initial_Sold_premium_put"].append(CP_PE_2)

            writing_Active_status(Active_status_read)

            Active_call_Strike.remove(CE_Strike_remove)
            Active_Initial_Sold_premium_call=[]
            Active_SL_Call=[]


            Active_Initial_Sold_premium_put.append(CP_PE_2)
            Active_SL_Put.append(SL_PE_2)

            Active_Initial_Sold_premium_call.append(CP_CE_2)
            Active_SL_Call.append(SL_CE_2)

            index_row=min(index_row_CE,index_row_PE)

            rows=df_trending_up_dict[key_list[0]][0].shape[0]

            column_list_time=df_trending_up_dict[key_list[0]][0]["Time"].tolist()
            len_time=len(column_list_time)
            Time_max=column_list_time[len_time-2]
            
            run_len=rows-index_row
            rows_df_len=rows

            print(f"The number of rows in the data frame is {rows} and index is {index_row} and index CE is {index_row_CE} and index PE is {index_row_PE}")

            return rows_df_len,index_row,df_trending_up_dict,Active_call_Strike,Active_put_Strike,Active_Initial_Sold_premium_call,Active_Initial_Sold_premium_put,Active_SL_Call,Active_SL_Put
        else:
            SL_PE_2=2*CP_PE_2

            running_log_update("Entry",f"Put_stk_{max_len_pe}",triggered_strike_put,"Put",time_obs_PE,formatted_date,week,formatted_Date_of_Init[k],formatted_Date_of_Expiry[k],0,0)


            Active_status_read=read_Active_status()
            Active_status_read["Deactive Call Strike"].append(CE_Strike_remove)
            Active_status_read["Deactive Call Strike Premium Initial"].append(str(Initial_CE_remove))

            Active_status_read["Active_call_Strike"].remove(str(CE_Strike_remove))
            Active_status_read["Active_Initial_Sold_premium_call"].remove(str(Initial_CE_remove))

            Active_status_read["Active_put_Strike"].append(triggered_strike_call)
            Active_status_read["Active_Initial_Sold_premium_put"].append(CP_PE_2)

            writing_Active_status(Active_status_read)

            Active_call_Strike.remove(CE_Strike_remove)

            Active_Initial_Sold_premium_call=[]
            Active_SL_Call=[]

            Active_Initial_Sold_premium_put.append(CP_PE_2)
            Active_SL_Put.append(SL_PE_2)

            index_row=index_row_PE

            rows=df_trending_up_dict[key_list[0]][0].shape[0]
            run_len=rows-index_row
            rows_df_len=rows

            column_list_time=df_trending_up_dict[key_list[0]][0]["Time"].tolist()
            len_time=len(column_list_time)
            Time_max=column_list_time[len_time-2]

            print(f"The number of rows in the data frame is {rows} and index is {index_row} and index PE is {index_row_PE}")

            return rows_df_len,index_row,df_trending_up_dict,Active_call_Strike,Active_put_Strike,Active_Initial_Sold_premium_call,Active_Initial_Sold_premium_put,Active_SL_Call,Active_SL_Put
        

    elif Market_trend=="Trending Down":
        max_len_ce=len(Active_call_Strike)

        if max_len_ce<=(max_credit_spreads-1):
            triggered_strike_call=Active_call_Strike[max_len_ce-1]
            triggered_strike_put=Active_put_Strike[0]-offset
            union_strikes_list=Active_put_Strike+Active_call_Strike
            over_all_len=len(union_strikes_list)
            starting_point=0
            ending_point=over_all_len
            Strikes_dict["Call"]=Active_call_Strike
            Strikes_dict["Put"]=Active_put_Strike
            constant=0
        else:
            triggered_strike_call=Active_call_Strike[max_len_ce-1]
            union_strikes_list=Active_call_Strike
            over_all_len=len(union_strikes_list)
            triggered_strike_put=None
            starting_point=1
            ending_point=over_all_len+1
            Strikes_dict["Call"]=Active_call_Strike
            print(f"The strikes dictonary is {Strikes_dict}")
            constant=1


        for i in range(starting_point,ending_point):
            Right=find_key(Strikes_dict,union_strikes_list[i-constant])

            if Right=="Put":
                PE_strikes[f"PE_Strike_{max_len_ce}"]=union_strikes_list[i]-offset
                PE_strikes[f"file_PE_{max_len_ce}"]=f'NIFTY{str(PE_strikes[f"PE_Strike_{max_len_ce}"])}_PE.csv'
                PE_strikes[f"df_PE_{max_len_ce}"]=pd.read_csv(path_expiry_date_recurring+PE_strikes[f"file_PE_{max_len_ce}"])

                if (len(PE_strikes[f"df_PE_{max_len_ce}"].loc[4,'Time']))>5:
                    PE_strikes[f"df_PE_{max_len_ce}"]['Time'] = PE_strikes[f"df_PE_{max_len_ce}"]['Time'].apply(lambda x: x[:5])
                else:
                    pass

                df_trending_down_dict[f"df_PE_{max_len_ce}"]=[PE_strikes[f"df_PE_{max_len_ce}"],"Put",PE_strikes[f"PE_Strike_{max_len_ce}"]]

                if len(df_trending_down_dict)==1:
                    pass
                elif len(df_trending_down_dict)>1:
                    len_1=len(df_trending_down_dict)
                    keys = list(df_trending_down_dict.keys())
                    Key_1=keys[len_1-2]
                    Key_2=keys[len_1-1]
                    df_1=df_trending_down_dict[Key_1][0]
                    df_2=df_trending_down_dict[Key_2][0]
                    rt_1=df_trending_down_dict[Key_1][1]
                    rt_2=df_trending_down_dict[Key_2][1]
                    df_1,df_2=merging(df_1,df_2,rt_1,rt_2,Key_1,Key_2)
                    df_trending_down_dict[Key_1][0]=df_1
                    df_trending_down_dict[Key_2][0]=df_2
                else:
                    pass

            elif Right=="Call":
                CE_strikes[f"file_CE_{i-constant}"]=f'NIFTY{union_strikes_list[i-constant]}_CE.csv'
                CE_strikes[f"df_CE_{i-constant}"]=pd.read_csv(path_expiry_date_recurring+CE_strikes[f"file_CE_{i-constant}"])

                if (len(CE_strikes[f"df_CE_{i-constant}"].loc[4,'Time']))>5:
                    CE_strikes[f"df_CE_{i-constant}"]['Time'] = CE_strikes[f"df_CE_{i-constant}"]['Time'].apply(lambda x: x[:5])
                else:
                    pass

                df_trending_down_dict[f"df_CE_{i-constant}"]=[CE_strikes[f"df_CE_{i-constant}"],"Call",union_strikes_list[i-constant]]

                if len(df_trending_down_dict)==1:
                    pass
                elif len(df_trending_down_dict)>1:
                    len_1=len(df_trending_down_dict)
                    keys = list(df_trending_down_dict.keys())
                    Key_1=keys[len_1-2]
                    Key_2=keys[len_1-1]
                    df_1=df_trending_down_dict[Key_1][0]
                    df_2=df_trending_down_dict[Key_2][0]
                    rt_1=df_trending_down_dict[Key_1][1]
                    rt_2=df_trending_down_dict[Key_2][1]
                    df_1,df_2=merging(df_1,df_2,rt_1,rt_2,Key_1,Key_2)
                    df_trending_down_dict[Key_1][0]=df_1
                    df_trending_down_dict[Key_2][0]=df_2
                else:
                    pass

            else:
                pass

        key_list=list(df_trending_down_dict.keys())
        print(f"Key list is: {key_list} and triggered strike is: {triggered_strike_call}")
        ts = pd.Timestamp(Date)
        formatted_date = ts.strftime('%Y-%m-%d')
        week=date_to_week(formatted_date)

        for keyss in key_list:
            print(f"Right: {df_trending_down_dict[keyss][1]} Strike: {df_trending_down_dict[keyss][2]}")

        for keys_i in key_list:
            if df_trending_down_dict[keys_i][2]==triggered_strike_call and df_trending_down_dict[keys_i][1]=="Call":
                print(f"Newly added Call Strike is {df_trending_down_dict[keys_i][2]}")
                string_repl=str(keys_i)
                resu=string_repl.replace("df_CE_", "")
                resu=int(resu)
                index_row_CE = CE_strikes[keys_i].index[(CE_strikes[keys_i]['Time'] == target_time_df) & (CE_strikes[keys_i]['Date'] == formatted_date)].tolist()
                index_row_CE=index_row_CE[0]
                CP_CE=CE_strikes[keys_i].loc[index_row_CE,f"close CE {resu}"]
                CP_CE_2,index_row_CE,time_obs_CE=Execution_check_Code(target_time_df,formatted_date,index_row_CE,CP_CE,CE_strikes[keys_i],"CE",keys_i)

            if df_trending_down_dict[keys_i][2]==triggered_strike_put and df_trending_down_dict[keys_i][1]=="Put":
                Active_put_Strike.append(df_trending_down_dict[keys_i][2])
                print(f"Newly added Put Strike is {df_trending_down_dict[keys_i][2]}")
                string_repl=str(keys_i)
                resu=string_repl.replace("df_PE_", "")
                resu=int(resu)
                index_row_PE = PE_strikes[keys_i].index[(PE_strikes[keys_i]['Time'] == target_time_df) & (PE_strikes[keys_i]['Date'] == formatted_date)].tolist()
                index_row_PE=index_row_PE[0]
                CP_PE=PE_strikes[keys_i].loc[index_row_PE,f"close PE {resu}"]
                CP_PE_2,index_row_PE,time_obs_PE=Execution_check_Code(target_time_df,formatted_date,index_row_PE,CP_PE,PE_strikes[keys_i],"PE",keys_i)
            elif triggered_strike_put==None:
                pass


        PE_Strike_remove=Active_put_Strike[0]
        Initial_PE_remove=Active_Initial_Sold_premium_put[0]
        SL_PE_remove=Active_SL_Put[0]

        print(f"SL to remove {SL_PE_remove}")

        Startjee_1_dict_Put.pop(PE_Strike_remove)

        if max_len_ce<=(max_credit_spreads-1):
            SL_PE_2=2*CP_PE_2
            SL_CE_2=2*CP_CE_2

            running_log_update("Entry",f"Put_stk_{max_len_ce}",triggered_strike_put,"Put",time_obs_PE,formatted_date,week,formatted_Date_of_Init[k],formatted_Date_of_Expiry[k],0,0)
            running_log_update("Entry",f"Call_stk_{max_len_ce}",triggered_strike_call,"Call",time_obs_CE,formatted_date,week,formatted_Date_of_Init[k],formatted_Date_of_Expiry[k],0,0)

            Active_status_read=read_Active_status()
            Active_status_read["Deactive Put Strike"].append(PE_Strike_remove)
            Active_status_read["Deactive Put Strike Premium Initial"].append(str(Initial_PE_remove))

            Active_status_read["Active_put_Strike"].remove(str(PE_Strike_remove))
            Active_status_read["Active_Initial_Sold_premium_put"].remove(str(Initial_PE_remove))

            Active_status_read["Active_call_Strike"].append(triggered_strike_call)
            Active_status_read["Active_Initial_Sold_premium_call"].append(CP_CE_2)

            Active_status_read["Active_put_Strike"].append(triggered_strike_put)
            Active_status_read["Active_Initial_Sold_premium_put"].append(CP_PE_2)

            writing_Active_status(Active_status_read)

            Active_put_Strike.remove(PE_Strike_remove)
            Active_Initial_Sold_premium_put=[]
            Active_SL_Put=[]


            Active_Initial_Sold_premium_put.append(CP_PE_2)
            Active_SL_Put.append(SL_PE_2)

            Active_Initial_Sold_premium_call.append(CP_CE_2)
            Active_SL_Call.append(SL_CE_2)

            index_row=min(index_row_CE,index_row_PE)

            rows=df_trending_down_dict[key_list[0]][0].shape[0]
            run_len=rows-index_row

            rows_df_len=rows

            return rows_df_len,index_row,df_trending_down_dict,Active_call_Strike,Active_put_Strike,Active_Initial_Sold_premium_call,Active_Initial_Sold_premium_put,Active_SL_Call,Active_SL_Put
        else:
            SL_CE_2=2*CP_CE_2

            running_log_update("Entry",f"Call_stk_{max_len_ce}",triggered_strike_call,"Call",time_obs_CE,formatted_date,week,formatted_Date_of_Init[k],formatted_Date_of_Expiry[k],0,0)


            Active_status_read=read_Active_status()
            Active_status_read["Deactive Put Strike"].append(PE_Strike_remove)
            Active_status_read["Deactive Put Strike Premium Initial"].append(str(Initial_PE_remove))

            Active_status_read["Active_put_Strike"].remove(str(PE_Strike_remove))
            Active_status_read["Active_Initial_Sold_premium_put"].remove(str(Initial_PE_remove))

            Active_status_read["Active_call_Strike"].append(triggered_strike_call)
            Active_status_read["Active_Initial_Sold_premium_call"].append(CP_CE_2)

            writing_Active_status(Active_status_read)

            Active_put_Strike.remove(PE_Strike_remove)
            Active_Initial_Sold_premium_put=[]
            Active_SL_Put=[]

            Active_Initial_Sold_premium_call.append(CP_CE_2)
            Active_SL_Call.append(SL_CE_2)

            index_row=index_row_CE

            rows=df_trending_down_dict[key_list[0]][0].shape[0]
            run_len=rows-index_row

            rows_df_len=rows

            return rows_df_len,index_row,df_trending_down_dict,Active_call_Strike,Active_put_Strike,Active_Initial_Sold_premium_call,Active_Initial_Sold_premium_put,Active_SL_Call,Active_SL_Put


def update_lists_call(list_name, value):
    all_lists = [Call_stk_1, Call_stk_2, Call_stk_3, Call_stk_4]

    if list_name == "Call_stk_1":
        Call_stk_1.append(value)
        for lst in [Call_stk_2, Call_stk_3, Call_stk_4]:
            lst.append(None)
    elif list_name == "Call_stk_2":
        Call_stk_2.append(value)
        for lst in [Call_stk_1, Call_stk_3, Call_stk_4]:
            lst.append(None)
    elif list_name == "Call_stk_3":
        Call_stk_3.append(value)
        for lst in [Call_stk_1, Call_stk_2, Call_stk_4]:
            lst.append(None)
    elif list_name == "Call_stk_4":
        Call_stk_4.append(value)
        for lst in [Call_stk_1, Call_stk_2, Call_stk_3]:
            lst.append(None)
    else:
        pass


def update_lists_put(list_name, value):
        
    if list_name == "Put_stk_1":
        Put_stk_1.append(value)
        for lst in [ Put_stk_2, Put_stk_3, Put_stk_4]:
            lst.append(None)
    elif list_name == "Put_stk_2":
        Put_stk_2.append(value)
        for lst in [Put_stk_1, Put_stk_3, Put_stk_4]:
            lst.append(None)
    elif list_name == "Put_stk_3":
        Put_stk_3.append(value)
        for lst in [Put_stk_1, Put_stk_2, Put_stk_4]:
            lst.append(None)
    elif list_name == "Put_stk_4":
        Put_stk_4.append(value)
        for lst in [Put_stk_1, Put_stk_2, Put_stk_3]:
            lst.append(None)
    else:
        pass


def writing_Active_status(Active_status):
    with open(Path_backtest_Report+"active_status.txt", "w") as file:
        for key, value in Active_status.items():
            file.write(f"{key}={','.join(map(str, value))}\n")

def read_Active_status():
    Active_status_read = {}
    with open(Path_backtest_Report+"active_status.txt", "r") as file:
        for line in file:
            key, value_str = line.strip().split("=")
            value = [x for x in value_str.split(",")]
            Active_status_read[key] = value

    return Active_status_read

def renaming_columns(df,right,idx,old_idx):

    if right=="Call":
        new_column_names_CE = {
        'Date': 'Date',
        "Time": "Time",
        f"open CE {old_idx}": f"open CE {idx}",
        f"high CE {old_idx}": f"high CE {idx}",
        f"low CE {old_idx}": f"low CE {idx}",
        f"close CE {old_idx}":f"close CE {idx}",
        f"volume CE {old_idx}":f"volume CE {idx}",
        f"oi CE {old_idx}":f"oi CE {idx}"
        }

        df.rename(columns=new_column_names_CE, inplace=True)

        return df
    
    elif right=="Put":
        new_column_names_PE={
        'Date': 'Date',
        "Time": "Time",
        f"open PE {old_idx}": f"open PE {idx}",
        f"high PE {old_idx}": f"high PE {idx}",
        f"low PE {old_idx}": f"low PE {idx}",
        f"close PE {old_idx}":f"close PE {idx}",
        f"volume PE {old_idx}":f"volume PE {idx}",
        f"oi PE {old_idx}":f"oi PE {idx}"
        }

        df.rename(columns=new_column_names_PE, inplace=True)

        return df

def morning_code(path_expiry_date_recurring,date,Active_call_Strike,Active_put_Strike):
    global Market_trend
    global rev

    PE_strikes = {}
    CE_strikes={}
    morning_df={}
    Strikes_dict={}
    Strikes_dict["Call"]=Active_call_Strike
    Strikes_dict["Put"]=Active_put_Strike

    union_strikes_list=Active_call_Strike+Active_put_Strike
    union_strikes_list.insert(0,0)
    over_all_len=len(union_strikes_list)


    for i in range(1,over_all_len):
        Right=find_key(Strikes_dict,union_strikes_list[i])

        if Right=="Call":
            CE_strikes[f"file_CE_{i}"]=f'NIFTY{union_strikes_list[i]}_CE.csv'
            CE_strikes[f"df_CE_{i}"]=pd.read_csv(path_expiry_date_recurring+CE_strikes[f"file_CE_{i}"])

            if (len(CE_strikes[f"df_CE_{i}"].loc[4,'Time']))>5:
                CE_strikes[f"df_CE_{i}"]['Time'] = CE_strikes[f"df_CE_{i}"]['Time'].apply(lambda x: x[:5])
            else:
                pass

            morning_df[f"df_CE_{i}"]=[CE_strikes[f"df_CE_{i}"],"Call",union_strikes_list[i]]

            if len(morning_df)==1:
                pass
            elif len(morning_df)>1:
                len_1=len(morning_df)
                keys = list(morning_df.keys())
                Key_1=keys[len_1-2]
                Key_2=keys[len_1-1]
                df_1=morning_df[Key_1][0]
                df_2=morning_df[Key_2][0]
                rt_1=morning_df[Key_1][1]
                rt_2=morning_df[Key_2][1]
                df_1,df_2=merging(df_1,df_2,rt_1,rt_2,Key_1,Key_2)
                morning_df[Key_1][0]=df_1
                morning_df[Key_2][0]=df_2
            else:
                pass

        elif Right=="Put":
            PE_strikes[f"file_PE_{i}"]=f'NIFTY{union_strikes_list[i]}_PE.csv'
            PE_strikes[f"df_PE_{i}"]=pd.read_csv(path_expiry_date_recurring+PE_strikes[f"file_PE_{i}"])

            if (len(PE_strikes[f"df_PE_{i}"].loc[4,'Time']))>5:
                PE_strikes[f"df_PE_{i}"]['Time'] = PE_strikes[f"df_PE_{i}"]['Time'].apply(lambda x: x[:5])
            else:
                pass

            morning_df[f"df_PE_{i}"]=[PE_strikes[f"df_PE_{i}"],"Put",union_strikes_list[i]]

            if len(morning_df)==1:
                pass
            elif len(morning_df)>1:
                len_1=len(morning_df)
                keys = list(morning_df.keys())
                Key_1=keys[len_1-2]
                Key_2=keys[len_1-1]
                df_1=morning_df[Key_1][0]
                df_2=morning_df[Key_2][0]
                rt_1=morning_df[Key_1][1]
                rt_2=morning_df[Key_2][1]
                df_1,df_2=merging(df_1,df_2,rt_1,rt_2,Key_1,Key_2)
                morning_df[Key_1][0]=df_1
                morning_df[Key_2][0]=df_2
            else:
                pass

    keys_list_collected=list(morning_df.keys())

    input_date=date
    parsed_date = datetime.strptime(input_date, "%d-%b-%Y")
    date= parsed_date.strftime("%Y-%m-%d")
    
    Morning_DF=morning_df[keys_list_collected[0]][0]


    Morning_row_index = Morning_DF.index[(Morning_DF['Time'] == Checking_time)&(Morning_DF['Date'] == date)].tolist()
    print(Morning_row_index)
    Morning_row_index=Morning_row_index[0]
    print(f"The reversal status is {rev}")


    key_mapping={}

    for keys_ii in keys_list_collected:
        if Market_trend=="Trending Up":
            len_PE=len(Active_put_Strike)
            sliced_file=keys_ii[:6]

            if rev==1 and len(Active_put_Strike)==0:
                new_column_names_CE = {
                'Date': 'Date',
                "Time": "Time",
                f"open CE": f"open CE {len_PE}",
                f"high CE": f"high CE {len_PE}",
                f"low CE": f"low CE {len_PE}",
                f"close CE":f"close CE {len_PE}",
                f"volume CE":f"volume CE {len_PE}",
                f"oi CE":f"oi CE {len_PE}"
                }
                Morning_DF.rename(columns=new_column_names_CE, inplace=True)
                morning_df[keys_list_collected[0]][0]=Morning_DF
            else:
                pass

            if sliced_file=="df_CE_":
                string_1=keys_ii
                substring_to_remove_CE = "df_CE_"
                file_num_1=string_1.replace(substring_to_remove_CE,"")
                file_num_1=int(file_num_1)
            
                key_mapping[keys_ii]=f"df_CE_{len_PE}"
                df_going=morning_df[keys_ii][0]
                right=morning_df[keys_ii][1]
                got_df=renaming_columns(df_going,right,len_PE,file_num_1)
                morning_df[keys_ii][0]=got_df

            elif sliced_file=="df_PE_":
                string_1=keys_ii
                substring_to_remove_PE = "df_PE_"
                file_num_1=string_1.replace(substring_to_remove_PE,"")
                file_num_1=int(file_num_1)

                stk=morning_df[keys_ii][2]
                target_idx=Active_put_Strike.index(stk)
                key_mapping[keys_ii]=f"df_PE_{target_idx+1}"
                df_going=morning_df[keys_ii][0]
                right=morning_df[keys_ii][1]
                got_df=renaming_columns(df_going,right,target_idx+1,file_num_1)    
                morning_df[keys_ii][0]=got_df
            else:
                pass

        elif Market_trend=="Trending Down":
            len_CE=len(Active_call_Strike)
            sliced_file=keys_ii[:6]

            if rev==1 and len(Active_call_Strike)==0:
                new_column_names_PE = {
                'Date': 'Date',
                "Time": "Time",
                f"open PE": f"open PE {len_CE}",
                f"high PE": f"high PE {len_CE}",
                f"low PE": f"low PE {len_CE}",
                f"close PE":f"close PE {len_CE}",
                f"volume PE":f"volume PE {len_CE}",
                f"oi PE":f"oi PE {len_CE}"
                }
                Morning_DF.rename(columns=new_column_names_PE, inplace=True)
                morning_df[keys_list_collected[0]][0]=Morning_DF
            else:
                pass

            if sliced_file=="df_PE_":
                string_1=keys_ii
                substring_to_remove_PE = "df_PE_"
                file_num_1=string_1.replace(substring_to_remove_PE,"")
                file_num_1=int(file_num_1)

                print(f"Ingoing length of CE {len_CE} and file_num_1 {file_num_1}")

                key_mapping[keys_ii]=f"df_PE_{len_CE}"
                df_going=morning_df[keys_ii][0]
                right=morning_df[keys_ii][1]
                print(df_going)
                got_df=renaming_columns(df_going,right,len_CE,file_num_1)
                morning_df[keys_ii][0]=got_df 

            elif sliced_file=="df_CE_":
                string_1=keys_ii
                substring_to_remove_CE = "df_CE_"
                file_num_1=string_1.replace(substring_to_remove_CE,"")
                file_num_1=int(file_num_1)

                stk=morning_df[keys_ii][2]
                target_idx=Active_call_Strike.index(stk)
                key_mapping[keys_ii]=f"df_CE_{target_idx+1}"
                df_going=morning_df[keys_ii][0]
                right=morning_df[keys_ii][1]
                got_df=renaming_columns(df_going,right,target_idx+1,file_num_1)
                morning_df[keys_ii][0]=got_df    
            else:
                pass       


        elif Market_trend=="Neutral":
            sliced_file=keys_ii[:6]

            if sliced_file=="df_CE_":

                string_1=keys_ii
                substring_to_remove_CE = "df_CE_"
                file_num_1=string_1.replace(substring_to_remove_CE,"")
                file_num_1=int(file_num_1)

                key_mapping[keys_ii]=f"df_CE_{1}"
                df_going=morning_df[keys_ii][0]
                right=morning_df[keys_ii][1]
                got_df=renaming_columns(df_going,right,1,file_num_1)
                morning_df[keys_ii][0]=got_df

            elif sliced_file=="df_PE_":

                string_1=keys_ii
                substring_to_remove_PE = "df_PE_"
                file_num_1=string_1.replace(substring_to_remove_PE,"")
                file_num_1=int(file_num_1)

                key_mapping[keys_ii]=f"df_PE_{1}"
                df_going=morning_df[keys_ii][0]
                right=morning_df[keys_ii][1]
                got_df=renaming_columns(df_going,right,1,file_num_1)
                morning_df[keys_ii][0]=got_df     
        else:
            pass


    morning_df = {key_mapping.get(old_key, old_key): value for old_key, value in morning_df.items()}

    keys_output=list(morning_df.keys())
    print(keys_output)


    return Morning_row_index,morning_df

def morning_SL_finding(df,Active_SL_call,Active_SL_put,input_index):
    global Market_trend

    keys_list_df=list(df.keys())
    print(f"Keys list is {keys_list_df}")
    console_output_log_recording(f"Keys list is {keys_list_df}")
    union_SL_List=Active_SL_call+Active_SL_put
    time=df[keys_list_df[0]][0].loc[input_index,"Time"]

    print(f"The target morning time is {time}")
    console_output_log_recording(f"The target morning time is {time}")

    if Market_trend=="Trending Up":
        for ii in range(len(keys_list_df)):
            if df[keys_list_df[ii]][1]=="Call":
                string_1=keys_list_df[ii]
                substring_to_remove_CE = "df_CE_"
                file_num_1=string_1.replace(substring_to_remove_CE,"")
                file_num_1=int(file_num_1)

                close_CE=df[keys_list_df[ii]][0].loc[input_index,f"close CE {file_num_1}"]
                time=df[keys_list_df[ii]][0].loc[input_index,"Time"]
                if close_CE>=Active_SL_call[0]:
                    Active_SL_call[0]=close_CE
                    print(f"Time: {time} The Updated SL is: {Active_SL_call[0]}")
                    console_output_log_recording(f"Time: {time} The Updated SL is: {Active_SL_call[0]}")
                else:
                    pass
            elif df[keys_list_df[ii]][1]=="Put":
                string_2=keys_list_df[ii]
                substring_to_remove_PE = "df_PE_"
                file_num_2=string_2.replace(substring_to_remove_PE,"")
                file_num_2=int(file_num_2)

                close_PE=df[keys_list_df[ii]][0].loc[input_index,f"close PE {file_num_2}"]
                time=df[keys_list_df[ii]][0].loc[input_index,"Time"]
                if close_PE>=Active_SL_put[ii-1]:
                    
                    print(f"Time: {time} The Updated SL is: {Active_SL_put[ii-1]} and close PE is {close_PE}")
                    Active_SL_put[ii-1]=close_PE
                    console_output_log_recording(f"Time: {time} The Updated SL is: {Active_SL_put[ii-1]}")
                else:
                    pass
            else:
                pass


    elif Market_trend=="Trending Down":
        for ii in range(len(keys_list_df)):
            if df[keys_list_df[ii]][1]=="Call":
                string_1=keys_list_df[ii]
                substring_to_remove_CE = "df_CE_"
                file_num_1=string_1.replace(substring_to_remove_CE,"")
                file_num_1=int(file_num_1)

                close_CE=df[keys_list_df[ii]][0].loc[input_index,f"close CE {file_num_1}"]
                time=df[keys_list_df[ii]][0].loc[input_index,"Time"]
                if close_CE>=Active_SL_call[ii-1]:
                    Active_SL_call[ii-1]=close_CE
                    print(f"Time: {time} The Updated SL is: {Active_SL_call[ii-1]}")
                    console_output_log_recording(f"Time: {time} The Updated SL is: {Active_SL_call[ii-1]}")
                else:
                    pass
            elif df[keys_list_df[ii]][1]=="Put":
                string_2=keys_list_df[ii]
                substring_to_remove_PE = "df_PE_"
                file_num_2=string_2.replace(substring_to_remove_PE,"")
                file_num_2=int(file_num_2)

                close_PE=df[keys_list_df[ii]][0].loc[input_index,f"close PE {file_num_2}"]
                time=df[keys_list_df[ii]][0].loc[input_index,"Time"]
                if close_PE>=Active_SL_put[0]:
                    
                    print(f"Time: {time} The Updated SL is: {Active_SL_put[0]} and close PE is {close_PE}")
                    Active_SL_put[ii-1]=close_PE
                    console_output_log_recording(f"Time: {time} The Updated SL is: {Active_SL_put[0]}")
                else:
                    pass
            else:
                pass
    
    else:
        pass


    return Active_SL_call,Active_SL_put


def index_computation(key,Right):
    if Right=="CE":
        string_1 = key
        substring_to_remove_CE = "df_CE_"
        file_num_1 = string_1.replace(substring_to_remove_CE, "")
        file_num_1 = int(file_num_1)
        return file_num_1
    elif Right=="PE":
        string_1 = key
        substring_to_remove_PE = "df_PE_"
        file_num_1 = string_1.replace(substring_to_remove_PE, "")
        file_num_1 = int(file_num_1)
        return file_num_1
    else:
        pass



def routine_code(index_row,Active_call_Strike,Active_put_Strike,Active_Initial_Sold_premium_call,Active_Initial_Sold_premium_put,Active_SL_Call,Active_SL_Put,Day,Initial_day,Expiry_date): 
    global Net_P_L
    global Market_trend
    global run_len
    global df_call_init,df_put_init
    global rev
    global max_historical_call_credit_spread
    global max_historical_put_credit_spread
    global max_credit_spreads

    Initial_day = datetime.strptime(Initial_day, "%d-%b-%Y")
    current_day = Initial_day + timedelta(days=Day)
    while current_day.weekday() in [5, 6]:
        current_day += timedelta(days=1)

    output_date = current_day.strftime("%d-%b-%Y")
    previous_day.append(output_date)
    l_1=len(previous_day)

    if output_date==previous_day[l_1-2] and l_1>2:
        pass
    else:
        print(output_date)

        if output_date in holidays_date:
            pass
        else:
            path_date=f"{Access_path_date}/{output_date}/"
            path_expiry_date_recurring=f"{path_date}/NIFTY_{Expiry_date}/"

            if Day==0:
                rows=df_call_init.shape[0]
                rows_df_len=rows
                run_len=rows-index_row
                starting_point=1
            else:
                Morning_row_index,Morning_DF=morning_code(path_expiry_date_recurring,output_date,Active_call_Strike,Active_put_Strike)
                Morning_row_index=Morning_row_index-1
                keys_ll=list(Morning_DF.keys())
                rows=Morning_DF[keys_ll[0]][0].shape[0]
                rows_df_len=rows
                index_row=Morning_row_index
                run_len=rows-index_row
                if Market_trend=="Neutral":
                    for ii in keys_ll:
                        if Morning_DF[ii][1]=="Call":
                            df_call_init=Morning_DF[ii][0]
                        elif Morning_DF[ii][1]=="Put":
                            df_put_init=Morning_DF[ii][0]
                elif Market_trend=="Trending Up":
                    df_trending_up_dict=Morning_DF
                    count=-1
                    Active_SL_Call,Active_SL_Put=morning_SL_finding(df_trending_up_dict,Active_SL_Call,Active_SL_Put,Morning_row_index)
                elif Market_trend=="Trending Down":
                    df_trending_down_dict=Morning_DF
                    keys_kk=list(df_trending_down_dict.keys())
                    len_keys=len(keys_kk)
                    final_key=keys_kk[len_keys-1]
                    keys_kk.remove(final_key)
                    desired_order=[final_key]+keys_kk
                    df_trending_down_dict = {key: df_trending_down_dict[key] for key in desired_order}

                    keys_kk=list(df_trending_down_dict.keys())

                    count=-1

                    Active_SL_Call,Active_SL_Put=morning_SL_finding(df_trending_down_dict,Active_SL_Call,Active_SL_Put,Morning_row_index)
                else:
                    pass


            for i in range(run_len):

                if Market_trend=="Neutral":
                    CE_SL=Active_SL_Call[0]
                    PE_SL=Active_SL_Put[0]

                    ce_initial_Price=Active_Initial_Sold_premium_call[0]
                    pe_initial_Price=Active_Initial_Sold_premium_put[0]

                    CE_Current_pr=df_call_init.loc[(i+index_row),"high CE 1"]
                    PE_Current_pr_1=df_put_init.loc[(i+index_row),"high PE 1"]

                    CE_Current_pr_close=df_call_init.loc[(i+index_row),"close CE 1"]
                    PE_Current_pr_1_close=df_put_init.loc[(i+index_row),"close PE 1"]

                    Startjee_1_dict_Call[Call_Strike]=[CE_Current_pr,ce_initial_Price,CE_SL]
                    Startjee_1_dict_Put[Put_Strike]=[PE_Current_pr_1,pe_initial_Price,PE_SL]

                    CE_instantinious_pr=[CE_Current_pr_close]
                    PE_instantinious_pr=[PE_Current_pr_1_close]

                    if CE_Current_pr<CE_SL and PE_Current_pr_1<PE_SL:

                        call_premium_collected=ce_initial_Price-df_call_init.loc[(index_row+i),"close CE 1"]
                        put_premium_collected=pe_initial_Price-df_put_init.loc[(index_row+i),"close PE 1"]
                        Net_P_L=call_premium_collected+put_premium_collected
                        Net_P_L=Lot_size*Net_P_L
                        time=df_call_init.loc[(index_row+i),"Time"]

                        if Startjee_2==1:
                            pass
                        else:
                            SL_update(time,Active_Initial_Sold_premium_call,Active_Initial_Sold_premium_put,CE_instantinious_pr,PE_instantinious_pr,Active_call_Strike,Active_put_Strike,Active_SL_Call,Active_SL_Put,reversal_status,Startjee_1_dict_Call,Startjee_1_dict_Put)
                        print(f"time: {time}, Initial_price CE: {round(ce_initial_Price,2)}, Current Price CE: {round(CE_Current_pr_close,2)}, Call Premium Collected: {round(call_premium_collected,2)}")
                        print(f"time: {time}, Initial_price PE: {round(pe_initial_Price,2)}, Current Price PE: {round(PE_Current_pr_1_close,2)}, Put Premium Collected: {round(put_premium_collected,2)}")
                        print(f"time: {time},Net Profit and Loss: {round(Net_P_L,2)}")

                        console_output_log_recording(f"time: {time}, Initial_price CE: {round(ce_initial_Price,2)}, Current Price CE: {round(CE_Current_pr_close,2)}, Call Premium Collected: {round(call_premium_collected,2)}")
                        console_output_log_recording(f"time: {time}, Initial_price PE: {round(pe_initial_Price,2)}, Current Price PE: {round(PE_Current_pr_1_close,2)}, Put Premium Collected: {round(put_premium_collected,2)}")
                        console_output_log_recording(f"time: {time},Net Profit and Loss: {round(Net_P_L,2)}")

                        #####################################  Analysis Code  #######################################
                        # Date_ana.append(output_date)
                        # Time_ana.append(time)
                        # Call_preimum_ana.append(call_premium_collected)
                        # Put_premium_ana.append(put_premium_collected)
                        # Net_Profit_loss_ana.append(Net_P_L)
                        # Call_CE_1_CP_ana.append(CE_Current_pr_close)
                        # SL_1_Call_ana.append(CE_SL)
                        # Call_CE_2_CP_ana.append(None)
                        # SL_2_Call_ana.append(None)
                        # Call_CE_3_CP_ana.append(None)
                        # SL_3_Call_ana.append(None)
                        # Call_CE_4_CP_ana.append(None)
                        # SL_4_Call_ana.append(None)

                        # Put_PE_1_CP_ana.append(PE_Current_pr_1_close)
                        # SL_1_Put_ana.append(PE_SL)
                        # Put_PE_2_CP_ana.append(None)
                        # SL_2_Put_ana.append(None)
                        # Put_PE_3_CP_ana.append(None)
                        # SL_3_Put_ana.append(None)
                        # Put_PE_4_CP_ana.append(None)
                        # SL_4_Put_ana.append(None)
                        #####################################  Analysis Code  #######################################

                    elif CE_Current_pr>=CE_SL and PE_Current_pr_1<PE_SL:
                        PE_Strike=Active_put_Strike[0]
                        CE_Strike=Active_call_Strike[0]

                        current_strike_CE=Active_call_Strike[0]
                        PE_Strike_2=PE_Strike+50
                        Market_trend="Trending Up"
                        Active_put_Strike.append(PE_Strike_2)

                        max_historical_put_credit_spread=len(Active_put_Strike)

                        call_premium_collected=ce_initial_Price-CE_SL
                        historical_realized_profit_loss["Call"]=historical_realized_profit_loss["Call"]+call_premium_collected

                        put_premium_collected=pe_initial_Price-PE_Current_pr_1_close
                        Net_P_L=call_premium_collected+put_premium_collected
                        Net_P_L=Lot_size*Net_P_L

                        time=df_call_init.loc[(index_row+i),"Time"]
                        Date=df_call_init.loc[(index_row+i),"Date"]
                        ts = pd.Timestamp(Date)
                        formatted_date = ts.strftime('%Y-%m-%d')
                        week=date_to_week(formatted_date)
                        running_log_update("SL_Hit","Call_stk_1",CE_Strike,"Call",time,formatted_date,week,formatted_Date_of_Init[k],formatted_Date_of_Expiry[k],0,0)

                        print(f"SL hit time: {time} Strike: {current_strike_CE}")
                        print(f"time: {time}, Initial_price CE: {round(ce_initial_Price,2)}, Current Price CE: {round(CE_SL,2)}, Call Premium Collected: {round(call_premium_collected,2)}")
                        print(f"time: {time}, Initial_price PE: {round(pe_initial_Price,2)}, Current Price PE: {round(PE_Current_pr_1_close,2)}, Put Premium Collected: {round(put_premium_collected,2)}")
                        print(f"time: {time},Net Profit and Loss: {round(Net_P_L,2)}")

                        console_output_log_recording(f"SL hit time: {time}")
                        console_output_log_recording(f"time: {time}, Initial_price CE: {round(ce_initial_Price,2)}, Current Price CE: {round(CE_SL,2)}, Call Premium Collected: {round(call_premium_collected,2)}")
                        console_output_log_recording(f"time: {time}, Initial_price PE: {round(pe_initial_Price,2)}, Current Price PE: {round(PE_Current_pr_1_close,2)}, Put Premium Collected: {round(put_premium_collected,2)}")
                        console_output_log_recording(f"time: {time},Net Profit and Loss: {round(Net_P_L,2)}")

                        # Date_ana.append(output_date)
                        # Time_ana.append(time)
                        # Call_preimum_ana.append(call_premium_collected)
                        # Put_premium_ana.append(put_premium_collected)
                        # Net_Profit_loss_ana.append(Net_P_L)
                        # Call_CE_1_CP_ana.append(CE_SL)
                        # SL_1_Call_ana.append(CE_SL)
                        # Call_CE_2_CP_ana.append(None)
                        # SL_2_Call_ana.append(None)
                        # Call_CE_3_CP_ana.append(None)
                        # SL_3_Call_ana.append(None)
                        # Call_CE_4_CP_ana.append(None)
                        # SL_4_Call_ana.append(None)

                        # Put_PE_1_CP_ana.append(PE_Current_pr_1_close)
                        # SL_1_Put_ana.append(PE_SL)
                        # Put_PE_2_CP_ana.append(None)
                        # SL_2_Put_ana.append(None)
                        # Put_PE_3_CP_ana.append(None)
                        # SL_3_Put_ana.append(None)
                        # Put_PE_4_CP_ana.append(None)
                        # SL_4_Put_ana.append(None)


                        rows_df_len,index_row,df_trending_up_dict,Active_call_Strike,Active_put_Strike,Active_Initial_Sold_premium_call,Active_Initial_Sold_premium_put,Active_SL_Call,Active_SL_Put=volatility_strike_pred(Date,time,path_expiry_date_recurring,Startjee_1_dict_Call,Startjee_1_dict_Put)
                        count=i


                    elif CE_Current_pr<CE_SL and PE_Current_pr_1>=PE_SL:
                        PE_Strike=Active_put_Strike[0]
                        CE_Strike=Active_call_Strike[0]

                        PE_Strike_1=PE_Strike
                        CE_Strike_2=CE_Strike-50
                        Market_trend="Trending Down"  
                        Active_call_Strike.append(CE_Strike_2) 

                        max_historical_call_credit_spread=len(Active_call_Strike)

                        put_premium_collected=pe_initial_Price-PE_SL
                        historical_realized_profit_loss["Put"]=historical_realized_profit_loss["Put"]+put_premium_collected

                        call_premium_collected=ce_initial_Price-CE_Current_pr_close
                        Net_P_L=call_premium_collected+put_premium_collected
                        Net_P_L=Lot_size*Net_P_L

                        time=df_call_init.loc[(index_row+i),"Time"]
                        Date=df_call_init.loc[(index_row+i),"Date"]
                        ts = pd.Timestamp(Date)
                        formatted_date = ts.strftime('%Y-%m-%d')
                        week=date_to_week(formatted_date)
                        print(week)

                        running_log_update("SL_Hit","Put_stk_1",PE_Strike,"Put",time,Date,week,formatted_Date_of_Init[k],formatted_Date_of_Expiry[k],0,0)

                        print(f"SL hit time: {time} Strike: {PE_Strike_1}")
                        print(f"time: {time}, Initial_price CE: {round(ce_initial_Price,2)}, Current Price CE: {round(CE_SL,2)}, Call Premium Collected: {round(call_premium_collected,2)}")
                        print(f"time: {time}, Initial_price PE: {round(pe_initial_Price,2)}, Current Price PE: {round(PE_Current_pr_1_close,2)}, Put Premium Collected: {round(put_premium_collected,2)}")
                        print(f"time: {time},Net Profit and Loss: {round(Net_P_L,2)}")

                        console_output_log_recording(f"SL hit time: {time}")
                        console_output_log_recording(f"time: {time}, Initial_price CE: {round(ce_initial_Price,2)}, Current Price CE: {round(CE_SL,2)}, Call Premium Collected: {round(call_premium_collected,2)}")
                        console_output_log_recording(f"time: {time}, Initial_price PE: {round(pe_initial_Price,2)}, Current Price PE: {round(PE_Current_pr_1_close,2)}, Put Premium Collected: {round(put_premium_collected,2)}")
                        console_output_log_recording(f"time: {time},Net Profit and Loss: {round(Net_P_L,2)}")


                        Date_ana.append(output_date)
                        Time_ana.append(time)
                        Call_preimum_ana.append(call_premium_collected)
                        Put_premium_ana.append(put_premium_collected)
                        Net_Profit_loss_ana.append(Net_P_L)
                        Call_CE_1_CP_ana.append(CE_SL)
                        SL_1_Call_ana.append(CE_SL)
                        Call_CE_2_CP_ana.append(None)
                        SL_2_Call_ana.append(None)
                        Call_CE_3_CP_ana.append(None)
                        SL_3_Call_ana.append(None)
                        Call_CE_4_CP_ana.append(None)
                        SL_4_Call_ana.append(None)

                        Put_PE_1_CP_ana.append(PE_Current_pr_1_close)
                        SL_1_Put_ana.append(PE_SL)
                        Put_PE_2_CP_ana.append(None)
                        SL_2_Put_ana.append(None)
                        Put_PE_3_CP_ana.append(None)
                        SL_3_Put_ana.append(None)
                        Put_PE_4_CP_ana.append(None)
                        SL_4_Put_ana.append(None)


                        rows_df_len,index_row,df_trending_down_dict,Active_call_Strike,Active_put_Strike,Active_Initial_Sold_premium_call,Active_Initial_Sold_premium_put,Active_SL_Call,Active_SL_Put=volatility_strike_pred(Date,time,path_expiry_date_recurring,Startjee_1_dict_Call,Startjee_1_dict_Put)
                        count=i
                        print(f"Active_call_Strike {Active_call_Strike}")
                        print(f"Active_put_Strike {Active_put_Strike}")

                    else:
                        pass

                elif Market_trend=="Trending Up":
                    union_strikes_list=Active_call_Strike+Active_put_Strike
                    keys_list=list(df_trending_up_dict.keys())
                    print(f"Present Date is: {output_date}")
                    console_output_log_recording(f"Present Date is: {output_date}")
                    multiple=len(Active_put_Strike)
                    Put_premium_collected=0
                    put_premium_collected_list=[]
                    PE_instantinious_pr=[]

                    if len(Active_put_Strike)==max_credit_spreads:
                        constant=1
                    else:
                        constant=0

                    print(union_strikes_list)

                    for j in range(len(union_strikes_list)):
                        print(f"len keys: {len(keys_list)} and j is {j}")
                        print(f"Searching key list {keys_list[j]}")
                        console_output_log_recording(f"len keys: {len(keys_list)} and j is {j}")
                        console_output_log_recording(f"Searching key list {keys_list[j]}")

                        if df_trending_up_dict[keys_list[j]][1]=="Call":

                            string_1=keys_list[j]
                            substring_to_remove_CE = "df_CE_"
                            file_num_1=string_1.replace(substring_to_remove_CE,"")
                            file_num_1=int(file_num_1)

                            CE_SL=Active_SL_Call[0]

                            if (i+index_row-count-1)<rows_df_len:

                                CE_current_High=df_trending_up_dict[keys_list[j]][0].loc[(i+index_row-count-1),f"high CE {file_num_1}"]
                                CE_current_close=df_trending_up_dict[keys_list[j]][0].loc[(i+index_row-count-1),f"close CE {file_num_1}"]
                                CE_initial_Price=Active_Initial_Sold_premium_call[0]
                                time=df_trending_up_dict[keys_list[j]][0].loc[(i+index_row-count-1),"Time"]

                                CE_instantinious_pr=[CE_current_close]
                                Startjee_1_dict_Call[Active_call_Strike[0]]=[CE_current_close,CE_initial_Price,CE_SL]

                                if CE_current_High<CE_SL:
                                    Call_premium_collected=CE_initial_Price-CE_current_close
                                    print(f"time: {time}, Initial_price CE: {round(CE_initial_Price,2)}, Current Price CE: {round(CE_current_close,2)}, Call Premium Collected: {round(Call_premium_collected,2)}")
                                    console_output_log_recording(f"time: {time}, Initial_price CE: {round(CE_initial_Price,2)}, Current Price CE: {round(CE_current_close,2)}, Call Premium Collected: {round(Call_premium_collected,2)}")
                                else:
                                    if rev==0 and max_historical_put_credit_spread<=max_credit_spreads:
                                        Call_premium_collected=CE_initial_Price-CE_SL
                                        historical_realized_profit_loss["Call"]=historical_realized_profit_loss["Call"]+Call_premium_collected
                                        CE_Strike=Active_call_Strike[0]
                                        time=df_trending_up_dict[keys_list[j]][0].loc[(i+index_row-count-1),"Time"]
                                        Date=df_trending_up_dict[keys_list[j]][0].loc[(i+index_row-count-1),"Date"]
                                        ts = pd.Timestamp(Date)
                                        Date = ts.strftime('%Y-%m-%d')
                                        week=date_to_week(Date)

                                        print(f"SL hit time: {time} Strike: {CE_Strike}")
                                        print(f"time: {time}, Initial_price CE: {round(CE_initial_Price,2)}, Current Price CE: {round(CE_SL,2)}, Call Premium Collected: {round(Call_premium_collected,2)}")

                                        console_output_log_recording(f"SL hit time: {time} Strike: {CE_Strike}")
                                        console_output_log_recording(f"time: {time}, Initial_price CE: {round(CE_initial_Price,2)}, Current Price CE: {round(CE_SL,2)}, Call Premium Collected: {round(Call_premium_collected,2)}")

                                        prev_len=len(Active_put_Strike)
                                        PE_STK=Active_put_Strike[multiple-1]
                                        Put_STK_NEW=PE_STK+50
                                        Active_put_Strike.append(Put_STK_NEW)

                                        max_historical_put_credit_spread=len(Active_put_Strike)

                                        running_log_update("SL_Hit",f"Call_stk_{prev_len}",CE_Strike,"Call",time,Date,week,formatted_Date_of_Init[k],formatted_Date_of_Expiry[k],0,0)

                                        rows_df_len,index_row,df_trending_up_dict,Active_call_Strike,Active_put_Strike,Active_Initial_Sold_premium_call,Active_Initial_Sold_premium_put,Active_SL_Call,Active_SL_Put=volatility_strike_pred(Date,time,path_expiry_date_recurring,Startjee_1_dict_Call,Startjee_1_dict_Put)
                                        union_strikes_list=Active_call_Strike+Active_put_Strike
                                        keys_list=list(df_trending_up_dict.keys())
                                        count=i

                                        if len(Active_put_Strike)>=max_credit_spreads:
                                            Call_premium_collected=0
                                            CE_instantinious_pr=[]


                                        for jj in range(len(Active_put_Strike)):
                                            if len(Active_put_Strike)<=(max_credit_spreads-1):
                                                PE_current_close=df_trending_up_dict[keys_list[jj+1]][0].loc[(i+index_row-count-1),f"close PE {jj+1}"]
                                                PE_instantinious_pr.insert((jj-1),PE_current_close)
                                            else:
                                                PE_current_close=df_trending_up_dict[keys_list[jj]][0].loc[(i+index_row-count-1),f"close PE {jj}"]
                                                PE_instantinious_pr.insert((jj-1),PE_current_close)    

                                    elif rev==1 and max_historical_put_credit_spread<=max_credit_spreads:
                                        Call_premium_collected=CE_initial_Price-CE_SL
                                        historical_realized_profit_loss["Call"]=historical_realized_profit_loss["Call"]+Call_premium_collected
                                        CE_Strike=Active_call_Strike[0]
                                        time=df_trending_up_dict[keys_list[j]][0].loc[(i+index_row-count-1),"Time"]
                                        Date=df_trending_up_dict[keys_list[j]][0].loc[(i+index_row-count-1),"Date"]
                                        ts = pd.Timestamp(Date)
                                        Date = ts.strftime('%Y-%m-%d')

                                        week=date_to_week(Date)   
                                        running_log_update("SL_Hit",f"Call_stk_{max_historical_put_credit_spread}",CE_Strike,"Call",time,Date,week,formatted_Date_of_Init[k],formatted_Date_of_Expiry[k],0,0)

                                        Active_call_Strike.remove(CE_Strike)   
                                        union_strikes_list.remove(CE_Strike)     
                                        df_trending_up_dict.pop(keys_list[j])
                                        keys_list=list(df_trending_up_dict.keys())

                                        print(f"Call credit spread removed after reversal for strike {CE_Strike}")   

                                        if len(Active_put_Strike)>=max_credit_spreads:
                                            Call_premium_collected=0
                                            CE_instantinious_pr=[]

                                        console_output_log_recording(f"Call premium collected at the time of the sl hit {Call_premium_collected}")

                                        for jj in range(len(Active_put_Strike)):
                                            if len(Active_put_Strike)<=(max_credit_spreads-1) and len(Active_call_Strike)!=0:
                                                file_num_1 = index_computation(keys_list[jj+1],"PE")

                                                PE_current_close=df_trending_up_dict[keys_list[jj+1]][0].loc[(i+index_row-count-1),f"close PE {file_num_1}"]
                                                PE_instantinious_pr.insert((jj-1),PE_current_close)
                                            elif len(Active_put_Strike)<=(max_credit_spreads-1) and len(Active_call_Strike)==0:
                                                file_num_1 = index_computation(keys_list[jj],"PE")

                                                PE_current_close=df_trending_up_dict[keys_list[jj]][0].loc[(i+index_row-count-1),f"close PE {file_num_1}"]
                                                PE_instantinious_pr.insert((jj-1),PE_current_close)   

                                            else:
                                                file_num_1 = index_computation(keys_list[jj],"PE")

                                                PE_current_close=df_trending_up_dict[keys_list[jj]][0].loc[(i+index_row-count-1),f"close PE {file_num_1}"]
                                                PE_instantinious_pr.insert((jj-1),PE_current_close)   

                                        break

                                    else:
                                        pass                                      
                            else:
                                pass

                        elif df_trending_up_dict[keys_list[j]][1]=="Put":
                            string_2=keys_list[j]
                            substring_to_remove_PE = "df_PE_"
                            file_num_2=string_2.replace(substring_to_remove_PE,"")
                            file_num_2=int(file_num_2)

                            if (i+index_row-count-1)<rows_df_len:
                                PE_SL=Active_SL_Put[j-1+constant]
                                PE_current_High=df_trending_up_dict[keys_list[j]][0].loc[(i+index_row-count-1),f"high PE {file_num_2}"]
                                PE_current_close=df_trending_up_dict[keys_list[j]][0].loc[(i+index_row-count-1),f"close PE {file_num_2}"]
                                PE_initial_Price=Active_Initial_Sold_premium_put[j-1+constant]
                                time=df_trending_up_dict[keys_list[j]][0].loc[(i+index_row-count-1),"Time"]


                                PE_instantinious_pr.insert((j-1+constant),PE_current_close)
                                Startjee_1_dict_Put[Active_put_Strike[j-1+constant]]=[PE_current_close,PE_initial_Price,PE_SL]

                                if PE_current_High<PE_SL:
                                    Put_premium_collected=Put_premium_collected+PE_initial_Price-PE_current_close
                                    print(f"time: {time}, Initial_price PE: {round(PE_initial_Price,2)}, Current Price PE: {round(PE_current_close,2)}, Put Premium Collected: {round(Put_premium_collected,2)}")
                                    console_output_log_recording(f"time: {time}, Initial_price PE: {round(PE_initial_Price,2)}, Current Price PE: {round(PE_current_close,2)}, Put Premium Collected: {round(Put_premium_collected,2)}")

                                    instantiniuos_put_premium_collected=PE_initial_Price-PE_current_close
                                    instantiniuos_put_premium_collected=round(instantiniuos_put_premium_collected,2)
                                    put_premium_collected_list.insert((j-1+constant),instantiniuos_put_premium_collected)

                                elif PE_current_High>=PE_SL:
                                    Put_premium_collected=Put_premium_collected+PE_initial_Price-PE_SL
                                    historical_realized_profit_loss["Put"]=historical_realized_profit_loss["Put"]+PE_initial_Price-PE_SL

                                    instantiniuos_put_premium_collected=PE_initial_Price-PE_SL
                                    instantiniuos_put_premium_collected=round(instantiniuos_put_premium_collected,2)
                                    put_premium_collected_list.insert((j-1+constant),instantiniuos_put_premium_collected)

                                    time=df_trending_up_dict[keys_list[j]][0].loc[(i+index_row-count-1),"Time"]
                                    Date=df_trending_up_dict[keys_list[j]][0].loc[(i+index_row-count-1),"Date"]
                                    ts = pd.Timestamp(Date)
                                    Date = ts.strftime('%Y-%m-%d')
                                    week=date_to_week(Date)

                                    Strike_remove_PE=df_trending_up_dict[keys_list[j]][2]
                                    PE_Strike=Strike_remove_PE

                                    print(f"SL hit time: {time} Strike: {PE_Strike}")
                                    print(f"time: {time}, Initial_price PE: {round(PE_initial_Price,2)}, Current Price PE: {round(PE_SL,2)}, Put Premium Collected: {round(Put_premium_collected,2)}")

                                    console_output_log_recording(f"SL hit time: {time} Strike: {PE_Strike}")
                                    console_output_log_recording(f"time: {time}, Initial_price PE: {round(PE_initial_Price,2)}, Current Price PE: {round(PE_SL,2)}, Put Premium Collected: {round(Put_premium_collected,2)}")

                                    running_log_update("SL_Hit",f"Put_stk_{file_num_2}",PE_Strike,"Put",time,Date,week,formatted_Date_of_Init[k],formatted_Date_of_Expiry[k],0,0)
                                    
                                    Active_put_Strike.remove(Strike_remove_PE)
                                    Active_Initial_Sold_premium_put.remove(PE_initial_Price)
                                    Active_SL_Put.remove(PE_SL)
                                    rev=1

                                    union_strikes_list.remove(Strike_remove_PE)
                                    df_trending_up_dict.pop(keys_list[j])
                                    keys_list=list(df_trending_up_dict.keys())
                                    j=len(union_strikes_list)-1

                                    for j in range(len(union_strikes_list)):
                                        if df_trending_up_dict[keys_list[j]][1]=="Put":
                                            string_2=keys_list[j]
                                            substring_to_remove_PE = "df_PE_"
                                            file_num_2=string_2.replace(substring_to_remove_PE,"")
                                            file_num_2=int(file_num_2)

                                            PE_SL=Active_SL_Put[j-1+constant]
                                            PE_current_High=df_trending_up_dict[keys_list[j]][0].loc[(i+index_row-count-1),f"high PE {file_num_2}"]
                                            PE_current_close=df_trending_up_dict[keys_list[j]][0].loc[(i+index_row-count-1),f"close PE {file_num_2}"]
                                            PE_initial_Price=Active_Initial_Sold_premium_put[j-1+constant]
                                            time=df_trending_up_dict[keys_list[j]][0].loc[(i+index_row-count-1),"Time"]

                                            PE_instantinious_pr.insert((j-1+constant),PE_current_close)
                                            Startjee_1_dict_Put[Active_put_Strike[j-1+constant]]=[PE_current_close,PE_initial_Price,PE_SL]

                                    break
                                else:
                                    pass
                            else:
                                pass
                        else:
                            pass

                    if max_historical_put_credit_spread>=max_credit_spreads:
                        Call_premium_collected=0
                        CE_instantinious_pr=[]
                        CE_SL=0
                    else:
                        pass

                    if (i+index_row-count-1)<rows_df_len and len(union_strikes_list)!=0:
                        time=df_trending_up_dict[keys_list[j]][0].loc[(i+index_row-count-1),"Time"]
                        Net_P_L=Call_premium_collected+Put_premium_collected+historical_realized_profit_loss["Call"]+historical_realized_profit_loss["Put"]
                        Net_P_L=Lot_size*Net_P_L
                        if Startjee_2==1:
                            pass
                        else:
                            SL_update(time,Active_Initial_Sold_premium_call,Active_Initial_Sold_premium_put,CE_instantinious_pr,PE_instantinious_pr,Active_call_Strike,Active_put_Strike,Active_SL_Call,Active_SL_Put,reversal_status,Startjee_1_dict_Call,Startjee_1_dict_Put)
                        historical_CE_premium_collected=round(historical_realized_profit_loss['Call'],2)
                        historical_PE_premium_collected=round(historical_realized_profit_loss['Put'],2)
                        print(f"time: {time},Net Profit and Loss: {round(Net_P_L,2)}, Historical realized profit Call: {historical_CE_premium_collected}, Historical realized profit Put: {historical_PE_premium_collected}")
                        print(f"Instantinious Put premium collected list: {put_premium_collected_list}")

                        console_output_log_recording(f"time: {time},Net Profit and Loss: {round(Net_P_L,2)}, Historical realized profit Call: {historical_CE_premium_collected}, Historical realized profit Put: {historical_PE_premium_collected}")
                        console_output_log_recording(f"Instantinious Put premium collected list: {put_premium_collected_list}")

                    #####################################  Analysis Code  #######################################
                        # Date_ana.append(output_date)
                        # Time_ana.append(time)
                        # Call_preimum_ana.append(Call_premium_collected)
                        # Put_premium_ana.append(Put_premium_collected)
                        # Net_Profit_loss_ana.append(Net_P_L)
                        # if len(Active_put_Strike)==2:
                        #     Call_CE_1_CP_ana.append(CE_instantinious_pr[0])
                        #     SL_1_Call_ana.append(Active_SL_Call[0])
                        #     Call_CE_2_CP_ana.append(None)
                        #     SL_2_Call_ana.append(None)
                        #     Call_CE_3_CP_ana.append(None)
                        #     SL_3_Call_ana.append(None)
                        #     Call_CE_4_CP_ana.append(None)
                        #     SL_4_Call_ana.append(None)

                        #     Put_PE_1_CP_ana.append(PE_instantinious_pr[0])
                        #     SL_1_Put_ana.append(Active_SL_Put[0])
                        #     Put_PE_2_CP_ana.append(PE_instantinious_pr[1])
                        #     SL_2_Put_ana.append(Active_SL_Put[1])
                        #     Put_PE_3_CP_ana.append(None)
                        #     SL_3_Put_ana.append(None)
                        #     Put_PE_4_CP_ana.append(None)
                        #     SL_4_Put_ana.append(None)
                        # elif len(Active_put_Strike)==3:
                        #     Call_CE_1_CP_ana.append(CE_instantinious_pr[0])
                        #     SL_1_Call_ana.append(Active_SL_Call[0])
                        #     Call_CE_2_CP_ana.append(None)
                        #     SL_2_Call_ana.append(None)
                        #     Call_CE_3_CP_ana.append(None)
                        #     SL_3_Call_ana.append(None)
                        #     Call_CE_4_CP_ana.append(None)
                        #     SL_4_Call_ana.append(None)

                        #     Put_PE_1_CP_ana.append(PE_instantinious_pr[0])
                        #     SL_1_Put_ana.append(Active_SL_Put[0])
                        #     Put_PE_2_CP_ana.append(PE_instantinious_pr[1])
                        #     SL_2_Put_ana.append(Active_SL_Put[1])
                        #     Put_PE_3_CP_ana.append(PE_instantinious_pr[2])
                        #     SL_3_Put_ana.append(Active_SL_Put[2])
                        #     Put_PE_4_CP_ana.append(None)
                        #     SL_4_Put_ana.append(None)
                        # elif len(Active_put_Strike)==4:
                        #     Call_CE_1_CP_ana.append(None)
                        #     SL_1_Call_ana.append(None)
                        #     Call_CE_2_CP_ana.append(None)
                        #     SL_2_Call_ana.append(None)
                        #     Call_CE_3_CP_ana.append(None)
                        #     SL_3_Call_ana.append(None)
                        #     Call_CE_4_CP_ana.append(None)
                        #     SL_4_Call_ana.append(None)


                        #     Put_PE_1_CP_ana.append(PE_instantinious_pr[0])
                        #     SL_1_Put_ana.append(Active_SL_Put[0])
                        #     Put_PE_2_CP_ana.append(PE_instantinious_pr[1])
                        #     SL_2_Put_ana.append(Active_SL_Put[1])
                        #     Put_PE_3_CP_ana.append(PE_instantinious_pr[2])
                        #     SL_3_Put_ana.append(Active_SL_Put[2])
                        #     Put_PE_4_CP_ana.append(PE_instantinious_pr[3])
                        #     SL_4_Put_ana.append(Active_SL_Put[3])
                        # elif len(Active_put_Strike)==3 and rev==1:
                        #     Call_CE_1_CP_ana.append(CE_instantinious_pr[0])
                        #     SL_1_Call_ana.append(Active_SL_Call[0])
                        #     Call_CE_2_CP_ana.append(None)
                        #     SL_2_Call_ana.append(None)
                        #     Call_CE_3_CP_ana.append(None)
                        #     SL_3_Call_ana.append(None)
                        #     Call_CE_4_CP_ana.append(None)
                        #     SL_4_Call_ana.append(None)

                        #     Put_PE_1_CP_ana.append(PE_instantinious_pr[0])
                        #     SL_1_Put_ana.append(Active_SL_Put[0])
                        #     Put_PE_2_CP_ana.append(PE_instantinious_pr[1])
                        #     SL_2_Put_ana.append(Active_SL_Put[1])
                        #     Put_PE_3_CP_ana.append(PE_instantinious_pr[2])
                        #     SL_3_Put_ana.append(Active_SL_Put[2])
                        #     Put_PE_4_CP_ana.append(None)
                        #     SL_4_Put_ana.append(None)

                        # elif len(Active_put_Strike)==2 and rev==1:
                        #     Call_CE_1_CP_ana.append(CE_instantinious_pr[0])
                        #     SL_1_Call_ana.append(Active_SL_Call[0])
                        #     Call_CE_2_CP_ana.append(None)
                        #     SL_2_Call_ana.append(None)
                        #     Call_CE_3_CP_ana.append(None)
                        #     SL_3_Call_ana.append(None)
                        #     Call_CE_4_CP_ana.append(None)
                        #     SL_4_Call_ana.append(None)

                        #     Put_PE_1_CP_ana.append(PE_instantinious_pr[0])
                        #     SL_1_Put_ana.append(Active_SL_Put[0])
                        #     Put_PE_2_CP_ana.append(PE_instantinious_pr[1])
                        #     SL_2_Put_ana.append(Active_SL_Put[1])
                        #     Put_PE_3_CP_ana.append(None)
                        #     SL_3_Put_ana.append(None)
                        #     Put_PE_4_CP_ana.append(None)
                        #     SL_4_Put_ana.append(None)

                        # elif len(Active_put_Strike)==1 and rev==1:
                        #     Call_CE_1_CP_ana.append(CE_instantinious_pr[0])
                        #     SL_1_Call_ana.append(Active_SL_Call[0])
                        #     Call_CE_2_CP_ana.append(None)
                        #     SL_2_Call_ana.append(None)
                        #     Call_CE_3_CP_ana.append(None)
                        #     SL_3_Call_ana.append(None)
                        #     Call_CE_4_CP_ana.append(None)
                        #     SL_4_Call_ana.append(None)

                        #     Put_PE_1_CP_ana.append(PE_instantinious_pr[0])
                        #     SL_1_Put_ana.append(Active_SL_Put[0])
                        #     Put_PE_2_CP_ana.append(None)
                        #     SL_2_Put_ana.append(None)
                        #     Put_PE_3_CP_ana.append(None)
                        #     SL_3_Put_ana.append(None)
                        #     Put_PE_4_CP_ana.append(None)
                        #     SL_4_Put_ana.append(None)

                        # elif len(Active_put_Strike)==0 and rev==1:
                        #     Call_CE_1_CP_ana.append(CE_instantinious_pr[0])
                        #     SL_1_Call_ana.append(Active_SL_Call[0])
                        #     Call_CE_2_CP_ana.append(None)
                        #     SL_2_Call_ana.append(None)
                        #     Call_CE_3_CP_ana.append(None)
                        #     SL_3_Call_ana.append(None)
                        #     Call_CE_4_CP_ana.append(None)
                        #     SL_4_Call_ana.append(None)

                        #     Put_PE_1_CP_ana.append(None)
                        #     SL_1_Put_ana.append(None)
                        #     Put_PE_2_CP_ana.append(None)
                        #     SL_2_Put_ana.append(None)
                        #     Put_PE_3_CP_ana.append(None)
                        #     SL_3_Put_ana.append(None)
                        #     Put_PE_4_CP_ana.append(None)
                        #     SL_4_Put_ana.append(None)
                        # else:
                        #     pass
                    elif len(union_strikes_list)==0:
                        Net_P_L=historical_realized_profit_loss["Call"]+historical_realized_profit_loss["Put"]
                        Net_P_L=Lot_size*Net_P_L
                        historical_CE_premium_collected=round(historical_realized_profit_loss['Call'],2)
                        historical_PE_premium_collected=round(historical_realized_profit_loss['Put'],2)
                        print(f"time: {time},Net Profit and Loss: {round(Net_P_L,2)}, Historical realized profit Call: {historical_CE_premium_collected}, Historical realized profit Put: {historical_PE_premium_collected}")
                        print(f"Instantinious Put premium collected list: {put_premium_collected_list}")

                        console_output_log_recording(f"time: {time},Net Profit and Loss: {round(Net_P_L,2)}, Historical realized profit Call: {historical_CE_premium_collected}, Historical realized profit Put: {historical_PE_premium_collected}")
                        console_output_log_recording(f"Instantinious Put premium collected list: {put_premium_collected_list}")
                        break
                    #####################################  Analysis Code  #######################################

                    
                elif Market_trend == "Trending Down":
                    union_strikes_list =Active_put_Strike + Active_call_Strike
                    keys_list = list(df_trending_down_dict.keys())
                    print(f"Present Date is: {output_date}")
                    print(f"The Key list is {keys_list}")
                    console_output_log_recording(f"Present Date is: {output_date}")
                    console_output_log_recording(f"The Key list is {keys_list}")
                    multiple = len(Active_call_Strike)
                    Call_premium_collected = 0
                    call_premium_collected_list = []
                    CE_instantinious_pr = []

                    if len(Active_call_Strike) == max_credit_spreads:
                        constant = 1
                    else:
                        constant = 0

                    print(union_strikes_list)

                    for j in range(len(union_strikes_list)):

                        if df_trending_down_dict[keys_list[j]][1] == "Call":

                            string_1 = keys_list[j]
                            substring_to_remove_CE = "df_CE_"
                            file_num_1 = string_1.replace(substring_to_remove_CE, "")
                            file_num_1 = int(file_num_1)

                            if (i + index_row - count - 1) < rows_df_len:
                                CE_SL = Active_SL_Call[j - 1 + constant]
                                CE_current_High = df_trending_down_dict[keys_list[j]][0].loc[(i + index_row - count - 1), f"high CE {file_num_1}"]
                                CE_current_close = df_trending_down_dict[keys_list[j]][0].loc[(i + index_row - count - 1), f"close CE {file_num_1}"]
                                CE_initial_Price = Active_Initial_Sold_premium_call[j - 1 + constant]
                                time = df_trending_down_dict[keys_list[j]][0].loc[(i + index_row - count - 1), "Time"]

                                CE_instantinious_pr.insert((j - 1 + constant), CE_current_close)
                                Startjee_1_dict_Call[Active_call_Strike[j - 1 + constant]] = [CE_current_close,CE_initial_Price, CE_SL]


                                if CE_current_High < CE_SL:
                                    Call_premium_collected = Call_premium_collected + CE_initial_Price - CE_current_close
                                    print(f"time: {time}, Initial_price CE: {round(CE_initial_Price, 2)}, Current Price CE: {round(CE_current_close, 2)}, Call Premium Collected: {round(Call_premium_collected, 2)}")
                                    console_output_log_recording(f"time: {time}, Initial_price CE: {round(CE_initial_Price, 2)}, Current Price CE: {round(CE_current_close, 2)}, Call Premium Collected: {round(Call_premium_collected, 2)}")

                                    instantiniuos_call_premium_collected = CE_initial_Price - CE_current_close
                                    instantiniuos_call_premium_collected = round(instantiniuos_call_premium_collected, 2)
                                    call_premium_collected_list.insert((j - 1 + constant),instantiniuos_call_premium_collected)


                                elif CE_current_High >= CE_SL:
                                    Call_premium_collected = Call_premium_collected + CE_initial_Price - CE_SL
                                    historical_realized_profit_loss["Call"] = historical_realized_profit_loss["Call"] + CE_initial_Price - CE_SL

                                    instantiniuos_call_premium_collected = CE_initial_Price - CE_SL
                                    instantiniuos_call_premium_collected = round(instantiniuos_call_premium_collected, 2)
                                    call_premium_collected_list.insert((j - 1 + constant),instantiniuos_call_premium_collected)

                                    time = df_trending_down_dict[keys_list[j]][0].loc[(i + index_row - count - 1), "Time"]
                                    Date = df_trending_down_dict[keys_list[j]][0].loc[(i + index_row - count - 1), "Date"]
                                    ts = pd.Timestamp(Date)
                                    Date = ts.strftime('%Y-%m-%d')
                                    week = date_to_week(Date)

                                    Strike_remove_CE = df_trending_down_dict[keys_list[j]][2]
                                    CE_Strike = Strike_remove_CE

                                    print(f"SL hit time: {time} Strike: {CE_Strike}")
                                    print(f"time: {time}, Initial_price CE: {round(CE_initial_Price, 2)}, Current Price CE: {round(CE_SL, 2)}, Call Premium Collected: {round(Call_premium_collected, 2)}")

                                    console_output_log_recording(f"SL hit time: {time} Strike: {CE_Strike}")
                                    console_output_log_recording(f"time: {time}, Initial_price CE: {round(CE_initial_Price, 2)}, Current Price CE: {round(CE_SL, 2)}, Call Premium Collected: {round(Call_premium_collected, 2)}")

                                    running_log_update("SL_Hit", f"Call_stk_{file_num_1}", CE_Strike, "Call", time, Date,week, formatted_Date_of_Init[k], formatted_Date_of_Expiry[k], 0,0)

                                    Active_call_Strike.remove(Strike_remove_CE)
                                    Active_Initial_Sold_premium_call.remove(CE_initial_Price)
                                    Active_SL_Call.remove(CE_SL)
                                    rev = 1


                                    union_strikes_list.remove(Strike_remove_CE)
                                    df_trending_down_dict.pop(keys_list[j])
                                    keys_list = list(df_trending_down_dict.keys())
                                    j=len(union_strikes_list)-1

                                    for j in range(len(union_strikes_list)):
                                        if df_trending_down_dict[keys_list[j]][1] == "Call":
                                            string_1 = keys_list[j]
                                            substring_to_remove_CE = "df_CE_"
                                            file_num_1 = string_1.replace(substring_to_remove_CE, "")
                                            file_num_1 = int(file_num_1)

                                            CE_SL = Active_SL_Call[j - 1 + constant]
                                            CE_current_High = df_trending_down_dict[keys_list[j]][0].loc[(i + index_row - count - 1), f"high CE {file_num_1}"]
                                            CE_current_close = df_trending_down_dict[keys_list[j]][0].loc[(i + index_row - count - 1), f"close CE {file_num_1}"]
                                            CE_initial_Price = Active_Initial_Sold_premium_call[j - 1 + constant]
                                            time = df_trending_down_dict[keys_list[j]][0].loc[(i + index_row - count - 1), "Time"]

                                            CE_instantinious_pr.insert((j - 1 + constant), CE_current_close)
                                            Startjee_1_dict_Call[Active_call_Strike[j - 1 + constant]] = [CE_current_close,CE_initial_Price, CE_SL]

                                    break
                                else:
                                    pass

                            else:
                                pass

                        elif df_trending_down_dict[keys_list[j]][1] == "Put":
                            string_2 = keys_list[j]
                            substring_to_remove_PE = "df_PE_"
                            file_num_2 = string_2.replace(substring_to_remove_PE, "")
                            file_num_2 = int(file_num_2)

                            PE_SL = Active_SL_Put[0]

                            if (i + index_row - count - 1) < rows_df_len:

                                PE_current_High = df_trending_down_dict[keys_list[j]][0].loc[(i + index_row - count - 1), f"high PE {file_num_2}"]
                                PE_current_close = df_trending_down_dict[keys_list[j]][0].loc[(i + index_row - count - 1), f"close PE {file_num_2}"]
                                PE_initial_Price = Active_Initial_Sold_premium_put[0]
                                time = df_trending_down_dict[keys_list[j]][0].loc[(i + index_row - count - 1), "Time"]

                                PE_instantinious_pr = [PE_current_close]
                                Startjee_1_dict_Put[Active_put_Strike[0]] = [PE_current_close, PE_initial_Price,PE_SL]

                                if PE_current_High < PE_SL:
                                    Put_premium_collected = PE_initial_Price - PE_current_close
                                    print(f"time: {time}, Initial_price PE: {round(PE_initial_Price, 2)}, Current Price PE: {round(PE_current_close, 2)}, Put Premium Collected: {round(Put_premium_collected, 2)}")
                                    console_output_log_recording(f"time: {time}, Initial_price PE: {round(PE_initial_Price, 2)}, Current Price PE: {round(PE_current_close, 2)}, Put Premium Collected: {round(Put_premium_collected, 2)}")

                                else:
                                    if rev == 0 and max_historical_call_credit_spread <= max_credit_spreads:
                                        Put_premium_collected = PE_initial_Price - PE_SL
                                        historical_realized_profit_loss["Put"] = historical_realized_profit_loss["Put"] + Put_premium_collected
                                        PE_Strike = Active_put_Strike[0]
                                        time = df_trending_down_dict[keys_list[j]][0].loc[(i + index_row - count - 1), "Time"]
                                        Date = df_trending_down_dict[keys_list[j]][0].loc[(i + index_row - count - 1), "Date"]
                                        ts = pd.Timestamp(Date)
                                        Date = ts.strftime('%Y-%m-%d')
                                        week = date_to_week(Date)

                                        print(f"SL hit time: {time} Strike: {PE_Strike}")
                                        print(f"time: {time}, Initial_price PE: {round(PE_initial_Price, 2)}, Current Price PE: {round(PE_SL, 2)}, Put Premium Collected: {round(Put_premium_collected, 2)}")

                                        console_output_log_recording(f"SL hit time: {time} Strike: {PE_Strike}")
                                        console_output_log_recording(f"time: {time}, Initial_price PE: {round(PE_initial_Price, 2)}, Current Price PE: {round(PE_SL, 2)}, Put Premium Collected: {round(Put_premium_collected, 2)}")

                                        prev_len = len(Active_call_Strike)
                                        CE_STK = Active_call_Strike[multiple - 1]
                                        Call_STK_NEW = CE_STK - 50
                                        Active_call_Strike.append(Call_STK_NEW)

                                        max_historical_call_credit_spread = len(Active_call_Strike)

                                        running_log_update("SL_Hit", f"Put_stk_{prev_len}", PE_Strike, "Put", time,Date, week, formatted_Date_of_Init[k],formatted_Date_of_Expiry[k], 0, 0)

                                        rows_df_len, index_row, df_trending_down_dict, Active_call_Strike, Active_put_Strike, Active_Initial_Sold_premium_call, Active_Initial_Sold_premium_put, Active_SL_Call, Active_SL_Put = volatility_strike_pred(Date, time, path_expiry_date_recurring, Startjee_1_dict_Call,Startjee_1_dict_Put)
                                        union_strikes_list = Active_put_Strike + Active_call_Strike
                                        keys_list = list(df_trending_down_dict.keys())
                                        count = i

                                        if len(Active_call_Strike) >= max_credit_spreads:
                                            Put_premium_collected = 0
                                            PE_instantinious_pr = []

                                        for jj in range(len(Active_call_Strike)):
                                            if len(Active_call_Strike) <= (max_credit_spreads - 1):
                                                CE_current_close = df_trending_down_dict[keys_list[jj + 1]][0].loc[(i + index_row - count - 1), f"close CE {jj + 1}"]
                                                CE_instantinious_pr.insert((jj - 1), CE_current_close)
                                            else:
                                                CE_current_close = df_trending_down_dict[keys_list[jj]][0].loc[(i + index_row - count - 1), f"close CE {jj}"]
                                                CE_instantinious_pr.insert((jj - 1), CE_current_close)


                                    elif rev == 1 and max_historical_call_credit_spread <= max_credit_spreads:
                                        Put_premium_collected = PE_initial_Price - PE_SL
                                        historical_realized_profit_loss["Put"] = historical_realized_profit_loss["Put"] + Put_premium_collected
                                        PE_Strike = Active_put_Strike[0]
                                        time = df_trending_down_dict[keys_list[j]][0].loc[(i + index_row - count - 1), "Time"]
                                        Date = df_trending_down_dict[keys_list[j]][0].loc[(i + index_row - count - 1), "Date"]
                                        ts = pd.Timestamp(Date)
                                        Date = ts.strftime('%Y-%m-%d')

                                        week = date_to_week(Date)
                                        running_log_update("SL_Hit", f"Put_stk_{max_historical_call_credit_spread}",PE_Strike, "Put", time, Date, week,formatted_Date_of_Init[k], formatted_Date_of_Expiry[k], 0, 0)

                                        Active_put_Strike.remove(PE_Strike)
                                        union_strikes_list.remove(PE_Strike)
                                        df_trending_down_dict.pop(keys_list[j])
                                        keys_list = list(df_trending_down_dict.keys())

                                        print(f"Put credit spread removed after reversal for strike {PE_Strike} and key list is {keys_list}")

                                        if len(Active_call_Strike) >= max_credit_spreads:
                                            Put_premium_collected = 0
                                            PE_instantinious_pr = []

                                        console_output_log_recording(f"Put premium collected at the time of the sl hit {Put_premium_collected}")

                                        for jj in range(len(Active_call_Strike)):
                                            if len(Active_call_Strike) <= (max_credit_spreads - 1) and len(Active_put_Strike)!=0:
                                                file_num_1 = index_computation(keys_list[jj+1],"CE")

                                                CE_current_close = df_trending_down_dict[keys_list[jj + 1]][0].loc[(i + index_row - count - 1), f"close CE {file_num_1}"]
                                                CE_instantinious_pr.insert((jj - 1), CE_current_close)
                                            elif len(Active_call_Strike) <= (max_credit_spreads - 1) and len(Active_put_Strike)==0:
                                                file_num_1 = index_computation(keys_list[jj],"CE")

                                                CE_current_close = df_trending_down_dict[keys_list[jj]][0].loc[(i + index_row - count - 1), f"close CE {file_num_1}"]
                                                CE_instantinious_pr.insert((jj - 1), CE_current_close)
                                            else:
                                                file_num_1 = index_computation(keys_list[jj],"CE")

                                                CE_current_close = df_trending_down_dict[keys_list[jj]][0].loc[(i + index_row - count - 1), f"close CE {file_num_1}"]
                                                CE_instantinious_pr.insert((jj - 1), CE_current_close)

                                        break

                                    else:
                                        pass
                            else:
                                pass


                    if max_historical_call_credit_spread >= max_credit_spreads:
                        Put_premium_collected = 0
                        PE_instantinious_pr = []
                        PE_SL = 0
                    else:
                        pass

                    print(f"Max historical call {max_historical_call_credit_spread} and max credit spread {max_credit_spreads} and reversal is {rev}")
                    if (i + index_row - count - 1) < rows_df_len and len(union_strikes_list)!=0:
                        time = df_trending_down_dict[keys_list[j]][0].loc[(i + index_row - count - 1), "Time"]
                        Net_P_L = Call_premium_collected + Put_premium_collected + historical_realized_profit_loss[
                            "Call"] + historical_realized_profit_loss["Put"]
                        Net_P_L = Lot_size * Net_P_L
                        if Startjee_2==1:
                            pass
                        else:
                            SL_update(time, Active_Initial_Sold_premium_call, Active_Initial_Sold_premium_put,
                                  CE_instantinious_pr, PE_instantinious_pr, Active_call_Strike, Active_put_Strike,
                                  Active_SL_Call, Active_SL_Put, reversal_status, Startjee_1_dict_Call,
                                  Startjee_1_dict_Put)
                        historical_CE_premium_collected = round(historical_realized_profit_loss['Call'], 2)
                        historical_PE_premium_collected = round(historical_realized_profit_loss['Put'], 2)
                        print(f"time: {time},Net Profit and Loss: {round(Net_P_L, 2)}, Historical realized profit Call: {historical_CE_premium_collected}, Historical realized profit Put: {historical_PE_premium_collected}")
                        print(f"Instantinious Call premium collected list: {call_premium_collected_list}")

                        console_output_log_recording(f"time: {time},Net Profit and Loss: {round(Net_P_L, 2)}, Historical realized profit Call: {historical_CE_premium_collected}, Historical realized profit Put: {historical_PE_premium_collected}")
                        console_output_log_recording(f"Instantinious Call premium collected list: {call_premium_collected_list}")

                        #####################################  Analysis Code  #######################################
                        # Date_ana.append(output_date)
                        # Time_ana.append(time)
                        # Call_preimum_ana.append(Call_premium_collected)
                        # Put_premium_ana.append(Put_premium_collected)
                        # Net_Profit_loss_ana.append(Net_P_L)
                        # if len(Active_call_Strike) == 2:
                        #     Call_CE_1_CP_ana.append(CE_instantinious_pr[0])
                        #     SL_1_Call_ana.append(Active_SL_Call[0])
                        #     Call_CE_2_CP_ana.append(CE_instantinious_pr[1])
                        #     SL_2_Call_ana.append(Active_SL_Call[1])
                        #     Call_CE_3_CP_ana.append(None)
                        #     SL_3_Call_ana.append(None)
                        #     Call_CE_4_CP_ana.append(None)
                        #     SL_4_Call_ana.append(None)

                        #     Put_PE_1_CP_ana.append(PE_instantinious_pr[0])
                        #     SL_1_Put_ana.append(Active_SL_Put[0])
                        #     Put_PE_2_CP_ana.append(None)
                        #     SL_2_Put_ana.append(None)
                        #     Put_PE_3_CP_ana.append(None)
                        #     SL_3_Put_ana.append(None)
                        #     Put_PE_4_CP_ana.append(None)
                        #     SL_4_Put_ana.append(None)
                        # elif len(Active_call_Strike) == 3:
                        #     Call_CE_1_CP_ana.append(CE_instantinious_pr[0])
                        #     SL_1_Call_ana.append(Active_SL_Call[0])
                        #     Call_CE_2_CP_ana.append(CE_instantinious_pr[1])
                        #     SL_2_Call_ana.append(Active_SL_Call[1])
                        #     Call_CE_3_CP_ana.append(CE_instantinious_pr[2])
                        #     SL_3_Call_ana.append(Active_SL_Call[2])
                        #     Call_CE_4_CP_ana.append(None)
                        #     SL_4_Call_ana.append(None)

                        #     Put_PE_1_CP_ana.append(PE_instantinious_pr[0])
                        #     SL_1_Put_ana.append(Active_SL_Put[0])
                        #     Put_PE_2_CP_ana.append(None)
                        #     SL_2_Put_ana.append(None)
                        #     Put_PE_3_CP_ana.append(None)
                        #     SL_3_Put_ana.append(None)
                        #     Put_PE_4_CP_ana.append(None)
                        #     SL_4_Put_ana.append(None)
                        # elif len(Active_call_Strike) == 4:
                        #     Call_CE_1_CP_ana.append(CE_instantinious_pr[0])
                        #     SL_1_Call_ana.append(Active_SL_Call[0])
                        #     Call_CE_2_CP_ana.append(CE_instantinious_pr[1])
                        #     SL_2_Call_ana.append(Active_SL_Call[1])
                        #     Call_CE_3_CP_ana.append(CE_instantinious_pr[2])
                        #     SL_3_Call_ana.append(Active_SL_Call[2])
                        #     Call_CE_4_CP_ana.append(CE_instantinious_pr[3])
                        #     SL_4_Call_ana.append(Active_SL_Call[3])

                        #     Put_PE_1_CP_ana.append(None)
                        #     SL_1_Put_ana.append(None)
                        #     Put_PE_2_CP_ana.append(None)
                        #     SL_2_Put_ana.append(None)
                        #     Put_PE_3_CP_ana.append(None)
                        #     SL_3_Put_ana.append(None)
                        #     Put_PE_4_CP_ana.append(None)
                        #     SL_4_Put_ana.append(None)
                        # elif len(Active_call_Strike) == 3 and rev == 1:
                        #     Call_CE_1_CP_ana.append(CE_instantinious_pr[0])
                        #     SL_1_Call_ana.append(Active_SL_Call[0])
                        #     Call_CE_2_CP_ana.append(CE_instantinious_pr[1])
                        #     SL_2_Call_ana.append(Active_SL_Call[1])
                        #     Call_CE_3_CP_ana.append(CE_instantinious_pr[2])
                        #     SL_3_Call_ana.append(Active_SL_Call[2])
                        #     Call_CE_4_CP_ana.append(None)
                        #     SL_4_Call_ana.append(None)

                        #     Put_PE_1_CP_ana.append(PE_instantinious_pr[0])
                        #     SL_1_Put_ana.append(Active_SL_Put[0])
                        #     Put_PE_2_CP_ana.append(None)
                        #     SL_2_Put_ana.append(None)
                        #     Put_PE_3_CP_ana.append(None)
                        #     SL_3_Put_ana.append(None)
                        #     Put_PE_4_CP_ana.append(None)
                        #     SL_4_Put_ana.append(None)

                        # elif len(Active_call_Strike) == 2 and rev == 1:
                        #     Call_CE_1_CP_ana.append(CE_instantinious_pr[0])
                        #     SL_1_Call_ana.append(Active_SL_Call[0])
                        #     Call_CE_2_CP_ana.append(CE_instantinious_pr[1])
                        #     SL_2_Call_ana.append(Active_SL_Call[1])
                        #     Call_CE_3_CP_ana.append(None)
                        #     SL_3_Call_ana.append(None)
                        #     Call_CE_4_CP_ana.append(None)
                        #     SL_4_Call_ana.append(None)

                        #     Put_PE_1_CP_ana.append(PE_instantinious_pr[0])
                        #     SL_1_Put_ana.append(Active_SL_Put[0])
                        #     Put_PE_2_CP_ana.append(None)
                        #     SL_2_Put_ana.append(None)
                        #     Put_PE_3_CP_ana.append(None)
                        #     SL_3_Put_ana.append(None)
                        #     Put_PE_4_CP_ana.append(None)
                        #     SL_4_Put_ana.append(None)

                        # elif len(Active_call_Strike) == 1 and rev == 1:
                        #     Call_CE_1_CP_ana.append(CE_instantinious_pr[0])
                        #     SL_1_Call_ana.append(Active_SL_Call[0])
                        #     Call_CE_2_CP_ana.append(None)
                        #     SL_2_Call_ana.append(None)
                        #     Call_CE_3_CP_ana.append(None)
                        #     SL_3_Call_ana.append(None)
                        #     Call_CE_4_CP_ana.append(None)
                        #     SL_4_Call_ana.append(None)

                        #     Put_PE_1_CP_ana.append(PE_instantinious_pr[0])
                        #     SL_1_Put_ana.append(Active_SL_Put[0])
                        #     Put_PE_2_CP_ana.append(None)
                        #     SL_2_Put_ana.append(None)
                        #     Put_PE_3_CP_ana.append(None)
                        #     SL_3_Put_ana.append(None)
                        #     Put_PE_4_CP_ana.append(None)
                        #     SL_4_Put_ana.append(None)

                        # elif len(Active_call_Strike) == 0 and rev == 1:
                        #     Call_CE_1_CP_ana.append(None)
                        #     SL_1_Call_ana.append(None)
                        #     Call_CE_2_CP_ana.append(None)
                        #     SL_2_Call_ana.append(None)
                        #     Call_CE_3_CP_ana.append(None)
                        #     SL_3_Call_ana.append(None)
                        #     Call_CE_4_CP_ana.append(None)
                        #     SL_4_Call_ana.append(None)

                        #     Put_PE_1_CP_ana.append(PE_instantinious_pr[0])
                        #     SL_1_Put_ana.append(Active_SL_Put[0])
                        #     Put_PE_2_CP_ana.append(None)
                        #     SL_2_Put_ana.append(None)
                        #     Put_PE_3_CP_ana.append(None)
                        #     SL_3_Put_ana.append(None)
                        #     Put_PE_4_CP_ana.append(None)
                        #     SL_4_Put_ana.append(None)
                        # else:
                        #     pass
                    elif len(union_strikes_list)==0:
                        Net_P_L = historical_realized_profit_loss["Call"] + historical_realized_profit_loss["Put"]
                        Net_P_L = Lot_size * Net_P_L
                        historical_CE_premium_collected = round(historical_realized_profit_loss['Call'], 2)
                        historical_PE_premium_collected = round(historical_realized_profit_loss['Put'], 2)
                        print(f"time: {time},Net Profit and Loss: {round(Net_P_L, 2)}, Historical realized profit Call: {historical_CE_premium_collected}, Historical realized profit Put: {historical_PE_premium_collected}")
                        print(f"Instantinious Call premium collected list: {call_premium_collected_list}")

                        console_output_log_recording(f"time: {time},Net Profit and Loss: {round(Net_P_L, 2)}, Historical realized profit Call: {historical_CE_premium_collected}, Historical realized profit Put: {historical_PE_premium_collected}")
                        console_output_log_recording(f"Instantinious Call premium collected list: {call_premium_collected_list}")
                        break
                    #####################################  Analysis Code  #######################################


                else:
                    pass



start_time = datetime.strptime("9:14", "%H:%M")
end_time = datetime.strptime("15:30", "%H:%M")

# Define the interval (3 minutes)
interval = timedelta(minutes=5)

# Initialize an empty list to store the generated times
time_list = []

# Generate the times
current_time = start_time
while current_time <= end_time:
    time_list.append(current_time.strftime("%H:%M"))
    current_time += interval


for k in range(len(formatted_Date_of_Init)):
    if formatted_Date_of_Expiry[k] in Rejected_Expiry_Dates:
        pass
    else:
        start_date = datetime.strptime(formatted_Date_of_Init[k], "%d-%b-%Y")
        end_date = datetime.strptime(formatted_Date_of_Expiry[k], "%d-%b-%Y")
        num_days=(end_date-start_date).days+1
        print(num_days)
        Active_call_Strike=[]
        Active_put_Strike=[]
        Active_Initial_Sold_premium_call=[]
        Active_Initial_Sold_premium_put=[]
        Active_SL_Call=[]
        Active_SL_Put=[]
        previous_day=[]
        Active_status={}
        Market_trend="Neutral"
        Day=0
        Net_P_L=0
        reversal_status=None
        rev=0
        Len_ce=0
        Len_pe=0
        historical_realized_profit_loss={}
        historical_realized_profit_loss["Call"]=0
        historical_realized_profit_loss["Put"]=0
        max_historical_call_credit_spread=1
        max_historical_put_credit_spread=1

        with open(Path_backtest_Report+"active_status.txt", "w") as file:
            file.truncate()

        with open(Path_backtest_Report+'Back_testing_Console_output_log_file.txt', 'w') as file:
            file.truncate()

        
        for j in range(num_days):
            if Day==0:
                ############# Path Update ###################
                path_init_date=f"{Access_path_date}{formatted_Date_of_Init[k]}/"
                path_expiry_date=f"{path_init_date}NIFTY_{formatted_Date_of_Expiry[k]}/"

                ############# Extracting Closing Price from Initial Strike ###################
                Call_Strike=file_startjee.loc[k,"Call Strike"]
                Put_Strike=file_startjee.loc[k,"Put Strike"]
                Call_Strike=int(Call_Strike)
                Put_Strike=int(Put_Strike)
                


                file_call=f"NIFTY{str(Call_Strike)}_CE.csv"
                file_put=f"NIFTY{str(Put_Strike)}_PE.csv"

                df_call_init=pd.read_csv(path_expiry_date+file_call)
                df_put_init=pd.read_csv(path_expiry_date+file_put)

                if (len(df_call_init.loc[4,'Time']))>5:
                    df_call_init['Time'] = df_call_init['Time'].apply(lambda x: x[:5])
                    df_put_init['Time'] = df_put_init['Time'].apply(lambda x: x[:5])
                else:
                    pass

                df_CE_1=df_call_init
                df_PE_1=df_put_init
                df_call_init,df_put_init=merging(df_call_init,df_put_init,"Call","Put","df_CE_1","df_PE_1")

                date_str = formatted_Date_of_Init[k]
                date_obj = datetime.strptime(date_str, "%d-%b-%Y")
                Desired_Date = date_obj.strftime("%Y-%m-%d")

                row_index_call = df_call_init.index[(df_call_init['Time'] == Desired_time_CE)&(df_call_init['Date'] == Desired_Date)].tolist()
                row_index_put = df_put_init.index[(df_put_init['Time'] == Desired_time_PE)&(df_put_init['Date'] == Desired_Date)].tolist()

                print(f"Desired Date format: {Desired_Date} and type of it is {type(Desired_Date)}")
                week=date_to_week(Desired_Date)

                running_log_update("Entry","Call_stk_1",Call_Strike,"Call",Desired_time_CE,Desired_Date,week,formatted_Date_of_Init[k],formatted_Date_of_Expiry[k],0,0)
                running_log_update("Entry","Put_stk_1",Put_Strike,"Put",Desired_time_PE,Desired_Date,week,formatted_Date_of_Init[k],formatted_Date_of_Expiry[k],0,0)

                row_index_call=row_index_call[0]
                row_index_put=row_index_put[0]
                CE_price=df_call_init.loc[row_index_call,"close CE 1"]
                PE_price=df_put_init.loc[row_index_put,"close PE 1"]
                SL_CE=2*CE_price
                SL_PE=2*PE_price


                ####################  Updating the Status ####################################
                Active_call_Strike.append(Call_Strike)
                Active_put_Strike.append(Put_Strike)
                Active_Initial_Sold_premium_call.append(CE_price)
                Active_Initial_Sold_premium_put.append(PE_price)
                Active_SL_Call.append(SL_CE)
                Active_SL_Put.append(SL_PE)


                Active_status["Active_call_Strike"]=[Call_Strike]
                Active_status["Active_put_Strike"]=[Put_Strike]
                Active_status["Active_Initial_Sold_premium_call"]=[CE_price]
                Active_status["Active_Initial_Sold_premium_put"]=[PE_price]

                Active_status["Deactive Put Strike"]=[]
                Active_status["Deactive Put Strike Premium Initial"]=[]
                Active_status["Deactive Call Strike"]=[]
                Active_status["Deactive Call Strike Premium Initial"]=[]
                
                writing_Active_status(Active_status)

                
                index_row=row_index_call
                Initial_day=formatted_Date_of_Init[k]
                Expiry_date=formatted_Date_of_Expiry[k]

                print(f"Length of the Call Strike is {Active_call_Strike} Length of the Put Strike is {Active_put_Strike}")
                routine_code(index_row,Active_call_Strike,Active_put_Strike,Active_Initial_Sold_premium_call,Active_Initial_Sold_premium_put,Active_SL_Call,Active_SL_Put,Day,Initial_day,Expiry_date)
                Day=Day+1
            
            else:
                union_strike_list_computed=Active_call_Strike+Active_put_Strike
                if len(union_strike_list_computed)!=0:
                    routine_code(index_row,Active_call_Strike,Active_put_Strike,Active_Initial_Sold_premium_call,Active_Initial_Sold_premium_put,Active_SL_Call,Active_SL_Put,Day,Initial_day,Expiry_date)
                    Day=Day+1
                elif len(union_strike_list_computed)==0:
                    print("All SL hit day End")

    margin_deployed=MARGIN_DEPLOYED

    Len_ce=max_historical_call_credit_spread
    Len_pe=max_historical_put_credit_spread

    final_log(Initial_day,Expiry_date,Market_trend,Net_P_L,margin_deployed,Len_ce,Len_pe,rev,"Call_stk_1","Put_stk_1")


    input_list=[date_init,date_exp,market_sentiment,Call_stk_1,Call_stk_2,Call_stk_3,Call_stk_4,Put_stk_1,Put_stk_2,Put_stk_3,Put_stk_4,sl_hit_time,sl_hit_date,sl_hit_week,Entry_time_call,Entry_time_put,
                Entry_date,Entry_week,profit_loss,Margin,ROI,Net_Credit_Spread_Call,Net_Credit_Spread_Put,Net_Credit_Spread,reverse]

    equalized_lists = equalize_lists(input_list)

final_data={"Date of Initiation":date_init,"Date of Expiry":date_exp,"Market Sentiment":market_sentiment,
            "CE Strike 1":Call_stk_1,"CE Strike 2":Call_stk_2,"CE Strike 3":Call_stk_3,"CE Strike 4":Call_stk_4,
            "PE Strike 1":Put_stk_1,"PE Strike 2":Put_stk_2,"PE Strike 3":Put_stk_3,"PE Strike 4":Put_stk_4,
            "SL hit Time":sl_hit_time,"SL hit Date":sl_hit_date,"SL hit Week":sl_hit_week,"Entry Time Call":Entry_time_call,
            "Entry Time Put":Entry_time_put,"Entry Time Date":Entry_date,"Entry Time Week":Entry_week,"Profit and Loss":profit_loss,
            "Margin Used":Margin,"Profit Loss percent":ROI,"Overall Credit Spread Call":Net_Credit_Spread_Call,"Overall Credit Spread Put":Net_Credit_Spread_Put,
            "Overall Credit Spread Used":Net_Credit_Spread,"Reversal Status":reverse}

# print(f"date_init: {len(equalized_lists[0])}")
# print(f"date_exp: {len(equalized_lists[1])}")
# print(f"market_sentiment: {len(equalized_lists[2])}")
# print(f"Call_stk_1: {len(equalized_lists[3])}")
# print(f"Call_stk_2: {len(equalized_lists[4])}")
# print(f"Call_stk_3: {len(equalized_lists[5])}")
# print(f"Call_stk_4: {len(equalized_lists[6])}")
# print(f"Put_stk_1: {len(equalized_lists[7])}")
# print(f"Put_stk_2: {len(equalized_lists[8])}")
# print(f"Put_stk_3: {len(equalized_lists[9])}")
# print(f"Put_stk_4: {len(equalized_lists[10])}")
# print(f"sl_hit_time: {len(equalized_lists[11])}")
# print(f"sl_hit_date: {len(equalized_lists[12])}")
# print(f"sl_hit_week: {len(equalized_lists[13])}")
# print(f"Entry_time_call: {len(equalized_lists[14])}")
# print(f"Entry_time_put: {len(equalized_lists[15])}")
# print(f"Entry_date: {len(equalized_lists[16])}")
# print(f"Entry_week: {len(equalized_lists[17])}")
# print(f"profit_loss: {len(equalized_lists[18])}")
# print(f"Margin: {len(equalized_lists[19])}")
# print(f"ROI: {len(equalized_lists[20])}")
# print(f"Net_Credit_Spread_Call: {len(equalized_lists[21])}")
# print(f"Net_Credit_Spread_Put: {len(equalized_lists[22])}")
# print(f"Net_Credit_Spread: {len(equalized_lists[23])}")
# print(f"reverse: {len(equalized_lists[24])}")


# print(f"date_init: {date_init}")
# print(f"date_exp: {date_exp}")
# print(f"market_sentiment: {market_sentiment}")
# print(f"Call_stk_1: {Call_stk_1}")
# print(f"Call_stk_2: {Call_stk_2}")
# print(f"Call_stk_3: {Call_stk_3}")
# print(f"Call_stk_4: {Call_stk_4}")
# print(f"Put_stk_1: {Put_stk_1}")
# print(f"Put_stk_2: {Put_stk_2}")
# print(f"Put_stk_3: {Put_stk_3}")
# print(f"Put_stk_4: {Put_stk_4}")
# print(f"sl_hit_time: {sl_hit_time}")
# print(f"sl_hit_date: {sl_hit_date}")
# print(f"sl_hit_week: {sl_hit_week}")
# print(f"Entry_time_call: {Entry_time_call}")
# print(f"Entry_time_put: {Entry_time_put}")
# print(f"Entry_date: {Entry_date}")
# print(f"Entry_week: {Entry_week}")
# print(f"profit_loss: {profit_loss}")
# print(f"Margin: {Margin}")
# print(f"ROI: {ROI}")
# print(f"Net_Credit_Spread_Call: {Net_Credit_Spread_Call}")
# print(f"Net_Credit_Spread_Put: {Net_Credit_Spread_Put}")
# print(f"Net_Credit_Spread: {Net_Credit_Spread}")
# print(f"reverse: {reverse}")

Analysis_data_output={"Date":Date_ana,"Time":Time_ana,"Net Profit and Loss":Net_Profit_loss_ana,"Call Premium Collected": Call_preimum_ana,"Put Premium Collected": Put_premium_ana,
                      "Close CE_1":Call_CE_1_CP_ana,"SL Call 1":SL_1_Call_ana,"Close CE_2":Call_CE_2_CP_ana,"SL Call 2":SL_2_Call_ana,"Close CE_3":Call_CE_3_CP_ana,"SL Call 3":SL_3_Call_ana,"Close CE_4":Call_CE_4_CP_ana,"SL Call 4":SL_4_Call_ana,
                      "Close PE_1":Put_PE_1_CP_ana,"SL Put 1":SL_1_Put_ana,"Close PE_2":Put_PE_2_CP_ana,"SL Put 2":SL_2_Put_ana,"Close PE_3":Put_PE_3_CP_ana,"SL Put 3":SL_3_Put_ana,"Close PE_4":Put_PE_4_CP_ana,"SL Put 4":SL_4_Put_ana}

Analysis_generated_df=pd.DataFrame(Analysis_data_output)
Analysis_generated_df.to_csv(Path_backtest_Report+"Analysis_generated_df.csv",index=False)

final_generated_DF=pd.DataFrame(final_data)
final_generated_DF.to_csv(Path_backtest_Report+"final_generated_DF.csv",index=False)