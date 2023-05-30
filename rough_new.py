import Daily_Option_chain_data
import pandas as pd


path="D:/ashu/Finance/algo_trading/Option_chain_data/"
file_1="data1.xlsx"
coloumns_number=77
length_of_time=25
time_array=[11,9,23]

finial_file=Daily_Option_chain_data.Daily_option_chain_report_generation(path+file_1,coloumns_number,length_of_time)

#finial_file.to_excel(path+'finial_file.xlsx', index=False)

for i in range(len(time_array)):
    file=f"data{i+2}.xlsx"
    time_length=time_array[i]
    file_gen=Daily_Option_chain_data.Daily_option_chain_report_generation(path+file,coloumns_number,time_length)
    print(i)
    finial_file = pd.concat([finial_file, file_gen], axis=0)

finial_file.to_excel(path+'full_and_finial_file.xlsx', index=False)


# open_price=18338.1
# close_price=18202.4
# Open_strike_price = round(open_price / 50) * 50
# Close_strike_price=round(close_price / 50) * 50
# x_min=min(Open_strike_price,Close_strike_price)
# y_max=max(Open_strike_price,Close_strike_price)
# x_min=x_min-50
# y_max=y_max

# file_1=pd.read_excel(path+"full_and_finial_file.xlsx")
# filtered_df = file_1[(file_1['strikePrice'] >= x_min) & (file_1['strikePrice'] <= y_max)]



# import matplotlib.pyplot as plt

# grouped_data = filtered_df.groupby('strikePrice')

# # Create the subplots
# fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 10))

# # Plot on the first subplot
# for strike_price, group in grouped_data:
#     ax1.plot(group['Time'], group['CE_CHNG_IN_OI'], label=f'Strike Price: {strike_price}')
# ax1.set(xlabel='Time', ylabel='COI')
# ax1.set_title('Change in OI on call side VS Time')
# ax1.grid(True)
# ax1.autoscale(enable=True, axis='both', tight=True)
# ax1.autoscale(enable=True, axis='x', tight=True)
# ax1.set_xlim(group['Time'].iloc[0], group['Time'].iloc[-1])
# ax1.legend()

# # Plot on the second subplot
# for strike_price, group in grouped_data:
#     ax2.plot(group['Time'], group['CE_CHNG'], label=f'Strike Price: {strike_price}')
# ax2.set(xlabel='Time', ylabel='COP')
# ax2.set_title('Change in Premium on call side VS Time')
# ax2.grid(True)
# ax2.autoscale(enable=True, axis='both', tight=True)
# ax2.autoscale(enable=True, axis='x', tight=True)
# ax2.set_xlim(group['Time'].iloc[0], group['Time'].iloc[-1])
# ax2.legend()

# # Set up the zooming functionality
# def on_scroll(event):
#     for ax in [ax1, ax2]:
#         x_min, x_max = ax.get_xlim()
#         x_range = x_max - x_min
#         if event.button == 'up':
#             ax.set(xlim=(x_min + x_range * 0.1, x_max - x_range * 0.1))
#         elif event.button == 'down':
#             ax.set(xlim=(x_min - x_range * 0.1, x_max + x_range * 0.1))
#     plt.draw()

# fig.canvas.mpl_connect('scroll_event', on_scroll)


# ax1.set_xticklabels([])


# plt.xticks(rotation=90)

# # Show the plots
# plt.tight_layout()
# plt.show()