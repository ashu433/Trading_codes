import pandas as pd
import matplotlib.pyplot as plt

def Daily_option_chain_report_generation(file_name,coloumn_size,Recorded_number_of_time):
    file_1=file_name
    num_of_rows=coloumn_size
    Time_number=Recorded_number_of_time
    file_1=pd.read_excel(file_1,sheet_name='NIFTY')
    xox=file_1.iloc[0,1]
    file_1.insert(0, 'TIME',0)
    file_1.loc[:num_of_rows+2,"TIME"]=xox
    file_1 = file_1.drop(file_1.index[:2])
    file_1.columns = file_1.iloc[0]
    file_1 = file_1[1:]
    file_1 = file_1.rename(columns={file_1.columns[0]: 'Time'})
    file_1=file_1.reset_index(drop=True)

    file_1.reset_index(drop=True)
    a_time = num_of_rows + 1
    a_skip_1 = num_of_rows
    a_skip_2 = num_of_rows + 4
    a_array_start = num_of_rows + 4
    a_array_end = 2 * num_of_rows + 3
    diff = num_of_rows + 4
    l1=[]

    for i in range(1, Time_number):
        p = (i - 1) * diff
        index = a_time + p
        if index in file_1.index:
            pass
        else:
            
            file_1.loc[index]

    for i in range(1, Time_number):
        p = (i - 1) * diff
        index = a_time + p
        if index in file_1.index:
            xox = file_1.loc[index, "CE_CHNG_IN_OI"]
            file_1.loc[(a_array_start+p):(a_array_end+p),'Time']=xox
            x11=list(range((a_skip_1+p),(a_skip_2+p)))
            l1=l1+x11
            

    file_1 = file_1.drop(l1).reset_index(drop=True)

    return file_1
