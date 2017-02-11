#!/usr/bin/python
#-*-coding:utf-8-*-
'''@author:duncan'''
import sys
import os
import time
sys.path.append("..")
import NLTKLearning.SentimentModule as senti

project_path = os.path.abspath("..")
data_folder_path = "/TweetsProcess/TweetsSamples/"
filename = "victoriabeckham"
new_file_path = project_path + data_folder_path + filename

# 测试情感
with open(new_file_path) as f:
    doc = f.readlines()

starttime = time.time()
print (senti.sentiment(str(doc).decode('utf-8')))
print "耗时%fs" % (time.time() - starttime)