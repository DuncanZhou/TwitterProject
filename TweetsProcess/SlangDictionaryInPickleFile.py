#!/usr/bin/python
#-*-coding:utf-8-*-
'''@author:duncan'''

import os
import pickle
'''
read the No-slang file and convert to dictionary
'''
project_path = os.path.abspath("..")
data_folder_path = "/TweetsProcess/SlangDictionary/"
filename = "No-Slang"
file_path = project_path + data_folder_path + filename

Slang = {}
with open(file_path) as f:
    lines = f.readlines()
    for line in lines:
        dic = line.split(":")
        key = dic[0].rstrip()
        Slang[key] = dic[1].replace("\n","")
'''
将俚语字典持久化
'''
slang_pickle_file = project_path + data_folder_path + "Slang.pickle"
save_Slang_dic = open(slang_pickle_file,"wb")
pickle.dump(Slang,save_Slang_dic)
save_Slang_dic.close()
'''
俚语字典已保存
'''


