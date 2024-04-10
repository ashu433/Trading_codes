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
################### Variables of the startjee ##############

def merging(df_CE,df_PE,Right_1,Right_2):
    if Right_1=="Call" and Right_2=="Put":
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


def Execution_check_Code(Triggered_time,Date,index_row,Closing_price,DF,right):

    while True:
        if right=="CE":
            high_max=max(DF.loc[index_row+1,"high CE"],DF.loc[index_row+2,"high CE"],DF.loc[index_row+3,"high CE"],DF.loc[index_row+4,"high CE"],DF.loc[index_row+5,"high CE"])
            low_min=min(DF.loc[index_row+1,"low CE"],DF.loc[index_row+2,"low CE"],DF.loc[index_row+3,"low CE"],DF.loc[index_row+4,"low CE"],DF.loc[index_row+5,"low CE"])
        elif right=="PE":
            high_max=max(DF.loc[index_row+1,"high PE"],DF.loc[index_row+2,"high PE"],DF.loc[index_row+3,"high PE"],DF.loc[index_row+4,"high PE"],DF.loc[index_row+5,"high PE"])
            low_min=min(DF.loc[index_row+1,"low PE"],DF.loc[index_row+2,"low PE"],DF.loc[index_row+3,"low PE"],DF.loc[index_row+4,"low PE"],DF.loc[index_row+5,"low PE"])
        else:
            pass

        if low_min<=Closing_price<=high_max:
            break
        else:
            index=time_list.index(Triggered_time)
            time_new=time_list[index+1]
            index_row = DF.index[(DF['Time'] == time_new)&(DF['Date'] == Date)].tolist()
            index_row=index_row[0]
            if right=="CE":
                Closing_price=DF.loc[index_row,"close CE"]
            elif right=="PE":
                Closing_price=DF.loc[index_row,"close PE"]

    return Closing_price,index_row,time_new


def date_to_week(date):
    date_object = datetime.strptime(date, "%Y-%m-%d")
    day_of_week = date_object.strftime('%A')
    return day_of_week




def volatility_strike_pred(Date,Time,path_expiry_date_recurring,Startjee_1_dict_Call,Startjee_1_dict_Put,CE_Strike_1=None,CE_Strike_2=None,CE_Strike_3=None,CE_Strike_4=None,PE_Strike_1=None,PE_Strike_2=None,PE_Strike_3=None,PE_Strike_4=None,Len_pe=None,Len_ce=None):
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
            Startjee_1_dict_Call.pop(CE_Strike_1)

            Call_stk_1.append(-CE_Strike_1)


            week=date_to_week(Date)


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


            if (len(df_CE.loc[4,'Time']))>5:
                df_CE['Time'] = df_CE['Time'].apply(lambda x: x[:5])
                df_PE_1['Time'] = df_PE_1['Time'].apply(lambda x: x[:5])
                df_PE_2['Time'] = df_PE_2['Time'].apply(lambda x: x[:5])
            else:
                pass

            index_row = df_CE.index[(df_CE['Time'] == Triggered_time)&(df_CE['Date'] == Date)].tolist()
            index_row=index_row[0]

            CP_CE=df_CE.loc[index_row,"close CE"]
            CP_CE,index_row_CE,time_obs_CE=Execution_check_Code(Triggered_time,Date,index_row,CP_CE,df_CE,"CE")

            running_log_update("Entry","Call_stk_2",CE_Strike_2,"Call",time_obs_CE,Date,week,formatted_Date_of_Init[k],formatted_Date_of_Expiry[k],0,0)
            


            CP_PE_2=df_PE_2.loc[index_row,"close PE"]
            CP_PE_2,index_row_PE,time_obs_PE=Execution_check_Code(Triggered_time,Date,index_row,CP_PE_2,df_PE_2,"PE")

            running_log_update("Entry","Put_stk_2",PE_Strike_2,"Put",time_obs_PE,Date,week,formatted_Date_of_Init[k],formatted_Date_of_Expiry[k],0,0)
         
            
            index_row=min(index_row_CE,index_row_PE)

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
            Startjee_1_dict_Call.pop(CE_Strike_2)

            week=date_to_week(Date)

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

            if (len(df_CE_3.loc[4,'Time']))>5:
                df_CE_3['Time'] = df_CE_3['Time'].apply(lambda x: x[:5])
                df_PE_1['Time'] = df_PE_1['Time'].apply(lambda x: x[:5])
                df_PE_2['Time'] = df_PE_2['Time'].apply(lambda x: x[:5]) 
                df_PE_3['Time'] = df_PE_3['Time'].apply(lambda x: x[:5]) 
            else:
                pass

            index_row = df_CE_3.index[(df_CE_3['Time'] == Triggered_time)&(df_CE_3['Date'] == Date)].tolist()
            index_row=index_row[0]

            CP_CE_3=df_CE_3.loc[index_row,"close CE"]
            CP_CE_3,index_row_CE,time_obs_CE=Execution_check_Code(Triggered_time,Date,index_row,CP_CE_3,df_CE_3,"CE")

            running_log_update("Entry","Call_stk_3",CE_Strike_3,"Call",time_obs_CE,Date,week,formatted_Date_of_Init[k],formatted_Date_of_Expiry[k],0,0)

            CP_PE_3=df_PE_3.loc[index_row,"close PE"]
            CP_PE_3,index_row_PE,time_obs_PE=Execution_check_Code(Triggered_time,Date,index_row,CP_PE_3,df_PE_3,"PE")

            running_log_update("Entry","Put_stk_3",PE_Strike_3,"Put",time_obs_PE,Date,week,formatted_Date_of_Init[k],formatted_Date_of_Expiry[k],0,0)

            index_row=min(index_row_CE,index_row_PE)

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
            Startjee_1_dict_Call.pop(CE_Strike_3)

            week=date_to_week(Date)


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

            if (len(df_PE_1.loc[4,'Time']))>5:
                df_PE_1['Time'] = df_PE_1['Time'].apply(lambda x: x[:5])
                df_PE_2['Time'] = df_PE_2['Time'].apply(lambda x: x[:5]) 
                df_PE_3['Time'] = df_PE_3['Time'].apply(lambda x: x[:5]) 
                df_PE_4['Time'] = df_PE_4['Time'].apply(lambda x: x[:5])
            else:
                pass
            index_row = df_PE_1.index[(df_PE_1['Time'] == Triggered_time)&(df_PE_1['Date'] == Date)].tolist()
            index_row=index_row[0]
            CP_PE_4=df_PE_4.loc[index_row,"close PE"]
            CP_PE_4,index_row,time_obs_PE=Execution_check_Code(Triggered_time,Date,index_row,CP_PE_4,df_PE_4,"PE")

            running_log_update("Entry","Put_stk_4",PE_Strike_4,"Put",time_obs_PE,Date,week,formatted_Date_of_Init[k],formatted_Date_of_Expiry[k],1,0,"Call_stk_3")

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
    
    elif Market_trend=="Trending Down":

        if Len_ce==1:

            PE_Strike_2=PE_Strike_1+offset
            Startjee_1_dict_Put.pop(PE_Strike_1)

            week=date_to_week(Date)

            Active_put_Strike=[]
            Active_put_Strike.append(PE_Strike_2)
            Active_call_Strike.append(CE_Strike_2)


            file_ce_1=f"NIFTY{str(CE_Strike_1)}_CE.csv"
            file_ce_2=f"NIFTY{str(CE_Strike_2)}_CE.csv"
            file_pe_2=f"NIFTY{str(PE_Strike_2)}_PE.csv"        

            df_CE_1=pd.read_csv(path_expiry_date_recurring+file_ce_1)
            df_CE_2=pd.read_csv(path_expiry_date_recurring+file_ce_2)
            df_PE_2=pd.read_csv(path_expiry_date_recurring+file_pe_2)

            df_CE_1,df_CE_2=merging(df_CE_1,df_CE_2,"Call","Call")
            df_CE_2,df_PE_2=merging(df_CE_2,df_PE_2,"Call","Put")

            if (len(df_CE_2.loc[4,'Time']))>5:
                df_CE_2['Time'] = df_CE_2['Time'].apply(lambda x: x[:5])
                df_CE_1['Time'] = df_CE_1['Time'].apply(lambda x: x[:5])
                df_PE_2['Time'] = df_PE_2['Time'].apply(lambda x: x[:5])
            else:
                pass

            index_row = df_CE_1.index[(df_CE_1['Time'] == Triggered_time)&(df_CE_1['Date'] == Date)].tolist()
            index_row=index_row[0]

            CP_PE=df_PE_2.loc[index_row,"close PE"]
            CP_PE,index_row_PE,time_obs_PE=Execution_check_Code(Triggered_time,Date,index_row,CP_PE,df_PE_2,"PE")

            running_log_update("Entry","Put_stk_2",PE_Strike_2,"Put",time_obs_PE,Date,week,formatted_Date_of_Init[k],formatted_Date_of_Expiry[k],0,0)
            

            CP_CE_2=df_CE_2.loc[index_row,"close CE"]
            CP_CE_2,index_row_CE,time_obs_CE=Execution_check_Code(Triggered_time,Date,index_row,CP_CE_2,df_CE_2,"CE")

            running_log_update("Entry","Call_stk_2",CE_Strike_2,"Call",time_obs_CE,Date,week,formatted_Date_of_Init[k],formatted_Date_of_Expiry[k],0,0)

            index_row=min(index_row_CE,index_row_PE)

            SL_PE=2*CP_PE
            SL_CE_2=2*CP_CE_2

            Active_status_read=read_Active_status()
            Active_status_read["Deactive Put Strike"].append(PE_Strike_1)
            Active_status_read["Deactive Put Strike Premium Initial"].append(Active_Initial_Sold_premium_put[0])
            Active_status_read["Deactive Put Strike SL"].append(Active_SL_Put[0])

            Active_status_read["Active_put_Strike"].remove(PE_Strike_1)
            Active_status_read["Active_Initial_Sold_premium_put"].remove(Active_Initial_Sold_premium_put[0])
            Active_status_read["Active_SL_Put"].remove(Active_SL_Put[0])

            Active_status_read["Active_call_Strike"].append(PE_Strike_2)
            Active_status_read["Active_Initial_Sold_premium_call"].append(CP_PE)
            Active_status_read["Active_SL_Call"].append(SL_PE)

            Active_status_read["Active_call_Strike"].append(CE_Strike_2)
            Active_status_read["Active_Initial_Sold_premium_call"].append(CP_CE_2)
            Active_status_read["Active_SL_Call"].append(SL_CE_2)

            writing_Active_status(Active_status_read)

            Active_Initial_Sold_premium_put=[]
            Active_SL_Put=[]
            Active_Initial_Sold_premium_put.append(CP_PE)
            Active_SL_Put.append(SL_PE)
            Active_Initial_Sold_premium_call.append(CP_CE_2)
            Active_SL_Call.append(SL_CE_2)


            
            rows=df_CE_2.shape[0]
            run_len=rows-index_row

            return index_row,df_CE_1,df_CE_2,df_PE_2
        
        elif Len_ce==2:

            PE_Strike_3=PE_Strike_2+offset
            Startjee_1_dict_Put.pop(PE_Strike_2)

            week=date_to_week(Date)

            Active_put_Strike=[]
            Active_put_Strike.append(PE_Strike_3)
            Active_call_Strike.append(CE_Strike_3)


            file_ce_3=f"NIFTY{str(CE_Strike_3)}_CE.csv"
            file_ce_2=f"NIFTY{str(CE_Strike_2)}_CE.csv"
            file_ce_1=f"NIFTY{str(CE_Strike_1)}_CE.csv"
            file_pe_3=f"NIFTY{str(PE_Strike_3)}_PE.csv"

            df_CE_3=pd.read_csv(path_expiry_date_recurring+file_ce_3)
            df_CE_2=pd.read_csv(path_expiry_date_recurring+file_ce_2)
            df_CE_1=pd.read_csv(path_expiry_date_recurring+file_ce_1)
            df_PE_3=pd.read_csv(path_expiry_date_recurring+file_pe_3)

            df_CE_3,df_CE_2=merging(df_CE_3,df_CE_2,"Call","Call")
            df_CE_2,df_CE_1=merging(df_CE_2,df_CE_1,"Call","Call")
            df_PE_3,df_CE_2=merging(df_PE_3,df_PE_1,"Put","Call")

            if (len(df_CE_3.loc[4,'Time']))>5:
                df_CE_3['Time'] = df_CE_3['Time'].apply(lambda x: x[:5])
                df_CE_2['Time'] = df_CE_2['Time'].apply(lambda x: x[:5])
                df_CE_1['Time'] = df_CE_1['Time'].apply(lambda x: x[:5])
                df_PE_3['Time'] = df_PE_3['Time'].apply(lambda x: x[:5])  
            else:
                pass

            index_row = df_CE_3.index[(df_CE_3['Time'] == Triggered_time)&(df_CE_3['Date'] == Date)].tolist()
            index_row=index_row[0]

            CP_CE_3=df_CE_3.loc[index_row,"close CE"]
            CP_CE_3,index_row_CE,time_obs_CE=Execution_check_Code(Triggered_time,Date,index_row,CP_CE_3,df_CE_3,"CE")

            running_log_update("Entry","Call_stk_3",CE_Strike_3,"Call",time_obs_CE,Date,week,formatted_Date_of_Init[k],formatted_Date_of_Expiry[k],0,0)
            

            CP_PE_3=df_PE_3.loc[index_row,"close PE"]
            CP_PE_3,index_row_PE,time_obs_PE=Execution_check_Code(Triggered_time,Date,index_row,CP_PE_3,df_PE_3,"PE")

            running_log_update("Entry","Put_stk_3",PE_Strike_3,"Put",time_obs_PE,Date,week,formatted_Date_of_Init[k],formatted_Date_of_Expiry[k],0,0)

            index_row=min(index_row_CE,index_row_PE)
            
            SL_CE_3=2*CP_CE_3
            SL_PE_3=2*CP_PE_3

            Active_status_read=read_Active_status()
            Active_status_read["Deactive Put Strike"].append(PE_Strike_2)
            Active_status_read["Deactive Put Strike Premium Initial"].append(Active_Initial_Sold_premium_put[0])
            Active_status_read["Deactive Put Strike SL"].append(Active_SL_Put[0])

            Active_status_read["Active_put_Strike"].remove(PE_Strike_2)
            Active_status_read["Active_Initial_Sold_premium_put"].remove(Active_Initial_Sold_premium_put[0])
            Active_status_read["Active_SL_Put"].remove(Active_SL_Put[0])

            Active_status_read["Active_put_Strike"].append(PE_Strike_3)
            Active_status_read["Active_Initial_Sold_premium_put"].append(CP_PE_3)
            Active_status_read["Active_SL_Put"].append(SL_PE_3)

            Active_status_read["Active_call_Strike"].append(CE_Strike_3)
            Active_status_read["Active_Initial_Sold_premium_call"].append(CP_CE_3)
            Active_status_read["Active_SL_Call"].append(SL_CE_3)

            writing_Active_status(Active_status_read)

            Active_Initial_Sold_premium_put=[]
            Active_SL_Put=[]
            Active_Initial_Sold_premium_put.append(CP_PE_3)
            Active_SL_Put.append(SL_PE_3)
            Active_Initial_Sold_premium_call.append(CP_CE_3)
            Active_SL_Call.append(SL_CE_3)
            
            rows=df_CE_3.shape[0]
            run_len=rows-index_row

            return index_row,df_CE_3,df_CE_2,df_CE_1,df_PE_3   
        
        elif Len_ce==3:

            Active_put_Strike=[]
            Active_call_Strike.append(CE_Strike_4)
            Startjee_1_dict_Put.pop(PE_Strike_3)

            week=date_to_week(Date)


            file_ce_4=f"NIFTY{str(CE_Strike_4)}_CE.csv"
            file_ce_3=f"NIFTY{str(CE_Strike_3)}_CE.csv"
            file_ce_2=f"NIFTY{str(CE_Strike_2)}_CE.csv"
            file_ce_1=f"NIFTY{str(CE_Strike_1)}_CE.csv"

            df_CE_1=pd.read_csv(path_expiry_date_recurring+file_ce_1)
            df_CE_2=pd.read_csv(path_expiry_date_recurring+file_ce_2)
            df_CE_3=pd.read_csv(path_expiry_date_recurring+file_ce_3)
            df_CE_4=pd.read_csv(path_expiry_date_recurring+file_ce_4)

            df_CE_2,df_CE_1=merging(df_CE_2,df_CE_1,"Call","Call")
            df_CE_3,df_CE_1=merging(df_CE_3,df_CE_1,"Call","Call")
            df_CE_4,df_CE_3=merging(df_CE_4,df_CE_3,"Call","Call")

            if (len(df_CE_3.loc[4,'Time']))>5:
                df_CE_3['Time'] = df_CE_3['Time'].apply(lambda x: x[:5])
                df_CE_2['Time'] = df_CE_2['Time'].apply(lambda x: x[:5])
                df_CE_1['Time'] = df_CE_1['Time'].apply(lambda x: x[:5])
                df_CE_4['Time'] = df_CE_4['Time'].apply(lambda x: x[:5])  
            else:
                pass

            index_row = df_CE_1.index[(df_CE_1['Time'] == Triggered_time)&(df_CE_1['Date'] == Date)].tolist()
            index_row=index_row[0]
            CP_CE_4=df_CE_4.loc[index_row,"close PE"]
            CP_CE_4,index_row,time_obs_CE=Execution_check_Code(Triggered_time,Date,index_row,CP_CE_4,df_CE_4,"CE")

            running_log_update("Entry","Call_stk_4",CE_Strike_4,"Call",time_obs_CE,Date,week,formatted_Date_of_Init[k],formatted_Date_of_Expiry[k],0,1,"PE_Strike_3")

            SL_CE_4=2*CP_CE_4

            Active_status_read=read_Active_status()
            Active_status_read["Deactive Put Strike"].append(PE_Strike_3)
            Active_status_read["Deactive Put Strike Premium Initial"].append(Active_Initial_Sold_premium_put[0])
            Active_status_read["Deactive Put Strike SL"].append(Active_SL_Put[0])

            Active_status_read["Active_put_Strike"].remove(PE_Strike_3)
            Active_status_read["Active_Initial_Sold_premium_put"].remove(Active_Initial_Sold_premium_put[0])
            Active_status_read["Active_SL_Put"].remove(Active_SL_Put[0])

            Active_status_read["Active_call_Strike"].append(CE_Strike_4)
            Active_status_read["Active_Initial_Sold_premium_call"].append(CP_CE_4)
            Active_status_read["Active_SL_Call"].append(SL_CE_4)

            writing_Active_status(Active_status_read)

            Active_Initial_Sold_premium_put=[]
            Active_SL_Put=[]
            Active_Initial_Sold_premium_call.append(CP_CE_4)
            Active_SL_Call.append(SL_CE_4)
            run_len=rows-index_row

            return index_row,df_CE_1,df_CE_2,df_CE_3,df_CE_4



def update_lists_call(list_name, value):
    all_lists = [Call_stk_1, Call_stk_2, Call_stk_3, Call_stk_4, Put_stk_1, Put_stk_2, Put_stk_3, Put_stk_4]

    if list_name == "Call_stk_1":
        Call_stk_1.append(value)
        for lst in [Call_stk_2, Call_stk_3, Call_stk_4, Put_stk_1, Put_stk_2, Put_stk_3, Put_stk_4]:
            lst.append(None)
    elif list_name == "Call_stk_2":
        Call_stk_2.append(value)
        for lst in [Call_stk_1, Call_stk_3, Call_stk_4, Put_stk_1, Put_stk_2, Put_stk_3, Put_stk_4]:
            lst.append(None)
    elif list_name == "Call_stk_3":
        Call_stk_3.append(value)
        for lst in [Call_stk_1, Call_stk_2, Call_stk_4, Put_stk_1, Put_stk_2, Put_stk_3, Put_stk_4]:
            lst.append(None)
    elif list_name == "Call_stk_4":
        Call_stk_4.append(value)
        for lst in [Call_stk_1, Call_stk_2, Call_stk_3, Put_stk_1, Put_stk_2, Put_stk_3, Put_stk_4]:
            lst.append(None)
    else:
        pass


def update_lists_put(list_name, value):
        
    if list_name == "Put_stk_1":
        Put_stk_1.append(value)
        for lst in [Call_stk_1, Call_stk_2, Call_stk_3, Call_stk_4, Put_stk_2, Put_stk_3, Put_stk_4]:
            lst.append(None)
    elif list_name == "Put_stk_2":
        Put_stk_2.append(value)
        for lst in [Call_stk_1, Call_stk_2, Call_stk_3, Call_stk_4, Put_stk_1, Put_stk_3, Put_stk_4]:
            lst.append(None)
    elif list_name == "Put_stk_3":
        Put_stk_3.append(value)
        for lst in [Call_stk_1, Call_stk_2, Call_stk_3, Call_stk_4, Put_stk_1, Put_stk_2, Put_stk_4]:
            lst.append(None)
    elif list_name == "Put_stk_4":
        Put_stk_4.append(value)
        for lst in [Call_stk_1, Call_stk_2, Call_stk_3, Call_stk_4, Put_stk_1, Put_stk_2, Put_stk_3]:
            lst.append(None)
    else:
        pass


def running_log_update(entry_exit,list_name,Strike_entry,right,time,date,week,initiation_date,expiry_date,last_pe,last_ce,alternate_strike=None):

    if entry_exit=="Entry" and right=="Call" and last_ce==0 and last_pe==0:
        update_lists_call(list_name,Strike_entry)
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
        sl_hit_date.append(date)
        sl_hit_time.append(time)
        sl_hit_week.append(date)

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
        sl_hit_date.append(date)
        sl_hit_time.append(time)
        sl_hit_week.append(date)

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

    week=date_to_week(expiry_date)

    update_lists_call(alternate_strike_call,None)
    update_lists_put(alternate_strike_put,None)
    Entry_time_call.append("15:30")
    Entry_date.append(expiry_date)
    Entry_week.append(week)

    sl_hit_date.append(expiry_date)
    sl_hit_time.append("15:30")
    sl_hit_week.append(None)




def routine_code(index_row,Active_call_Strike,Active_put_Strike,Active_Initial_Sold_premium_call,Active_Initial_Sold_premium_put,Active_SL_Call,Active_SL_Put,Day,Initial_day,Expiry_date):
    global run_len
    global Market_trend
    global df_call_init
    global df_put_init
    global Net_P_L
    global reversal_status

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

            if Day!=0:
                if Market_trend=="Neutral":
                    index_row,df_ce,df_pe=morning_code(path_expiry_date_recurring,output_date)
                    df_call_init=df_ce
                    df_put_init=df_pe
                    running_index=index_row
                elif Market_trend=="Trending Up":
                    len_pe_1=len(Active_put_Strike)

                    if len_pe_1==2:
                        index_row,df_CE,df_PE_1,df_PE_2=morning_code(path_expiry_date_recurring,output_date)
                    elif len_pe_1==3:
                        index_row,df_CE_3,df_PE_1,df_PE_2,df_PE_3=morning_code(path_expiry_date_recurring,output_date)
                    elif len_pe_1==4:
                        index_row,df_PE_1,df_PE_2,df_PE_3,df_PE_4=morning_code(path_expiry_date_recurring,output_date)
                    else:
                        pass
                
                elif Market_trend=="Trending Down":

                    len_ce_1=len(Active_call_Strike)

                    if len_ce_1==2:
                        index_row,df_CE_1,df_CE_2,df_PE_2=morning_code(path_expiry_date_recurring,output_date)
                    elif len_ce_1==3:
                        index_row,df_CE_1,df_CE_2,df_CE_3,df_PE_3=morning_code(path_expiry_date_recurring,output_date)
                    elif len_ce_1==4:
                        index_row,df_CE_1,df_CE_2,df_CE_3,df_CE_4=morning_code(path_expiry_date_recurring,output_date)
                    else:
                        pass


            if Market_trend=="Neutral":
                CE_Strike=Active_call_Strike[0]
                PE_Strike=Active_put_Strike[0]
                rows=df_call_init.shape[0]
                run_len=rows-index_row
                ce_initial_Price=Active_Initial_Sold_premium_call[0]
                pe_initial_Price=Active_Initial_Sold_premium_put[0]

            for i in range(run_len):

                if Market_trend=="Neutral":
                    CE_SL=Active_SL_Call[0]
                    PE_SL=Active_SL_Put[0]

                    CE_Current_pr=df_call_init.loc[(i+index_row+1),"high CE"]
                    PE_Current_pr_1=df_put_init.loc[(i+index_row+1),"high PE"]

                    CE_Current_pr_close=df_call_init.loc[(i+index_row+1),"close CE"]
                    PE_Current_pr_1_close=df_put_init.loc[(i+index_row+1),"close PE"]

                    Startjee_1_dict_Call[Call_Strike]=[CE_Current_pr,ce_initial_Price,CE_SL]
                    Startjee_1_dict_Put[Put_Strike]=[PE_Current_pr_1,pe_initial_Price,PE_SL]

                    CE_instantinious_pr=[CE_Current_pr_close]
                    PE_instantinious_pr=[PE_Current_pr_1_close]


                    if df_call_init.loc[(index_row+i+1),"high CE"]<CE_SL and df_put_init.loc[(index_row+i+1),"high PE"]<PE_SL:
                        call_premium_collected=ce_initial_Price-df_call_init.loc[(index_row+i+1),"close CE"]
                        put_premium_collected=pe_initial_Price-df_put_init.loc[(index_row+i+1),"close PE"]
                        Net_P_L=Net_P_L+call_premium_collected+put_premium_collected
                        time=df_call_init.loc[(index_row+i+1),"Time"]

                        SL_update(time,Active_Initial_Sold_premium_call,Active_Initial_Sold_premium_put,CE_instantinious_pr,PE_instantinious_pr,Active_call_Strike,Active_put_Strike,Active_SL_Call,Active_SL_Put,reversal_status,Startjee_1_dict_Call,Startjee_1_dict_Put)

                    elif df_call_init.loc[(index_row+i+1),"high CE"]>=CE_SL and df_put_init.loc[(index_row+i+1),"high PE"]<PE_SL:
                        current_strike_CE=CE_Strike
                        PE_Strike_2=PE_Strike+50
                        Market_trend="Trending Up"

                        call_premium_collected=ce_initial_Price-CE_SL
                        put_premium_collected=pe_initial_Price-df_put_init.loc[(index_row+i+1),"close PE"]
                        Net_P_L=Net_P_L+call_premium_collected+put_premium_collected

                        Time=df_call_init.loc[(index_row+i+1),"Time"]
                        Date=df_call_init.loc[(index_row+i+1),"Date"]
                        week=date_to_week(Date)

                        running_log_update("SL_Hit","Call_stk_1",CE_Strike,"Call",Time,Date,week,formatted_Date_of_Init[k],formatted_Date_of_Expiry[k],0,0)

                        index_row,df_CE,df_PE_1,df_PE_2=volatility_strike_pred(Date,Time,path_expiry_date_recurring,Startjee_1_dict_Call,Startjee_1_dict_Put,current_strike_CE,0,0,0,PE_Strike,PE_Strike_2,0,0,Len_pe,1)

                    elif df_call_init.loc[(index_row+i+1),"high CE"]<CE_SL and df_put_init.loc[(index_row+i+1),"high PE"]>=PE_SL:
                        PE_Strike_1=PE_Strike
                        CE_Strike_2=CE_Strike-50
                        Market_trend="Trending Down"

                        call_premium_collected=ce_initial_Price-df_call_init.loc[(index_row+i+1),"close CE"]
                        put_premium_collected=pe_initial_Price-PE_SL
                        Net_P_L=Net_P_L+call_premium_collected+put_premium_collected

                        Time=df_call_init.loc[(index_row+i+1),"Time"]
                        Date=df_call_init.loc[(index_row+i+1),"Date"]
                        week=date_to_week(Date)

                        running_log_update("SL_Hit","Put_stk_1",PE_Strike,"Put",Time,Date,week,formatted_Date_of_Init[k],formatted_Date_of_Expiry[k],0,0)

                        index_row,df_CE_1,df_CE_2,df_PE_2=volatility_strike_pred(Date,Time,path_expiry_date_recurring,Startjee_1_dict_Call,Startjee_1_dict_Put,CE_Strike,CE_Strike_2,0,0,PE_Strike_1,0,0,0,1,Len_ce)
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

                        CE_Current_pr_close=df_CE.loc[(i+index_row+1),"close CE"]
                        PE_Current_pr_1_close=df_PE_1.loc[(i+index_row+1),"close PE"]
                        PE_Current_pr_2_close=df_PE_2.loc[(i+index_row+1),"close PE"]

                        CE_instantinious_pr=[CE_Current_pr_close]
                        PE_instantinious_pr=[PE_Current_pr_1_close,PE_Current_pr_2_close]

                        ce_initial_Price=Active_Initial_Sold_premium_call[0]
                        pe_initial_Price_1=Active_Initial_Sold_premium_put[0]
                        pe_initial_Price_2=Active_Initial_Sold_premium_put[1]

                        Startjee_1_dict_Call[Active_call_Strike[0]]=[CE_Current_pr_close,ce_initial_Price,CE_SL]
                        Startjee_1_dict_Put[Active_put_Strike[0]]=[PE_Current_pr_1_close,pe_initial_Price_1,PE_1_SL]
                        Startjee_1_dict_Put[Active_put_Strike[1]]=[PE_Current_pr_2_close,pe_initial_Price_2,PE_2_SL]


                        if CE_Current_pr<CE_SL and PE_Current_pr_1<PE_1_SL and PE_Current_pr_2<PE_2_SL:
                            call_premium_collected=ce_initial_Price-df_CE.loc[(index_row+i+1),"close CE"]
                            put_premium_collected_1=pe_initial_Price_1-df_PE_1.loc[(index_row+i+1),"close PE"]
                            put_premium_collected_2=pe_initial_Price_2-df_PE_2.loc[(index_row+i+1),"close PE"]
                            Net_P_L=Net_P_L+call_premium_collected+put_premium_collected_1+put_premium_collected_2
                            
                            time=df_CE.loc[(index_row+i+1),"Time"]
                            SL_update(time,Active_Initial_Sold_premium_call,Active_Initial_Sold_premium_put,CE_instantinious_pr,PE_instantinious_pr,Active_call_Strike,Active_put_Strike,Active_SL_Call,Active_SL_Put,reversal_status,Startjee_1_dict_Call,Startjee_1_dict_Put)

                        elif CE_Current_pr>=CE_SL and PE_Current_pr_1<PE_1_SL and PE_Current_pr_2<PE_2_SL:
                            CE_Strike_2=Active_call_Strike[0]
                            PE_strike_3=Active_put_Strike[1]+50
                            PE_strike_2=Active_put_Strike[1]
                            PE_strike_1=Active_put_Strike[0]

                            call_premium_collected=ce_initial_Price-CE_SL
                            put_premium_collected_1=pe_initial_Price_1-df_PE_1.loc[(index_row+i+1),"close PE"]
                            put_premium_collected_2=pe_initial_Price_2-df_PE_2.loc[(index_row+i+1),"close PE"]
                            Net_P_L=Net_P_L+call_premium_collected+put_premium_collected_1+put_premium_collected_2

                            Time=df_CE.loc[(index_row+i+1),"Time"]
                            Date=df_CE.loc[(index_row+i+1),"Date"]

                            week=date_to_week(Date)

                            running_log_update("SL_Hit","Call_stk_2",CE_Strike_2,"Call",Time,Date,week,formatted_Date_of_Init[k],formatted_Date_of_Expiry[k],0,0)

                            index_row,df_CE_3,df_PE_1,df_PE_2,df_PE_3=volatility_strike_pred(Date,Time,path_expiry_date_recurring,Startjee_1_dict_Call,Startjee_1_dict_Put,0,CE_Strike_2,0,0,PE_strike_1,PE_Strike_2,PE_strike_3,0,Len_pe,1)

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

                                call_premium_collected=ce_initial_Price-df_CE.loc[(index_row+i+1),"close CE"]
                                put_premium_collected_1=pe_initial_Price_1-df_PE_1.loc[(index_row+i+1),"close PE"]
                                Net_P_L=Net_P_L+call_premium_collected+put_premium_collected_1
                                time=df_CE.loc[(index_row+i+1),"Time"]
                                SL_update(time,Active_Initial_Sold_premium_call,Active_Initial_Sold_premium_put,CE_instantinious_pr,PE_instantinious_pr,Active_call_Strike,Active_put_Strike,Active_SL_Call,Active_SL_Put,reversal_status,Startjee_1_dict_Call,Startjee_1_dict_Put)
                            else:
                                call_premium_collected=ce_initial_Price-df_CE.loc[(index_row+i+1),"close CE"]
                                put_premium_collected_1=pe_initial_Price_1-df_PE_1.loc[(index_row+i+1),"close PE"]
                                Net_P_L=Net_P_L+call_premium_collected+put_premium_collected_1
                                time=df_CE.loc[(index_row+i+1),"Time"]
                                SL_update(time,Active_Initial_Sold_premium_call,Active_Initial_Sold_premium_put,CE_instantinious_pr,PE_instantinious_pr,Active_call_Strike,Active_put_Strike,Active_SL_Call,Active_SL_Put,reversal_status,Startjee_1_dict_Call,Startjee_1_dict_Put)

                        elif CE_Current_pr>=CE_SL and PE_Current_pr_1<PE_1_SL and PE_Current_pr_2>=PE_2_SL:

                            Active_status_read=read_Active_status()
                            deleted_strike_pe=Active_status_read["Deactive Put Strike"]
                            deleted_strike_ce=Active_status_read["Deactive Call Strike"]

                            Put_strikes_remove=Active_status_read["Active_put_Strike"]
                            Call_Strikes_remove=Active_status_read["Active_call_Strike"]
                            Strike_ce_remove_copy=Call_Strikes_remove[0]
                            Strike_pe_remove_copy=Put_strikes_remove[1]

                            if Strike_pe_remove_copy not in deleted_strike_pe or Strike_ce_remove_copy not in deleted_strike_ce:  
                                reversal_status=21110 #" the format is len,rev,CE_2,PE_2,PE_1"

                                Active_status_read["Deactive Put Strike"].append(Strike_pe_remove_copy)
                                Active_status_read["Deactive Call Strike"].append(Strike_ce_remove_copy)
                                Active_status_read["Deactive Call Strike Premium Initial"].append(Active_Initial_Sold_premium_call[0])
                                Active_status_read["Deactive Call Strike SL"].append(Active_SL_Call[0])
                                Active_status_read["Deactive Put Strike Premium Initial"].append(Active_Initial_Sold_premium_put[1])
                                Active_status_read["Deactive Put Strike SL"].append(Active_SL_Put[1])
                                writing_Active_status(Active_status_read)




                                put_premium_collected_1=pe_initial_Price_1-df_PE_1.loc[(index_row+i+1),"close PE"]
                                Net_P_L=Net_P_L+put_premium_collected_1
                                time=df_PE_1.loc[(index_row+i+1),"Time"]
                                SL_update(time,Active_Initial_Sold_premium_call,Active_Initial_Sold_premium_put,CE_instantinious_pr,PE_instantinious_pr,Active_call_Strike,Active_put_Strike,Active_SL_Call,Active_SL_Put,reversal_status,Startjee_1_dict_Call,Startjee_1_dict_Put)
                            else:
                                put_premium_collected_1=pe_initial_Price_1-df_PE_1.loc[(index_row+i+1),"close PE"]
                                Net_P_L=Net_P_L+put_premium_collected_1
                                time=df_PE_1.loc[(index_row+i+1),"Time"]
                                SL_update(time,Active_Initial_Sold_premium_call,Active_Initial_Sold_premium_put,CE_instantinious_pr,PE_instantinious_pr,Active_call_Strike,Active_put_Strike,Active_SL_Call,Active_SL_Put,reversal_status,Startjee_1_dict_Call,Startjee_1_dict_Put)

                        elif CE_Current_pr<CE_SL and PE_Current_pr_1>=PE_1_SL and PE_Current_pr_2>=PE_2_SL:

                            Active_status_read=read_Active_status()
                            deleted_strike_pe=Active_status_read["Deactive Put Strike"]
                            Put_strikes_remove=Active_status_read["Active_put_Strike"]

                            Strike_pe_1_remove_copy=Put_strikes_remove[0]
                            Strike_pe_2_remove_copy=Put_strikes_remove[1]

                            if Strike_pe_1_remove_copy not in deleted_strike or Strike_pe_2_remove_copy not in deleted_strike:  
                                reversal_status=21011 #" the format is len,rev,CE_2,PE_2,PE_1"
                                Active_status_read["Deactive Put Strike"].append(Strike_pe_1_remove_copy)
                                Active_status_read["Deactive Put Strike"].append(Strike_pe_2_remove_copy)
                                Active_status_read["Deactive Put Strike Premium Initial"].append(Active_Initial_Sold_premium_put[0])
                                Active_status_read["Deactive Put Strike Premium Initial"].append(Active_Initial_Sold_premium_put[1])
                                Active_status_read["Deactive Put Strike SL"].append(Active_SL_Put[0])
                                Active_status_read["Deactive Put Strike SL"].append(Active_SL_Put[1])


                                writing_Active_status(Active_status_read)

                                call_premium_collected=ce_initial_Price-df_CE.loc[(index_row+i+1),"close CE"]
                                Net_P_L=Net_P_L+call_premium_collected
                                time=df_CE.loc[(index_row+i+1),"Time"]
                                SL_update(time,Active_Initial_Sold_premium_call,Active_Initial_Sold_premium_put,CE_instantinious_pr,PE_instantinious_pr,Active_call_Strike,Active_put_Strike,Active_SL_Call,Active_SL_Put,reversal_status,Startjee_1_dict_Call,Startjee_1_dict_Put)
                            else:
                                call_premium_collected=ce_initial_Price-df_CE.loc[(index_row+i+1),"close CE"]
                                Net_P_L=Net_P_L+call_premium_collected
                                time=df_CE.loc[(index_row+i+1),"Time"]
                                SL_update(time,Active_Initial_Sold_premium_call,Active_Initial_Sold_premium_put,CE_instantinious_pr,PE_instantinious_pr,Active_call_Strike,Active_put_Strike,Active_SL_Call,Active_SL_Put,reversal_status,Startjee_1_dict_Call,Startjee_1_dict_Put)

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
                            if Strike_pe_1_remove_copy not in deleted_strike_pe or Strike_pe_2_remove_copy not in deleted_strike_pe or Strike_ce_1_remove_copy not in deleted_strike_ce:  
                                reversal_status=21111 #" the format is len,rev,CE_2,PE_2,PE_1"
                                Active_status_read["Deactive Put Strike"].append(Strike_pe_1_remove_copy)
                                Active_status_read["Deactive Put Strike"].append(Strike_pe_2_remove_copy)
                                Active_status_read["Deactive Put Strike Premium Initial"].append(Active_Initial_Sold_premium_put[0])
                                Active_status_read["Deactive Put Strike Premium Initial"].append(Active_Initial_Sold_premium_put[1])
                                Active_status_read["Deactive Put Strike SL"].append(Active_SL_Put[0])
                                Active_status_read["Deactive Put Strike SL"].append(Active_SL_Put[1])
                                Active_status_read["Deactive Call Strike"].append(Strike_ce_remove_copy)
                                Active_status_read["Deactive Call Strike Premium Initial"].append(Active_Initial_Sold_premium_call[0])
                                Active_status_read["Deactive Call Strike SL"].append(Active_SL_Call[0])

                                writing_Active_status(Active_status_read)


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

                        CE_Current_pr_close=df_CE.loc[(i+index_row+1),"close CE"]
                        PE_Current_pr_1_close=df_PE_1.loc[(i+index_row+1),"close PE"]
                        PE_Current_pr_2_close=df_PE_2.loc[(i+index_row+1),"close PE"]
                        PE_Current_pr_3_close=df_PE_3.loc[(i+index_row+1),"close PE"]

                        ce_initial_Price=Active_Initial_Sold_premium_call[0]
                        pe_initial_Price_1=Active_Initial_Sold_premium_put[0]
                        pe_initial_Price_2=Active_Initial_Sold_premium_put[1]
                        pe_initial_Price_3=Active_Initial_Sold_premium_put[2]

                        Startjee_1_dict_Call[Active_call_Strike[0]]=[CE_Current_pr_close,ce_initial_Price,CE_SL]
                        Startjee_1_dict_Put[Active_put_Strike[0]]=[PE_Current_pr_1_close,pe_initial_Price_1,PE_1_SL]
                        Startjee_1_dict_Put[Active_put_Strike[1]]=[PE_Current_pr_2_close,pe_initial_Price_2,PE_2_SL]
                        Startjee_1_dict_Put[Active_put_Strike[2]]=[PE_Current_pr_3_close,pe_initial_Price_3,PE_3_SL]

                        CE_instantinious_pr=[CE_Current_pr_close]
                        PE_instantinious_pr=[PE_Current_pr_1_close,PE_Current_pr_2_close,PE_Current_pr_3_close]

                        if CE_Current_pr<CE_SL and PE_Current_pr_1<PE_1_SL and PE_Current_pr_2<PE_2_SL and PE_Current_pr_3<PE_3_SL:
                            call_premium_collected=ce_initial_Price-df_CE_3.loc[(index_row+i+1),"close CE"]
                            put_premium_collected_1=pe_initial_Price_1-df_PE_1.loc[(index_row+i+1),"close PE"]
                            put_premium_collected_2=pe_initial_Price_2-df_PE_2.loc[(index_row+i+1),"close PE"]
                            put_premium_collected_3=pe_initial_Price_3-df_PE_3.loc[(index_row+i+1),"close PE"]
                            Net_P_L=Net_P_L+call_premium_collected+put_premium_collected_1+put_premium_collected_2+put_premium_collected_3
                            time=df_PE_1.loc[(index_row+i+1),"Time"]
                            SL_update(time,Active_Initial_Sold_premium_call,Active_Initial_Sold_premium_put,CE_instantinious_pr,PE_instantinious_pr,Active_call_Strike,Active_put_Strike,Active_SL_Call,Active_SL_Put,reversal_status,Startjee_1_dict_Call,Startjee_1_dict_Put)

                        elif CE_Current_pr>=CE_SL and PE_Current_pr_1<PE_1_SL and PE_Current_pr_2<PE_2_SL and PE_Current_pr_3<PE_3_SL:
                            CE_Strike_3=Active_call_Strike[0]
                            PE_Strike_4=Active_put_Strike[2]+50
                            PE_Strike_3=Active_put_Strike[2]
                            PE_Strike_2=Active_put_Strike[1]
                            PE_Strike_1=Active_put_Strike[0]

                            call_premium_collected=ce_initial_Price-CE_SL
                            put_premium_collected_1=pe_initial_Price_1-df_PE_1.loc[(index_row+i+1),"close PE"]
                            put_premium_collected_2=pe_initial_Price_2-df_PE_2.loc[(index_row+i+1),"close PE"]
                            put_premium_collected_3=pe_initial_Price_3-df_PE_3.loc[(index_row+i+1),"close PE"]
                            Net_P_L=Net_P_L+call_premium_collected+put_premium_collected_1+put_premium_collected_2+put_premium_collected_3

                            Time=df_CE_3.loc[(index_row+i+1),"Time"]
                            Date=df_CE_3.loc[(index_row+i+1),"Date"]

                            week=date_to_week(Date)

                            running_log_update("SL_Hit","Call_stk_3",CE_Strike_3,"Call",Time,Date,week,formatted_Date_of_Init[k],formatted_Date_of_Expiry[k],0,0)

                            index_row,df_PE_1,df_PE_2,df_PE_3,df_PE_4=volatility_strike_pred(Date,Time,path_expiry_date_recurring,Startjee_1_dict_Call,Startjee_1_dict_Put,0,0,CE_Strike_3,0,PE_Strike_1,PE_Strike_2,PE_Strike_3,PE_Strike_4,Len_pe,1)

                        elif CE_Current_pr<CE_SL and PE_Current_pr_1<PE_1_SL and PE_Current_pr_2<PE_2_SL and PE_Current_pr_3>=PE_3_SL:
                            Active_status_read=read_Active_status()
                            deleted_strike_pe=Active_status_read["Deactive Put Strike"]
                            Put_strikes_remove=Active_status_read["Active_put_Strike"]
                            Strike_pe_remove_copy=Put_strikes_remove[2]

                            if Strike_pe_remove_copy not in deleted_strike_pe:  
                                reversal_status=310100 #" the format is len,rev,CE_2,PE_2,PE_1"
                                Active_status_read["Deactive Put Strike"].append(Strike_pe_remove_copy)
                                Active_status_read["Deactive Put Strike Premium Initial"].append(Active_Initial_Sold_premium_put[2])
                                Active_status_read["Deactive Put Strike SL"].append(Active_SL_Put[2])

                                writing_Active_status(Active_status_read)



                                call_premium_collected=ce_initial_Price-df_CE_3.loc[(index_row+i+1),"close CE"]
                                put_premium_collected_1=pe_initial_Price_1-df_PE_1.loc[(index_row+i+1),"close PE"]
                                put_premium_collected_2=pe_initial_Price_2-df_PE_2.loc[(index_row+i+1),"close PE"]
                                Net_P_L=Net_P_L+call_premium_collected+put_premium_collected_1+put_premium_collected_2
                                time=df_PE_1.loc[(index_row+i+1),"Time"]
                                SL_update(time,Active_Initial_Sold_premium_call,Active_Initial_Sold_premium_put,CE_instantinious_pr,PE_instantinious_pr,Active_call_Strike,Active_put_Strike,Active_SL_Call,Active_SL_Put,reversal_status,Startjee_1_dict_Call,Startjee_1_dict_Put)
                            else:
                                call_premium_collected=ce_initial_Price-df_CE_3.loc[(index_row+i+1),"close CE"]
                                put_premium_collected_1=pe_initial_Price_1-df_PE_1.loc[(index_row+i+1),"close PE"]
                                put_premium_collected_2=pe_initial_Price_2-df_PE_2.loc[(index_row+i+1),"close PE"]
                                Net_P_L=Net_P_L+call_premium_collected+put_premium_collected_1+put_premium_collected_2
                                time=df_PE_1.loc[(index_row+i+1),"Time"]
                                SL_update(time,Active_Initial_Sold_premium_call,Active_Initial_Sold_premium_put,CE_instantinious_pr,PE_instantinious_pr,Active_call_Strike,Active_put_Strike,Active_SL_Call,Active_SL_Put,reversal_status,Startjee_1_dict_Call,Startjee_1_dict_Put)

                        elif CE_Current_pr>=CE_SL and PE_Current_pr_1<PE_1_SL and PE_Current_pr_2<PE_2_SL and PE_Current_pr_3>=PE_3_SL:

                            Active_status_read=read_Active_status()
                            deleted_strike_pe=Active_status_read["Deactive Put Strike"]
                            deleted_strike_ce=Active_status_read["Deactive Call Strike"]

                            Put_strikes_remove=Active_status_read["Active_put_Strike"]
                            Call_Strikes_remove=Active_status_read["Active_call_Strike"]

                            Strike_pe_remove_copy=Put_strikes_remove[2]
                            Strike_ce_remove_copy=Call_strikes_remove[0]

                            if Strike_pe_remove_copy not in deleted_strike_pe or Strike_ce_remove_copy not in deleted_strike_ce:  
                                reversal_status=311100 #" the format is len,rev,CE_2,PE_2,PE_1"
                                Active_status_read["Deactive Put Strike"].append(Strike_pe_remove_copy)
                                Active_status_read["Deactive Call Strike"].append(Strike_ce_remove_copy)
                                Active_status_read["Deactive Put Strike Premium Initial"].append(Active_Initial_Sold_premium_put[2])
                                Active_status_read["Deactive Put Strike SL"].append(Active_SL_Put[2])
                                Active_status_read["Deactive Call Strike Premium Initial"].append(Active_Initial_Sold_premium_call[0])
                                Active_status_read["Deactive Call Strike SL"].append(Active_SL_Call[0])

                                writing_Active_status(Active_status_read)



                                put_premium_collected_1=pe_initial_Price_1-df_PE_1.loc[(index_row+i+1),"close PE"]
                                put_premium_collected_2=pe_initial_Price_2-df_PE_2.loc[(index_row+i+1),"close PE"]
                                Net_P_L=Net_P_L+call_premium_collected+put_premium_collected_1+put_premium_collected_2
                                time=df_PE_1.loc[(index_row+i+1),"Time"]
                                SL_update(time,Active_Initial_Sold_premium_call,Active_Initial_Sold_premium_put,CE_instantinious_pr,PE_instantinious_pr,Active_call_Strike,Active_put_Strike,Active_SL_Call,Active_SL_Put,reversal_status,Startjee_1_dict_Call,Startjee_1_dict_Put)
                            else:
                                put_premium_collected_1=pe_initial_Price_1-df_PE_1.loc[(index_row+i+1),"close PE"]
                                put_premium_collected_2=pe_initial_Price_2-df_PE_2.loc[(index_row+i+1),"close PE"]
                                Net_P_L=Net_P_L+call_premium_collected+put_premium_collected_1+put_premium_collected_2
                                time=df_PE_1.loc[(index_row+i+1),"Time"]
                                SL_update(time,Active_Initial_Sold_premium_call,Active_Initial_Sold_premium_put,CE_instantinious_pr,PE_instantinious_pr,Active_call_Strike,Active_put_Strike,Active_SL_Call,Active_SL_Put,reversal_status,Startjee_1_dict_Call,Startjee_1_dict_Put)

                        elif CE_Current_pr<CE_SL and PE_Current_pr_1<PE_1_SL and PE_Current_pr_2>=PE_2_SL and PE_Current_pr_3>=PE_3_SL:
                            Active_status_read=read_Active_status()
                            deleted_strike_pe=Active_status_read["Deactive Put Strike"]
                            Put_strikes_remove=Active_status_read["Active_put_Strike"]
        

                            Strike_pe_2_remove_copy=Put_strikes_remove[1]
                            Strike_pe_3_remove_copy=Put_strikes_remove[2]

                            if Strike_pe_2_remove_copy not in deleted_strike_pe or Strike_pe_3_remove_copy not in deleted_strike_pe:  
                                reversal_status=310110 #" the format is len,rev,CE_2,PE_2,PE_1"
                                Active_status_read["Deactive Put Strike"].append(Strike_pe_2_remove_copy)
                                Active_status_read["Deactive Put Strike"].append(Strike_pe_3_remove_copy)
                                Active_status_read["Deactive Put Strike Premium Initial"].append(Active_Initial_Sold_premium_put[2])
                                Active_status_read["Deactive Put Strike Premium Initial"].append(Active_Initial_Sold_premium_put[3])
                                Active_status_read["Deactive Put Strike SL"].append(Active_SL_Put[2])
                                Active_status_read["Deactive Put Strike SL"].append(Active_SL_Put[3])

                                writing_Active_status(Active_status_read)



                                call_premium_collected=ce_initial_Price-df_CE_3.loc[(index_row+i+1),"close CE"]
                                put_premium_collected_1=pe_initial_Price_1-df_PE_1.loc[(index_row+i+1),"close PE"]
                                Net_P_L=Net_P_L+call_premium_collected+put_premium_collected_1
                                time=df_PE_1.loc[(index_row+i+1),"Time"]
                                SL_update(time,Active_Initial_Sold_premium_call,Active_Initial_Sold_premium_put,CE_instantinious_pr,PE_instantinious_pr,Active_call_Strike,Active_put_Strike,Active_SL_Call,Active_SL_Put,reversal_status,Startjee_1_dict_Call,Startjee_1_dict_Put)
                            else:
                                call_premium_collected=ce_initial_Price-df_CE_3.loc[(index_row+i+1),"close CE"]
                                put_premium_collected_1=pe_initial_Price_1-df_PE_1.loc[(index_row+i+1),"close PE"]
                                Net_P_L=Net_P_L+call_premium_collected+put_premium_collected_1
                                time=df_PE_1.loc[(index_row+i+1),"Time"]
                                SL_update(time,Active_Initial_Sold_premium_call,Active_Initial_Sold_premium_put,CE_instantinious_pr,PE_instantinious_pr,Active_call_Strike,Active_put_Strike,Active_SL_Call,Active_SL_Put,reversal_status,Startjee_1_dict_Call,Startjee_1_dict_Put)

                        elif CE_Current_pr>=CE_SL and PE_Current_pr_1<PE_1_SL and PE_Current_pr_2>=PE_2_SL and PE_Current_pr_3>=PE_3_SL:
                            Active_status_read=read_Active_status()
                            deleted_strike_pe=Active_status_read["Deactive Put Strike"]
                            deleted_strike_ce=Active_status_read["Deactive Call Strike"]

                            Put_strikes_remove=Active_status_read["Active_put_Strike"]
                            Call_Strikes_remove=Active_status_read["Active_call_Strike"]

                            Strike_pe_2_remove_copy=Put_strikes_remove[1]
                            Strike_pe_3_remove_copy=Put_strikes_remove[2]
                            Strike_ce_1_remove_copy=Call_Strikes_remove[0]


                            if Strike_pe_3_remove_copy not in deleted_strike_pe or Strike_pe_2_remove_copy not in deleted_strike_pe or Strike_ce_1_remove_copy not in deleted_strike_ce:  
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



                                put_premium_collected_1=pe_initial_Price_1-df_PE_1.loc[(index_row+i+1),"close PE"]
                                Net_P_L=Net_P_L+put_premium_collected_1
                                time=df_PE_1.loc[(index_row+i+1),"Time"]
                                SL_update(time,Active_Initial_Sold_premium_call,Active_Initial_Sold_premium_put,CE_instantinious_pr,PE_instantinious_pr,Active_call_Strike,Active_put_Strike,Active_SL_Call,Active_SL_Put,reversal_status,Startjee_1_dict_Call,Startjee_1_dict_Put)
                            else:
                                put_premium_collected_1=pe_initial_Price_1-df_PE_1.loc[(index_row+i+1),"close PE"]
                                Net_P_L=Net_P_L+put_premium_collected_1
                                time=df_PE_1.loc[(index_row+i+1),"Time"]
                                SL_update(time,Active_Initial_Sold_premium_call,Active_Initial_Sold_premium_put,CE_instantinious_pr,PE_instantinious_pr,Active_call_Strike,Active_put_Strike,Active_SL_Call,Active_SL_Put,reversal_status,Startjee_1_dict_Call,Startjee_1_dict_Put)
                        elif CE_Current_pr<CE_SL and PE_Current_pr_1>=PE_1_SL and PE_Current_pr_2>=PE_2_SL and PE_Current_pr_3>=PE_3_SL:
                            Active_status_read=read_Active_status()
                            deleted_strike_pe=Active_status_read["Deactive Put Strike"]

                            Put_strikes_remove=Active_status_read["Active_put_Strike"]

                            Strike_pe_1_remove_copy=Put_strikes_remove[0]
                            Strike_pe_2_remove_copy=Put_strikes_remove[1]
                            Strike_pe_3_remove_copy=Put_strikes_remove[2]

                            if Strike_pe_1_remove_copy not in deleted_strike_pe or Strike_pe_2_remove_copy not in deleted_strike_pe or Strike_pe_3_remove_copy not in deleted_strike_pe:  
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

                                writing_Active_status(Active_status_read)

                                call_premium_collected=ce_initial_Price-df_CE_3.loc[(index_row+i+1),"close CE"]
                                Net_P_L=Net_P_L+call_premium_collected
                                time=df_CE_3.loc[(index_row+i+1),"Time"]
                                SL_update(time,Active_Initial_Sold_premium_call,Active_Initial_Sold_premium_put,CE_instantinious_pr,PE_instantinious_pr,Active_call_Strike,Active_put_Strike,Active_SL_Call,Active_SL_Put,reversal_status,Startjee_1_dict_Call,Startjee_1_dict_Put)
                            else:
                                call_premium_collected=ce_initial_Price-df_CE_3.loc[(index_row+i+1),"close CE"]
                                Net_P_L=Net_P_L+call_premium_collected
                                time=df_CE_3.loc[(index_row+i+1),"Time"]
                                SL_update(time,Active_Initial_Sold_premium_call,Active_Initial_Sold_premium_put,CE_instantinious_pr,PE_instantinious_pr,Active_call_Strike,Active_put_Strike,Active_SL_Call,Active_SL_Put,reversal_status,Startjee_1_dict_Call,Startjee_1_dict_Put)

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
                            if Strike_pe_1_remove_copy not in deleted_strike_pe or Strike_pe_2_remove_copy not in deleted_strike_pe or Strike_pe_3_remove_copy not in deleted_strike_pe or Strike_ce_remove_copy not in deleted_strike_ce: 
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

                        
                        PE_Current_pr_1_close=df_PE_1.loc[(i+index_row+1),"close PE"]
                        PE_Current_pr_2_close=df_PE_2.loc[(i+index_row+1),"close PE"]
                        PE_Current_pr_3_close=df_PE_3.loc[(i+index_row+1),"close PE"]
                        PE_Current_pr_4_close=df_PE_4.loc[(i+index_row+1),"close PE"]

                        pe_initial_Price_1=Active_Initial_Sold_premium_put[0]
                        pe_initial_Price_2=Active_Initial_Sold_premium_put[1]
                        pe_initial_Price_3=Active_Initial_Sold_premium_put[2]
                        pe_initial_Price_4=Active_Initial_Sold_premium_put[3]

                        CE_instantinious_pr=[]
                        PE_instantinious_pr=[PE_Current_pr_1_close,PE_Current_pr_2_close,PE_Current_pr_3_close,PE_Current_pr_4_close]

                        
                        Startjee_1_dict_Put[Active_put_Strike[0]]=[PE_Current_pr_1_close,pe_initial_Price_1,PE_1_SL]
                        Startjee_1_dict_Put[Active_put_Strike[1]]=[PE_Current_pr_2_close,pe_initial_Price_2,PE_2_SL]
                        Startjee_1_dict_Put[Active_put_Strike[2]]=[PE_Current_pr_3_close,pe_initial_Price_3,PE_3_SL]
                        Startjee_1_dict_Put[Active_put_Strike[3]]=[PE_Current_pr_4_close,pe_initial_Price_4,PE_4_SL]

                        if PE_Current_pr_1<PE_1_SL and PE_Current_pr_2<PE_2_SL and PE_Current_pr_3<PE_3_SL and PE_Current_pr_4<PE_4_SL:
                            put_premium_collected_1=pe_initial_Price_1-df_PE_1.loc[(index_row+i+1),"close PE"]
                            put_premium_collected_2=pe_initial_Price_2-df_PE_2.loc[(index_row+i+1),"close PE"]
                            put_premium_collected_3=pe_initial_Price_3-df_PE_3.loc[(index_row+i+1),"close PE"]
                            put_premium_collected_4=pe_initial_Price_4-df_PE_4.loc[(index_row+i+1),"close PE"]
                            Net_P_L=Net_P_L+put_premium_collected_1+put_premium_collected_2+put_premium_collected_3+put_premium_collected_4
                            time=df_PE_1.loc[(index_row+i+1),"Time"]
                            SL_update(time,Active_Initial_Sold_premium_call,Active_Initial_Sold_premium_put,CE_instantinious_pr,PE_instantinious_pr,Active_call_Strike,Active_put_Strike,Active_SL_Call,Active_SL_Put,reversal_status,Startjee_1_dict_Call,Startjee_1_dict_Put)

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


                                put_premium_collected_1=pe_initial_Price_1-df_PE_1.loc[(index_row+i+1),"close PE"]
                                put_premium_collected_2=pe_initial_Price_2-df_PE_2.loc[(index_row+i+1),"close PE"]
                                put_premium_collected_3=pe_initial_Price_3-df_PE_3.loc[(index_row+i+1),"close PE"]
                                Net_P_L=Net_P_L+put_premium_collected_1+put_premium_collected_2+put_premium_collected_3
                                time=df_PE_1.loc[(index_row+i+1),"Time"]
                                SL_update(time,Active_Initial_Sold_premium_call,Active_Initial_Sold_premium_put,CE_instantinious_pr,PE_instantinious_pr,Active_call_Strike,Active_put_Strike,Active_SL_Call,Active_SL_Put,reversal_status,Startjee_1_dict_Call,Startjee_1_dict_Put)
                            else:
                                put_premium_collected_1=pe_initial_Price_1-df_PE_1.loc[(index_row+i+1),"close PE"]
                                put_premium_collected_2=pe_initial_Price_2-df_PE_2.loc[(index_row+i+1),"close PE"]
                                put_premium_collected_3=pe_initial_Price_3-df_PE_3.loc[(index_row+i+1),"close PE"]
                                Net_P_L=Net_P_L+put_premium_collected_1+put_premium_collected_2+put_premium_collected_3
                                time=df_PE_1.loc[(index_row+i+1),"Time"]
                                SL_update(time,Active_Initial_Sold_premium_call,Active_Initial_Sold_premium_put,CE_instantinious_pr,PE_instantinious_pr,Active_call_Strike,Active_put_Strike,Active_SL_Call,Active_SL_Put,reversal_status,Startjee_1_dict_Call,Startjee_1_dict_Put)

                        elif PE_Current_pr_1<PE_1_SL and PE_Current_pr_2<PE_2_SL and PE_Current_pr_3>=PE_3_SL and PE_Current_pr_4>=PE_4_SL:
                                                        
                            Active_status_read=read_Active_status()
                            deleted_strike_pe=Active_status_read["Deactive Put Strike"]
                            Put_strikes_remove=Active_status_read["Active_put_Strike"]

                            Strike_pe_3_remove_copy=Put_strikes_remove[2]
                            Strike_pe_4_remove_copy=Put_strikes_remove[3]


                            if Strike_pe_4_remove_copy not in deleted_strike_pe or Strike_pe_3_remove_copy not in deleted_strike_pe:  
                                reversal_status=411100 #" the format is len,rev,CE_2,PE_2,PE_1"
                                Active_status_read["Deactive Put Strike"].append(Strike_pe_4_remove_copy)
                                Active_status_read["Deactive Put Strike Premium Initial"].append(Active_Initial_Sold_premium_put[3])
                                Active_status_read["Deactive Put Strike SL"].append(Active_SL_Put[3])
                                Active_status_read["Deactive Put Strike"].append(Strike_pe_3_remove_copy)
                                Active_status_read["Deactive Put Strike Premium Initial"].append(Active_Initial_Sold_premium_put[2])
                                Active_status_read["Deactive Put Strike SL"].append(Active_SL_Put[2])

                                writing_Active_status(Active_status_read)


                                put_premium_collected_1=pe_initial_Price_1-df_PE_1.loc[(index_row+i+1),"close PE"]
                                put_premium_collected_2=pe_initial_Price_2-df_PE_2.loc[(index_row+i+1),"close PE"]
                                Net_P_L=Net_P_L+put_premium_collected_1+put_premium_collected_2
                                time=df_PE_1.loc[(index_row+i+1),"Time"]
                                SL_update(time,Active_Initial_Sold_premium_call,Active_Initial_Sold_premium_put,CE_instantinious_pr,PE_instantinious_pr,Active_call_Strike,Active_put_Strike,Active_SL_Call,Active_SL_Put,reversal_status,Startjee_1_dict_Call,Startjee_1_dict_Put)
                            else:
                                put_premium_collected_1=pe_initial_Price_1-df_PE_1.loc[(index_row+i+1),"close PE"]
                                put_premium_collected_2=pe_initial_Price_2-df_PE_2.loc[(index_row+i+1),"close PE"]
                                Net_P_L=Net_P_L+put_premium_collected_1+put_premium_collected_2
                                time=df_PE_1.loc[(index_row+i+1),"Time"]
                                SL_update(time,Active_Initial_Sold_premium_call,Active_Initial_Sold_premium_put,CE_instantinious_pr,PE_instantinious_pr,Active_call_Strike,Active_put_Strike,Active_SL_Call,Active_SL_Put,reversal_status,Startjee_1_dict_Call,Startjee_1_dict_Put)

                        elif PE_Current_pr_1<PE_1_SL and PE_Current_pr_2>=PE_2_SL and PE_Current_pr_3>=PE_3_SL and PE_Current_pr_4>=PE_4_SL:

                            Active_status_read=read_Active_status()
                            deleted_strike_pe=Active_status_read["Deactive Put Strike"]
                            Put_strikes_remove=Active_status_read["Active_put_Strike"]

                            Strike_pe_2_remove_copy=Put_strikes_remove[1]
                            Strike_pe_3_remove_copy=Put_strikes_remove[2]
                            Strike_pe_4_remove_copy=Put_strikes_remove[3]

                            if Strike_pe_4_remove_copy not in deleted_strike_pe or Strike_pe_3_remove_copy not in deleted_strike_pe or Strike_pe_2_remove_copy not in deleted_strike_pe:  
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


                                put_premium_collected_1=pe_initial_Price_1-df_PE_1.loc[(index_row+i+1),"close PE"]
                                Net_P_L=Net_P_L+put_premium_collected_1
                                time=df_PE_1.loc[(index_row+i+1),"Time"]
                                SL_update(time,Active_Initial_Sold_premium_call,Active_Initial_Sold_premium_put,CE_instantinious_pr,PE_instantinious_pr,Active_call_Strike,Active_put_Strike,Active_SL_Call,Active_SL_Put,reversal_status,Startjee_1_dict_Call,Startjee_1_dict_Put)
                            else:
                                put_premium_collected_1=pe_initial_Price_1-df_PE_1.loc[(index_row+i+1),"close PE"]
                                Net_P_L=Net_P_L+put_premium_collected_1
                                time=df_PE_1.loc[(index_row+i+1),"Time"]
                                SL_update(time,Active_Initial_Sold_premium_call,Active_Initial_Sold_premium_put,CE_instantinious_pr,PE_instantinious_pr,Active_call_Strike,Active_put_Strike,Active_SL_Call,Active_SL_Put,reversal_status,Startjee_1_dict_Call,Startjee_1_dict_Put)

                        elif PE_Current_pr_1>=PE_1_SL and PE_Current_pr_2>=PE_2_SL and PE_Current_pr_3>=PE_3_SL and PE_Current_pr_4>=PE_4_SL:
                            Active_status_read=read_Active_status()
                            deleted_strike_pe=Active_status_read["Deactive Put Strike"]
                            Put_strikes_remove=Active_status_read["Active_put_Strike"]

                            Strike_pe_1_remove_copy=Put_strikes_remove[0]
                            Strike_pe_2_remove_copy=Put_strikes_remove[1]
                            Strike_pe_3_remove_copy=Put_strikes_remove[2]
                            Strike_pe_4_remove_copy=Put_strikes_remove[3]


                            if Strike_pe_4_remove_copy not in deleted_strike_pe or Strike_pe_3_remove_copy not in deleted_strike_pe or Strike_pe_2_remove_copy not in deleted_strike_pe or Strike_pe_1_remove_copy not in deleted_strike_pe:  
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

                                break

                            else:
                                pass

                        else:
                            pass
                    else:
                        pass



                elif Market_trend=="Trending Down":
                    Len_ce=len(Active_call_Strike)
                    Len_pe=len(Active_put_Strike)

                    if Len_ce==2:
                        CE_1_SL=Active_SL_Call[0]
                        CE_2_SL=Active_SL_Call[1]
                        PE_2_SL=Active_SL_Put[0]

                        CE_Current_pr_1=df_CE_1.loc[(i+index_row+1),"high CE"]
                        CE_Current_pr_2=df_CE_2.loc[(i+index_row+1),"high CE"]
                        PE_Current_pr_2=df_PE_2.loc[(i+index_row+1),"high PE"]

                        CE_Current_pr_1_close=df_CE_1.loc[(i+index_row+1),"close CE"]
                        CE_Current_pr_2_close=df_CE_2.loc[(i+index_row+1),"close CE"]
                        PE_Current_pr_2_close=df_PE_2.loc[(i+index_row+1),"close PE"]

                        CE_instantinious_pr=[CE_Current_pr_1_close,CE_Current_pr_2_close]
                        PE_instantinious_pr=[PE_Current_pr_2_close]

                        ce_initial_Price_1=Active_Initial_Sold_premium_call[0]
                        ce_initial_Price_2=Active_Initial_Sold_premium_call[1]
                        pe_initial_Price_2=Active_Initial_Sold_premium_put[0]

                        Startjee_1_dict_Call[Active_call_Strike[0]]=[CE_Current_pr_1_close,ce_initial_Price_1,CE_1_SL]
                        Startjee_1_dict_Call[Active_call_Strike[1]]=[CE_Current_pr_2_close,ce_initial_Price_2,CE_2_SL]
                        Startjee_1_dict_Put[Active_put_Strike[1]]=[PE_Current_pr_2_close,pe_initial_Price_2,PE_2_SL]

                        if CE_Current_pr_1<CE_1_SL and CE_Current_pr_2<CE_2_SL and PE_Current_pr_2<PE_2_SL:
                            call_premium_collected_1=ce_initial_Price_1-df_CE_1.loc[(index_row+i+1),"close CE"]
                            call_premium_collected_2=ce_initial_Price_2-df_CE_2.loc[(index_row+i+1),"close CE"]
                            put_premium_collected_2=pe_initial_Price_2-df_PE_2.loc[(index_row+i+1),"close PE"]
                            Net_P_L=Net_P_L+call_premium_collected_1+call_premium_collected_2+put_premium_collected_2
                            
                            time=df_CE_1.loc[(index_row+i+1),"Time"]
                            Date=df_CE_1.loc[(running_index+i+1),"Date"]
                            SL_update(time,Active_Initial_Sold_premium_call,Active_Initial_Sold_premium_put,CE_instantinious_pr,PE_instantinious_pr,Active_call_Strike,Active_put_Strike,Active_SL_Call,Active_SL_Put,reversal_status,Startjee_1_dict_Call,Startjee_1_dict_Put)
                        
                        elif CE_Current_pr_1<CE_1_SL and CE_Current_pr_2<CE_2_SL and PE_Current_pr_1>=PE_2_SL:
                            CE_Strike_1=Active_call_Strike[0]
                            CE_Strike_2=Active_call_Strike[1]
                            CE_Strike_3=Active_call_Strike[1]-50
                            PE_strike_2=Active_put_Strike[0]

                            call_premium_collected_1=ce_initial_Price_1-df_CE_1.loc[(index_row+i+1),"close CE"]
                            call_premium_collected_2=ce_initial_Price_2-df_CE_2.loc[(index_row+i+1),"close CE"]
                            put_premium_collected_2=pe_initial_Price_2-PE_2_SL
                            Net_P_L=Net_P_L+call_premium_collected_1+call_premium_collected_2+put_premium_collected_2                            

                            Time=df_CE_1.loc[(index_row+i+1),"Time"]
                            Date=df_CE_1.loc[(index_row+i+1),"Date"]

                            week=date_to_week(Date)

                            running_log_update("SL_Hit","Put_stk_2",PE_strike_2,"Put",Time,Date,week,formatted_Date_of_Init[k],formatted_Date_of_Expiry[k],0,0)

                            index_row,df_CE_3,df_CE_2,df_CE_1,df_PE_3=volatility_strike_pred(Date,Time,path_expiry_date_recurring,Startjee_1_dict_Call,Startjee_1_dict_Put,CE_Strike_1,CE_Strike_2,CE_Strike_3,0,0,PE_strike_2,0,0,1,Len_ce)

######### REVESAL SEQUENCE ######

                        elif CE_Current_pr_1<CE_1_SL and CE_Current_pr_2>=CE_2_SL and PE_Current_pr_2<PE_2_SL:
                            Active_status_read=read_Active_status()
                            deleted_strike=Active_status_read["Deactive Call Strike"]
                            Call_strikes_remove=Active_status_read["Active_call_Strike"]
                            Strike_ce_remove_copy=Call_strikes_remove[1]


                            if Strike_ce_remove_copy not in deleted_strike:  
                                reversal_status=21010 #" the format is len,rev,CE_2,PE_2,PE_1"
                                Active_status_read["Deactive Call Strike"].append(Strike_ce_remove_copy)
                                Active_status_read["Deactive Call Strike Premium Initial"].append(Active_Initial_Sold_premium_call[1])
                                Active_status_read["Deactive Call Strike SL"].append(Active_SL_Call[1])

                                writing_Active_status(Active_status_read)

                                call_premium_collected_1=ce_initial_Price_1-df_CE_1.loc[(index_row+i+1),"close CE"]
                                put_premium_collected_2=pe_initial_Price_2-df_PE_2.loc[(index_row+i+1),"close PE"]
                                Net_P_L=Net_P_L+call_premium_collected_1+put_premium_collected_2
                                time=df_CE_1.loc[(index_row+i+1),"Time"]
                                SL_update(time,Active_Initial_Sold_premium_call,Active_Initial_Sold_premium_put,CE_instantinious_pr,PE_instantinious_pr,Active_call_Strike,Active_put_Strike,Active_SL_Call,Active_SL_Put,reversal_status,Startjee_1_dict_Call,Startjee_1_dict_Put)
                            else:
                                call_premium_collected_1=ce_initial_Price_1-df_CE_1.loc[(index_row+i+1),"close CE"]
                                put_premium_collected_2=pe_initial_Price_2-df_PE_2.loc[(index_row+i+1),"close PE"]
                                Net_P_L=Net_P_L+call_premium_collected_1+put_premium_collected_2
                                time=df_CE_1.loc[(index_row+i+1),"Time"]
                                SL_update(time,Active_Initial_Sold_premium_call,Active_Initial_Sold_premium_put,CE_instantinious_pr,PE_instantinious_pr,Active_call_Strike,Active_put_Strike,Active_SL_Call,Active_SL_Put,reversal_status,Startjee_1_dict_Call,Startjee_1_dict_Put)
                       
                        elif CE_Current_pr_1<CE_1_SL and CE_Current_pr_2>=CE_2_SL and PE_Current_pr_2>=PE_2_SL:
                            Active_status_read=read_Active_status()
                            deleted_strike_pe=Active_status_read["Deactive Put Strike"]
                            deleted_strike_ce=Active_status_read["Deactive Call Strike"]

                            Put_strikes_remove=Active_status_read["Active_put_Strike"]
                            Call_Strikes_remove=Active_status_read["Active_call_Strike"]

                            Strike_ce_remove_copy=Call_Strikes_remove[1]
                            Strike_pe_remove_copy=Put_strikes_remove[0]

                            if Strike_pe_remove_copy not in deleted_strike_pe or Strike_ce_remove_copy not in deleted_strike_ce:  
                                reversal_status=21110 #" the format is len,rev,CE_2,PE_2,PE_1"

                                Active_status_read["Deactive Put Strike"].append(Strike_pe_remove_copy)
                                Active_status_read["Deactive Call Strike"].append(Strike_ce_remove_copy)
                                Active_status_read["Deactive Put Strike Premium Initial"].append(Active_Initial_Sold_premium_put[0])
                                Active_status_read["Deactive Put Strike SL"].append(Active_SL_Put[0])
                                Active_status_read["Deactive Call Strike Premium Initial"].append(Active_Initial_Sold_premium_call[1])
                                Active_status_read["Deactive Call Strike SL"].append(Active_SL_Call[1])
                                writing_Active_status(Active_status_read)



                                call_premium_collected_1=ce_initial_Price_1-df_CE_1.loc[(index_row+i+1),"close CE"]
                                Net_P_L=Net_P_L+call_premium_collected_1
                                time=df_CE_1.loc[(index_row+i+1),"Time"]
                                SL_update(time,Active_Initial_Sold_premium_call,Active_Initial_Sold_premium_put,CE_instantinious_pr,PE_instantinious_pr,Active_call_Strike,Active_put_Strike,Active_SL_Call,Active_SL_Put,reversal_status,Startjee_1_dict_Call,Startjee_1_dict_Put)
                            else:
                                call_premium_collected_1=ce_initial_Price_1-df_CE_1.loc[(index_row+i+1),"close CE"]
                                Net_P_L=Net_P_L+call_premium_collected_1
                                time=df_CE_1.loc[(index_row+i+1),"Time"]
                                SL_update(time,Active_Initial_Sold_premium_call,Active_Initial_Sold_premium_put,CE_instantinious_pr,PE_instantinious_pr,Active_call_Strike,Active_put_Strike,Active_SL_Call,Active_SL_Put,reversal_status,Startjee_1_dict_Call,Startjee_1_dict_Put)

                        elif CE_Current_pr_1>=CE_1_SL and CE_Current_pr_2>=CE_2_SL and PE_Current_pr_2<PE_2_SL:
                            Active_status_read=read_Active_status()
                            deleted_strike_ce=Active_status_read["Deactive Call Strike"]
                            Call_strikes_remove=Active_status_read["Active_call_Strike"]

                            Strike_ce_1_remove_copy=Call_strikes_remove[0]
                            Strike_ce_2_remove_copy=Call_strikes_remove[1]

                            if Strike_ce_1_remove_copy not in deleted_strike or Strike_ce_2_remove_copy not in deleted_strike:  
                                reversal_status=21011 #" the format is len,rev,CE_2,PE_2,PE_1"
                                Active_status_read["Deactive Call Strike"].append(Strike_ce_1_remove_copy)
                                Active_status_read["Deactive Call Strike"].append(Strike_ce_2_remove_copy)
                                Active_status_read["Deactive Call Strike Premium Initial"].append(Active_Initial_Sold_premium_call[0])
                                Active_status_read["Deactive Call Strike Premium Initial"].append(Active_Initial_Sold_premium_call[1])
                                Active_status_read["Deactive Call Strike SL"].append(Active_SL_Call[0])
                                Active_status_read["Deactive Call Strike SL"].append(Active_SL_Call[1])

                                writing_Active_status(Active_status_read)

                                put_premium_collected_2=pe_initial_Price_2-df_PE_2.loc[(index_row+i+1),"close CE"]
                                Net_P_L=Net_P_L+put_premium_collected_2
                                time=df_PE_2.loc[(index_row+i+1),"Time"]
                                SL_update(time,Active_Initial_Sold_premium_call,Active_Initial_Sold_premium_put,CE_instantinious_pr,PE_instantinious_pr,Active_call_Strike,Active_put_Strike,Active_SL_Call,Active_SL_Put,reversal_status,Startjee_1_dict_Call,Startjee_1_dict_Put)
                            else:
                                put_premium_collected_2=pe_initial_Price_2-df_PE_2.loc[(index_row+i+1),"close CE"]
                                Net_P_L=Net_P_L+put_premium_collected_2
                                time=df_PE_2.loc[(index_row+i+1),"Time"]
                                SL_update(time,Active_Initial_Sold_premium_call,Active_Initial_Sold_premium_put,CE_instantinious_pr,PE_instantinious_pr,Active_call_Strike,Active_put_Strike,Active_SL_Call,Active_SL_Put,reversal_status,Startjee_1_dict_Call,Startjee_1_dict_Put)

                        elif CE_Current_pr_1>=CE_1_SL and CE_Current_pr_2>=CE_2_SL and PE_Current_pr_2>=PE_2_SL:
                            ## read the text file and get the strike to remove from that file and get the deleted strikes list
                            Active_status_read=read_Active_status()
                            deleted_strike_pe=Active_status_read["Deactive Put Strike"]
                            deleted_strike_ce=Active_status_read["Deactive Call Strike"]

                            Put_strikes_remove=Active_status_read["Active_put_Strike"]
                            Call_Strikes_remove=Active_status_read["Active_call_Strike"]

                            Strike_ce_1_remove_copy=Call_strikes_remove[0]
                            Strike_ce_2_remove_copy=Call_strikes_remove[1]
                            Strike_pe_1_remove_copy=Put_strikes_remove[0]

                            ## Read the list from the text file  ########
                            # deleted_strike=data
                            if Strike_pe_1_remove_copy not in deleted_strike_pe or Strike_pe_2_remove_copy not in deleted_strike_pe or Strike_ce_1_remove_copy not in deleted_strike_ce:  
                                reversal_status=21111 #" the format is len,rev,CE_2,PE_2,PE_1"
                                Active_status_read["Deactive Call Strike"].append(Strike_ce_1_remove_copy)
                                Active_status_read["Deactive Call Strike"].append(Strike_ce_2_remove_copy)
                                Active_status_read["Deactive Call Strike Premium Initial"].append(Active_Initial_Sold_premium_call[0])
                                Active_status_read["Deactive Call Strike Premium Initial"].append(Active_Initial_Sold_premium_call[1])
                                Active_status_read["Deactive Call Strike SL"].append(Active_SL_Call[0])
                                Active_status_read["Deactive Call Strike SL"].append(Active_SL_Call[1])
                                Active_status_read["Deactive Put Strike"].append(Strike_pe_remove_copy)
                                Active_status_read["Deactive Put Strike Premium Initial"].append(Active_Initial_Sold_premium_put[0])
                                Active_status_read["Deactive Put Strike SL"].append(Active_SL_Put[0])

                                writing_Active_status(Active_status_read)

                                break
                        else:
                            pass
                    
                    elif Len_ce==3:

                        CE_1_SL=Active_SL_Call[0]
                        CE_2_SL=Active_SL_Call[1]
                        CE_3_SL=Active_SL_Call[2]
                        PE_3_SL=Active_SL_Put[0]

                        CE_Current_pr_1=df_CE_1.loc[(i+index_row+1),"high CE"]
                        CE_Current_pr_2=df_CE_2.loc[(i+index_row+1),"high CE"]
                        CE_Current_pr_3=df_CE_3.loc[(i+index_row+1),"high CE"]
                        PE_Current_pr_3=df_PE_3.loc[(i+index_row+1),"high PE"]

                        CE_Current_pr_1_close=df_CE_1.loc[(i+index_row+1),"close CE"]
                        CE_Current_pr_2_close=df_CE_2.loc[(i+index_row+1),"close CE"]
                        CE_Current_pr_3_close=df_CE_3.loc[(i+index_row+1),"close CE"]
                        PE_Current_pr_3_close=df_PE_3.loc[(i+index_row+1),"close PE"]

                        ce_initial_Price_1=Active_Initial_Sold_premium_call[0]
                        ce_initial_Price_2=Active_Initial_Sold_premium_call[1]
                        ce_initial_Price_3=Active_Initial_Sold_premium_call[2]
                        pe_initial_Price_3=Active_Initial_Sold_premium_put[0]

                        Startjee_1_dict_Call[Active_call_Strike[0]]=[CE_Current_pr_1_close,ce_initial_Price_1,CE_1_SL]
                        Startjee_1_dict_Call[Active_call_Strike[1]]=[CE_Current_pr_2_close,ce_initial_Price_2,CE_2_SL]
                        Startjee_1_dict_Call[Active_call_Strike[2]]=[CE_Current_pr_3_close,ce_initial_Price_3,CE_3_SL]
                        Startjee_1_dict_Put[Active_call_Strike[0]]=[PE_Current_pr_3_close,pe_initial_Price_3,PE_3_SL]

                        CE_instantinious_pr=[CE_Current_pr_1_close,CE_Current_pr_2_close,CE_Current_pr_3_close]
                        PE_instantinious_pr=[PE_Current_pr_3_close]

                        if CE_Current_pr_1<CE_1_SL and CE_Current_pr_2<CE_2_SL and CE_Current_pr_3<CE_3_SL and PE_Current_pr_3<PE_3_SL: 
                            call_premium_collected_1=ce_initial_Price_1-df_CE_1.loc[(index_row+i+1),"close CE"]
                            call_premium_collected_2=ce_initial_Price_2-df_CE_2.loc[(index_row+i+1),"close CE"]
                            call_premium_collected_3=ce_initial_Price_3-df_CE_3.loc[(index_row+i+1),"close CE"]
                            put_premium_collected_3=pe_initial_Price_3-df_PE_3.loc[(index_row+i+1),"close PE"]
                            Net_P_L=Net_P_L+call_premium_collected_1+call_premium_collected_2+call_premium_collected_3+put_premium_collected_3
                            time=df_PE_3.loc[(index_row+i+1),"Time"]
                            SL_update(time,Active_Initial_Sold_premium_call,Active_Initial_Sold_premium_put,CE_instantinious_pr,PE_instantinious_pr,Active_call_Strike,Active_put_Strike,Active_SL_Call,Active_SL_Put,reversal_status,Startjee_1_dict_Call,Startjee_1_dict_Put)

                        elif CE_Current_pr_1<CE_1_SL and CE_Current_pr_2<CE_2_SL and CE_Current_pr_3<CE_3_SL and PE_Current_pr_3>=PE_3_SL: 
                            
                            
                            CE_Strike_3=Active_call_Strike[2]
                            CE_Strike_2=Active_call_Strike[1]
                            CE_Strike_1=Active_call_Strike[0]
                            PE_strike_3=Active_put_Strike[0]
                            CE_Strike_4=CE_Strike_3-50

                            call_premium_collected_1=ce_initial_Price_1-df_CE_1.loc[(index_row+i+1),"close CE"]
                            call_premium_collected_2=ce_initial_Price_2-df_CE_2.loc[(index_row+i+1),"close CE"]
                            call_premium_collected_3=ce_initial_Price_3-df_CE_3.loc[(index_row+i+1),"close CE"]
                            put_premium_collected_3=pe_initial_Price_2-PE_3_SL
                            Net_P_L=Net_P_L+call_premium_collected_1+call_premium_collected_2+call_premium_collected_3+put_premium_collected_3                              
                            

                            Time=df_CE_3.loc[(index_row+i+1),"Time"]
                            Date=df_CE_3.loc[(index_row+i+1),"Date"]
                            week=date_to_week(Date)

                            running_log_update("SL_Hit","Put_stk_3",PE_strike_3,"Put",Time,Date,week,formatted_Date_of_Init[k],formatted_Date_of_Expiry[k],0,0)

                            index_row,df_CE_1,df_CE_2,df_CE_3,df_CE_4=volatility_strike_pred(Date,Time,path_expiry_date_recurring,Startjee_1_dict_Call,Startjee_1_dict_Put,CE_Strike_1,CE_Strike_2,CE_Strike_3,CE_Strike_4,0,0,PE_strike_3,0,1,Len_ce)

######### REVESAL SEQUENCE ######


                        elif CE_Current_pr_1<CE_1_SL and CE_Current_pr_2<CE_2_SL and CE_Current_pr_3>=CE_3_SL and PE_Current_pr_3<PE_3_SL: 
                            Active_status_read=read_Active_status()
                            deleted_strike_ce=Active_status_read["Deactive Call Strike"]
                            Call_strikes_remove=Active_status_read["Active_call_Strike"]
                            Strike_ce_remove_copy=Call_strikes_remove[2]

                            if Strike_ce_remove_copy not in deleted_strike_ce:  
                                reversal_status=310100 #" the format is len,rev,CE_2,PE_2,PE_1"
                                Active_status_read["Deactive Call Strike"].append(Strike_ce_remove_copy)
                                Active_status_read["Deactive Call Strike Premium Initial"].append(Active_Initial_Sold_premium_call[2])
                                Active_status_read["Deactive Call Strike SL"].append(Active_SL_Call[2])

                                writing_Active_status(Active_status_read)


                                put_premium_collected_3=pe_initial_Price_3-df_PE_3.loc[(index_row+i+1),"close PE"]
                                call_premium_collected_1=ce_initial_Price_1-df_CE_1.loc[(index_row+i+1),"close CE"]
                                call_premium_collected_2=ce_initial_Price_2-df_CE_2.loc[(index_row+i+1),"close CE"]
                                Net_P_L=Net_P_L+call_premium_collected+put_premium_collected_1+put_premium_collected_2
                                time=df_PE_1.loc[(index_row+i+1),"Time"]
                                SL_update(time,Active_Initial_Sold_premium_call,Active_Initial_Sold_premium_put,CE_instantinious_pr,PE_instantinious_pr,Active_call_Strike,Active_put_Strike,Active_SL_Call,Active_SL_Put,reversal_status,Startjee_1_dict_Call,Startjee_1_dict_Put)
                            else:
                                put_premium_collected_3=pe_initial_Price_3-df_PE_3.loc[(index_row+i+1),"close PE"]
                                call_premium_collected_1=ce_initial_Price_1-df_CE_1.loc[(index_row+i+1),"close CE"]
                                call_premium_collected_2=ce_initial_Price_2-df_CE_2.loc[(index_row+i+1),"close CE"]
                                Net_P_L=Net_P_L+call_premium_collected+put_premium_collected_1+put_premium_collected_2
                                time=df_PE_1.loc[(index_row+i+1),"Time"]
                                SL_update(time,Active_Initial_Sold_premium_call,Active_Initial_Sold_premium_put,CE_instantinious_pr,PE_instantinious_pr,Active_call_Strike,Active_put_Strike,Active_SL_Call,Active_SL_Put,reversal_status,Startjee_1_dict_Call,Startjee_1_dict_Put)
 
                        elif CE_Current_pr_1<CE_1_SL and CE_Current_pr_2<CE_2_SL and CE_Current_pr_3>=CE_3_SL and PE_Current_pr_3>=PE_3_SL: 
                            Active_status_read=read_Active_status()
                            deleted_strike_pe=Active_status_read["Deactive Put Strike"]
                            deleted_strike_ce=Active_status_read["Deactive Call Strike"]

                            Put_strikes_remove=Active_status_read["Active_put_Strike"]
                            Call_Strikes_remove=Active_status_read["Active_call_Strike"]

                            Strike_ce_remove_copy=Call_strikes_remove[2]
                            Strike_pe_remove_copy=Put_strikes_remove[0]

                            if Strike_pe_remove_copy not in deleted_strike_pe or Strike_ce_remove_copy not in deleted_strike_ce:  
                                reversal_status=311100 #" the format is len,rev,CE_2,PE_2,PE_1"
                                Active_status_read["Deactive Put Strike"].append(Strike_pe_remove_copy)
                                Active_status_read["Deactive Call Strike"].append(Strike_ce_remove_copy)
                                Active_status_read["Deactive Call Strike Premium Initial"].append(Active_Initial_Sold_premium_call[2])
                                Active_status_read["Deactive Call Strike SL"].append(Active_SL_Call[2])
                                Active_status_read["Deactive Put Strike Premium Initial"].append(Active_Initial_Sold_premium_put[0])
                                Active_status_read["Deactive Put Strike SL"].append(Active_SL_Put[0])

                                writing_Active_status(Active_status_read)


                                call_premium_collected_1=ce_initial_Price_1-df_CE_1.loc[(index_row+i+1),"close CE"]
                                call_premium_collected_2=ce_initial_Price_2-df_CE_2.loc[(index_row+i+1),"close CE"]
                                Net_P_L=Net_P_L+call_premium_collected_1+call_premium_collected_2
                                time=df_PE_1.loc[(index_row+i+1),"Time"]
                                SL_update(time,Active_Initial_Sold_premium_call,Active_Initial_Sold_premium_put,CE_instantinious_pr,PE_instantinious_pr,Active_call_Strike,Active_put_Strike,Active_SL_Call,Active_SL_Put,reversal_status,Startjee_1_dict_Call,Startjee_1_dict_Put)
                            else:
                                call_premium_collected_1=ce_initial_Price_1-df_CE_1.loc[(index_row+i+1),"close CE"]
                                call_premium_collected_2=ce_initial_Price_2-df_CE_2.loc[(index_row+i+1),"close CE"]
                                Net_P_L=Net_P_L+call_premium_collected_1+call_premium_collected_2
                                time=df_PE_1.loc[(index_row+i+1),"Time"]
                                SL_update(time,Active_Initial_Sold_premium_call,Active_Initial_Sold_premium_put,CE_instantinious_pr,PE_instantinious_pr,Active_call_Strike,Active_put_Strike,Active_SL_Call,Active_SL_Put,reversal_status,Startjee_1_dict_Call,Startjee_1_dict_Put)

                        elif CE_Current_pr_1<CE_1_SL and CE_Current_pr_2>=CE_2_SL and CE_Current_pr_3>=CE_3_SL and PE_Current_pr_3<PE_3_SL: 
                            Active_status_read=read_Active_status()
                            deleted_strike_ce=Active_status_read["Deactive Call Strike"]
                            Call_strikes_remove=Active_status_read["Active_call_Strike"]
        

                            Strike_ce_2_remove_copy=Call_strikes_remove[1]
                            Strike_ce_3_remove_copy=Call_strikes_remove[2]

                            if Strike_ce_2_remove_copy not in deleted_strike_ce or Strike_ce_3_remove_copy not in deleted_strike_ce:  
                                reversal_status=310110 #" the format is len,rev,CE_2,PE_2,PE_1"
                                Active_status_read["Deactive Call Strike"].append(Strike_ce_2_remove_copy)
                                Active_status_read["Deactive Call Strike"].append(Strike_ce_3_remove_copy)
                                Active_status_read["Deactive Call Strike Premium Initial"].append(Active_Initial_Sold_premium_call[1])
                                Active_status_read["Deactive Call Strike Premium Initial"].append(Active_Initial_Sold_premium_call[2])
                                Active_status_read["Deactive Call Strike SL"].append(Active_SL_Call[1])
                                Active_status_read["Deactive Call Strike SL"].append(Active_SL_Call[2])

                                writing_Active_status(Active_status_read)


                                call_premium_collected_1=ce_initial_Price_1-df_CE_1.loc[(index_row+i+1),"close CE"]
                                put_premium_collected_3=pe_initial_Price_3-df_PE_3.loc[(index_row+i+1),"close PE"]
                                Net_P_L=Net_P_L+call_premium_collected_1+put_premium_collected_3
                                time=df_CE_1.loc[(index_row+i+1),"Time"]
                                SL_update(time,Active_Initial_Sold_premium_call,Active_Initial_Sold_premium_put,CE_instantinious_pr,PE_instantinious_pr,Active_call_Strike,Active_put_Strike,Active_SL_Call,Active_SL_Put,reversal_status,Startjee_1_dict_Call,Startjee_1_dict_Put)
                            else:
                                call_premium_collected_1=ce_initial_Price_1-df_CE_1.loc[(index_row+i+1),"close CE"]
                                put_premium_collected_3=pe_initial_Price_3-df_PE_3.loc[(index_row+i+1),"close PE"]
                                Net_P_L=Net_P_L+call_premium_collected_1+put_premium_collected_3
                                time=df_CE_1.loc[(index_row+i+1),"Time"]
                                SL_update(time,Active_Initial_Sold_premium_call,Active_Initial_Sold_premium_put,CE_instantinious_pr,PE_instantinious_pr,Active_call_Strike,Active_put_Strike,Active_SL_Call,Active_SL_Put,reversal_status,Startjee_1_dict_Call,Startjee_1_dict_Put)
 
                        elif CE_Current_pr_1<CE_1_SL and CE_Current_pr_2>=CE_2_SL and CE_Current_pr_3>=CE_3_SL and PE_Current_pr_3>=PE_3_SL:
                            Active_status_read=read_Active_status()
                            deleted_strike_pe=Active_status_read["Deactive Put Strike"]
                            deleted_strike_ce=Active_status_read["Deactive Call Strike"]

                            Put_strikes_remove=Active_status_read["Active_put_Strike"]
                            Call_Strikes_remove=Active_status_read["Active_call_Strike"]

                            Strike_pe_3_remove_copy=Put_strikes_remove[0]
                            Strike_ce_3_remove_copy=Call_Strikes_remove[2]
                            Strike_ce_2_remove_copy=Call_Strikes_remove[1]


                            if Strike_ce_3_remove_copy not in deleted_strike_ce or Strike_ce_2_remove_copy not in deleted_strike_ce or Strike_pe_3_remove_copy not in deleted_strike_pe:  
                                reversal_status=311110 #" the format is len,rev,CE_2,PE_2,PE_1"

                                Active_status_read["Deactive Call Strike"].append(Strike_ce_2_remove_copy)
                                Active_status_read["Deactive Call Strike"].append(Strike_ce_3_remove_copy)
                                Active_status_read["Deactive Call Strike Premium Initial"].append(Active_Initial_Sold_premium_call[1])
                                Active_status_read["Deactive Call Strike Premium Initial"].append(Active_Initial_Sold_premium_call[2])
                                Active_status_read["Deactive Call Strike SL"].append(Active_SL_Call[1])
                                Active_status_read["Deactive Call Strike SL"].append(Active_SL_Call[2])
                                Active_status_read["Deactive Put Strike"].append(Strike_pe_3_remove_copy)
                                Active_status_read["Deactive Put Strike Premium Initial"].append(Active_Initial_Sold_premium_put[0])
                                Active_status_read["Deactive Put Strike SL"].append(Active_SL_Put[0])

                                writing_Active_status(Active_status_read)


                                call_premium_collected_1=ce_initial_Price_1-df_CE_1.loc[(index_row+i+1),"close CE"]
                                Net_P_L=Net_P_L+call_premium_collected_1
                                time=df_CE_1.loc[(index_row+i+1),"Time"]
                                SL_update(time,Active_Initial_Sold_premium_call,Active_Initial_Sold_premium_put,CE_instantinious_pr,PE_instantinious_pr,Active_call_Strike,Active_put_Strike,Active_SL_Call,Active_SL_Put,reversal_status,Startjee_1_dict_Call,Startjee_1_dict_Put)
                            else:
                                call_premium_collected_1=ce_initial_Price_1-df_CE_1.loc[(index_row+i+1),"close CE"]
                                Net_P_L=Net_P_L+call_premium_collected_1
                                time=df_CE_1.loc[(index_row+i+1),"Time"]
                                SL_update(time,Active_Initial_Sold_premium_call,Active_Initial_Sold_premium_put,CE_instantinious_pr,PE_instantinious_pr,Active_call_Strike,Active_put_Strike,Active_SL_Call,Active_SL_Put,reversal_status,Startjee_1_dict_Call,Startjee_1_dict_Put)
                        
                        elif CE_Current_pr_1>=CE_1_SL and CE_Current_pr_2>=CE_2_SL and CE_Current_pr_3>=CE_3_SL and PE_Current_pr_3<PE_3_SL:
                            Active_status_read=read_Active_status()
                            deleted_strike_ce=Active_status_read["Deactive Call Strike"]

                            Call_strikes_remove=Active_status_read["Active_call_Strike"]

                            Strike_ce_1_remove_copy=Call_strikes_remove[0]
                            Strike_ce_2_remove_copy=Call_strikes_remove[1]
                            Strike_ce_3_remove_copy=Call_strikes_remove[2]

                            if Strike_ce_1_remove_copy not in deleted_strike_ce or Strike_ce_2_remove_copy not in deleted_strike_ce or Strike_ce_3_remove_copy not in deleted_strike_ce:  
                                reversal_status=310111 #" the format is len,rev,CE_2,PE_2,PE_1"
                                Active_status_read["Deactive Call Strike"].append(Strike_ce_1_remove_copy)
                                Active_status_read["Deactive Call Strike"].append(Strike_ce_2_remove_copy)
                                Active_status_read["Deactive Call Strike"].append(Strike_ce_3_remove_copy)
                                Active_status_read["Deactive Call Strike Premium Initial"].append(Active_Initial_Sold_premium_call[0])
                                Active_status_read["Deactive Call Strike Premium Initial"].append(Active_Initial_Sold_premium_call[1])
                                Active_status_read["Deactive Call Strike Premium Initial"].append(Active_Initial_Sold_premium_call[2])
                                Active_status_read["Deactive Call Strike SL"].append(Active_SL_Call[0])
                                Active_status_read["Deactive Call Strike SL"].append(Active_SL_Call[1])
                                Active_status_read["Deactive Call Strike SL"].append(Active_SL_Call[2])

                                writing_Active_status(Active_status_read)

                                put_premium_collected_3=pe_initial_Price_3-df_PE_3.loc[(index_row+i+1),"close CE"]
                                Net_P_L=Net_P_L+put_premium_collected_3
                                time=df_PE_3.loc[(index_row+i+1),"Time"]
                                SL_update(time,Active_Initial_Sold_premium_call,Active_Initial_Sold_premium_put,CE_instantinious_pr,PE_instantinious_pr,Active_call_Strike,Active_put_Strike,Active_SL_Call,Active_SL_Put,reversal_status,Startjee_1_dict_Call,Startjee_1_dict_Put)
                            else:
                                put_premium_collected_3=pe_initial_Price_3-df_PE_3.loc[(index_row+i+1),"close CE"]
                                Net_P_L=Net_P_L+put_premium_collected_3
                                time=df_PE_3.loc[(index_row+i+1),"Time"]
                                SL_update(time,Active_Initial_Sold_premium_call,Active_Initial_Sold_premium_put,CE_instantinious_pr,PE_instantinious_pr,Active_call_Strike,Active_put_Strike,Active_SL_Call,Active_SL_Put,reversal_status,Startjee_1_dict_Call,Startjee_1_dict_Put)

                        elif CE_Current_pr_1>=CE_1_SL and CE_Current_pr_2>=CE_2_SL and CE_Current_pr_3>=CE_3_SL and PE_Current_pr_3>=PE_3_SL:
                            Active_status_read=read_Active_status()
                            deleted_strike_pe=Active_status_read["Deactive Put Strike"]
                            deleted_strike_ce=Active_status_read["Deactive Call Strike"]

                            Put_strikes_remove=Active_status_read["Active_put_Strike"]
                            Call_Strikes_remove=Active_status_read["Active_call_Strike"]

                            Strike_ce_1_remove_copy=Call_strikes_remove[0]
                            Strike_ce_2_remove_copy=Call_strikes_remove[1]
                            Strike_ce_3_remove_copy=Call_strikes_remove[2]
                            Strike_pe_3_remove_copy=Put_strikes_remove[0]


                            ## Read the list from the text file  ########
                            # deleted_strike=data
                            if Strike_ce_1_remove_copy not in deleted_strike_ce or Strike_ce_2_remove_copy not in deleted_strike_ce or Strike_ce_3_remove_copy not in deleted_strike_ce or Strike_pe_remove_copy not in deleted_strike_pe: 
                                reversal_status=311111 #" the format is len,rev,CE_2,PE_2,PE_1"

                                Active_status_read["Deactive Call Strike"].append(Strike_ce_1_remove_copy)
                                Active_status_read["Deactive Call Strike"].append(Strike_ce_2_remove_copy)
                                Active_status_read["Deactive Call Strike"].append(Strike_ce_3_remove_copy)
                                Active_status_read["Deactive Call Strike Premium Initial"].append(Active_Initial_Sold_premium_call[0])
                                Active_status_read["Deactive Call Strike Premium Initial"].append(Active_Initial_Sold_premium_call[1])
                                Active_status_read["Deactive Call Strike Premium Initial"].append(Active_Initial_Sold_premium_call[2])
                                Active_status_read["Deactive Call Strike SL"].append(Active_SL_Call[0])
                                Active_status_read["Deactive Call Strike SL"].append(Active_SL_Call[1])
                                Active_status_read["Deactive Call Strike SL"].append(Active_SL_Call[2])
                                Active_status_read["Deactive Put Strike"].append(Strike_pe_1_remove_copy)
                                Active_status_read["Deactive Put Strike Premium Initial"].append(Active_Initial_Sold_premium_put[0])
                                Active_status_read["Deactive Put Strike SL"].append(Active_SL_Put[0])

                                writing_Active_status(Active_status_read)

                                break
                        else:
                            pass

                    elif Len_ce==4:

                        CE_1_SL=Active_SL_Call[0]
                        CE_2_SL=Active_SL_Call[1]
                        CE_3_SL=Active_SL_Call[2]
                        CE_4_SL=Active_SL_Call[3]

                        CE_Current_pr_1=df_CE_1.loc[(i+index_row+1),"high CE"]
                        CE_Current_pr_2=df_CE_2.loc[(i+index_row+1),"high CE"]
                        CE_Current_pr_3=df_CE_3.loc[(i+index_row+1),"high CE"]
                        CE_Current_pr_4=df_CE_4.loc[(i+index_row+1),"high CE"]

                        
                        CE_Current_pr_1_close=df_CE_1.loc[(i+index_row+1),"close CE"]
                        CE_Current_pr_2_close=df_CE_2.loc[(i+index_row+1),"close CE"]
                        CE_Current_pr_3_close=df_CE_3.loc[(i+index_row+1),"close CE"]
                        CE_Current_pr_4_close=df_CE_4.loc[(i+index_row+1),"close CE"]

                        ce_initial_Price_1=Active_Initial_Sold_premium_call[0]
                        ce_initial_Price_2=Active_Initial_Sold_premium_call[1]
                        ce_initial_Price_3=Active_Initial_Sold_premium_call[2]
                        ce_initial_Price_4=Active_Initial_Sold_premium_call[3]

                        CE_instantinious_pr=[CE_Current_pr_1_close,CE_Current_pr_2_close,CE_Current_pr_3_close,CE_Current_pr_4_close]
                        PE_instantinious_pr=[]

                        
                        Startjee_1_dict_Put[Active_put_Strike[0]]=[PE_Current_pr_1_close,pe_initial_Price_1,PE_1_SL]
                        Startjee_1_dict_Put[Active_put_Strike[1]]=[PE_Current_pr_2_close,pe_initial_Price_2,PE_2_SL]
                        Startjee_1_dict_Put[Active_put_Strike[2]]=[PE_Current_pr_3_close,pe_initial_Price_3,PE_3_SL]
                        Startjee_1_dict_Put[Active_put_Strike[3]]=[PE_Current_pr_4_close,pe_initial_Price_4,PE_4_SL]

                        if CE_Current_pr_1<CE_1_SL and CE_Current_pr_2<CE_2_SL and CE_Current_pr_3<CE_3_SL and CE_Current_pr_4<CE_4_SL:
                            call_premium_collected_1=ce_initial_Price_1-df_CE_1.loc[(index_row+i+1),"close CE"]
                            call_premium_collected_2=ce_initial_Price_2-df_CE_2.loc[(index_row+i+1),"close CE"]
                            call_premium_collected_3=ce_initial_Price_3-df_CE_3.loc[(index_row+i+1),"close CE"]
                            call_premium_collected_4=ce_initial_Price_4-df_CE_4.loc[(index_row+i+1),"close CE"]
                            Net_P_L=Net_P_L+call_premium_collected_1+call_premium_collected_2+call_premium_collected_3+call_premium_collected_4
                            time=df_CE_1.loc[(index_row+i+1),"Time"]
                            SL_update(time,Active_Initial_Sold_premium_call,Active_Initial_Sold_premium_put,CE_instantinious_pr,PE_instantinious_pr,Active_call_Strike,Active_put_Strike,Active_SL_Call,Active_SL_Put,reversal_status,Startjee_1_dict_Call,Startjee_1_dict_Put)

                        elif CE_Current_pr_1<CE_1_SL and CE_Current_pr_2<CE_2_SL and CE_Current_pr_3<CE_3_SL and CE_Current_pr_4>=CE_4_SL:
                            Active_status_read=read_Active_status()
                            deleted_strike_ce=Active_status_read["Deactive Call Strike"]
                            Call_strikes_remove=Active_status_read["Active_call_Strike"]

                            Strike_ce_4_remove_copy=Call_strikes_remove[3]

                            if Strike_ce_4_remove_copy not in deleted_strike_ce:  
                                reversal_status=411000 #" the format is len,rev,CE_2,PE_2,PE_1"
                                Active_status_read["Deactive Call Strike"].append(Strike_ce_4_remove_copy)
                                Active_status_read["Deactive Call Strike Premium Initial"].append(Active_Initial_Sold_premium_call[3])
                                Active_status_read["Deactive Call Strike SL"].append(Active_SL_Call[3])

                                writing_Active_status(Active_status_read)


                                call_premium_collected_1=ce_initial_Price_1-df_CE_1.loc[(index_row+i+1),"close CE"]
                                call_premium_collected_2=ce_initial_Price_2-df_CE_2.loc[(index_row+i+1),"close CE"]
                                call_premium_collected_3=ce_initial_Price_3-df_CE_3.loc[(index_row+i+1),"close CE"]
                                Net_P_L=Net_P_L+call_premium_collected_1+call_premium_collected_2+call_premium_collected_3
                                time=df_CE_1.loc[(index_row+i+1),"Time"]
                                SL_update(time,Active_Initial_Sold_premium_call,Active_Initial_Sold_premium_put,CE_instantinious_pr,PE_instantinious_pr,Active_call_Strike,Active_put_Strike,Active_SL_Call,Active_SL_Put,reversal_status,Startjee_1_dict_Call,Startjee_1_dict_Put)
                            else:
                                call_premium_collected_1=ce_initial_Price_1-df_CE_1.loc[(index_row+i+1),"close CE"]
                                call_premium_collected_2=ce_initial_Price_2-df_CE_2.loc[(index_row+i+1),"close CE"]
                                call_premium_collected_3=ce_initial_Price_3-df_CE_3.loc[(index_row+i+1),"close CE"]
                                Net_P_L=Net_P_L+call_premium_collected_1+call_premium_collected_2+call_premium_collected_3
                                time=df_CE_1.loc[(index_row+i+1),"Time"]
                                SL_update(time,Active_Initial_Sold_premium_call,Active_Initial_Sold_premium_put,CE_instantinious_pr,PE_instantinious_pr,Active_call_Strike,Active_put_Strike,Active_SL_Call,Active_SL_Put,reversal_status,Startjee_1_dict_Call,Startjee_1_dict_Put)
 
                        elif CE_Current_pr_1<CE_1_SL and CE_Current_pr_2<CE_2_SL and CE_Current_pr_3>=CE_3_SL and CE_Current_pr_4>=CE_4_SL:
                            Active_status_read=read_Active_status()
                            deleted_strike_ce=Active_status_read["Deactive Call Strike"]
                            Call_strikes_remove=Active_status_read["Active_call_Strike"]

                            Strike_ce_3_remove_copy=Call_strikes_remove[2]
                            Strike_ce_4_remove_copy=Call_strikes_remove[3]


                            if Strike_ce_4_remove_copy not in deleted_strike_ce or Strike_ce_3_remove_copy not in deleted_strike_ce:  
                                reversal_status=411100 #" the format is len,rev,CE_2,PE_2,PE_1"
                                Active_status_read["Deactive Call Strike"].append(Strike_ce_4_remove_copy)
                                Active_status_read["Deactive Call Strike Premium Initial"].append(Active_Initial_Sold_premium_call[3])
                                Active_status_read["Deactive Call Strike SL"].append(Active_SL_Call[3])
                                Active_status_read["Deactive Call Strike"].append(Strike_ce_3_remove_copy)
                                Active_status_read["Deactive Call Strike Premium Initial"].append(Active_Initial_Sold_premium_call[2])
                                Active_status_read["Deactive Call Strike SL"].append(Active_SL_Call[2])

                                writing_Active_status(Active_status_read)


                                call_premium_collected_1=ce_initial_Price_1-df_CE_1.loc[(index_row+i+1),"close CE"]
                                call_premium_collected_2=ce_initial_Price_2-df_CE_2.loc[(index_row+i+1),"close CE"]
                                Net_P_L=Net_P_L+call_premium_collected_1+call_premium_collected_2
                                time=df_PE_1.loc[(index_row+i+1),"Time"]
                                SL_update(time,Active_Initial_Sold_premium_call,Active_Initial_Sold_premium_put,CE_instantinious_pr,PE_instantinious_pr,Active_call_Strike,Active_put_Strike,Active_SL_Call,Active_SL_Put,reversal_status,Startjee_1_dict_Call,Startjee_1_dict_Put)
                            else:
                                call_premium_collected_1=ce_initial_Price_1-df_CE_1.loc[(index_row+i+1),"close CE"]
                                call_premium_collected_2=ce_initial_Price_2-df_CE_2.loc[(index_row+i+1),"close CE"]
                                Net_P_L=Net_P_L+call_premium_collected_1+call_premium_collected_2
                                time=df_CE_1.loc[(index_row+i+1),"Time"]
                                SL_update(time,Active_Initial_Sold_premium_call,Active_Initial_Sold_premium_put,CE_instantinious_pr,PE_instantinious_pr,Active_call_Strike,Active_put_Strike,Active_SL_Call,Active_SL_Put,reversal_status,Startjee_1_dict_Call,Startjee_1_dict_Put)

                        elif CE_Current_pr_1<CE_1_SL and CE_Current_pr_2>=CE_2_SL and CE_Current_pr_3>=CE_3_SL and CE_Current_pr_4>=CE_4_SL:
                            Active_status_read=read_Active_status()
                            deleted_strike_ce=Active_status_read["Deactive Call Strike"]
                            Call_strikes_remove=Active_status_read["Active_call_Strike"]

                            Strike_ce_2_remove_copy=Call_strikes_remove[1]
                            Strike_ce_3_remove_copy=Call_strikes_remove[2]
                            Strike_ce_4_remove_copy=Call_strikes_remove[3]


                            if Strike_ce_4_remove_copy not in deleted_strike_ce or Strike_ce_3_remove_copy not in deleted_strike_ce or Strike_ce_2_remove_copy not in deleted_strike_ce:  
                                reversal_status=411100 #" the format is len,rev,CE_2,PE_2,PE_1"
                                Active_status_read["Deactive Call Strike"].append(Strike_ce_4_remove_copy)
                                Active_status_read["Deactive Call Strike Premium Initial"].append(Active_Initial_Sold_premium_call[3])
                                Active_status_read["Deactive Call Strike SL"].append(Active_SL_Call[3])
                                Active_status_read["Deactive Call Strike"].append(Strike_ce_3_remove_copy)
                                Active_status_read["Deactive Call Strike Premium Initial"].append(Active_Initial_Sold_premium_call[2])
                                Active_status_read["Deactive Call Strike SL"].append(Active_SL_Call[2])
                                Active_status_read["Deactive Call Strike"].append(Strike_ce_2_remove_copy)
                                Active_status_read["Deactive Call Strike Premium Initial"].append(Active_Initial_Sold_premium_call[1])
                                Active_status_read["Deactive Call Strike SL"].append(Active_SL_Call[1])

                                writing_Active_status(Active_status_read)


                                call_premium_collected_1=ce_initial_Price_1-df_CE_1.loc[(index_row+i+1),"close CE"]
                                Net_P_L=Net_P_L+call_premium_collected_1
                                time=df_CE_1.loc[(index_row+i+1),"Time"]
                                SL_update(time,Active_Initial_Sold_premium_call,Active_Initial_Sold_premium_put,CE_instantinious_pr,PE_instantinious_pr,Active_call_Strike,Active_put_Strike,Active_SL_Call,Active_SL_Put,reversal_status,Startjee_1_dict_Call,Startjee_1_dict_Put)
                            else:
                                call_premium_collected_1=ce_initial_Price_1-df_CE_1.loc[(index_row+i+1),"close CE"]
                                Net_P_L=Net_P_L+call_premium_collected_1
                                time=df_CE_1.loc[(index_row+i+1),"Time"]
                                SL_update(time,Active_Initial_Sold_premium_call,Active_Initial_Sold_premium_put,CE_instantinious_pr,PE_instantinious_pr,Active_call_Strike,Active_put_Strike,Active_SL_Call,Active_SL_Put,reversal_status,Startjee_1_dict_Call,Startjee_1_dict_Put)

                        elif CE_Current_pr_1>=CE_1_SL and CE_Current_pr_2>=CE_2_SL and CE_Current_pr_3>=CE_3_SL and CE_Current_pr_4>=CE_4_SL:
                            Active_status_read=read_Active_status()
                            deleted_strike_ce=Active_status_read["Deactive Call Strike"]
                            Call_strikes_remove=Active_status_read["Active_call_Strike"]

                            Strike_ce_1_remove_copy=Call_strikes_remove[0]
                            Strike_ce_2_remove_copy=Call_strikes_remove[1]
                            Strike_ce_3_remove_copy=Call_strikes_remove[2]
                            Strike_ce_4_remove_copy=Call_strikes_remove[3]


                            if Strike_ce_4_remove_copy not in deleted_strike_ce or Strike_ce_3_remove_copy not in deleted_strike_ce or Strike_ce_2_remove_copy not in deleted_strike_ce or Strike_ce_1_remove_copy not in deleted_strike_ce:  
                                reversal_status=411100 #" the format is len,rev,CE_2,PE_2,PE_1"
                                Active_status_read["Deactive Call Strike"].append(Strike_ce_4_remove_copy)
                                Active_status_read["Deactive Call Strike Premium Initial"].append(Active_Initial_Sold_premium_call[3])
                                Active_status_read["Deactive Call Strike SL"].append(Active_SL_Call[3])
                                Active_status_read["Deactive Call Strike"].append(Strike_ce_3_remove_copy)
                                Active_status_read["Deactive Call Strike Premium Initial"].append(Active_Initial_Sold_premium_call[2])
                                Active_status_read["Deactive Call Strike SL"].append(Active_SL_Call[2])
                                Active_status_read["Deactive Call Strike"].append(Strike_ce_2_remove_copy)
                                Active_status_read["Deactive Call Strike Premium Initial"].append(Active_Initial_Sold_premium_call[1])
                                Active_status_read["Deactive Call Strike SL"].append(Active_SL_Call[1])
                                Active_status_read["Deactive Call Strike"].append(Strike_ce_1_remove_copy)
                                Active_status_read["Deactive Call Strike Premium Initial"].append(Active_Initial_Sold_premium_call[0])
                                Active_status_read["Deactive Call Strike SL"].append(Active_SL_Call[0])

                                writing_Active_status(Active_status_read)

                                break
                        else:
                            pass
                    
                    else:
                        pass


                else:
                    pass
            



def morning_code(path_expiry_date_recurring,date):


    if Market_trend=="Neutral":
        CE_stk= Active_call_Strike[0]
        PE_stk=Active_put_Strike[0]

        file_ce_1=f"NIFTY{str(CE_stk)}_CE.csv"
        file_pe_1=f"NIFTY{str(PE_stk)}_PE.csv"

        df_ce=pd.read_csv(path_expiry_date_recurring+file_ce_1)
        df_pe=pd.read_csv(path_expiry_date_recurring+file_pe_1)

        if (len(df_ce.loc[4,'Time']))>5:
            df_ce['Time'] = df_ce['Time'].apply(lambda x: x[:5])
            df_pe['Time'] = df_pe['Time'].apply(lambda x: x[:5])
        else:
            pass

        df_ce,df_pe=merging(df_ce,df_pe,"Call","Put")
        row_index_call = df_ce.index[(df_ce['Time'] == Checking_time)&(df_ce['Date'] == date)].tolist()

        index_row=row_index_call[0]

        return index_row,df_ce,df_pe
    
    elif Market_trend=="Trending Up":
        len_pe=len(Active_put_Strike)
        len_ce=len(Active_call_Strike)

        if len_pe==2:
            PE_stk_1=Active_put_Strike[0]
            PE_stk_2=Active_put_Strike[1]
            CE_stk=Active_call_Strike[0]

            file_pe_1=f"NIFTY{str(PE_stk_1)}_PE.csv"
            file_pe_2=f"NIFTY{str(PE_stk_2)}_PE.csv"
            file_ce_1=f"NIFTY{str(CE_stk)}_CE.csv"

            df_pe_1=pd.read_csv(path_expiry_date_recurring+file_pe_1)
            df_pe_2=pd.read_csv(path_expiry_date_recurring+file_pe_2)
            df_ce=pd.read_csv(path_expiry_date_recurring+file_ce_1)


            if len(df_ce.loc[4,'Time'])>5:
                df_ce['Time'] = df_ce['Time'].apply(lambda x: x[:5])
                df_pe_1['Time'] = df_pe_1['Time'].apply(lambda x: x[:5])
                df_pe_2['Time'] = df_pe_2['Time'].apply(lambda x: x[:5])
            else:
                pass

            df_ce,df_pe_1=merging(df_ce,df_pe_1,"Call","Put")
            df_pe_1,df_pe_2=merging(df_pe_1,df_pe_2,"Put","Put")

            row_index_call = df_ce.index[(df_ce['Time'] == Checking_time)&(df_ce['Date'] == date)].tolist()

            index_row=row_index_call[0]
            return index_row,df_ce,df_pe_1,df_pe_2
        
        elif len_pe==3:
            PE_stk_1=Active_put_Strike[0]
            PE_stk_2=Active_put_Strike[1]
            PE_stk_3=Active_put_Strike[2]
            CE_stk=Active_call_Strike[0]

            file_pe_1=f"NIFTY{str(PE_stk_1)}_PE.csv"
            file_pe_2=f"NIFTY{str(PE_stk_2)}_PE.csv"
            file_pe_3=f"NIFTY{str(PE_stk_3)}_PE.csv"
            file_ce_1=f"NIFTY{str(CE_stk)}_CE.csv"

            df_pe_1=pd.read_csv(path_expiry_date_recurring+file_pe_1)
            df_pe_2=pd.read_csv(path_expiry_date_recurring+file_pe_2)
            df_pe_3=pd.read_csv(path_expiry_date_recurring+file_pe_3)
            df_ce=pd.read_csv(path_expiry_date_recurring+file_ce_1)

            if len(df_ce.loc[4,'Time'])>5:
                df_ce['Time'] = df_ce['Time'].apply(lambda x: x[:5])
                df_pe_1['Time'] = df_pe_1['Time'].apply(lambda x: x[:5])
                df_pe_2['Time'] = df_pe_2['Time'].apply(lambda x: x[:5])
                df_pe_3['Time'] = df_pe_3['Time'].apply(lambda x: x[:5])
            else:
                pass

            df_ce,df_pe_1=merging(df_ce,df_pe_1,"Call","Put")
            df_pe_1,df_pe_2=merging(df_pe_1,df_pe_2,"Put","Put")
            df_pe_3,df_pe_2=merging(df_pe_3,df_pe_2,"Put","Put")

            row_index_call = df_ce.index[(df_ce['Time'] == Checking_time)&(df_ce['Date'] == date)].tolist()

            index_row=row_index_call[0]
            return index_row,df_ce,df_pe_1,df_pe_2,df_pe_3
        
        elif len_pe==4:
            PE_stk_1=Active_put_Strike[0]
            PE_stk_2=Active_put_Strike[1]
            PE_stk_3=Active_put_Strike[2]
            PE_stk_4=Active_put_Strike[3]

            file_pe_1=f"NIFTY{str(PE_stk_1)}_PE.csv"
            file_pe_2=f"NIFTY{str(PE_stk_2)}_PE.csv"
            file_pe_3=f"NIFTY{str(PE_stk_3)}_PE.csv"
            file_pe_4=f"NIFTY{str(PE_stk_4)}_PE.csv"

            df_pe_1=pd.read_csv(path_expiry_date_recurring+file_pe_1)
            df_pe_2=pd.read_csv(path_expiry_date_recurring+file_pe_2)
            df_pe_3=pd.read_csv(path_expiry_date_recurring+file_pe_3)
            df_pe_4=pd.read_csv(path_expiry_date_recurring+file_pe_4)

            if len(df_pe_1.loc[4,'Time'])>5:
                df_pe_1['Time'] = df_pe_1['Time'].apply(lambda x: x[:5])
                df_pe_2['Time'] = df_pe_2['Time'].apply(lambda x: x[:5])
                df_pe_3['Time'] = df_pe_3['Time'].apply(lambda x: x[:5])
                df_pe_4['Time'] = df_pe_4['Time'].apply(lambda x: x[:5])
            else:
                pass

            df_pe_1,df_pe_2=merging(df_pe_1,df_pe_2,"Put","Put")
            df_pe_3,df_pe_2=merging(df_pe_3,df_pe_2,"Put","Put")
            df_pe_4,df_pe_3=merging(df_pe_4,df_pe_3,"Put","Put")

            row_index_call = df_ce.index[(df_ce['Time'] == Checking_time)&(df_ce['Date'] == date)].tolist()

            index_row=row_index_call[0]
            return index_row,df_pe_1,df_pe_2,df_pe_3,df_pe_4
        

    elif Market_trend=="Trending Down":

        len_pe=len(Active_put_Strike)
        len_ce=len(Active_call_Strike)

        if len_ce==2:
            CE_stk_1=Active_call_Strike[0]
            CE_stk_2=Active_call_Strike[1]
            PE_stk_2=Active_put_Strike[0]

            file_ce_1=f"NIFTY{str(CE_stk_1)}_CE.csv"
            file_ce_2=f"NIFTY{str(CE_stk_2)}_CE.csv"
            file_pe_2=f"NIFTY{str(PE_stk_1)}_PE.csv"

            df_ce_1=pd.read_csv(path_expiry_date_recurring+file_ce_1)
            df_ce_2=pd.read_csv(path_expiry_date_recurring+file_ce_2)
            df_pe_2=pd.read_csv(path_expiry_date_recurring+file_pe_2)


            if len(df_ce_1.loc[4,'Time'])>5:
                df_ce_1['Time'] = df_ce_1['Time'].apply(lambda x: x[:5])
                df_ce_2['Time'] = df_ce_2['Time'].apply(lambda x: x[:5])
                df_pe_2['Time'] = df_pe_2['Time'].apply(lambda x: x[:5])
            else:
                pass

            df_ce_1,df_pe_2=merging(df_ce_1,df_pe_2,"Call","Put")
            df_ce_1,df_ce_2=merging(df_ce_1,df_ce_2,"Call","Call")

            row_index_call = df_ce_1.index[(df_ce_1['Time'] == Checking_time)&(df_ce_1['Date'] == date)].tolist()

            index_row=row_index_call[0]
            return index_row,df_ce_1,df_ce_2,df_pe_2
        
        elif len_ce==3:
            CE_stk_1=Active_call_Strike[0]
            CE_stk_2=Active_call_Strike[1]
            CE_stk_3=Active_call_Strike[2]
            PE_stk_3=Active_put_Strike[0]

            file_ce_1=f"NIFTY{str(CE_stk_1)}_CE.csv"
            file_ce_2=f"NIFTY{str(CE_stk_2)}_CE.csv"
            file_ce_3=f"NIFTY{str(CE_stk_3)}_CE.csv"
            file_pe_3=f"NIFTY{str(PE_stk_3)}_PE.csv"

            df_ce_1=pd.read_csv(path_expiry_date_recurring+file_ce_1)
            df_ce_2=pd.read_csv(path_expiry_date_recurring+file_ce_2)
            df_ce_3=pd.read_csv(path_expiry_date_recurring+file_ce_3)
            df_pe_2=pd.read_csv(path_expiry_date_recurring+file_pe_3)

            if len(df_ce_1.loc[4,'Time'])>5:
                df_ce_1['Time'] = df_ce_1['Time'].apply(lambda x: x[:5])
                df_ce_2['Time'] = df_ce_2['Time'].apply(lambda x: x[:5])
                df_ce_3['Time'] = df_ce_3['Time'].apply(lambda x: x[:5])
                df_pe_3['Time'] = df_pe_3['Time'].apply(lambda x: x[:5])
            else:
                pass

            df_ce_1,df_pe_3=merging(df_ce_1,df_pe_3,"Call","Put")
            df_ce_1,df_ce_2=merging(df_ce_1,df_ce_2,"Call","Call")
            df_ce_1,df_ce_3=merging(df_ce_1,df_ce_3,"Call","Call")

            row_index_call = df_ce_1.index[(df_ce_1['Time'] == Checking_time)&(df_ce_1['Date'] == date)].tolist()

            index_row=row_index_call[0]
            return index_row,df_ce_1,df_ce_2,df_ce_3,df_pe_3
        
        elif len_ce==4:
            CE_stk_1=Active_call_Strike[0]
            CE_stk_2=Active_call_Strike[1]
            CE_stk_3=Active_call_Strike[2]
            CE_stk_4=Active_call_Strike[3]

            file_ce_1=f"NIFTY{str(CE_stk_1)}_CE.csv"
            file_ce_2=f"NIFTY{str(CE_stk_2)}_CE.csv"
            file_ce_3=f"NIFTY{str(CE_stk_3)}_CE.csv"
            file_ce_4=f"NIFTY{str(CE_stk_4)}_CE.csv"

            df_ce_1=pd.read_csv(path_expiry_date_recurring+file_ce_1)
            df_ce_2=pd.read_csv(path_expiry_date_recurring+file_ce_2)
            df_ce_3=pd.read_csv(path_expiry_date_recurring+file_ce_3)
            df_ce_4=pd.read_csv(path_expiry_date_recurring+file_ce_4)

            if len(df_ce_1.loc[4,'Time'])>5:
                df_ce_1['Time'] = df_ce_1['Time'].apply(lambda x: x[:5])
                df_ce_2['Time'] = df_ce_2['Time'].apply(lambda x: x[:5])
                df_ce_3['Time'] = df_ce_3['Time'].apply(lambda x: x[:5])
                df_ce_4['Time'] = df_ce_4['Time'].apply(lambda x: x[:5])
            else:
                pass

            df_ce_1,df_ce_4=merging(df_ce_1,df_ce_4,"Call","Call")
            df_ce_1,df_ce_2=merging(df_ce_1,df_ce_2,"Call","Call")
            df_ce_1,df_ce_3=merging(df_ce_1,df_ce_3,"Call","Call")

            row_index_call = df_ce_1.index[(df_ce_1['Time'] == Checking_time)&(df_ce_1['Date'] == date)].tolist()

            index_row=row_index_call[0]
            return index_row,df_ce_1,df_ce_2,df_ce_3,df_ce_4



def table_recording_code(Initial_day,Expiry_date,Day):
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
            if output_date==Expiry_date:
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
                df_call_init,df_put_init=merging(df_call_init,df_put_init,"Call","Put")

                date_str = formatted_Date_of_Init[k]
                date_obj = datetime.strptime(date_str, "%d-%b-%Y")
                Desired_Date = date_obj.strftime("%Y-%m-%d")

                row_index_call = df_call_init.index[(df_call_init['Time'] == Desired_time_CE)&(df_call_init['Date'] == Desired_Date)].tolist()
                row_index_put = df_put_init.index[(df_put_init['Time'] == Desired_time_PE)&(df_put_init['Date'] == Desired_Date)].tolist()

                week=date_to_week(Desired_Date)

                running_log_update("Entry","Call_stk_1",Call_Strike,"Call",Desired_time_CE,Desired_Date,week,formatted_Date_of_Init[k],formatted_Date_of_Expiry[k],0,0)
                running_log_update("Entry","Put_stk_1",Put_Strike,"Put",Desired_time_PE,Desired_Date,week,formatted_Date_of_Init[k],formatted_Date_of_Expiry[k],0,0)

                row_index_call=row_index_call[0]
                row_index_put=row_index_put[0]
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

                
                index_row=row_index_call
                Initial_day=formatted_Date_of_Init[k]
                Expiry_date=formatted_Date_of_Expiry[k]


                routine_code(index_row,Active_call_Strike,Active_put_Strike,Active_Initial_Sold_premium_call,Active_Initial_Sold_premium_put,Active_SL_Call,Active_SL_Put,Day,Initial_day,Expiry_date)
                
                Day=Day+1
            else:

                routine_code(index_row,Active_call_Strike,Active_put_Strike,Active_Initial_Sold_premium_call,Active_Initial_Sold_premium_put,Active_SL_Call,Active_SL_Put,Day,Initial_day,Expiry_date)
                margin_deployed=MARGIN_DEPLOYED
                
                if reversal_status is not None:
                    rev=1
                else:
                    rev=0

                final_log(Initial_day,Expiry_date,Market_trend,Net_P_L,margin_deployed,Len_ce,Len_pe,rev,"Call_stk_1","Put_stk_1")
                Day=Day+1
                

final_data={"Date of Initiation":date_init,"Date of Expiry":date_exp,"Market Sentiment":market_sentiment,
            "CE Strike 1":Call_stk_1,"CE Strike 2":Call_stk_2,"CE Strike 3":Call_stk_3,"CE Strike 4":Call_stk_4,
            "PE Strike 1":Put_stk_1,"PE Strike 2":Put_stk_2,"PE Strike 3":Put_stk_3,"PE Strike 4":Put_stk_4,
            "SL hit Time":sl_hit_time,"SL hit Date":sl_hit_date,"SL hit Week":sl_hit_week,"Entry Time Call":Entry_time_call,
            "Entry Time Put":Entry_time_put,"Entry Time Date":Entry_date,"Entry Time Week":Entry_week,"Profit and Loss":profit_loss,
            "Margin Used":Margin,"Profit Loss percent":ROI,"Overall Credit Spread Call":Net_Credit_Spread_Call,"Overall Credit Spread Put":Net_Credit_Spread_Put,
            "Overall Credit Spread Used":Net_Credit_Spread,"Reversal Status":reverse}


final_generated_DF=pd.DataFrame(final_data)
final_generated_DF.to_csv(Path_backtest_Report+final_generated_DF,index=False)