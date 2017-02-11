#!/usr/bin/python
#-*-coding:utf-8-*-
'''@author:duncan'''

import os
import pickle

project_path = os.path.abspath("..")
data_folder_path = "/TweetsProcess/TweetsSamples/"
filename = "victoriabeckham"
file_path = project_path + data_folder_path + filename
piclke_path = project_path + "/DocumentClassify/pickles/"
tf_transformer_path = piclke_path + "tf_transformer.picle"
categories_path = piclke_path + "categories.pickle"
MultinomialNB_classifier_path = piclke_path + "MultinomialNB_classifier.pickle"
count_vect_path = piclke_path + "count_vect.pickle"
txt = []
text = ""
with open(file_path) as f:
    doc = f.readlines()
    for line in doc:
        text += line.replace("\n","")
# print text
txt.append(text)
# 测试数据转化为特征向量

open_file = open(count_vect_path)
count_vect = pickle.load(open_file)
open_file.close()

x_test_counts = count_vect.transform(txt)

open_file = open(tf_transformer_path)
tf_transformer = pickle.load(open_file)
open_file.close()

x_test_tf = tf_transformer.transform(x_test_counts)
# 分类
open_file = open(MultinomialNB_classifier_path)
clf = pickle.load(open_file)
open_file.close()

open_file = open(categories_path)
target_names = pickle.load(open_file)
open_file.close()

result = target_names[clf.predict(x_test_tf)[0]]
print result