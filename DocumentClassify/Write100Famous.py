#!/usr/bin/python
import xlrd
import xlwt
xlsfile = xlwt.Workbook()
sheet = xlsfile.add_sheet('100Famous')
with open("/home/duncan/top100","r") as f:
	lines = f.readlines()
	for row,line in zip(range(0,len(lines)),lines):
		values = line.split("\t")
		for col in range(len(values)):
			value = values[col].replace("\n","")
			sheet.write(row,col,value.decode("utf-8"))
xlsfile.save("/home/duncan/100Famous.xls")
print "Done"