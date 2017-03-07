#!/usr/bin/python
#-*-coding:utf-8-*-
'''@author:duncan'''

import os
import math
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import pickle
import re
from numpy import *

project_path = os.path.abspath("..")
project_folder_path = os.path.abspath(".." + os.path.sep + "..")
twitter_data_folder_path = project_folder_path + "/TweetsSamples/"
slang_data_folder_path = "/TweetsProcess/SlangDictionary/"
topverbwords_folder_path = "/TweetsProcess/Top100VerbWords/"
topverbwords_filename = "Top100VerbWords"
slangfilename = "Slang.pickle"

suffix = ".txt"

slang_file_path =  project_path + slang_data_folder_path + slangfilename
topverbwords_file_path = project_path + topverbwords_folder_path + topverbwords_filename

twitter_stop_words = ["@","from","TO","to",":","!",".","#","https","RT","URL","in","&",";","re","''","?","thank","thanks","do","be","today","yesterday","tomorrow","night","tonight","day","year","last","oh","yeah"]
# 读入top100动词
with open(topverbwords_file_path,"r") as f:
    verbwords = f.readlines()
topverbwords = map(lambda line:line.replace("\n",""),verbwords)

'''
兴趣候选集读写处理
'''
def FromFilegetUserInterestCandidate(path,username):
    open_file = open(path + username,"r")
    userInterestCandidate = pickle.load(open_file)
    open_file.close()
    return userInterestCandidate

# 测试文本
# test_text = "I like playing table tennis in my spare time! https://wwww.baidu.com @ZhaoLei How about you?"
# Generation(PreProcess(test_text))

# 得到某一个用户的兴趣候选集,threshold设定读入每个用户的推文数
def getUserInterestTop100(filepath,UserName,threshold):
    usercandidate = []
    interest_pickle_path = project_folder_path + "/InterestCandidate/" + UserName
    interest_set_pickle_path = project_folder_path + "/InterestSetCandidate/" + UserName
    doc = ""
    user_tweet_id = 1
    with open(filepath,"rb") as f:
        lines = f.readlines()
        for line in lines:
            if user_tweet_id < threshold:
                # 移除回复/对话的推文 （是以@XXXX开头）
                if re.match(r"^@[\d|\w|_]+",line) == None:
                    line.replace("\n","")
                    # print "user tweet id is %d" % user_tweet_id
                    usercandidate += Generation(PreProcess(line.decode("utf-8")))
                    user_tweet_id += 1
            else:
                break
    # 将用户兴趣候选集持久化
    UserInterestCandidate = CalculateTF(usercandidate)
    usercandidate_set = set(usercandidate)
    save_file = open(interest_set_pickle_path,"wb")
    pickle.dump(usercandidate_set,save_file)
    save_file.close()
    save_file = open(interest_pickle_path,"wb")
    pickle.dump(UserInterestCandidate,save_file)
    save_file.close()
    print "%s推特用户兴趣候选集已保存" % UserName
    return UserInterestCandidate

# 得到文件夹下所有文件名即twitter用户screenname
def getFileName(path):
    filenameRs = []
    filename = os.listdir(path)
    for f in filename:
        filenameRs.append(f)
    return filenameRs

# 批处理用户
def getUsersInterestCandidate(path):
    users_screen_name = getFileName(path)
    userid = 1
    for username in users_screen_name:
        print "用户id:%s\t姓名:%s" % (userid,username)
        file_path = path + username
        # 先测试读每个用户100条推文
        getUserInterestTop100(file_path,username,100)
        userid += 1

def getNumberoffiles(path):
    filename = []
    filename = os.listdir(path)
    return len(filename)

'''
步骤1:推文预处理
读入推文后先去除回复性对话推文  分词  去除超链接  去除停用词 转换俚语和缩写形式  词干还原  词性标注
'''
def ReadTweets(file):
    tweets = ""
    with open(file,'r') as f:
        lines = f.readlines()
        lineid = 1
        for line in lines:
            if lineid % 2 == 0:
                tweets += line
            lineid += 1
    return tweets

def saveTweets(path):
    filename = os.listdir(path)
    for file in filename:
        tweets = ReadTweets(path + file)
        with open(project_path + twitter_data_folder_path + file[:-4],"w") as f:
            f.writelines(tweets)
        print "%s推文处理完成" % file[:-4]
    print "全部处理完成"


def PreProcess(text):
    # open_file = open(slang_file_path,"rb")
    # slang = pickle.load(open_file)
    # open_file.close()
    # clear @/#/http
    toClear = re.findall(r'[@|#][\d|\w|_]+|http[\w|:|.|/|\d]+',text)
    # print toClear
    for c in toClear:
        text = text.replace(c," ")
    # print text
    wordslist = []
    words = word_tokenize(text)
    # clear @/#/url/emotion
    for word in words:
        # count = 0
        if word not in (stopwords.words("english") and twitter_stop_words):
            # if word in slang:
            # 	count += 1
            # 	print count
            #     word = slang[word]
            #     subwords = word.split(" ")
            #     for subword in subwords:
            #         if subword not in (stopwords.words("english") and twitter_stop_words):
            #             # 转换成小写
            #             wordslist.append(subword.lower())
            # else:
            if len(word) > 2:
                # clear emotion
                if word.isalpha():
                    wordslist.append(word.lower())
    try:
        pos = nltk.pos_tag(wordslist)
    # wordlist = [ps.stem(w[0],w[1]) for w in pos]
    # pos = nltk.pos_tag(wordslist)
    except Exception as e:
        pos = []
    return pos

'''
步骤2：兴趣词或短语生成候选集
兴趣词的模式为
单个词形式：Noun|Adjective|Verb (经测试效果不是很好，暂时选用名词Noun形式)
词组形式：(Verb?)(Adjective|Noun)Noun+ (词组形式暂时选用动词+名词 或  形容词+名词形式)
动词和名词先做词性还原
'''
def Generation(pos):
    if len(pos) < 1:
        return []
    usercandidate = []
    lemmatizer = WordNetLemmatizer()
    single_pattern = ["N","J","V"]
    SingleCandidate = []
    MultiCandidate = []
    for w in pos:
        word = ""
        if w[1][0] in single_pattern:
            # if w[1][0] == 'V':
            #     # 排除前100常用的动词
            #     word = lemmatizer.lemmatize(w[0],'v')
            #     if word in topverbwords:
            #         continue
            if(w[1][0] == 'N'):
                word = lemmatizer.lemmatize(w[0])
            # else:
            #     word = lemmatizer.lemmatize(w[0],'a')
            if len(word) != 0 and word not in (stopwords.words("english") and twitter_stop_words) and len(word) <= 20:
                SingleCandidate.append(word.lower())
    i = 0
    while(i < len(pos) - 2):
        phase = ""
        # verb + adj + n+ or verb n+
        if (pos[i])[1][0] == 'V' and (pos[i + 1][1][0] == 'N' or (pos[i + 1][1][0] == "J" and pos[i + 2][1][0] == "N")):
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
        # adj + n+
        elif(pos[i][1][0] == "J" and pos[i + 1][1][0] == "N"):
            if((i !=0 and pos[i - 1 ][1][0] != "V") or i == 0):
                phase +=lemmatizer.lemmatize((pos[i])[0],"a") + " " + lemmatizer.lemmatize((pos[i + 1])[0])
                i += 2
                while(i < len(pos) and (pos[i])[1][0] == 'N'):
                    phase += " " + lemmatizer.lemmatize((pos[i])[0],"n")
                    i += 1
            MultiCandidate.append(phase)
        # n n+
        # elif(pos[i][1][0] == "N" and pos[i + 1][1][0] == "N"):
        #     if((i != 0 and pos[i - 1][1][0] != "V" and pos[i - 1][1][0] != "J") or i ==0):
        #         phase += lemmatizer.lemmatize((pos[i])[0]) + " " + lemmatizer.lemmatize((pos[i + 1])[0])
        #         i += 2
        #         while(i < len(pos) and (pos[i])[1][0] == 'N'):
        #             phase += " " + lemmatizer.lemmatize((pos[i])[0])
        #             i += 1
        #     MultiCandidate.append(phase)
        else:
            i += 1
    if len(MultiCandidate) != 0 or len(SingleCandidate) != 0:
        # print MultiCandidate + SingleCandidate
        usercandidate = MultiCandidate + SingleCandidate
    return usercandidate

'''
步骤3：候选集排序
单用户使用TF词频排序
'''
def CalculateTF(usercandidate):
    vac = set(usercandidate)
    vacdic = {}
    for phase in vac:
        vacdic[phase] = usercandidate.count(phase)
    # 按照键值排序
    vacdic = sorted(vacdic.items(),key = lambda dic:dic[1],reverse = True)
    # 输出前100个兴趣候选集
    # print vacdic[:100]
    return vacdic[:100]

def CalculateTFIDF(path1,path2):
    filename = os.listdir(path1)
    # 首先将兴趣候选集全部读入内存
    candidate_set = []
    for f in filename:
        open_file = open(path2 + f,"rb")
        ui_candidate_set = pickle.load(open_file)
        open_file.close()
        candidate_set.append(ui_candidate_set)

    totalcandidate = {}
    tcWithTFIDF = {}
    for f in filename:
        totalcandidate[f] = FromFilegetUserInterestCandidate(path1,f)
    for key in totalcandidate.keys():
        ucWithTFIDF = []
        for candidate in totalcandidate[key]:
            tocheck = candidate[0]
            idf = 1
            for user in ui_candidate_set:
                if tocheck in user:
                    idf += 1
            IDF = math.log(len(ui_candidate_set) * 1.0 / idf)
            TFIDF = candidate[1] * IDF
            ucWithTFIDF.append(TFIDF)
        tcWithTFIDF[key] = ucWithTFIDF
    # 将计算好TFIDF的兴趣候选集重新持久化
    save_file = open(project_folder_path + "/TotalCandidateWithTFIDF.pickle","wb")
    pickle.dump(tcWithTFIDF,save_file)
    save_file.close()
    return tcWithTFIDF

# first get the candidate with TFIDF

def getUserCandidate(path):
    filename = os.listdir(path)
    userscandidate = []
    for f in filename:
        userscandidate.append(FromFilegetUserInterestCandidate(path,f))
    return userscandidate

def CalucateSum(matrix,col):
    sum = 0
    for i in range(matrix.shape[0]):
        sum += matrix[i,col]
    return sum

def CalucateWeight(usercandidate):
    matrix = []
    for u1 in range(len(usercandidate)):
        line = []
        for u2 in range(len(usercandidate)):
            weight = min(usercandidate[u1][1],usercandidate[u2][1])
            line.append(weight)
        matrix.append(line)
    newmatrix = oldmatrix = mat(matrix)
    for i in range(newmatrix.shape[0]):
        for j in range(newmatrix.shape[0]):
            newmatrix[i,j] = oldmatrix[i,j] * 1.0 / CalucateSum(oldmatrix,j)
    return newmatrix

# threshold
# dampFactor in (0,1)
def CalucateTextRank(ucMatrix,threshold,dampFactor,uid,InitTRMatrix,uiCandidateWithTFIDF):
    TFIDFMatrix = mat(uiCandidateWithTFIDF[uid]) * (1 - dampFactor)
    # print TFIDFMatrix.shape
    TRMatrix = InitTRMatrix.T
    oldMatrix = TRMatrix
    # iteration
    iteration = 0
    while True:
        newMatrix = TRMatrix = ucMatrix * TRMatrix + TFIDFMatrix.T
        flag = True
        for i in range(newMatrix.shape[0]):
            if math.fabs(newMatrix[i,0] - oldMatrix[i,0]) > threshold:
                flag = False
                break
        if flag == True:
            break
        iteration += 1
        oldMatrix = TRMatrix
    print "the number of iteration is %d " % iteration
    return TRMatrix

def CalucateUCTR(usercandidate,ucTRMatrix):
    ucTR = {}
    i = 0
    for user in usercandidate:
        candidate = user[0]
        TR = ucTRMatrix[i,0]
        i += 1
        ucTR[candidate] = TR
    # 按照ucTR的键值排序
    ucTR = sorted(ucTR.items(),key = lambda dic:dic[1],reverse = True)
    print ucTR[:10]
    return ucTR

# CalculateTFIDF(project_folder_path + "/InterestCandidate/",project_folder_path + "/InterestSetCandidate/")
def test():
    # # 生成所有用户的兴趣候选集标签
    getUsersInterestCandidate(twitter_data_folder_path)
    # 计算兴趣候选集的TFIDF
    CalculateTFIDF(project_folder_path + "/InterestCandidate/",project_folder_path + "/InterestSetCandidate/")
    TR = []
    for i in range(100):
        TR.append(1)
    InitTRMatrix = mat(TR)

    open_file = open(project_folder_path + "/TotalCandidateWithTFIDF.pickle","rb")
    uiCandidateWithTFIDF = pickle.load(open_file)
    open_file.close()
    print "TFIDF矩阵加载完毕."
    k1p1girl_candidate = FromFilegetUserInterestCandidate(project_folder_path + "/InterestCandidate/","realDonaldTrump")
    print "%s 用户候选集加载完毕" % "realDonaldTrump"
    print "开始计算该用户候选集"
    ucmatrix = CalucateWeight(k1p1girl_candidate)
    ucTRMatrix = CalucateTextRank(ucmatrix,0.000001,0.85,"realDonaldTrump",InitTRMatrix,uiCandidateWithTFIDF)
    CalucateUCTR(k1p1girl_candidate,ucTRMatrix)

test()