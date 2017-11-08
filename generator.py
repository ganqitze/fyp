# day = 32
# month = 10
# year_start = 3 #2013
# year_end = 8 #2017

# log_file = "C://Users/User/Desktop/datedate.txt"
# with open(log_file, "a") as my_log:		
# 	for x in xrange(year_start,year_end):
# 		for y in xrange(1,month):
# 			for z in list(range(1,day)):
# 				date = "0%d/0%d/201%d\n" %(z,y,x)
# 				my_log.write(date.encode("utf-8"))




# log_file = "C://Users/User/Desktop/minister.txt"
# with open(log_file) as f:
#     blacklist = f.read()


# with open(log_file, "a") as f:
#     f.write(blacklist.lower())




# hour = 24
# mins = 60
# log_file = "C://Users/User/Desktop/time2.txt"
# with open(log_file, "w") as my_log:		
# 	for x in xrange(0,hour):
# 		for y in xrange(0,mins, 10):
# 			time = "%d.%d\n" %(x,y)
# 			my_log.write(time.encode("utf-8"))

log_file = "C://Users/User/Desktop/date1.txt"
log1_file = "C://Users/User/Desktop/date3.txt"
with open(log_file) as f:
    blacklist = f.readlines()

with open(log1_file, "w") as f: 
	for x in blacklist:
		if len(x) == 8:
			numm = "0%s" %(x)
			f.write(numm)
		else:
			f.write(x)
			# print numm

