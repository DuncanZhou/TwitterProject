#!/usr/bin/python
#-*-coding:utf-8-*-
'''@author:duncan'''
import sys
import os
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import pickle

project_path = os.path.abspath("..")
twitter_data_folder_path = "/TweetsProcess/TweetsSamples/"
slang_data_folder_path = "/TweetsProcess/SlangDictionary/"
slangfilename = "Slang.pickle"
filename = "victoriabeckham"
suffix = ".txt"
new_file_path = project_path + twitter_data_folder_path + filename
twitter_data_full_path = new_file_path + suffix
slang_file_path =  project_path + slang_data_folder_path + slangfilename
'''
初步读入预处理
'''
# def PreProcess(filepath):
#     with open(filepath,"r") as f:
#         newdoc = []
#         lines = f.readlines()
#         flag = 0
#         for line in lines:
#             flag += 1
#             if flag % 2 == 0:
#                 try:
#                     word_tokenize(line)
#                     newdoc.append(line)
#                 except Exception as e:
#                     pass
#
#     with open(new_file_path,"w") as f:
#         f.writelines(newdoc)
#     return new_file_path
# print "推文预处理完成，新文件目录为:"
# print PreProcess(twitter_data_full_path)
twitter_stop_words = ["@","from","TO","to",":","!",".","#","https","RT","URL","in","&",";","re","''","?","thank","Thank"]
'''
步骤1:推文预处理
读入推文后先去除回复性对话推文  分词  去除超链接  去除停用词 转换俚语和缩写形式  词干还原  词性标注
'''
def PreProcess(text):
    ps = PorterStemmer()
    open_file = open(slang_file_path,"rb")
    slang = pickle.load(open_file)
    open_file.close()
    wordslist = []
    words = word_tokenize(text)
    for word in words:
        if word.find("https") == -1 and word.find("/") == -1  and word not in (stopwords.words("english") and twitter_stop_words):
            if word in slang:
                word = slang[word]
                subwords = word.split(" ")
                for subword in subwords:
                    if subword not in (stopwords.words("english") and twitter_stop_words):
                        wordslist.append(subword)
            else:
                if len(word) > 2:
                    wordslist.append(word)
    pos = nltk.pos_tag(wordslist)
    return pos
'''
步骤2：兴趣词或短语生成候选集
兴趣词的模式为
单个词形式：Noun|Adjective|Verb
词组形式：(Verb?)(Adjective|Noun)Noun+
'''

def Generation(pos):
    single_pattern = ["N","A","V"]
    SingleCandidate = []
    MultiCandidate = []
    for w in pos:
        if w[1][0] in single_pattern:
            SingleCandidate.append(w[0])
    print SingleCandidate
'''
步骤3：候选集排序
'''
doc = ""
with open(new_file_path,"rb") as f:
    lines = f.readlines()
    i = 0
    for line in lines:
        if i >= 100:
            break
        line.replace("\n","")
        Generation(PreProcess(line.decode('utf-8')))
        i += 1










