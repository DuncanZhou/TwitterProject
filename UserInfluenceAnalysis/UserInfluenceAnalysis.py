#!/usr/bin/python
#-*-coding:utf-8-*-
'''@author:duncan'''

import MySQLdb
hostname = "localhost"
username = "root"
password = "123"
databasename = "TwitterUserInfo"

class User:
    'twitter用户对象'
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
            verify = "是"
        else:
            verify = "否"
        if self.location == "":
            location = "未填写"
        else:
            location = self.location

        return "用户id:%s  screen_name：%s  姓名:%s  是否认证:%s  地理位置:%s  粉丝数:%d  关注人数:%d  推文数:%d  点赞次数:%d" % (self.id,self.screen_name,self.name,verify,location,self.followers_count,self.friends_count,self.statuses_count,self.favourites_cout)

# 数据库相关操作函数
# 连接数据库操作
def Conn(hostname,username,password,databasename):
    db = MySQLdb.connect(hostname,username,password,databasename)
    return db

# 获取用户基本信息列表
def getUsersInfo():
    db = Conn(hostname,username,password,databasename)
    cursor = db.cursor()
    cursor.execute("SELECT * FROM EnUserInfo")
    data = cursor.fetchall()
    user = []
    for d in data:
        twitter_user = User(d[0],d[1],d[2],d[3],d[6],d[7],d[8],d[9],d[11])
        user.append(twitter_user)
    db.close()
    return user

# 根据用户id查找用户信息
def getUserInfo(id):
    db = Conn(hostname,username,password,databasename)
    cursor = db.cursor()
    cursor.execute("SELECT * FROM EnUserInfo where user_id = %s" % id)
    d = cursor.fetchall()
    twitter_user = User(d[0][0],d[0][1],d[0][2],d[0][3],d[0][6],d[0][7],d[0][8],d[0][9],d[0][11])
    return twitter_user

# 得到当前结果集总数
def getTotoalCount():
    db = Conn(hostname,username,password,databasename)
    cursor = db.cursor()
    cursor.execute("SELECT COUNT(*) FROM EnUserInfo")
    counts = cursor.fetchall()
    return counts[0][0]

# 用户相关操作
# 过滤掉推文数小于10的推特用户，返回用户id列表
def Filter(users):
    idRs = []
    userRs = []
    for user in users:
        if user.getUserStatuses_count() > 10:
            userRs.append(user)
    print "过滤后剩余结果数%d" % len(userRs)
    return userRs

# 得到认证过的用户列表
def getVerifiedUser(users):
    results = []
    for user in users:
        if user.getUserVerified() == 1:
            results.append(user.getUserId())
    return results

# 得到用户的粉丝列表
def getFollowers(user_id):
    pass

# 基于PageRank算法影响力排序
def PageRank(users):
    pass

if __name__ == '__main__':
    # print "原数据集数目:%d" % getTotoalCount()
    users = getUsersInfo()
    for user in users:
        print user

    # # 过滤后的用户id结果集
    # filterResult = Filter(users)
    # for rs in filterResult:
    #     print rs.getProportion()
    #
    # # 获取认证过的用户
    # # verifiedUserResult = getVerifiedUser(filterResult)
    # # print "认证过的用户数目为%d" % len(verifiedUserResult)


