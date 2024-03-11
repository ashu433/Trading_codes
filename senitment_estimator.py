import OI_sentiment_Estimator
import pandas as pd
import ppt_generation_participants

#################################################################################################
#################################################################################################
#################################################################################################
###################### Inputs to append #########################################################
#################################################################################################
#################################################################################################
#################################################################################################

def sentiment_participants(day,month_in_words,month_in_numbers,year,Nifty_closing_price,month_file):
    day=day
    month=month_in_words
    month_file=month_file
    month_in_numbers=month_in_numbers
    year=year
    pick_up_path=f"D:/ashu/Finance/EOD_derivative_cash_data/{month}_{year}/{day}_{month_in_numbers}_{year}/"
    file_1=pick_up_path+f"fii_stats_{day}-{month_file}-{year}.xls"
    file_2=pick_up_path+f"fao_participant_oi_{day}{month_in_numbers}{year}.csv"
    nifty_closing_price=Nifty_closing_price
    date=f"{day}-{month}-{year}"
    path="D:/ashu/Finance/algo_trading/images/"

    #################################################################################################
    #################################################################################################
    #################################################################################################
    ###################### All CSV File generation code that to be put in ppt #######################
    #################################################################################################
    #################################################################################################
    #################################################################################################


    ##FII STATICS 

    Fii_statsics=OI_sentiment_Estimator.FII_Stastics(file_1)
    OI_sentiment_Estimator.FII_data_analysis(Fii_statsics)

    # Overall Participant wise Futures and Options dataframes generation

    future_data,Option_data,Big_Institution_data_futures,Big_Institution_data_option,over_all_f_o=OI_sentiment_Estimator.Participant_wise_Future_Option(file_2)

    # Image saving

    OI_sentiment_Estimator.image_saving(future_data,Option_data)


    # Dataframe to csv file generation


    Fii_statsics.to_csv(path+"FII_stats.csv",index=False)
    future_data.to_csv(path+"Participant_Futures.csv",index=False)
    Option_data.to_csv(path+"Participant_Option.csv",index=False)
    Big_Institution_data_futures.to_csv(path+"Big_Institution_data_futures.csv",index=False)
    Big_Institution_data_option.to_csv(path+"Big_Institution_data_option.csv",index=False)

    xox=OI_sentiment_Estimator.Comparision_between_FII_stats_report_participants_report(Fii_statsics,over_all_f_o)

    print(xox)

    #################################################################################################
    #################################################################################################
    #################################################################################################
    ###################### Final File generation code ###############################################
    #################################################################################################
    #################################################################################################
    #################################################################################################

    OI_sentiment_Estimator.final_future_file(path+"Participant_Futures.csv",date,nifty_closing_price)
    OI_sentiment_Estimator.final_Option_file(path+"Participant_Option.csv",date,nifty_closing_price)

    ppt_generation_participants.ppt_generation(date)