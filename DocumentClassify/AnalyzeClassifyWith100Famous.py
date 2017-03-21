#!/usr/bin/python
#-*-coding:utf-8-*-
'''@author:duncan'''
import MySQLdb

import re

import time
import xlrd
import TweetsClassify
import TweetsClassifyTraining
import os
from nltk.corpus import stopwords
from nltk import word_tokenize

project_folder_path = os.path.abspath(".." + os.path.sep + "..")
Famous_tweets_path = project_folder_path + "/Famous_Tweets"
TestTweets_path = project_folder_path + "/TwitterProject/DocumentClassify/TestTweets/"
# hostname = "localhost"
# username = "root"
# password = "123"
# databasename = "TwitterUserInfo"

class Famous:
    def __init__(self,name,screen_name,category):
        self.name = name
        self.screen_name = screen_name
        self.category = category

    def __str__(self):
        return "姓名: %s   screen_name: %s   类别: %s" % (self.name,self.screen_name,self.category)
# 获取用户
def getUsers(cursor):
    users = []
    cursor.execute("SELECT * FROM 100Famous")
    data = cursor.fetchall()
    for d in data:
        user = Famous(d[0],d[1],d[2])
        users.append(user)
    return users

# Read users from xls file
def ReadFromXls():
    users = []
    data = xlrd.open_workbook('100Famous.xls')
    sheet = data.sheet_by_name('100Famous')
    rown = sheet.nrows
    for i in range(1,rown):
        user = []
        screen_name = sheet.cell(i,4).value
        if screen_name != "":
            name = sheet.cell(i,1).value.split("/")
            if len(name) > 1:
                name = name[1]
            else:
                name = name[0]
            category = sheet.cell(i,3).value
            user.append((name.encode("utf-8"),screen_name.encode("utf-8"),category.encode("utf-8")))
            users.append(user)
    return users

# write 100 famous users into db
def InsertIntodb(cursor,users):
    for user in users:
        # print user[0][0],user[0][1],user[0][2]
        cursor.execute("""INSERT INTO 100Famous(name,screen_name,category) VALUES("%s","%s","%s")""" % (user[0][0],user[0][1],user[0][2]))
    print "Insert Successfully"

# 使用除回复性其他推文作为输入
def GetClassifyResultsByAllTweets(tweets_path):

    '''
    :param tweets_path: 推文所在路径
    :return: 返回字典 格式:{screen_name:category}
    '''
    resdic = {}
    snames = os.listdir(tweets_path)
    for name in snames:
        text = ""
        with open(tweets_path + "/" + name,"r") as f:
            lines = f.readlines()
            for line in lines:
                # 移除回复性推文,看结果是否能提升
                if re.match(r"""^["|.]?@[\w|_]+""",line) == None:
                    text += line
            # text = f.read()
            res = TweetsClassify.Classify(text)
            # print "%s ==> %s" % (name,res)
            resdic[name] = res
    return resdic

# 使用推文前4000词频的词作为输入
def GetClassifyResultsByTF(tweets_path):
    twitter_stop_words = ["@","from","TO","to",":","!",".","#","https","RT","URL","in","&",";","re","''","?","thank","thanks","do","be","today","yesterday","tomorrow","night","tonight","day","year","last","oh","yeah"]
    resdic = {}
    snames = os.listdir(tweets_path)
    for name in snames:
        text = ""
        with open(tweets_path + "/" + name,"r") as f:
            starttime = time.time()
            text = f.read()
            re.sub(r"""\n@.+"""," ",text)
            words = word_tokenize(text.decode("utf-8"))
            # 判断是否是单词,去除停用词
            wordlist = [word for word in words if word.isalpha() and word not in (twitter_stop_words and stopwords.words("english"))]

            # 以下步骤统计词频
            wordset = set(wordlist)
            worddic = {}
            for word in wordset:
                worddic[word] = wordlist.count(word)
            worddic = sorted(worddic.items(),key=lambda dic:dic[1],reverse=True)
            lastwords = [word[0] for word in worddic[:4000]]

            # 合并成文本
            text = " ".join(lastwords)
            firsttime = time.time()
            print "处理推文花费 %f s" % (firsttime - starttime)
            res = TweetsClassify.Classify(text)
            secondtime = time.time()
            print "分类推文花费 %f s" % (secondtime - firsttime)
            # print "%s ==> %s" % (name,res)
            resdic[name] = res
    return resdic

if __name__ == '__main__':
    conn = MySQLdb.connect(
        host='localhost',
        port = 3306,
        user='root',
        passwd='123',
        db ='TwitterUserInfo',
    )
    cursor = conn.cursor()

    # # Read from xls file
    # users = ReadFromXls()
    # # Insert into db
    # InsertIntodb(cursor,users)

    # 获取所有名人
    users = getUsers(cursor)
    # for user in users:
    #     print user.category
    #------------------------------------------------选择训练集训练--------------------------------
    '''
    BCC分类：business/entertainment/politics/sport/technology
    CNN分类：agriculture/economy/education/entertainment/military/politics/religion/sports/technology

    DataSet1 是 CNN + BCC新闻数据集(分类融合起来)
    DataSet2 是 BCC新闻数据集
    DataSet3 是 CNN新闻数据集
    DataSet4 是 CNN + BCC新闻数据集(CNN填补BCC没有的分类)
    DataSet5 是 CNN新闻 + BCC新闻 + 推文数据集(融合)
    '''
    # 用名人推文来测试
    for i in range(1,6):
        data_set_path = "/DocumentClassify/DataSet%s" % (str(i))
        TweetsClassifyTraining.Training(data_set_path)

        #------------------------------------------------进行测试--------------------------------
        # 以去除回复性推文作为输入
        # resdic =  GetClassifyResultsByAllTweets(Famous_tweets_path)

        # 以词频单词作为输入
        resdic =  GetClassifyResultsByTF(Famous_tweets_path)

        # 将resdic分类结果写入文件
        with open("/home/duncan/DataSet%d-Results" % i,"w") as f:
            for key in resdic.keys():
                for user in users:
                    if user.screen_name == key:
                        f.write(user.name + "  ==>  " + "分类器分类结果: " + resdic[key] + "  ==>  " + "正确结果: " + user.category)
                        f.write("\n")
                        break
        #------------------------------------------------计算分类精度--------------------------------
        accuracy = TweetsClassify.Accuracy(resdic,users)
        print "使用DataSet%d分类结果:共%d个名人,分类准确率为%f" % (i,len(resdic),accuracy)
        print "-------------------------------------------------------------------------------------------"

    # 用和新闻推文来测试分类精度
    # for i in range(1,6):
    #     data_set_path = "/DocumentClassify/DataSet%s" % (str(i))
    #     TweetsClassifyTraining.Training(data_set_path)
    #
    #     #------------------------------------------------进行测试--------------------------------
    #     filenames = os.listdir(TestTweets_path)
    #     count = 0
    #     filesid = 0
    #     for dir in filenames:
    #         files = os.listdir(TestTweets_path + dir)
    #         for file in files:
    #             filesid += 1
    #             with open(TestTweets_path + dir + "/" + file,"r") as f:
    #                 text = f.read()
    #             res = TweetsClassify.Classify(text)
    #             if res == dir:
    #                 count += 1
    #     print "accuracy is %f" % (count * 1.0 / filesid)
    #     print "-------------------------------------------------------------------------------------------"

    # 关闭数据库连接
    cursor.close()
    conn.commit()
    conn.close()
