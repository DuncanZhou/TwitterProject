#!/usr/bin/python
#-*-coding:utf-8-*-
'''@author:duncan'''
import sys
import os
from nltk.tokenize import word_tokenize

project_path = os.path.abspath("..")
data_folder_path = "/TweetsProcess/TweetsSamples/"
filename = "victoriabeckham"
suffix = ".txt"
new_file_path = project_path + data_folder_path + filename
data_full_path = new_file_path + suffix
def PreProcess(filepath):
    with open(filepath,"r") as f:
        newdoc = []
        lines = f.readlines()
        flag = 0
        for line in lines:
            flag += 1
            if flag % 2 == 0:
                try:
                    word_tokenize(line)
                    newdoc.append(line)
                except Exception as e:
                    pass

    with open(new_file_path,"w") as f:
        f.writelines(newdoc)
    return new_file_path
print "推文预处理完成，新文件目录为:"
print PreProcess(data_full_path)







