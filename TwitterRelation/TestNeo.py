#!/usr/bin/python
#-*-coding:utf-8-*-
'''@author:duncan'''

from py2neo import Graph,Node,Relationship

# # 连接数据库
# test_graph = Graph("http://localhost:7474/db/data",username="neo4j",password="123")
graph = Graph()
# test_node_1 = Node(label = "User",name = "test_node_1")
# test_node_2 = Node(label = "User",name = "test_node_2")
#
# # 创建节点
# test_graph.create(test_node_1)
# test_graph.create(test_node_1)
#
# # 创建关系
# node_1_call_node2 = Relationship(test_node_1,"CALL",test_node_2)
# node_1_call_node2['count'] = 1
# node_2_call_node1 = Relationship(test_node_2,"CALL",test_node_1)
# node_2_call_node1['count'] = 2
# test_graph.create(node_1_call_node2)
# test_graph.create(node_2_call_node1)
#
# # 更新属性值
# node_1_call_node2['count'] += 1
# test_graph.push(node_1_call_node2)

# 查询
# find_node_1 = test_graph.find_one(label='User',property_key="name",property_value="test_node_1")
# print find_node_1


# print test_graph.cypher.execute("MATCH (p:User) WHERE p.name=%s RETURN p.name" % 'test_node_1')


# 通过节点/关系查找相关联的节点/关系
# find_relationship = test_graph.match_one(start_node=find_node_1,end_node=find_node_3,bidirectional=False)
# print find_relationship

