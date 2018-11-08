# -*- coding: utf-8 -*-

from scrapy.crawler import CrawlerProcess
from scrap.scrap.spiders.hl7_spider import Hl7Spider

# Scrap the JSON text from hl7 reference
process = CrawlerProcess({
    "USER_AGENT":
    "Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0"
})
process.crawl(Hl7Spider)
process.start()
