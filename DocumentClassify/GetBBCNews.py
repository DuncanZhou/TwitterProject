#!/usr/bin/python
#-*-coding:utf-8-*-
'''@author:duncan'''

import json
from bs4 import BeautifulSoup
import urllib2
import os
'''
由于CNN爬取的数据集用来分类效果不好,所以再尝试爬去BBC数据集,爬取9个分类中原BBC中没有的另外4个分类,分别是
Agriculture     Religion       Education       Military
每个分类准备需要500个文本,也就是需要500个有用的页面
通过搜索关键字搜索得到结果页,每页有10个链接,有可能有坏的链接,所以大约请求60个搜索页面,假设返回600个链接
在结果页面中取标题和新闻内容
'''
categories = ["Agriculture","Religion","Education","Military"]
# 搜索页面终止条件,返回的页面为空
# 搜索页面样例:http://www.bbc.co.uk/search/more?page=5&q=Religion&sa_f=search-product--suggest

News_DataSet_path = "/home/duncan/BBC_News_Crawl/"
# 生成各分类的搜索页面链接
def GenerateUrls():
    search_url = "http://www.bbc.co.uk/search/more?page=PAGE&q=CATEGORY&sa_f=search-product--suggest"
    category_urls = {}
    for category in categories:
        urls = []
        # 每个分类生成50个搜索页面
        for i in range(1,51):
            url = search_url.replace("PAGE",str(i)).replace("CATEGORY",category)
            urls.append(url)
        category_urls[category] = urls
    return category_urls

# 获取搜索页面中的结果页面链接
def GetPageUrls(url):
    html = urllib2.urlopen(url).read()
    soup = BeautifulSoup(html,"lxml")
    titles = soup.find_all("h1")
    urls = []
    # 定位到标题处
    for title in titles:
        href = title.find_all("a")
        for h in href:
            urls.append(h['href'])
    return urls

# 获取结果页面中的文本内容
def GetPageText(url):
    if "news" in url.split("/") == False:
        return None
    html = urllib2.urlopen(url).read()
    soup = BeautifulSoup(html,"lxml")
    # 定位到文章主内容区
    story_body = soup.find_all(attrs={"class":"story-body__inner"})
    text = ""
    for res in story_body:
        # 取p标签里的内容
        story = res.find_all("p")
        for s in story:
            if s.string != None:
                text += s.string + "\n"
    if text == "":
        return None
    print "已获取一个页面"
    return text

if __name__ == '__main__':
    # 生成搜索的urls
    Category_urls = GenerateUrls()
    print "搜索页链接生成成功"
    # 获取搜索页面的结果页面的链接
    Page_Text_urls = {}
    for category in categories:
        urls =  Category_urls[category]
        page_urls = []
        for url in urls:
            res = GetPageText(url)
            if res != None:
                page_urls += res
        # 每个分类对应的结果页面的链接
        Page_Text_urls[category] = page_urls
    print "结果页面链接生成成功"
    # 将结果页面的链接存储
    with open("BBC_Page_urls","w") as f:
        for category in categories:
            for url in Page_Text_urls[category]:
                f.write(url)
                f.write("\n")
            f.write("\n")
    # 开始获取文本
    for category in categories:
        # 如果不存在该分类的文件夹则创建该分类目录
        if os.path.exists(News_DataSet_path + category) == False:
            os.mkdir(News_DataSet_path + category)
        category_text_path = News_DataSet_path + category + "/"
        urls = Page_Text_urls[category]
        count = 1
        for url in urls:
            text = GetPageText(url)
            if text == None or text == "":
                continue
            with open(category_text_path + str(count),"w") as f:
                f.write(text)
                count += 1
        print "finished %s" % category