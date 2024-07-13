from datetime import date

today = date.today()
yesterday = today.replace(today.year, today.month, today.day-1)
print(yesterday)