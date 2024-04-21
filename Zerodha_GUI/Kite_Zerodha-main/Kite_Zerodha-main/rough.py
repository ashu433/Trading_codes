# import json

# def writing_market_status(dict_name,text_file="Market_status.txt"):
#     with open(Path_backtest_Report+text_file, 'w') as file:
#         json.dump(dict_name, file)

# def reading_market_status(text_file="Market_status.txt"):
#     with open(Path_backtest_Report+text_file, 'r') as file:
#         json_data = file.read()
#         present_market_status= json.loads(json_data)

#         return present_market_status
    
# def ensure_nested_dict(main_dict, key):
#     if key not in main_dict:
#         main_dict[key] = {}

# def limit_status_set(strike):

#     main_dict=reading_market_status("Running_log.txt")

#     strike=-strike

#     ensure_nested_dict(main_dict, strike)

#     main_dict[strike]["Date"]="22-10-2024"
#     main_dict[strike]["Time"]="09:20:55"
#     main_dict[strike]["Right"]="Call"
#     main_dict[strike]["Order ID"]="1122334455"
#     main_dict[strike]["Status"]="COMPLETE"
#     main_dict[strike]["Type"]="Sell"
#     main_dict[strike]["Initial Price"]=23.6
#     main_dict[strike]["Trailing SL"]=43.5

#     writing_market_status(main_dict,"Running_log.txt")

# initial=0
# Path_backtest_Report="D:/ashu/Finance/algo_trading/Zerodha_GUI/Kite_Zerodha-main/Kite_Zerodha-main/Live_market_data_gathering/"
# # if initial==1:

# #     main_dict={}
# #     writing_market_status(main_dict,"Running_log.txt")
# #     limit_status_set(22000)
# #     # limit_status_set(22800)
# #     # limit_status_set(-22000)
# #     # limit_status_set(-22800)

# # elif initial==0:
# #     limit_status_set(20300)

# # else:
#     # pass

# # main_dict=reading_market_status("Running_log.txt")
# # # print(main_dict[str(22000)]["Order ID"])
# # main_dict[str(22000)]["Order ID"]="tutututututu"
# # writing_market_status(main_dict,"Running_log.txt")

# Active_strike_list_Call=[22500]
# Active_strike_list_Put=[21200,21250]
# reversal_status=0
# max_call_credit_spreads=1
# max_put_credit_spreads=2

# market_status={}
# market_status["Market Trend"]="Trending Up"
# market_status["Active Call Strikes"]=Active_strike_list_Call
# market_status["Active Put Strikes"]=Active_strike_list_Put
# market_status["Reversal status"]=reversal_status
# market_status["Maximum call credit Spread"]=max_call_credit_spreads
# market_status["Maximum put credit Spread"]=max_put_credit_spreads

# with open(Path_backtest_Report+"Market_status.txt", 'w') as file:
#     json.dump(market_status, file)

for i in range(5):
    for k in range(5):
        print(f"i: {i} j: {k}")

        if k==2:
            break
    
    print(f"Broken value of the k is {k}")