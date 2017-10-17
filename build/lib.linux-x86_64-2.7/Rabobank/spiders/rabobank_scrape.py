import scrapy
from scrapy import log
from Rabobank.items import RabobankItem
import os
import re
from format import doFormattingUnicode
from dateutil.parser import parse
from scrapContainer import scrap


class Rabobank(scrapy.Spider):
	name = "my_scraper"
	allowed_domains = ['rabobank.nl']
	start_urls = ( 'https://www.rabobank.nl/particulieren/hypotheek/hypotheekrente/?intcamp=pa-hypotheek&inttype=tegel-hypotheekrente&intsource=hypotheek', )


	def parse(self, response):
		log.msg('parse(%s)' % response.url, level = log.DEBUG)
		
		#remove output file if exists
		try:
			os.remove("output.csv")
		except OSError:
			pass

		divRows = response.xpath("//*[@class='s14-lamella--shadow']")
		items = RabobankItem()


		#target table headings (h3)
		target1 = [u'Alle rentepercentages hypotheek met Basisvoorwaarden']
		target2 = [u'Alle rentepercentages hypotheek met Plusvoorwaarden']
		
		#validity since date search
		validString = response.xpath("//li[contains(text(),'totdat wij de tarieven wijzigen')]/text()").extract()
		validString = doFormattingUnicode(str(validString))

		regex = r"([0-9]+\s+[a-z]+\s+[0-9])\w+"
		pattern = re.compile(regex)
		matches = re.search(regex, validString, re.DOTALL)
		if matches:
			date = parse(matches.group(0))
			date = str(date).split()[0]
			#log.msg("ValidityDiv -----------------------------------------------%s" % date, level = log.DEBUG)

		#validString = "18 september 2017"

		f = open("output.csv","a+")
		#f.write("CountryCode;ProviderName;ProductName;LoanType;Period;Rate;Coverage;Check Date;ValidSinceDate;NHG\n")
	
		for divRow in divRows:
			head = divRow.xpath("div/h2/text()").extract()
			if(head==target1):
				divRow = divRow.xpath("div")
				scrap(divRow, date)
			
			if(head==target2):
				#log.msg("div row ----- %s" % str(divRow.xpath("div/div/table").extract()), level = log.DEBUG)
				divRow = divRow.xpath("div")
				scrap(divRow, date)

			f.close()
		yield items

	