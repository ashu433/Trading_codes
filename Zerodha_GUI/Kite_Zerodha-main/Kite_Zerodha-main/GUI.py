import datetime
from kite_trade import *
import pandas as pd
import ast
import Intraday_live_data
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np
from tkinter import *
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import warnings




def get_weekdays_before_date(target_date):
    import datetime
    weekdays = ['Friday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday']
    target_date = datetime.datetime.strptime(target_date, '%d-%b-%Y').date()

    result_dates = []

    for weekday in weekdays:
        # Find the weekday's index (0 - Monday, 1 - Tuesday, ..., 6 - Sunday)
        weekday_index = weekdays.index(weekday)

        # Calculate the number of days to subtract to get the desired weekday
        days_to_subtract = (target_date.weekday() - weekday_index + 7) % 7

        # Calculate the previous weekday date
        previous_weekday = target_date - datetime.timedelta(days=days_to_subtract)

        result_dates.append(previous_weekday.strftime('%Y-%m-%d'))

    return result_dates


def data_frame_list_generation(Strike_Prices):
    df=[]


    for i in range(len(Strike_Prices)):
        df_i=pd.read_csv(path_strike_price+name+str(Strike_Prices[i])+".csv")
        new_df=df_i[["Datetime","Cumulative Bullishness","Cumulative SB call","Cumulative SB put"]]

        new_column_names = {
                "Datetime":"Datetime",
                "Cumulative Bullishness":f'"Cumulative Bullishness "{Strike_Prices[i]}',
                "Cumulative SB call":f'"Cumulative SB call "{Strike_Prices[i]}',
                "Cumulative SB put":f'"Cumulative SB put "{Strike_Prices[i]}',
            # Add more columns as needed
            }
        
        new_df.rename(columns=new_column_names, inplace=True)

        df.append(new_df)

    merged_df = df[0]

    # Loop through the remaining dataframes and merge on 'Datetime'
    for df in df[1:]:
        merged_df = merged_df.merge(df, on='Datetime', how='inner')

    final_df=[]

    for i in range(len(Strike_Prices)):
        df_i = merged_df[["Datetime",f'"Cumulative Bullishness "{Strike_Prices[i]}',f'"Cumulative SB call "{Strike_Prices[i]}',f'"Cumulative SB put "{Strike_Prices[i]}']]

        new_column_names = {
                "Datetime":"Datetime",
                f'"Cumulative Bullishness "{Strike_Prices[i]}':"Cumulative Bullishness",
                f'"Cumulative SB call "{Strike_Prices[i]}':"Cumulative SB call",
                f'"Cumulative SB put "{Strike_Prices[i]}':"Cumulative SB put",
            # Add more columns as needed
            }
        
        df_i.rename(columns=new_column_names, inplace=True)

        final_df.append(df_i)

    return final_df


def create_toolbar(fig_canvas, frame):
    toolbar = NavigationToolbar2Tk(fig_canvas, frame)
    toolbar.update()
    return toolbar

def zoom_in(event):
    for ax in axs1:
        xmin, xmax = ax.get_xlim()
        ymin, ymax = ax.get_ylim()
        x_center = (xmin + xmax) / 2
        y_center = (ymin + ymax) / 2
        ax.set_xlim(xmin + (xmax - xmin) * 0.1, xmax - (xmax - xmin) * 0.1)
        ax.set_ylim(ymin + (ymax - ymin) * 0.1, ymax - (ymax - ymin) * 0.1)
    canvas1.draw()

def zoom_out(event):
    for ax in axs1:
        xmin, xmax = ax.get_xlim()
        ymin, ymax = ax.get_ylim()
        x_center = (xmin + xmax) / 2
        y_center = (ymin + ymax) / 2
        ax.set_xlim(xmin - (xmax - xmin) * 0.1, xmax + (xmax - xmin) * 0.1)
        ax.set_ylim(ymin - (ymax - ymin) * 0.1, ymax + (ymax - ymin) * 0.1)
    canvas1.draw()


def move_left(event):
    for ax in axs1:
        xmin, xmax = ax.get_xlim()
        x_range = xmax - xmin
        ax.set_xlim(xmin - x_range * 0.1, xmax - x_range * 0.1)
    canvas1.draw()

def move_right(event):
    for ax in axs1:
        xmin, xmax = ax.get_xlim()
        x_range = xmax - xmin
        ax.set_xlim(xmin + x_range * 0.1, xmax + x_range * 0.1)
    canvas1.draw()


def comparision_build_up_CE(row):
        if ((row['COI CE'] > 0 and row['COP CE'] > 0)):
            return 'LB'
        elif ((row['COI CE'] < 0 and row['COP CE'] < 0)):
            return 'LC'
        elif ((row['COI CE'] > 0 and row['COP CE'] < 0)):
            return 'SB'
        elif ((row['COI CE'] < 0 and row['COP CE'] > 0)):
            return 'SC'
        else:
            pass


def comparision_build_up_PE(row):
        if ((row['COI PE'] > 0 and row['COP PE'] > 0)):
            return 'LB'
        elif ((row['COI PE'] < 0 and row['COP PE'] < 0)):
            return 'LC'
        elif ((row['COI PE'] > 0 and row['COP PE'] < 0)):
            return 'SB'
        elif ((row['COI PE'] < 0 and row['COP PE'] > 0)):
            return 'SC'
        else:
            pass


def comparision(row):
        if ((row['COI'] > 0 and row['COP'] > 0)):
            return 'LB'
        elif ((row['COI'] < 0 and row['COP'] < 0)):
            return 'LC'
        elif ((row['COI'] > 0 and row['COP'] < 0)):
            return 'SB'
        elif ((row['COI'] < 0 and row['COP'] > 0)):
            return 'SC'
        else:
            pass

def strip_until_number(input_str):
    for i, char in enumerate(input_str):
        if char.isdigit():
            return input_str[:i]

def comparision_CE(row):
        if (row['Conclusion CE'] =="LB"):
            return 0
        elif (row['Conclusion CE'] =="LC"):
            return 0
        elif (row['Conclusion CE'] =="SB"):
            return -1
        elif (row['Conclusion CE'] =="SC"):
            return -1
        else:
            pass

def comparision_PE(row):
        if (row['Conclusion PE'] =="LB"):
            return 0
        elif (row['Conclusion PE'] =="LC"):
            return 0
        elif (row['Conclusion PE'] =="SB"):
            return 1
        elif (row['Conclusion PE'] =="SC"):
            return 1
        else:
            pass


def on_mousewheel(event):
    canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")


def create_plot(frame):
    global canvas2, axs2
    
    fig, axs2 = plt.subplots(nrows=1, ncols=1, figsize=(20, 9))
    axs2.set_xlabel('Time')
    axs2.set_ylabel('Cumulative Bullishness by sellers (in Lakhs)')
    axs2.set_title('Bulleshness Contracts by sellers in Lakhs')
    axs2.grid(True)

    canvas2 = FigureCanvasTkAgg(fig, master=frame)
    canvas2.draw()
    canvas2.get_tk_widget().pack()

    return canvas2, axs2

def update_figure_2():
    
    global canvas2
    global ax2

    axs2.clear()


    for i in range(len(Strike_Prices)):
        df=pd.read_csv(path+name+str(Strike_Prices[i])+".csv")
        df['Cumulative Bullishness'] /= 100000
        axs2.plot(df['Time'], df['Cumulative Bullishness'], marker='o', label=str(Strike_Prices[i]))

    axs2.set_xlabel('Time')
    axs2.set_ylabel('Cumulative Bullishness by sellers (in Lakhs)')
    axs2.set_title('Bulleshness Contracts by sellers in Lakhs')
    axs2.grid(True)

    axs2.legend()
    plt.xticks(rotation=90)
    plt.tight_layout()

    canvas2.draw()

    print("Updated new window")

    # new_Window.after(1000, update_figure_2, new_Window)


def Open_window_1_overall_bullishness():
        
    global Strike_Prices

    new_Window=Toplevel(root)
    new_Window.title("Intraday Bullishness")

    scrollable_frame = ttk.Frame(new_Window)
    scrollable_frame.pack(fill="both", expand=True)

    canvas = Canvas(scrollable_frame)
    canvas.pack(side="left", fill="both", expand=True)

    scrollbar_y = ttk.Scrollbar(scrollable_frame, orient="vertical", command=canvas.yview)
    scrollbar_y.pack(side="right", fill="y")
    canvas.configure(yscrollcommand=scrollbar_y.set)

    scrollbar_x = ttk.Scrollbar(new_Window, orient="horizontal", command=canvas.xview)
    scrollbar_x.pack(fill="x")
    canvas.configure(xscrollcommand=scrollbar_x.set)

    canvas.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    scrollable_content = ttk.Frame(canvas)
    canvas.create_window((0, 0), window=scrollable_content, anchor="nw")

    frame2 = ttk.Frame(scrollable_content)
    frame2.pack(fill="both", expand=True)

    canvas2, axs2 = create_plot(frame2)


    update_figure_2()


    menubar = Menu(new_Window)
    new_Window.config(menu=menubar)
    menubar.add_command(label="Back to Main Window", command=new_Window.destroy)

    frame3=Frame(new_Window)
    frame3.pack(anchor='nw')

    b1=Button(frame3,text="Refresh",command=update_figure_2)
    b1.pack()

    toolbar_frame3 = ttk.Frame(frame3)  # New frame for toolbar
    toolbar_frame3.pack(anchor="nw")   # Place it at top right corner

    toolbar2 = create_toolbar(canvas2, toolbar_frame3)

def update_figures():

    global name
    global axs1, axs2
    global path
    global time_list
    global specific_date
    global xox
    global Strike_Prices

    axs1[0].clear()
    axs1[1].clear()
    axs1[2].clear()

    color_ce_list=[]
    color_pe_list=[]

    with open(path+"Call_put_quote_token.txt",'r') as file:
        content_strike_price=file.read()

    content_read=ast.literal_eval(content_strike_price)

    Strike_Prices=content_read['Strike Prices']
    token_CE=content_read['token_call']
    token_PE=content_read['token_put']

    for ii in range(len(Strike_Prices)):

        instrument_token_CE = token_CE[ii]
        instrument_token_PE = token_PE[ii]

        import datetime

        from_datetime = datetime.datetime.now() - datetime.timedelta(days=4)     # From last & days
        to_datetime = datetime.datetime.now()
        interval = "minute"
        content_CE=kite.historical_data(instrument_token_CE, from_datetime, to_datetime, interval, continuous=False, oi=True)
        content_PE=kite.historical_data(instrument_token_PE, from_datetime, to_datetime, interval, continuous=False, oi=True)

        Content_CE=str(content_CE)
        Content_PE=str(content_PE)

        cleaned_contents_CE = Content_CE.replace("datetime.datetime", "").replace(", tzinfo=tzoffset(None, 19800)", "")
        cleaned_contents_PE = Content_PE.replace("datetime.datetime", "").replace(", tzinfo=tzoffset(None, 19800)", "")

        data_CE = ast.literal_eval(cleaned_contents_CE)
        data_PE = ast.literal_eval(cleaned_contents_PE)

        df_CE = pd.DataFrame(data_CE)
        df_PE = pd.DataFrame(data_PE)

        df_CE['date'] = df_CE['date'].apply(lambda x: pd.Timestamp(year=x[0], month=x[1], day=x[2], hour=x[3], minute=x[4]))
        df_CE['Date'] = df_CE['date'].dt.strftime('%Y-%m-%d')
        df_CE['Time'] = df_CE['date'].dt.strftime('%H:%M')
        df_CE = df_CE.drop(columns=['date'])

        df_PE['date'] = df_PE['date'].apply(lambda x: pd.Timestamp(year=x[0], month=x[1], day=x[2], hour=x[3], minute=x[4]))
        df_PE['Date'] = df_PE['date'].dt.strftime('%Y-%m-%d')
        df_PE['Time'] = df_PE['date'].dt.strftime('%H:%M')
        df_PE = df_PE.drop(columns=['date'])

        df_CE = df_CE[['Date', 'Time', 'open', 'high', 'low', 'close','volume','oi']]
        df_PE = df_PE[['Date', 'Time', 'open', 'high', 'low', 'close','volume','oi']]




        rows_CE=df_CE.shape[0]
        rows_PE=df_PE.shape[0]

        df_CE["COI"]=0
        df_PE["COI"]=0

        df_CE["COP"]=0
        df_PE["COP"]=0

        for i in range(1,rows_CE):
            df_CE.iloc[i,8]=df_CE.iloc[i,7]-df_CE.iloc[(i-1),7]
            df_CE.iloc[i,9]=df_CE.iloc[i,5]-df_CE.iloc[(i-1),5]

        for i in range(1,rows_PE):
            df_PE.iloc[i,8]=df_PE.iloc[i,7]-df_PE.iloc[(i-1),7]
            df_PE.iloc[i,9]=df_PE.iloc[i,5]-df_PE.iloc[(i-1),5]


        df_CE["Date"] = pd.to_datetime(df_CE["Date"])
        df_CE = df_CE[df_CE["Date"] == specific_date]

        df_PE["Date"] = pd.to_datetime(df_PE["Date"])
        df_PE = df_PE[df_PE["Date"] == specific_date]

        df_CE.reset_index(drop=True, inplace=True)
        df_PE.reset_index(drop=True, inplace=True)

        columns_to_remove = ["open", "high", "low"]
        df_CE = df_CE.drop(columns=columns_to_remove)
        df_PE = df_PE.drop(columns=columns_to_remove)

        df_CE["Conclusion CE"]=0
        df_PE["Conclusion PE"]=0


        new_column_names_CE = {
        'COI': 'COI CE',
        "close": "close CE",
        "volume": "volume CE",
        "oi": "oi CE",
        "COP": "COP CE",
        # Add more columns as needed
        }
        new_column_names_PE = {
            'COI': 'COI PE',
            "close": "close PE",
            "volume": "volume PE",
            "oi": "oi PE",
            "COP": "COP PE",
            # Add more columns as needed
        }

        df_CE.rename(columns=new_column_names_CE, inplace=True)
        df_PE.rename(columns=new_column_names_PE, inplace=True)

        columns_to_remove = ["Date", "Time"]
        df_PE = df_PE.drop(columns=columns_to_remove)

        finial_file = pd.concat([df_CE, df_PE], axis=1)
        finial_file=finial_file[(finial_file["COI CE"] != 0) | (finial_file["COI PE"] != 0)]
        finial_file.fillna(0,inplace=True)

        finial_file.reset_index(drop=True, inplace=True)

        
        rows_total=finial_file.shape[0]

        for j in range(1,rows_total):
            finial_file.iloc[j,6]=finial_file.iloc[j,2]-finial_file.iloc[(j-1),2]
            finial_file.iloc[j,12]=finial_file.iloc[j,8]-finial_file.iloc[(j-1),8]

        finial_file["Conclusion CE"]=finial_file.apply(comparision_build_up_CE,axis=1)
        finial_file["Conclusion PE"]=finial_file.apply(comparision_build_up_PE,axis=1)

        finial_file = finial_file.where(pd.notna(finial_file), None)

        color_map_ce = {
        'SB': 'red',
        'LC': 'red',
        'LB': 'green',
        'SC': 'green',
        None: "black"
        }

        color_map_pe = {
            'LB': 'red',
            'SC': 'red',
            'SB': 'green',
            'LC': 'green',
            None: "black"
        }

        color_ce=[color_map_ce[conclusion] for conclusion in finial_file['Conclusion CE']]
        color_pe=[color_map_pe[conclusion] for conclusion in finial_file['Conclusion PE']]

        color_ce_list.append(color_ce)
        color_pe_list.append(color_pe)
        finial_file.reset_index(drop=True, inplace=True)

        finial_file["Bullishness CE"]=finial_file.apply(comparision_CE,axis=1)
        finial_file["Bullishness PE"]=finial_file.apply(comparision_PE,axis=1)

        finial_file["Bullishness CE"]=finial_file["Bullishness CE"]*finial_file["COI CE"]
        finial_file["Bullishness PE"]=finial_file["Bullishness PE"]*finial_file["COI PE"]
        finial_file["Over All Bullishness"]=finial_file["Bullishness CE"]+finial_file["Bullishness PE"]

        
        row_final=finial_file.shape[0]
        
        finial_file.fillna(0, inplace=True)
        finial_file["Cumulative Bullishness"]=0
        finial_file.iloc[0,17]=finial_file.iloc[0,16]
        for i in range(1,row_final):
            finial_file.iloc[i,17]=finial_file.iloc[i,16]+finial_file.iloc[(i-1),17]

        finial_file.to_csv(path+name+str(Strike_Prices[ii])+".csv",index=False)


    for mm in range(len(Strike_Prices)):

        finial_file=pd.read_csv(path+name+str(Strike_Prices[mm])+".csv")
        index_with_zero = finial_file[finial_file['Over All Bullishness'] == 0].index.tolist()
        for kk in index_with_zero:
            if (finial_file.iloc[kk,14]==0 and finial_file.iloc[kk,15]==0):
                pass
            else:
                finial_file.iloc[kk,16]=finial_file.iloc[kk,14]+finial_file.iloc[kk,15]

        row_final=finial_file.shape[0]
        
        finial_file.fillna(0, inplace=True)
        finial_file["Cumulative Bullishness"]=0
        finial_file.iloc[0,17]=finial_file.iloc[0,16]
        for i in range(1,row_final):
            finial_file.iloc[i,17]=finial_file.iloc[i,16]+finial_file.iloc[(i-1),17]


        finial_file['LB CE'] = finial_file.apply(lambda row: row['COI CE'] if row['Conclusion CE'] == 'LB' else None, axis=1)
        finial_file['SB CE'] = finial_file.apply(lambda row: row['COI CE'] if row['Conclusion CE'] == 'SB' else None, axis=1)
        finial_file['LC CE'] = finial_file.apply(lambda row: row['COI CE'] if row['Conclusion CE'] == 'LC' else None, axis=1)
        finial_file['SC CE'] = finial_file.apply(lambda row: row['COI CE'] if row['Conclusion CE'] == 'SC' else None, axis=1)

        finial_file['LB PE'] = finial_file.apply(lambda row: row['COI PE'] if row['Conclusion PE'] == 'LB' else None, axis=1)
        finial_file['SB PE'] = finial_file.apply(lambda row: row['COI PE'] if row['Conclusion PE'] == 'SB' else None, axis=1)
        finial_file['LC PE'] = finial_file.apply(lambda row: row['COI PE'] if row['Conclusion PE'] == 'LC' else None, axis=1)
        finial_file['SC PE'] = finial_file.apply(lambda row: row['COI PE'] if row['Conclusion PE'] == 'SC' else None, axis=1)

        finial_file = finial_file.fillna(0)

        finial_file["Net_SB_call"]=finial_file['SB CE']+finial_file['SC CE']
        finial_file["Net_SB_put"]=finial_file['SB PE']+finial_file['SC PE']

        finial_file["Cumulative SB call"]=0
        rows1=finial_file.shape[0]
        finial_file.iloc[0,28]=finial_file.iloc[0,26]
        for i in range(1,rows1):
            finial_file.iloc[i,28]=finial_file.iloc[i,26]+finial_file.iloc[(i-1),28]


        finial_file["Cumulative SB put"]=0
        rows2=finial_file.shape[0]
        finial_file.iloc[0,29]=finial_file.iloc[0,27]
        for i in range(1,rows2):
            finial_file.iloc[i,29]=finial_file.iloc[i,27]+finial_file.iloc[(i-1),29]

        finial_file.to_csv(path+name+str(Strike_Prices[mm])+".csv",index=False)


    final_file1=pd.read_csv(path+name+str(Strike_Prices[0])+".csv")
    final_file2=pd.read_csv(path+name+str(Strike_Prices[1])+".csv")
    final_file3=pd.read_csv(path+name+str(Strike_Prices[2])+".csv")

    bar_width = 0.35
    # fig1, axs1 = plt.subplots(nrows=3, ncols=1, figsize=(10, 18))  # Create a 3x1 grid of subplots

    run=0

    for i,(ax, finial_file, color_ce, color_pe) in enumerate(zip(axs1, [final_file1, final_file2, final_file3], color_ce_list, color_pe_list)):

        finial_file.set_index("Time", inplace=True)
        index = np.arange(len(finial_file))  # Index for the x-axis

        
        ce_bars = ax.bar(index, finial_file["COI CE"]/ 100000, width=bar_width, color=color_ce, edgecolor='black', label="COI CE")
        pe_bars = ax.bar(index + bar_width, finial_file["COI PE"]/ 100000, width=bar_width, color=color_pe, edgecolor='black', label="COI PE")

        if i < 2:
            ax.set_xticklabels([])

        ax.set_ylabel("COI in Lakhs")
        ax.set_xticks(index + bar_width / 2)
        ax.set_xticklabels(finial_file.index, rotation=45)

        if i == 0:
            ax.legend(["COI CE (ATM)", "COI PE (ATM)"], title=str(Strike_Prices[i]))
        elif i == 1:
            ax.legend(["COI CE (OTM)", "COI PE (ITM)"], title=str(Strike_Prices[i]))
        elif i == 2:
            ax.legend(["COI CE (ITM)", "COI PE (OTM)"], title=str(Strike_Prices[i]))

        run=run+1



        for ce_bar, pe_bar, conclusion_ce, conclusion_pe in zip(ce_bars, pe_bars, finial_file["Conclusion CE"], finial_file["Conclusion PE"]):
            ax.text(ce_bar.get_x() + ce_bar.get_width() / 2, ce_bar.get_height(), conclusion_ce, ha='center', va='bottom', fontsize=8)
            ax.text(pe_bar.get_x() + pe_bar.get_width() / 2, pe_bar.get_height(), conclusion_pe, ha='center', va='bottom', fontsize=8)

            ce_value = ce_bar.get_height() 
            pe_value = pe_bar.get_height()

            ax.annotate(f"CE: {ce_value:.2f}\nPE: {pe_value:.2f}",
                        xy=(ce_bar.get_x(), ce_bar.get_height()),  # Adjust the xy coordinates for the left side
                        xytext=(-5, 5),  # Offset for the text
                        textcoords="offset points",
                        ha='right', va='center', fontsize=8) 
            

    current_time = datetime.datetime.now().time()
    print(f"the current time is {current_time}")

    current_datetime = datetime.datetime.now()
    delayed_datetime = current_datetime - datetime.timedelta(minutes=1)
    delayed_time = delayed_datetime.strftime('%H:%M')
    delayed_time=str(delayed_time)

    canvas1.draw()

    # root.after(60000, update_figures)

    final_file1=pd.read_csv(path+name+str(Strike_Prices[0])+".csv")
    rows_delay=final_file1.shape[0]
    time_last=final_file1.iloc[rows_delay-1,1]

####################################################### Final hrs Update #################################
    
    print(f"Updating update figure {xox} times")
    xox=xox+1

    if time_last==delayed_time:
        schedule_next_execution()
    else:
        update_figures()

    # schedule_next_execution()
####################################################### Final hrs Update #################################

def create_plot1(frame3):
    global canvas3, axes
    
    fig, axes = plt.subplots(3, 1, figsize=(20, 10))

    canvas3 = FigureCanvasTkAgg(fig, master=frame3)
    canvas3.draw()
    canvas3.get_tk_widget().pack()

    return canvas3, axes

def update_figure_3():
    
    global canvas3
    global axes
    global Strike_Prices


    df1=pd.read_csv(path+name+str(Strike_Prices[0])+".csv")
    df2=pd.read_csv(path+name+str(Strike_Prices[1])+".csv")
    df3=pd.read_csv(path+name+str(Strike_Prices[2])+".csv")

    In_money=['ITM','ATM','OTM']
    length=len(In_money)

    for i, df in enumerate([df1, df2, df3]):
        ax = axes[i]
        ax.clear()
        ax.plot(df['Time'], df['Cumulative SB call']/100000, marker='o', linestyle='-', color='red', label=f'Call SB: {Strike_Prices[i]} {In_money[i]}')
        ax.plot(df['Time'], df['Cumulative SB put']/100000, marker='o', linestyle='-', color='green', label=f'Put SB: {Strike_Prices[i]} {In_money[length-1-i]}')
        ax.set_xlabel('Time')
        ax.set_ylabel('Cumulative SB call(in Lakhs)')
        ax.legend()
        ax.tick_params(axis='x', rotation=90)

    plt.tight_layout()

    canvas3.draw()

    print("Updated new window")



def Open_window_2_over_all():

    global Strike_Prices

    new_Window2=Toplevel(root)
    new_Window2.title("Intraday Buildup")

    scrollable_frame = ttk.Frame(new_Window2)
    scrollable_frame.pack(fill="both", expand=True)

    canvas = Canvas(scrollable_frame)
    canvas.pack(side="left", fill="both", expand=True)

    scrollbar_y = ttk.Scrollbar(scrollable_frame, orient="vertical", command=canvas.yview)
    scrollbar_y.pack(side="right", fill="y")
    canvas.configure(yscrollcommand=scrollbar_y.set)

    scrollbar_x = ttk.Scrollbar(new_Window2, orient="horizontal", command=canvas.xview)
    scrollbar_x.pack(fill="x")
    canvas.configure(xscrollcommand=scrollbar_x.set)

    canvas.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    scrollable_content = ttk.Frame(canvas)
    canvas.create_window((0, 0), window=scrollable_content, anchor="nw")

    frame3 = ttk.Frame(scrollable_content)
    frame3.pack(fill="both", expand=True)

    canvas3, axes = create_plot1(frame3)


    update_figure_3()


    menubar = Menu(new_Window2)
    new_Window2.config(menu=menubar)
    menubar.add_command(label="Back to Main Window", command=new_Window2.destroy)


    frame6=Frame(new_Window2)
    frame6.pack(anchor='nw')
    
    b1=Button(frame6,text="Refresh",command=update_figure_3)
    b1.pack()

    toolbar_frame6 = ttk.Frame(frame6)  # New frame for toolbar
    toolbar_frame6.pack(anchor="nw")   # Place it at top right corner

    toolbar3 = create_toolbar(canvas3, toolbar_frame6)

def create_plot2(frame4):
    global canvas4, axeswin_3
    
    fig, axeswin_3 = plt.subplots(nrows=1, ncols=1, figsize=(100, 9))

    canvas4 = FigureCanvasTkAgg(fig, master=frame4)
    canvas4.draw()
    canvas4.get_tk_widget().pack()

    return canvas4, axeswin_3

def update_figure_4():
    
    global canvas4
    global axeswin_3
    global Strike_Prices

    warnings.filterwarnings("ignore")

    final_df=data_frame_list_generation(Strike_Prices)

    axs2=axeswin_3
    axs2.clear()

    xox=0

    for data_frame in final_df:
        data_frame['Cumulative Bullishness'] /= 100000
        axs2.plot(data_frame['Datetime'], data_frame['Cumulative Bullishness'], marker='o', label=str(Strike_Prices[xox]))
        xox=xox+1

    axs2.set_xlabel('Datetime')
    axs2.set_ylabel('Cumulative Bullishness by sellers (in Lakhs)')
    axs2.set_title('Bulleshness Contracts by sellers in Lakhs')
    axs2.grid(True)

    axs2.legend()
    plt.xticks(rotation=90)
    plt.tight_layout()

    canvas4.draw()



def Open_window_3_over_all():
    global Strike_Prices

    new_Window3=Toplevel(root)
    new_Window3.title("Over All Bullishness")

    scrollable_frame = ttk.Frame(new_Window3)
    scrollable_frame.pack(fill="both", expand=True)

    canvas = Canvas(scrollable_frame)
    canvas.pack(side="left", fill="both", expand=True)

    scrollbar_y = ttk.Scrollbar(scrollable_frame, orient="vertical", command=canvas.yview)
    scrollbar_y.pack(side="right", fill="y")
    canvas.configure(yscrollcommand=scrollbar_y.set)

    scrollbar_x = ttk.Scrollbar(new_Window3, orient="horizontal", command=canvas.xview)
    scrollbar_x.pack(fill="x")
    canvas.configure(xscrollcommand=scrollbar_x.set)

    canvas.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    scrollable_content = ttk.Frame(canvas)
    canvas.create_window((0, 0), window=scrollable_content, anchor="nw")

    frame4 = ttk.Frame(scrollable_content)
    frame4.pack(fill="both", expand=True)

    canvas4, axeswin_3 = create_plot2(frame4)

    update_figure_4()

    menubar = Menu(new_Window3)
    new_Window3.config(menu=menubar)
    menubar.add_command(label="Back to Main Window", command=new_Window3.destroy)


    frame7=Frame(new_Window3)
    frame7.pack(anchor='nw')
    
    b1=Button(frame7,text="Refresh",command=update_figure_4)
    b1.pack()

    toolbar_frame7 = ttk.Frame(frame7)  # New frame for toolbar
    toolbar_frame7.pack(anchor="nw")   # Place it at top right corner

    toolbar5 = create_toolbar(canvas4, toolbar_frame7)

 

def create_plot3(frame8):
    global canvas5, axeswin_4
    
    fig, axeswin_4 = plt.subplots(3, 1, figsize=(100, 10))

    canvas5 = FigureCanvasTkAgg(fig, master=frame8)
    canvas5.draw()
    canvas5.get_tk_widget().pack()

    return canvas5, axeswin_4


def update_figure_5():
    global canvas5
    global axeswin_4
    global Strike_Prices

    warnings.filterwarnings("ignore")
    df=data_frame_list_generation(Strike_Prices)
    axes=axeswin_4

    for i, df in enumerate(df):
        ax = axes[i]
        ax.clear()
        ax.plot(df['Datetime'], df['Cumulative SB call']/100000, marker='o', linestyle='-', color='red', label=f'Call SB: {Strike_Prices[i]}')
        ax.plot(df['Datetime'], df['Cumulative SB put']/100000, marker='o', linestyle='-', color='green', label=f'Put SB: {Strike_Prices[i]}')
        ax.set_xlabel('Datetime')
        ax.set_ylabel('Cumulative SB call(in Lakhs)')
        ax.legend()
        ax.tick_params(axis='x', rotation=90)

    plt.tight_layout()

    canvas5.draw()

    print("Updated new window")

def Open_window_4_over_all():
    global Strike_Prices

    new_Window4=Toplevel(root)
    new_Window4.title("Overall Buildup")

    scrollable_frame = ttk.Frame(new_Window4)
    scrollable_frame.pack(fill="both", expand=True)

    canvas = Canvas(scrollable_frame)
    canvas.pack(side="left", fill="both", expand=True)

    scrollbar_y = ttk.Scrollbar(scrollable_frame, orient="vertical", command=canvas.yview)
    scrollbar_y.pack(side="right", fill="y")
    canvas.configure(yscrollcommand=scrollbar_y.set)

    scrollbar_x = ttk.Scrollbar(new_Window4, orient="horizontal", command=canvas.xview)
    scrollbar_x.pack(fill="x")
    canvas.configure(xscrollcommand=scrollbar_x.set)

    canvas.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    scrollable_content = ttk.Frame(canvas)
    canvas.create_window((0, 0), window=scrollable_content, anchor="nw")

    frame8 = ttk.Frame(scrollable_content)
    frame8.pack(fill="both", expand=True)

    canvas5, axeswin_4 = create_plot3(frame8)

    update_figure_5()

    menubar = Menu(new_Window4)
    new_Window4.config(menu=menubar)
    menubar.add_command(label="Back to Main Window", command=new_Window4.destroy)


    frame9=Frame(new_Window4)
    frame9.pack(anchor='nw')
    
    b1=Button(frame9,text="Refresh",command=update_figure_5)
    b1.pack()

    toolbar_frame9 = ttk.Frame(frame9)  # New frame for toolbar
    toolbar_frame9.pack(anchor="nw")   # Place it at top right corner

    toolbar9 = create_toolbar(canvas5, toolbar_frame9)

def schedule_next_execution():
    global time_list

    times_to_execute=time_list

    # Get the current time
    current_time = datetime.now().strftime("%H:%M:%S")

    # Find the next time in the list that is greater than the current time
    next_time = None
    for time in times_to_execute:
        if time > current_time:
            next_time = time
            break

    if next_time:
        # Calculate the time difference in seconds
        time_difference = (datetime.strptime(next_time, "%H:%M:%S") - datetime.strptime(current_time, "%H:%M:%S")).total_seconds()

        # Schedule the next execution of update_figures() at the calculated time difference
        root.after(int(time_difference * 1000), update_figures)
    else:
        # No more times in the list for today, you can handle this case as needed
        print("No more times to execute today")



global specific_date
global weekday_dates
global time_list

path="D:/ashu/Finance/algo_trading/Zerodha_GUI/OI_Raw_Data_Collected/"
path_strike_price="D:/ashu/Finance/algo_trading/Zerodha_GUI/Non_Intraday_OI_Data_Collected/"

path_main="D:/ashu/Finance/algo_trading/Zerodha_GUI/Kite_Zerodha-main/Kite_Zerodha-main/"

df=pd.read_csv(path_main+"Enctoke_Expiry_month_end_info.csv")
content_enctoken=df.iloc[0,0]

expiry_days_list=["10-Nov-2023(Friday)","13-Nov-2023(Monday)","14-Nov-2023(Tuesday)","15-Nov-2023(Wednesday)","16-Nov-2023(Thursday)"]

enctoken = content_enctoken

kite = KiteApp(enctoken=enctoken)

import datetime

with open(path_main+"expiry_date.txt",'r') as file:
    content_expiry_date=file.read()


content_expiry_day=content_expiry_date

with open(path+"Call_put_quote_token.txt",'r') as file:
    content_strike_price=file.read()

content_read=ast.literal_eval(content_strike_price)

Quote=content_read['quote_call'][0]

result = strip_until_number(Quote)


name=str(result)
expiry=content_expiry_day


today = datetime.datetime.now().date()
formatted_date = today.strftime('%Y-%m-%d')
specific_date = formatted_date


########################################## Time list computation #######################################

from datetime import datetime, timedelta

# Define the start and end times
start_time = datetime.strptime("9:18:00", "%H:%M:%S")
end_time = datetime.strptime("15:30:00", "%H:%M:%S")

# Define the interval (3 minutes)
interval = timedelta(minutes=3)

# Initialize an empty list to store the generated times
time_list = []

# Generate the times
current_time = start_time
while current_time <= end_time:
    time_list.append(current_time.strftime("%H:%M:%S"))
    current_time += interval


time_string = "09:16:00"

# Define the format of the time string
time_format = "%H:%M:%S"

time_object = datetime.strptime(time_string, time_format).time()

time_object =time_object.strftime("%H:%M:%S")

time_list.insert(0,time_object)

########################################## Time list computation ########################################

xox=0

root = Tk()
root.title("Intraday Bar Plot OI Buildup")

scrollable_frame = ttk.Frame(root)
scrollable_frame.pack(fill="both", expand=True)

canvas = Canvas(scrollable_frame)
canvas.pack(side="left", fill="both", expand=True)

scrollbar_y = ttk.Scrollbar(scrollable_frame, orient="vertical", command=canvas.yview)
scrollbar_y.pack(side="right", fill="y")
canvas.configure(yscrollcommand=scrollbar_y.set)

scrollbar_x = ttk.Scrollbar(root, orient="horizontal", command=canvas.xview)
scrollbar_x.pack(fill="x")
canvas.configure(xscrollcommand=scrollbar_x.set)

canvas.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

scrollable_content = ttk.Frame(canvas)
canvas.create_window((0, 0), window=scrollable_content, anchor="nw")

frame1 = ttk.Frame(scrollable_content)
frame1.pack(fill="both", expand=True)

fig1, axs1 = plt.subplots(nrows=3, ncols=1, figsize=(20, 20))
for ax in axs1:
    ax.plot([], [])
    ax.set_xlim(0, 10)
    ax.set_ylim(-2, 2)

canvas1 = FigureCanvasTkAgg(fig1, master=frame1)
canvas1.draw()
canvas1.get_tk_widget().pack()




root.bind("<KeyPress-z>", zoom_in)  # Press "z" to zoom in
root.bind("<KeyPress-x>", zoom_out)  # Press "x" to zoom out
root.bind("<Left>", move_left)  # Press the left arrow key to move left
root.bind("<Right>", move_right)

menubar = Menu(root)

# Create a "File" menu
file_menu = Menu(menubar, tearoff=0)

menubar.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="Intraday Bullishness", command=Open_window_1_overall_bullishness)
file_menu.add_command(label="Intraday Buildup", command=Open_window_2_over_all)
file_menu.add_command(label="Overall Bullishness", command=Open_window_3_over_all)
file_menu.add_command(label="Overall Buildup", command=Open_window_4_over_all)



root.config(menu=menubar)

frame3=Frame(root)
frame3.pack(anchor='nw')

toolbar_frame3 = ttk.Frame(frame3)  # New frame for toolbar
toolbar_frame3.pack(anchor="ne")   # Place it at top right corner

toolbar3 = create_toolbar(canvas1, toolbar_frame3)

update_figures()
# schedule_next_execution()

root.bind("<MouseWheel>", on_mousewheel)

root.mainloop()