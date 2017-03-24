#!/usr/bin/python
import os
path = "/home/duncan/WikiData/"
categories = os.listdir(path)
for category in categories:
	with open(path + category,"r") as f:
		lines = f.readlines()
		count = 0
		fileid = 1
		for line in lines:
			text = ""
			text += line
			if count == 8:
				with open(path + category + str(fileid),"w") as f:
					f.write(text)
				text = ""
				count = 0
				fileid += 1
			count += 1


