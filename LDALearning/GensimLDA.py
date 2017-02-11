#!/usr/bin/python
#-*-coding:utf-8-*-
'''@author:duncan'''

import codecs
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from gensim.models import LdaModel
from gensim.corpora import Dictionary

train = []
with open("/home/duncan/TwitterProject/TweetsProcess/TweetsSamples/taylorswift13") as f:
    doc = f.readlines()

twitter_stop_words = ["@","from","TO","to",":","!",".","#","https","RT","URL","in","&",";","re","http"]
for line in doc:
    words = word_tokenize(line.decode('utf-8'),language="english")
    train.append([w for w in words if w not in (stopwords.words("english") and twitter_stop_words)])

dictionary = Dictionary(train)
corpus = [dictionary.doc2bow(text) for text in train]
lda = LdaModel(corpus=corpus,id2word=dictionary,num_topics=100)
for top in lda.print_topics(20,10):
    print top