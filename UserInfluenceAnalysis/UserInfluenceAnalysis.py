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
    def __init__(self,id,name,followers_count,friends_count,statuses_count,favourites_count,location,verified):
        self._id = id
        self._name = name
        self._followers_count = followers_count
        self._friends_count = friends_count
        self._statuses_count = statuses_count
        self._favourites_cout = favourites_count
        self._location = location
        self._verified = verified

    def getProportion(self):
        if self._friends_count != 0:
            return (self._followers_count) * 1.0 / self._friends_count
        else:
            return (self._followers_count) * 1.0 / 0.1

    def setCountAttr(self,followers_count,friends_count):
        self._friends_count = friends_count
        self._followers_count = followers_count

    def getUserName(self):
        return self._name

    def getUserStatuses_count(self):
        return self._statuses_count

    def getUserId(self):
        return self._id

    def getUserVerified(self):
        return self._verified

    def __str__(self):
        if self._verified == 1:
            verify = "是"
        else:
            verify = "否"
        if self._location is None:
            location = "未填写"
        else:
            location = self._location

        return "用户id:%s,姓名:%s,是否认证:%s,地理位置:%s,粉丝数:%d,关注人数:%d,推文数:%d,点赞次数:%d" % (self._id,self._name,verify,location,self._followers_count,self._friends_count,self._statuses_count,self._favourites_cout)

# 数据库相关操作函数
# 连接数据库操作
def Conn(hostname,username,password,databasename):
    db = MySQLdb.connect(hostname,username,password,databasename)
    return db

# 获取用户基本信息列表
def setUserInfo():
    db = Conn(hostname,username,password,databasename)
    cursor = db.cursor()
    cursor.execute("SELECT * FROM user_5")
    data = cursor.fetchall()
    user = []
    for d in data:
        twitter_user = User(d[0],d[1],d[8],d[7],d[6],d[9],d[3],d[13])
        user.append(twitter_user)
    db.close()
    return user

# 根据用户id查找用户信息
def getUserInfo(id):
    db = Conn(hostname,username,password,databasename)
    cursor = db.cursor()
    cursor.execute("SELECT * FROM user_5 where user_id = %s" % id)
    d = cursor.fetchall()
    twitter_user = User(d[0][0],d[0][1],d[0][8],d[0][7],d[0][6],d[0][9],d[0][3],d[0][13])
    return twitter_user

# 得到当前结果集总数
def getTotoalCount():
    db = Conn(hostname,username,password,databasename)
    cursor = db.cursor()
    cursor.execute("SELECT COUNT(*) FROM user_5")
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


if __name__ == '__main__':
    print "原数据集数目:%d" % getTotoalCount()
    users = setUserInfo()

    # 过滤后的用户id结果集
    filterResult = Filter(users)
    for rs in filterResult:
        print rs.getProportion()

    # 获取认证过的用户
    # verifiedUserResult = getVerifiedUser(filterResult)
    # print "认证过的用户数目为%d" % len(verifiedUserResult)


