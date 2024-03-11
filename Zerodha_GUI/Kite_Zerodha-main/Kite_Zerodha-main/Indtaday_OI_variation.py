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
import date_time_format




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

################################    Segment Selection and token Generation  #####################################

def find_closest_index(numbers, target):
    closest_index = None
    min_difference = float('inf')  # Set to positive infinity initially

    for i, number in enumerate(numbers):
        difference = abs(number - target)

        if difference < min_difference:
            min_difference = difference
            closest_index = i

    return closest_index

def quote_token_computation(strike_price_list_new,name,expiry):
    global Month_end
    global kite

    Strike_Prices=strike_price_list_new

    enctoken = content_enctoken

    kite = KiteApp(enctoken=enctoken)

    if Month_end==0:
        call_list=[]
        put_list=[]
        token_CE=[]
        token_PE=[]
        call_put_dict={}

        from datetime import datetime


        formatted_date=date_time_format.date_time_format(expiry)

        if name=="SENSEX":
            
            for i in range(len(Strike_Prices)):
                quote_CE=name+formatted_date+str(Strike_Prices[i])+"CE"
                quote_PE=name+formatted_date+str(Strike_Prices[i])+"PE"
                call_list.append(quote_CE)
                put_list.append(quote_PE)

            for j in range(len(Strike_Prices)):
                atm_token_ce=kite.ltp("BFO:"+call_list[j])
                atm_token_pe=kite.ltp("BFO:"+put_list[j])
                ATM_Token_CE=atm_token_ce["BFO:"+call_list[j]]['instrument_token']
                ATM_Token_PE=atm_token_pe["BFO:"+put_list[j]]['instrument_token']
                token_CE.append(ATM_Token_CE)
                token_PE.append(ATM_Token_PE)

            call_put_dict["quote_call"]=call_list
            call_put_dict["quote_put"]=put_list
            call_put_dict["token_call"]=token_CE
            call_put_dict["token_put"]=token_PE
            call_put_dict["Strike Prices"]=Strike_Prices

            print(call_put_dict)

            with open(path+"Call_put_quote_token.txt",'w') as file:
                file.write(str(call_put_dict))

        else:

            for i in range(len(Strike_Prices)):
                quote_CE=name+formatted_date+str(Strike_Prices[i])+"CE"
                quote_PE=name+formatted_date+str(Strike_Prices[i])+"PE"
                call_list.append(quote_CE)
                put_list.append(quote_PE)

            for j in range(len(Strike_Prices)):
                atm_token_ce=kite.ltp("NFO:"+call_list[j])
                atm_token_pe=kite.ltp("NFO:"+put_list[j])
                ATM_Token_CE=atm_token_ce["NFO:"+call_list[j]]['instrument_token']
                ATM_Token_PE=atm_token_pe["NFO:"+put_list[j]]['instrument_token']
                token_CE.append(ATM_Token_CE)
                token_PE.append(ATM_Token_PE)

            call_put_dict["quote_call"]=call_list
            call_put_dict["quote_put"]=put_list
            call_put_dict["token_call"]=token_CE
            call_put_dict["token_put"]=token_PE
            call_put_dict["Strike Prices"]=Strike_Prices

            print(call_put_dict)

            with open(path+"Call_put_quote_token.txt",'w') as file:
                file.write(str(call_put_dict))

    elif Month_end==1:

        from datetime import datetime

        call_list=[]
        put_list=[]
        token_CE=[]
        token_PE=[]
        call_put_dict={}
        # parsed_date = datetime.strptime(expiry, '%d-%b-%Y')
        # formatted_date = parsed_date.strftime('%Y%b').upper()


        formatted_date=date_time_format.date_time_format()

        if name=="SENSEX":
            for i in range(len(Strike_Prices)):
                quote_CE=name+formatted_date+str(Strike_Prices[i])+"CE"
                quote_PE=name+formatted_date+str(Strike_Prices[i])+"PE"
                call_list.append(quote_CE)
                put_list.append(quote_PE)


            for j in range(len(Strike_Prices)):
                atm_token_ce=kite.ltp("BFO:"+call_list[j])
                atm_token_pe=kite.ltp("BFO:"+put_list[j])
                ATM_Token_CE=atm_token_ce["BFO:"+call_list[j]]['instrument_token']
                ATM_Token_PE=atm_token_pe["BFO:"+put_list[j]]['instrument_token']
                token_CE.append(ATM_Token_CE)
                token_PE.append(ATM_Token_PE)


            call_put_dict["quote_call"]=call_list
            call_put_dict["quote_put"]=put_list
            call_put_dict["token_call"]=token_CE
            call_put_dict["token_put"]=token_PE
            call_put_dict["Strike Prices"]=Strike_Prices

            print(call_put_dict)

            with open(path+"Call_put_quote_token.txt",'w') as file:
                file.write(str(call_put_dict))

        else:
            for i in range(len(Strike_Prices)):
                quote_CE=name+formatted_date+str(Strike_Prices[i])+"CE"
                quote_PE=name+formatted_date+str(Strike_Prices[i])+"PE"
                call_list.append(quote_CE)
                put_list.append(quote_PE)


            for j in range(len(Strike_Prices)):
                atm_token_ce=kite.ltp("NFO:"+call_list[j])
                atm_token_pe=kite.ltp("NFO:"+put_list[j])
                ATM_Token_CE=atm_token_ce["NFO:"+call_list[j]]['instrument_token']
                ATM_Token_PE=atm_token_pe["NFO:"+put_list[j]]['instrument_token']
                token_CE.append(ATM_Token_CE)
                token_PE.append(ATM_Token_PE)


            call_put_dict["quote_call"]=call_list
            call_put_dict["quote_put"]=put_list
            call_put_dict["token_call"]=token_CE
            call_put_dict["token_put"]=token_PE
            call_put_dict["Strike Prices"]=Strike_Prices

            print(call_put_dict)

            with open(path+"Call_put_quote_token.txt",'w') as file:
                file.write(str(call_put_dict))            

    else:
        pass

def strike_update(expiry,name,closing_price):
    global path
    global content_enctoken

    instrument=["NIFTY 50","NIFTY BANK","NIFTY FIN SERVICE","NIFTY MID SELECT","SENSEX"]
    Strike_interval=[50,100,50,25,100]

    enctoken = content_enctoken

    kite = KiteApp(enctoken=enctoken)

    if name=="NIFTY":
        final_new=Intraday_live_data.getoptionchain(name,expiry)
        final_new.reset_index(drop=True, inplace=True)

        Nifty_current_price=closing_price

        index = (final_new['strikePrice'] - Nifty_current_price).abs().idxmin()
        ATM_strike_price=final_new['strikePrice'].iloc[index]

        ATM_Plus_one=ATM_strike_price+Strike_interval[0]
        ATM_Minus_one=ATM_strike_price-Strike_interval[0]

        strike_price_list_new=[ATM_strike_price,ATM_Plus_one,ATM_Minus_one]

        quote_token_computation(strike_price_list_new,name,expiry)

    elif name=="BANKNIFTY":
        final_new=Intraday_live_data.getoptionchain(name,expiry)
        final_new.reset_index(drop=True, inplace=True)

        BankNifty_current_price=closing_price

        index = (final_new['strikePrice'] - BankNifty_current_price).abs().idxmin()
        ATM_strike_price=final_new['strikePrice'].iloc[index]

        ATM_Plus_one=ATM_strike_price+Strike_interval[1]
        ATM_Minus_one=ATM_strike_price-Strike_interval[1]

        strike_price_list_new=[ATM_strike_price,ATM_Plus_one,ATM_Minus_one]
        quote_token_computation(strike_price_list_new,name,expiry)

    elif name=="FINNIFTY":
        final_new=Intraday_live_data.getoptionchain(name,expiry)
        final_new.reset_index(drop=True, inplace=True)

        FinNifty_current_price=closing_price

        index = (final_new['strikePrice'] - FinNifty_current_price).abs().idxmin()
        ATM_strike_price=final_new['strikePrice'].iloc[index]

        ATM_Plus_one=ATM_strike_price+Strike_interval[2]
        ATM_Minus_one=ATM_strike_price-Strike_interval[2]

        strike_price_list_new=[ATM_strike_price,ATM_Plus_one,ATM_Minus_one]   
        quote_token_computation(strike_price_list_new,name,expiry)

    elif name=="MIDCPNIFTY":

        start=8700
        end=12100

        itteration=(end-start)/Strike_interval[3]

        strike_list=[]

        for i in range(int(itteration)):
            strike=start+Strike_interval[3]*i
            strike_list.append(strike)

        MIDCPNifty_current_price=closing_price

        index=find_closest_index(strike_list,int(MIDCPNifty_current_price))
        ATM_strike_price=strike_list[index]

        ATM_Plus_one=ATM_strike_price+Strike_interval[3]
        ATM_Minus_one=ATM_strike_price-Strike_interval[3]

        strike_price_list_new=[ATM_strike_price,ATM_Plus_one,ATM_Minus_one]   
        quote_token_computation(strike_price_list_new,name,expiry)

    elif name=="SENSEX":

        start=63700
        end=75400

        itteration=(end-start)/Strike_interval[4]

        strike_list=[]

        for i in range(int(itteration)):
            strike=start+Strike_interval[4]*i
            strike_list.append(strike)

        Sensexcurrent_price=closing_price

        index=find_closest_index(strike_list,int(Sensexcurrent_price))
        ATM_strike_price=strike_list[index]

        ATM_Plus_one=ATM_strike_price+Strike_interval[4]
        ATM_Minus_one=ATM_strike_price-Strike_interval[4]

        strike_price_list_new=[ATM_strike_price,ATM_Plus_one,ATM_Minus_one]   
        quote_token_computation(strike_price_list_new,name,expiry)
    else:
        pass

################################    Segment Selection and token Generation  #####################################

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


def inital_computation():
    global name
    global specific_date
    global path

    with open(path+"Call_put_quote_token.txt","r") as file:
        content_quote_token=file.read()

    quote_token = ast.literal_eval(content_quote_token)

    call_list=quote_token['quote_call']
    put_list=quote_token['quote_put']
    call_token=quote_token['token_call']
    put_token=quote_token['token_put']
    Strike_Prices=quote_token['Strike Prices']

def create_plot(frame2):
    global canvas2, axs2
    
    fig, axs2 = plt.subplots(nrows=1, ncols=1, figsize=(20, 10))
    axs2.set_xlabel('Time')
    axs2.set_ylabel('Cumulative Bullishness by sellers (in Lakhs)')
    axs2.set_title('Bulleshness Contracts by sellers in Lakhs')
    axs2.grid(True)

    canvas2 = FigureCanvasTkAgg(fig, master=frame2)
    canvas2.draw()
    canvas2.get_tk_widget().pack()

    return canvas2, axs2

def update_figure_2(new_Window):
    
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


    update_figure_2(new_Window)


    menubar = Menu(new_Window)
    new_Window.config(menu=menubar)
    menubar.add_command(label="Back to Main Window", command=new_Window.destroy)

    frame5=Frame(new_Window)
    frame5.pack(anchor='nw')

    toolbar_frame5 = ttk.Frame(frame5)  # New frame for toolbar
    toolbar_frame5.pack(anchor="nw")   # Place it at top right corner

    toolbar2 = create_toolbar(canvas2, toolbar_frame5)


def create_plot1(frame3):
    global canvas3, axes
    
    fig, axes = plt.subplots(3, 1, figsize=(20, 10))

    canvas3 = FigureCanvasTkAgg(fig, master=frame3)
    canvas3.draw()
    canvas3.get_tk_widget().pack()

    return canvas3, axes

def update_figure_3(new_Window2):
    
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
        ax.plot(df['Time'], df['Cumulative SB call']/100000, marker='o', linestyle='-', color='red', label=f'Call SB: {Strike_Prices[i]} {In_money[i]}')
        ax.plot(df['Time'], df['Cumulative SB put']/100000, marker='o', linestyle='-', color='green', label=f'Put SB: {Strike_Prices[i]} {In_money[length-1-i]}')
        ax.set_xlabel('Time')
        ax.set_ylabel('Cumulative SB call(in Lakhs)')
        ax.legend()
        ax.tick_params(axis='x', rotation=90)

    plt.tight_layout()

    canvas3.draw()

    print("Updated new window")


def Plot():

    nifty_price=float(entry.get())
    strike_update(expiry_date,name,nifty_price)

    update_figures(nifty_price)


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


    update_figure_3(new_Window2)


    menubar = Menu(new_Window2)
    new_Window2.config(menu=menubar)
    menubar.add_command(label="Back to Main Window", command=new_Window2.destroy)


    frame6=Frame(new_Window2)
    frame6.pack(anchor='nw')

    toolbar_frame6 = ttk.Frame(frame6)  # New frame for toolbar
    toolbar_frame6.pack(anchor="nw")   # Place it at top right corner

    toolbar3 = create_toolbar(canvas3, toolbar_frame6)

def update_figures(closing_price):

    global name
    global axs1, axs2
    global specific_date
    global Strike_Prices

    axs1[0].clear()
    axs1[1].clear()
    axs1[2].clear()
    # axs2.clear()

    color_ce_list=[]
    color_pe_list=[]

    with open(path+"Call_put_quote_token.txt",'r') as file:
        content_strike_price=file.read()

    content_read=ast.literal_eval(content_strike_price)

    Strike_Prices=content_read['Strike Prices']
    token_CE=content_read['token_call']
    token_PE=content_read['token_put']

    import datetime


    for ii in range(len(Strike_Prices)):
        instrument_token_CE = token_CE[ii]
        instrument_token_PE = token_PE[ii]

        from_datetime = datetime.datetime.now() - datetime.timedelta(days=10)     # From last & days
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

        # finial_file.to_csv(path+name+str(Strike_Prices[ii])+".csv",index=False)


        

        color_map_ce = {
        'SB': 'red',
        'LC': 'red',
        'LB': 'green',
        'SC': 'green',
        None: "black",
        0:"black"
        }

        color_map_pe = {
            'LB': 'red',
            'SC': 'red',
            'SB': 'green',
            'LC': 'green',
            None: "black",
            0:"black"
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

        
        ce_bars = ax.bar(index, finial_file["COI CE"]/100000, width=bar_width, color=color_ce, edgecolor='black', label="COI CE")
        pe_bars = ax.bar(index + bar_width, finial_file["COI PE"]/100000, width=bar_width, color=color_pe, edgecolor='black', label="COI PE")

        if i < 2:
            ax.set_xticklabels([])

        ax.set_ylabel("COI in Lakhs")
        ax.set_xticks(index + bar_width / 2)
        ax.set_xticklabels(finial_file.index, rotation=45)

        if i == 0:
            ax.legend(["COI CE (ITM)", "COI PE (OTM)"], title=str(Strike_Prices[i]))
        elif i == 1:
            ax.legend(["COI CE (ATM)", "COI PE (ATM)"], title=str(Strike_Prices[i]))
        elif i == 2:
            ax.legend(["COI CE (OTM)", "COI PE (ITM)"], title=str(Strike_Prices[i]))

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


    plt.tight_layout()

    canvas1.draw()
    print("Updated Parent Window")


global specific_date
global weekday_dates
global Strike_Prices

path="D:/ashu/Finance/algo_trading/Zerodha_GUI/OI_Raw_Data_Collected/"


path_main="D:/ashu/Finance/algo_trading/Zerodha_GUI/Kite_Zerodha-main/Kite_Zerodha-main/"

df=pd.read_csv(path_main+"Enctoke_Expiry_month_end_info.csv")
content_enctoken=df.iloc[0,0]

enctoken = content_enctoken

kite = KiteApp(enctoken=enctoken)

import datetime

with open(path_main+"expiry_date.txt",'r') as file:
    content_expiry_date=file.read()

content_expiry_day=content_expiry_date

########################################################## All Update Here #############################################################
segment=["NIFTY","FINNIFTY","BANKNIFTY","MIDCPNIFTY","SENSEX"]
instrument=["NIFTY 50","NIFTY BANK","NIFTY FIN SERVICE","NIFTY MID SELECT","SENSEX"]

expiry_days=["15-Feb-2024","09-Jan-2024","10-Jan-2024","08-Jan-2024","12-Jan-2024"]

expiry=content_expiry_day
today = datetime.datetime.now().date() 
formatted_date = today.strftime('%Y-%m-%d')
specific_date = formatted_date
Month_end=df.iloc[0,2]
expiry_date=expiry_days[0]
name=segment[0]
instrument_name=instrument[0]

if instrument=="SENSEX":
    Sensex_current_price=kite.ltp([f"BSE:{instrument_name}"])
    closing_price=Sensex_current_price[f'BSE:{instrument_name}']['last_price']
else:
    nse_current_price=kite.ltp([f"NSE:{instrument_name}"])
    closing_price=nse_current_price[f'NSE:{instrument_name}']['last_price']

strike_update(expiry_date,name,closing_price)

################################################################# All Update Here #####################################################

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

# frame2 = ttk.Frame(scrollable_content)
# frame2.pack(fill="both", expand=True)

fig1, axs1 = plt.subplots(nrows=3, ncols=1, figsize=(20, 20))
for ax in axs1:
    ax.plot([], [])
    ax.set_xlim(0, 10)
    ax.set_ylim(-2, 2)

canvas1 = FigureCanvasTkAgg(fig1, master=frame1)
canvas1.draw()
canvas1.get_tk_widget().pack()


# toolbar_frame1 = ttk.Frame(frame1)  # New frame for toolbar
# toolbar_frame1.pack(anchor="ne")   # Place it at top right corner

# toolbar1 = create_toolbar(canvas1, toolbar_frame1)

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

root.config(menu=menubar)

frame4=Frame(root)
frame4.pack(anchor='nw')

l1=Label(frame4,text="Enter Nifty Price")
l1.pack()

entry = Entry(frame4)
entry.pack()

plotting_button=Button(frame4,text='Plot',command=Plot)
plotting_button.pack()

toolbar_frame4 = ttk.Frame(frame4)  # New frame for toolbar
toolbar_frame4.pack(anchor="ne")   # Place it at top right corner

toolbar4 = create_toolbar(canvas1, toolbar_frame4)

update_figures(closing_price)

root.bind("<MouseWheel>", on_mousewheel)

root.mainloop()