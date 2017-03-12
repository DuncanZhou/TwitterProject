#!/usr/bin/python
#-*-coding:utf-8-*-
'''@author:duncan'''

import os
import pickle

project_folder_path = os.path.abspath(".." + os.path.sep + "..")
project_path = os.path.abspath("..")
data_folder_path = "/TweetsSamples/"
famouse_tweets_folder_path = project_folder_path + "/TweetsSamples/famous_users_tweets/"
piclke_path = project_path + "/DocumentClassify/pickles/"
tf_transformer_path = piclke_path + "tf_transformer.picle"
categories_path = piclke_path + "categories.pickle"
MultinomialNB_classifier_path = piclke_path + "MultinomialNB_classifier.pickle"
count_vect_path = piclke_path + "count_vect.pickle"

def Classify(text):
    '''
    :param text:待分类的文本
    :return: 返回分类结果
    '''
    if text == "" or text == None:
        return "None"
    txt = []
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
    return result

# 获取推文
def getTweets(file_path):
    '''

    :param file_path:推文文件路径
    :return: 文本内容
    '''
    text = ""
    with open(file_path) as f:
        doc = f.readlines()
        for line in doc:
            text += line.replace("\n","")
    return text

# 测试分类器效果
def test():
    famous_screen_name = os.listdir(famouse_tweets_folder_path)
    # print famous_screen_name
    for name in famous_screen_name:
        filename = name
        file_path = famouse_tweets_folder_path + filename
        text = getTweets(file_path)
        print "%s => %s" % (filename,Classify(text))
test()