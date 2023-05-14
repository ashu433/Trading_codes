import OI_sentiment_Estimator
import pandas as pd


file_1="fii_stats_12-May-2023.xls"
file_2="fao_participant_oi_12052023.csv"
nifty_closing_price=18314.8
Bank_nifty_closing_price=43793.55
date="12-May-2023"

path="D:/ashu/Finance/algo_trading/images/"

Fii_statsics=OI_sentiment_Estimator.FII_Stastics(file_1)

future_data,Option_data,Big_Institution_data_futures,Big_Institution_data_option,over_all_f_o=OI_sentiment_Estimator.Participant_wise_Future_Option(file_2)

# OI_sentiment_Estimator.final_file_generation_future(Big_Institution_data_futures,nifty_closing_price,Bank_nifty_closing_price,date)
# OI_sentiment_Estimator.final_file_generation_Options(Big_Institution_data_option,nifty_closing_price,Bank_nifty_closing_price,date)

futures=pd.read_csv("Final_1_file.csv")
Options=pd.read_csv("Final_1_file_Options.csv")

OI_sentiment_Estimator.over_all_OI_buildup_Options(Options)
OI_sentiment_Estimator.over_all_OI_buildup_futures(futures)

OI_sentiment_Estimator.image_saving(future_data,Option_data)
OI_sentiment_Estimator.FII_data_analysis(Fii_statsics)

Fii_statsics.to_csv(path+"FII_stats.csv",index=False)
future_data.to_csv(path+"Participant_Futures.csv",index=False)
Option_data.to_csv(path+"Participant_Option.csv",index=False)
Big_Institution_data_futures.to_csv(path+"Big_Institution_data_futures.csv",index=False)
Big_Institution_data_option.to_csv(path+"Big_Institution_data_option.csv",index=False)

xox=OI_sentiment_Estimator.Comparision_between_FII_stats_report_participants_report(Fii_statsics,over_all_f_o)

print(xox)