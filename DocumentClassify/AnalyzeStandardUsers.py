#!/usr/bin/python
#-*-coding:utf-8-*-
'''@author:duncan'''
import MySQLdb
import pymongo
from pymongo import MongoClient
import re

import time
import xlrd
import TweetsClassify
import TweetsClassifyTraining
import os
import sys
from nltk.corpus import stopwords
from nltk import word_tokenize

project_folder_path = os.path.abspath(".." + os.path.sep + "..")
Famous_tweets_path = project_folder_path + "/Famous_Tweets"
TestTweets_path = project_folder_path + "/TwitterProject/DocumentClassify/TestTweets/"

# 导入另一个文件夹下的脚本
from sys import path
path.append(project_folder_path + "/TwitterProject/TwitterUsers/")
import TwitterUsers

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
def getStandardUsers(cursor):
    users = []
    cursor.execute("SELECT * FROM StandardUsers")
    data = cursor.fetchall()
    for d in data:
        user = TwitterUsers.User(d[3],d[1],d[0],d[4],d[7],d[9],d[8],d[10],d[14])
        user.setCategory(d[2])
        users.append(user)
    return users


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

# 并不是把推文全部作为输入,在去除推文中停用词并将所有单词作为输入
def GetClassifyResultsByTF(users_id,tweet_mongo):
    twitter_stop_words = ["@","from","TO","to",":","!",".","#","https","RT","URL","in","&",";","re","''","?","thank","thanks","do","be","today","yesterday","tomorrow","night","tonight","day","year","last","oh","yeah"]

    # 返回四种分类器的结果
    Classifiers = ['MultinomialNB','LinearSVM','RandomForest','SGD','ExtraTree']
    weight = [0.4,0.3,0.1,0.1,0.1]
    results = []
    multiclassifier_result = {}
    MultinomialNB_resdic = {}
    # LinearSVM_resdic = {}
    # RandomForest_resdic = {}
    # SGD_resdic = {}
    # ExtraTree_resdic = {}

    # 从mongodb中根据user_id读取推文
    for id in users_id:
        tweets = tweet_mongo.find({'user_id':long(id)})
        text = ""
        # 获取该用户所有推文,并处理
        for tweet in tweets:
            text += tweet['text']
        # 删除推文中@的人
        re.sub(r"""\n@.+"""," ",text)
        # words = word_tokenize(text.decode("utf-8"))
        words = word_tokenize(text)
        # 判断是否是单词,去除停用词
        wordlist = [word for word in words if word.isalpha() and word not in (twitter_stop_words and stopwords.words("english"))]

        # 以下步骤统计词频,由于统计词频效果不好,故舍弃
        # wordset = set(wordlist)
        # worddic = {}
        # for word in wordset:
        #     worddic[word] = wordlist.count(word)
        # worddic = sorted(worddic.items(),key=lambda dic:dic[1],reverse=True)
        # lastwords = [word[0] for word in worddic[:4000]]

        # 合并成文本
        # text = " ".join(lastwords)
        text = " ".join(wordlist)


        # 单模型
        MultinomialNB_res = TweetsClassify.Classify(text,"MultinomialNB")
    #     LinearSVM_res = TweetsClassify.Classify(text,"LinearSVM")
    #     RandomForest_res = TweetsClassify.Classify(text,"RandomForest")
    #     SGD_res = TweetsClassify.Classify(text,"SGD")
    #     ExtraTree_res = TweetsClassify.Classify(text,"ExtraTree")
    #
        MultinomialNB_resdic[id] = MultinomialNB_res
    #     LinearSVM_resdic[id] = LinearSVM_res
    #     RandomForest_resdic[id] = RandomForest_res
    #     SGD_resdic[id] = SGD_res
    #     ExtraTree_resdic[id] = ExtraTree_res
    # results.append(MultinomialNB_resdic)
    # results.append(LinearSVM_resdic)
    # results.append(RandomForest_resdic)
    # results.append(SGD_resdic)
    # results.append(ExtraTree_resdic)

        # 多模型融合
        result = TweetsClassify.Classify_MultiModels(text,Classifiers,weight)
        multiclassifier_result[id] = result
    return multiclassifier_result,MultinomialNB_resdic

# 从mysql中查询用户的分类形成字典返回
def GetCategoryById(users_id,cursor):
    category_dic = {}
    for id in users_id:
        cursor.execute("select category from StandardUsers where userid = '%s'" % id)
        data = cursor.fetchall()
        category = data[0][0]
        category_dic[id] = category
    return category_dic

if __name__ == '__main__':

    # 分类器类型
    Classifiers = ['MultinomialNB','LinearSVM','RandomForest','SGD','ExtraTree']
    start = time.time()
    conn = MySQLdb.connect(
        host='localhost',
        port = 3306,
        user='root',
        passwd='123',
        db ='TwitterUserInfo',
    )
    cursor = conn.cursor()

    # 配置Mongodb查询
    client = MongoClient('127.0.0.1',27017)
    db = client.twitterForTestInflu
    tweet = db.PreStandardUsers

    # # Read from xls file
    # users = ReadFromXls()
    # # Insert into db
    # InsertIntodb(cursor,users)

    # 获取所有名人
    # users = getUsers(cursor)

    # 获取标准人物样本库中的用户
    StandardUsers = getStandardUsers(cursor)
    # 将用户的id保存


    StandardUsers_id = []
    no_tweets_id = []
    # i = 0
    for user in StandardUsers:
        StandardUsers_id.append(user.id)
        # tweets = tweet.find({'user_id':long(user.id)})
    #     i += 1
    #     print i
    #     text = ""
    #     for t in tweets:
    #         text += t['text']
    # print no_tweets_id
    # sys.exit(0)

#------------------------------------------------选择训练集训练--------------------------------
    '''
    BCC分类：business/entertainment/politics/sport/technology
    CNN分类：agriculture/economy/education/entertainment/military/politics/religion/sports/technology

    DataSet1 是 CNN + BCC新闻数据集(分类融合起来)
    DataSet2 是 BCC新闻数据集(加了维基词条的一些文章,加了CNN的一些文本,结果有提升)
    DataSet3 是 CNN新闻数据集
    DataSet4 是 CNN + BCC新闻数据集(CNN填补BCC没有的分类)
    DataSet5 是 CNN新闻 + BCC新闻 + 推文数据集(融合)
    '''
    # 用名人推文来测试
    # for i in range(1,6):
    #     data_set_path = "/DocumentClassify/DataSet%s" % (str(i))
    #     TweetsClassifyTraining.Training(data_set_path)
    #
    #     #------------------------------------------------进行测试--------------------------------
    #     # 以去除回复性推文作为输入
    #     # resdic =  GetClassifyResultsByAllTweets(Famous_tweets_path)
    #
    #     # 以词频单词作为输入
    #     resdic =  GetClassifyResultsByTF(Famous_tweets_path)
    #
    #     # 将resdic分类结果写入文件
    #     with open("/home/duncan/DataSet%d-Results" % i,"w") as f:
    #         for key in resdic.keys():
    #             for user in users:
    #                 if user.screen_name == key:
    #                     f.write(user.name + "  ==>  " + "分类器分类结果: " + resdic[key] + "  ==>  " + "正确结果: " + user.category)
    #                     f.write("\n")
    #                     break
    #     #------------------------------------------------计算分类精度--------------------------------
    #     accuracy = TweetsClassify.Accuracy(resdic,users)
    #     print "使用DataSet%d分类结果:共%d个名人,分类准确率为%f" % (i,len(resdic),accuracy)
    #     print "-------------------------------------------------------------------------------------------"
    data_set_path = "/DocumentClassify/DataSet2"
    # 已经训练好了模型则不需要再训练
    TweetsClassifyTraining.Training(data_set_path)

    #------------------------------------------------进行测试--------------------------------
    # 以去除回复性推文作为输入
    # resdic =  GetClassifyResultsByAllTweets(Famous_tweets_path)

    # 以词频单词作为输入
    print "----------------------------开始分类------------------------------------------------"

    # -------------------------------------------------------------------------------------------------
    # 获取用户的类别
    category_dic = GetCategoryById(StandardUsers_id,cursor)

    # # 单模型
    # results = GetClassifyResultsByTF(StandardUsers_id,tweet)
    #
    # # 将resdic分类结果写入文件
    # for (res,classifier) in zip(results,Classifiers):
    #     # res是每个分类器的结果字典
    #     with open("/home/duncan/%s-Results" % classifier,"w") as f:
    #         for key in res.keys():
    #             for user in StandardUsers:
    #                 if user.id == key:
    #                     f.write(user.id + "  ==>  " + "分类器分类结果: " + res[key] + "  ==>  " + "正确结果: " + user.category)
    #                     f.write("\n")
    #                     break
    # #------------------------------------------------计算分类精度--------------------------------
    #     accuracy = TweetsClassify.Accuracy(res,category_dic)
    #     print "分类结果:%s分类器:共%d个名人,分类准确率为%f" % (classifier,len(res),accuracy)
    # ---------------------------------------------------------------------------------------------------------

    # 多模型融合分类
    # ---------------------------------------------------------------------------------------------------------
    MultiModels_results,Multinomial_results = GetClassifyResultsByTF(StandardUsers_id,tweet)

    # 将多项式分类器分类结果写入文件
    with open("/home/duncan/Multinomial_NB_Classifier-results",'w') as f:
        for key in Multinomial_results.keys():
            for user in StandardUsers:
                if user.id == key:
                    f.write(user.id + "  ==>  " + "分类器分类结果: " + Multinomial_results[key] + "  ==>  " + "正确结果: " + user.category)
                    f.write("\n")
                    break
    accuracy = TweetsClassify.Accuracy(Multinomial_results,category_dic)
    print "分类结果:多项式贝叶斯分类器:共%d个名人,分类准确率为%f" % (len(Multinomial_results),accuracy)

    # 多分类器融合结果写入文件
    with open("/home/duncan/MultiClassifier-results",'w') as f:
        for key in MultiModels_results.keys():
            for user in StandardUsers:
                if user.id == key:
                    f.write(user.id + "  ==>  " + "分类器分类结果: " + MultiModels_results[key] + "  ==>  " + "正确结果: " + user.category)
                    f.write("\n")
                    break
    accuracy = TweetsClassify.Accuracy(MultiModels_results,category_dic)
    print "分类结果:分类器融合:共%d个名人,分类准确率为%f" % (len(MultiModels_results),accuracy)
    # ---------------------------------------------------------------------------------------------------------
    print "-------------------------------------------------------------------------------------------"

    # accuracy = TweetsClassify.Accuracy(BernoulliNB_resdic,users)
    # print "使用DataSet%d分类结果,伯努力贝叶斯分类器:共%d个名人,分类准确率为%f" % (2,len(BernoulliNB_resdic),accuracy)
    # print "-------------------------------------------------------------------------------------------"
    #
    # accuracy = TweetsClassify.Accuracy(LinearSVM_resdic,users)
    # print "使用DataSet%d分类结果,线性SVM分类器:共%d个名人,分类准确率为%f" % (2,len(LinearSVM_resdic),accuracy)
    # print "-------------------------------------------------------------------------------------------"
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
    end = time.time()
    print "共用时%fs" % (end - start)
