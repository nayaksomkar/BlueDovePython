import datetime

seconds = 104


convert = str(datetime.timedelta(seconds = seconds))
convert  = convert.split(':')

print(int(convert[0]))
print(int(convert[1]))
print(int(convert[2]))