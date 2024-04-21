import json
import ast


def writing_market_status(dict_name,text_file="Market_status.txt"):
    with open(Path_backtest_Report+text_file, 'w') as file:
        json.dump(dict_name, file)

def reading_market_status(text_file="Market_status.txt"):
    with open(Path_backtest_Report+text_file, 'r') as file:
        json_data = file.read()
        present_market_status= json.loads(json_data)

        return present_market_status


def ensure_nested_dict(main_dict, key):
    if key not in main_dict:
        main_dict[key] = {}


Path_backtest_Report="D:/ashu/Finance/algo_trading/Zerodha_GUI/Kite_Zerodha-main/Kite_Zerodha-main/Live_market_data_gathering/"

with open(Path_backtest_Report+"Order_log.txt", "r") as file:
    content = file.read()

# target_quote="NIFTY24APR22500CE"
# Strike=22500
# Right="Call"
# Stop_Loss=0

# # Parse the JSON string into a Python object (list of dictionaries)
# list_of_dicts = ast.literal_eval(content)

# for i in range(len(list_of_dicts)):
#     running_log=reading_market_status("Running_log.txt")

#     if list_of_dicts[i]['tradingsymbol']==target_quote and list_of_dicts[i]['order_type']=="SL":

#         Date_time=list_of_dicts[i]['order_timestamp']
#         date, time = Date_time.split()
#         Order_ID=list_of_dicts[i]['order_id']
#         Status_present=list_of_dicts[i]['status']
#         price=list_of_dicts[i]['average_price']

#         Strike=-Strike
#         ensure_nested_dict(running_log, Strike)
#         running_log[Strike]["Date"]=date
#         running_log[Strike]["Time"]=time
#         running_log[Strike]["Right"]=Right
#         running_log[Strike]["Order ID"]=str(Order_ID)
#         running_log[Strike]["Status"]="TRIGGER PENDING"
#         running_log[Strike]["Type"]="Buy Hedges"
#         running_log[Strike]["Initial Price"]=price
#         running_log[Strike]["Trailing SL"]=price

#         writing_market_status(running_log,"Running_log.txt")

# running_log={}
# writing_market_status(running_log,"Running_log.txt")

running_log=reading_market_status("Running_log.txt")
print(running_log[str(-22500)]["Status"])