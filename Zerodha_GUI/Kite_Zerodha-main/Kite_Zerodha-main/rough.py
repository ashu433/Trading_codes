from kite_trade import *
import pandas as pd
import numpy as np


path_main="D:/ashu/Finance/algo_trading/Zerodha_GUI/Kite_Zerodha-main/Kite_Zerodha-main/"
df=pd.read_csv(path_main+"Enctoke_Expiry_month_end_info.csv")
content_enctoken=df.iloc[0,0]
enctoken = content_enctoken
kite = KiteApp(enctoken=enctoken)

Nifty=kite.ltp(["NSE:NIFTY 50"])
Nifty_Spot_price=Nifty['NSE:NIFTY 50']['last_price']
print(Nifty_Spot_price)


# Vix=kite.ltp(["NSE:INDIA VIX"])
# Present_vol=Vix['NSE:INDIA VIX']['last_price']
# print(Present_vol)

Present_vol=13

range=((Present_vol/np.sqrt(252))*Nifty_Spot_price)/100
print(range)

offset=round(range,2)
offset = round(offset / 50) * 50
offset=int(offset)
print(offset)