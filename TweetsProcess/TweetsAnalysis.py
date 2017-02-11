#!/usr/bin/python
#-*-coding:utf-8-*-
'''@author:duncan'''

import nltk
from nltk.tokenize import word_tokenize
import os
from nltk.corpus import stopwords
from nltk import FreqDist
from statistics import mode

project_path = os.path.abspath("..")
data_folder_path = "/TweetsProcess/TweetsSamples/"
filename = "realDonaldTrump"
file_path = project_path + data_folder_path + filename
with open(file_path) as f:
    doc = f.readlines()
# 从推文中获取主题
topics = []
for line in doc:
    str = line.split(" ")
    for s in str:
        if len(s) > 1 and s[0] == '#' and (s[1] >= 'A' and s[1] <= 'Z'):
            s = s.replace("\r\n","")
            topics.append(s[1:])
print set(topics)
print len(set(topics))
print mode(topics)

# 从中提取名词
# allow_types = ['N']
# twitter_stop_words = ["@","from","TO","to",":","!",".","#","https","RT","URL","in","&",";","re","'","[","]","\\r\\n","http","'RT","Thank","time","today","tomorrow"]
# all_words = word_tokenize(str(doc).decode('utf-8'))
# words = [w for w in all_words if w not in (stopwords.words("english") and twitter_stop_words)]
# pos_words = nltk.pos_tag(words)
# noun_words = []
# for w in pos_words:
#     if w[1][0] in allow_types:
#         noun_words.append(w[0])
# noun_words = FreqDist(noun_words)
# print noun_words.most_common(20)