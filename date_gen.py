day = 32
month = 10
year_start = 3 #2013
year_end = 8 #2017

log_file = "C://Users/User/Desktop/date.txt"
with open(log_file, "a") as my_log:		
	for x in xrange(year_start,year_end):
		for y in xrange(1,month):
			for z in list(range(1,day)):
				date = "%d/0%d/201%d\n" %(z,y,x)
				my_log.write(date.encode("utf-8"))


		