#!/usr/bin/python
#-*-coding:utf-8-*-
'''@author:duncan'''

import xml.dom.minidom

# 生成XML文件
def GenerateXml():
    # 获取DOM树实现对象
    impl = xml.dom.minidom.getDOMImplementation()
    # 创建DOM树,'TwitterUsers'为根节点名称
    dom = impl.createDocument(None,'TwitterUsers',None)
    root = dom.documentElement

    # 创建子节点
    user = dom.createElement('user1')
    root.appendChild(user)

    # 姓名节点标签
    nameE = dom.createElement('name')
    # 标签增加属性
    nameE.setAttribute("coding","utf-8")

    # 姓名标签内容
    nameT = dom.createTextNode('Luhaha')
    # 将内容加入标签中
    nameE.appendChild(nameT)

    # 把标签加入到子节点中
    user.appendChild(nameE)

    with open('/home/duncan/XML-Test.xml','w') as f:
        dom.writexml(f,addindent=" ",newl='\n')

if __name__ == '__main__':
    GenerateXml()

