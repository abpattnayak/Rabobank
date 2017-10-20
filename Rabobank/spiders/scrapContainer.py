import scrapy
from scrapy import log
import os

def scrap(divRow):
	f = open("output.csv", "w+")
	f.write(str(divRow.xpath("h3/text()").extract()).replace("']","").replace("[u'",""))
	f.write("\n")
	
	tableRows = divRow.xpath("div/table/tbody/tr")
	headers = tableRows[0].xpath("td")
	f.write(" \t")
	for i in range(1,len(headers)):
		#log.msg("XX %s" % str(headers[i].xpath("strong/text()").extract()).replace(",",".").replace("[u'","").replace("']",""), level = log.DEBUG)
		f.write(str(headers[i].xpath("strong/text()").extract()).replace(",",".").replace("[u'","").replace("']",""))
		f.write("\t")
	f.write("\n")
	for i in range(1,len(tableRows)):
		tableDatas = tableRows[i].xpath("td")
		for j in range(0,len(tableDatas)):
			#log.msg("XX %s" % str(tableDatas[j].xpath("text()").extract()).replace("[u'","").replace("']",""), level = log.DEBUG)
			f.write(str(tableDatas[j].xpath("text()").extract()).replace(",",".").replace("[u'","").replace("']",""))
			f.write("\t")
		f.write("\n")
	f.write("\n\n")
	f.close()