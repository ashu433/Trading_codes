import Intraday_live_data
import pandas as pd
import time
from datetime import  timedelta, datetime
import schedule
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from tkinter import Tk, Button, Frame
import threading
from tkinter import *
from matplotlib.figure import Figure


path="D:/ashu/Finance/algo_trading/Option_chain_data/"

def plot_live_data(csv_file_path):
    # Create a figure and axes for the plots
    fig, axes = plt.subplots(2, 3, figsize=(20, 20))
    fig.subplots_adjust(hspace=0.1)

    # Set the titles and labels for each subplot

    titles = ['COI on call side VS Time', 'Premium on Call side VS Time',
              'COI by Volume Call VS Time', 'COI on put side VS Time',
              'Premium on Put side VS Time', 'COI by Volume Put VS Time']
    xlabels = ['Time', 'Time', 'Time', 'Time', 'Time', 'Time']
    ylabels = ['COI on Call side', 'Call side premium', 'COI by Volume Call', 'COI on Put side',
               'Put side premium', 'COI by Volume Put']


    # Create a Tkinter window
    root = Tk()

    root.title("Open Interest Options GUI")

    button_frame = Frame(root)
    button_frame.pack(anchor='nw',fill=X)

############################## Parameters Frame ################################################

    f1=Frame(root,bg="grey",borderwidth=6,relief=SUNKEN)
    f1.pack(side=LEFT,fill="y")

    l1=Label(f1,text="Parameters",font="comicsansms 9 bold",bg="red",relief=SUNKEN)
    l1.grid()

    l2=Label(f1, text="Strike Prices to Plot:",font="comicsansms 9 bold")
    l2.grid(row=1,pady=10)

    entry_1 = Entry(f1)
    entry_1.grid(row=2)

    l3=Label(f1, text="Strike Prices to remove:",font="comicsansms 9 bold")
    l3.grid(row=4,pady=10)

    entry_2 = Entry(f1)
    entry_2.grid(row=5)

    l4=Label(f1, text="ATM",font="comicsansms 9 bold")
    l4.grid(row=7,pady=10)

    l5=Label(f1, text="ATM+1",font="comicsansms 9 bold")
    l5.grid(row=8,pady=4)

    l6=Label(f1, text="ATM-1",font="comicsansms 9 bold")
    l6.grid(row=9,pady=4)

    l7=Label(f1, text="ATM+2",font="comicsansms 9 bold")
    l7.grid(row=10,pady=4)

    l8=Label(f1, text="ATM-2",font="comicsansms 9 bold")
    l8.grid(row=11,pady=4)

    l9=Label(f1, text="Last Update",font="comicsansms 9 bold")
    l9.grid(row=12,pady=10)

    def insert_strike_price():
        strike_prices = entry_1.get().split(',')
        strike_prices = [int(price.strip()) for price in strike_prices if price.strip() != '']
        with open("Strike_prices.txt","a") as file:
            for items in strike_prices:
                file.write(str(items)+"\n")

    def remove_strike_price():
        strike_prices = entry_2.get().split(',')
        strike_prices = [int(price.strip()) for price in strike_prices if price.strip() != '']
        print(strike_prices)
        with open("Strike_prices.txt",'r') as file:
            lines = file.readlines()
        
        updated_lines = []

        for line in lines:
            if str(strike_prices[0]) not in line:
                updated_lines.append(line)


        with open("Strike_prices.txt", 'w') as file:
            file.writelines(updated_lines)


################################ Parameters Frame ################################################


    # Create a canvas for the plots and embed it in the window
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().pack()
    # Variables to keep track of the legend visibility for each subplot
    legend_visible = [False] * len(titles)

    # Function to toggle the visibility of legends
    def toggle_legend(i):
        nonlocal legend_visible
        legend_visible[i] = not legend_visible[i]
        axes.flat[i].legend().set_visible(legend_visible[i])
        canvas.draw()

    toolbar=NavigationToolbar2Tk(canvas,button_frame,pack_toolbar=False)
    toolbar.update()
    toolbar.pack(side=RIGHT,anchor='ne')

    buttons = []
    for i, title in enumerate(titles):
        button = Button(button_frame, text=f'Toggle Legend - Plot {i+1}',
                        command=lambda i=i: toggle_legend(i))
        button.pack(side='left',anchor='nw')
        buttons.append(button)
    

    # Function to update the plots with new data
    def update_plots():
        # Read the CSV file into a dataframe
        data = pd.read_csv(csv_file_path)
        x=data.shape[0]
        Last_data_updated_time=data.iloc[x-1,0]

        ############################################ ATM STRIKE PRICE COMPUTATION ##############################################################

        name="NIFTY"
        expiry="31-Aug-2023"

        final_new=Intraday_live_data.getoptionchain(name,expiry)
        final_new.reset_index(drop=True, inplace=True)
        Nifty_current_price=final_new["Nifty Current Price"].iloc[1]
        index = (final_new['strikePrice'] - Nifty_current_price).abs().idxmin()
        ATM_strike_price=final_new['strikePrice'].iloc[index]
        ATM_Plus_one=ATM_strike_price+50
        ATM_Plus_two=ATM_strike_price+100
        ATM_Minus_one=ATM_strike_price-50
        ATM_Minus_two=ATM_strike_price-100


        l4.config(text=f"ATM: {ATM_strike_price}")
        l5.config(text=f"ATM+1: {ATM_Plus_one}")
        l6.config(text=f"ATM-1: {ATM_Minus_one}")
        l7.config(text=f"ATM+2: {ATM_Plus_two}")
        l8.config(text=f"ATM-2: {ATM_Minus_two}")
        l9.config(text=f"Last Update: {Last_data_updated_time}")
        ############################################ ATM STRIKE PRICE COMPUTATION ##############################################################

        with open("Strike_prices.txt", "r") as file:
            lines = file.readlines()

        # Process the lines and create a list of dictionaries
        data_1 = []
        for line in lines:
            line = line.strip()
            if line:
                data_1.append({"Value": line})

        Strike_Price_list = pd.DataFrame(data_1)

        Strike_Price_list = Strike_Price_list.rename(columns={'Value': 'strikePrice'})

        Strike_Price_list=Strike_Price_list.astype(int)

        merged_df = pd.merge(data, Strike_Price_list, left_on='strikePrice', right_on='strikePrice')

        grouped_data = merged_df.groupby('strikePrice')

        # Clear the previous plots
        for ax in axes.flat:
            ax.clear()

        # Plot the data in each subplot
        for i, (title, xlabel, ylabel) in enumerate(zip(titles, xlabels, ylabels)):
            ax = axes.flat[i]
            for strike_price, group in grouped_data:
                ######################################################### CALL SIDE PLOT #######################################################
                if (strike_price>ATM_strike_price):
                    if i == 0:
                        ax.plot(group['Time'], group['CE_CHNG_IN_OI'], label=f'Strike Price: {strike_price}', linestyle="dashed")
                else:
                    if i == 0:
                        ax.plot(group['Time'], group['CE_CHNG_IN_OI'], label=f'Strike Price: {strike_price}', linestyle="solid")

                if (strike_price>ATM_strike_price):
                    if i == 1:
                        ax.plot(group['Time'], group['CE_LTP'], label=f'Strike Price: {strike_price}', linestyle="dashed")
                else:
                    if i == 1:
                        ax.plot(group['Time'], group['CE_LTP'], label=f'Strike Price: {strike_price}', linestyle="solid")

                if (strike_price>ATM_strike_price):
                    if i == 2:
                        ax.plot(group['Time'], group['COI_by_Volume_Call'], label=f'Strike Price: {strike_price}', linestyle="dashed")
                else:
                    if i == 2:
                        ax.plot(group['Time'], group['COI_by_Volume_Call'], label=f'Strike Price: {strike_price}', linestyle="solid")

                ######################################################### PUT SIDE PLOT #######################################################
                if (strike_price<ATM_strike_price):
                    if i == 3:
                        ax.plot(group['Time'], group['PE_CHNG_IN_OI'], label=f'Strike Price: {strike_price}', linestyle="dashed")
                else:
                    if i == 3:
                        ax.plot(group['Time'], group['PE_CHNG_IN_OI'], label=f'Strike Price: {strike_price}', linestyle="solid")

                if (strike_price<ATM_strike_price):
                    if i == 4:
                        ax.plot(group['Time'], group['PE_LTP'], label=f'Strike Price: {strike_price}', linestyle="dashed")
                else:
                    if i == 4:
                        ax.plot(group['Time'], group['PE_LTP'], label=f'Strike Price: {strike_price}', linestyle="solid")

                if (strike_price<ATM_strike_price):
                    if i == 5:
                        ax.plot(group['Time'], group['COI_by_Volume_Put'], label=f'Strike Price: {strike_price}', linestyle="dashed")
                else:
                    if i == 5:
                        ax.plot(group['Time'], group['COI_by_Volume_Put'], label=f'Strike Price: {strike_price}', linestyle="solid")

                    

            # Check if current subplot is in the top row
            if i < 3:
                ax.set_xticklabels([])

            ax.set_ylabel(ylabel)
            ax.set_title(title)
            ax.legend().set_visible(legend_visible[i])
            ax.tick_params(axis='x', rotation=90)

        # Refresh the canvas
        canvas.draw()

        # Schedule the next update
        root.after(300000, update_plots)


    # Schedule the first update
    root.after(0, update_plots)

    

    button_plot = Button(f1, text="Plot", command=insert_strike_price)
    button_plot.grid(row=3,pady=10)

    button_remove = Button(f1, text="Remove Plot", command=remove_strike_price)
    button_remove.grid(row=6,pady=10)

    toolbar=NavigationToolbar2Tk(canvas,root,pack_toolbar=False)
    toolbar.update()
    toolbar.pack()



    # Run the Tkinter event loop
    root.mainloop()



# Set the path to your CSV file
csv_file_path = path+'Option_chain_data_saving.csv'


# Call the function to plot the live data
plot_live_data(csv_file_path)
