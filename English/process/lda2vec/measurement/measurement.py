import os.path
import pickle
import csv
import time
from datetime import datetime
from palmettopy.palmetto import Palmetto

start_time = time.time()

base_path_lin  = "/home/User/fyp/English/process/lda2vec/measurement"
base_path_win = "C:/Users/User/Desktop/fyp/English/process/lda2vec/measurement"

topic_file = os.path.join(base_path_lin, "topic_20.csv")
coherence_file = os.path.join(base_path_lin, "coherence_20.csv")

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
	