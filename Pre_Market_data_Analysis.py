import pandas as pd


# path="D:/ashu/Finance/algo_trading/Pre_market/"
# file=path+"MW-Pre-Open-Market-08-Jul-2023.xlsx"

def pre_market(closing_price,weightage_file,Pre_market_file):
    path="D:/ashu/Finance/algo_trading/Pre_market/"
    Pre_market_data=pd.read_csv(path+Pre_market_file)
    weightage_wise_data_nifty_50_stocks=pd.read_excel(weightage_file)
    desired_order = weightage_wise_data_nifty_50_stocks['STOCK SYMBOL'].unique()
    Pre_market_data['SYMBOL \n'] = Pre_market_data['SYMBOL \n'].astype('category')
    Pre_market_data['SYMBOL \n'].cat.set_categories(desired_order, inplace=True)
    Pre_market_data = Pre_market_data.sort_values('SYMBOL \n')
    Pre_market_data = Pre_market_data.reset_index(drop=True)
    Pre_market_final_file=pd.concat([Pre_market_data['SYMBOL \n'], Pre_market_data['%CHNG \n'], Pre_market_data['VALUE '],weightage_wise_data_nifty_50_stocks['WEIGHTAGE']], axis=1)
    Pre_market_final_file['%CHNG \n']=Pre_market_final_file['%CHNG \n'].replace('-', 0)
    Pre_market_final_file['%CHNG \n']=Pre_market_final_file['%CHNG \n'].astype(float)
    weightage_wise_change=(Pre_market_final_file["WEIGHTAGE"]*Pre_market_final_file["%CHNG \n"])/100
    Pre_market_final_file=pd.concat([Pre_market_final_file, pd.DataFrame(weightage_wise_change)], axis=1)
    Pre_market_final_file = Pre_market_final_file.rename(columns={0: "weightage_wise_change"})
    xx=Pre_market_final_file["weightage_wise_change"].sum()
    xx=float(xx)
    previous_day_closing_price=closing_price
    Predicted_open_price_of_Nifty=previous_day_closing_price+((xx*previous_day_closing_price)/100)
    Predicted_open_price_of_Nifty=round(Predicted_open_price_of_Nifty,2)
    return Predicted_open_price_of_Nifty,xx


previous_day_closing_price=19646.05
nifty_price,percentage=pre_market(previous_day_closing_price,"weightage_wise_Nifty_50_Stocks.xlsx","MW-Pre-Open-Market-31-Jul-2023.csv")

if percentage>0:
    print(f"Market is expected to gap up by {percentage}% at the opening price of: {nifty_price}")
else:
    print(f"Market is expected to gap down by {percentage}% at the opening price of: {nifty_price}")