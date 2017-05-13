#!/usr/bin/python
#-*-coding:utf-8-*-
'''@author:duncan'''

from neo4j.v1 import GraphDatabase,basic_auth

# 加载驱动
# 无加密方式
driver = GraphDatabase.driver("bolt://localhost:7687",auth=basic_auth("neo4j","123"))
# 加密方式
driver = GraphDatabase.driver("bolt://localhost:7687",auth=basic_auth("neo4j","123"),encrypted=True)

# 创建会话
session = driver.session()

# 查询并返回结果
result = session.run("MATCH (a:Person) WHERE a.name = 'Arthur' RETURN a.name AS name,a.title AS title")


for record in result:
    print ("%s%s" % (record['title'],record['name']))

# 运行事务
with session.begin_transaction() as tx:
    tx.run("MATCH (n:Person {name:'Duncan'}) DELETE n")
    tx.success = True

# 关闭会话
session.close()