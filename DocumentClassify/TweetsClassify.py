#!/usr/bin/python
#-*-coding:utf-8-*-
'''@author:duncan'''

import os
import pickle

project_folder_path = os.path.abspath(".." + os.path.sep + "..")
project_path = os.path.abspath("..")
data_folder_path = "/TweetsSamples/"
famouse_tweets_folder_path = project_folder_path + "/TweetsSamples/famous_users_tweets/"
pickle_path = project_path + "/DocumentClassify/pickles/"
tf_transformer_path = pickle_path + "tf_transformer.picle"
categories_path = pickle_path + "categories.pickle"
MultinomialNB_classifier_path = pickle_path + "MultinomialNB_classifier.pickle"
count_vect_path = pickle_path + "count_vect.pickle"

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



def Accuracy(resdic,users):
    '''
    :param resdic: 格式: {screen_name:category}
    :param users:  格式: {name,screen_name,category}
    :return:准确率
    '''
    correct = 0
    for dickey in resdic.keys():
        for user in users:
            if dickey == user.screen_name and resdic[dickey] == user.category:
                correct += 1
                break
    return (correct * 1.0 / len(resdic))

# 测试分类器效果
def test():
    # 读取20个名人screenname/name/标注分类
    open_file = open(pickle_path + "20famous.pickle")
    famous = pickle.load(open_file)
    open_file.close()
    famous_screen_name = os.listdir(famouse_tweets_folder_path)
    # print famous_screen_name
    correct  = 0
    for name in famous_screen_name:
        filename = name
        file_path = famouse_tweets_folder_path + filename
        text = getTweets(file_path)
        category = Classify(text)
        for user in famous:
            if name == user[0] and user[2] == category:
                correct += 1
                break
        print "%s => %s" % (name,category)
    print "以标注的20个名人为准准确率为:"
    print (correct * 1.0 / 20)