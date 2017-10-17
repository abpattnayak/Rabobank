import scrapy
import datetime
import re
from dateutil.parser import parse
from selenium import webdriver
from scrapy import log
from format import doFormattingUnicode, changeMonth

class ProductSpider(scrapy.Spider):
    name = "product_spider"
    allowed_domains = ['ing.nl']
    start_urls = ['https://www.ing.nl/particulier/hypotheken/actuele-hypotheekrente/index.html']

    def __init__(self):
        self.driver = webdriver.Chrome()

    def parse(self, response):
        f = open("output-ing.csv", "a+")
        self.driver.get(response.url)
        now = datetime.datetime.now()
        sel = scrapy.Selector(text=self.driver.page_source)
        ctr = 0
        tables =  sel.xpath('//table[@class="table table-b table-lr-unpadded l-mb-0"]/tbody');
        
        title = sel.xpath("//table[@class='table table-b table-lr-unpadded l-mb-0']/thead/tr/th/p/text()").extract()
        title = str(title).split()[0]

        #validity since date search
        validString = sel.xpath("//p[contains(@class, 'small-font') and contains(text(),'Deze tarieven gelden voor nieuwe offertes en renteaanpassingen voor bestaande hypotheken uitgebracht vanaf')]/text()").extract()
        validString = doFormattingUnicode(str(validString[0]))
        log.msg("Date ------------- %s" %validString, level = log.DEBUG)

        regex = r"([0-9]+\s+[a-z]+\s+[0-9])\w+"
        pattern = re.compile(regex)
        matches = re.search(regex, validString, re.DOTALL)
        if matches:
            log.msg("Date ------------- %s" %matches.group(0), level = log.DEBUG)
            date = changeMonth(matches.group(0))
            date = parse(date)
            date = str(date).split()[0]
            
        for i in range(0,2): #tables
            rows = tables[i].xpath("tr")
            headers = tables[i].xpath("tr/td/strong/text()").extract()
            for j in range(1,len(rows)):
                datas = rows[j].xpath("td/text()").extract()
                for k in range(1, len(datas)):
                    f.write("NL;ING;")
                    f.write("ING")
                    f.write(doFormattingUnicode(title))
                    f.write(";")
                    f.write("Annuiteitenhypotheek")
                    f.write(";")
                    f.write(datas[0])
                    f.write(";")
                    data = doFormattingUnicode(datas[k])
                    f.write(data)
                    f.write(";")
                    temp = headers[k-1].encode("utf-8").strip()
                    f.write(temp)
                    f.write(";")
                    f.write(str(now.strftime("%Y-%m-%d")))
                    f.write(";")
                    f.write(date)
                    f.write(";")
                    f.write("N;\n")
        
        self.driver.close()