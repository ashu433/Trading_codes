import Intraday_live_data
import pandas as pd
import time
from datetime import  timedelta, datetime
import schedule
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import Tk, Button, Frame
import threading


path="D:/ashu/Finance/algo_trading/Option_chain_data/"

def plot_live_data(csv_file_path):
    # Create a figure and axes for the plots
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    fig.subplots_adjust(hspace=0.5)

    # Set the titles and labels for each subplot

    titles = ['COI on call side VS Time', 'Premium on Call side VS Time',
              'COI by Volume Call VS Time', 'COI on put side VS Time',
              'Premium on Put side VS Time', 'COI by Volume Put VS Time']
    xlabels = ['Time', 'Time', 'Time', 'Time', 'Time', 'Time']
    ylabels = ['COI on Call side', 'Call side premium', 'COI by Volume Call', 'COI on Put side',
               'Put side premium', 'COI by Volume Put']

    # titles = ['COI on call side VS Time', 'COI on put side VS Time',
    #           'Premium on Call side VS Time', 'Premium on Put side VS Time',
    #           'COI by Volume Call VS Time', 'COI by Volume Put VS Time']
    # xlabels = ['Time', 'Time', 'Time', 'Time', 'Time', 'Time']
    # ylabels = ['COI on Call side', 'COI on Put side', 'Call side premium', 'Put side premium',
    #            'COI by Volume Call', 'COI by Volume Put']

    # Create a Tkinter window
    root = Tk()

    # Create a frame to hold the buttons
    button_frame = Frame(root)
    button_frame.pack()

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

    # Create buttons for each subplot
    buttons = []
    for i, title in enumerate(titles):
        button = Button(button_frame, text=f'Toggle Legend - Plot {i+1}',
                        command=lambda i=i: toggle_legend(i))
        button.pack(side='left')
        buttons.append(button)

    # Function to update the plots with new data
    def update_plots():
        # Read the CSV file into a dataframe
        data = pd.read_csv(csv_file_path)

        # Group the data by 'strikePrice'
        grouped_data = data.groupby('strikePrice')

        # Clear the previous plots
        for ax in axes.flat:
            ax.clear()

        # Plot the data in each subplot
        for i, (title, xlabel, ylabel) in enumerate(zip(titles, xlabels, ylabels)):
            ax = axes.flat[i]
            for strike_price, group in grouped_data:
                if i == 0:
                    ax.plot(group['Time'], group['CE_CHNG_IN_OI'], label=f'Strike Price: {strike_price}')
                elif i == 1:
                    ax.plot(group['Time'], group['CE_LTP'], label=f'Strike Price: {strike_price}')
                elif i == 2:
                    ax.plot(group['Time'], group['COI_by_Volume_Call'], label=f'Strike Price: {strike_price}')
                elif i == 3:
                    ax.plot(group['Time'], group['PE_CHNG_IN_OI'], label=f'Strike Price: {strike_price}')
                elif i == 4:
                    ax.plot(group['Time'], group['PE_LTP'], label=f'Strike Price: {strike_price}')
                elif i == 5:
                    ax.plot(group['Time'], group['COI_by_Volume_Put'], label=f'Strike Price: {strike_price}')


                # if i == 0:
                #     ax.plot(group['Time'], group['CE_CHNG_IN_OI'], label=f'Strike Price: {strike_price}')
                # elif i == 1:
                #     ax.plot(group['Time'], group['PE_CHNG_IN_OI'], label=f'Strike Price: {strike_price}')
                # elif i == 2:
                #     ax.plot(group['Time'], group['CE_LTP'], label=f'Strike Price: {strike_price}')
                # elif i == 3:
                #     ax.plot(group['Time'], group['PE_LTP'], label=f'Strike Price: {strike_price}')
                # elif i == 4:
                #     ax.plot(group['Time'], group['COI_by_Volume_Call'], label=f'Strike Price: {strike_price}')
                # elif i == 5:
                #     ax.plot(group['Time'], group['COI_by_Volume_Put'], label=f'Strike Price: {strike_price}')

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

    # Run the Tkinter event loop
    root.mainloop()


# Set the path to your CSV file
csv_file_path = path+'Option_chain_data_saving.csv'

# Call the function to plot the live data
plot_live_data(csv_file_path)
