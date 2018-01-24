import os.path
import pickle
import csv
import time
from datetime import datetime
from palmettopy.palmetto import Palmetto

start_time = time.time()

base_path_lin  = "/home/User/fyp/"
base_path_win = "C:/Users/User/Desktop/fyp/"

topic_file = os.path.join(base_path_lin, "topic.csv")
coherence_file = os.path.join(base_path_lin, "coherence.csv")

# palmetto = Palmetto()
palmetto = Palmetto("http://localhost:7777/service/")

# open(coherence_file, 'ab').close()

def save_coherence(measures):
    with open(coherence_file, "ab") as newFile:
        newFileWriter = csv.writer(newFile)
        newFileWriter.writerow(measures)

def read_topic():
	with open(topic_file) as f:
		mycsv = csv.reader(f)
		mycsv = list(mycsv)
	return mycsv


topic_list = read_topic()
print "start"
for i in range(0, len(topic_list)):
	interval_time = time.time()
	coherence_list = []
	sums = avg = 0
	for j in range(0, len(topic_list[0])):
		# print topic_list[i][j]
		# print i, j
		text = topic_list[i][j].replace('[u\'', '').replace(' u\'', ' ').replace('\']', '').replace('\',', '')
		text = text.split()
		# print text
		coherence = palmetto.get_coherence(text, coherence_type="cv")
		# print coherence		
		coherence_list.append(coherence)
		sums += coherence
	avg = sums / len(topic_list[0])
	coherence_list.append(avg)
	save_coherence(coherence_list)
	print i, avg, (time.time() - interval_time)
print("--- Done all! %s seconds ---" % (time.time() - start_time))
	





# hue = [u'invest', u'gives', u'aspects', u'exceeded', u'retailers', u'performance', u'list', u'applications', u'written', u'fgv']

# from palmettopy.palmetto import Palmetto
# palmetto = Palmetto()
# palmetto = Palmetto("http://example.com/myownendpoint")
# print flat_list
# coherence = palmetto.get_coherence(text, coherence_type="cv")
# print coherence

# for i in range(0, len(mycsv[0])):
	# palmetto.get_coherence(mycsv[0][i])



# text = "[u'invest', u'gives', u'aspects', u'exceeded', u'retailers', u'performance', u'list', u'applications', u'written', u'fgv']"
# text2 = "[u'2', u'1', u'3', u'4', u'3', u'5', u'list', u'2', u'ht', u'ht']"

# text = text.replace('[', '').replace('\']', '').replace('u\'', '\'').replace('\',', '')
# text2 = text2.replace('[', '').replace('\']', '').replace('u\'', '').replace('\',', '')

# mylist = []
# mylist.append([])
# mylist.append([])
# mylist[0].append(text)
# mylist[1].append(text2)
# print mylist


# with open(topic_file) as f:
# 	mycsv = csv.reader(f)
# 	mycsv = list(mycsv)
# 	text = mycsv[1][1]
# print text

# print mycsv
# flat_list = [item for sublist in mycsv for item in sublist]

# mylist = []
# for top in flat_list:
# 	top = top.replace('[', '')
# 	top = top.replace('u\'', '')
# 	top = top.replace('\'', '')
# 	top = top.replace(']', '')
# 	mylist.append(top)
# print mylist


# import webbrowser
# import multiprocessing


# services = ['cv']
# url = u'http://palmetto.aksw.org/palmetto-webapp/service/{}?words={}'
# reqs = [url.format(s, '%20'.join(top)) for s in services for top in mylist]
# print reqs
# print " HELO WORLD"
# coherence = webbrowser.open(reqs[0])
# print coherence.value()









# <type 'list'>
# <Response [200]> http://palmetto.aksw.org/palmetto-webapp/service/cv {'words': u
# 'invest gives aspects exceeded retailers performance list applications written f
# gv'}
# 0.279318981077