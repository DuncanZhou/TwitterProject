#!/usr/bin/python
#-*-coding:utf-8-*-
'''@author:duncan'''

# 该脚本为与neo4j交互层


from neo4j.v1 import GraphDatabase,basic_auth





def Conn():
    # 加载驱动
    # 加密方式
    driver = GraphDatabase.driver("bolt://localhost:7687",auth=basic_auth("neo4j","123"),encrypted=True)
    # 创建会话
    session = driver.session()
    return driver,session

def Close(session,driver):
    session.close()
    driver.close()

def CreateNodesFromCSV(path):
    '''
    :param path: CSV文件路径
    :return:
    '''
    driver,session = Conn()
    # 从CSV文件中创建结点
    statement = "LOAD CSV WITH HEADERS FROM '%s' AS line\
    CREATE (:TwitterUser { name:line.userid,userid: line.userid, screen_name:line.screen_name,followers_count:toInt(line.followers_count),friends_count:toInt(line.friends_count),favourites_count:line.favourites_count,location:line.location,verified:toInt(line.verified),category:line.category})" % path
    # # 利用事务运行query
    with session.begin_transaction() as tx:
        tx.run(statement)
        tx.success = True
    # session.run(statement)
    Close(session,driver)
