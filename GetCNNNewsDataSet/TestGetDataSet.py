#!/usr/bin/python
#-*-coding:utf-8-*-
'''@author:duncan'''
import json
from bs4 import BeautifulSoup
import urllib2
# test religion
class CNNNewsSpider():
    name = "CNNNewsSpider"
    allowed_domains = ["edition.cnn.com"]
    categories = ["politics","religion","economy","military","education","technology","sports","entertainment","agriculture","money"]
    start_urls = []
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
            for i in range(1,3):
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
            url = self.url_prefix + data["url"]
            urls.append(url)
        return urls

    # get text url in every category
    def generateCategoryUrls(self,pageurl):
        categoryUrl = {}
        for ca in self.categories:
            urls = []
            # pageurls is a list-type
            pageurls = pageurl[ca]
            for url in pageurls:
                try:
                    texturls = self.getOnePageURLs(url)
                    urls += texturls
                except Exception as e:
                    pass
            categoryUrl[ca] = urls
            print "finished category %s" % ca

        with open("category-urls","wb") as f:
            for key in categoryUrl.keys():
                print len(categoryUrl[key])
                f.write(key)
                f.write("\t")
                for url in categoryUrl[key]:
                    if url != None:
                        f.write(url) + f.write("\t")
        return categoryUrl

    # get the text in one page
    def getText(self,url):
        text = ""
        html = urllib2.urlopen(url).read()
        soup = BeautifulSoup(html,"lxml")
        result = soup.find_all(attrs={"class":"zn-body__paragraph"})
        for res in result:
            text += res.string
        return text

if __name__ == '__main__':
    spider = CNNNewsSpider()
    pageurl = spider.generatePageUrls()
    # print pageurl
    spider.generateCategoryUrls(pageurl)
# spider.getOnePageURLs("http://searchapp.cnn.com/search/query.jsp?page=3&npp=10start=21&text=health&type=all&bucket=true&sort=relevance")



