from kite_trade import *
import pandas as pd
import datetime
import ast
import matplotlib.pyplot as plt
import numpy as np
from tkinter import *
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

def create_toolbar(fig_canvas, frame):
    toolbar = NavigationToolbar2Tk(fig_canvas, frame)
    toolbar.update()
    return toolbar

def conclusion_fut(row):
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


def future_data_parsing():
    global start_date
    global end_date

    kite = KiteApp(enctoken=enctoken)

    date_obj = datetime.datetime.strptime(start_date, '%d-%m-%Y')

    current_date = datetime.datetime.now()

    # Format the datetime object to the desired format '26-Sep-2023'
    target_date_str = date_obj.strftime('%d-%b-%Y')
  
    start_date = datetime.datetime.strptime(target_date_str, "%d-%b-%Y")


    date_obj = datetime.datetime.strptime(end_date, '%d-%m-%Y')

    # Format the datetime object to the desired format '26-Sep-2023'
    target_date_str = date_obj.strftime('%d-%b-%Y')

    end_date = datetime.datetime.strptime(target_date_str, "%d-%b-%Y")


    # Define the months abbreviation
    month_abbreviations = {
        1: 'JAN',
        2: 'FEB',
        3: 'MAR',
        4: 'APR',
        5: 'MAY',
        6: 'JUN',
        7: 'JUL',
        8: 'AUG',
        9: 'SEP',
        10: 'OCT',
        11: 'NOV',
        12: 'DEC'
    }

    # Check if the current date is within the target date range
    if start_date <= current_date <= end_date:
        # Format the date as "DDMON" (e.g., "23OCT")
        # formatted_date = f"{current_date.year:02d}{month_abbreviations[current_date.month]}"
        formatted_date = f"{current_date.year:02d}NOV"
        print(formatted_date[2:])
    else:
        print("Current date is not within the specified range.")

    token=name+formatted_date[2:]+segment


    fut_token_ltp=kite.ltp("NFO:"+token)
    instrument_token_fut=fut_token_ltp["NFO:"+token]['instrument_token']

    from_datetime = datetime.datetime.now() - datetime.timedelta(days=30)     # From last & days
    to_datetime = datetime.datetime.now()
    interval = "15minute"
    content_FUT=kite.historical_data(instrument_token_fut, from_datetime, to_datetime, interval, continuous=False, oi=True)

    content_FUT=str(content_FUT)

    cleaned_contents_FUT = content_FUT.replace("datetime.datetime", "").replace(", tzinfo=tzoffset(None, 19800)", "")
    data_FUT = ast.literal_eval(cleaned_contents_FUT)

    df_FUT = pd.DataFrame(data_FUT)


    df_FUT['date'] = df_FUT['date'].apply(lambda x: pd.Timestamp(year=x[0], month=x[1], day=x[2], hour=x[3], minute=x[4]))
    df_FUT['Date'] = df_FUT['date'].dt.strftime('%Y-%m-%d')
    df_FUT['Time'] = df_FUT['date'].dt.strftime('%H:%M')
    df_FUT = df_FUT.drop(columns=['date'])

    df_FUT= df_FUT[['Date', 'Time', 'open', 'high', 'low', 'close','volume','oi']]


    rows_FUT=df_FUT.shape[0]

    df_FUT["COI"]=0
    df_FUT["COP"]=0

    df_FUT.iloc[0,8]=df_FUT.iloc[0,7]
    df_FUT.iloc[0,9]=df_FUT.iloc[0,5]

    for i in range(1,rows_FUT):
        df_FUT.iloc[i,8]=df_FUT.iloc[i,7]-df_FUT.iloc[(i-1),7]
        df_FUT.iloc[i,9]=df_FUT.iloc[i,5]-df_FUT.iloc[(i-1),5]

    columns_to_remove = ["open", "high", "low"]
    df_FUT = df_FUT.drop(columns=columns_to_remove)

    df_FUT["Bulidup Conclusion Fut"]=df_FUT.apply(conclusion_fut,axis=1)

    df_FUT['LB'] = df_FUT.apply(lambda row: row['COI'] if row['Bulidup Conclusion Fut'] == 'LB' else None, axis=1)
    df_FUT['SB'] = df_FUT.apply(lambda row: row['COI'] if row['Bulidup Conclusion Fut'] == 'SB' else None, axis=1)
    df_FUT['LC'] = df_FUT.apply(lambda row: row['COI'] if row['Bulidup Conclusion Fut'] == 'LC' else None, axis=1)
    df_FUT['SC'] = df_FUT.apply(lambda row: row['COI'] if row['Bulidup Conclusion Fut'] == 'SC' else None, axis=1)

    df_FUT.fillna(0, inplace=True)

    df_FUT["Net LB"]=df_FUT['LB']+df_FUT['LC']
    df_FUT["Net SB"]=df_FUT['SB']+df_FUT['SC']

    df_FUT = df_FUT.iloc[1:]
    df_FUT.reset_index(drop=True, inplace=True)

    df_FUT["Cumulative LB"]=0
    df_FUT["Cumulative SB"]=0

    rows_cumulative=df_FUT.shape[0]
    df_FUT.iloc[0,14]=df_FUT.iloc[0,12]
    df_FUT.iloc[0,15]=df_FUT.iloc[0,13]
    for i in range(1,rows_cumulative):
        df_FUT.iloc[i,14]=df_FUT.iloc[i,12]+df_FUT.iloc[(i-1),14]
        df_FUT.iloc[i,15]=df_FUT.iloc[i,13]+df_FUT.iloc[(i-1),15]

    df_FUT['Date'] = pd.to_datetime(df_FUT['Date']).dt.strftime('%d-%m')
    df_FUT['Datetime'] = df_FUT['Date'] + ': ' + df_FUT['Time']
    df_FUT.drop(['Date', 'Time'], axis=1, inplace=True)
    cols = list(df_FUT.columns)
    cols = ['Datetime'] + [col for col in cols if col != 'Datetime']
    df_FUT = df_FUT[cols]

    df_FUT.to_csv(path_futures+"Future_OI.csv",index=False)

    df_FUT['Cumulative LB'] /= 100000
    df_FUT['Cumulative SB'] /= 100000

    axs2.plot(df_FUT['Datetime'], df_FUT['Cumulative LB'], marker='o',label=f"Long Build UP Expiry: {df.iloc[0,4]}", color='green')
    axs2.plot(df_FUT['Datetime'], df_FUT['Cumulative SB'], marker='o',label=f"Shot Build UP Expiry: {df.iloc[0,4]}", color='red')

    axs2.set_xlabel('Datetime')
    axs2.set_ylabel('Cumulative OI (In Lakhs)')
    axs2.set_title('Net Build UP OI In Futures')
    axs2.grid(True)

    axs2.legend()
    plt.xticks(rotation=90)
    plt.tight_layout()

    canvas1.draw()


def on_mousewheel(event):
    canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

def zoom_in(event):
    global axs2
    xmin, xmax = axs2.get_xlim()
    ymin, ymax = axs2.get_ylim()
    x_center = (xmin + xmax) / 2
    y_center = (ymin + ymax) / 2
    axs2.set_xlim(xmin + (xmax - xmin) * 0.1, xmax - (xmax - xmin) * 0.1)
    axs2.set_ylim(ymin + (ymax - ymin) * 0.1, ymax - (ymax - ymin) * 0.1)
    canvas1.draw()

def zoom_out(event):
    global axs2
    xmin, xmax = axs2.get_xlim()
    ymin, ymax = axs2.get_ylim()
    x_center = (xmin + xmax) / 2
    y_center = (ymin + ymax) / 2
    axs2.set_xlim(xmin - (xmax - xmin) * 0.1, xmax + (xmax - xmin) * 0.1)
    axs2.set_ylim(ymin - (ymax - ymin) * 0.1, ymax + (ymax - ymin) * 0.1)
    canvas1.draw()


def move_left(event):
    global axs2
    xmin, xmax = axs2.get_xlim()
    x_range = xmax - xmin
    axs2.set_xlim(xmin - x_range * 0.1, xmax - x_range * 0.1)
    canvas1.draw()

def move_right(event):
    xmin, xmax = axs2.get_xlim()
    x_range = xmax - xmin
    axs2.set_xlim(xmin + x_range * 0.1, xmax + x_range * 0.1)
    canvas1.draw()

path_main="D:/ashu/Finance/algo_trading/Zerodha_GUI/Kite_Zerodha-main/Kite_Zerodha-main/"
path_futures="D:/ashu/Finance/algo_trading/Zerodha_GUI/Futures_OI_Raw_data/"


df=pd.read_csv(path_main+"Enctoke_Expiry_month_end_info.csv")


start_date = df.iloc[0,3]
end_date = df.iloc[0,4]

name="NIFTY"
segment="FUT"


content_enctoken=df.iloc[0,0]

enctoken = content_enctoken

###################################################### Tkinter ########################################################

root = Tk()
root.title("Matplotlib in Tkinter with Scrollbars")

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

fig1, axs2 = plt.subplots(nrows=1, ncols=1, figsize=(100, 9))

canvas1 = FigureCanvasTkAgg(fig1, master=frame1)
canvas1.draw()
canvas1.get_tk_widget().pack()


frame2=Frame(root)
frame2.pack(anchor='nw')


toolbar_frame1 = ttk.Frame(frame2)  # New frame for toolbar
toolbar_frame1.pack(anchor="ne")   # Place it at top right corner

toolbar1 = create_toolbar(canvas1, toolbar_frame1)

future_data_parsing()


menubar = Menu(root)

# Create a "File" menu


root.bind("<KeyPress-z>", zoom_in)  # Press "z" to zoom in
root.bind("<KeyPress-x>", zoom_out)  # Press "x" to zoom out
root.bind("<Left>", move_left)  # Press the left arrow key to move left
root.bind("<Right>", move_right)

root.bind("<MouseWheel>", on_mousewheel)

root.mainloop()