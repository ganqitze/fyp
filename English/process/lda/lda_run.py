from datetime import datetime
import time
import os.path
import cPickle as pickle
import pandas as pd
import logging
import warnings
warnings.filterwarnings(action='ignore', category=UserWarning, module='gensim')
import gensim
from gensim import corpora, models

logging.basicConfig()

start_time = time.time()


Lda = gensim.models.ldamodel.LdaModel

# Reload from saved
dictionary = corpora.Dictionary.load('dictionary.dict')
doc_term_matrix = corpora.MmCorpus('corpus.mm')
print dictionary
print len(doc_term_matrix)


# Running and Training LDA model on the document term matrix.
ldamodel = Lda(doc_term_matrix, num_topics=1, id2word = dictionary, passes=1)
# print 'used: {:.2f}s'.format(time()-start)
print(ldamodel.print_topics(num_topics=1, num_words=10))
ldamodel.save('topic.model')

print("--- Done %s seconds ---" % (time.time() - start_time))