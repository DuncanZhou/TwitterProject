#!/usr/bin/python
#-*-coding:utf-8-*-
'''@author:duncan'''
from sklearn.externals import joblib
import numpy as np
from sklearn import datasets
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer

twenty_train = datasets.load_files("/home/duncan/data/20news-bydate/20news-bydate-train")
twenty_test = datasets.load_files("/home/duncan/data/20news-bydate/20news-bydate-test")


docs_news = ['God is love','OpenGL on the GPU is fast','I have a pen.I have an apple.En~!ApplePen','How are you? I\'m fine.Thank you']

text_clf1 = joblib.load("/home/duncan/sklearn-SGDclf-doc")
text_clf2 = joblib.load("/home/duncan/sklearn-bayesclf-doc")
predicted1 = text_clf1.predict(docs_news)
predicted2 = text_clf2.predict(docs_news)
res = []
for doc,category1,category2 in zip(docs_news,predicted1,predicted2):
    labels = []
    if labels.__contains__(category1) == False:
        labels.append(category1)
    if labels.__contains__(category2) == False:
        labels.append(category2)
    res.append(map(lambda x:twenty_train.target_names[x],labels))
    #print doc,res
dict = zip(docs_news,res)
i = 0
for dic in dict:
    print dic[0].__str__() + " => " + '.'.join(res[i])
    i += 1
