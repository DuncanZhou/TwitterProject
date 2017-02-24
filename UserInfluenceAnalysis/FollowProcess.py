#!/usr/bin/python
#-*-coding:utf-8-*-
'''@author:duncan'''

import os
import pickle

project_folder_path = os.path.abspath(".." + os.path.sep + "..")
following_path = project_folder_path + "/following/"
follower_path = project_folder_path + "/follower"
following_dic_path = project_folder_path + "/FollowingDic/"

def getPrefix(path):
    prefix = os.listdir(path)
    prefix = map(lambda fname:fname.replace(".txt",""),prefix)
    return prefix

def getFileID(prefix,filepath):
    with open(filepath,"r") as f:
        suffix = []
        lines = f.readlines()
        lineid = 1
        for line in lines:
            if lineid % 2 != 0:
                line = line[1:].replace("\r\n","")
                suffix.append(line)
            lineid += 1
    userIDs = map(lambda line:prefix + line,suffix)
    return userIDs

def ConstructFollowingDic(path):
    dic = {}
    # 构造字典,对应每个文件中对应的id号
    filename = getPrefix(path)
    for file in filename:
        userID = set(getFileID(file,path + file + '.txt'))
        dic[file] = userID
    # 将字典持久化
    save_file = open(following_dic_path + "followingdic.pickle","wb")
    pickle.dump(dic,save_file)
    save_file.close()
    return dic


def test():
    pass
test()