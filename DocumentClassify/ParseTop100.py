from bs4 import BeautifulSoup

with open("/home/duncan/Top100","r") as f:
	html = f.read()
	soup = BeautifulSoup(html,"lxml")
	results = soup.find_all("td")
	famous = []
	count = 1
	user = []
	for res in results:
		if count == 6:
			famous.append(user)
			user = []
			user.append(res.string.encode('utf-8'))
			count = 1
		else:
			user.append(res.string.encode('utf-8'))
		count += 1
with open("top100","w") as f:
	for user in famous:
		f.writelines(user[0] + "\t"+ user[1] + "\t" + user[4])
		f.write("\n")
