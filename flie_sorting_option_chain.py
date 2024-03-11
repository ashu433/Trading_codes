import Daily_Option_chain_data
import pandas as pd
import os
import glob
import every_day_initial_final_OI_buildup



def file_sorting_of_Option_chain(date,month_word,month_number,year,number_of_rows,closing_price):

    date=date
    month_word=month_word
    month_number=month_number
    year=year
    coloumns_number=number_of_rows
    closing_price=closing_price
    path_1=f"D:/ashu/Finance/Option_chain_data/{month_word}_{year}/{date}_{month_number}_{year}/"
    path_2="D:/ashu/Finance/algo_trading/Option_chain_data/"

    Date_ppt=f"{date}-{month_number}-{year}"

    xlsx_files = glob.glob(os.path.join(path_1, '*.xlsx'))
    num_xlsx_files = len(xlsx_files)
    print(num_xlsx_files)


    time_arr_overall_len=[]
    for i in range(1,num_xlsx_files+1):
        data_1=pd.read_excel(path_1+f"data{i}.xlsx")
        row=data_1.shape[0]
        time_arr=[]
        i=0
        while True:
            x=(coloumns_number+4)*i
            i=i+1
            if x<=row:
                l1=data_1.iloc[x,1]
                time_arr.append(l1)
            else:
                break
        l2=len(time_arr) 
        time_arr_overall_len.append(l2)

    l3=len(time_arr_overall_len)
    print(time_arr_overall_len)

    length_of_time=time_arr_overall_len[0]
    time_array=time_arr_overall_len[1:l3]

    file_1=path_1+"data1.xlsx"

    finial_file=Daily_Option_chain_data.Daily_option_chain_report_generation(file_1,coloumns_number,length_of_time)

    #finial_file.to_excel(path+'finial_file.xlsx', index=False)

    for i in range(len(time_array)):
        file=path_1+f"data{i+2}.xlsx"
        time_length=time_array[i]
        file_gen=Daily_Option_chain_data.Daily_option_chain_report_generation(file,coloumns_number,time_length)
        print(i)
        finial_file = pd.concat([finial_file, file_gen], axis=0)

    finial_file.to_excel(path_2+'full_and_finial_file.xlsx', index=False)


    every_day_initial_final_OI_buildup.Every_day_initial_final_Oi_buildup(coloumns_number,closing_price,Date_ppt)



if __name__=='__main__':  
    pass