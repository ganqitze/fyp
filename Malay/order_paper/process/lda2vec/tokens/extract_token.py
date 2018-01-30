import os.path
import pickle
import csv
import time
from datetime import datetime
from palmettopy.palmetto import Palmetto

start_time = time.time()

base_path_lin  = "/home/User/fyp/Malay/order_paper/process/lda2vec/tokens"
base_path_win = "C:/Users/User/Desktop/fyp/Malay/order_paper/process/lda2vec/tokens"

topic_file = "C:/Users/User/Desktop/fyp/Malay/order_paper/process/lda2vec/#20/topic.csv"
# topic_file = os.path.join(base_path_win, "topic_10.csv")
text_file = os.path.join(base_path_win, "topic_20.txt")
index_file = os.path.join(base_path_win, "topic_i_20.txt")


open(text_file, 'wb').close()
open(index_file, 'wb').close()

def save_text(measures):
    with open(text_file, "ab") as newFile:
        newFileWriter = csv.writer(newFile)
        newFileWriter.writerow(measures)

def save_index(measures):
    with open(index_file, "ab") as newFile:
        newFileWriter = csv.writer(newFile)
        newFileWriter.writerow(measures)

def read_topic():
	with open(topic_file) as f:
		mycsv = csv.reader(f)
		mycsv = list(mycsv)
	return mycsv


topic_list = read_topic()
print "start"
print len(topic_list)
text_list = []
for i in range(0, len(topic_list)):
	

	for j in range(0, len(topic_list[0])):
		# print topic_list[i][j]
		text = topic_list[i][j].replace('[u\'', '').replace(' u\'', ' ').replace('\']', '').replace('\',', '')
		text = text.split()
		# print text

		text_list.append(text)
	# print text_list
	# save_text(text_list)
	# print i, (time.time() - interval_time)

# print text_list
c = a = 0
for text in text_list:
	interval_time = time.time()
	a += 1
	save_index(str(len(text)))
	for i in text:
		save_text(i.split())
		c += 1
	print a, (time.time() - interval_time)
print c
print("--- Done all! %s seconds ---" % (time.time() - start_time))

