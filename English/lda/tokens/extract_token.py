import os.path
import pickle
import csv
import time
from datetime import datetime
from palmettopy.palmetto import Palmetto

start_time = time.time()

base_path_lin  = "/home/User/fyp/English/lda/tokens/"
base_path_win = "C:/Users/User/Desktop/fyp/English/lda/tokens/"

topic_file = "C:/Users/User/Desktop/fyp/English/lda/#20/topic.csv"
# topic_file = os.path.join(base_path_win, "topic_10.csv")
text_file = os.path.join(base_path_win, "topic_20.txt")
text_index_file = os.path.join(base_path_win, "index_topic_20.txt")


open(text_file, 'wb').close()
open(text_index_file, 'wb').close()
def save_text(measures):
    with open(text_file, "ab") as newFile:
        newFileWriter = csv.writer(newFile)
        newFileWriter.writerow(measures)

def read_topic():
	with open(topic_file) as f:
		mycsv = csv.reader(f)
		mycsv = list(mycsv)
	return mycsv

def save_index_text(measures):
    with open(text_index_file, "ab") as newFile:
        newFileWriter = csv.writer(newFile)
        newFileWriter.writerow(measures)


topic_list = read_topic()
print "start"
# print len(topic_list)
text_list = []

# print topic_list[0][2].split()
interval_time = time.time()
for i in range(0, len(topic_list)):
	for j in range(0, len(topic_list[0])):
		# print topic_list[i][j]
		text = topic_list[i][j].replace('[u\'', '').replace(' u\'', ' ').replace('\']', '').replace('\',', '').replace('+', '').replace('\"', '').replace('\')', '').replace('*', ' ')
		# text = text.replace('(0,', '').replace('(1,', '').replace('(2,', '').replace('(3,', '').replace('(4,', '').replace('(5,', '').replace('(6,', '').replace('(7,', '').replace('(8,', '').replace('(9,', '')
		text = text.replace('(0,', '').replace('(1,', '').replace('(2,', '').replace('(3,', '').replace('(4,', '').replace('(5,', '').replace('(6,', '').replace('(7,', '').replace('(8,', '').replace('(9,', '').replace('(10,', '').replace('(11,', '').replace('(12,', '').replace('(13,', '').replace('(14,', '').replace('(15,', '').replace('(16,', '').replace('(17,', '').replace('(18,', '').replace('(19,', '')
		# text = text.replace('(0,', '').replace('(1,', '').replace('(2,', '').replace('(3,', '').replace('(4,', '').replace('(5,', '').replace('(6,', '').replace('(7,', '').replace('(8,', '').replace('(9,', '').replace('(10,', '').replace('(11,', '').replace('(12,', '').replace('(13,', '').replace('(14,', '').replace('(15,', '').replace('(16,', '').replace('(17,', '').replace('(18,', '').replace('(19,', '').replace('(20,', '').replace('(21,', '').replace('(22,', '').replace('(23,', '').replace('(24,', '').replace('(25,', '').replace('(26,', '').replace('(27,', '').replace('(28,', '').replace('(29,', '')
		text = text.split()

		text_list.append(text)
	# print text_list
	# save_text(text_list)
print "parsing", (time.time() - interval_time)

# print text_list

c = a = 0
for text in text_list:
	interval_time = time.time()
	a += 1
	for i in text:
		save_index_text(i.split())
		c += 1
	print a, (time.time() - interval_time)
print "# cell", c

interval_time = time.time()
with open(text_index_file) as f:
    topic_index = f.readlines()
topic_index = [x.strip() for x in topic_index] 
for i in range(0, len(topic_index)):
	if (i % 2 != 0):
		save_text(topic_index[i].split())
print "indexing", (time.time() - interval_time)

print("--- Done all! %s seconds ---" % (time.time() - start_time))

