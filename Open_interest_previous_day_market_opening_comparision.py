import pandas as pd
import numpy as np





def OI_previous_day_market_opening_comparison(OI_present_day,last_day,interval_present_day,interval_last_day):
    path="D:/ashu/Finance/algo_trading/Option_chain_data/"
    Present_day_OI=OI_present_day
    last_day_OI=last_day
    Present_day=pd.read_csv(Present_day_OI)
    Last_day=pd.read_excel(last_day_OI)
    interval_Present_day=interval_present_day
    interval_Last_day=interval_last_day
    column_list_Present_day = Present_day['Time'][::interval_Present_day].tolist()
    column_list_Last_day = Last_day['Time'][::interval_Last_day].tolist()
    len_present_day=len(column_list_Present_day)
    len_Last_day=len(column_list_Last_day)
    Present_day_starting_time=column_list_Present_day[0]
    Last_day_closing_time=column_list_Last_day[len_Last_day-1]
    present_day_df=Present_day[Present_day["Time"]==Present_day_starting_time]
    present_day_df=present_day_df.reset_index(drop=True)
    Last_day_df=Last_day[Last_day["Time"]==Last_day_closing_time]
    Last_day_df=Last_day_df.reset_index(drop=True)
    Nifty_current_price_Last_day=Last_day_df["Nifty Current Price"].iloc[1]
    index = (Last_day_df['strikePrice'] - Nifty_current_price_Last_day).abs().idxmin()
    ATM_strike_price_Last_day=Last_day_df['strikePrice'].iloc[index]

    Nifty_current_price_present_day=present_day_df["Nifty Current Price"].iloc[1]
    index = (present_day_df['strikePrice'] - Nifty_current_price_present_day).abs().idxmin()
    ATM_strike_price_present_day=present_day_df['strikePrice'].iloc[index]

    last_day_strike_price_list=[]
    Present_day_strike_price_list=[]

    for i in range(-2,3):
        last=ATM_strike_price_Last_day+i*50
        present=ATM_strike_price_present_day+i*50
        last_day_strike_price_list.append(last)
        Present_day_strike_price_list.append(present)

    combined_strike_prices=Present_day_strike_price_list+last_day_strike_price_list
    union_strike_prices=list(set(combined_strike_prices))
    union_strike_prices=np.sort(union_strike_prices).astype(int)
    strike_prices=pd.DataFrame(union_strike_prices)
    strike_prices=strike_prices.rename(columns={0: 'strikePrice'})

    Last_day_filtered_df = strike_prices.merge(Last_day_df, on='strikePrice', how='inner')
    present_day_filtered_df = strike_prices.merge(present_day_df, on='strikePrice', how='inner')

    change_in_OI_call= pd.DataFrame({'change_in_OI_call': present_day_filtered_df["CE_OI"] - Last_day_filtered_df["CE_OI"]})
    change_in_OI_put=pd.DataFrame({'change_in_OI_put': present_day_filtered_df["PE_OI"] - Last_day_filtered_df["PE_OI"]})
    change_in_Premium_call=pd.DataFrame({'change_in_Premium_call': present_day_filtered_df["CE_LTP"] - Last_day_filtered_df["CE_LTP"]})
    change_in_Premium_put=pd.DataFrame({'change_in_Premium_put': present_day_filtered_df["PE_LTP"] - Last_day_filtered_df["PE_LTP"]})

    money_flow_call=pd.DataFrame({'money_flow_call': change_in_OI_call["change_in_OI_call"]*change_in_Premium_call["change_in_Premium_call"]})
    money_flow_put=pd.DataFrame({'money_flow_put': change_in_OI_put["change_in_OI_put"]*change_in_Premium_put["change_in_Premium_put"]})
    percentage_change_in_OI_call=pd.DataFrame({'percentage_change_in_OI_call': (change_in_OI_call["change_in_OI_call"]/Last_day_filtered_df["CE_OI"])*100})
    percentage_change_in_OI_put=pd.DataFrame({'percentage_change_in_OI_put': (change_in_OI_put["change_in_OI_put"]/Last_day_filtered_df["PE_OI"])*100})
    percentage_change_in_premium_call=pd.DataFrame({'percentage_change_in_premium_call': (change_in_Premium_call["change_in_Premium_call"]/Last_day_filtered_df["CE_LTP"])*100})
    percentage_change_in_premium_put=pd.DataFrame({'percentage_change_in_premium_put': (change_in_Premium_put["change_in_Premium_put"]/Last_day_filtered_df["PE_LTP"])*100})

    Starting_day_conclusion_df=pd.concat([strike_prices, change_in_OI_call, change_in_OI_put, change_in_Premium_call, change_in_Premium_put, percentage_change_in_OI_call, percentage_change_in_OI_put,percentage_change_in_premium_call,percentage_change_in_premium_put,money_flow_call,money_flow_put], axis=1)

    def apply_condition(row):
        if ((row['change_in_OI_call'] > 0 and row['change_in_Premium_call'] > 0)):
            return 'Long BuildUP'
        elif ((row['change_in_OI_call'] < 0 and row['change_in_Premium_call'] < 0)):
            return 'Long Covering'
        elif ((row['change_in_OI_call'] > 0 and row['change_in_Premium_call'] < 0)):
            return 'Shot Buildup'
        elif ((row['change_in_OI_call'] < 0 and row['change_in_Premium_call'] > 0)):
            return 'Shot Covering'
        else:
            pass

    def apply_condition_put(row):
        if ((row['change_in_OI_put'] > 0 and row['change_in_Premium_put'] > 0)):
            return 'Long BuildUP'
        elif ((row['change_in_OI_put'] < 0 and row['change_in_Premium_put'] < 0)):
            return 'Long Covering'
        elif ((row['change_in_OI_put'] > 0 and row['change_in_Premium_put'] < 0)):
            return 'Shot Buildup'
        elif ((row['change_in_OI_put'] < 0 and row['change_in_Premium_put'] > 0)):
            return 'Shot Covering'
        else:
            pass

    Starting_day_conclusion_df["Conclusion_call"]=Starting_day_conclusion_df.apply(apply_condition, axis=1)
    Starting_day_conclusion_df["Conclusion_put"]=Starting_day_conclusion_df.apply(apply_condition_put, axis=1)

    Starting_day_conclusion_df.to_csv(path+"conclusion_starting_day.csv",index=False)


path_1="D:/ashu/Finance/OI_at_Market_Opening/"
path="D:/ashu/Finance/algo_trading/Option_chain_data/"
interval_Present_day=79
interval_Last_day=78
Present_day=path_1+"Option_chain_data_saving_17_07_2023.csv"
Last_day=path+"full_and_finial_file.xlsx"

OI_previous_day_market_opening_comparison(Present_day,Last_day,interval_Present_day,interval_Last_day)
