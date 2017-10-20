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
from rabobank_utils import rabo_scraper


class ProductSpider(scrapy.Spider):
    name = "product_spider"
    allowed_domains = ['ing.nl']
    #start_urls = ['https://www.ing.nl/particulier/hypotheken/actuele-hypotheekrente/index.html']

    #def __init__(self):
        #self.driver = webdriver.Chrome()

    def start_requests(self):
        urls = ['https://www.ing.nl/particulier/hypotheken/actuele-hypotheekrente/index.html']
        for url in urls:
            yield scrapy.Request(url = url, callback = self.parse)

    def parse(self, response):
        
        #ING Bank I

        self.driver = webdriver.PhantomJS()
        self.driver.set_window_size(1120, 550)
        #remove output file if exists
        #try:
        #    os.remove("ing_data.csv")
        #except OSError:
        #    pass
        #f = open("output-ing.csv", "a+")
        
        items = []
        self.driver.get(response.url)
        #self.driver.implicitly_wait(50)
        log.msg("URL ----- %s" %response.url, level = log.DEBUG) 
        sel = scrapy.Selector(text=self.driver.page_source)
        ctr = 0
        
        productName1 = "Annuïteitenhypotheek"
        productName2 = "Lineaire hypotheek" 

        #validity since date search
        
        validString = sel.xpath("//p[contains(@class, 'small-font') and contains(text(),'Deze tarieven gelden voor nieuwe offertes en renteaanpassingen voor bestaande hypotheken uitgebracht vanaf')]/text()").extract()

        validString = doFormattingUnicode(str(validString[0]).encode("utf-8").strip())
        
        regex = r"([0-9]+\s+[a-z]+\s+[0-9])\w+"
        pattern = re.compile(regex)
        matches = re.search(regex, validString, re.DOTALL)
        if matches:
            date = changeMonth(matches.group(0))
            date = parse(date)
            date = str(date).split()[0]
        
        ing_scraper(productName1, sel, date)
        ing_scraper(productName2, sel, date)

        self.driver.close()


        #ING Bank II
        
        self.driver = webdriver.PhantomJS()
        self.driver.set_window_size(1120, 550)
        

        url2 = 'https://www.ing.nl/particulier/hypotheken/actuele-hypotheekrente/actuele-hypotheekrente-andere-hypotheken/index.html'
        self.driver.get(url2)
        sel = scrapy.Selector(text=self.driver.page_source)
        log.msg("URL ----- %s" %url2, level = log.DEBUG) 
        validString = sel.xpath("//small[contains(text(),'Deze tarieven gelden voor nieuwe offertes en renteaanpassingen voor bestaande hypotheken uitgebracht vanaf')]/text()").extract()
        log.msg("String ----> %s" %validString, level = log.DEBUG)
        validString = doFormattingUnicode((validString[0]).encode("utf-8").strip())
        
        regex = r"([0-9]+\s+[a-z]+\s+[0-9])\w+"
        pattern = re.compile(regex)
        matches = re.search(regex, validString, re.DOTALL)
        if matches:
            date = changeMonth(matches.group(0))
            date = parse(date)
            date = str(date).split()[0]

        productName3 = "Aflossingsvrije hypotheek"
        productName4 = "Bankspaarhypotheek" 

        ing_scraper(productName3, sel, date)
        ing_scraper(productName4, sel, date)


        #Rabobank
        self.driver = webdriver.PhantomJS()
        self.driver.set_window_size(1120, 550)
        

        url2 = 'https://www.rabobank.nl/particulieren/hypotheek/hypotheekrente/?intcamp=pa-hypotheek&inttype=tegel-hypotheekrente&intsource=hypotheek'
        self.driver.get(url2)
        sel = scrapy.Selector(text = self.driver.page_source)
        log.msg("URL ----- %s" %url2, level = log.DEBUG) 
        

        divRows = sel.xpath("//*[@class='s14-lamella--shadow']")
        
        #target table headings (h3)
        target1 = [u'Alle rentepercentages hypotheek met Basisvoorwaarden']
        target2 = [u'Alle rentepercentages hypotheek met Plusvoorwaarden']
        
        #validity since date search
        validString = sel.xpath("//li[contains(text(),'totdat wij de tarieven wijzigen')]/text()").extract()
        validString = changeMonth(doFormattingUnicode(str(validString)))

        regex = r"([0-9]+\s+[a-z]+\s+[0-9])\w+"
        pattern = re.compile(regex)
        matches = re.search(regex, validString, re.DOTALL)
        if matches:
            date = parse(matches.group(0))
            date = str(date).split()[0]
            
        f = open("output.csv","a+")
        
        for divRow in divRows:
            head = divRow.xpath("div/h2/text()").extract()
            if(head==target1):
                divRow = divRow.xpath("div")
                rabo_scraper(divRow, date)
            
            if(head==target2):
                #log.msg("div row ----- %s" % str(divRow.xpath("div/div/table").extract()), level = log.DEBUG)
                divRow = divRow.xpath("div")
                rabo_scraper(divRow, date)

            f.close()
        
        return items