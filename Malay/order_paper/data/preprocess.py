# Author: Chris Moody <chrisemoody@gmail.com>
# License: MIT

# This example loads a large 800MB Hacker News comments dataset
# and preprocesses it. This can take a few hours, and a lot of
# memory, so please be patient!
from datetime import datetime
import time
import os.path
import nltk
import numpy as np
import pandas as pd
import logging
import cPickle as pickle
from lda2vec import preprocess, Corpus
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
import warnings
warnings.filterwarnings(action='ignore', category=UserWarning, module='gensim')
import gensim
from gensim import corpora, models

logging.basicConfig()

start_time = time.time()

max_length = 32767   # Limit of 250 words per comment
# min_author_comments = 50  # Exclude authors with fewer comments
nrows = None  # Number of rows of file to read; None reads in full file

base_path_lin  = "/home/User/Desktop/fyp/Malay/order_paper"
base_path_win = "C:/Users/User/Desktop/fyp/Malay/order_paper"

fn = os.path.join(base_path_win, "parse/log3.csv")

# url = "https://zenodo.org/record/45901/files/hacker_news_comments.csv"
# if not os.path.exists(fn):
#     import requests
#     response = requests.get(url, stream=True, timeout=2400)
#     with open(fn, 'w') as fh:
#         # Iterate over 1MB chunks
#         for data in response.iter_content(1024**2):
#             fh.write(data)


features = []
# Convert to unicode (spaCy only works with unicode)
features = pd.read_csv(fn, encoding='utf8', nrows=nrows)
# Convert all integer arrays to int32
for col, dtype in zip(features.columns, features.dtypes):
    if dtype is np.dtype('int64'):
        features[col] = features[col].astype('int32')

# Tokenize the texts
# If this fails it's likely spacy. Install a recent spacy version.
# Only the most recent versions have tokenization of noun phrases
# I'm using SHA dfd1a1d3a24b4ef5904975268c1bbb13ae1a32ff
# Also try running python -m spacy.en.download all --force
texts = features.pop('content').values
# texts = features.pop('comment_text').values


# # STEM the text
factory = StemmerFactory()
stemmer = factory.create_stemmer()
katadasar = [stemmer.stem(x) for x in texts]

tokens, vocab = preprocess.tokenize(katadasar, max_length, n_threads=4,
                                    merge=False)
# print tokens
# print len(tokens), len(vocab)


# LDA
# tokenize words using nltk
tokens = [nltk.word_tokenize(x) for x in texts]
dictionary = corpora.Dictionary(tokens)
dictionary.save('dictionary.dict')
print dictionary

doc_term_matrix = [dictionary.doc2bow(doc) for doc in tokens]
corpora.MmCorpus.serialize('corpus.mm', doc_term_matrix)
print len(doc_term_matrix)
print doc_term_matrix[100]
print "LDA preprocess complete"
# END OF LDA


del texts

# # Make a ranked list of rare vs frequent words
corpus = Corpus()
corpus.update_word_count(tokens)
corpus.finalize()

# # The tokenization uses spaCy indices, and so may have gaps
# # between indices for words that aren't present in our dataset.
# # This builds a new compact index
compact = corpus.to_compact(tokens)
# # Remove extremely rare words
pruned = corpus.filter_count(compact, min_count=10)
# Words tend to have power law frequency, so selectively
# downsample the most prevalent words
clean = corpus.subsample_frequent(pruned)
print "n_words", np.unique(clean).max()

# # Extract numpy arrays over the fields we want covered by topics
# # Convert to categorical variables
# # author_counts = features['comment_author'].value_counts()
# # to_remove = author_counts[author_counts < min_author_comments].index
# # mask = features['comment_author'].isin(to_remove).values
# # author_name = features['comment_author'].values.copy()
# # author_name[mask] = 'infrequent_author'
# # features['comment_author'] = author_name
# # authors = pd.Categorical(features['comment_author'])
# # author_id = authors.codes
# # author_name = authors.categories
# # story_id = pd.Categorical(features['story_id']).codes
# # # Chop timestamps into days
# # story_time = pd.to_datetime(features['story_time'], unit='s')
# # days_since = (story_time - story_time.min()) / pd.Timedelta('1 day')
# # time_id = days_since.astype('int32')
# # features['story_id_codes'] = story_id
# # features['author_id_codes'] = story_id
# # features['time_id_codes'] = time_id

paper_id = pd.Categorical(features['paper_id']).codes
features['paper_id_codes'] = paper_id

# Chop timestamps into days
paper_date = pd.to_datetime(features['date'])
# today_date = pd.to_datetime(datetime.today())
days_since = abs((paper_date - paper_date.min()) / pd.Timedelta('1 day'))
date_id = days_since.astype('int32') #time_id

# print "n_authors", author_id.max()
# print "n_stories", story_id.max()
# print "n_times", time_id.max()

# # Extract outcome supervised features
# # ranking = features['comment_ranking'].values
# # score = features['story_comment_count'].values

# # Now flatten a 2D array of document per row and word position
# # per column to a 1D array of words. This will also remove skips
# # and OoV words
# feature_arrs = (story_id, author_id, time_id, ranking, score)
# flattened, features_flat = corpus.compact_to_flat(pruned, *feature_arrs)
# # Flattened feature arrays
# (story_id_f, author_id_f, time_id_f, ranking_f, score_f) = features_flat

feature_arrs = (paper_id, date_id)
flattened, features_flat = corpus.compact_to_flat(pruned, *feature_arrs)
# Flattened feature arrays
(paper_id_f, date_id_f) = features_flat

# # # Save the data
# # pickle.dump(corpus, open('corpus', 'w'), protocol=2)
# # pickle.dump(vocab, open('vocab', 'w'), protocol=2)
# # features.to_pickle('features.pd')
# # data = dict(flattened=flattened, story_id=story_id_f, author_id=author_id_f,
# #             time_id=time_id_f, ranking=ranking_f, score=score_f,
# #             author_name=author_name, author_index=author_id)
# # np.savez('data', **data)
# # np.save(open('tokens', 'w'), tokens)

pickle.dump(corpus, open('corpus', 'wb'), protocol=2)
pickle.dump(vocab, open('vocab', 'wb'), protocol=2)
features.to_pickle('features.pd')
data = dict(flattened=flattened, paper_id=paper_id_f, date_id=date_id_f)
np.savez('data', **data)
np.save(open('tokens', 'wb'), tokens)

print("--- Done %s seconds ---" % (time.time() - start_time))