import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def FII_Stastics(File_name):
    FII_stats=pd.read_excel(File_name)
    FII_stats.columns=FII_stats.iloc[0]
    FII_stats=FII_stats.drop(0)
    FII_stats.fillna(value=0,inplace=True)
    FII_stats.columns = FII_stats.columns + '_' + FII_stats.iloc[0].astype(str)
    FII_stats = FII_stats.iloc[1:]
    FII_stats = FII_stats.iloc[:, :-1]
    FII_stats = FII_stats.rename(columns={np.nan: 'TempName'})
    FII_stats = FII_stats.rename(columns={'TempName': 'FII'})
    statstics_data_FII=FII_stats[["FII","BUY_No. of contracts","SELL_No. of contracts","OPEN INTEREST AT THE END OF THE DAY_No. of contracts"]]
    Total_contracts=statstics_data_FII['BUY_No. of contracts'].astype(int) + statstics_data_FII['SELL_No. of contracts'].astype(int)
    new_statstics_data_FII=pd.concat([statstics_data_FII,pd.DataFrame(Total_contracts)],axis=1)
    new_statstics_data_FII=new_statstics_data_FII.rename(columns={0:"Total_Contracts"})
    new_statstics_data_FII = new_statstics_data_FII.rename(columns={'OPEN INTEREST AT THE END OF THE DAY_No. of contracts': 'OPEN INTEREST AT THE END OF THE DAY'})
    return new_statstics_data_FII


def Participant_wise_Future_Option(File_name):
    participant_wise_data=pd.read_csv(File_name)
    participant_wise_data.columns = participant_wise_data.iloc[0]
    participant_wise_data=participant_wise_data.drop(0)
    participant_wise_data=participant_wise_data.dropna(axis=1)
    f_o_data_index=participant_wise_data[["Client Type","Future Index Long","Future Index Short","Option Index Call Long","Option Index Call Short","Option Index Put Long","Option Index Put Short"]]
    future_oi=f_o_data_index['Future Index Long'].astype(int)+f_o_data_index['Future Index Short'].astype(int)
    Option_oi=f_o_data_index['Option Index Call Long'].astype(int)+f_o_data_index['Option Index Call Short'].astype(int)+f_o_data_index['Option Index Put Long'].astype(int)+f_o_data_index['Option Index Put Short'].astype(int)
    new_f_o_data_index=pd.concat([f_o_data_index,pd.DataFrame(future_oi)],axis=1)
    new_f_o_data_index=new_f_o_data_index.rename(columns={0:"Total_Future_OI"})
    new_f_o_data_index=pd.concat([new_f_o_data_index,pd.DataFrame(Option_oi)],axis=1)
    new_f_o_data_index=new_f_o_data_index.rename(columns={0:"Total_Option_OI"})

    ####################### Future data processing ##################################################

    future_data=new_f_o_data_index[["Client Type","Future Index Long","Future Index Short","Total_Future_OI"]]
    percentage_long=(future_data["Future Index Long"].astype(float)/future_data["Total_Future_OI"].astype(float))*100
    percentage_short=(future_data["Future Index Short"].astype(float)/future_data["Total_Future_OI"].astype(float))*100
    total_long_absolute=future_data["Future Index Long"].astype(float)-future_data["Future Index Short"].astype(float)
    future_data=pd.concat([future_data,pd.DataFrame(percentage_long)],axis=1)
    future_data=future_data.rename(columns={0:"percentage_long"})
    future_data=pd.concat([future_data,pd.DataFrame(percentage_short)],axis=1)
    future_data=future_data.rename(columns={0:"percentage_short"})
    future_data=pd.concat([future_data,pd.DataFrame(total_long_absolute)],axis=1)
    future_data=future_data.rename(columns={0:"total_long_absolute"})
    future_data = future_data.drop(future_data.index[-1])
    Long_vs_Short=future_data['Future Index Long'].astype(float)/future_data['Future Index Short'].astype(float)
    future_data=pd.concat([future_data,pd.DataFrame(Long_vs_Short)],axis=1)
    future_data=future_data.rename(columns={0:"Long_vs_Short"})

    ############## Options ######################################

    Option_data=new_f_o_data_index[["Client Type","Option Index Call Long","Option Index Call Short","Option Index Put Long","Option Index Put Short","Total_Option_OI"]]
    total_long_Option=Option_data["Option Index Call Long"].astype(float)+Option_data["Option Index Put Short"].astype(float)
    total_short_Option=Option_data["Option Index Call Short"].astype(float)+Option_data["Option Index Put Long"].astype(float)
    percentage_long_option=(total_long_Option/Option_data["Total_Option_OI"].astype(float))*100
    percentage_short_option=(total_short_Option/Option_data["Total_Option_OI"].astype(float))*100
    net_long=total_long_Option-total_short_Option
    Option_data=pd.concat([Option_data,pd.DataFrame(total_long_Option)],axis=1)
    Option_data=Option_data.rename(columns={0:"total_long_Option"})
    Option_data=pd.concat([Option_data,pd.DataFrame(total_short_Option)],axis=1)
    Option_data=Option_data.rename(columns={0:"total_short_Option"})
    Option_data=pd.concat([Option_data,pd.DataFrame(percentage_long_option)],axis=1)
    Option_data=Option_data.rename(columns={0:"percentage_long_option"})
    Option_data=pd.concat([Option_data,pd.DataFrame(percentage_short_option)],axis=1)
    Option_data=Option_data.rename(columns={0:"percentage_short_option"})
    Option_data=pd.concat([Option_data,pd.DataFrame(net_long)],axis=1)
    Option_data=Option_data.rename(columns={0:"net_long"})
    Option_data = Option_data.drop(Option_data.index[-1])
    Long_vs_Short_options=Option_data['total_long_Option'].astype(float)/Option_data['total_short_Option'].astype(float)
    Option_data=pd.concat([Option_data,pd.DataFrame(Long_vs_Short_options)],axis=1)
    Option_data=Option_data.rename(columns={0:"Long_vs_Short"})
    Big_Institution_data_futures = future_data.drop(index=1)
    Big_Institution_data_option = Option_data.drop(index=1)
    return future_data,Option_data,Big_Institution_data_futures,Big_Institution_data_option,new_f_o_data_index

def FII_data_analysis(file_name):
    path="D:/ashu/Finance/algo_trading/images/"
    new_statstics_data_FII=file_name
    FII_activity_in_futures=(float(new_statstics_data_FII.iloc[0,3])/(float(new_statstics_data_FII.iloc[0,3])+float(new_statstics_data_FII.iloc[6,3])))*100
    FII_activity_in_options=(float(new_statstics_data_FII.iloc[6,3])/(float(new_statstics_data_FII.iloc[0,3])+float(new_statstics_data_FII.iloc[6,3])))*100
    FII_activity_in_futures_nifty=(float(new_statstics_data_FII.iloc[4,3])/float(new_statstics_data_FII.iloc[0,3]))*100
    FII_activity_in_futures_bank_nifty=(float(new_statstics_data_FII.iloc[2,3])/float(new_statstics_data_FII.iloc[0,3]))*100
    FII_activity_in_option_nifty=(float(new_statstics_data_FII.iloc[7,3])/float(new_statstics_data_FII.iloc[6,3]))*100
    FII_activity_in_option_bank_nifty=(float(new_statstics_data_FII.iloc[10,3])/float(new_statstics_data_FII.iloc[6,3]))*100
    data = {'Future': [FII_activity_in_futures],
            'Options': [FII_activity_in_options]}
    df=pd.DataFrame(data)
    ax=df.plot.bar()
    for i, bar in enumerate(ax.containers):
        ax.bar_label(bar, label_type='edge', fontsize=10)
    ax.set_xlabel('Future and Options')
    ax.set_ylabel('% share in each instrument')
    ax.set_title('Micro and Macro sentiment of the FII')
    plt.savefig(path+"Micro and Macro sentiment of the FII.png")

    data_index = {'Nifty Future': [FII_activity_in_futures_nifty],'Bank Nifty Future': [FII_activity_in_futures_bank_nifty],'Nifty Options': [FII_activity_in_option_nifty],'Bank Nifty Options': [FII_activity_in_option_bank_nifty]}
    df_index=pd.DataFrame(data_index)

    ax=df_index.plot.bar()
    for i, bar in enumerate(ax.containers):
        ax.bar_label(bar, label_type='edge', fontsize=10)
    ax.set_xlabel('Index')
    ax.set_ylabel('% share in each index')
    ax.set_title('FII_Index_share_in_each_instrument')
    plt.savefig(path+"FII Index share in each instrument.png")




def image_saving(future_file,option_file):

    ######################## Futures images ################################################
    path="D:/ashu/Finance/algo_trading/images/"

    future_file.plot(kind='pie', y="Total_Future_OI", labels=future_file['Client Type'], autopct='%1.1f%%')
    plt.title('Total Open Interest of the different participants in Futures')
    plt.axis('equal')
    plt.savefig(path+"Total_Open_Interest_of_the_different_participants_Futures.png")

    future_file["Future Index Long"]=future_file["Future Index Long"].astype(int)
    future_file.plot(kind='pie', y="Future Index Long", labels=future_file['Client Type'], autopct='%1.1f%%')
    plt.title('Total Long Pogition in Futures')
    plt.axis('equal')
    plt.savefig(path+"Total_Long_Pogition_in_Futures.png")

    future_file["Future Index Short"]=future_file["Future Index Short"].astype(int)
    future_file.plot(kind='pie', y="Future Index Short", labels=future_file['Client Type'], autopct='%1.1f%%')
    plt.title('Total Short Pogition in Futures')
    plt.axis('equal')
    plt.savefig(path+"Total_Short_Pogition_in_Futures.png")

    long_short=future_file[["percentage_long","percentage_short"]]
    long_short=long_short.round(2)
    long_short.set_index(future_file["Client Type"], inplace=True)
    ax = long_short.plot(kind='bar',color=['green', 'red'], edgecolor='black')
    for i, bar in enumerate(ax.containers):
        ax.bar_label(bar, label_type='edge', fontsize=10)
    ax.legend(['Long','Short'])
    fig = plt.gcf()
    fig.set_size_inches(8, 8)
    plt.ylabel("Percentage")
    plt.title("% long and short of the each Participants OI in Futures")

    plt.savefig(path+"%_long_and_short_of_the_each_Participants_OI_in_Futures.png")
    
    Big_Institution_data_futures = future_file.drop(index=1)
    Big_Institution_data_futures.plot(kind='pie', y="Future Index Long", labels=Big_Institution_data_futures['Client Type'], autopct='%1.1f%%')
    plt.title('Total Long Pogition of big clients in Futures')
    plt.axis('equal')

    plt.savefig(path+"Total_Long_Pogition_of_big_clients_Futures.png")

    Big_Institution_data_futures.plot(kind='pie', y="Future Index Short", labels=Big_Institution_data_futures['Client Type'], autopct='%1.1f%%')
    plt.title('Total Shot Pogition of big clients in Futures')
    plt.axis('equal')
    plt.savefig(path+"Total_Shot_Pogition_of_big_clients_Futures.png")

    ######################## Options Images ########################################

    option_file.plot(kind='pie', y="Total_Option_OI", labels=option_file['Client Type'], autopct='%1.1f%%')
    plt.title('Total Open Interest of the different participants in Options')
    plt.axis('equal')
    plt.savefig(path+"Total_Open_Interest_of_the_different_participants_Options.png")

    option_file["total_short_Option"]=option_file["total_short_Option"].astype(int)
    option_file.plot(kind='pie', y="total_short_Option", labels=option_file['Client Type'], autopct='%1.1f%%')
    plt.title('Total Short Pogitions of the different participants in Options')
    plt.axis('equal')
    plt.savefig(path+"Total_Short_Pogition_in_Options.png")

    Big_Institution_data = option_file.drop(index=1)
    Big_Institution_data.plot(kind='pie', y="total_short_Option", labels=Big_Institution_data['Client Type'], autopct='%1.1f%%')
    plt.title('Total Shot Pogition of big clients in Options')
    plt.axis('equal')
    plt.savefig(path+"Total_Shot_Pogition_of_big_clients_Options.png")

    Big_Institution_data.plot(kind='pie', y="total_long_Option", labels=Big_Institution_data['Client Type'], autopct='%1.1f%%')
    plt.title('Total Long Pogition of big clients in Options')
    plt.axis('equal')
    plt.savefig(path+"Total_Long_Pogition_of_big_clients_Options.png")

    option_file["total_long_Option"]=option_file["total_long_Option"].astype(int)
    option_file.plot(kind='pie', y="total_long_Option", labels=option_file['Client Type'], autopct='%1.1f%%')
    plt.title('Total Long pogitions of the different participants in Options')
    plt.axis('equal')
    plt.savefig(path+"Total_Long_pogition_of_different_participants_Options.png")

    long_short=option_file[["percentage_long_option","percentage_short_option"]]
    long_short=long_short.round(2)
    long_short.set_index(option_file["Client Type"], inplace=True)
    ax = long_short.plot(kind='bar',color=['green', 'red'], edgecolor='black')
    for i, bar in enumerate(ax.containers):
        ax.bar_label(bar, label_type='edge', fontsize=10)
    ax.legend(['Long','Short'])
    fig = plt.gcf()
    fig.set_size_inches(6, 6)
    plt.ylabel("Percentage")
    plt.title("% long and short of the each Participants OI in Options")
    plt.savefig(path+"%_long_and_short_of_the_each_Participants_OI_in_Options.png")


# def final_file_generation_future(Big_inititution_futures,closing_price_nifty,closing_price_Bank_nifty,date):
#     ####################################### Future data analysis ####################################
#     Big_Institution_data_futures=Big_inititution_futures
#     Date=date
#     close_nifty=closing_price_nifty
#     close_bank_nifty=closing_price_Bank_nifty
#     new_data=Big_Institution_data_futures[["Client Type","total_long_absolute"]]
#     xox=new_data.T
#     xox.columns=xox.iloc[0]
#     xox=xox.drop("Client Type")
#     xox=xox.rename({'Client Type': 'Date', 'total_long_absolute': Date})
#     xox = xox.rename(columns={'Client Type': 'Date'})
#     xox.insert(loc=0, column='Date', value=Date)
#     # final_file=pd.concat([data_2, xox], axis=0)
#     final_file=xox
#     final_file.to_csv('Sentiment_Estimator.csv', mode='a', header=False, index=False)
#     data_2=pd.read_csv("Sentiment_Estimator.csv")
#     mom=data_2.shape
#     pop=mom[0]
#     tot=data_2.iloc[pop-1,1:]-data_2.iloc[pop-2,1:]
#     tot=pd.DataFrame(tot)
#     tot=tot.T
#     tot = tot.rename(columns={'DII': 'Change in OI in DII','FII': 'Change in OI in FII','Pro': 'Change in OI in Pro'})
#     tot=tot.rename({0: pop-1})
#     new_data_1=pd.concat([data_2.iloc[:pop-1],tot],axis=1)
#     new_data_1.fillna(0,inplace=True)
#     new_data_1=pd.DataFrame(new_data_1.iloc[pop-1])
#     new_data_1=new_data_1.T
#     new_data_1.iloc[0,0]=Date
#     new_data_1.iloc[0,1]=data_2.iloc[pop-1,1]
#     new_data_1.iloc[0,2]=data_2.iloc[pop-1,2]
#     new_data_1.iloc[0,3]=data_2.iloc[pop-1,3]
#     new_data_frame=pd.DataFrame({'Closing price of the nifty': [close_nifty], 'Closing price of the Bank nifty': [close_bank_nifty]})
#     new_data_frame = new_data_frame.rename(index={0:pop-1})
#     new_data_1=pd.concat([new_data_1,new_data_frame],axis=1)
#     new_data_1.to_csv('Final_1_file.csv', mode='a', header=False, index=False)

# def final_file_generation_Options(Big_inititution_Options,closing_price_nifty,closing_price_Bank_nifty,date):

#     Big_Institution_data=Big_inititution_Options
#     Date=date
#     close_nifty=closing_price_nifty
#     close_bank_nifty=closing_price_Bank_nifty

#     new_data=Big_Institution_data[["Client Type","net_long"]]
#     xox=new_data.T
#     xox.columns=xox.iloc[0]
#     xox=xox.drop("Client Type")
#     xox=xox.rename({'net_long': Date})
#     xox.insert(loc=0, column='Date', value=Date)
#     # # final_file=pd.concat([data_2, xox], axis=0)
#     final_file=xox
#     final_file.to_csv('Sentiment_Estimator_Options.csv', mode='a', header=False, index=False)
#     data_2=pd.read_csv("Sentiment_Estimator_Options.csv")
#     mom=data_2.shape
#     pop=mom[0]
#     tot=data_2.iloc[pop-1,1:]-data_2.iloc[pop-2,1:]
#     tot=pd.DataFrame(tot)
#     tot=tot.T
#     tot = tot.rename(columns={'DII': 'Change in OI in DII','FII': 'Change in OI in FII','Pro': 'Change in OI in Pro'})
#     tot=tot.rename({0: pop-1})
#     new_data_1=pd.concat([data_2.iloc[:pop-1],tot],axis=1)
#     new_data_1.fillna(0,inplace=True)
#     new_data_1=pd.DataFrame(new_data_1.iloc[pop-1])
#     new_data_1=new_data_1.T
#     new_data_1.iloc[0,0]=Date
#     new_data_1.iloc[0,1]=data_2.iloc[pop-1,1]
#     new_data_1.iloc[0,2]=data_2.iloc[pop-1,2]
#     new_data_1.iloc[0,3]=data_2.iloc[pop-1,3]
#     new_data_frame=pd.DataFrame({'Closing price of the nifty': [close_nifty], 'Closing price of the Bank nifty': [close_bank_nifty]})
#     new_data_frame = new_data_frame.rename(index={0:pop-1})
#     new_data_1=pd.concat([new_data_1,new_data_frame],axis=1)
#     new_data_1.to_csv('Final_1_file_Options.csv', mode='a', header=False, index=False)


# def over_all_OI_buildup_futures(futures):

#     path="D:/ashu/Finance/algo_trading/images/"
#     futures=futures

#     Change_in_OI_Futures=futures[["Change in OI in DII","Change in OI in FII","Change in OI in Pro"]]
#     Change_in_OI_Futures.set_index(futures["Date"], inplace=True)
#     ax = Change_in_OI_Futures.plot(kind='bar',color=['green', 'red',"blue"], edgecolor='black')
#     for i, bar in enumerate(ax.containers):
#         ax.bar_label(bar, label_type='edge', fontsize=10)

#     ax2 = ax.twinx()
#     ax2.plot(futures['Date'], futures['Closing price of the nifty'], color='Black', marker='o')
#     ax2.set_ylabel('Closing price')
#     ax2.legend("Closing Price",loc='upper left')



#     ax.legend(['Change in OI in DII','Change in OI in FII','Change in OI in Pro'])
#     fig = plt.gcf()
#     fig.set_size_inches(10, 10)
#     plt.ylabel("Change in OI")
#     plt.title("Change in Futures OI and Nifty 50 Closing Price")
#     plt.savefig(path+"Change_in_Futures_OI_and_Nifty_50_Closing_Price.png")

#     overall_long_pogition=futures["Change in OI in DII"]+futures["Change in OI in FII"]+futures["Change in OI in Pro"]
#     futures=pd.concat([futures,pd.DataFrame(overall_long_pogition)],axis=1)
#     futures=futures.rename(columns={0:"overall_long_pogition"})

#     Over_all_long_pogitions=futures[['overall_long_pogition']]
#     Over_all_long_pogitions.set_index(futures["Date"], inplace=True)
#     ax11 = Over_all_long_pogitions.plot(kind='bar',color='blue', alpha=0.5, edgecolor='black')
#     for i, bar in enumerate(ax11.containers):
#         ax11.bar_label(bar, label_type='edge', fontsize=10)

#     ax2 = ax11.twinx()
#     ax2.plot(futures['Date'], futures['Closing price of the nifty'], color='Black', marker='o')
#     ax2.set_ylabel('Closing price')
#     ax2.legend("Closing Price",loc='upper left')



#     ax11.legend(['Over all long pogitions'])
#     fig = plt.gcf()
#     fig.set_size_inches(10, 10)
#     plt.ylabel("Change in OI")
#     plt.title("Over all Change in Futures OI and Nifty 50 Closing Price")
#     plt.savefig(path+"Over_all_Change_in_Futures_OI_and_Nifty_50_Closing_Price.png")

#     ##################################### Net OI Build up Futures ##############################################

#     Net_OI_Build_up_futures=futures[["DII","FII","Pro"]]
#     Net_OI_Build_up_futures.set_index(futures["Date"], inplace=True)
#     ax = Net_OI_Build_up_futures.plot(kind='bar',color=['green', 'red',"blue"], edgecolor='black')
#     for i, bar in enumerate(ax.containers):
#         ax.bar_label(bar, label_type='edge', fontsize=10)

#     ax.legend(['DII','FII','Pro'])
#     fig = plt.gcf()
#     fig.set_size_inches(10, 10)
#     plt.ylabel("Net OI Build Up")
#     plt.title("Net OI build up of the different participants in Futures")
#     plt.savefig(path+"Net_OI_build_up_of_the_different_participants_in_Futures.png")


# def over_all_OI_buildup_Options(Options):
#     path="D:/ashu/Finance/algo_trading/images/"
#     Options=Options
#     Change_in_OI_Options=Options[["Change in OI in DII","Change in OI in FII","Change in OI in Pro"]]
#     Change_in_OI_Options.set_index(Options["Date"], inplace=True)
#     ax = Change_in_OI_Options.plot(kind='bar',color=['green', 'red',"blue"], edgecolor='black')
#     for i, bar in enumerate(ax.containers):
#         ax.bar_label(bar, label_type='edge', fontsize=10)

#     ax2 = ax.twinx()
#     ax2.plot(Options['Date'], Options['Closing price of the nifty'], color='Black', marker='o')
#     ax2.set_ylabel('Closing price')
#     ax2.legend("Closing Price",loc='upper left')



#     ax.legend(['Change in OI in DII','Change in OI in FII','Change in OI in Pro'])
#     fig = plt.gcf()
#     fig.set_size_inches(10, 10)
#     plt.ylabel("Change in OI")
#     plt.title("Change in Options OI and Nifty 50 Closing Price Options")
#     plt.savefig(path+"Change_in_Options_OI_and_Nifty_50_Closing_Price.png")

#     overall_long_pogition_Options=Options["Change in OI in DII"]+Options["Change in OI in FII"]+Options["Change in OI in Pro"]
#     Options=pd.concat([Options,pd.DataFrame(overall_long_pogition_Options)],axis=1)
#     Options=Options.rename(columns={0:"overall_long_pogition"})

#     Over_all_long_pogitions=Options[['overall_long_pogition']]
#     Over_all_long_pogitions.set_index(Options["Date"], inplace=True)
#     ax11 = Over_all_long_pogitions.plot(kind='bar',color='blue', alpha=0.5, edgecolor='black')
#     for i, bar in enumerate(ax11.containers):
#         ax11.bar_label(bar, label_type='edge', fontsize=10)

#     ax2 = ax11.twinx()
#     ax2.plot(Options['Date'], Options['Closing price of the nifty'], color='Black', marker='o')
#     ax2.set_ylabel('Closing price')
#     ax2.legend("Closing Price",loc='upper left')



#     ax11.legend(['Over all long pogitions'])
#     fig = plt.gcf()
#     fig.set_size_inches(10, 10)
#     plt.ylabel("Change in OI")
#     plt.title("Change in Options OI and Nifty 50 Closing Price")

#     plt.savefig(path+"Over_all_Change_in_Options_OI_and_Nifty_50_Closing_Price.png")

#     ############################### Net OI Build UP Options##############################################

#     Net_OI_Build_up=Options[["DII","FII","Pro"]]
#     Net_OI_Build_up.set_index(Options["Date"], inplace=True)
#     ax = Net_OI_Build_up.plot(kind='bar',color=['green', 'red',"blue"], edgecolor='black')
#     for i, bar in enumerate(ax.containers):
#         ax.bar_label(bar, label_type='edge', fontsize=10)

#     ax.legend(['DII','FII','Pro'])
#     fig = plt.gcf()
#     fig.set_size_inches(10, 10)
#     plt.ylabel("Net OI Build Up")
#     plt.title("Net OI build up of the different participants in Options")
    
#     plt.savefig(path+"Net_OI_build_up_of_the_different_participants_in_Options.png")

def Comparision_between_FII_stats_report_participants_report(Fii_data_stats_report,Overall_f_o_data):
    new_statstics_data_FII=Fii_data_stats_report
    new_f_o_data_index=Overall_f_o_data
    FII_future_statics_report=new_statstics_data_FII.iloc[0,3]
    FII_option_statics_report=new_statstics_data_FII.iloc[6,3]
    # FII_future_contract_statics_report=new_statstics_data_FII.iloc[0,4]
    # FII_option_contract_statics_report=new_statstics_data_FII.iloc[6,4]
    FII_future_participant_wise_report=new_f_o_data_index.iloc[2,7]
    FII_option_participant_wise_report=new_f_o_data_index.iloc[2,8]
    # FII_volume_future_participant_wise_report=new_f_o_volume_data_index.iloc[2,7]
    # FII_volume_option_participant_wise_report=new_f_o_volume_data_index.iloc[2,8]
    x=float(FII_future_participant_wise_report)/float(FII_future_statics_report)
    y=float(FII_option_participant_wise_report)/float(FII_option_statics_report)
    # z=float(FII_volume_future_participant_wise_report)/float(FII_future_contract_statics_report)
    # m=float(FII_volume_option_participant_wise_report)/float(FII_option_contract_statics_report)
    data = {'Future_OI': [x], 'Option_OI': [y]}
    df = pd.DataFrame(data)
    return df


def final_future_file(Participant_wise_report_future,Date,Nifty_closing_price):
    Future=pd.read_csv(Participant_wise_report_future)
    Date=Date
    Nifty_closing_price=Nifty_closing_price

    defired_future_data=Future[["Future Index Long","Future Index Short","total_long_absolute"]]
    defired_future_data=defired_future_data.T

    data_array = defired_future_data.to_numpy().reshape(1, -1)
    reshaped_data = np.reshape(data_array, (1, 12))
    new_df = pd.DataFrame(reshaped_data)
    new_column_names = {0: 'Client Long', 1: 'DII Long',2: 'FII Long', 3: 'Pro Long',4: 'Client Short', 5: 'DII Short',6: 'FII Short', 7: 'Pro Short', 8: 'Net Long Client',9: 'Net Long DII', 10: 'Net Long FII', 11: 'Net Long Pro'}
    new_df.rename(columns=new_column_names, inplace=True)
    new_df.insert(loc=0, column="Date", value=Date)

    Future_data=pd.read_csv("Sentiment_Futures.csv")
    final_data= pd.concat([Future_data, new_df], axis=0)
    final_data.to_csv("Sentiment_Futures.csv",index=False)

    num_rows=final_data.shape[0]
    x=num_rows
    Futures_data_ROC=final_data.iloc[x-1,1:]-final_data.iloc[x-2,1:]
    Futures_data_ROC=pd.DataFrame(Futures_data_ROC)
    Futures_data_ROC=Futures_data_ROC.T
    Futures_data_ROC.insert(loc=0, column="Date", value=Date)
    Futures_data_ROC.insert(loc=1, column="Nifty Closing Price", value=Nifty_closing_price)
    new_column_names_ROC = {"Client Long": 'Client Long ROC', "DII Long": 'DII Long ROC',"FII Long": 'FII Long ROC', "Pro Long": 'Pro Long ROC',"Client Short": 'Client Short ROC', "DII Short": 'DII Short ROC',"FII Short": 'FII Short ROC', "Pro Short": 'Pro Short ROC', "Net Long Client": 'Net Long Client ROC',"Net Long DII": 'Net Long DII ROC', "Net Long FII": 'Net Long FII ROC', "Net Long Pro": 'Net Long Pro ROC'}
    Futures_data_ROC.rename(columns=new_column_names_ROC, inplace=True)

    Future_roc_past=pd.read_csv("Futures_data_ROC.csv")
    Futures_data_ROC_final= pd.concat([Future_roc_past, Futures_data_ROC], axis=0)
    Futures_data_ROC_final.to_csv("Futures_data_ROC.csv",index=False)


def final_Option_file(Participant_wise_report_Option,Date,Nifty_closing_price):
    Option=pd.read_csv(Participant_wise_report_Option)
    Date=Date
    Nifty_closing_price=Nifty_closing_price

    defired_Option_data=Option[["Option Index Call Short","Option Index Put Short","Option Index Call Long","Option Index Put Long","net_long"]]
    defired_Option_data=defired_Option_data.T

    data_array = defired_Option_data.to_numpy().reshape(1, -1)
    reshaped_data = np.reshape(data_array, (1, 20))
    new_df = pd.DataFrame(reshaped_data)
    new_column_names = {0: 'Client Call Short', 1: 'DII Call Short',2: 'FII Call Short', 3: 'Pro Call Short',4: 'Client Put Short', 5: 'DII Put Short',6: 'FII Put Short', 7: 'Pro Put Short', 8: 'Client Call Long', 9: 'DII Call Long',10: 'FII Call Long', 11: 'Pro Call Long',12: 'Client Put Long', 13: 'DII Put Long',14: 'FII Put Long', 15: 'Pro Put Long',16: 'Client Net long', 17: 'DII Net long',18: 'FII Net long', 19: 'Pro Net long'}
    new_df.rename(columns=new_column_names, inplace=True)
    new_df.insert(loc=0, column="Date", value=Date)

    Option_data=pd.read_csv("Sentiment_Options.csv")
    final_data= pd.concat([Option_data, new_df], axis=0)
    final_data.to_csv("Sentiment_Options.csv",index=False)

    num_rows=final_data.shape[0]
    x=num_rows
    Options_data_ROC=final_data.iloc[x-1,1:]-final_data.iloc[x-2,1:]
    Options_data_ROC=pd.DataFrame(Options_data_ROC)
    Options_data_ROC=Options_data_ROC.T
    Options_data_ROC.insert(loc=0, column="Date", value=Date)
    Options_data_ROC.insert(loc=1, column="Nifty Closing Price", value=Nifty_closing_price)
    new_column_names_ROC = {"Client Call Short": 'Client Call Short ROC', "DII Call Short": 'DII Call Short ROC',"FII Call Short": 'FII Call Short ROC', "Pro Call Short": 'Pro Call Short ROC',"Client Put Short": 'Client Put Short ROC', "DII Put Short": 'DII Put Short ROC',"FII Put Short": 'FII Put Short ROC', "Pro Put Short": 'Pro Put Short ROC', "Client Call Long": 'Client Call Long ROC', "DII Call Long": 'DII Call Long ROC',"FII Call Long": 'FII Call Long ROC', "Pro Call Long": 'Pro Call Long ROC',"Client Put Long": 'Client Put Long ROC', "DII Put Long": 'DII Put Long ROC',"FII Put Long": 'FII Put Long ROC', "Pro Put Long": 'Pro Put Long ROC'}
    Options_data_ROC.rename(columns=new_column_names_ROC, inplace=True)

    Option_roc_past=pd.read_csv("Options_data_ROC.csv")
    Option_data_ROC_final= pd.concat([Option_roc_past, Options_data_ROC], axis=0)
    Option_data_ROC_final.to_csv("Options_data_ROC.csv",index=False)

if __name__=='__main__':  
    pass