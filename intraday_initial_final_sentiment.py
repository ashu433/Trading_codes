import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

def start_of_the_day_sentiment_call(file,interval,distance,ATM_Init,ATM_End):
    file_2=pd.read_excel(file)
    interval = interval
    column_list = file_2['Time'][::interval].tolist()
    print(column_list)
    p=distance
    x=len(column_list)
    start_time=column_list[0]
    intial_test=column_list[p]
    initial_intraday_analysis_start=file_2[file_2['Time'] == start_time]
    initial_intraday_analysis_end=file_2[file_2['Time'] == intial_test]


    ATM_init=ATM_Init
    range=5
    ATM_max=ATM_init+range*50
    ATM_min=ATM_init-range*50

    ########################### Call side data cleaning ###############################################################

    Intraday_start_df = initial_intraday_analysis_start[(initial_intraday_analysis_start['strikePrice'] >= ATM_min) & (initial_intraday_analysis_start['strikePrice'] <= ATM_max)]
    largest_values = Intraday_start_df['CE_OI'].nlargest(3)
    filtered_df_start = Intraday_start_df[Intraday_start_df['CE_OI'].isin(largest_values)]
    print(filtered_df_start["strikePrice"])

    ATM_end=ATM_End
    range=5
    ATM_max=ATM_end+range*50
    ATM_min=ATM_end-range*50

    Intraday_start_end_df = initial_intraday_analysis_end[(initial_intraday_analysis_end['strikePrice'] >= ATM_min) & (initial_intraday_analysis_end['strikePrice'] <= ATM_max)]
    largest_values_end = Intraday_start_end_df['CE_OI'].nlargest(3)
    filtered_df_start_end = Intraday_start_end_df[Intraday_start_end_df['CE_OI'].isin(largest_values_end)]
    print(filtered_df_start_end["strikePrice"])

    unique_values = pd.concat([filtered_df_start_end['strikePrice'], filtered_df_start["strikePrice"]]).unique()
    new_df= pd.DataFrame({"strikePrice": unique_values})
    new_df= new_df.sort_values("strikePrice")
    x=new_df.size

    file_call_start=initial_intraday_analysis_start[(initial_intraday_analysis_start['strikePrice'] == new_df.iloc[0,0])]
    i=1

    while i<x:
        generated_row_call = initial_intraday_analysis_start[(initial_intraday_analysis_start['strikePrice'] == new_df.iloc[i,0])]
        file_call_start = pd.concat([file_call_start, generated_row_call], axis=0)
        i=i+1

    file_call_end=initial_intraday_analysis_end[(initial_intraday_analysis_end['strikePrice'] == new_df.iloc[0,0])]
    i=1

    while i<x:
        generated_row_call = initial_intraday_analysis_end[(initial_intraday_analysis_end['strikePrice'] == new_df.iloc[i,0])]
        file_call_end = pd.concat([file_call_end, generated_row_call], axis=0)
        i=i+1

    new_df_start_call= file_call_start.rename(columns={"CE_OI": "CE_OI_"+start_time,"CE_LTP": "CE_LTP_"+start_time})
    new_df_end_call= file_call_end.rename(columns={"CE_OI": "CE_OI_"+intial_test,"CE_LTP": "CE_LTP_"+intial_test})
    OI_data_initial_day_call=pd.concat([new_df_start_call["strikePrice"].reset_index(drop=True),new_df_start_call["CE_OI_"+start_time].reset_index(drop=True),new_df_end_call["CE_OI_"+intial_test].reset_index(drop=True),new_df_start_call["CE_LTP_"+start_time].reset_index(drop=True),new_df_end_call["CE_LTP_"+intial_test].reset_index(drop=True)], axis=1)

    OI_data_call = OI_data_initial_day_call[["CE_OI_"+start_time,"CE_OI_"+intial_test]]
    OI_data_call.set_index(OI_data_initial_day_call["strikePrice"], inplace=True)

    Premium_data_call=OI_data_initial_day_call[["CE_LTP_"+start_time,"CE_LTP_"+intial_test]]
    Premium_data_call.set_index(OI_data_initial_day_call["strikePrice"], inplace=True)

    #################################### Plotting for the call plots #################################################
 
    fig1 = plt.figure(1, figsize=(0,0))

    ax1 = OI_data_call.plot(kind='bar', color=['blue', 'red'], edgecolor='black')

    for container in ax1.containers:
        ax1.bar_label(container, label_type='edge', fontsize=10, color='black', padding=3)

    ax1.legend([start_time, intial_test])
    plt.xlabel('Strike Price')
    plt.ylabel('Maximum OI on Call side')
    plt.title('Maximum OI on the Call side VS strike price')

    fig2 = plt.figure(2, figsize=(8, 6))

    ax2 = Premium_data_call.plot(kind='bar', color=['blue', 'red'], edgecolor='black')

    for container in ax2.containers:
        ax2.bar_label(container, label_type='edge', fontsize=10, color='black', padding=3)

    ax2.legend([start_time, intial_test])
    plt.xlabel('Strike Price')
    plt.ylabel('Premium on Call side')
    plt.title('Premium on Call side VS strike price')

    plt.show()


def start_of_the_day_sentiment_put(file,interval,distance,ATM_Init,ATM_End):
    file_2=pd.read_excel(file)
    interval = interval
    column_list = file_2['Time'][::interval].tolist()
    print(column_list)
    p=distance
    x=len(column_list)
    start_time=column_list[0]
    intial_test=column_list[p]
    initial_intraday_analysis_start=file_2[file_2['Time'] == start_time]
    initial_intraday_analysis_end=file_2[file_2['Time'] == intial_test]
    ATM_init=ATM_Init
    range=5
    ATM_max=ATM_init+range*50
    ATM_min=ATM_init-range*50

    ########################### Put side data cleaning ###############################################################
    Intraday_start_df_PE = initial_intraday_analysis_start[(initial_intraday_analysis_start['strikePrice'] >= ATM_min) & (initial_intraday_analysis_start['strikePrice'] <= ATM_max)]
    largest_values_PE = Intraday_start_df_PE['PE_OI'].nlargest(3)
    filtered_df_start_PE = Intraday_start_df_PE[Intraday_start_df_PE['PE_OI'].isin(largest_values_PE)]
    print(filtered_df_start_PE['strikePrice'])


    ATM_end=ATM_End
    range=5
    ATM_max=ATM_end+range*50
    ATM_min=ATM_end-range*50


    Intraday_start_end_df_PE = initial_intraday_analysis_end[(initial_intraday_analysis_end['strikePrice'] >= ATM_min) & (initial_intraday_analysis_end['strikePrice'] <= ATM_max)]
    largest_values_end_PE = Intraday_start_end_df_PE['PE_OI'].nlargest(3)
    filtered_df_start_end_PE = Intraday_start_end_df_PE[Intraday_start_end_df_PE['PE_OI'].isin(largest_values_end_PE)]
    print(filtered_df_start_end_PE['strikePrice'])

    unique_values_PE = pd.concat([filtered_df_start_end_PE['strikePrice'], filtered_df_start_PE["strikePrice"]]).unique()
    new_df_PE= pd.DataFrame({"strikePrice": unique_values_PE})
    new_df_PE= new_df_PE.sort_values("strikePrice")
    x=new_df_PE.size
    print(new_df_PE["strikePrice"])

    file_put_start=initial_intraday_analysis_start[(initial_intraday_analysis_start['strikePrice'] == new_df_PE.iloc[0,0])]
    i=1

    while i<x:
        generated_row_put = initial_intraday_analysis_start[(initial_intraday_analysis_start['strikePrice'] == new_df_PE.iloc[i,0])]
        file_put_start = pd.concat([file_put_start, generated_row_put], axis=0)
        i=i+1

    file_put_end=initial_intraday_analysis_end[(initial_intraday_analysis_end['strikePrice'] == new_df_PE.iloc[0,0])]
    i=1

    while i<x:
        generated_row_put = initial_intraday_analysis_end[(initial_intraday_analysis_end['strikePrice'] == new_df_PE.iloc[i,0])]
        file_put_end = pd.concat([file_put_end, generated_row_put], axis=0)
        i=i+1

    new_df_start_put= file_put_start.rename(columns={"PE_OI": "PE_OI_"+start_time,"PE_LTP": "PE_LTP_"+start_time})
    new_df_end_put= file_put_end.rename(columns={"PE_OI": "PE_OI_"+intial_test,"PE_LTP": "PE_LTP_"+intial_test})
    OI_data_initial_day_put=pd.concat([new_df_start_put["strikePrice"].reset_index(drop=True),new_df_start_put["PE_OI_"+start_time].reset_index(drop=True),new_df_end_put["PE_OI_"+intial_test].reset_index(drop=True),new_df_start_put["PE_LTP_"+start_time].reset_index(drop=True),new_df_end_put["PE_LTP_"+intial_test].reset_index(drop=True)], axis=1)

    OI_data_put=OI_data_initial_day_put[["PE_OI_"+start_time,"PE_OI_"+intial_test]]
    OI_data_put.set_index(OI_data_initial_day_put["strikePrice"], inplace=True)

    Premium_data_put=OI_data_initial_day_put[["PE_LTP_"+start_time,"PE_LTP_"+intial_test]]
    Premium_data_put.set_index(OI_data_initial_day_put["strikePrice"], inplace=True)


    #################################### Plotting for the Put plots #################################################


    fig1 = plt.figure(1, figsize=(0,0))
    ax3 = Premium_data_put.plot(kind='bar',color=['blue', 'red'], edgecolor='black')
    for i, bar in enumerate(ax3.containers):
        ax3.bar_label(bar, label_type='edge', fontsize=10)

    ax3.legend([start_time,intial_test])
    plt.xlabel('Strike Price')
    plt.ylabel('Premium on Put side')
    plt.title('Premium on Put side VS strike price')


    fig2 = plt.figure(2, figsize=(8, 6))
    ax4 = OI_data_put.plot(kind='bar',color=['blue', 'red'], edgecolor='black')
    for i, bar in enumerate(ax4.containers):
        ax4.bar_label(bar, label_type='edge', fontsize=10)

    ax4.legend([start_time,intial_test])
    plt.xlabel('Strike Price')
    plt.ylabel('Maximum OI on Put side')
    plt.title('Maximum OI on the Put side VS strike price')

    plt.show()


############################################# EOD Data cleaning on the call side ######################################

def final_45_minutes_start_call(file,interval,distance,ATM_Init,ATM_End):
    file_2=pd.read_excel(file)
    interval = interval
    column_list = file_2['Time'][::interval].tolist()
    print(column_list)
    d=distance
    x=len(column_list)
    eod_test_start=column_list[x-d]
    ending_time=column_list[x-1]
    eod_intraday_analysis_start=file_2[file_2['Time'] == eod_test_start]
    eod_intraday_analysis_end=file_2[file_2['Time'] == ending_time]

    ATM_init=ATM_Init
    range=5
    ATM_max=ATM_init+range*50
    ATM_min=ATM_init-range*50

    EOD_start_df_call = eod_intraday_analysis_start[(eod_intraday_analysis_start['strikePrice'] >= ATM_min) & (eod_intraday_analysis_start['strikePrice'] <= ATM_max)]
    largest_values = EOD_start_df_call['CE_OI'].nlargest(3)
    EOD_filtered_df_start_call = EOD_start_df_call[EOD_start_df_call['CE_OI'].isin(largest_values)]
    print(EOD_filtered_df_start_call["strikePrice"])

    ATM_end=ATM_End
    range=5
    ATM_max=ATM_end+range*50
    ATM_min=ATM_end-range*50

    EOD_end_df_call = eod_intraday_analysis_end[(eod_intraday_analysis_end['strikePrice'] >= ATM_min) & (eod_intraday_analysis_end['strikePrice'] <= ATM_max)]
    largest_values_end = EOD_end_df_call['CE_OI'].nlargest(3)
    EOD_filtered_df_end_call = EOD_end_df_call[EOD_end_df_call['CE_OI'].isin(largest_values_end)]
    print(EOD_filtered_df_end_call["strikePrice"])

    unique_values = pd.concat([EOD_filtered_df_start_call['strikePrice'], EOD_filtered_df_end_call["strikePrice"]]).unique()
    new_df= pd.DataFrame({"strikePrice": unique_values})
    new_df= new_df.sort_values("strikePrice")

    print(new_df["strikePrice"])

    x=new_df.size

    file_call_start=eod_intraday_analysis_start[(eod_intraday_analysis_start['strikePrice'] == new_df.iloc[0,0])]
    i=1

    while i<x:
        generated_row = eod_intraday_analysis_start[(eod_intraday_analysis_start['strikePrice'] == new_df.iloc[i,0])]
        file_call_start = pd.concat([file_call_start, generated_row], axis=0)
        i=i+1

    file_call_end=eod_intraday_analysis_end[(eod_intraday_analysis_end['strikePrice'] == new_df.iloc[0,0])]
    i=1

    while i<x:
        generated_row = eod_intraday_analysis_end[(eod_intraday_analysis_end['strikePrice'] == new_df.iloc[i,0])]
        file_call_end = pd.concat([file_call_end, generated_row], axis=0)
        i=i+1


    new_df_start= file_call_start.rename(columns={"CE_OI": "CE_OI_"+eod_test_start,"CE_LTP": "CE_LTP_"+eod_test_start})
    new_df_end= file_call_end.rename(columns={"CE_OI": "CE_OI_"+ending_time,"CE_LTP": "CE_LTP_"+ending_time})
    OI_data_initial_day_call=pd.concat([file_call_end["strikePrice"].reset_index(drop=True),new_df_start["CE_OI_"+eod_test_start].reset_index(drop=True),new_df_end["CE_OI_"+ending_time].reset_index(drop=True),new_df_start["CE_LTP_"+eod_test_start].reset_index(drop=True),new_df_end["CE_LTP_"+ending_time].reset_index(drop=True)], axis=1)

    print(file_call_end["strikePrice"])

    OI_data=OI_data_initial_day_call[["CE_OI_"+eod_test_start,"CE_OI_"+ending_time]]
    OI_data.set_index(OI_data_initial_day_call["strikePrice"], inplace=True)

    Premium_data=OI_data_initial_day_call[["CE_LTP_"+eod_test_start,"CE_LTP_"+ending_time]]
    Premium_data.set_index(OI_data_initial_day_call["strikePrice"], inplace=True)

    ##############################  Plotting on call side ##########################################

    fig1 = plt.figure(1, figsize=(0,0))
    ax1 = OI_data.plot(kind='bar',color=['blue', 'red'], edgecolor='black')
    for i, bar in enumerate(ax1.containers):
        ax1.bar_label(bar, label_type='edge', fontsize=10)

    ax1.legend([eod_test_start,ending_time])
    plt.xlabel('Strike Price')
    plt.ylabel('Maximum OI on Call side')
    plt.title('Maximum OI on the Call side VS strike price')

    fig1 = plt.figure(2, figsize=(8, 6))
    ax2 = Premium_data.plot(kind='bar',color=['blue', 'red'], edgecolor='black')
    for i, bar in enumerate(ax2.containers):
        ax2.bar_label(bar, label_type='edge', fontsize=10)

    ax2.legend([eod_test_start,ending_time])
    plt.xlabel('Strike Price')
    plt.ylabel('Premium on Call side')
    plt.title('Premium on Call side VS strike price')

    plt.show()



    ############################################### EOD PUT side Data Cleaning ##########################################

def final_45_minutes_start_put(file,interval,distance,ATM_Init,ATM_End):
    file_2=pd.read_excel(file)
    interval = interval
    column_list = file_2['Time'][::interval].tolist()
    print(column_list)
    d=distance
    x=len(column_list)
    eod_test_start=column_list[x-d]
    ending_time=column_list[x-1]
    eod_intraday_analysis_start=file_2[file_2['Time'] == eod_test_start]
    eod_intraday_analysis_end=file_2[file_2['Time'] == ending_time]

    ATM_init=ATM_Init
    range=5
    ATM_max=ATM_init+range*50
    ATM_min=ATM_init-range*50

    EOD_start_df_put = eod_intraday_analysis_start[(eod_intraday_analysis_start['strikePrice'] >= ATM_min) & (eod_intraday_analysis_start['strikePrice'] <= ATM_max)]
    largest_values = EOD_start_df_put['PE_OI'].nlargest(3)
    EOD_filtered_df_start_put = EOD_start_df_put[EOD_start_df_put['PE_OI'].isin(largest_values)]
    print(EOD_filtered_df_start_put["strikePrice"])

    ATM_end=ATM_End
    range=5
    ATM_max=ATM_end+range*50
    ATM_min=ATM_end-range*50

    EOD_end_df_put = eod_intraday_analysis_end[(eod_intraday_analysis_end['strikePrice'] >= ATM_min) & (eod_intraday_analysis_end['strikePrice'] <= ATM_max)]
    largest_values_end = EOD_end_df_put['PE_OI'].nlargest(3)
    EOD_filtered_df_end_put = EOD_end_df_put[EOD_end_df_put['PE_OI'].isin(largest_values_end)]
    print(EOD_filtered_df_end_put["strikePrice"])

    unique_values = pd.concat([EOD_filtered_df_start_put['strikePrice'], EOD_filtered_df_end_put["strikePrice"]]).unique()
    new_df= pd.DataFrame({"strikePrice": unique_values})
    new_df= new_df.sort_values("strikePrice")

    print(new_df["strikePrice"])

    x=new_df.size

    file_put_start=eod_intraday_analysis_start[(eod_intraday_analysis_start['strikePrice'] == new_df.iloc[0,0])]
    i=1

    while i<x:
        generated_row = eod_intraday_analysis_start[(eod_intraday_analysis_start['strikePrice'] == new_df.iloc[i,0])]
        file_put_start = pd.concat([file_put_start, generated_row], axis=0)
        i=i+1

    file_put_end=eod_intraday_analysis_end[(eod_intraday_analysis_end['strikePrice'] == new_df.iloc[0,0])]
    i=1

    while i<x:
        generated_row = eod_intraday_analysis_end[(eod_intraday_analysis_end['strikePrice'] == new_df.iloc[i,0])]
        file_put_end = pd.concat([file_put_end, generated_row], axis=0)
        i=i+1


    new_df_start= file_put_start.rename(columns={"PE_OI": "PE_OI_"+eod_test_start,"PE_LTP": "PE_LTP_"+eod_test_start})
    new_df_end= file_put_end.rename(columns={"PE_OI": "PE_OI_"+ending_time,"PE_LTP": "PE_LTP_"+ending_time})
    OI_data_initial_day_put=pd.concat([file_put_start["strikePrice"].reset_index(drop=True),new_df_start["PE_OI_"+eod_test_start].reset_index(drop=True),new_df_end["PE_OI_"+ending_time].reset_index(drop=True),new_df_start["PE_LTP_"+eod_test_start].reset_index(drop=True),new_df_end["PE_LTP_"+ending_time].reset_index(drop=True)], axis=1)

    print(file_put_end["strikePrice"])

    OI_data=OI_data_initial_day_put[["PE_OI_"+eod_test_start,"PE_OI_"+ending_time]]
    OI_data.set_index(OI_data_initial_day_put["strikePrice"], inplace=True)

    Premium_data=OI_data_initial_day_put[["PE_LTP_"+eod_test_start,"PE_LTP_"+ending_time]]
    Premium_data.set_index(OI_data_initial_day_put["strikePrice"], inplace=True)

    ##############################  Plotting on call side ##########################################

    fig1 = plt.figure(1, figsize=(0,0))
    ax1 = OI_data.plot(kind='bar',color=['blue', 'red'], edgecolor='black')
    for i, bar in enumerate(ax1.containers):
        ax1.bar_label(bar, label_type='edge', fontsize=10)

    ax1.legend([eod_test_start,ending_time])
    plt.xlabel('Strike Price')
    plt.ylabel('Maximum OI on Put side')
    plt.title('Maximum OI on the Put side VS strike price')

    fig1 = plt.figure(2, figsize=(8, 6))
    ax2 = Premium_data.plot(kind='bar',color=['blue', 'red'], edgecolor='black')
    for i, bar in enumerate(ax2.containers):
        ax2.bar_label(bar, label_type='edge', fontsize=10)

    ax2.legend([eod_test_start,ending_time])
    plt.xlabel('Strike Price')
    plt.ylabel('Premium on Put side')
    plt.title('Premium on Put side VS strike price')

    plt.show()