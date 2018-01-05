from datetime import datetime
import time
import csv
import os.path
import pickle
import pandas as pd
import logging
import warnings
warnings.filterwarnings(action='ignore', category=UserWarning, module='gensim')
import gensim
from gensim import corpora, models
from gensim.models.coherencemodel import CoherenceModel

logging.basicConfig()

start_time = time.time()

n_topic = 10
n_word = 10

base_path_lin  = "/home/User/fyp/Malay/order_paper/lda/#10/"
base_path_lin2  = "/home/ganqitze/Desktop/fyp/Malay/order_paper/lda/#10/"
base_path_win = "C:/Users/User/Desktop/fyp/Malay/order_paper/lda/#10"

topic_file = os.path.join(base_path_lin2, "topic.csv")
coherence_file = os.path.join(base_path_lin2, "coherence.csv")

# open(topic_file, 'wb').close()
# open(coherence_file, 'wb').close()

def save_topic(text):    
    with open(topic_file, "ab") as newFile:
        newFileWriter = csv.writer(newFile)
        newFileWriter.writerow(text)

def save_coherence(measures):
    with open(coherence_file, "ab") as newFile:
        newFileWriter = csv.writer(newFile)
        newFileWriter.writerow(measures)



Lda = gensim.models.ldamodel.LdaModel

# Reload from saved
lda_dictionary = corpora.Dictionary.load('../data/dictionary.dict')
doc_term_matrix = corpora.MmCorpus('../data/corpus.mm')
lda_tokens = pickle.load(open('../data/tokens.p', 'rb'))
# print dictionary
# print len(doc_term_matrix)


counter = avg = 0
while avg < 0.90 and counter < 1000:
	sums = []
	# Running and Training LDA model on the document term matrix.
	ldamodel = Lda(doc_term_matrix, num_topics=n_topic, id2word=lda_dictionary, passes=10)
	topic_list = ldamodel.print_topics(num_topics=n_topic, num_words=n_word)

	# LDA Coherence
	cm = CoherenceModel(model=ldamodel, texts=lda_tokens, dictionary=lda_dictionary, coherence='c_v')
	for i in cm.get_coherence_per_topic():
		sums.append(i)
	avg = cm.get_coherence()
	sums.append(avg)
	# print avg, cm.get_coherence()
	# print cm.get_coherence_per_topic()
	counter += 1
	save_topic(topic_list)
	save_coherence(sums)
	ldamodel.save('topic.model')
	print counter, avg
else:
	# save_topic(topic_list)
	# save_coherence(sums)
	# ldamodel.save('topic.model')
	print("COMPLETE with epoch: ", counter)

print("--- Done %s seconds ---" % (time.time() - start_time))