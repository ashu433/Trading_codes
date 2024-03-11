from kite_trade import *
import time 
import datetime
import pandas as pd
import ast
import Intraday_live_data
from datetime import datetime
import os
import threading
import date_time_format

path_main="D:/ashu/Finance/algo_trading/Zerodha_GUI/Kite_Zerodha-main/Kite_Zerodha-main/"

df=pd.read_csv(path_main+"Enctoke_Expiry_month_end_info.csv")
content_enctoken=df.iloc[0,0]
content_expiry_day=df.iloc[0,1]
Month_end=df.iloc[0,2]

enctoken = content_enctoken
expiry=content_expiry_day

########### 1 means Yes and 0 means No ##################




def moving_average(quote,token):
    global path
    weightage=[0.2,0.090909,0.039216,0.00995]
    print(quote)
    files_in_min=[".csv","_5_min.csv"]

    for mm in range(len(files_in_min)):
        for k in range(len(quote)):
            data=pd.read_csv(path+quote[k]+files_in_min[mm])
            data=data.iloc[:-1]
            rows=data.shape[0]
            data["EMA 9"]=0
            data["EMA 21"]=0
            data["EMA 50"]=0
            data["EMA 200"]=0

            average_9=data["close"][:9].mean()
            average_21=data["close"][:21].mean()
            average_50=data["close"][:50].mean()
            average_200=data["close"][:200].mean()
            data.iloc[8,6]=average_9
            data.iloc[20,7]=average_21
            data.iloc[49,8]=average_50
            data.iloc[199,9]=average_200

            for i in range(rows):
                if (200+i)<rows:
                    data.iloc[9+i,6]=(data.iloc[9+i,5]-data.iloc[8+i,6])*weightage[0]+data.iloc[8+i,6]
                    data.iloc[21+i,7]=(data.iloc[21+i,5]-data.iloc[20+i,7])*weightage[1]+data.iloc[20+i,7]
                    data.iloc[50+i,8]=(data.iloc[50+i,5]-data.iloc[49+i,8])*weightage[2]+data.iloc[49+i,8]
                    data.iloc[200+i,9]=(data.iloc[200+i,5]-data.iloc[199+i,9])*weightage[3]+data.iloc[199+i,9]
                elif rows<=(200+i)<rows+150:
                    data.iloc[9+i,6]=(data.iloc[9+i,5]-data.iloc[8+i,6])*weightage[0]+data.iloc[8+i,6]
                    data.iloc[21+i,7]=(data.iloc[21+i,5]-data.iloc[20+i,7])*weightage[1]+data.iloc[20+i,7]
                    data.iloc[50+i,8]=(data.iloc[50+i,5]-data.iloc[49+i,8])*weightage[2]+data.iloc[49+i,8]
                elif rows+150<=(200+i)<rows+179:
                    data.iloc[9+i,6]=(data.iloc[9+i,5]-data.iloc[8+i,6])*weightage[0]+data.iloc[8+i,6]
                    data.iloc[21+i,7]=(data.iloc[21+i,5]-data.iloc[20+i,7])*weightage[1]+data.iloc[20+i,7]
                elif rows+179<=(200+i)<rows+191:
                    data.iloc[9+i,6]=(data.iloc[9+i,5]-data.iloc[8+i,6])*weightage[0]+data.iloc[8+i,6]
                else:
                    break
            
            data.to_csv(path+quote[k]+files_in_min[mm],index=False)


def historical(strike_price_list_new,strike_price_to_remove,expiry):
    from datetime import datetime
    global path
    global Month_end

    if Month_end==1:
        quote=[]
        quote_remove=[]
        token=[]

        # parsed_date = datetime.strptime(expiry, '%d-%b-%Y')
        # formatted_date = parsed_date.strftime('%Y%b').upper()
        name="NIFTY"
        formatted_date=date_time_format.date_time_format()

        for ii in range(len(strike_price_list_new)):
            quote_ATM_PE=name+formatted_date+str(strike_price_list_new[ii])+"PE"
            quote_ATM_CE=name+formatted_date+str(strike_price_list_new[ii])+"CE"
            quote.append(quote_ATM_CE)
            quote.append(quote_ATM_PE)

        for iii in range(len(quote)):
            atm_token_pe=kite.ltp("NFO:"+quote[iii])
            ATM_Token=atm_token_pe["NFO:"+quote[iii]]['instrument_token']
            token.append(ATM_Token)

    elif Month_end==0:
        # parsed_date = datetime.strptime(expiry, '%d-%b-%Y')
        # formatted_date = parsed_date.strftime('%y%m%d')
        name="NIFTY"

        # char_list = list(formatted_date)

        # if char_list[2]=='0':
        #     char_list.pop(2)

        formatted_date=date_time_format.date_time_format()

        quote=[]
        quote_remove=[]
        token=[]

        for ii in range(len(strike_price_list_new)):
            quote_ATM_PE=name+formatted_date+str(strike_price_list_new[ii])+"PE"
            quote_ATM_CE=name+formatted_date+str(strike_price_list_new[ii])+"CE"
            quote.append(quote_ATM_CE)
            quote.append(quote_ATM_PE)
        

        for iii in range(len(quote)):
            atm_token_pe=kite.ltp("NFO:"+quote[iii])
            ATM_Token=atm_token_pe["NFO:"+quote[iii]]['instrument_token']
            token.append(ATM_Token)
    else:
        pass
    

    with open(path+"quote_file.txt",'w') as file:
        file.write(str(quote))

    with open(path+"token_file.txt",'w') as file:
        file.write(str(token))

    import datetime

    for i in range(len(token)):
        instrument_token = token[i]
        from_datetime = datetime.datetime.now() - datetime.timedelta(days=6)     # From last & days
        to_datetime = datetime.datetime.now()
        interval = "minute"
        x=kite.historical_data(instrument_token, from_datetime, to_datetime, interval, continuous=False, oi=False)

        with open(path+quote[i]+'.txt', "a") as file: 
            file.write(str(x) + "\n")

############################################################ 5 min data collection code start #########################################################

    for i in range(len(token)):
        instrument_token = token[i]
        from_datetime = datetime.datetime.now() - datetime.timedelta(days=10)     # From last & days
        to_datetime = datetime.datetime.now()
        interval = "5minute"
        x_5_min=kite.historical_data(instrument_token, from_datetime, to_datetime, interval, continuous=False, oi=False)

        with open(path+quote[i]+'_5_min.txt', "a") as file: 
            file.write(str(x_5_min) + "\n")


############################################################ 5 min data collection code end #########################################################



    for i in range(len(token)):

        with open(path+quote[i]+'.txt', 'r') as file:
            file_contents = file.read()

        cleaned_contents = file_contents.replace("datetime.datetime", "").replace(", tzinfo=tzoffset(None, 19800)", "")

        data = ast.literal_eval(cleaned_contents)

        df = pd.DataFrame(data)

        df['date'] = df['date'].apply(lambda x: pd.Timestamp(year=x[0], month=x[1], day=x[2], hour=x[3], minute=x[4]))
        df['Date'] = df['date'].dt.strftime('%Y-%m-%d')
        df['Time'] = df['date'].dt.strftime('%H:%M')
        df = df.drop(columns=['date'])

        df = df[['Date', 'Time', 'open', 'high', 'low', 'close']]
        df.to_csv(path+quote[i]+".csv",index=False)
        os.remove(path+quote[i]+'.txt')

############################################################ 5 min data collection code start #########################################################

    for i in range(len(token)):

        with open(path+quote[i]+'_5_min.txt', 'r') as file:
            file_contents = file.read()

        cleaned_contents = file_contents.replace("datetime.datetime", "").replace(", tzinfo=tzoffset(None, 19800)", "")

        data = ast.literal_eval(cleaned_contents)

        df = pd.DataFrame(data)

        df['date'] = df['date'].apply(lambda x: pd.Timestamp(year=x[0], month=x[1], day=x[2], hour=x[3], minute=x[4]))
        df['Date'] = df['date'].dt.strftime('%Y-%m-%d')
        df['Time'] = df['date'].dt.strftime('%H:%M')
        df = df.drop(columns=['date'])

        df = df[['Date', 'Time', 'open', 'high', 'low', 'close']]
        df.to_csv(path+quote[i]+"_5_min.csv",index=False)
        os.remove(path+quote[i]+'_5_min.txt')

############################################################ 5 min data collection code end #########################################################

    moving_average(quote,token)



def strike_update(expiry):
    global path
    final_new=pd.read_csv(path+"Nifty_option_chain.csv")

    nifty_current_price=kite.ltp(["NSE:NIFTY 50"])
    Nifty_current_price=nifty_current_price['NSE:NIFTY 50']['last_price']

    index = (final_new['strikePrice'] - Nifty_current_price).abs().idxmin()
    ATM_strike_price=final_new['strikePrice'].iloc[index]

    ATM_Plus_one=ATM_strike_price+50
    ATM_Minus_one=ATM_strike_price-50

    strike_price_list_new=[ATM_strike_price,ATM_Plus_one,ATM_Minus_one]

    with open(path+"strike_price_list.txt",'r') as file:
        content=file.read()

    if str(strike_price_list_new) in content:
        pass
    else:
        if os.path.getsize(path+"strike_price_list.txt") == 0:
            strike_price_to_add=strike_price_list_new
            strike_price_to_remove=None
            with open(path+"strike_price_list.txt",'w') as file:
                file.write(str(strike_price_list_new))
        else:
            with open(path+"strike_price_list.txt",'w') as file:
                file.write(str(strike_price_list_new))
            old_stk_price = ast.literal_eval(content)
            set1 = set(old_stk_price)
            set2 = set(strike_price_list_new)
            strike_price_to_add = list(set2 - set1)
            strike_price_to_remove = list(set1 - set2)

        print(strike_price_list_new)
        print(strike_price_to_add)
        print(strike_price_to_remove)

        historical(strike_price_list_new,strike_price_to_remove,expiry)

def historical_datacollection():

    global path
    name="NIFTY"
    global expiry

    global enctoken
    kite = KiteApp(enctoken=enctoken)
    

    final_new=Intraday_live_data.getoptionchain(name,expiry)
    final_new.reset_index(drop=True, inplace=True)

    final_new.to_csv(path+"Nifty_option_chain.csv",index=False)

    with open(path+"Strike_price_list.txt",'w') as file:
        pass

    while True:

        strike_update(expiry)
        time.sleep(300)



def live_data_1_min():

    with open(path+"quote_file.txt",'r') as file:
        quote_read=file.read()

    with open(path+"token_file.txt",'r') as file:
        token_read=file.read()


    quote= ast.literal_eval(quote_read)
    token= ast.literal_eval(token_read)

    import datetime

    for k in range(len(quote)):
        weightage=[0.2,0.090909,0.039216,0.00995]
        data=pd.read_csv(path+quote[k]+".csv")

        instrument_token = token[k]
        from_datetime = datetime.datetime.now() - datetime.timedelta(days=7)     # From last & days
        to_datetime = datetime.datetime.now()
        interval = "minute"
        x=kite.historical_data(instrument_token, from_datetime, to_datetime, interval, continuous=False, oi=False)

        l=len(x)
        # print(l)
        ##################################################################################################
        last_time = data['Time'].iloc[-1]
        time_obj = datetime.datetime.strptime(last_time, '%H:%M')
        new_time_obj = time_obj + datetime.timedelta(minutes=1)
        new_time_str = new_time_obj.strftime('%H:%M')

        p=1

        while True:
            # print(f"run{k},with p value {p}")
            dt=x[l-p]['date']
            split_datetime_list = [(dt.strftime('%Y-%m-%d'), dt.strftime('%H:%M'))]
            date=split_datetime_list[0][0]
            time=split_datetime_list[0][1]

            if time==new_time_str:
                break

            p=p+1


        ##################################################################################################

        data_dict = {
            'Date': date,
            'Time': time,
            'open': x[l-p]['open'],
            'high': x[l-p]['high'],
            'low': x[l-p]['low'],
            'close': x[l-p]['close'],
            'EMA 9':0,
            'EMA 21':0,
            'EMA 50':0,
            'EMA 200':0,
        }

        new_data_1_min = pd.DataFrame([data_dict])


        final_file= pd.concat([data,new_data_1_min], axis=0)
        rows=final_file.shape[0]

        final_file.iloc[rows-1,6]=(final_file.iloc[rows-1,5]-final_file.iloc[rows-2,6])*weightage[0]+final_file.iloc[rows-2,6]
        final_file.iloc[rows-1,7]=(final_file.iloc[rows-1,5]-final_file.iloc[rows-2,7])*weightage[1]+final_file.iloc[rows-2,7]
        final_file.iloc[rows-1,8]=(final_file.iloc[rows-1,5]-final_file.iloc[rows-2,8])*weightage[2]+final_file.iloc[rows-2,8]
        final_file.iloc[rows-1,9]=(final_file.iloc[rows-1,5]-final_file.iloc[rows-2,9])*weightage[3]+final_file.iloc[rows-2,9]

        # final_file= pd.concat([data,new_data_1_min], axis=0)
        print(f"Time: {time}")
        final_file.to_csv(path+quote[k]+".csv",index=False)


def live_data_5_min():

    with open(path+"quote_file.txt",'r') as file:
        quote_read=file.read()

    with open(path+"token_file.txt",'r') as file:
        token_read=file.read()


    quote= ast.literal_eval(quote_read)
    token= ast.literal_eval(token_read)

    import datetime

    for k in range(len(quote)):
        weightage=[0.2,0.090909,0.039216,0.00995]
        data=pd.read_csv(path+quote[k]+"_5_min.csv")

        instrument_token = token[k]
        from_datetime = datetime.datetime.now() - datetime.timedelta(days=7)     # From last & days
        to_datetime = datetime.datetime.now()
        interval = "5minute"
        x=kite.historical_data(instrument_token, from_datetime, to_datetime, interval, continuous=False, oi=False)

        l=len(x)

        ##################################################################################################
        last_time = data['Time'].iloc[-1]
        time_obj = datetime.datetime.strptime(last_time, '%H:%M')
        new_time_obj = time_obj + datetime.timedelta(minutes=5)
        new_time_str = new_time_obj.strftime('%H:%M')

        p=1

        while True:
            dt=x[l-p]['date']
            split_datetime_list = [(dt.strftime('%Y-%m-%d'), dt.strftime('%H:%M'))]
            date=split_datetime_list[0][0]
            time=split_datetime_list[0][1]

            if time==new_time_str:
                break

            p=p+1


        ##################################################################################################

        data_dict = {
            'Date': date,
            'Time': time,
            'open': x[l-p]['open'],
            'high': x[l-p]['high'],
            'low': x[l-p]['low'],
            'close': x[l-p]['close'],
            'EMA 9':0,
            'EMA 21':0,
            'EMA 50':0,
            'EMA 200':0,
        }

        new_data_5_min = pd.DataFrame([data_dict])


        final_file= pd.concat([data,new_data_5_min], axis=0)
        rows=final_file.shape[0]

        final_file.iloc[rows-1,6]=(final_file.iloc[rows-1,5]-final_file.iloc[rows-2,6])*weightage[0]+final_file.iloc[rows-2,6]
        final_file.iloc[rows-1,7]=(final_file.iloc[rows-1,5]-final_file.iloc[rows-2,7])*weightage[1]+final_file.iloc[rows-2,7]
        final_file.iloc[rows-1,8]=(final_file.iloc[rows-1,5]-final_file.iloc[rows-2,8])*weightage[2]+final_file.iloc[rows-2,8]
        final_file.iloc[rows-1,9]=(final_file.iloc[rows-1,5]-final_file.iloc[rows-2,9])*weightage[3]+final_file.iloc[rows-2,9]

        # final_file= pd.concat([data,new_data_1_min], axis=0)
        print(f"Time: {time}")
        final_file.to_csv(path+quote[k]+"_5_min.csv",index=False)





def live_data_collection_1_min():
    time.sleep(60)
    i=0
    while True:
       live_data_1_min()
       print(f"Run completed for 1 min data collection: {i}")
       i=i+1
       time.sleep(60)


def live_data_collection_5_min():
    time.sleep(300)
    i=0
    while True:
       live_data_5_min()
       print(f"Run completed for 5 min data collection: {i}")
       i=i+1
       time.sleep(300)




import datetime
import time

def calculate_delay():
    now = datetime.datetime.now()
    minutes = now.minute
    seconds = now.second
    
    # Calculate the remaining time to the next multiple of 5 minutes
    remaining_minutes = 5 - (minutes % 5)
    if remaining_minutes == 0:
        remaining_minutes = 5  # If it's already a multiple of 5, wait for the next one
        
    remaining_seconds = 60 - seconds
    
    total_delay_seconds = remaining_minutes * 60 - seconds
    return total_delay_seconds

def main():
    delay_seconds = calculate_delay()
    print(f"Waiting for {delay_seconds} seconds...")
    time.sleep(delay_seconds)
    
    # Your code to start running after the delay
    thread1 = threading.Thread(target=historical_datacollection)
    thread2 = threading.Thread(target=live_data_collection_1_min)
    thread3 = threading.Thread(target=live_data_collection_5_min)

    thread1.start()
    thread2.start()
    thread3.start()

    thread1.join()  
    thread2.join()  
    thread3.join()  



kite = KiteApp(enctoken=enctoken)
path="D:/ashu/Finance/algo_trading/Zerodha_GUI/raw_data_collected/"

try:
    for filename in os.listdir(path):
        file_path = os.path.join(path, filename)
        if os.path.isfile(file_path):
            os.remove(file_path)
except Exception as e:
    print(f"An error occurred: {e}")


main()

# thread1 = threading.Thread(target=historical_datacollection)
# thread2 = threading.Thread(target=live_data_collection_1_min)
# thread3 = threading.Thread(target=live_data_collection_5_min)

# thread1.start()
# thread2.start()
# thread3.start()


# thread1.join()  
# thread2.join()  
# thread3.join()  