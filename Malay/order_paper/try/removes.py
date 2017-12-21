# Author: Chris Moody <chrisemoody@gmail.com>
# License: MIT

# This example loads a large 800MB Hacker News comments dataset
# and preprocesses it. This can take a few hours, and a lot of
# memory, so please be patient!
from datetime import datetime
import time
start_time = time.time()


from lda2vec import preprocess, Corpus
import numpy as np
import pandas as pd
import logging
import cPickle as pickle
import os.path

from Sastrawi.Stemmer.StemmerFactory import StemmerFactory


logging.basicConfig()


max_length = 32767   # Limit of 250 words per comment
# min_author_comments = 50  # Exclude authors with fewer comments
nrows = None  # Number of rows of file to read; None reads in full file

# base_path_lin  = "/home/User/Desktop/fyp/order_paper"
# base_path_win = "C:/Users/User/Desktop/fyp/order_paper"

# fn = "hacker_news_comments.csv"
fn = "C:/Users/User/Desktop/fyp/Malay/order_paper/parse/log2.csv"

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


# STEM the text
factory = StemmerFactory()
stemmer = factory.create_stemmer()
katadasar = [stemmer.stem(x) for x in texts]
print katadasar.type()
import re

pattern = re.compile(r'PR-13[1-5][1-3]-[a-zA-Z0-9_]')

# for x in katadasar:
# 	for y in x.split():
# 		if re.findall(pattern, y):
# 			x = x.replace(' ' + y + ' ', ' Y ')
# 	katadasar[x] = x
 

print texts


# Remove stopword
# r = [x.replace(' ' + y + ' ', ' Q ') for x in texts for y in x.split() if re.findall(pattern, y)]
# print r


print("--- Done %s seconds ---" % (time.time() - start_time))