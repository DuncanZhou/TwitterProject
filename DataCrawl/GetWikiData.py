#!/usr/bin/python
# Example : "https://en.wikipedia.org/wiki/Agriculture"
import urllib2
from bs4 import BeautifulSoup

Example_url = "https://en.wikipedia.org/wiki/CATEGORY"
categories = ['Politics','Religion','Military','Education','Technology','Agriculture','Sports','Entertainment','Economy']

Military = ["Army","Navy","Air Force","War","Weapon"]
Agriculture = ['Crop','Agricultural engineering','land','soil','humus','grass','meadow','prairie','fallow','hacienda','countryside','farmer','settle','cowboy','shepherd','vintager','livestock','granary','pigpen','boar','clod','furrow']
Religion = ['Belief','sect','Christianty','Catholicism','Protestantism','Judaism','Islamism','Buddhism','Muslim','church', 'sermon','cathedral','clergy','pastor','pray','hymn','psalm','Bible','pilgrim']
Technology = ['artificial intelligence','biotechnology','bandwidth','bookmark','browser','cache memory','CPU','database','firewall','hacker','internet','LCD','robotics','touchscreen','VR']
Economy = ['IPO','major_economic_indicators','market capitalization','institutional shares','risk management','collateralised loans','bear sales','inflation','bubble economy','Engel coefficient','NASDAQ','supervisory board','bank','depositor','principal','overdraw','cash','check','surplus', 'devaluation', 'revaluation', 'stock', 'market capitalization']
Sports = ['Table tennis','Gymnastics', 'Running', 'Cycling', 'Skiing', 'Swimming', 'Fencing', 'Baseball', 'Volleyball', 'Football', 'Basketball', 'Diving', 'Polo', 'Water polo', 'Softball', 'Tennis', 'Badminton', 'Boxing', 'Toxophily', 'Judo', 'Rugby', 'Golf', 'Rings','Ice skating', 'Marathon', 'Sailing', 'Yacht', 'Rowing']
Politics = ['legislation', 'constitution', 'senate', 'federal system', 'congress', 'welfare', 'White House']
Education = ['primary education', 'educational history','diploma', 'tuition', 'fee-paying school', 'minor', 'scholarship', 'professor', 'lecturer', 'master', 'bachelor', 'graduate student', 'abroad student', 'undergraduate', 'university', 'high school', 'college', 'headmaster', 'teaching assistant', 'junior', 'senior', 'sophomore']

# get the data
def GetData(category):
	result = ""
	try:
		url = Example_url.replace("CATEGORY",category)
		html = urllib2.urlopen(url).read()
		soup = BeautifulSoup(html,'lxml')
		texts = soup.find_all('p')
		for text in texts:
			if text.get_text() != None:
				result += text.get_text() + "\n"
	except Exception as e:
		return None
	return result
if __name__ == '__main__':
	for category in Education:
		result = GetData(category)
		if result == None:
			continue
		with open("/home/duncan/WikiData/" + "Wiki-" + category,"w") as f:
			f.write(result.encode("utf-8"))

