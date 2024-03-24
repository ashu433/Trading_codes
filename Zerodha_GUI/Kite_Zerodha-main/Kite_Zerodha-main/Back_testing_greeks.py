import pandas as pd
from datetime import datetime,timedelta
import os
import Black_scholes_model


Access_path_date="H:/My Drive/Daily_F_O_data/Options/Index/"
Accesst_path_Spot_IR="H:/My Drive/Daily_F_O_data/"
path_main="D:/ashu/Finance/algo_trading/Zerodha_GUI/Kite_Zerodha-main/Kite_Zerodha-main/"

Accepted_Expiry_Dates=["12-Mar-2020","09-Apr-2020","28-May-2020","19-Apr-2020","03-Dec-2020","28-Jan-2021","11-Mar-2021","01-Apr-2021","15-Apr-2021","22-Apr-2021","12-May-2021","22-Jul-2021","18-Aug-2021","03-Nov-2021","27-Jan-2022","03-Mar-2022","13-Apr-2022","05-May-2022","11-Aug-2022","18-Aug-2022","01-Sep-2022","06-Oct-2022","10-Nov-2022","26-Jan-2023","09-Mar-2023","30-Mar-2023","06-Apr-2023","04-May-2023","29-Jun-2023","17-Aug-2023","21-Sep-2023","05-Oct-2023","26-Oct-2023","16-Nov-2023","30-Nov-2023","28-Nov-2023"]
Rejected_Expiry_Dates=["27-Feb-2020","01-Apr-2020","16-Apr-2020","07-May-2020","08-Oct-2020","31-Dec-2020","08-Apr-2021","16-Apr-2021","21-Oct-2021","11-Nov-2021","25-Nov-2021","24-Mar-2022","21-Apr-2022","27-Oct-2022","13-Apr-2023","20-Apr-2023"]

file_startjee=pd.read_excel(path_main+"Startjee.xlsx", sheet_name="Past_Backtesting")

Date_of_Init=file_startjee["Date of Initiation"].tolist()
Date_of_Expiry=file_startjee["Expiry"].tolist()

formatted_Date_of_Init = [date.strftime('%d-%b-%Y') for date in Date_of_Init]
formatted_Date_of_Expiry = [date.strftime('%d-%b-%Y') for date in Date_of_Expiry]
Date_of_initiation=[]
Expiry_date=[]
Call_Strike=[]
Put_Strike=[]

desired_time="09:20"

def option_greegs_calculation(Strike_price,Option_price,Date_of_initiation,Expiry_date,Right):
    Strike_price=int(Strike_price)
    Initiation_date=Date_of_initiation
    Completion_date=Expiry_date
    start_date = datetime.strptime(Initiation_date, "%d-%b-%Y")
    end_date = datetime.strptime(Completion_date, "%d-%b-%Y")
    total_days = (end_date - start_date).days + 1
    Time=total_days/365
    Spot_price_file=pd.read_csv(Accesst_path_Spot_IR+"Nifty_50_Historical.csv")
    Interest_Rate=pd.read_csv(Accesst_path_Spot_IR+"91_Days_T_Bill_Data.csv")
    Desired_Date=Date_of_initiation

    date_obj = datetime.strptime(Desired_Date, '%d-%b-%Y')
    previous_date_obj = date_obj - timedelta(days=1)
    previous_date_str = previous_date_obj.strftime('%d-%b-%Y')

    Spot_price_file['Date'] = pd.to_datetime(Spot_price_file['Date'], format='%d-%m-%Y', errors='coerce')
    New_desired_date = pd.to_datetime(Desired_Date, format='%d-%b-%Y')
    filtered_df = Spot_price_file[(Spot_price_file['Date'] == Desired_Date) & (Spot_price_file['Time'] == desired_time)]
    index = filtered_df.index[0] if not filtered_df.empty else None
    closing_price=Spot_price_file.loc[index,"Close"]

    date_list=Interest_Rate["Date"].tolist()
    formatted_date=[]

    for i in range(len(date_list)):
        date=date_list[i]
        date_obj = datetime.strptime(date, "%m/%d/%Y")
        date_new = date_obj.strftime("%d-%m-%Y")
        formatted_date.append(date_new)

    Interest_Rate["Date"]=formatted_date

    Interest_Rate['Date'] = pd.to_datetime(Interest_Rate['Date'], format='%d-%m-%Y', errors='coerce')
    # New_desired_date = pd.to_datetime(previous_date_str, format='%d-%b-%Y')
    # filtered_df_IR = Interest_Rate[(Interest_Rate['Date'] == previous_date_str)]
    # index = filtered_df_IR.index[0] if not filtered_df_IR.empty else None
    # Interest_Rate=Interest_Rate.loc[index,"Price"]
    New_desired_date = pd.to_datetime(previous_date_str, format='%d-%b-%Y')
    filtered_df_IR = Interest_Rate[Interest_Rate['Date'] == New_desired_date]
    if filtered_df_IR.empty:
        next_date = New_desired_date + pd.DateOffset(days=1)
        filtered_df_IR = Interest_Rate[Interest_Rate['Date'] == next_date]
        index = filtered_df_IR.index[0] if not filtered_df_IR.empty else None
        Interest_Rate=Interest_Rate.loc[index,"Price"]
    else:
        index = filtered_df_IR.index[0] if not filtered_df_IR.empty else None
        Interest_Rate=Interest_Rate.loc[index,"Price"]

    Option_price=float(Option_price)
    closing_price=float(closing_price)
    IR=Interest_Rate/100
    IR=float(IR)

    if Right=="CE":
        r='c'
    elif Right=="PE":
        r='p'
    else:
        pass

    implied_volatility=Black_scholes_model.implied_vol(IR,closing_price,Strike_price,Time,Option_price,r)
    if implied_volatility==None:
        Delta=None
        Implied_volatility=None
        return Delta, Implied_volatility
    else:
        Delta,Gamma, Vega, Theta, Rho=Black_scholes_model.option_greeks(r,closing_price,Strike_price,Time,IR,implied_volatility)
        return Delta, implied_volatility



for i in range(len(formatted_Date_of_Init)):
    if formatted_Date_of_Expiry[i] in Rejected_Expiry_Dates:
        Date_of_initiation.append(formatted_Date_of_Init[i])
        Expiry_date.append(formatted_Date_of_Expiry[i])
        Call_Strike.append(None)
        Put_Strike.append(None)
    else:
        path_init_date=f"{Access_path_date}/{formatted_Date_of_Init[i]}/"
        path_expiry_date=f"{path_init_date}/NIFTY_{formatted_Date_of_Expiry[i]}/"

        print(path_init_date)
        print(path_expiry_date)
        file_names = os.listdir(path_expiry_date)
        csv_files = [file for file in file_names if file.endswith('.csv')]
        Strike_price_CE=[]
        Strike_price_PE=[]
        delta_CE=[]
        delta_PE=[]

        for j in range(len(csv_files)):
            strike_data=pd.read_csv(path_expiry_date+csv_files[j])
            strike_data['Time'] = strike_data['Time'].str.slice(0, 5)

            if desired_time in strike_data['Time'].values:
                index = strike_data[strike_data['Time'] == desired_time].index[0]
                Option_price=strike_data.iloc[index,5]
                string = csv_files[j]
                result = string.replace("NIFTY", "")
                result = result.replace(".csv", "")
                x=len(result)
                right=result[x-2:x]
                Strike=result.replace(f"_{right}","")
                delta,IV=option_greegs_calculation(Strike,Option_price,formatted_Date_of_Init[i],formatted_Date_of_Expiry[i],right)
                print(f"Strike Price: {Strike} right: {right} Delta: {delta} IV: {IV}")

                if right=="CE":
                    Strike_price_CE.append(Strike)
                    delta_CE.append(delta)
                elif right=="PE":
                    Strike_price_PE.append(Strike)
                    delta_PE.append(delta)
                else:
                    pass
            else:
                pass

        Strike_Delta_Call={"Call Strike":Strike_price_CE,"Call Delta":delta_CE}
        Strike_Delta_Put={"Put Strike":Strike_price_PE,"Put Delta":delta_PE}
        Strike_Delta_Call_df=pd.DataFrame(Strike_Delta_Call)
        Strike_Delta_Put_df=pd.DataFrame(Strike_Delta_Put)
        df_Call=Strike_Delta_Call_df.dropna()
        df_Put=Strike_Delta_Put_df.dropna()
        df_Call.reset_index(drop=True, inplace=True)
        df_Put.reset_index(drop=True, inplace=True)
        df_Put['Put Delta'] = -1*df_Put['Put Delta']
        index_call = (df_Call["Call Delta"] < 0.15).idxmax()
        Selected_Strike_Call=df_Call.loc[index_call,"Call Strike"]

        index_Put = (df_Put["Put Delta"] - 0.15)
        closest_to_zero_index = index_Put.abs().idxmin()
        Selected_Strike_Put=df_Put.loc[closest_to_zero_index, "Put Strike"]

        print(f"Selected Call Strike: {Selected_Strike_Call} and Selected Put Strike {Selected_Strike_Put}")
        Date_of_initiation.append(formatted_Date_of_Init[i])
        Expiry_date.append(formatted_Date_of_Expiry[i])
        Call_Strike.append(Selected_Strike_Call)
        Put_Strike.append(Selected_Strike_Put)


final_generated_dict={"Date of Initiation":Date_of_initiation,"Expiry":Expiry_date,"Call Strike":Call_Strike,"Put Strike":Put_Strike}
final_generated_DF=pd.DataFrame(final_generated_dict)
final_generated_DF.to_csv(path_main+"Computed_Strikes.csv",index=False)