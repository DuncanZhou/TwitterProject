#!/usr/bin/python
#-*-coding:utf-8-*-
'''@author:duncan'''
import time
import json
from bs4 import BeautifulSoup
import urllib2
import os
import re
# test religion
class CNNNewsSpider():
    name = "CNNNewsSpider"
    allowed_domains = ["edition.cnn.com"]
    categories = ["politics","religion","economy","military","education","technology","sports","entertainment","agriculture","money"]
    url_prefix = "http://edition.cnn.com"

    def generateAddress(self,page,start,category):
        search_address = "http://searchapp.cnn.com/search/query.jsp?page=%d&npp=10start=%d&text=%s&type=all&bucket=true&sort=relevance" % (page,start,category)
        return search_address

    # get the urls about every category
    def generatePageUrls(self):
        category = {}
        for ca in self.categories:
            # every category with 1000 pages i.e. every category has 10000 text
            caAddress = []
            # i from 1 to 1000
            for i in range(1,1001):
                url = self.generateAddress(i,(10 * (i - 1) + 1),ca)
                caAddress.append(url)
            category[ca] = caAddress
        return category

    # get urls in one page
    def getOnePageURLs(self,url):
        urls = []
        html = urllib2.urlopen(url).read()
        soup = BeautifulSoup(html,"lxml")
        # headline = sel.xpath("//h3[@class='cd__headline']")
        originjson = soup.find_all("textarea")[0].string
        originjson = originjson.lstrip()
        originjson = originjson.rstrip()
        jsondata = json.loads(originjson.encode('utf-8'))
        results = jsondata["results"]
        for data in results[0]:
            if re.match(r"^http",data["url"]) == None:
                url = self.url_prefix + data["url"]
            else:
                url = data["url"]
            urls.append(url)
        return urls

    # get text url in every category
    def generateCategoryUrls(self,pageurl):
        categoryUrl = {}
        for ca in self.categories:
            id = 0
            urls = []
            # pageurls is a list-type
            pageurls = pageurl[ca]
            for url in pageurls:
                try:
                    texturls = self.getOnePageURLs(url)
                    urls += texturls
                except Exception as e:
                    pass
                id += 1
                print "process %d urls" % id
            categoryUrl[ca] = urls
            urls_path = "/home/duncan/CNNNewsDataSet/"
            # 把获取得到的文本页面链接存入
            with open(urls_path + ca + "texturls","wb") as f:
                for url in urls:
                    f.write(url)
                    f.write("\n")
            print "finished category urls %s" % ca
        return categoryUrl

    # get the text in one page
    def getText(self,url):
        text = ""
        # 只抓取以html结尾的网页
        if len(re.findall(r".html$",url)) == 0:
            return text
        try:
            html = urllib2.urlopen(url).read()
            soup = BeautifulSoup(html,"lxml")
            result = soup.find_all(attrs={"class":"zn-body__paragraph"})
            for res in result:
                if res.string != None:
                    text += res.string
        except Exception as e:
            pass
        return text

    # categoryUrl is a dictionary-type
    def DownloadText(self,categoryUrl):
        for category in categoryUrl.keys():
            # 创建类别的文本文件夹
            if os.path.exists("/home/duncan/CNNNewsDataSet/" + category + "Text") == False:
                os.mkdir("/home/duncan/CNNNewsDataSet/" + category + "Text")
            categoryText_foler_path = "/home/duncan/CNNNewsDataSet/" + category + "Text/"
            texturls = categoryUrl[category]
            id = 1
            for url in texturls:
                text = self.getText(url)
                if text != "":
                    # 写入文件
                    with open(categoryText_foler_path + str(id),"w") as f:
                        f.write(text.encode("utf-8"))
                    id += 1
            print "finished fetching %s category text" % category

    # 从一个url中下载文本
    def DownloadOnePageText(self,url):
        text = ""
        try:
            text = self.getText(url)
        except Exception as e:
            pass
        return text

if __name__ == '__main__':
    starttime = time.time()
    spider = CNNNewsSpider()
    # pageurl = spider.generatePageUrls()
    # categoryUrl = spider.generateCategoryUrls(pageurl)
    # spider.DownloadText(categoryUrl)

    # test getting text
    with open("/home/duncan/CNNNewsDataSet/religiontexturls","r") as f:
        urls = f.readlines()
        id = 1
        for url in urls:
            text = spider.DownloadOnePageText(url)
            if text == "":
                continue
            # 写入文件
            with open("/home/duncan/CNNNewsDataSet/religionText/" + str(id),"w") as f:
                f.write(text.encode("utf-8"))
            id += 1
            print "已写入%d个文本" % id
    endtime = time.time()
    print "cost %f s" % (endtime - starttime)




