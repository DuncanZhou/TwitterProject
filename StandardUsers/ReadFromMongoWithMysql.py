#!/usr/bin/python
#-*-coding:utf-8-*-
'''@author:duncan'''

# 根据mysql-PreStandardUsers表中还没有分类的用户的userid在mongodb中读取他们的推文并存入文本中



import MySQLdb
from pymongo import MongoClient
import os
project_folder_path = os.path.abspath(".." + os.path.sep + "..")
# 导入另一个文件夹下的脚本
from sys import path
path.append(project_folder_path + "/TwitterProject/TwitterUsers/")
import TwitterUsers
tweets_folder = project_folder_path + "/PreStandardUsersTweets/"


# 读取用户userid
def getUsers(cursor):
    cursor.execute("SELECT * FROM PreStandardUsers WHERE category is null")
    data = cursor.fetchall()
    users = []
    for d in data:
        twitter_user = TwitterUsers.User(d[3],d[1],d[0],d[8],d[9],d[7],d[10],d[4],d[14])
        users.append(twitter_user)
    return users

# 读取用户的推文并存入文件中
def getTweetsByID(userid,search):
    tweets = []
    tweetsInfo = []
    result = search.find({"user_id":long(userid)})
    for res in result:
        tweetsInfo.append(res)
        tweets.append(res['text'])
    return tweets,tweetsInfo

# 根据id找screen_name
def getScreenName(id,users):
    for user in users:
        if user.id == id:
            return user.screen_name

# 从数据库中获取screen_name
def getSName(id,cursor):
    cursor.execute("SELECT screen_name from PreStandardUsers where userid = %s" % id)
    result = cursor.fetchall()
    for res in result:
        return res[0]
# 查询出来的信息转储到另一个表中
def Restore(tweets,search):
    for tweet in tweets:
        search.insert(tweet)
    print "insert"

if __name__ == "__main__":
    conn = MySQLdb.connect(
        host='localhost',
        port = 3306,
        user='root',
        passwd='123',
        db ='TwitterUserInfo',
    )
    cursor = conn.cursor()

    # connect to mongodb localhost
    client = MongoClient('127.0.0.1',27017)
    db = client.twitterForTestInflu

    users = getUsers(cursor)


    tweets2 = []
    tweets1 = []
    tweets3 = []
    NoTweetsID = []
    NoTweetsIDLast = []

    for user in users:
        if user.id[:2] == "12":
            tweets2.append(user.id)
        elif user.id[:2] == "11":
            tweets1.append(user.id)
        else:
            tweets3.append(user.id)

    for tweets in tweets2:
        tweet,tweetsInfo = getTweetsByID(tweets,db.tweets_12)
        # print type(tweetsInfo)
        if len(tweet) != 0:
            Restore(tweetsInfo,db.PreStandardUsers)
            # 写入文本中,以screen_name命名
            text = ""
            for t in tweet:
                text += t + "\n"
            filename = getScreenName(tweets,users)
            with open(tweets_folder + filename,'w') as f:
                f.write(text.encode("utf-8"))
        else:
            NoTweetsID.append(tweets)

    for tweets in tweets1:
        tweet,tweetsInfo = getTweetsByID(tweets,db.tweets_11)
        if len(tweet) != 0:
            Restore(tweetsInfo,db.PreStandardUsers)
            # 写入文本中,以screen_name命名
            text = ""
            for t in tweet:
                text += t + "\n"
            filename = getScreenName(tweets,users)
            with open(tweets_folder + filename,'w') as f:
                f.write(text.encode("utf-8"))
        else:
            NoTweetsID.append(tweets)

    for tweets in tweets3:
        tweet,tweetsInfo = getTweetsByID(tweets,db.tweets_10)
        if len(tweet) != 0:
            Restore(tweetsInfo,db.PreStandardUsers)
            # 写入文本中,以screen_name命名
            text = ""
            for t in tweet:
                text += t + "\n"
            filename = getScreenName(tweets,users)
            with open(tweets_folder + filename,'w') as f:
                f.write(text.encode("utf-8"))
        else:
            NoTweetsID.append(tweets)

    # 剩下来没找到的再在tweets集合中再找一遍
    for tweets in NoTweetsID:
        tweet,tweetsInfo = getTweetsByID(tweets,db.tweets)
        if len(tweet) != 0:
            Restore(tweetsInfo,db.PreStandardUsers)
            # 写入文本中,以screen_name命名
            text = ""
            for t in tweet:
                text += t + "\n"
            filename = getScreenName(tweets,users)
            with open(tweets_folder + filename,'w') as f:
                f.write(text)
        else:
            NoTweetsIDLast.append(tweets)

    print len(NoTweetsIDLast)
    with open("/home/duncan/toCrawl",'w') as f:
        for id in NoTweetsIDLast:
            f.write(id)
            f.write("\n")

    cursor.close()
    conn.commit()
    conn.close()

