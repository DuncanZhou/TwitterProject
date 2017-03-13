#!/usr/bin/python
#-*-coding:utf-8-*-
'''@author:duncan'''

import os
import pickle
from sklearn import datasets
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB

'''
装载训练集
'''
project_path = os.path.abspath("..")
piclke_path = project_path + "/DocumentClassify/pickles/"
'''
BCC分类：business/entertainment/politics/sport/technology
CNN分类：agriculture/economy/education/entertainment/military/politics/religion/sports/technology

DataSet1 是 CNN + BCC新闻数据集(分类融合起来)
DataSet2 是 BCC新闻数据集
DataSet3 是 CNN新闻数据集
DataSet4 是 CNN + BCC新闻数据集(CNN填补BCC没有的分类)
'''
data_set_path = "/DocumentClassify/DataSet4"
training_set_path = project_path + data_set_path
# print training_set_path
training_set = datasets.load_files(training_set_path)
print "文本类别分别是:"
categories = training_set.target_names
print categories
categories_path = piclke_path + "categories.pickle"
save_categories = open(categories_path,"wb")
pickle.dump(categories,save_categories)
save_categories.close()

# 统计词频
count_vect = CountVectorizer(stop_words="english",decode_error="ignore")
x_train_counts = count_vect.fit_transform(training_set.data)

count_vect_path = piclke_path + "count_vect.pickle"
save_count_vect = open(count_vect_path,"wb")
pickle.dump(count_vect,save_count_vect)
save_count_vect.close()
print "词频向量已保存"

# 计算词频-逆文档词频
tf_transformer = TfidfTransformer().fit(x_train_counts)
# 持久化tf_transformer
tf_transformer_path = piclke_path + "tf_transformer.picle"
save_tf_transformer = open(tf_transformer_path,"wb")
pickle.dump(tf_transformer,save_tf_transformer)
save_tf_transformer.close()
print "词频-文档逆词频已保存"
x_train_tf = tf_transformer.transform(x_train_counts)

# 多项式贝叶斯分类器分类
clf = MultinomialNB().fit(x_train_tf,training_set.target)

print "分类器训练完成......."
MultinomialNB_classifier_path = piclke_path + "MultinomialNB_classifier.pickle"
save_tweets_MultinomialNB_classifier = open(MultinomialNB_classifier_path,"wb")
pickle.dump(clf,save_tweets_MultinomialNB_classifier)
save_tweets_MultinomialNB_classifier.close()

print "分类器已保存，目录为" + MultinomialNB_classifier_path

