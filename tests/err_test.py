from time import localtime, strftime
now = strftime("%Y-%m-%d %H:%M:%S", localtime())
print(now)