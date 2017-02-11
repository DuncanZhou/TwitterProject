#!/usr/bin/python
#-*-coding:utf-8-*-
'''@author:duncan'''
from sklearn.externals import joblib
import numpy as np
from sklearn import datasets

twenty_train = datasets.load_files("/home/duncan/data/20news-bydate/20news-bydate-train")
twenty_test = datasets.load_files("/home/duncan/data/20news-bydate/20news-bydate-test")

text_clf = joblib.load("/home/duncan/sklearn-SGDclf-doc")
predicted = text_clf.predict(twenty_test.data)

print np.mean(predicted == twenty_test.target)