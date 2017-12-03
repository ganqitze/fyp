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


# log_file = "C://Users/User/Desktop/ment.txt"
# with open(log_file) as f:
#     blacklist = f.read()
# open(log_file, 'w').close()
# with open(log_file, "w") as f:
#     f.write(blacklist.title())


# hour = 24
# mins = 60
# log_file = "C://Users/User/Desktop/time2.txt"
# with open(log_file, "w") as my_log:		
# 	for x in xrange(0,hour):
# 		for y in xrange(0,mins, 10):
# 			time = "%d.%d\n" %(x,y)
# 			my_log.write(time.encode("utf-8"))


# log_file = "C://Users/User/Desktop/date1.txt"
# log1_file = "C://Users/User/Desktop/date3.txt"
# with open(log_file) as f:
#     blacklist = f.readlines()
# with open(log1_file, "w") as f: 
# 	for x in blacklist:
# 		if len(x) == 8:
# 			numm = "0%s" %(x)
# 			f.write(numm)
# 		else:
# 			f.write(x)
# 			# print numm

# meeting-code = 
# num-code = 
# log_file = "C://Users/User/Desktop/code.txt"
# with open(log_file, "w") as my_log:		
# 	for x in xrange(1, 6):
# 		for y in xrange(1,4):
# 			for z in xrange(0, 100000):
# 				code = "PR-13%d%d-%05d\n" %(x,y,z)
# 				# print code
# 				my_log.write(code.encode("utf-8"))


# log_file = "C://Users/User/Desktop/num.txt"
# with open(log_file, 'w') as my_log:
# 	for x in range(200, 801):
# 		num = "%d\n" %(x)
# 		my_log.write(num.encode("utf-8"))

# log_file = "C://Users/User/Desktop/ee.txt"
# with open(log_file) as f:
#     blacklist = f.readlines()
# blacklist = [x.strip() for x in blacklist]
# open(log_file, 'w').close()
# hue = sorted(list(set(blacklist)))
# 	# print hue
# with open(log_file, "w") as f:
# 	for x in hue:
# 		haha = "%s\n" %(x)
# 		f.write(haha)

# import nltk
# from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
# factory = StemmerFactory()
# stemmer = factory.create_stemmer()

# blob = """ PR-1351-MQT0015 berkuasa terutamanya PDRM menangani ancaman pengganas Daesh PR-1351-MQT0002 Kota bercadang kajian menyeluruh pemberian subsidi bersasar ianya dinikmati PR-1351-MQT0005 Laksamana elaun risiko bomba penyelamat dikuatkuasakan PERTANYAAN-PERTANYAAN BAGI JAWAB LISAN PR-1351-L00284 mengatasi pemerdagangan manusia kesemua pintu-pintu masuk perancangan bekerjasama agensi-agensi perlindungan bantuan mangsa pemerdagangan penyeludupan PR-1351-L00624 statistik terkini syarikat-syarikat China milikan ekuiti projek-projek Forest City Iskandar Johor Melaka Gateway East Coast Rail Line Malaysia-China Industrial Park PR-1351-L00193 pendirian menghadapi tekanan pentadbiran Amerika sejauh ianya dikhuatiri kesan PR-1351-L00661 subsidi minyak minyak masak keperluan dibayar sekiranya penjimatan subsidi dimansuhkan langkah-langkah dicadangkan membebankan melaksanakan had siling Terangkan impak PR-1351-L00118 status terkini pengiktirafan pengajian Diploma Vokasional MQA Sekolah Menengah Vokasional SMV dinaiktaraf Kolej Vokasional PR-1351-L00324 langkah-langkah menangani serangan virus-virus merbahaya kencing tikus Leptospirosis seumpamanya virus misteri maut kejadian Kelantan lalu PR-1351-L01139 pelaksanaan CEO Faculty Programme Institut Pengajian IPTA impak positif mahasiswa siswi IPTA bercadang memperluaskan Institut Pengajian Swasta IPTS terutamanya dimiliki agensi-agensi PR-1351-L00949 Mara menaja pelajar bidang-bidang kritikal perubatan pergigian"""
# katadasar = stemmer.stem(blob)
# stem_tokens = nltk.word_tokenize(katadasar)

# print len(katadasar), katadasar, len(stem_tokens), stem_tokens

