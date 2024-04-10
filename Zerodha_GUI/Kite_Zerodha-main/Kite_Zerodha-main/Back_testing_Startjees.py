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

Accepted_Expiry_Dates=["12-Mar-2020","09-Apr-2020","28-May-2020","19-Apr-2020","03-Dec-2020","28-Jan-2021","11-Mar-2021","01-Apr-2021","15-Apr-2021","22-Apr-2021","12-May-2021","22-Jul-2021","18-Aug-2021","03-Nov-2021","27-Jan-2022","03-Mar-2022","13-Apr-2022","05-May-2022","11-Aug-2022","18-Aug-2022","01-Sep-2022","06-Oct-2022","10-Nov-2022","26-Jan-2023","09-Mar-2023","30-Mar-2023","06-Apr-2023","04-May-2023","29-Jun-2023","17-Aug-2023","21-Sep-2023","05-Oct-2023","26-Oct-2023","16-Nov-2023","30-Nov-2023","28-Nov-2023"]
Rejected_Expiry_Dates=["27-Feb-2020","01-Apr-2020","16-Apr-2020","07-May-2020","08-Oct-2020","31-Dec-2020","08-Apr-2021","16-Apr-2021","21-Oct-2021","11-Nov-2021","25-Nov-2021","24-Mar-2022","21-Apr-2022","27-Oct-2022","13-Apr-2023","20-Apr-2023"]
holidays_date=[]


file_startjee=pd.read_excel(path_main+"Startjee.xlsx", sheet_name="Past_Backtesting")
Date_of_Init=file_startjee["Date of Initiation"].tolist()
Date_of_Expiry=file_startjee["Expiry"].tolist()

formatted_Date_of_Init = [date.strftime('%d-%b-%Y') for date in Date_of_Init]
formatted_Date_of_Expiry = [date.strftime('%d-%b-%Y') for date in Date_of_Expiry]

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


Startjee_1_dict_Call={}
Startjee_1_dict_Put={}

################### Variables of the startjee ##############
Desired_time_CE="09:20"
Desired_time_PE="09:20"
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
################### Variables of the startjee ##############


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




def volatility_strike_pred(Date,Time,path_expiry_date_recurring,Startjee_1_dict_Call,Startjee_1_dict_Put):
    global run_len
    global Market_trend
    global Active_call_Strike, Active_put_Strike
    global Active_Initial_Sold_premium_call, Active_Initial_Sold_premium_put
    global Active_SL_Call, Active_SL_Put

#######################################   OFFSET CALCULATION   ############################################################

    input_time_str = Time
    input_time = datetime.strptime(input_time_str, "%H:%M")
    time_list_dt = [datetime.strptime(time_str, "%H:%M") for time_str in time_list]
    closest_time_index = min(range(len(time_list_dt)), key=lambda i: abs(time_list_dt[i] - input_time))
    Triggered_time=time_list[closest_time_index]

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
    Strikes_dict["Call"]=Active_call_Strike
    Strikes_dict["Put"]=Active_put_Strike
#######################################   OFFSET CALCULATION   ############################################################

    if Market_trend=="Trending Up":
        max_len_pe=len(Active_put_Strike)

        print(Market_trend)

        if max_len_pe<=3:
            triggered_strike_put=Active_put_Strike[max_len_pe-1]
            triggered_strike_call=Active_call_Strike[0]+offset
            union_strikes_list=Active_call_Strike+Active_put_Strike
            over_all_len=len(union_strikes_list)
        else:
            triggered_strike_put=Active_put_Strike[max_len_pe-1]
            union_strikes_list=Active_put_Strike
            over_all_len=len(union_strikes_list)
            triggered_strike_call=None



        for i in range(over_all_len):
            Right=find_key(Strikes_dict,union_strikes_list[i])
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
                PE_strikes[f"file_PE_{i}"]=f'NIFTY{union_strikes_list[i]}_PE.csv'
                PE_strikes[f"df_PE_{i}"]=pd.read_csv(path_expiry_date_recurring+PE_strikes[f"file_PE_{i}"])

                if (len(PE_strikes[f"df_PE_{i}"].loc[4,'Time']))>5:
                    PE_strikes[f"df_PE_{i}"]['Time'] = PE_strikes[f"df_PE_{i}"]['Time'].apply(lambda x: x[:5])
                else:
                    pass

                df_trending_up_dict[f"df_PE_{i}"]=[PE_strikes[f"df_PE_{i}"],"Put",union_strikes_list[i]]

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
                index_row_CE = CE_strikes[keys_i].index[(CE_strikes[keys_i]['Time'] == Triggered_time) & (CE_strikes[keys_i]['Date'] == formatted_date)].tolist()
                index_row_CE=index_row_CE[0]
                CP_CE=CE_strikes[keys_i].loc[index_row_CE,f"close CE {resu}"]
                CP_CE_2,index_row_CE,time_obs_CE=Execution_check_Code(Triggered_time,formatted_date,index_row_CE,CP_CE,CE_strikes[keys_i],"CE",keys_i)

            if df_trending_up_dict[keys_i][2]==triggered_strike_put and df_trending_up_dict[keys_i][1]=="Put":
                print(f"Newly added Put Strike is {df_trending_up_dict[keys_i][2]}")
                string_repl=str(keys_i)
                resu=string_repl.replace("df_PE_", "")
                resu=int(resu)
                index_row_PE = PE_strikes[keys_i].index[(PE_strikes[keys_i]['Time'] == Triggered_time) & (PE_strikes[keys_i]['Date'] == formatted_date)].tolist()
                index_row_PE=index_row_PE[0]
                CP_PE=PE_strikes[keys_i].loc[index_row_PE,f"close PE {resu}"]
                CP_PE_2,index_row_PE,time_obs_PE=Execution_check_Code(Triggered_time,formatted_date,index_row_PE,CP_PE,PE_strikes[keys_i],"PE",keys_i)
            elif triggered_strike_call==None:
                pass

        CE_Strike_remove=Active_call_Strike[0]
        Initial_CE_remove=Active_Initial_Sold_premium_call[0]
        SL_CE_remove=Active_SL_Call[0]

        Startjee_1_dict_Call.pop(CE_Strike_remove)

        if max_len_pe<=3:
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
            run_len=rows-index_row

            return index_row,df_trending_up_dict,Active_call_Strike,Active_put_Strike,Active_Initial_Sold_premium_call,Active_Initial_Sold_premium_put,Active_SL_Call,Active_SL_Put
        else:
            SL_PE_2=2*CP_PE_2

            running_log_update("Entry",f"Call_stk_{max_len_pe}",triggered_strike_call,"Put",time_obs_CE,formatted_date,week,formatted_Date_of_Init[k],formatted_Date_of_Expiry[k],0,0)


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

            return index_row,df_trending_up_dict
        

    elif Market_trend=="Trending Down":
        max_len_ce=len(Active_call_Strike)

        if max_len_ce<=3:
            triggered_strike_call=Active_call_Strike[max_len_ce-1]
            triggered_strike_put=Active_put_Strike[0]-offset
            union_strikes_list=Active_put_Strike+Active_call_Strike
            over_all_len=len(union_strikes_list)
        else:
            triggered_strike_call=Active_call_Strike[max_len_ce-1]
            union_strikes_list=Active_call_Strike
            over_all_len=len(union_strikes_list)
            triggered_strike_put=None


        union_strikes_list=Active_put_Strike+Active_call_Strike
        over_all_len=len(union_strikes_list)

        for i in range(over_all_len):
            Right=find_key(Strikes_dict,union_strikes_list[i])
            if Right=="Call":
                CE_strikes[f"file_CE_{i}"]=f'NIFTY{union_strikes_list[i]}_CE.csv'
                CE_strikes[f"df_CE_{i}"]=pd.read_csv(path_expiry_date_recurring+CE_strikes[f"file_CE_{i}"])

                if (len(CE_strikes[f"df_CE_{i}"].loc[4,'Time']))>5:
                    CE_strikes[f"df_CE_{i}"]['Time'] = CE_strikes[f"df_CE_{i}"]['Time'].apply(lambda x: x[:5])
                else:
                    pass

                df_trending_down_dict[f"df_CE_{i}"]=[CE_strikes[f"df_CE_{i}"],"Call",union_strikes_list[i]]

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

            elif Right=="Put":
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

            else:
                pass

        key_list=list(df_trending_down_dict.keys())
        ts = pd.Timestamp(Date)
        formatted_date = ts.strftime('%Y-%m-%d')
        week=date_to_week(formatted_date)


        for keys_i in key_list:
            if df_trending_down_dict[keys_i][2]==triggered_strike_call and df_trending_down_dict[keys_i][1]=="Call":
                print(f"Newly added Call Strike is {df_trending_down_dict[keys_i][2]}")
                string_repl=str(keys_i)
                resu=string_repl.replace("df_CE_", "")
                resu=int(resu)
                index_row_CE = CE_strikes[keys_i].index[(CE_strikes[keys_i]['Time'] == Triggered_time) & (CE_strikes[keys_i]['Date'] == formatted_date)].tolist()
                index_row_CE=index_row_CE[0]
                CP_CE=CE_strikes[keys_i].loc[index_row_CE,f"close CE {resu}"]
                CP_CE_2,index_row_CE,time_obs_CE=Execution_check_Code(Triggered_time,formatted_date,index_row_CE,CP_CE,CE_strikes[keys_i],"CE",keys_i)

            if df_trending_down_dict[keys_i][2]==triggered_strike_put and df_trending_down_dict[keys_i][1]=="Put":
                Active_put_Strike.append(df_trending_down_dict[keys_i][2])
                print(f"Newly added Put Strike is {df_trending_down_dict[keys_i][2]}")
                string_repl=str(keys_i)
                resu=string_repl.replace("df_PE_", "")
                resu=int(resu)
                index_row_PE = PE_strikes[keys_i].index[(PE_strikes[keys_i]['Time'] == Triggered_time) & (PE_strikes[keys_i]['Date'] == formatted_date)].tolist()
                index_row_PE=index_row_PE[0]
                CP_PE=PE_strikes[keys_i].loc[index_row_PE,f"close PE {resu}"]
                CP_PE_2,index_row_PE,time_obs_PE=Execution_check_Code(Triggered_time,formatted_date,index_row_PE,CP_PE,PE_strikes[keys_i],"PE",keys_i)
            elif triggered_strike_put==None:
                pass






        PE_Strike_remove=Active_put_Strike[0]
        Initial_PE_remove=Active_Initial_Sold_premium_put[0]
        SL_PE_remove=Active_SL_Put[0]

        print(f"SL to remove {SL_PE_remove}")

        Startjee_1_dict_Put.pop(PE_Strike_remove)

        if max_len_ce<=3:
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

            return index_row,df_trending_down_dict
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

            return index_row,df_trending_down_dict


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


def routine_code(index_row,Active_call_Strike,Active_put_Strike,Active_Initial_Sold_premium_call,Active_Initial_Sold_premium_put,Active_SL_Call,Active_SL_Put,Day,Initial_day,Expiry_date):
    global Net_P_L
    global Market_trend
    global run_len

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
                run_len=rows-index_row
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
                        SL_update(time,Active_Initial_Sold_premium_call,Active_Initial_Sold_premium_put,CE_instantinious_pr,PE_instantinious_pr,Active_call_Strike,Active_put_Strike,Active_SL_Call,Active_SL_Put,reversal_status,Startjee_1_dict_Call,Startjee_1_dict_Put)
                        print(f"Premium collected on call side {round(call_premium_collected,2)} Premium collected on put side {round(put_premium_collected,2)}")
                        print(f"and net profit and loss is {round(Net_P_L,2)} SL for Call is {CE_SL} and SL for Put is {PE_SL} at time is {time}")

                    elif CE_Current_pr>=CE_SL and PE_Current_pr_1<PE_SL:
                        PE_Strike=Active_put_Strike[0]
                        CE_Strike=Active_call_Strike[0]

                        current_strike_CE=Active_call_Strike[0]
                        PE_Strike_2=PE_Strike+50
                        Market_trend="Trending Up"
                        Active_put_Strike.append(PE_Strike_2)

                        call_premium_collected=ce_initial_Price-CE_SL
                        put_premium_collected=pe_initial_Price-df_put_init.loc[(index_row+i+1),"close PE 1"]
                        Net_P_L=call_premium_collected+put_premium_collected
                        Net_P_L=Lot_size*Net_P_L

                        time=df_call_init.loc[(index_row+i),"Time"]
                        Date=df_call_init.loc[(index_row+i),"Date"]
                        ts = pd.Timestamp(Date)
                        formatted_date = ts.strftime('%Y-%m-%d')
                        week=date_to_week(formatted_date)
                        running_log_update("SL_Hit","Call_stk_1",CE_Strike,"Call",time,Date,week,formatted_Date_of_Init[k],formatted_Date_of_Expiry[k],0,0)

                        print(f"SL hit at time {time} at Profit and loss of {round(Net_P_L,2)}")

                        index_row,df_trending_up_dict,Active_call_Strike,Active_put_Strike,Active_Initial_Sold_premium_call,Active_Initial_Sold_premium_put,Active_SL_Call,Active_SL_Put=volatility_strike_pred(Date,time,path_expiry_date_recurring,Startjee_1_dict_Call,Startjee_1_dict_Put)

                        count=i


                    elif CE_Current_pr<CE_SL and PE_Current_pr_1>=PE_SL:
                        PE_Strike=Active_put_Strike[0]
                        CE_Strike=Active_call_Strike[0]

                        PE_Strike_1=PE_Strike
                        CE_Strike_2=CE_Strike-50
                        Market_trend="Trending Down"  
                        Active_call_Strike.append(CE_Strike_2)                 
                        time=df_call_init.loc[(index_row+i),"Time"]
                        Date=df_call_init.loc[(index_row+i),"Date"]
                        ts = pd.Timestamp(Date)
                        formatted_date = ts.strftime('%Y-%m-%d')
                        week=date_to_week(formatted_date)
                        print(week)

                        running_log_update("SL_Hit","Put_stk_1",PE_Strike,"Put",time,Date,week,formatted_Date_of_Init[k],formatted_Date_of_Expiry[k],0,0)

                        print(f"SL Hit time is {time}")

                        index_row,df_trending_down_dict=volatility_strike_pred(Date,time,path_expiry_date_recurring,Startjee_1_dict_Call,Startjee_1_dict_Put)
                        print(f"Active_call_Strike {Active_call_Strike}")
                        print(f"Active_put_Strike {Active_put_Strike}")

                    else:
                        pass

                elif Market_trend=="Trending Up":
                    union_strikes_list=Active_call_Strike+Active_put_Strike
                    keys_list=list(df_trending_up_dict.keys())

                    multiple=len(Active_put_Strike)
                    PE_instantinious_pr=[None]*multiple
                    Put_premium_collected=0

                    for j in range(len(union_strikes_list)):
                        if df_trending_up_dict[keys_list[j]][1]=="Call":
                            string_1=keys_list[j]
                            substring_to_remove_CE = "df_CE_"
                            file_num_1=string_1.replace(substring_to_remove_CE,"")
                            file_num_1=int(file_num_1)

                            CE_SL=Active_SL_Call[0]
                            CE_current_High=df_trending_up_dict[keys_list[j]][0].loc[(i+index_row-count-1),f"high CE {file_num_1}"]
                            CE_current_close=df_trending_up_dict[keys_list[j]][0].loc[(i+index_row-count-1),f"close CE {file_num_1}"]
                            CE_initial_Price=Active_Initial_Sold_premium_call[0]

                            CE_instantinious_pr=[CE_current_close]
                            Startjee_1_dict_Call[Active_call_Strike[0]]=[CE_current_close,CE_initial_Price,CE_SL]

                            if CE_current_High<CE_SL:
                                Call_premium_collected=CE_initial_Price-CE_current_close
                            else:
                                Call_premium_collected=CE_initial_Price-CE_SL
                                time=df_trending_up_dict[keys_list[j]][0].loc[(i+index_row-count-1),"Time"]
                                Date=df_trending_up_dict[keys_list[j]][0].loc[(i+index_row-count-1),"Date"]
                                PE_STK=Active_put_Strike[multiple-1]
                                Put_STK_NEW=PE_STK+50
                                Active_put_Strike.append(Put_STK_NEW)

                                index_row,df_trending_up_dict=volatility_strike_pred(Date,time,path_expiry_date_recurring,Startjee_1_dict_Call,Startjee_1_dict_Put)
                                union_strikes_list=Active_call_Strike+Active_put_Strike
                                keys_list=list(df_trending_up_dict.keys())
                                count=i


                        elif df_trending_up_dict[keys_list[j]][1]=="Put":
                            string_2=keys_list[j]
                            substring_to_remove_PE = "df_PE_"
                            file_num_2=string_2.replace(substring_to_remove_PE,"")
                            file_num_2=int(file_num_2)

                            PE_SL=Active_put_Strike[j-1]
                            PE_current_High=df_trending_up_dict[keys_list[j]][0].loc[(i+index_row-count-1),f"high PE {file_num_2}"]
                            PE_current_close=df_trending_up_dict[keys_list[j]][0].loc[(i+index_row-count-1),f"close PE {file_num_2}"]
                            PE_initial_Price=Active_Initial_Sold_premium_put[j-1]

                            PE_instantinious_pr.insert((j-1),PE_current_close)
                            Startjee_1_dict_Put[Active_put_Strike[j-1]]=[PE_current_close,PE_initial_Price,PE_SL]

                            if PE_current_High<PE_SL:
                                Put_premium_collected=Put_premium_collected+PE_initial_Price-PE_current_close
                            else:
                                Put_premium_collected=Put_premium_collected+PE_initial_Price-PE_SL
                                Strike_remove_PE=df_trending_up_dict[keys_list[j]][2]
                                union_strikes_list.remove(Strike_remove_PE)
                                df_trending_up_dict.pop(keys_list[j])
                                keys_list=list(df_trending_up_dict.keys())
                        else:
                            pass

                    Net_P_L=Call_premium_collected+Put_premium_collected
                    Net_P_L=Lot_size*Net_P_L
                    Call_premium_collected=Lot_size*Call_premium_collected
                    Put_premium_collected=Lot_size*Put_premium_collected
                    time=df_trending_up_dict[keys_list[j]][0].loc[(i+index_row-count-1),"Time"]
                    SL_update(time,Active_Initial_Sold_premium_call,Active_Initial_Sold_premium_put,CE_instantinious_pr,PE_instantinious_pr,Active_call_Strike,Active_put_Strike,Active_SL_Call,Active_SL_Put,reversal_status,Startjee_1_dict_Call,Startjee_1_dict_Put)

                    print(f"The the Net Profit and Loss is {round(Net_P_L,2)} at time is {time} and call SL is {CE_SL} and put SL 1 is {Active_SL_Put[0]} and put SL 2 is {Active_SL_Put[1]}")
                    print(f"Call Premium collected {round(Call_premium_collected,2)} at time is {time}")
                    print(f"Put Premium collected {round(Put_premium_collected,2)} at time is {time}")
                elif Market_trend=="Trending Down":
                    pass
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
        Len_ce=0
        Len_pe=0

        with open(Path_backtest_Report+"active_status.txt", "w") as file:
            file.truncate()
        
        for j in range(num_days):
            if Day==0:
                ############# Path Update ###################
                path_init_date=f"{Access_path_date}/{formatted_Date_of_Init[k]}/"
                path_expiry_date=f"{path_init_date}/NIFTY_{formatted_Date_of_Expiry[k]}/"

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


            #     ####################  Updating the Status ####################################
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


                routine_code(index_row,Active_call_Strike,Active_put_Strike,Active_Initial_Sold_premium_call,Active_Initial_Sold_premium_put,Active_SL_Call,Active_SL_Put,Day,Initial_day,Expiry_date)
                
                Day=Day+1


final_data={"Date of Initiation":date_init,"Date of Expiry":date_exp,"Market Sentiment":market_sentiment,
            "CE Strike 1":Call_stk_1,"CE Strike 2":Call_stk_2,"CE Strike 3":Call_stk_3,"CE Strike 4":Call_stk_4,
            "PE Strike 1":Put_stk_1,"PE Strike 2":Put_stk_2,"PE Strike 3":Put_stk_3,"PE Strike 4":Put_stk_4,
            "SL hit Time":sl_hit_time,"SL hit Date":sl_hit_date,"SL hit Week":sl_hit_week,"Entry Time Call":Entry_time_call,
            "Entry Time Put":Entry_time_put,"Entry Time Date":Entry_date,"Entry Time Week":Entry_week,"Profit and Loss":profit_loss,
            "Margin Used":Margin,"Profit Loss percent":ROI,"Overall Credit Spread Call":Net_Credit_Spread_Call,"Overall Credit Spread Put":Net_Credit_Spread_Put,
            "Overall Credit Spread Used":Net_Credit_Spread,"Reversal Status":reverse}

# print(f"date_init: {len(date_init)}")
# print(f"date_exp: {len(date_exp)}")
# print(f"market_sentiment: {len(market_sentiment)}")
# print(f"Call_stk_1: {len(Call_stk_1)}")
# print(f"Call_stk_2: {len(Call_stk_2)}")
# print(f"Call_stk_3: {len(Call_stk_3)}")
# print(f"Call_stk_4: {len(Call_stk_4)}")
# print(f"Put_stk_1: {len(Put_stk_1)}")
# print(f"Put_stk_2: {len(Put_stk_2)}")
# print(f"Put_stk_3: {len(Put_stk_3)}")
# print(f"Put_stk_4: {len(Put_stk_4)}")
# print(f"sl_hit_time: {len(sl_hit_time)}")
# print(f"sl_hit_date: {len(sl_hit_date)}")
# print(f"sl_hit_week: {len(sl_hit_week)}")
# print(f"Entry_time_call: {len(Entry_time_call)}")
# print(f"Entry_time_put: {len(Entry_time_put)}")
# print(f"Entry_date: {len(Entry_date)}")
# print(f"Entry_week: {len(Entry_week)}")
# print(f"profit_loss: {len(profit_loss)}")
# print(f"Margin: {len(Margin)}")
# print(f"ROI: {len(ROI)}")
# print(f"Net_Credit_Spread_Call: {len(Net_Credit_Spread_Call)}")
# print(f"Net_Credit_Spread_Put: {len(Net_Credit_Spread_Put)}")
# print(f"Net_Credit_Spread: {len(Net_Credit_Spread)}")
# print(f"reverse: {len(reverse)}")


# # print(f"Call_stk_1: {Call_stk_1}")
# # print(f"Call_stk_2: {Call_stk_2}")
# # print(f"Call_stk_3: {Call_stk_3}")
# # print(f"Call_stk_4: {Call_stk_4}")
# # print(f"Put_stk_1: {Put_stk_1}")
# # print(f"Put_stk_2: {Put_stk_2}")
# # print(f"Put_stk_3: {Put_stk_3}")
# # print(f"Put_stk_4: {Put_stk_4}")



final_generated_DF=pd.DataFrame(final_data)
final_generated_DF.to_csv(Path_backtest_Report+"final_generated_DF.csv",index=False)

            # else:

            #     routine_code(index_row,Active_call_Strike,Active_put_Strike,Active_Initial_Sold_premium_call,Active_Initial_Sold_premium_put,Active_SL_Call,Active_SL_Put,Day,Initial_day,Expiry_date)
            # #     margin_deployed=MARGIN_DEPLOYED
                
            # #     if reversal_status is not None:
            # #         rev=1
            # #     else:
            # #         rev=0

            # #     final_log(Initial_day,Expiry_date,Market_trend,Net_P_L,margin_deployed,Len_ce,Len_pe,rev,"Call_stk_1","Put_stk_1")
            #     Day=Day+1