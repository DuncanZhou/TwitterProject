#!/usr/bin/python
#-*-coding:utf-8-*-
'''@author:duncan'''

from sklearn import datasets
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
import numpy as np


'''
装载数据
'''
training_set = datasets.load_files("/home/duncan/data/20news-bydate/20news-bydate-train")
testing_set = datasets.load_files("/home/duncan/data/20news-bydate/20news-bydate-test")
# print training_set.target_names

# 统计词频
count_vect = CountVectorizer(stop_words="english",decode_error="ignore")
x_train_counts = count_vect.fit_transform(training_set.data)
#wordlists = count_vect.get_feature_names()
# print wordlists[0]
# print wordlists
# # print x_train_counts.shape
#
# # 利用词频作为特征，训练得到多项式分类器
# clf = MultinomialNB().fit(x_train_counts,training_set.target)
#
# x_test_counts = count_vect.transform(testing_set.data)
# predicted = clf.predict(x_test_counts)
# print "基于词频准确率为:"
# print np.mean(predicted == testing_set.target)
#
# 基于词频逆文档词频(TF-IDF)为特征
print "计算tf-idf"
tf_transformer = TfidfTransformer(use_idf = True).fit(x_train_counts)
x_train_tf = tf_transformer.transform(x_train_counts)
#
# x_test_counts = count_vect.transform(testing_set.data)
# x_test_tf = tf_transformer.transform(x_test_counts)
# predicted = clf.predict(x_test_tf)
# print "基于词频-逆文档词频准确率为:"
# print np.mean(predicted == testing_set.target)


