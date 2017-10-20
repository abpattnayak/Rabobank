import scrapy
from scrapy import log
from Rabobank.items import RabobankItem
import os
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

		divRows = response.xpath("//*[@class='content s14-richtext']")
		items = RabobankItem()


		#target table headings (h3)
		target1 = [u'Rentepercentage hypotheek met Basisvoorwaarden']
		target2 = [u'Rentepercentage hypotheek met Plusvoorwaarden']
		
		for divRow in divRows:
			head = divRow.xpath("h3/text()").extract()
			if(head==target2):
				scrap(divRow)

		yield items

	