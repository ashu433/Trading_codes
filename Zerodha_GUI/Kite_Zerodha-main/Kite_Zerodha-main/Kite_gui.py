import datetime
from kite_trade import *
import pandas as pd

path_main="D:/ashu/Finance/algo_trading/Zerodha_GUI/Kite_Zerodha-main/Kite_Zerodha-main/"

with open(path_main+"Option_Futures_info.txt",'r') as file:
    content=file.read()

content=list(content)
print(content[0])