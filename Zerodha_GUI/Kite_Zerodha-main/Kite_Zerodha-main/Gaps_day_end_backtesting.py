import pandas as pd
from datetime import datetime,timedelta
import os
import Black_scholes_model
import numpy as np
import warnings

warnings.filterwarnings('ignore')

Access_path_date="H:/My Drive/Daily_F_O_data/Options/Index/"
Accesst_path_Spot_IR="H:/My Drive/Daily_F_O_data/"
path_main="D:/ashu/Finance/algo_trading/Zerodha_GUI/Kite_Zerodha-main/Kite_Zerodha-main/"
path_spot_vol="H:/My Drive/Daily_F_O_data/Daily_closing_price_data/"
Path_backtest_Report="D:/ashu/Finance/algo_trading/Zerodha_GUI/Kite_Zerodha-main/Kite_Zerodha-main/Back_Test_Files_Report/"

Start_date="03-Jan-2020"
End_date="28-Jun-2024"

start_date = datetime.strptime(Start_date, "%d-%b-%Y")
end_date = datetime.strptime(End_date, "%d-%b-%Y")

# Initialize an empty list to store the dates
date_list = []

# Iterate over the range of dates
current_date = start_date
while current_date <= end_date:
    if current_date.weekday() < 5:  # Monday to Friday are 0 to 4
        date_list.append(current_date.strftime("%d-%b-%Y"))
    current_date += timedelta(days=1)

Nifty_daily_date=pd.read_csv(path_main+"Nifty_daily_data.csv")
date_nifty=Nifty_daily_date["Date"].tolist()
formatted_date_list = [datetime.strptime(date, "%d-%m-%Y").strftime("%d-%b-%Y") for date in date_nifty]
index_start_date=formatted_date_list.index(Start_date)
Nifty_target_date_list=formatted_date_list[index_start_date:]

Rejected_Expiry_Dates=[]
holidays_date=[]

for day in date_list:
  if day not in Nifty_target_date_list:
    Date=day
    date_object = datetime.strptime(Date, "%d-%b-%Y")
    day_of_week = date_object.strftime('%A')

    if day_of_week=="Friday":
      date_obj = datetime.strptime(day, "%d-%b-%Y")
      new_date_obj = date_obj + timedelta(days=6)
      new_date_str = new_date_obj.strftime("%d-%b-%Y")
      Rejected_Expiry_Dates.append(new_date_str)
    else:
      holidays_date.append(day)
  else:
    pass
  

file_startjee=pd.read_excel(path_main+"Startjee.xlsx", sheet_name="Past_Backtesting")
Date_of_Init=file_startjee["Date of Initiation"].tolist()
Date_of_Expiry=file_startjee["Expiry"].tolist()

formatted_Date_of_Init = [date.strftime('%d-%b-%Y') for date in Date_of_Init]
formatted_Date_of_Expiry = [date.strftime('%d-%b-%Y') for date in Date_of_Expiry]


Day_end_time="15:25"
Square_off_time="09:15"
Distance_between_strikes=50
size=1
Lot_size=50
Expiry_distance=1
Strikes_distance_from_spot=[0,1,2,3,4]
profit_strangle_distances = {}
Date_List_all=[]


def console_output_log_recording(content):

    with open(Path_backtest_Report+'Gap_up_and_Gap_down_log.txt', 'a') as file:
        file.write(f"{content}.\n")

def adding_last_row_df(df,right):
    column_names = list(df.columns)

    if right=="Call":
        right_string="CE"
    elif right=="Put":
        right_string="PE"
    else:
        pass

    closing_price_string=column_names[5]
    
    if f"close {right_string}" in column_names:
        number=None
    else:
        substring_to_remove_CE = f"close {right_string} "
        file_num_1=closing_price_string.replace(substring_to_remove_CE,"")
        file_num_1=int(file_num_1)
        number=file_num_1


    last_time_str = df['Time'].iloc[-1]
    last_time = datetime.strptime(last_time_str, '%H:%M')
    new_time = (last_time + timedelta(minutes=1)).strftime('%H:%M')
    new_date = df['Date'].iloc[-1]

    if number==None:
        closing_price=df[f"close {right_string}"].iloc[-1]
        new_row = {
        'Date': new_date,
        'Time': new_time,
        f'open {right_string}': closing_price,
        f'high {right_string}': closing_price,
        f'low {right_string}': closing_price,
        f'close {right_string}': closing_price,
        f'volume {right_string}': 0,
        f'oi {right_string}': 0
        }
    else:
        closing_price=df[f"close {right_string} {number}"].iloc[-1]
        new_row = {
        'Date': new_date,
        'Time': new_time,
        f'open {right_string} {number}': closing_price,
        f'high {right_string} {number}': closing_price,
        f'low {right_string} {number}': closing_price,
        f'close {right_string} {number}': closing_price,
        f'volume {right_string}': 0,
        f'oi {right_string}': 0
        }


    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)

    return df

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

      df_1=adding_last_row_df(df_1,Right_1)
      df_2=adding_last_row_df(df_2,Right_2)


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

      df_1=adding_last_row_df(df_1,Right_1)
      df_2=adding_last_row_df(df_2,Right_2)

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

      df_1=adding_last_row_df(df_1,Right_1)
      df_2=adding_last_row_df(df_2,Right_2)

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

      df_1=adding_last_row_df(df_1,Right_1)
      df_2=adding_last_row_df(df_2,Right_2)

      df_combined = pd.merge(df_1, df_2, on=['Date', 'Time'], how='outer')
      df_combined['Date'] = pd.to_datetime(df_combined['Date'])
      df_combined['Time'] = pd.to_datetime(df_combined['Time'], format='%H:%M').dt.strftime('%H:%M')
      df_combined = df_combined.sort_values(by=['Date', 'Time'])
      df_combined = df_combined.fillna(method='ffill')
      df_1=df_combined[['Date','Time',f'open PE {file_num_1}',f'high PE {file_num_1}',f'low PE {file_num_1}',f'close PE {file_num_1}',f'volume PE {file_num_1}',f'oi PE {file_num_1}']]
      df_2=df_combined[['Date','Time',f'open CE {file_num_2}',f'high CE {file_num_2}',f'low CE {file_num_2}',f'close CE {file_num_2}',f'volume CE {file_num_2}',f'oi CE {file_num_2}']]
      return df_1,df_2

def Average_determination(df_call,df_put,row_index_call,row_index_put,Day_end):

    if Day_end==1:              
        Open_CE=df_call.loc[row_index_call[0],'open CE 1']
        High_CE=df_call.loc[row_index_call[0],'high CE 1']
        Low_CE=df_call.loc[row_index_call[0],'low CE 1']
        Close_CE=df_call.loc[row_index_call[0],'close CE 1']

        Average_call_price=(Open_CE+High_CE+Low_CE+Close_CE)/4

        Open_PE=df_put.loc[row_index_put[0],'open PE 1']
        High_PE=df_put.loc[row_index_put[0],'high PE 1']
        Low_PE=df_put.loc[row_index_put[0],'low PE 1']
        Close_PE=df_put.loc[row_index_put[0],'close PE 1']

        Average_put_price=(Open_PE+High_PE+Low_PE+Close_PE)/4

        return Average_call_price,Average_put_price
    elif Day_end==0:
        Open_CE=df_call.loc[row_index_call[0],'open CE 1']
        Open_PE=df_put.loc[row_index_put[0],'open PE 1']

        return Open_CE,Open_PE

for ii in range(len(Strikes_distance_from_spot)):
    profit_strangle_distances[f"Profit_Strangle_distance_{ii}"]=[]

with open(Path_backtest_Report+'Gap_up_and_Gap_down_log.txt', 'w') as file:
    file.truncate()

formatted_Date_of_Expiry.append("04-Jul-2024")
formatted_Date_of_Expiry.append("11-Jul-2024")

for k in range(len(formatted_Date_of_Init)):
    if formatted_Date_of_Expiry[k] in Rejected_Expiry_Dates:
        pass
    else:
        Starting_date = datetime.strptime(formatted_Date_of_Init[k], "%d-%b-%Y")
        Ending_date = datetime.strptime(formatted_Date_of_Expiry[k], "%d-%b-%Y")
        Starting_date = Starting_date.strftime('%Y-%m-%d')
        Ending_date = Ending_date.strftime('%Y-%m-%d')
        
        date_range = pd.date_range(start=Starting_date, end=Ending_date, freq='B')
        Dates_list = date_range.strftime('%d-%b-%Y').tolist()
        print(Dates_list)

        for j in range(len(Dates_list)-1):
           print(Dates_list[j])
           console_output_log_recording(f"The Date list is {Dates_list}")
           Present_date=Dates_list[j]

           

           if Present_date in holidays_date:
                pass
           else:
                path_present_date=f"{Access_path_date}{Present_date}/"
                path_expiry_date=f"{path_present_date}/NIFTY_{formatted_Date_of_Expiry[k+Expiry_distance]}/"
                print(formatted_Date_of_Expiry[k+Expiry_distance])

                console_output_log_recording(f"The target Expiry date is: {formatted_Date_of_Expiry[k+Expiry_distance]}")
                Date_List_all.append(Present_date)
                
                Nifty_spot_file=pd.read_csv(path_spot_vol+"NIFTY 50.csv")
                date_str=Dates_list[j]
                date_obj = datetime.strptime(date_str, '%d-%b-%Y')
                formatted_date = date_obj.strftime('%Y-%m-%d')
                row_index_spot = Nifty_spot_file.index[(Nifty_spot_file['Time'] == Day_end_time)&(Nifty_spot_file['Date'] == formatted_date)].tolist()
                Nifty_spot_price=Nifty_spot_file.loc[row_index_spot[0],"close"]
                Nifty_closest_Strike = round(Nifty_spot_price / 50) * 50
                print(f"Nifty Closest Strike: {Nifty_closest_Strike}")
                console_output_log_recording(f"Nifty Closest Strike: {Nifty_closest_Strike}")

                for distance in Strikes_distance_from_spot:
                    Call_Strike=Nifty_closest_Strike+distance*Lot_size
                    Put_Strike=Nifty_closest_Strike-distance*Lot_size

                    file_call=f"NIFTY{str(Call_Strike)}_CE.csv"
                    file_put=f"NIFTY{str(Put_Strike)}_PE.csv"

                    file_path_call=path_expiry_date+file_call
                    file_path_put=path_expiry_date+file_put

                    if not os.path.exists(file_path_call) or not os.path.exists(file_path_put):
                        Overall_profit=None
                        profit_strangle_distances[f"Profit_Strangle_distance_{distance}"].append(Overall_profit)
                    else:
                        df_call=pd.read_csv(path_expiry_date+file_call)
                        df_put=pd.read_csv(path_expiry_date+file_put)

                        if (len(df_call.loc[4,'Time']))>5:
                            df_call['Time'] = df_call['Time'].apply(lambda x: x[:5])
                            df_put['Time'] = df_put['Time'].apply(lambda x: x[:5])
                        else:
                            pass

                        df_call,df_put=merging(df_call,df_put,"Call","Put","df_CE_1","df_PE_1")

                        date_str_present = Present_date
                        date_obj_present = datetime.strptime(date_str_present, "%d-%b-%Y")
                        Desired_Date_present = date_obj_present.strftime("%Y-%m-%d")

                        row_index_call = df_call.index[(df_call['Time'] == Day_end_time)&(df_call['Date'] == Desired_Date_present)].tolist()
                        row_index_put = df_put.index[(df_put['Time'] == Day_end_time)&(df_put['Date'] == Desired_Date_present)].tolist()

                        Average_call_price_initiation,Average_put_price_initiation=Average_determination(df_call,df_put,row_index_call,row_index_put,1)

                        print(f"Average call price for call Strike {Call_Strike} is {Average_call_price_initiation}")
                        console_output_log_recording(f"Average call price for call Strike {Call_Strike} is {Average_call_price_initiation}")
                        print(f"Average put price for put Strike {Put_Strike} is {Average_put_price_initiation}")
                        console_output_log_recording(f"Average put price for put Strike {Put_Strike} is {Average_put_price_initiation}")

                        p=1

                        while True:
                            
                            Next_date=Dates_list[j+p]
                            print(f"Current Index: {j+p} and Next day is {Next_date}")

                            if Next_date in holidays_date:
                                p=p+1
                                Next_date=Dates_list[j+p]
                            else:
                                print(f"Next day is {Next_date}")
                                console_output_log_recording(f"Next day is {Next_date}")
                                path_Next_date=f"{Access_path_date}{Next_date}/"
                                path_expiry_date_next=f"{path_Next_date}/NIFTY_{formatted_Date_of_Expiry[k+Expiry_distance]}/"

                                df_call_next=pd.read_csv(path_expiry_date_next+file_call)
                                df_put_next=pd.read_csv(path_expiry_date_next+file_put)

                                if (len(df_call_next.loc[4,'Time']))>5:
                                    df_call_next['Time'] = df_call_next['Time'].apply(lambda x: x[:5])
                                    df_put_next['Time'] = df_put_next['Time'].apply(lambda x: x[:5])
                                else:
                                    pass

                                df_call_next,df_put_next=merging(df_call_next,df_put_next,"Call","Put","df_CE_1","df_PE_1")
                                date_str_next = Next_date
                                date_obj_next = datetime.strptime(date_str_next, "%d-%b-%Y")
                                Desired_Date_next = date_obj_next.strftime("%Y-%m-%d")

                                row_index_call_next = df_call_next.index[(df_call_next['Time'] == Square_off_time)&(df_call_next['Date'] == Desired_Date_next)].tolist()
                                row_index_put_next = df_put_next.index[(df_put_next['Time'] == Square_off_time)&(df_put_next['Date'] == Desired_Date_next)].tolist()

                                Opening_call_price_Next,Opening_put_price_Next=Average_determination(df_call_next,df_put_next,row_index_call_next,row_index_put_next,0)

                                print(f"Opening call price Next day for call Strike {Call_Strike} is {Opening_call_price_Next}")
                                console_output_log_recording(f"Opening call price Next day for call Strike {Call_Strike} is {Opening_call_price_Next}")
                                print(f"Opening put price Next day for put Strike {Put_Strike} is {Opening_put_price_Next}")
                                console_output_log_recording(f"Opening put price Next day for put Strike {Put_Strike} is {Opening_put_price_Next}")

                                break

                        Total_premium_collected_Call=Opening_call_price_Next-Average_call_price_initiation
                        Total_premium_collected_Put=Opening_put_price_Next-Average_put_price_initiation

                        Net_profit=Total_premium_collected_Call+Total_premium_collected_Put
                        Overall_profit=size*Lot_size*Net_profit

                        Overall_profit=round(Overall_profit,2)

                        
                        profit_strangle_distances[f"Profit_Strangle_distance_{distance}"].append(Overall_profit)



Gap_profit_loss={"Date":Date_List_all,"Profit and Loss Distance 0":profit_strangle_distances["Profit_Strangle_distance_0"],"Profit and Loss Distance 1":profit_strangle_distances["Profit_Strangle_distance_1"],"Profit and Loss Distance 2":profit_strangle_distances["Profit_Strangle_distance_2"]
                 ,"Profit and Loss Distance 3":profit_strangle_distances["Profit_Strangle_distance_3"],"Profit and Loss Distance 4":profit_strangle_distances["Profit_Strangle_distance_4"]}

# print(f"Date: {len(Date_List_all)}")
# print(f"Profit and Loss Distance 0: {len(profit_strangle_distances['Profit_Strangle_distance_0'])}")
# print(f"Profit and Loss Distance 1: {len(profit_strangle_distances['Profit_Strangle_distance_1'])}")
# print(f"Profit and Loss Distance 2: {len(profit_strangle_distances['Profit_Strangle_distance_2'])}")
# print(f"Profit and Loss Distance 3: {len(profit_strangle_distances['Profit_Strangle_distance_3'])}")
# print(f"Profit and Loss Distance 4: {len(profit_strangle_distances['Profit_Strangle_distance_4'])}")
# print(f"Profit and Loss Distance 5: {len(profit_strangle_distances['Profit_Strangle_distance_5'])}")
# print(f"Profit and Loss Distance 6: {len(profit_strangle_distances['Profit_Strangle_distance_6'])}")


Gap_profit_loss_df=pd.DataFrame(Gap_profit_loss)
Gap_profit_loss_df.to_csv(Path_backtest_Report+"Gap_profit_loss_df.csv",index=False)
