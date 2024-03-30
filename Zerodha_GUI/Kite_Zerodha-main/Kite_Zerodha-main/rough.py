from datetime import datetime

# Example date string
date_string = "03-Jan-2024"

# Convert the date string to a datetime object
date_object = datetime.strptime(date_string, "%d-%b-%Y")

# Get the day of the week
day_of_week = date_object.strftime('%A')

print("Day of the week:", day_of_week)
