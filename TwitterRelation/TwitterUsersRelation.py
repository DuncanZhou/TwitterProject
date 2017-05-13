#!/usr/bin/python
#-*-coding:utf-8-*-
'''@author:duncan'''


import sys
sys.path.append("..")
from Neo4jInteraction import TwitterWithNeo4j as neo4j

# 创建结点
def CreateNodes(path):
    '''

    :param path: CSV文件路径
    :return:
    '''
    neo4j.CreateNodesFromCSV(path)

if __name__ == '__main__':
    # csv文件需要放在默认import目录下
    CreateNodes("file:///users.csv")