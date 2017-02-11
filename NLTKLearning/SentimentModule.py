#!/usr/bin/python
#-*-coding:utf-8-*-
'''@author:duncan'''
import nltk
import random
# 多学习器-必须继承nltk的分类器
from nltk.classify import ClassifierI
# 投票机制选出投票最多的分类结果
from statistics import mode
import pickle
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import os


project_path = os.path.abspath("..")
pickle_path = project_path + "/NLTKLearning/pickle_algos"
# 定义投票分类器
class VotedClassifier(ClassifierI):
    # 初始化分类器
    def __init__(self,*classifiers):
        self._classifiers = classifiers
    # 分类
    def classify(self, features):
        votes = []
        for c in self._classifiers:
            v = c.classify(features)
            votes.append(v)
        return mode(votes)
    # 算出置信度
    def confidence(self,features):
        votes = []
        for c in self._classifiers:
            v = c.classify(features)
            votes.append(v)
        choice_votes = votes.count(mode(votes))
        conf = choice_votes * 1.0 / len(votes)
        # print mode(votes) + " number is %d " % votes.count(mode(votes)) + " total number is %d" % len(votes)
        return conf

# 加载文档
documents_f = open(pickle_path + "/documents.pickle","rb")
documents = pickle.load(documents_f)
documents_f.close()

# 加载特征属性
word_features5k_f = open(pickle_path + "/word_features5K.pickle","rb")
word_features5k = pickle.load(word_features5k_f)
word_features5k_f.close()

twitter_stop_words = ["@","from","TO","to",":","!",".","#","https","RT","URL","in","&",";","re"]
def Word2Features(document):
    words = word_tokenize(document)
    words = set([w for w in words if w not in (stopwords.words("english") and twitter_stop_words)])
    # print words
    features = {}
    for w in word_features5k:
        features[w] = (w in words)
    return features

# 加载之前保存的训练好的分类器模型
open_file = open(pickle_path + "/naivebayes.pickle","rb")
classifier = pickle.load(open_file)
open_file.close()

open_file = open(pickle_path + "/MNB_classifier.pickle","rb")
MNB_classifier = pickle.load(open_file)
open_file.close()

open_file = open(pickle_path + "/BernoulliNB_classifier.pickle","rb")
BernoulliNB_classifier = pickle.load(open_file)
open_file.close()

open_file = open(pickle_path + "/LogisticRegression_classifier.pickle","rb")
LogisticRegression_classifier = pickle.load(open_file)
open_file.close()

open_file = open(pickle_path + "/LinearSVC_classifier.pickle","rb")
LinearSVC_classifier = pickle.load(open_file)
open_file.close()

open_file = open(pickle_path +"/SGDC_classifier.pickle","rb")
SGDC_classifier = pickle.load(open_file)
open_file.close()

voted_classifier = VotedClassifier(classifier,LinearSVC_classifier,MNB_classifier,BernoulliNB_classifier,LogisticRegression_classifier,SGDC_classifier)

def sentiment(text):
    sentFeatures = Word2Features(text)
    return voted_classifier.classify(sentFeatures),voted_classifier.confidence(sentFeatures)

