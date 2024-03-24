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
strike_call=[]
strike_put=[]
sl_hit_call_date=[]
sl_hit_put_date=[]
sl_hit_call_time=[]
sl_hit_put_time=[]
sl_hit_call_week=[]
sl_hit_put_week=[]
Net_premium_collected_call=[]
Net_premium_collected_put=[]
Net_P_L=[]
Net_Credit_Spread_Call=[]
Net_Credit_Spread_Put=[]
Day=0
previous_day=[]
Market_trend="Neutral"
run_len=0
Active_status={}

###################
Desired_time="09:20"
Checking_time="09:30"

def merging(df_CE,df_PE,Right_1,Right_2):
    if Right_1=="Call" and Right_2=="PUT":
        df_combined = pd.merge(df_CE, df_PE, on=['Date', 'Time'], how='outer')
        df_combined['Date'] = pd.to_datetime(df_combined['Date'])
        df_combined['Time'] = pd.to_datetime(df_combined['Time'], format='%H:%M').dt.strftime('%H:%M')
        df_combined = df_combined.sort_values(by=['Date', 'Time'])
        df_combined = df_combined.fillna(method='ffill')
        df_CE=df_combined[['Date','Time','open CE','high CE','low CE','close CE','volume CE','oi CE']]
        df_PE=df_combined[['Date','Time','open PE','high PE','low PE','close PE','volume PE','oi PE']]
        return df_CE,df_PE
    elif Right_1=="Call" and Right_2=="Call":
        df_combined = pd.merge(df_CE, df_PE, on=['Date', 'Time'], how='outer')
        df_combined['Date'] = pd.to_datetime(df_combined['Date'])
        df_combined['Time'] = pd.to_datetime(df_combined['Time'], format='%H:%M').dt.strftime('%H:%M')
        df_combined = df_combined.sort_values(by=['Date', 'Time'])
        df_combined = df_combined.fillna(method='ffill')
        df_CE_1=df_combined[['Date','Time','open CE','high CE','low CE','close CE','volume CE','oi CE']]
        df_CE_2=df_combined[['Date','Time','open CE','high CE','low CE','close CE','volume CE','oi CE']]
        return df_CE_1,df_CE_2
    elif Right_1=="Put" and Right_2=="Put":
        df_combined = pd.merge(df_CE, df_PE, on=['Date', 'Time'], how='outer')
        df_combined['Date'] = pd.to_datetime(df_combined['Date'])
        df_combined['Time'] = pd.to_datetime(df_combined['Time'], format='%H:%M').dt.strftime('%H:%M')
        df_combined = df_combined.sort_values(by=['Date', 'Time'])
        df_combined = df_combined.fillna(method='ffill')
        df_PE_1=df_combined[['Date','Time','open CE','high CE','low CE','close CE','volume CE','oi CE']]
        df_PE_2=df_combined[['Date','Time','open CE','high CE','low CE','close CE','volume CE','oi CE']]
        return df_PE_1,df_PE_2

def SL_update():
    pass

def volatility_strike_pred(Len_pe,Date,Time,path_expiry_date_recurring,CE_Strike_1=None,CE_Strike_2=None,CE_Strike_3=None,CE_Strike_4=None,PE_Strike_1=None,PE_Strike_2=None,PE_Strike_3=None,PE_Strike_4=None):
    global run_len

    input_time_str = Time
    input_time = datetime.strptime(input_time_str, "%H:%M")
    time_list_dt = [datetime.strptime(time_str, "%H:%M") for time_str in time_list]
    closest_time_index = min(range(len(time_list_dt)), key=lambda i: abs(time_list_dt[i] - input_time))
    Triggered_time=time_list[closest_time_index]

    volatility_file=pd.read_csv(path_spot_vol+"India_Vix_Historical.csv")
    Nifty_spot_file=pd.read_csv(path_spot_vol+"Nifty_50_Historical.csv")
    row_index_vol = volatility_file.index[(volatility_file['Time'] == Triggered_time)&(volatility_file['Date'] == Date)].tolist()
    row_index_spot = Nifty_spot_file.index[(Nifty_spot_file['Time'] == Triggered_time)&(Nifty_spot_file['Date'] == Date)].tolist()

    volatility=volatility_file.loc[row_index_vol[0],"Close"]
    Nifty_spot_price=Nifty_spot_file.loc[row_index_spot[0],"Close"]

    range=((volatility/np.sqrt(252))*Nifty_spot_price)/100
    offset=round(range,2)
    offset = round(offset / 50) * 50
    offset=int(offset)


    global Market_trend

    if Market_trend=="Trending Up":
        if Len_pe==1:
            CE_Strike_2=CE_Strike_1+offset
            Active_call_Strike=[]
            Active_call_Strike.append(CE_Strike_2)
            Active_put_Strike.append(PE_Strike_2)

            file_ce=f"NIFTY{str(CE_Strike_2)}_CE.csv"
            file_pe_2=f"NIFTY{str(PE_Strike_2)}_PE.csv"
            file_pe_1=f"NIFTY{str(PE_Strike_1)}_PE.csv"
            df_CE=pd.read_csv(path_expiry_date_recurring+file_ce)
            df_PE_1=pd.read_csv(path_expiry_date_recurring+file_pe_1)
            df_PE_2=pd.read_csv(path_expiry_date_recurring+file_pe_2)
            df_CE,df_PE_1=merging(df_CE,df_PE_1,"Call","Put")
            df_PE_2,df_PE_1=merging(df_PE_2,df_PE_1,"Put","Put")

            index_row = df_CE.index[(df_CE['Time'] == Triggered_time)&(df_CE['Date'] == Date)].tolist()
            index_row=index_row[0]

            CP_CE=df_CE.loc[index_row,"close CE"]
            CP_PE_2=df_PE_2.loc[index_row,"close PE"]
            SL_CE=2*CP_CE
            SL_PE_2=2*CP_PE_2

            Active_status_read=read_Active_status()
            Active_status_read["Deactive Call Strike"].append(CE_Strike_1)
            Active_status_read["Deactive Call Strike Premium Initial"].append(Active_Initial_Sold_premium_call[0])
            Active_status_read["Deactive Call Strike SL"].append(Active_SL_Call[0])

            Active_status_read["Active_call_Strike"].remove(CE_Strike_1)
            Active_status_read["Active_Initial_Sold_premium_call"].remove(Active_Initial_Sold_premium_call[0])
            Active_status_read["Active_SL_Call"].remove(Active_SL_Call[0])

            Active_status_read["Active_call_Strike"].append(CE_Strike_2)
            Active_status_read["Active_Initial_Sold_premium_call"].append(CP_CE)
            Active_status_read["Active_SL_Call"].append(SL_CE)

            Active_status_read["Active_put_Strike"].append(PE_Strike_2)
            Active_status_read["Active_Initial_Sold_premium_put"].append(CP_PE_2)
            Active_status_read["Active_SL_Put"].append(SL_PE_2)

            writing_Active_status(Active_status_read)

            Active_Initial_Sold_premium_call=[]
            Active_SL_Call=[]
            Active_Initial_Sold_premium_call.append(CP_CE)
            Active_SL_Call.append(SL_CE)
            Active_Initial_Sold_premium_put.append(CP_PE_2)
            Active_SL_Put.append(SL_PE_2)


            
            rows=df_CE.shape[0]
            run_len=rows-index_row

            return index_row,df_CE,df_PE_1,df_PE_2
        
        elif Len_pe==2:

            CE_Strike_3=CE_Strike_2+offset
            Active_call_Strike=[]
            Active_call_Strike.append(CE_Strike_3)
            Active_put_Strike.append(PE_Strike_3)

            file_ce_3=f"NIFTY{str(CE_Strike_3)}_CE.csv"
            file_pe_3=f"NIFTY{str(PE_Strike_3)}_PE.csv"
            file_pe_2=f"NIFTY{str(PE_Strike_2)}_PE.csv"
            file_pe_1=f"NIFTY{str(PE_Strike_1)}_PE.csv"

            df_CE_3=pd.read_csv(path_expiry_date_recurring+file_ce_3)
            df_PE_1=pd.read_csv(path_expiry_date_recurring+file_pe_1)
            df_PE_2=pd.read_csv(path_expiry_date_recurring+file_pe_2)
            df_PE_3=pd.read_csv(path_expiry_date_recurring+file_pe_3)

            df_CE_3,df_PE_1=merging(df_CE_3,df_PE_1,"Call","Put")
            df_PE_2,df_PE_1=merging(df_PE_2,df_PE_1,"Put","Put")
            df_PE_3,df_PE_1=merging(df_PE_3,df_PE_1,"Put","Put")

            index_row = df_CE_3.index[(df_CE_3['Time'] == Triggered_time)&(df_CE_3['Date'] == Date)].tolist()
            index_row=index_row[0]

            CP_CE_3=df_CE_3.loc[index_row,"close CE"]
            CP_PE_3=df_PE_3.loc[index_row,"close PE"]
            SL_CE_3=2*CP_CE_3
            SL_PE_3=2*CP_PE_3

            Active_status_read=read_Active_status()
            Active_status_read["Deactive Call Strike"].append(CE_Strike_2)
            Active_status_read["Deactive Call Strike Premium Initial"].append(Active_Initial_Sold_premium_call[0])
            Active_status_read["Deactive Call Strike SL"].append(Active_SL_Call[0])

            Active_status_read["Active_call_Strike"].remove(CE_Strike_2)
            Active_status_read["Active_Initial_Sold_premium_call"].remove(Active_Initial_Sold_premium_call[0])
            Active_status_read["Active_SL_Call"].remove(Active_SL_Call[0])

            Active_status_read["Active_call_Strike"].append(CE_Strike_3)
            Active_status_read["Active_Initial_Sold_premium_call"].append(CP_CE_3)
            Active_status_read["Active_SL_Call"].append(SL_CE_3)

            Active_status_read["Active_put_Strike"].append(PE_Strike_3)
            Active_status_read["Active_Initial_Sold_premium_put"].append(CP_PE_3)
            Active_status_read["Active_SL_Put"].append(SL_PE_3)

            writing_Active_status(Active_status_read)

            Active_Initial_Sold_premium_call=[]
            Active_SL_Call=[]
            Active_Initial_Sold_premium_call.append(CP_CE_3)
            Active_SL_Call.append(SL_CE_3)
            Active_Initial_Sold_premium_put.append(CP_PE_3)
            Active_SL_Put.append(SL_PE_3)
            
            rows=df_CE_3.shape[0]
            run_len=rows-index_row

            return index_row,df_CE_3,df_PE_1,df_PE_2,df_PE_3
        
        elif Len_pe==3:
            Active_call_Strike=[]
            Active_put_Strike.append(PE_Strike_4)

            file_pe_4=f"NIFTY{str(PE_Strike_4)}_PE.csv"
            file_pe_3=f"NIFTY{str(PE_Strike_3)}_PE.csv"
            file_pe_2=f"NIFTY{str(PE_Strike_2)}_PE.csv"
            file_pe_1=f"NIFTY{str(PE_Strike_1)}_PE.csv"

            df_PE_1=pd.read_csv(path_expiry_date_recurring+file_pe_1)
            df_PE_2=pd.read_csv(path_expiry_date_recurring+file_pe_2)
            df_PE_3=pd.read_csv(path_expiry_date_recurring+file_pe_3)
            df_PE_4=pd.read_csv(path_expiry_date_recurring+file_pe_4)

            df_PE_2,df_PE_1=merging(df_PE_2,df_PE_1,"Put","Put")
            df_PE_3,df_PE_1=merging(df_PE_3,df_PE_1,"Put","Put")
            df_PE_4,df_PE_3=merging(df_PE_4,df_PE_3,"Put","Put")

            index_row = df_PE_1.index[(df_PE_1['Time'] == Triggered_time)&(df_PE_1['Date'] == Date)].tolist()

            index_row=index_row[0]
            CP_PE_4=df_PE_4.loc[index_row,"close PE"]
            SL_PE_4=2*CP_PE_4

            Active_status_read=read_Active_status()
            Active_status_read["Deactive Call Strike"].append(CE_Strike_3)
            Active_status_read["Deactive Call Strike Premium Initial"].append(Active_Initial_Sold_premium_call[0])
            Active_status_read["Deactive Call Strike SL"].append(Active_SL_Call[0])

            Active_status_read["Active_call_Strike"].remove(CE_Strike_3)
            Active_status_read["Active_Initial_Sold_premium_call"].remove(Active_Initial_Sold_premium_call[0])
            Active_status_read["Active_SL_Call"].remove(Active_SL_Call[0])

            Active_status_read["Active_put_Strike"].append(PE_Strike_4)
            Active_status_read["Active_Initial_Sold_premium_put"].append(CP_PE_4)
            Active_status_read["Active_SL_Put"].append(SL_PE_4)

            writing_Active_status(Active_status_read)

            Active_Initial_Sold_premium_call=[]
            Active_SL_Call=[]
            Active_Initial_Sold_premium_put.append(CP_PE_4)
            Active_SL_Put.append(SL_PE_4)
            run_len=rows-index_row

            return index_row,df_PE_1,df_PE_2,df_PE_3,df_PE_4


def reversal_status_func(reversal_status,Strike_pe_remove,Premium_to_remove,SL_to_Remove):
    pass





def routine_code(running_index,Active_call_Strike,Active_put_Strike,Active_Initial_Sold_premium_call,Active_Initial_Sold_premium_put,Active_SL_Call,Active_SL_Put,Day,Initial_day,Expiry_date):
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

            if Market_trend=="Neutral":
                CE_Strike=Active_call_Strike[0]
                PE_Strike=Active_put_Strike[0]
                rows=df_call_init.shape[0]
                run_len=rows-running_index
                ce_initial_Price=Active_Initial_Sold_premium_call[0]
                pe_initial_Price=Active_Initial_Sold_premium_put[0]

            for i in range(run_len):

                if Market_trend=="Neutral":
                    CE_SL=Active_SL_Call[0]
                    PE_SL=Active_SL_Put[0]

                    if df_call_init.loc[(running_index+i+1),"high CE"]<CE_SL and df_put_init.loc[(running_index+i+1),"high PE"]<PE_SL:
                        call_premium_collected=ce_initial_Price-df_call_init.loc[(running_index+i+1),"close CE"]
                        put_premium_collected=pe_initial_Price-df_put_init.loc[(running_index+i+1),"close PE"]
                        Net_P_L=call_premium_collected+put_premium_collected
                        SL_update()
                    elif df_call_init.loc[(running_index+i+1),"high CE"]>=CE_SL and df_put_init.loc[(running_index+i+1),"high PE"]<PE_SL:
                        current_strike_CE=CE_Strike
                        PE_Strike_2=PE_Strike+50
                        Market_trend="Trending Up"
                        Time=df_call_init.loc[(running_index+i+1),"Time"]
                        Date=df_call_init.loc[(running_index+i+1),"Date"]
                        index_row,df_CE,df_PE_1,df_PE_2=volatility_strike_pred(Len_pe,Date,Time,path_expiry_date_recurring,current_strike_CE,0,0,0,PE_Strike,PE_Strike_2,0,0)

                    elif df_call_init.loc[(running_index+i+1),"high CE"]<CE_SL and df_put_init.loc[(running_index+i+1),"high PE"]>=PE_SL:
                        PE_Strike_1=PE_Strike
                        CE_Strike_2=CE_Strike-50
                        Market_trend="Trending Down"
                        Time=df_call_init.loc[(running_index+i+1),"Time"]
                        index_row,df_CE_1,df_CE_2,df_PE=volatility_strike_pred(Len_ce,Time,path_expiry_date_recurring,CE_Strike,CE_Strike_2,0,0,PE_Strike_1,0,0,0)
                    else:
                        pass

                elif Market_trend=="Trending Up":
                    Len_ce=len(Active_call_Strike)
                    Len_pe=len(Active_put_Strike)
                    if Len_pe==2:
                        CE_SL=Active_SL_Call[0]
                        PE_1_SL=Active_SL_Put[0]
                        PE_2_SL=Active_SL_Put[1]

                        CE_Current_pr=df_CE.loc[(i+index_row+1),"high CE"]
                        PE_Current_pr_1=df_PE_1.loc[(i+index_row+1),"high PE"]
                        PE_Current_pr_2=df_PE_2.loc[(i+index_row+1),"high PE"]

                        ce_initial_Price=Active_Initial_Sold_premium_call[0]
                        pe_initial_Price_1=Active_Initial_Sold_premium_put[0]
                        pe_initial_Price_2=Active_Initial_Sold_premium_put[1]

                        if CE_Current_pr<CE_SL and PE_Current_pr_1<PE_1_SL and PE_Current_pr_2<PE_2_SL:
                            call_premium_collected=ce_initial_Price-df_CE.loc[(index_row+i+1),"close CE"]
                            put_premium_collected_1=pe_initial_Price_1-df_PE_1.loc[(index_row+i+1),"close PE"]
                            put_premium_collected_2=pe_initial_Price_2-df_PE_2.loc[(index_row+i+1),"close PE"]
                            Net_P_L=call_premium_collected+put_premium_collected_1+put_premium_collected_2
                            SL_update()

                        elif CE_Current_pr>=CE_SL and PE_Current_pr_1<PE_1_SL and PE_Current_pr_2<PE_2_SL:
                            CE_Strike_2=Active_call_Strike[0]
                            PE_strike_3=Active_put_Strike[1]+50
                            PE_strike_2=Active_put_Strike[1]
                            PE_strike_1=Active_put_Strike[0]

                            Time=df_CE.loc[(index_row+i+1),"Time"]
                            index_row,df_CE_3,df_PE_1,df_PE_2,df_PE_3=volatility_strike_pred(Len_pe,Time,path_expiry_date_recurring,0,CE_Strike_2,0,0,PE_strike_1,PE_strike_2,PE_strike_3,0)

######### REVESAL SEQUENCE ######

                        elif CE_Current_pr<CE_SL and PE_Current_pr_1<PE_1_SL and PE_Current_pr_2>=PE_2_SL:
                            

                            Active_status_read=read_Active_status()
                            deleted_strike=Active_status_read["Deactive Put Strike"]
                            Put_strikes_remove=Active_status_read["Active_put_Strike"]
                            Strike_pe_remove_copy=Put_strikes_remove[1]


                            if Strike_pe_remove_copy not in deleted_strike:  
                                reversal_status=21010 #" the format is len,rev,CE_2,PE_2,PE_1"
                                Active_status_read["Deactive Put Strike"].append(Strike_pe_remove_copy)
                                Active_status_read["Deactive Put Strike Premium Initial"].append(Active_Initial_Sold_premium_put[1])
                                Active_status_read["Deactive Put Strike SL"].append(Active_SL_Put[1])

                                writing_Active_status(Active_status_read)
                                Strike_pe_remove=Active_put_Strike[1]
                                Premium_to_remove=Active_Initial_Sold_premium_put[1]
                                SL_to_Remove=Active_SL_Put[1]
                                reversal_status_func(reversal_status,Strike_pe_remove,Premium_to_remove,SL_to_Remove)

                                call_premium_collected=ce_initial_Price-df_CE.loc[(index_row+i+1),"close CE"]
                                put_premium_collected_1=pe_initial_Price_1-df_PE_1.loc[(index_row+i+1),"close PE"]
                                Net_P_L=call_premium_collected+put_premium_collected_1
                                SL_update()
                            else:
                                call_premium_collected=ce_initial_Price-df_CE.loc[(index_row+i+1),"close CE"]
                                put_premium_collected_1=pe_initial_Price_1-df_PE_1.loc[(index_row+i+1),"close PE"]
                                Net_P_L=call_premium_collected+put_premium_collected_1
                                SL_update()

                        elif CE_Current_pr>=CE_SL and PE_Current_pr_1<PE_1_SL and PE_Current_pr_2>=PE_2_SL:

                            Active_status_read=read_Active_status()
                            deleted_strike_pe=Active_status_read["Deactive Put Strike"]
                            deleted_strike_ce=Active_status_read["Deactive Call Strike"]

                            Put_strikes_remove=Active_status_read["Active_put_Strike"]
                            Call_Strikes_remove=Active_status_read["Active_call_Strike"]
                            Strike_ce_remove_copy=Call_Strikes_remove[0]
                            Strike_pe_remove_copy=Put_strikes_remove[1]

                            if Strike_pe_remove_copy not in deleted_strike_pe and Strike_ce_remove_copy not in deleted_strike_ce:  
                                reversal_status=21110 #" the format is len,rev,CE_2,PE_2,PE_1"

                                Active_status_read["Deactive Put Strike"].append(Strike_pe_remove_copy)
                                Active_status_read["Deactive Call Strike"].append(Strike_ce_remove_copy)
                                Active_status_read["Deactive Call Strike Premium Initial"].append(Active_Initial_Sold_premium_call[0])
                                Active_status_read["Deactive Call Strike SL"].append(Active_SL_Call[0])
                                Active_status_read["Deactive Put Strike Premium Initial"].append(Active_Initial_Sold_premium_put[1])
                                Active_status_read["Deactive Put Strike SL"].append(Active_SL_Put[1])
                                writing_Active_status(Active_status_read)


                                Strike_remove=Active_call_Strike[0]
                                Premium_to_remove=Active_Initial_Sold_premium_call[0]
                                SL_to_Remove=Active_SL_Call[0]
                                out=reversal_status_func(reversal_status,Strike_remove,Premium_to_remove,SL_to_Remove)

                                put_premium_collected_1=pe_initial_Price_1-df_PE_1.loc[(index_row+i+1),"close PE"]
                                Net_P_L=put_premium_collected_1
                                SL_update()
                            else:
                                put_premium_collected_1=pe_initial_Price_1-df_PE_1.loc[(index_row+i+1),"close PE"]
                                Net_P_L=put_premium_collected_1
                                SL_update()

                        elif CE_Current_pr<CE_SL and PE_Current_pr_1>=PE_1_SL and PE_Current_pr_2>=PE_2_SL:

                            Active_status_read=read_Active_status()
                            deleted_strike_pe=Active_status_read["Deactive Put Strike"]
                            Put_strikes_remove=Active_status_read["Active_put_Strike"]

                            Strike_pe_1_remove_copy=Put_strikes_remove[0]
                            Strike_pe_2_remove_copy=Put_strikes_remove[1]

                            if Strike_pe_1_remove_copy not in deleted_strike and Strike_pe_2_remove_copy not in deleted_strike:  
                                reversal_status=21011 #" the format is len,rev,CE_2,PE_2,PE_1"
                                Active_status_read["Deactive Put Strike"].append(Strike_pe_1_remove_copy)
                                Active_status_read["Deactive Put Strike"].append(Strike_pe_2_remove_copy)
                                Active_status_read["Deactive Put Strike Premium Initial"].append(Active_Initial_Sold_premium_call[0])
                                Active_status_read["Deactive Put Strike Premium Initial"].append(Active_Initial_Sold_premium_call[1])
                                Active_status_read["Deactive Put Strike SL"].append(Active_SL_Put[0])
                                Active_status_read["Deactive Put Strike SL"].append(Active_SL_Put[1])

                                writing_Active_status(Active_status_read)

                                Strike_remove=Active_call_Strike[0]
                                Premium_to_remove=Active_Initial_Sold_premium_call[0]
                                SL_to_Remove=Active_SL_Call[0]
                                reversal_status_func(reversal_status,Strike_remove,Premium_to_remove,SL_to_Remove)

                                call_premium_collected=ce_initial_Price-df_CE.loc[(index_row+i+1),"close CE"]
                                Net_P_L=call_premium_collected
                                SL_update()
                            else:
                                call_premium_collected=ce_initial_Price-df_CE.loc[(index_row+i+1),"close CE"]
                                Net_P_L=call_premium_collected
                                SL_update()

                        elif CE_Current_pr>=CE_SL and PE_Current_pr_1>=PE_1_SL and PE_Current_pr_2>=PE_2_SL:
                            ## read the text file and get the strike to remove from that file and get the deleted strikes list
                            Active_status_read=read_Active_status()
                            deleted_strike_pe=Active_status_read["Deactive Put Strike"]
                            deleted_strike_ce=Active_status_read["Deactive Call Strike"]

                            Put_strikes_remove=Active_status_read["Active_put_Strike"]
                            Call_Strikes_remove=Active_status_read["Active_call_Strike"]

                            Strike_pe_1_remove_copy=Put_strikes_remove[0]
                            Strike_pe_2_remove_copy=Put_strikes_remove[1]
                            Strike_ce_1_remove_copy=Call_Strikes_remove[0]

                            ## Read the list from the text file  ########
                            # deleted_strike=data
                            if Strike_pe_1_remove_copy not in deleted_strike_pe and Strike_pe_2_remove_copy not in deleted_strike_pe and Strike_ce_1_remove_copy not in deleted_strike_ce:  
                                reversal_status=21111 #" the format is len,rev,CE_2,PE_2,PE_1"
                                Active_status_read["Deactive Put Strike"].append(Strike_pe_1_remove_copy)
                                Active_status_read["Deactive Put Strike"].append(Strike_pe_2_remove_copy)
                                Active_status_read["Deactive Put Strike Premium Initial"].append(Active_Initial_Sold_premium_call[0])
                                Active_status_read["Deactive Put Strike Premium Initial"].append(Active_Initial_Sold_premium_call[1])
                                Active_status_read["Deactive Put Strike SL"].append(Active_SL_Put[0])
                                Active_status_read["Deactive Put Strike SL"].append(Active_SL_Put[1])
                                Active_status_read["Deactive Call Strike"].append(Strike_ce_remove_copy)
                                Active_status_read["Deactive Call Strike Premium Initial"].append(Active_Initial_Sold_premium_call[0])
                                Active_status_read["Deactive Call Strike SL"].append(Active_SL_Call[0])

                                writing_Active_status(Active_status_read)

                                Strike_remove=Active_call_Strike[0]
                                Premium_to_remove=Active_Initial_Sold_premium_call[0]
                                SL_to_Remove=Active_SL_Call[0]
                                out=reversal_status_func(reversal_status,Strike_remove,Premium_to_remove,SL_to_Remove)
                                break

                            else:
                                pass
                        else:
                            pass

                    elif Len_pe==3:
                        CE_SL=Active_SL_Call[0]
                        PE_1_SL=Active_SL_Put[0]
                        PE_2_SL=Active_SL_Put[1]
                        PE_3_SL=Active_SL_Put[2]

                        CE_Current_pr=df_CE_3.loc[(i+index_row+1),"high CE"]
                        PE_Current_pr_1=df_PE_1.loc[(i+index_row+1),"high PE"]
                        PE_Current_pr_2=df_PE_2.loc[(i+index_row+1),"high PE"]
                        PE_Current_pr_3=df_PE_3.loc[(i+index_row+1),"high PE"]

                        ce_initial_Price=Active_Initial_Sold_premium_call[0]
                        pe_initial_Price_1=Active_Initial_Sold_premium_put[0]
                        pe_initial_Price_2=Active_Initial_Sold_premium_put[1]
                        pe_initial_Price_3=Active_Initial_Sold_premium_put[2]

                        if CE_Current_pr<CE_SL and PE_Current_pr_1<PE_1_SL and PE_Current_pr_2<PE_2_SL and PE_Current_pr_3<PE_3_SL:
                            call_premium_collected=ce_initial_Price-df_CE_3.loc[(index_row+i+1),"close CE"]
                            put_premium_collected_1=pe_initial_Price_1-df_PE_1.loc[(index_row+i+1),"close PE"]
                            put_premium_collected_2=pe_initial_Price_2-df_PE_2.loc[(index_row+i+1),"close PE"]
                            put_premium_collected_3=pe_initial_Price_3-df_PE_3.loc[(index_row+i+1),"close PE"]
                            Net_P_L=call_premium_collected+put_premium_collected_1+put_premium_collected_2+put_premium_collected_3
                            SL_update()

                        elif CE_Current_pr>=CE_SL and PE_Current_pr_1<PE_1_SL and PE_Current_pr_2<PE_2_SL and PE_Current_pr_3<PE_3_SL:
                            CE_Strike_3=Active_call_Strike[0]
                            PE_Strike_4=Active_put_Strike[2]+50
                            PE_strike_3=Active_put_Strike[2]
                            PE_strike_2=Active_put_Strike[1]
                            PE_strike_1=Active_put_Strike[0]

                            Time=df_CE_3.loc[(index_row+i+1),"Time"]
                            Date=df_CE_3.loc[(index_row+i+1),"Date"]
                            index_row,df_PE_1,df_PE_2,df_PE_3,df_PE_4=volatility_strike_pred(Len_pe,Date,Time,path_expiry_date_recurring,0,0,CE_Strike_3,0,PE_strike_1,PE_strike_2,PE_strike_3,PE_Strike_4)

                        elif CE_Current_pr<CE_SL and PE_Current_pr_1<PE_1_SL and PE_Current_pr_2<PE_2_SL and PE_Current_pr_3>=PE_3_SL:
                            Active_status_read=read_Active_status()
                            deleted_strike_pe=Active_status_read["Deactive Put Strike"]
                            Put_strikes_remove=Active_status_read["Active_put_Strike"]
                            Strike_pe_remove_copy=Put_strikes_remove[2]

                            if Strike_pe_remove_copy not in deleted_strike:  
                                reversal_status=310100 #" the format is len,rev,CE_2,PE_2,PE_1"
                                Active_status_read["Deactive Put Strike"].append(Strike_pe_remove_copy)
                                Active_status_read["Deactive Put Strike Premium Initial"].append(Active_Initial_Sold_premium_put[2])
                                Active_status_read["Deactive Put Strike SL"].append(Active_SL_Put[2])

                                writing_Active_status(Active_status_read)

                                Strike_pe_remove=Active_put_Strike[2]
                                Premium_to_remove=Active_Initial_Sold_premium_put[2]
                                SL_to_Remove=Active_SL_Put[2]
                                out=reversal_status_func(reversal_status,Strike_pe_remove,Premium_to_remove,SL_to_Remove)

                                call_premium_collected=ce_initial_Price-df_CE_3.loc[(index_row+i+1),"close CE"]
                                put_premium_collected_1=pe_initial_Price_1-df_PE_1.loc[(index_row+i+1),"close PE"]
                                put_premium_collected_2=pe_initial_Price_2-df_PE_2.loc[(index_row+i+1),"close PE"]
                                Net_P_L=call_premium_collected+put_premium_collected_1+put_premium_collected_2
                                SL_update()
                            else:
                                call_premium_collected=ce_initial_Price-df_CE_3.loc[(index_row+i+1),"close CE"]
                                put_premium_collected_1=pe_initial_Price_1-df_PE_1.loc[(index_row+i+1),"close PE"]
                                put_premium_collected_2=pe_initial_Price_2-df_PE_2.loc[(index_row+i+1),"close PE"]
                                Net_P_L=call_premium_collected+put_premium_collected_1+put_premium_collected_2
                                SL_update()

                        elif CE_Current_pr>=CE_SL and PE_Current_pr_1<PE_1_SL and PE_Current_pr_2<PE_2_SL and PE_Current_pr_3>=PE_3_SL:

                            Active_status_read=read_Active_status()
                            deleted_strike_pe=Active_status_read["Deactive Put Strike"]
                            deleted_strike_ce=Active_status_read["Deactive Call Strike"]

                            Put_strikes_remove=Active_status_read["Active_put_Strike"]
                            Call_Strikes_remove=Active_status_read["Active_call_Strike"]

                            Strike_pe_remove_copy=Put_strikes_remove[2]
                            Strike_ce_remove_copy=Put_strikes_remove[0]

                            if Strike_pe_remove_copy not in deleted_strike_pe and Strike_ce_remove_copy not in deleted_strike_ce:  
                                reversal_status=311100 #" the format is len,rev,CE_2,PE_2,PE_1"
                                Active_status_read["Deactive Put Strike"].append(Strike_pe_remove_copy)
                                Active_status_read["Deactive Call Strike"].append(Strike_ce_remove_copy)
                                Active_status_read["Deactive Put Strike Premium Initial"].append(Active_Initial_Sold_premium_put[2])
                                Active_status_read["Deactive Put Strike SL"].append(Active_SL_Put[2])
                                Active_status_read["Deactive Call Strike Premium Initial"].append(Active_Initial_Sold_premium_call[0])
                                Active_status_read["Deactive Call Strike SL"].append(Active_SL_Call[0])

                                writing_Active_status(Active_status_read)

                                Strike_pe_remove=Active_call_Strike[0]
                                Premium_to_remove=Active_Initial_Sold_premium_call[0]
                                SL_to_Remove=Active_SL_Call[0]
                                out=reversal_status_func(reversal_status,Strike_pe_remove,Premium_to_remove,SL_to_Remove)

                                put_premium_collected_1=pe_initial_Price_1-df_PE_1.loc[(index_row+i+1),"close PE"]
                                put_premium_collected_2=pe_initial_Price_2-df_PE_2.loc[(index_row+i+1),"close PE"]
                                Net_P_L=call_premium_collected+put_premium_collected_1+put_premium_collected_2
                                SL_update()
                            else:
                                put_premium_collected_1=pe_initial_Price_1-df_PE_1.loc[(index_row+i+1),"close PE"]
                                put_premium_collected_2=pe_initial_Price_2-df_PE_2.loc[(index_row+i+1),"close PE"]
                                Net_P_L=call_premium_collected+put_premium_collected_1+put_premium_collected_2
                                SL_update()

                        elif CE_Current_pr<CE_SL and PE_Current_pr_1<PE_1_SL and PE_Current_pr_2>=PE_2_SL and PE_Current_pr_3>=PE_3_SL:
                            Active_status_read=read_Active_status()
                            deleted_strike_pe=Active_status_read["Deactive Put Strike"]
                            Put_strikes_remove=Active_status_read["Active_put_Strike"]
        

                            Strike_pe_2_remove_copy=Put_strikes_remove[2]
                            Strike_pe_3_remove_copy=Put_strikes_remove[3]

                            if Strike_pe_2_remove_copy not in deleted_strike_pe and Strike_pe_3_remove_copy not in deleted_strike_pe:  
                                reversal_status=310110 #" the format is len,rev,CE_2,PE_2,PE_1"
                                Active_status_read["Deactive Put Strike"].append(Strike_pe_2_remove_copy)
                                Active_status_read["Deactive Put Strike"].append(Strike_pe_3_remove_copy)
                                Active_status_read["Deactive Put Strike Premium Initial"].append(Active_Initial_Sold_premium_put[2])
                                Active_status_read["Deactive Put Strike Premium Initial"].append(Active_Initial_Sold_premium_put[3])
                                Active_status_read["Deactive Put Strike SL"].append(Active_SL_Put[2])
                                Active_status_read["Deactive Put Strike SL"].append(Active_SL_Put[3])

                                writing_Active_status(Active_status_read)

                                Strike_pe_remove=Active_call_Strike[0]
                                Premium_to_remove=Active_Initial_Sold_premium_call[0]
                                SL_to_Remove=Active_SL_Call[0]
                                reversal_status_func(reversal_status,Strike_pe_remove,Premium_to_remove,SL_to_Remove)

                                call_premium_collected=ce_initial_Price-df_CE_3.loc[(index_row+i+1),"close CE"]
                                put_premium_collected_1=pe_initial_Price_1-df_PE_1.loc[(index_row+i+1),"close PE"]
                                Net_P_L=call_premium_collected+put_premium_collected_1
                                SL_update()
                            else:
                                call_premium_collected=ce_initial_Price-df_CE_3.loc[(index_row+i+1),"close CE"]
                                put_premium_collected_1=pe_initial_Price_1-df_PE_1.loc[(index_row+i+1),"close PE"]
                                Net_P_L=call_premium_collected+put_premium_collected_1
                                SL_update()

                        elif CE_Current_pr>=CE_SL and PE_Current_pr_1<PE_1_SL and PE_Current_pr_2>=PE_2_SL and PE_Current_pr_3>=PE_3_SL:
                            Active_status_read=read_Active_status()
                            deleted_strike_pe=Active_status_read["Deactive Put Strike"]
                            deleted_strike_ce=Active_status_read["Deactive Call Strike"]

                            Put_strikes_remove=Active_status_read["Active_put_Strike"]
                            Call_Strikes_remove=Active_status_read["Active_call_Strike"]

                            Strike_pe_2_remove_copy=Put_strikes_remove[1]
                            Strike_pe_3_remove_copy=Put_strikes_remove[2]
                            Strike_ce_1_remove_copy=Call_Strikes_remove[0]


                            if Strike_pe_3_remove_copy not in deleted_strike_pe and Strike_pe_2_remove_copy not in deleted_strike_pe and Strike_ce_1_remove_copy not in deleted_strike_ce:  
                                reversal_status=311110 #" the format is len,rev,CE_2,PE_2,PE_1"

                                Active_status_read["Deactive Put Strike"].append(Strike_pe_2_remove_copy)
                                Active_status_read["Deactive Put Strike"].append(Strike_pe_3_remove_copy)
                                Active_status_read["Deactive Put Strike Premium Initial"].append(Active_Initial_Sold_premium_put[1])
                                Active_status_read["Deactive Put Strike Premium Initial"].append(Active_Initial_Sold_premium_put[2])
                                Active_status_read["Deactive Put Strike SL"].append(Active_SL_Put[1])
                                Active_status_read["Deactive Put Strike SL"].append(Active_SL_Put[2])
                                Active_status_read["Deactive Call Strike"].append(Strike_ce_1_remove_copy)
                                Active_status_read["Deactive Call Strike Premium Initial"].append(Active_Initial_Sold_premium_call[0])
                                Active_status_read["Deactive Call Strike SL"].append(Active_SL_Call[0])

                                writing_Active_status(Active_status_read)

                                Strike_pe_remove=Active_call_Strike[0]
                                Premium_to_remove=Active_Initial_Sold_premium_call[0]
                                SL_to_Remove=Active_SL_Call[0]
                                reversal_status_func(reversal_status,Strike_pe_remove,Premium_to_remove,SL_to_Remove)


                                put_premium_collected_1=pe_initial_Price_1-df_PE_1.loc[(index_row+i+1),"close PE"]
                                Net_P_L=put_premium_collected_1
                                SL_update()
                            else:
                                put_premium_collected_1=pe_initial_Price_1-df_PE_1.loc[(index_row+i+1),"close PE"]
                                Net_P_L=put_premium_collected_1
                                SL_update()
                        elif CE_Current_pr<CE_SL and PE_Current_pr_1>=PE_1_SL and PE_Current_pr_2>=PE_2_SL and PE_Current_pr_3>=PE_3_SL:
                            Active_status_read=read_Active_status()
                            deleted_strike_pe=Active_status_read["Deactive Put Strike"]

                            Put_strikes_remove=Active_status_read["Active_put_Strike"]

                            Strike_pe_1_remove_copy=Put_strikes_remove[0]
                            Strike_pe_2_remove_copy=Put_strikes_remove[1]
                            Strike_pe_3_remove_copy=Put_strikes_remove[2]

                            if Strike_pe_1_remove_copy not in deleted_strike_pe and Strike_pe_2_remove_copy not in deleted_strike_pe and Strike_pe_3_remove_copy not in deleted_strike_pe:  
                                reversal_status=310111 #" the format is len,rev,CE_2,PE_2,PE_1"
                                Active_status_read["Deactive Put Strike"].append(Strike_pe_1_remove_copy)
                                Active_status_read["Deactive Put Strike"].append(Strike_pe_2_remove_copy)
                                Active_status_read["Deactive Put Strike"].append(Strike_pe_3_remove_copy)
                                Active_status_read["Deactive Put Strike Premium Initial"].append(Active_Initial_Sold_premium_put[0])
                                Active_status_read["Deactive Put Strike Premium Initial"].append(Active_Initial_Sold_premium_put[1])
                                Active_status_read["Deactive Put Strike Premium Initial"].append(Active_Initial_Sold_premium_put[2])
                                Active_status_read["Deactive Put Strike SL"].append(Active_SL_Put[0])
                                Active_status_read["Deactive Put Strike SL"].append(Active_SL_Put[1])
                                Active_status_read["Deactive Put Strike SL"].append(Active_SL_Put[2])
                                Active_status_read["Deactive Call Strike"].append(Strike_ce_1_remove_copy)
                                Active_status_read["Deactive Call Strike Premium Initial"].append(Active_Initial_Sold_premium_call[0])
                                Active_status_read["Deactive Call Strike SL"].append(Active_SL_Call[0])

                                writing_Active_status(Active_status_read)

                                Strike_pe_remove=Active_call_Strike[0]
                                Premium_to_remove=Active_Initial_Sold_premium_call[0]
                                SL_to_Remove=Active_SL_Call[0]
                                reversal_status_func(reversal_status,Strike_pe_remove,Premium_to_remove,SL_to_Remove)

                                call_premium_collected=ce_initial_Price-df_CE_3.loc[(index_row+i+1),"close CE"]
                                Net_P_L=call_premium_collected
                                SL_update()
                            else:
                                call_premium_collected=ce_initial_Price-df_CE_3.loc[(index_row+i+1),"close CE"]
                                Net_P_L=call_premium_collected
                                SL_update()
                        elif CE_Current_pr>=CE_SL and PE_Current_pr_1>=PE_1_SL and PE_Current_pr_2>=PE_2_SL and PE_Current_pr_3>=PE_3_SL:
                            Active_status_read=read_Active_status()
                            deleted_strike_pe=Active_status_read["Deactive Put Strike"]
                            deleted_strike_ce=Active_status_read["Deactive Call Strike"]

                            Put_strikes_remove=Active_status_read["Active_put_Strike"]
                            Call_Strikes_remove=Active_status_read["Active_call_Strike"]

                            Strike_pe_1_remove_copy=Put_strikes_remove[0]
                            Strike_pe_2_remove_copy=Put_strikes_remove[1]
                            Strike_pe_3_remove_copy=Put_strikes_remove[2]
                            Strike_ce_1_remove_copy=Call_Strikes_remove[0]


                            ## Read the list from the text file  ########
                            # deleted_strike=data
                            if Strike_pe_remove_copy not in deleted_strike:  
                                reversal_status=311111 #" the format is len,rev,CE_2,PE_2,PE_1"

                                Active_status_read["Deactive Put Strike"].append(Strike_pe_1_remove_copy)
                                Active_status_read["Deactive Put Strike"].append(Strike_pe_2_remove_copy)
                                Active_status_read["Deactive Put Strike"].append(Strike_pe_3_remove_copy)
                                Active_status_read["Deactive Put Strike Premium Initial"].append(Active_Initial_Sold_premium_put[0])
                                Active_status_read["Deactive Put Strike Premium Initial"].append(Active_Initial_Sold_premium_put[1])
                                Active_status_read["Deactive Put Strike Premium Initial"].append(Active_Initial_Sold_premium_put[2])
                                Active_status_read["Deactive Put Strike SL"].append(Active_SL_Put[0])
                                Active_status_read["Deactive Put Strike SL"].append(Active_SL_Put[1])
                                Active_status_read["Deactive Put Strike SL"].append(Active_SL_Put[2])
                                Active_status_read["Deactive Call Strike"].append(Strike_ce_1_remove_copy)
                                Active_status_read["Deactive Call Strike Premium Initial"].append(Active_Initial_Sold_premium_call[0])
                                Active_status_read["Deactive Call Strike SL"].append(Active_SL_Call[0])

                                writing_Active_status(Active_status_read)

                                Strike_pe_remove=Active_call_Strike[0]
                                Premium_to_remove=Active_Initial_Sold_premium_call[0]
                                SL_to_Remove=Active_SL_Call[0]
                                reversal_status_func(reversal_status,Strike_pe_remove,Premium_to_remove,SL_to_Remove)
                                break
                        else:
                            pass

                    elif Len_pe==4:
                        PE_1_SL=Active_SL_Put[0]
                        PE_2_SL=Active_SL_Put[1]
                        PE_3_SL=Active_SL_Put[2]
                        PE_4_SL=Active_SL_Put[3]

                        PE_Current_pr_1=df_PE_1.loc[(i+index_row+1),"high PE"]
                        PE_Current_pr_2=df_PE_2.loc[(i+index_row+1),"high PE"]
                        PE_Current_pr_3=df_PE_3.loc[(i+index_row+1),"high PE"]
                        PE_Current_pr_4=df_PE_4.loc[(i+index_row+1),"high PE"]

                        pe_initial_Price_1=Active_Initial_Sold_premium_put[0]
                        pe_initial_Price_2=Active_Initial_Sold_premium_put[1]
                        pe_initial_Price_3=Active_Initial_Sold_premium_put[2]
                        pe_initial_Price_4=Active_Initial_Sold_premium_put[3]

                        if PE_Current_pr_1<PE_1_SL and PE_Current_pr_2<PE_2_SL and PE_Current_pr_3<PE_3_SL and PE_Current_pr_4<PE_4_SL:
                            put_premium_collected_1=pe_initial_Price_1-df_PE_1.loc[(index_row+i+1),"close PE"]
                            put_premium_collected_2=pe_initial_Price_2-df_PE_2.loc[(index_row+i+1),"close PE"]
                            put_premium_collected_3=pe_initial_Price_3-df_PE_3.loc[(index_row+i+1),"close PE"]
                            put_premium_collected_4=pe_initial_Price_4-df_PE_4.loc[(index_row+i+1),"close PE"]
                            Net_P_L=put_premium_collected_1+put_premium_collected_2+put_premium_collected_3+put_premium_collected_4
                            SL_update()

                        elif PE_Current_pr_1<PE_1_SL and PE_Current_pr_2<PE_2_SL and PE_Current_pr_3<PE_3_SL and PE_Current_pr_4>=PE_4_SL:

                            Active_status_read=read_Active_status()
                            deleted_strike_pe=Active_status_read["Deactive Put Strike"]
                            Put_strikes_remove=Active_status_read["Active_put_Strike"]

                            Strike_pe_4_remove_copy=Put_strikes_remove[3]

                            if Strike_pe_4_remove_copy not in deleted_strike_pe:  
                                reversal_status=411000 #" the format is len,rev,CE_2,PE_2,PE_1"
                                Active_status_read["Deactive Put Strike"].append(Strike_pe_4_remove_copy)
                                Active_status_read["Deactive Put Strike Premium Initial"].append(Active_Initial_Sold_premium_put[3])
                                Active_status_read["Deactive Put Strike SL"].append(Active_SL_Put[3])

                                writing_Active_status(Active_status_read)

                                Strike_pe_remove=Active_call_Strike[0]
                                Premium_to_remove=Active_Initial_Sold_premium_call[0]
                                SL_to_Remove=Active_SL_Call[0]
                                reversal_status_func(reversal_status,Strike_pe_remove,Premium_to_remove,SL_to_Remove)

                                put_premium_collected_1=pe_initial_Price_1-df_PE_1.loc[(index_row+i+1),"close PE"]
                                put_premium_collected_2=pe_initial_Price_2-df_PE_2.loc[(index_row+i+1),"close PE"]
                                put_premium_collected_3=pe_initial_Price_3-df_PE_3.loc[(index_row+i+1),"close PE"]
                                Net_P_L=put_premium_collected_1+put_premium_collected_2+put_premium_collected_3
                                SL_update()
                            else:
                                put_premium_collected_1=pe_initial_Price_1-df_PE_1.loc[(index_row+i+1),"close PE"]
                                put_premium_collected_2=pe_initial_Price_2-df_PE_2.loc[(index_row+i+1),"close PE"]
                                put_premium_collected_3=pe_initial_Price_3-df_PE_3.loc[(index_row+i+1),"close PE"]
                                Net_P_L=put_premium_collected_1+put_premium_collected_2+put_premium_collected_3
                                SL_update()

                        elif PE_Current_pr_1<PE_1_SL and PE_Current_pr_2<PE_2_SL and PE_Current_pr_3>=PE_3_SL and PE_Current_pr_4>=PE_4_SL:
                                                        
                            Active_status_read=read_Active_status()
                            deleted_strike_pe=Active_status_read["Deactive Put Strike"]
                            Put_strikes_remove=Active_status_read["Active_put_Strike"]

                            Strike_pe_3_remove_copy=Put_strikes_remove[2]
                            Strike_pe_4_remove_copy=Put_strikes_remove[3]


                            if Strike_pe_4_remove_copy not in deleted_strike_pe and Strike_pe_3_remove_copy not in deleted_strike_pe:  
                                reversal_status=411100 #" the format is len,rev,CE_2,PE_2,PE_1"
                                Active_status_read["Deactive Put Strike"].append(Strike_pe_4_remove_copy)
                                Active_status_read["Deactive Put Strike Premium Initial"].append(Active_Initial_Sold_premium_put[3])
                                Active_status_read["Deactive Put Strike SL"].append(Active_SL_Put[3])
                                Active_status_read["Deactive Put Strike"].append(Strike_pe_3_remove_copy)
                                Active_status_read["Deactive Put Strike Premium Initial"].append(Active_Initial_Sold_premium_put[2])
                                Active_status_read["Deactive Put Strike SL"].append(Active_SL_Put[2])

                                writing_Active_status(Active_status_read)

                                Strike_pe_remove=Active_call_Strike[0]
                                Premium_to_remove=Active_Initial_Sold_premium_call[0]
                                SL_to_Remove=Active_SL_Call[0]
                                reversal_status_func(reversal_status,Strike_pe_remove,Premium_to_remove,SL_to_Remove)

                                put_premium_collected_1=pe_initial_Price_1-df_PE_1.loc[(index_row+i+1),"close PE"]
                                put_premium_collected_2=pe_initial_Price_2-df_PE_2.loc[(index_row+i+1),"close PE"]
                                Net_P_L=put_premium_collected_1+put_premium_collected_2
                                SL_update()
                            else:
                                put_premium_collected_1=pe_initial_Price_1-df_PE_1.loc[(index_row+i+1),"close PE"]
                                put_premium_collected_2=pe_initial_Price_2-df_PE_2.loc[(index_row+i+1),"close PE"]
                                Net_P_L=put_premium_collected_1+put_premium_collected_2
                                SL_update()

                        elif PE_Current_pr_1<PE_1_SL and PE_Current_pr_2>=PE_2_SL and PE_Current_pr_3>=PE_3_SL and PE_Current_pr_4>=PE_4_SL:

                            Active_status_read=read_Active_status()
                            deleted_strike_pe=Active_status_read["Deactive Put Strike"]
                            Put_strikes_remove=Active_status_read["Active_put_Strike"]

                            Strike_pe_2_remove_copy=Put_strikes_remove[1]
                            Strike_pe_3_remove_copy=Put_strikes_remove[2]
                            Strike_pe_4_remove_copy=Put_strikes_remove[3]

                            if Strike_pe_4_remove_copy not in deleted_strike_pe and Strike_pe_3_remove_copy not in deleted_strike_pe and Strike_pe_2_remove_copy not in deleted_strike_pe:  
                                reversal_status=411110 #" the format is len,rev,CE_2,PE_2,PE_1"
                                Active_status_read["Deactive Put Strike"].append(Strike_pe_4_remove_copy)
                                Active_status_read["Deactive Put Strike Premium Initial"].append(Active_Initial_Sold_premium_put[3])
                                Active_status_read["Deactive Put Strike SL"].append(Active_SL_Put[3])

                                Active_status_read["Deactive Put Strike"].append(Strike_pe_3_remove_copy)
                                Active_status_read["Deactive Put Strike Premium Initial"].append(Active_Initial_Sold_premium_put[2])
                                Active_status_read["Deactive Put Strike SL"].append(Active_SL_Put[2])

                                Active_status_read["Deactive Put Strike"].append(Strike_pe_2_remove_copy)
                                Active_status_read["Deactive Put Strike Premium Initial"].append(Active_Initial_Sold_premium_put[1])
                                Active_status_read["Deactive Put Strike SL"].append(Active_SL_Put[1])

                                writing_Active_status(Active_status_read)

                                Strike_pe_remove=Active_call_Strike[0]
                                Premium_to_remove=Active_Initial_Sold_premium_call[0]
                                SL_to_Remove=Active_SL_Call[0]
                                reversal_status_func(reversal_status,Strike_pe_remove,Premium_to_remove,SL_to_Remove)

                                put_premium_collected_1=pe_initial_Price_1-df_PE_1.loc[(index_row+i+1),"close PE"]
                                Net_P_L=put_premium_collected_1
                                SL_update()
                            else:
                                put_premium_collected_1=pe_initial_Price_1-df_PE_1.loc[(index_row+i+1),"close PE"]
                                Net_P_L=put_premium_collected_1
                                SL_update()

                        elif PE_Current_pr_1>=PE_1_SL and PE_Current_pr_2>=PE_2_SL and PE_Current_pr_3>=PE_3_SL and PE_Current_pr_4>=PE_4_SL:
                            Active_status_read=read_Active_status()
                            deleted_strike_pe=Active_status_read["Deactive Put Strike"]
                            Put_strikes_remove=Active_status_read["Active_put_Strike"]

                            Strike_pe_1_remove_copy=Put_strikes_remove[0]
                            Strike_pe_2_remove_copy=Put_strikes_remove[1]
                            Strike_pe_3_remove_copy=Put_strikes_remove[2]
                            Strike_pe_4_remove_copy=Put_strikes_remove[3]


                            if Strike_pe_4_remove_copy not in deleted_strike_pe and Strike_pe_3_remove_copy not in deleted_strike_pe and Strike_pe_2_remove_copy not in deleted_strike_pe and Strike_pe_1_remove_copy not in deleted_strike_pe:  
                                reversal_status=411111 #" the format is len,rev,CE_2,PE_2,PE_1"

                                Active_status_read["Deactive Put Strike"].append(Strike_pe_4_remove_copy)
                                Active_status_read["Deactive Put Strike Premium Initial"].append(Active_Initial_Sold_premium_put[3])
                                Active_status_read["Deactive Put Strike SL"].append(Active_SL_Put[3])

                                Active_status_read["Deactive Put Strike"].append(Strike_pe_3_remove_copy)
                                Active_status_read["Deactive Put Strike Premium Initial"].append(Active_Initial_Sold_premium_put[2])
                                Active_status_read["Deactive Put Strike SL"].append(Active_SL_Put[2])

                                Active_status_read["Deactive Put Strike"].append(Strike_pe_2_remove_copy)
                                Active_status_read["Deactive Put Strike Premium Initial"].append(Active_Initial_Sold_premium_put[1])
                                Active_status_read["Deactive Put Strike SL"].append(Active_SL_Put[1])

                                Active_status_read["Deactive Put Strike"].append(Strike_pe_1_remove_copy)
                                Active_status_read["Deactive Put Strike Premium Initial"].append(Active_Initial_Sold_premium_put[0])
                                Active_status_read["Deactive Put Strike SL"].append(Active_SL_Put[0])

                                writing_Active_status(Active_status_read)
                                
                                Strike_pe_remove=Active_call_Strike[0]
                                Premium_to_remove=Active_Initial_Sold_premium_call[0]
                                SL_to_Remove=Active_SL_Call[0]
                                out=reversal_status_func(reversal_status,Strike_pe_remove,Premium_to_remove,SL_to_Remove)

                                break

                            else:
                                pass

                        else:
                            pass
                    else:
                        pass












                elif Market_trend=="Trending Down":
                    pass
                else:
                    pass
            



def morning_code():

    ## Path_expiry_renew ################
    ## Get the index at time checking time ####
    ## Read the Active Strikes, there SL and Initial Premium for both call and put from the text file ####
    ## Determing the closing price at the checking time for the Active Strikes ######
    ## If the closing price at Checking time is less than SL than return index at checking time and merge the DF of active strikes and then return it ####
    ## If not then check the market trend is the adjustment is along the direction of the trend then call volatility strike 
    ## If the movement is not along the direction of the trend then remove that specific strike ####

    pass

def table_recording_code():
    pass 

def writing_Active_status(Active_status):
    with open(Path_backtest_Report+"active_status.txt", "w") as file:
        for key, value in Active_status.items():
            file.write(f"{key}={','.join(map(str, value))}\n")

def read_Active_status():
    Active_status_read = {}
    with open("active_status.txt", "r") as file:
        for line in file:
            key, value_str = line.strip().split("=")
            value = [int(x) for x in value_str.split(",")]
            Active_status_read[key] = value

    return Active_status_read

start_time = datetime.strptime("9:15", "%H:%M")
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


for k in range(1):
    if formatted_Date_of_Expiry[k] in Rejected_Expiry_Dates:
        pass
    else:
        start_date = datetime.strptime(formatted_Date_of_Init[k], "%d-%b-%Y")
        end_date = datetime.strptime(formatted_Date_of_Expiry[k], "%d-%b-%Y")
        num_days=(end_date-start_date).days+1
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
                df_call_init['Time'] = df_call_init['Time'].apply(lambda x: x[:5])
                df_put_init['Time'] = df_put_init['Time'].apply(lambda x: x[:5])
                df_call_init,df_put_init=merging(df_call_init,df_put_init,"Call","Put")

                date_str = formatted_Date_of_Init[k]
                date_obj = datetime.strptime(date_str, "%d-%b-%Y")
                Desired_Date = date_obj.strftime("%Y-%m-%d")
                row_index_call = df_call_init.index[(df_call_init['Time'] == Desired_time)&(df_call_init['Date'] == Desired_Date)].tolist()
                row_index_put = df_put_init.index[(df_put_init['Time'] == Desired_time)&(df_put_init['Date'] == Desired_Date)].tolist()
                CE_price=df_call_init.loc[row_index_call,"close CE"]
                PE_price=df_put_init.loc[row_index_put,"close PE"]
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
                Active_status["Active_SL_Call"]=[SL_CE]
                Active_status["Active_SL_Put"]=[SL_PE]

                Active_status["Deactive Put Strike"]=[]
                Active_status["Deactive Put Strike Premium Initial"]=[]
                Active_status["Deactive Put Strike SL"]=[]
                Active_status["Deactive Call Strike"]=[]
                Active_status["Deactive Call Strike Premium Initial"]=[]
                Active_status["Deactive Call Strike SL"]=[]
                
                writing_Active_status(Active_status)

                
                running_index=row_index_call[0]
                Initial_day=formatted_Date_of_Init[k]
                Expiry_date=formatted_Date_of_Expiry[k]

                # table_recording_code()
                routine_code(running_index,Active_call_Strike,Active_put_Strike,Active_Initial_Sold_premium_call,Active_Initial_Sold_premium_put,Active_SL_Call,Active_SL_Put,Day,Initial_day,Expiry_date)
                
                Day=Day+1
            else:
                
                # morning_code()
                routine_code(running_index,Active_call_Strike,Active_put_Strike,Active_Initial_Sold_premium_call,Active_Initial_Sold_premium_put,Active_SL_Call,Active_SL_Put,Day,Initial_day,Expiry_date)
                # table_recording_code()
                Day=Day+1
                
