#!/usr/bin/python
#-*-coding:utf-8-*-
'''@author:duncan'''
import MySQLdb
import xlrd
import TweetsClassify
import os

project_folder_path = os.path.abspath(".." + os.path.sep + "..")
Famous_tweets_path = project_folder_path + "/Famous_Tweets"
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

def GetClassifyResults(tweets_path):
    '''
    :param tweets_path: 推文所在路径
    :return: 返回字典 格式:{screen_name:category}
    '''
    resdic = {}
    snames = os.listdir(tweets_path)
    for name in snames:
        with open(tweets_path + "/" + name,"r") as f:
            text = f.read()
            res = TweetsClassify.Classify(text)
            print "%s ==> %s" % (name,res)
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
    resdic =  GetClassifyResults(Famous_tweets_path)
    # 计算正确率
    accuracy = TweetsClassify.Accuracy(resdic,users)
    print "共%d个名人,分类准确率为%f" % (len(resdic),accuracy)
    cursor.close()
    conn.commit()
    conn.close()
