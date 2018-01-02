from datetime import datetime
import time
import os.path
import cPickle as pickle
import pandas as pd
import logging
import nltk 
import warnings
warnings.filterwarnings(action='ignore', category=UserWarning, module='gensim')
import gensim
from gensim import corpora, models

logging.basicConfig()

nrows = None  # Number of rows of file to read; None reads in full file

start_time = time.time()

fn = "/home/ganqitze/Desktop/fyp/Malay/order_paper/parse/log.csv"

features = []
# Convert to unicode (spaCy only works with unicode)
features = pd.read_csv(fn, encoding='utf8', nrows=nrows)
# Convert all integer arrays to int32
# for col, dtype in zip(features.columns, features.dtypes):
#     if dtype is np.dtype('int64'):
#         features[col] = features[col].astype('int32')

texts = features.pop('content').values

# okenize words using nltk
tokens = [nltk.word_tokenize(x) for x in texts]
print("--- Done token %s seconds ---" % (time.time() - start_time))


# remove stopword - en-dash, code

del texts

dictionary = corpora.Dictionary(tokens)
dictionary.save('dictionary.dict')
print dictionary


doc_term_matrix = [dictionary.doc2bow(doc) for doc in tokens]
corpora.MmCorpus.serialize('corpus.mm', doc_term_matrix)

print len(doc_term_matrix)
# print doc_term_matrix[100]


#LDA runs
Lda = gensim.models.ldamodel.LdaModel


# Running and Training LDA model on the document term matrix.
ldamodel = Lda(doc_term_matrix, num_topics=1, id2word = dictionary, passes=1)
# print 'used: {:.2f}s'.format(time()-start)
print(ldamodel.print_topics(num_topics=1, num_words=10))

# print words per topic
# for i in ldamodel.print_topics(): 
#     for j in i: print j

# save the model
ldamodel.save('topic.model')


print("--- Done %s seconds ---" % (time.time() - start_time))