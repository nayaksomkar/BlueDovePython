from factorial import fac
import datetime


# To take input from the user
num = int(input("Enter a number    :    "))
start_time = str(datetime.datetime.now())[11:]
t1 = datetime.datetime.strptime(start_time, "%H:%M:%S.%f")

fac(num)

end_time = str(datetime.datetime.now())[11:]

t2 = datetime.datetime.strptime(end_time, "%H:%M:%S.%f")


print('Start time   :   ' + str(t1.time()),'End time   :   ' + str(t2.time()),sep='\n')

delta = t2 - t1


sec = delta.total_seconds()
print(f"Time difference is {sec/60} minutes")
# time difference in seconds
print(f"Time difference is {sec} seconds")

# time difference in milliseconds
ms = sec * 1000
print(f"Time difference is {ms} milliseconds")