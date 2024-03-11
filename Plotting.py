import pandas as pd
import matplotlib.pyplot as plt

def plotting(Open_price,Close_price,file):
    open_price=Open_price
    close_price=Close_price
    Open_strike_price = round(open_price / 50) * 50
    Close_strike_price=round(close_price / 50) * 50
    x_min=min(Open_strike_price,Close_strike_price)
    y_max=max(Open_strike_price,Close_strike_price)
    x_min=x_min-50
    y_max=y_max+50

    file_1=pd.read_excel(file)
    filtered_df = file_1[(file_1['strikePrice'] >= x_min) & (file_1['strikePrice'] <= y_max)]

    COI_by_Volume_Call=50*filtered_df["CE_CHNG_IN_OI"]/filtered_df["CE_Volume"]
    filtered_df=pd.concat([filtered_df,pd.DataFrame(COI_by_Volume_Call)],axis=1)
    filtered_df=filtered_df.rename(columns={0:"COI_by_Volume_Call"})

    COI_by_Volume_Put=50*(filtered_df["PE_CHNG_IN_OI"]/filtered_df["PE_Volume"])
    filtered_df=pd.concat([filtered_df,pd.DataFrame(COI_by_Volume_Put)],axis=1)
    filtered_df=filtered_df.rename(columns={0:"COI_by_Volume_Put"})

    grouped_data = filtered_df.groupby('strikePrice')

    titles = ['COI on call side VS Time', 'Premium on Call side VS Time',
              'COI by Volume Call VS Time', 'COI on put side VS Time',
              'Premium on Put side VS Time', 'COI by Volume Put VS Time']
    xlabels = ['Time', 'Time', 'Time', 'Time', 'Time', 'Time']
    ylabels = ['COI on Call side', 'Call side premium', 'COI by Volume Call', 'COI on Put side',
               'Put side premium', 'COI by Volume Put']

    ############ Plotting the data from the grouped_data in the 2 figures such that one figure contain the plot in 2x2 format and another figure contain the plot in 2x2 format

    fig, axes = plt.subplots(2, 3, figsize=(20, 20))
    fig.subplots_adjust(hspace=0.1)

    for i, (title, xlabel, ylabel) in enumerate(zip(titles, xlabels, ylabels)):
        ax = axes.flat[i]
        for strike_price, group in grouped_data:
            if i == 0:
                ax.plot(group['Time'], group['CE_CHNG_IN_OI'], label=f'Strike Price: {strike_price}')
            if i == 1:
                ax.plot(group['Time'], group['CE_LTP'], label=f'Strike Price: {strike_price}')
            if i == 2:
                ax.plot(group['Time'], group['COI_by_Volume_Call'], label=f'Strike Price: {strike_price}')
            if i == 3:
                ax.plot(group['Time'], group['PE_CHNG_IN_OI'], label=f'Strike Price: {strike_price}')
            if i == 4:
                ax.plot(group['Time'], group['PE_LTP'], label=f'Strike Price: {strike_price}')
            if i == 5:
                ax.plot(group['Time'], group['COI_by_Volume_Put'], label=f'Strike Price: {strike_price}')

        if i < 3:
            ax.set_xticklabels([])

        ax.set_ylabel(ylabel)
        ax.set_title(title)
        ax.legend()
        ax.tick_params(axis='x', rotation=90)
        
    plt.show()


path="D:/ashu/Finance/algo_trading/Option_chain_data/"

Open_price=19493.45
Close_price=19564.5

file=path+"full_and_finial_file.xlsx"

plotting(Open_price,Close_price,file)

