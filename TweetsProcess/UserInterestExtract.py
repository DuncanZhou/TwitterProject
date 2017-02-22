#!/usr/bin/python
#-*-coding:utf-8-*-
'''@author:duncan'''
import sys
import os
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import pickle

project_path = os.path.abspath("..")
twitter_data_folder_path = "/TweetsProcess/TweetsSamples/"
slang_data_folder_path = "/TweetsProcess/SlangDictionary/"
slangfilename = "Slang.pickle"
filename = "realDonaldTrump"
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
    # wordlist = [ps.stem(w[0],w[1]) for w in pos]
    # pos = nltk.pos_tag(wordslist)
    return pos
'''
步骤2：兴趣词或短语生成候选集
兴趣词的模式为
单个词形式：Noun|Adjective|Verb
词组形式：(Verb?)(Adjective|Noun)Noun+
动词和名词先做词性还原
'''

def Generation(pos):
    lemmatizer = WordNetLemmatizer()
    single_pattern = ["N","J","V"]
    SingleCandidate = []
    MultiCandidate = []
    for w in pos:
        if w[1][0] in single_pattern:
            if w[1][0] == 'V':
                word = lemmatizer.lemmatize(w[0],'v')
            elif(w[1][0] == 'N'):
                word = lemmatizer.lemmatize(w[0])
            else:
                word = lemmatizer.lemmatize(w[0],'a')
            SingleCandidate.append(word)
    # print SingleCandidate
    i = 0
    while(i < len(pos) - 1):
        phase = ""
        if (pos[i])[1][0] == 'V' and (pos[i + 1][1][0] == 'N' or pos[i + 1][1][0] == "J"):
            if pos[i + 1][1][0] == 'N':
                suffix = lemmatizer.lemmatize(pos[i + 1][0],'a')
            else:
                suffix = lemmatizer.lemmatize(pos[i + 1][0],'n')
            phase += lemmatizer.lemmatize((pos[i])[0],'v') + " " + suffix
            i = i + 2
            while(i < len(pos) and (pos[i])[1][0] == 'N'):
                phase += " " + lemmatizer.lemmatize((pos[i])[0])
                i += 1
            MultiCandidate.append(phase)
        elif(pos[i][1][0] == "J" and pos[i + 1][1][0] == "N"):
            if((i !=0 and pos[i - 1 ][1][0] != "V") or i == 0):
                phase +=lemmatizer.lemmatize((pos[i])[0],"a") + " " + lemmatizer.lemmatize((pos[i + 1])[0])
                i += 2
                while(i < len(pos) and (pos[i])[1][0] == 'N'):
                    phase += " " + lemmatizer.lemmatize((pos[i])[0],"n")
                    i += 1
            MultiCandidate.append(phase)
        elif(pos[i][1][0] == "N" and pos[i + 1][1][0] == "N"):
            if((i != 0 and pos[i - 1][1][0] != "V" and pos[i - 1][1][0] != "J") or i ==0):
                phase += lemmatizer.lemmatize((pos[i])[0]) + " " + lemmatizer.lemmatize((pos[i + 1])[0])
                i += 2
                while(i < len(pos) and (pos[i])[1][0] == 'N'):
                    phase += " " + lemmatizer.lemmatize((pos[i])[0])
                    i += 1
            MultiCandidate.append(phase)
        else:
            i += 1
    if len(MultiCandidate) != 0 and len(SingleCandidate) != 0:
        print MultiCandidate + SingleCandidate

'''
步骤3：候选集排序
'''

# 测试文本
# test_text = "I like playing table tennis in my spare time! https://wwww.baidu.com @ZhaoLei How about you?"
# Generation(PreProcess(test_text))

doc = ""
user_tweet_id = 1
with open(new_file_path,"rb") as f:
    lines = f.readlines()
    for line in lines:
        line.replace("\n","")
        print "user tweet id is %d" % user_tweet_id
        if user_tweet_id < 300:
            Generation(PreProcess(line.decode("utf-8")))
        else:
            break
        user_tweet_id += 1










