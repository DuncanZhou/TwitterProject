#!/usr/bin/python
#-*-coding:utf-8-*-
'''@author:duncan'''

import os
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import pickle

project_path = os.path.abspath("..")
twitter_data_folder_path = "/TweetsProcess/TweetsSamples/"
slang_data_folder_path = "/TweetsProcess/SlangDictionary/"
topverbwords_folder_path = "/TweetsProcess/Top100VerbWords/"
topverbwords_filename = "Top100VerbWords.pickle"
slangfilename = "Slang.pickle"

suffix = ".txt"

slang_file_path =  project_path + slang_data_folder_path + slangfilename
topverbwords_file_path = project_path + topverbwords_folder_path + topverbwords_filename
totalcandidate = []

twitter_stop_words = ["@","from","TO","to",":","!",".","#","https","RT","URL","in","&",";","re","''","?","thank","thanks","do","be","today","yesterday","tomorrow","night","tonight","day","year","last"]
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
        if word.find("http") == -1 and word.find("https") == -1 and word.find("/") == -1  and word not in (stopwords.words("english") and twitter_stop_words):
            if word in slang:
                word = slang[word]
                subwords = word.split(" ")
                for subword in subwords:
                    if subword not in (stopwords.words("english") and twitter_stop_words):
                        wordslist.append(subword.lower())
            else:
                if len(word) > 2:
                    wordslist.append(word.lower())
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
    # 读入前100的动词
    with open(topverbwords_file_path,"r") as f:
        verbwords = f.readlines()
    topverbwords = map(lambda line:line.replace("\n",""),verbwords)
    global totalcandidate
    lemmatizer = WordNetLemmatizer()
    single_pattern = ["N","J","V"]
    SingleCandidate = []
    MultiCandidate = []
    for w in pos:
        word = ""
        if w[1][0] in single_pattern:
            if w[1][0] == 'V':
                # 排除前100常用的动词
                word = lemmatizer.lemmatize(w[0],'v')
                if word in topverbwords:
                    continue
            elif(w[1][0] == 'N'):
                word = lemmatizer.lemmatize(w[0])
            else:
                word = lemmatizer.lemmatize(w[0],'a')
            if len(word) != 0 and word not in (stopwords.words("english") and twitter_stop_words) and len(word) <= 20:
                SingleCandidate.append(word.lower())
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
        totalcandidate += MultiCandidate + SingleCandidate

'''
步骤3：候选集排序
单用户使用TF词频排序
'''
def CalculateTF(totalcandidate):
    vac = set(totalcandidate)
    vacdic = {}
    for phase in vac:
        vacdic[phase] = totalcandidate.count(phase)
    # 按照键值排序
    vacdic = sorted(vacdic.items(),key = lambda dic:dic[1],reverse = True)
    # 输出前100个兴趣候选集
    print vacdic[:100]

# 测试文本
# test_text = "I like playing table tennis in my spare time! https://wwww.baidu.com @ZhaoLei How about you?"
# Generation(PreProcess(test_text))

def getUserInterestTop100(UserName):
    interest_pickle_path = project_path + "/TweetsProcess/UserInterestCandidate/" + UserName + ".pickle"
    doc = ""
    user_tweet_id = 1
    new_file_path = project_path + twitter_data_folder_path + UserName
    with open(new_file_path,"rb") as f:
        lines = f.readlines()
        for line in lines:
            # 移除回复/对话的推文
            if (line[0]+line[1]) != "RT":
                line.replace("\n","")
                print "user tweet id is %d" % user_tweet_id
                Generation(PreProcess(line.decode("utf-8")))
            user_tweet_id += 1
    # 将用户兴趣候选集持久化
    UerInterestCandidate = CalculateTF(totalcandidate)
    # save_file = open(interest_pickle_path,"wb")
    # pickle.dump(UerInterestCandidate,save_file)
    # save_file.close()
    print "推特用户兴趣候选集已保存"
    return UerInterestCandidate
getUserInterestTop100("victoriabeckham")