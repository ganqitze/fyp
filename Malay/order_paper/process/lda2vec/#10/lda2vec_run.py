# Author: Chris Moody <chrisemoody@gmail.com>
# License: MIT

# This simple example loads the newsgroups data from sklearn
# and train an LDA-like model on it
import os.path
import pickle
import time
import csv
import time
from datetime import datetime
start_time = time.time()

import chainer
from chainer import cuda
from chainer import serializers
import chainer.optimizers as O
import numpy as np

from lda2vec import utils
from lda2vec import prepare_topics, print_top_words_per_topic, topic_coherence
from lda2vec_model import LDA2Vec


base_path_lin  = "/home/User/fyp/Malay/order_paper/process/lda2vec/#10/"
base_path_win = "C:/Users/User/Desktop/fyp/Malay/order_paper/process/lda2vec/#10/"

topic_file = os.path.join(base_path_lin, "topic.csv")
coherence_file = os.path.join(base_path_lin, "coherence.csv")

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

gpu_id = int(os.getenv('CUDA_GPU', 0))
# cuda.get_device(gpu_id).use()
print "Using GPU " + str(gpu_id)

# # You must run preprocess.py before this data becomes available
# vocab = pickle.load(open('../data/vocab', 'r'))
# corpus = pickle.load(open('../data/corpus', 'r'))
# data = np.load(open('../data/data.npz', 'r'))
# flattened = data['flattened']
# story_id = data['story_id']
# author_id = data['author_id']
# time_id = data['time_id']
# ranking = data['ranking'].astype('float32')
# score = data['score'].astype('float32')

# # My part
vocab = pickle.load(open('../../../data/vocab.p', 'rb'))
corpus = pickle.load(open('../../../data/corpus.p', 'rb'))
data = np.load(open('../../../data/data.npz', 'rb'))
flattened = data['flattened']
paper_id = data['paper_id']
date_id = data['date_id']

# # Model Parameters
# # Number of documents
# n_stories = story_id.max() + 1
# # Number of users
# n_authors = author_id.max() + 1
# # Number of unique words in the vocabulary
# n_vocab = flattened.max() + 1
# # Number of dimensions in a single word vector
# n_units = 256
# # Number of topics to fit
# n_story_topics = 40
# n_author_topics = 20
# batchsize = 4096
# # Get the string representation for every compact key
# words = corpus.word_list(vocab)[:n_vocab]

# # My part
# Number of documents
n_stories = paper_id.max() + 1
# Number of unique words in the vocabulary
n_vocab = flattened.max() + 1
# Number of dimensions in a single word vector
n_units = 256
# Number of topics to fit
n_story_topics = 10
batchsize = 4096
# Get the string representation for every compact key
words = corpus.word_list(vocab)[:n_vocab]
print len(words)

# # How many tokens are in each story
# sty_idx, lengths = np.unique(story_id, return_counts=True)
# sty_len = np.zeros(sty_idx.max() + 1, dtype='int32')
# sty_len[sty_idx] = lengths
# print 'story token = ' + sty_len[sty_idx] 

# My part
paper_idx, lengths = np.unique(paper_id, return_counts=True)
paper_len = np.zeros(paper_idx.max() + 1, dtype='int32')
paper_len[paper_idx] = lengths
# print paper_len[paper_idx]
# # print 'story token = ' + paper_len[paper_idx] 

# # How many tokens are in each author
# aut_idx, lengths = np.unique(author_id, return_counts=True)
# aut_len = np.zeros(aut_idx.max() + 1, dtype='int32')
# aut_len[aut_idx] = lengths
# print 'author token = ' + aut_len[aut_idx]

# # Count all token frequencies
# tok_idx, freq = np.unique(flattened, return_counts=True)
# term_frequency = np.zeros(n_vocab, dtype='int32')
# term_frequency[tok_idx] = freq
# print 'token freq ' + term_frequency[tok_idx] 

# My part
tok_idx, freq = np.unique(flattened, return_counts=True)
term_frequency = np.zeros(n_vocab, dtype='int32')
term_frequency[tok_idx] = freq
# print 'token freq ', term_frequency[tok_idx] 

# model = LDA2Vec(n_stories=n_stories, n_story_topics=n_story_topics,
#                 n_authors=n_authors, n_author_topics=n_author_topics,
#                 n_units=n_units, n_vocab=n_vocab, counts=term_frequency,
#                 n_samples=15)
# if os.path.exists('lda2vec.hdf5'):
#     print "Reloading from saved"
#     serializers.load_hdf5("lda2vec.hdf5", model)
# # model.to_gpu()
# optimizer = O.Adam()
# optimizer.setup(model)
# clip = chainer.optimizer.GradientClipping(5.0)
# optimizer.add_hook(clip)

# My part
model = LDA2Vec(n_stories=n_stories, n_story_topics=n_story_topics, n_units=n_units, n_vocab=n_vocab, counts=term_frequency, n_samples=15)
if os.path.exists('lda2vec.hdf5'):
    print "Reloading from saved"
    serializers.load_hdf5("lda2vec.hdf5", model)
# model.to_gpu()
optimizer = O.Adam()
optimizer.setup(model)
clip = chainer.optimizer.GradientClipping(5.0)
optimizer.add_hook(clip)

# j = 0
# epoch = 0
# fraction = batchsize * 1.0 / flattened.shape[0]
# for epoch in range(5000):
#     ts = prepare_topics(cuda.to_cpu(model.mixture_sty.weights.W.data).copy(),
#                         cuda.to_cpu(model.mixture_sty.factors.W.data).copy(),
#                         cuda.to_cpu(model.sampler.W.data).copy(),
#                         words)
#     print_top_words_per_topic(ts)
#     ts['doc_lengths'] = sty_len
#     ts['term_frequency'] = term_frequency
#     np.savez('topics.story.pyldavis', **ts)
#     ta = prepare_topics(cuda.to_cpu(model.mixture_aut.weights.W.data).copy(),
#                         cuda.to_cpu(model.mixture_aut.factors.W.data).copy(),
#                         cuda.to_cpu(model.sampler.W.data).copy(),
#                         words)
#     print_top_words_per_topic(ta)
#     ta['doc_lengths'] = aut_len
#     ta['term_frequency'] = term_frequency
#     np.savez('topics.author.pyldavis', **ta)
#     for s, a, f in utils.chunks(batchsize, story_id, author_id, flattened):
#         t0 = time.time()
#         optimizer.zero_grads()
#         l = model.fit_partial(s.copy(), a.copy(), f.copy())
#         prior = model.prior()
#         loss = prior * fraction
#         loss.backward()
#         optimizer.update()
#         msg = ("J:{j:05d} E:{epoch:05d} L:{loss:1.3e} "
#                "P:{prior:1.3e} R:{rate:1.3e}")
#         prior.to_cpu()
#         loss.to_cpu()
#         t1 = time.time()
#         dt = t1 - t0
#         rate = batchsize / dt
#         logs = dict(loss=float(l), epoch=epoch, j=j,
#                     prior=float(prior.data), rate=rate)
#         print msg.format(**logs)
#         j += 1
#     serializers.save_hdf5("lda2vec.hdf5", model)

# My part
j = 0
epoch = 0
fraction = batchsize * 1.0 / flattened.shape[0]
avg = sum_coherence = 0
while avg < 0.90 and epoch < 1000:
# for epoch in range(1):
    ts = prepare_topics(cuda.to_cpu(model.mixture_sty.weights.W.data).copy(),
                        cuda.to_cpu(model.mixture_sty.factors.W.data).copy(),
                        cuda.to_cpu(model.sampler.W.data).copy(),
                        words)
    # print_top_words_per_topic(ts)
    topic_words = print_top_words_per_topic(ts)
    save_topic(topic_words)
    ts['doc_lengths'] = paper_len
    ts['term_frequency'] = term_frequency
    np.savez('topics.story.pyldavis', **ts)
    for p, f in utils.chunks(batchsize, paper_id, flattened):
        sum_coherence = 0
        avg = 0
        t0 = time.time()
        optimizer.zero_grads()
        l = model.fit_partial(p.copy(), f.copy())
        prior = model.prior()
        loss = prior * fraction
        loss.backward()
        optimizer.update()
        msg = ("J:{j:05d} E:{epoch:05d} L:{loss:1.3e} "
               "P:{prior:1.3e} R:{rate:1.3e}")
        prior.to_cpu()
        loss.to_cpu()
        t1 = time.time()
        dt = t1 - t0
        rate = batchsize / dt
        logs = dict(loss=float(l), epoch=epoch, j=j,
                    prior=float(prior.data), rate=rate)
        print msg.format(**logs)
        j += 1
    coherence = topic_coherence(topic_words, services=['cv'])
    coherence_train = [datetime.now().strftime("%Y-%m-%d %H:%M")]
    for j in range(n_story_topics):
        print j, coherence[(j, 'cv')]
        if coherence[(j, 'cv')] == None:
            coherence[(j, 'cv')] = -1
        sum_coherence += coherence[(j, 'cv')]
        coherence_train.append(coherence[(j, 'cv')])
    avg = sum_coherence/n_story_topics
    print avg
    epoch += 1
    coherence_train.append(avg)
    save_coherence(coherence_train)
    serializers.save_hdf5("lda2vec.hdf5", model)
else:
    serializers.save_hdf5("lda2vec.hdf5", model)
    print("COMPLETE with epoch: ", epoch)
print("--- Done all! %s seconds ---" % (time.time() - start_time))
