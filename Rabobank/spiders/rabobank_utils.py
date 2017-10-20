import scrapy
from scrapy import log
import os
import datetime
from format import doFormattingUnicode, doFormattingProductName, findCoverage

def rabo_scraper(divRow, validSince):
	f = open("output.csv", "a+")
	
	now = datetime.datetime.now()
	tableRows = divRow.xpath("div/table/tbody/tr")
	headers = tableRows[0].xpath("td")

	for i in range(1,len(tableRows)):
		tableDatas = tableRows[i].xpath("td")
		for j in range(1,len(tableDatas)):
			#log.msg("XX %s" % str(tableDatas[j].xpath("text()").extract()).replace("[u'","").replace("']",""), level = log.DEBUG)
			productName = doFormattingProductName((str(divRow.xpath("h2/text()").extract())))
			#static values
			f.write("NL;Robobank;")
			f.write("Rabobank")
			f.write(doFormattingUnicode(productName))
			f.write(";")

			#static values start
			f.write("Annuiteitenhypotheek;")

			f.write(doFormattingUnicode(str(tableDatas[0].xpath("text()").extract())))
			f.write(";")
			f.write(doFormattingUnicode(str(tableDatas[j].xpath("text()").extract())))
			f.write(";")
			if(j!=0):
				coverage = doFormattingUnicode(str(headers[j].xpath("strong/text()").extract()))
				coverage = findCoverage(coverage).split()
				coverageStart = coverage[0]
				coverageEnd = coverage[1]
				f.write(coverageStart)
				f.write(";")
				f.write(coverageEnd)
				f.write(";")
				f.write(str(now.strftime("%Y-%m-%d")))
				f.write(";")
				f.write(validSince)
				f.write(";")
				#static values start
				f.write("N;")
				f.write("\n")

			#f.write("\n")
	#f.write("\n\n")
	f.close()