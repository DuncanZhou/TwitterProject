#!/usr/bin/python
#-*-coding:utf-8-*-
'''@author:duncan'''

# 该脚本将TwitterUser基本信息写入CSV文本文件中

import csv
import sys
sys.path.append("..")
from MySQLInteraction import TwitterWithMysql as mysql

# 先从数据库中获取用户
def getUsers(table):
    '''

    :param table: 表名
    :return: 返回TwitterUser类对象的列表
    '''
    users = mysql.getUsersInfo(table)
    return users

def Write2CSV(users,path):
    '''
    :param users: 用户列表
    :param path:  写入文件路径
    '''
    with open(path,'wb') as csvfile:
        writer = csv.writer(csvfile)
        # 写入CSV文件的标题
        writer.writerow(['userid','screen_name','name','follwers_count','friends_count','favourites_count','location','verified','category'])
        twitter_users = []
        for user in users:
            temp = (user.id,user.screen_name,user.name,user.followers_count,user.friends_count,user.favourites_count,user.location,user.verified,user.category)
            twitter_users.append(temp)
        writer.writerows(twitter_users)
        csvfile.close()

if __name__ == '__main__':
    Write2CSV(getUsers('StandardUsers'),'/home/duncan/users.csv')



