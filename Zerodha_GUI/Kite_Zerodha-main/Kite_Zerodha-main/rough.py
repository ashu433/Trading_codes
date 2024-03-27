from datetime import datetime,timedelta

start_time = datetime.strptime("9:14", "%H:%M")
end_time = datetime.strptime("15:30", "%H:%M")

# Define the interval (3 minutes)
interval = timedelta(minutes=5)

# Initialize an empty list to store the generated times
time_list = []

# Generate the times
current_time = start_time
while current_time <= end_time:
    time_list.append(current_time.strftime("%H:%M"))
    current_time += interval

print(time_list)