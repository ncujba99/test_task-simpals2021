from datetime import datetime


date_time_str = "2020-06-16T09:43:13+03:00"

date_time_obj = datetime. strptime(date_time_str, '%Y-%m-%dT%H:%M:%S%z')
print(date_time_obj)

print(type(date_time_obj))