import schedule
import subprocess
import time

path="D:/ashu/Finance/algo_trading/Zerodha_GUI/Kite_Zerodha-main/Kite_Zerodha-main/"

def run_batch_file():
    # Replace "path_to_file.bat" with the actual path to your batch file
    subprocess.call([path+"Quote_Token_bat_file.bat"])

# Schedule the batch file to run at 9:20 AM every day
schedule.every().day.at("09:18").do(run_batch_file)

# Keep the program running to execute scheduled tasks
while True:
    schedule.run_pending()
    time.sleep(1)
