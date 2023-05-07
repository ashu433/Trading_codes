import schedule
import time 
from datetime import  timedelta, datetime

def task():
        # Get the current time in 24-hour format
    current_time = time.strftime("%H:%M:%S")

    # Convert the 24-hour format to 12-hour format with AM/PM
    time_parts = current_time.split(":")
    hours = int(time_parts[0])
    minutes = int(time_parts[1])
    seconds = int(time_parts[2])
    if hours >= 12:
        suffix = "PM"
        hours -= 12
    else:
        suffix = "AM"
    if hours == 0:
        hours = 12
    formatted_time = "{:02d}:{:02d}:{:02d} {}".format(hours, minutes, seconds, suffix)

    # Print the current time in 12-hour format with AM/PM
    print("The current time is", formatted_time)

schedule.every(5).seconds.until(timedelta(hours=6)).do(task)

while True:
    schedule.run_pending()
    time.sleep(1)
