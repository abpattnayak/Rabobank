# coding=utf-8
import re
import datetime
from scrapy import log

def ing_scraper(productName, selector, validSinceDate):
	#tables
	tables =  selector.xpath('//table[@class="table table-b table-lr-unpadded l-mb-0"]/tbody')

	now = datetime.datetime.now()
        
	f = open("output.csv", "a+")
        
	for i in range(0,2): #tables
		rows = tables[i].xpath("tr")
		headers = tables[i].xpath("tr/td/strong/text()").extract()
		for j in range(1,len(rows)):
			datas = rows[j].xpath("td/text()").extract()
			for k in range(1, len(datas)):
				#Country Code, Provider Name
				f.write("NL;ING;")
				#Product Name
				f.write("ING")
				f.write(productName)
				f.write(";")
				#Loan Type
				f.write(productName)
				f.write(";")
				#Period
				f.write(removeJaar(datas[0]))
				f.write(";")
				#Interest Rate
				data = formatUnicode(datas[k])
				data = removeSpecial(data.encode("utf-8").strip())
				f.write(str(float(data)+0.25))
				f.write(";")
				#Coverage Start
				if(headers[k-1] == ">101%"):
					f.write("101")
				f.write(";")
				#Coverage End
				nonBreakSpace = u'\xa0'
				coverageEnd = headers[k-1].replace(nonBreakSpace,"")
				coverageEnd = removeSpecial(formatUnicode(coverageEnd.encode("utf-8").strip()))
				if(headers[k-1] != ">101%" and coverageEnd != "NHG"):
					f.write(coverageEnd)
				f.write(";")
				#Check Date
				f.write(str(now.strftime("%Y-%m-%d")))
				f.write(";")
				#Valid Since Date
				f.write(validSinceDate)
				f.write(";")
				#NHG
				if(coverageEnd!="NHG"):
					f.write("N;\n")
				else:
					f.write("Y;\n")

def removeJaar(str):
	str = str.replace("jaar","")
	return str

def removeSpecial(str):
	str = str.replace("%","").replace("≤","").replace(">","")
	return str

def formatUnicode(str):
	str = str.replace(",",".").replace("']","").replace("[u'","")
	return str