import Daily_Option_chain_data
import pandas as pd


path="D:/ashu/Finance/algo_trading/Option_chain_data/"
file_1="data1.xlsx"
coloumns_number=79
length_of_time=70
time_array=[]

finial_file=Daily_Option_chain_data.Daily_option_chain_report_generation(path+file_1,coloumns_number,length_of_time)

#finial_file.to_excel(path+'finial_file.xlsx', index=False)

for i in range(len(time_array)):
    file=f"data{i+2}.xlsx"
    time_length=time_array[i]
    file_gen=Daily_Option_chain_data.Daily_option_chain_report_generation(path+file,coloumns_number,time_length)
    print(i)
    finial_file = pd.concat([finial_file, file_gen], axis=0)

finial_file.to_excel(path+'full_and_finial_file.xlsx', index=False)