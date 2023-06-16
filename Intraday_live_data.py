import requests
import pandas as pd
import time
import matplotlib.pyplot as plt
import json

sesi=requests.Session()
headers={}
headers['user-agent']='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'
a=sesi.get("https://www.nseindia.com/",headers=headers,timeout=20)

indices=["NIFTY","BANKNIFTY","FINNIFTY"]

def fetch_option_chain(scrip):
  if scrip in indices:
    url=f'https://www.nseindia.com/api/option-chain-indices?symbol={scrip}'
  else:
    stock=scrip.replace("&","%26")
    url=f"https://www.nseindia.com/api/option-chain-equities?symbol={stock}"


  a=sesi.get(url,headers=headers)
  return a.json()['records']

def getoptionchain(name,expiry):
  optionchain=pd.DataFrame()
  option_chain_record=fetch_option_chain(name)
  option_chain_data=option_chain_record['data']
  option_chain_data_df=pd.DataFrame(option_chain_data)
  option_chain_data_df=option_chain_data_df[(option_chain_data_df.expiryDate==expiry)]

  option_chain_ce=pd.DataFrame()
  option_chain_ce["CE"]=option_chain_data_df["CE"]

  Option_chain_ce_Expand=pd.concat([option_chain_ce.drop(["CE"],axis=1), option_chain_ce["CE"].apply(pd.Series)],axis=1)

  option_chain_pe=pd.DataFrame()
  option_chain_pe["PE"]=option_chain_data_df["PE"]

  Option_chain_pe_Expand=pd.concat([option_chain_pe.drop(["PE"],axis=1), option_chain_pe["PE"].apply(pd.Series)],axis=1)

  optionchain["CE_OI"]=Option_chain_ce_Expand['openInterest']
  optionchain["CE_CHNG_IN_OI"]=Option_chain_ce_Expand['changeinOpenInterest']
  optionchain["CE_Volume"]=Option_chain_ce_Expand["totalTradedVolume"]
  optionchain["CE_IV"]=Option_chain_ce_Expand["impliedVolatility"]
  optionchain["CE_LTP"]=Option_chain_ce_Expand["lastPrice"]
  optionchain["CE_CHNG"]=Option_chain_ce_Expand["change"]
  optionchain["CE_BID_QTY"]=Option_chain_ce_Expand["bidQty"]
  optionchain["CE_BID_PRICE"]=Option_chain_ce_Expand["bidprice"]
  optionchain["CE_ASK_PRICE"]=Option_chain_ce_Expand["askPrice"]
  optionchain["CE_ASK_QTY"]=Option_chain_ce_Expand["askQty"]

  optionchain["strikePrice"]=option_chain_data_df["strikePrice"]

  
  optionchain["PE_CHNG_IN_OI"]=Option_chain_pe_Expand['changeinOpenInterest']
  optionchain["PE_Volume"]=Option_chain_pe_Expand["totalTradedVolume"]
  optionchain["PE_IV"]=Option_chain_pe_Expand["impliedVolatility"]
  optionchain["PE_LTP"]=Option_chain_pe_Expand["lastPrice"]
  optionchain["PE_CHNG"]=Option_chain_pe_Expand["change"]
  optionchain["PE_BID_QTY"]=Option_chain_pe_Expand["bidQty"]
  optionchain["PE_BID_PRICE"]=Option_chain_pe_Expand["bidprice"]
  optionchain["PE_ASK_PRICE"]=Option_chain_pe_Expand["askPrice"]
  optionchain["PE_ASK_QTY"]=Option_chain_pe_Expand["askQty"]
  optionchain["PE_OI"]=Option_chain_pe_Expand['openInterest']
  optionchain["Nifty Current Price"] = Option_chain_pe_Expand['underlyingValue']

  return optionchain

def PCR_calculation(Option_chain,present_nifty_value):
  Option_chain=Option_chain.reset_index(drop=True)
  present_nifty_value=present_nifty_value
  index = (Option_chain['strikePrice'] - present_nifty_value).abs().idxmin()
  near_option_ATM=Option_chain.iloc[index]
  near_option_ATM_1_Plus=Option_chain.iloc[index+1]
  near_option_ATM_1_minus=Option_chain.iloc[index-1]
  near_option_ATM_2_Plus=Option_chain.iloc[index+2]
  near_option_ATM_2_minus=Option_chain.iloc[index-2]
  near_option_ATM_3_Plus=Option_chain.iloc[index+3]
  near_option_ATM_3_minus=Option_chain.iloc[index-3]
  near_option_ATM_4_Plus=Option_chain.iloc[index+4]
  near_option_ATM_4_minus=Option_chain.iloc[index-4]
  new=pd.concat([near_option_ATM_4_minus,near_option_ATM_3_minus,near_option_ATM_2_minus,near_option_ATM_1_minus,near_option_ATM,near_option_ATM_1_Plus,near_option_ATM_2_Plus,near_option_ATM_3_Plus,near_option_ATM_4_Plus],axis=1)
  final_new=new.T
  x=final_new["PE_OI"]/final_new["CE_OI"]
  y=final_new["CE_OI"]/final_new["PE_OI"]
  newest=pd.concat([final_new,pd.DataFrame(x)],axis=1)
  newest=newest.rename(columns={0:"PCR"})
  newest=pd.concat([newest,pd.DataFrame(y)],axis=1)
  newest=newest.rename(columns={0:"CPR"})
  return newest

def plotting(newest):
    S_R_data=newest[["CPR","PCR"]]
    S_R_data = S_R_data.round(2)
    S_R_data.set_index(newest["strikePrice"], inplace=True)
    ax = S_R_data.plot(kind='bar',color=['blue', 'red'], edgecolor='black')
    for i, bar in enumerate(ax.containers):
        ax.bar_label(bar, label_type='edge', fontsize=10)
    ax.legend(['Resistance','Support'])
    fig = plt.gcf()
    fig.set_size_inches(8, 8)
    plt.show()


if __name__=='__main__':  
    pass