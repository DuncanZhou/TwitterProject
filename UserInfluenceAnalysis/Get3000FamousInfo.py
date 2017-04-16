#!/usr/bin/python
#-*-coding:utf-8-*-
'''@author:duncan'''

import MySQLdb
import os
project_folder_path = os.path.abspath(".." + os.path.sep + "..")
from sys import path
path.append(project_folder_path + "/TwitterProject/TwitterUsers/")
import TwitterUsers
from xlwt import *

# 获取用户信息
def getUserInfo(id,cursor):
    cursor.execute("SELECT * FROM PreStandardUsers where userid = %s" % id)
    d = cursor.fetchall()
    twitter_user = TwitterUsers.User(d[0][3],d[0][1],d[0][0],d[0][4],d[0][7],d[0][9],d[0][8],d[0][10],d[0][14])
    return twitter_user

# 读出3000个人
def Read3000Famous(path,cursor):
    users = []
    with open("/home/duncan/3000Famous","r") as f:
        lines = f.readlines()
        for line in lines:
            users.append(getUserInfo(line,cursor))
    return users

# 将3000个名人写入excel表中
def Write2Excel(users):
    # 创建一个工作溥
    w = Workbook()
    # 创建一个表
    wsheet = w.add_sheet("待分类人物")
    # 第一行写入标题
    wsheet.write(0,0,"id")
    wsheet.write(0,1,"screen_name")
    wsheet.write(0,2,"name")
    wsheet.write(0,3,"粉丝数")
    wsheet.write(0,4,"好友人数")
    wsheet.write(0,5,"推文数")
    wsheet.write(0,6,"点赞次数")
    wsheet.write(0,7,"地理位置")
    wsheet.write(0,8,"是否认证")
    wsheet.write(0,9,"类别")
    row = 1
    for user in users:
        wsheet.write(row,0,user.id)
        wsheet.write(row,1,user.screen_name)
        wsheet.write(row,2,user.name)
        wsheet.write(row,3,user.followers_count)
        wsheet.write(row,4,user.friends_count)
        wsheet.write(row,5,user.statuses_count)
        wsheet.write(row,6,user.favourites_count)
        wsheet.write(row,7,user.location)
        wsheet.write(row,8,user.verified)
        row += 1