# test python & mongodb

import pymongo
from pymongo import MongoClient
import MySQLdb
import time
import re
import math

class User:
    def __init__(self,id,screen_name,name,location,statuses_count,friends_count,followers_count,favourites_count,verified):
        self.id = id
        self.screen_name = screen_name
        self.name = name
        self.followers_count = followers_count
        self.friends_count = friends_count
        self.statuses_count = statuses_count
        self.favourites_cout = favourites_count
        self.location = location
        self.verified = verified

    def getProportion(self):
        if self.friends_count != 0:
            return (self.followers_count) * 1.0 / self.friends_count
        else:
            return (self.followers_count) * 1.0 / 0.1

    def __str__(self):
        if self.verified == 1:
            verify = "yes"
        else:
            verify = "no"
        if self.location == "":
            location = "no file"
        else:
            location = self.location

        return "user id:%s  screen_name:%s  name:%s  verified:%s  location:%s  followers:%d  followings:%d  tweets:%d  favourites:%d" % (self.id,self.screen_name,self.name,verify,location,self.followers_count,self.friends_count,self.statuses_count,self.favourites_cout)

def getUsersInfo(cursor):
    # db = Conn(hostname,username,password,databasename)
    # cursor = db.cursor()
    cursor.execute("SELECT * FROM UsersForInfluence")
    data = cursor.fetchall()
    user = []
    for d in data:
        twitter_user = User(d[0],d[1],d[2],d[3],d[6],d[7],d[8],d[9],d[11])
        user.append(twitter_user)
    return user

def getUserInfo(id,cursor):
    cursor.execute("SELECT * FROM UsersForInfluence where user_id = %s" % id)
    d = cursor.fetchall()
    twitter_user = User(d[0][0],d[0][1],d[0][2],d[0][3],d[0][6],d[0][7],d[0][8],d[0][9],d[0][11])
    return twitter_user

def getUserTweets(userid,Search):
    tweets = []
    result = Search.find({"user_id":long(userid)})
    for res in result:
        tweets.append(res["text"])
    return tweets

# split Origin and RT
def CalucateParameters(tweets):
    OTN = RTN = RTrtN = ORTN = OFavN = RTFavN = 0
    for tweet in tweets:
        if re.match(r"^RT @[\w|\d|_]+",tweet["text"]) != None:
            RTN += 1
            RTrtN += tweet["retweet_count"]
            RTFavN += tweet["favorite_count"]
        else:
            OTN += 1
            ORTN += tweet["retweet_count"]
            OFavN += tweet["favorite_count"]
    # OriginNumber RTNumber
    return OTN,RTN,ORTN,RTrtN,OFavN,RTFavN

# active
def CalucateActive(user,OriginN,RTN):
    d_active = 0.5 * math.log(OriginN + 1,math.e) + 0.3 * math.log(RTN + 1,math.e) + 0.2 * math.log(user.followers_count + 1,math.e)
    return d_active

# Influence
def CalucateInfluence(ORTN,OFavN,RTN,RTFavN):
    return 0.4 * math.log(ORTN + 1,math.e) + 0.2 * math.log(OFavN + 1,math.e) + 0.2 * math.log(RTN + 1,math.e) + 0.2 * math.log(RTFavN + 1,math.e)

# twitter Influence
def CalucateTwitterInfluence(d_active,d_twitter):
    return 0.2 * d_active + 0.8 * d_twitter

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
    users = getUsersInfo(cursor)
    userid = []

    # define the name of database
    db = client.twitterForTestInflu
    tweets1 = db.tweets_10
    tweets2 = db.tweets_11
    tweets3 = db.tweets_12
    tweets = [tweets1,tweets2,tweets3]
    user_influ = {}

    for user in users:
        if user.id[:2] == "11":
            tweet = tweets2
        elif user.id[:2] == "12":
            tweet = tweets3
        else:
            tweet = tweets1
        if tweet.find({"user_id":long(user.id)}).count() > 0:
            userid.append(user.id)
    count = 0
    for id in userid:
        if id[:2] == "11":
            result = tweets2.find({"user_id":long(id)})
        elif id[:2] == "12":
            result = tweets3.find({"user_id":long(id)})
        else:
            result = tweets1.find({"user_id":long(id)})
        user = getUserInfo(id,cursor)
        OTN,RTN,ORTN,RTrtN,OFavN,RTFavN = CalucateParameters(result)
        user_influ[id] = CalucateTwitterInfluence(CalucateActive(user,OTN,RTN),CalucateInfluence(ORTN,OFavN,RTrtN,RTFavN))
        count += 1
        print count
    user_influ = sorted(user_influ.items(),key=lambda dic:dic[1],reverse=True)
    print user_influ[:10]
    cursor.close()
    conn.commit()
    conn.close()