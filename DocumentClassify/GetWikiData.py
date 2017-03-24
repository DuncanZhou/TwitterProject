#!/usr/bin/python
# Example : "https://en.wikipedia.org/wiki/Agriculture"
import urllib2
from bs4 import BeautifulSoup

Example_url = "https://en.wikipedia.org/wiki/CATEGORY"
categories = ['Politics','Religion','Military','Education','Technology','Agriculture','Sports','Entertainment','Economy']
Military = ["Army","Navy","Air Force","War","Weapon"]
Agriculture = ['Crop','Agricultural engineering','land','soil','humus','grass','meadow','prairie','fallow','hacienda','countryside','farmer','settle','cowboy','shepherd','vintager','livestock','granary','pigpen','boar','clod','furrow']
Religion = ['Belief','sect','Christianty','Catholicism','Protestantism','Judaism','Islamism','Buddhism','Muslim','church', 'sermon','cathedral','clergy','pastor','pray','hymn','psalm','Bible','pilgrim']

# get the data
def GetData(category):
	result = ""
	url = Example_url.replace("CATEGORY",category)
	html = urllib2.urlopen(url).read()
	soup = BeautifulSoup(html,'lxml')
	texts = soup.find_all('p')
	for text in texts:
		if text.get_text() != None:
			result += text.get_text() + "\n"
	return result
if __name__ == '__main__':
	for category in Religion:
		result = GetData(category)
		with open("/home/duncan/WikiData/" + "Wiki-" + category,"w") as f:
			f.write(result.encode("utf-8"))

