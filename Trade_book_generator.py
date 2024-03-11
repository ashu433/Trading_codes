import pandas as pd
import numpy as np

def Trade_book_virtual(text_file,Date):
    path="D:/ashu/Finance/algo_trading/Option_chain_data/"
    file=text_file
    trade_book=pd.read_csv(file, delimiter='\t', header=None)
    trade_book=trade_book.drop(0)
    trade_book=trade_book.drop([1, 2], axis=1)
    trade_book=trade_book.reset_index(drop=True)
    data = trade_book.values
    new_data = data.reshape(-1, 6)
    new_df = pd.DataFrame(new_data)
    new_df=new_df.drop(2,axis=1)
    new_df[0],new_df[4]=new_df[4],new_df[0]
    new_column_names = ['Time', 'Instrument', 'Quantity', 'Buy/Sell',"Premium"]
    new_df.columns = new_column_names
    data_1=new_df['Time'].str.split(' ', expand=True)
    data_2=new_df['Instrument'].str.split(' ', expand=True)
    column_mapping = {
        0: 'Time',
        1: 'Date',
    }
    data_1 = data_1.rename(columns=column_mapping)
    data_2['Expiry'] = data_2[1] + ' ' + data_2[2] + ' ' + data_2[3]
    data_2=data_2.drop([1, 2, 3], axis=1)
    data_2 = data_2.rename(columns={'Expiry': 'Expiry'})
    new_df =new_df.drop(["Time", "Instrument"], axis=1)
    column_order = list(data_1.columns) + list(data_2.columns) + list(new_df.columns)
    new_df = pd.concat([data_1, data_2, new_df], axis=1)
    new_df = new_df.reindex(columns=column_order)
    column_mapping = {
        0: 'Instrument',
        4: 'Strike Price',
        5: 'Option Type',
    }
    new_df = new_df.rename(columns=column_mapping)

    date=Date
    relevant_trade_portion=new_df[new_df['Date']==date]
    relevant_trade_portion=relevant_trade_portion.reset_index(drop=True)
    rows,coloumns=relevant_trade_portion.shape

    x=0
    premium=[]
    percentage_profit_Loss=[]
    trade=[]
    j=1
    relevant_trade_portion["Quantity"].astype(str)
    for i in range(rows):
        qty=relevant_trade_portion["Quantity"].iloc[rows-i-1]
        Qty=int(qty)
        x=Qty+x
        pre=relevant_trade_portion["Premium"].iloc[rows-i-1]
        Pre=float(pre)
        premium.append(Pre)
        trade.append(f"Trade_{j}")
        if x==0:
            j=j+1
            first_number=premium[0]
            percentages = [((num-first_number) / first_number) * 100 for num in premium]
            percentage_profit_Loss.extend(percentages)
            premium=[]
        else:
            continue 

    rounded_list = [round(num, 2) for num in percentage_profit_Loss]
    Trade = pd.DataFrame(trade, columns=['Trade Number'])
    Profit_loss = pd.DataFrame(rounded_list, columns=['Profit and Loss'])
    Trade=Trade[::-1].reset_index(drop=True).reset_index()
    Trade=Trade.drop("index",axis=1)
    Profit_loss=Profit_loss[::-1].reset_index(drop=True).reset_index()
    Profit_loss=Profit_loss.drop("index",axis=1)
    Final_Trade_Record = pd.concat([Trade, relevant_trade_portion, Profit_loss], axis=1)
    Final_Trade_Record["Profit and Loss"]=Final_Trade_Record['Profit and Loss'].replace(0.0, 'Start')
    Final_Trade_Record.to_csv(path+'Trade_Record_virtual.csv', index=False)


def Trade_book_real(filename,charges):
    path="D:/ashu/Finance/algo_trading/Option_chain_data/"
    file=filename
    trade_book_real=pd.read_csv(file)
    data_1 = trade_book_real['Time'].str.split(' ', expand=True)
    data_1=data_1.rename(columns={0: "Date"})
    data_1=data_1.rename(columns={1: "Time"})
    trade_book_real=trade_book_real.drop('Time', axis=1)
    trade_book_real=trade_book_real.drop('Product', axis=1)
    trade_book_real=trade_book_real.drop('Status', axis=1)

    trade_book_real= pd.concat([data_1, trade_book_real], axis=1)
    data_3=trade_book_real['Instrument'].str.split('(\d{2,})', expand=True)
    data_4=data_3[1].str.extract(r'(\d{5})(\d{5})')
    data_4[0] = pd.to_datetime(data_4[0], format='%y%m%d').dt.strftime('%y-%m-%d')

    data_3=data_3.drop(1, axis=1)
    new_column_names = {
        0: 'Instrument',
        2: "Order Type",
        # Add more columns as needed
    }

    data_3= data_3.rename(columns=new_column_names)

    new_column_names = {
    0: 'Expiry Day',
    1: "Strike Price",
    # Add more columns as needed
    }

    data_4= data_4.rename(columns=new_column_names)

    data_3= pd.concat([data_3, data_4], axis=1)

    trade_book_real=trade_book_real.drop('Instrument', axis=1)

    new_columns = data_3.columns.tolist()
    for idx, col in enumerate(new_columns):
        trade_book_real.insert(2 + idx, col, data_3[col])

    data_5=trade_book_real['Qty.'].str.split('/', expand=True)
    data_5=data_5.rename(columns={0: "Quantity"})
    qty_index = trade_book_real.columns.get_loc('Qty.')
    quantity_column = data_5['Quantity']
    trade_book_real.insert(qty_index + 1, 'Quantity', quantity_column)

    trade_book_real['Quantity'] = trade_book_real['Quantity'].astype(float)

    def change_sign(row):
        if row['Type'] == 'BUY':
            return row['Quantity']
        elif row['Type'] == 'SELL':
            return -row['Quantity']

    # Apply the custom function to create a new column 'Signed_Float_Column'
    trade_book_real['Quantity'] = trade_book_real.apply(change_sign, axis=1)

    trade_book_real=trade_book_real.drop('Qty.', axis=1)
    trade_book_real

    x=0
    premium=[]
    percentage_profit_Loss=[]
    trade=[]
    j=1
    # trade_book_real["Quantity"].astype(str)
    rows,coloumns=trade_book_real.shape
    for i in range(rows):
        qty=trade_book_real["Quantity"].iloc[rows-i-1]
        Qty=int(qty)
        x=Qty+x
        pre=trade_book_real["Avg. price"].iloc[rows-i-1]
        Pre=float(pre)
        premium.append(Pre)
        trade.append(f"Trade_{j}")
        if x==0:
            j=j+1
            first_number=premium[0]
            percentages = [((num-first_number) / first_number) * 100 for num in premium]
            percentage_profit_Loss.extend(percentages)
            premium=[]
        else:
            continue 

    rounded_list = [round(num, 2) for num in percentage_profit_Loss]
    Trade = pd.DataFrame(trade, columns=['Trade Number'])
    Profit_loss = pd.DataFrame(rounded_list, columns=['Profit and Loss'])
    Trade=Trade[::-1].reset_index(drop=True).reset_index()
    Trade=Trade.drop("index",axis=1)
    Profit_loss=Profit_loss[::-1].reset_index(drop=True).reset_index()
    Profit_loss=Profit_loss.drop("index",axis=1)

    Final_Trade_Record = pd.concat([Trade, trade_book_real, Profit_loss], axis=1)
    Final_Trade_Record['Expiry Day'] = pd.to_datetime(Final_Trade_Record['Expiry Day'], format='%y-%m-%d')
    Final_Trade_Record['Expiry Day'] = Final_Trade_Record['Expiry Day'].dt.strftime('%Y-%m-%d')
    Final_Trade_Record.to_csv(path+'Trade_Record_Real.csv', index=False)


    file2=charges
    Charges=pd.read_csv(file2, delimiter='\t', header=None)
    Charges[['Type of Charges', 'Net Deduction']] = Charges[0].str.extract(r'(\D+)(\d+)', expand=True)
    Charges['Type of Charges'] = Charges['Type of Charges'].str.strip()
    Charges['Net Deduction'] = pd.to_numeric(Charges['Net Deduction'])
    Charges=Charges.drop(0, axis=1)
    Charges.to_csv(path+'Charges.csv', index=False)


if __name__=='__main__':  
    pass
