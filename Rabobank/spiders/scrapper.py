# coding=utf-8
import scrapy
import datetime
import re, os
from scrapy.http import Request
from dateutil.parser import parse
from selenium import webdriver
from scrapy import log
from format import doFormattingUnicode, changeMonth
from ing_utils import ing_scraper

class ScrappingSpider(scrapy.Spider):
	name = 'scrapping_spider'

	#def __init__(self):
		#self.driver = webdriver.PhantomJS()

	def start_requests(self):
		urls = ['https://www.ing.nl/particulier/hypotheken/actuele-hypotheekrente/index.html','https://www.ing.nl/particulier/hypotheken/actuele-hypotheekrente/actuele-hypotheekrente-andere-hypotheken/index.html']
		for url in urls:
			yield scrapy.Request(url = url, callback = self.parse)

	def parse(self, response):
		self.driver = webdriver.Chrome()
		log.msg("URL -----> %s" % response.url, level = log.DEBUG)
		self.driver.get(response.url)
		sel = scrapy.Selector(text=self.driver.page_source)
		self.driver.close()