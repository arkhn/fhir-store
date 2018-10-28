import scrapy
import urllib.parse


class Hl7Spider(scrapy.Spider):
    name = "hl7"
    root_url = "http://www.hl7.org/fhir/"

    custom_settings = {
        'DOWNLOAD_DELAY':
        1,
        'USER_AGENT':
        'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'
    }

    def start_requests(self):
        urls = [
            urllib.parse.urljoin(self.root_url, 'resourcelist.html'),
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        links = response.css("tr.frm-contents").css("a").xpath(
            "@href").extract()
        filtered_links = list(filter(lambda x: "#" not in x, links))
        for link in filtered_links:
            url = urllib.parse.urljoin(self.root_url, link)
            yield scrapy.Request(url=url, callback=self.parse_links)

    def parse_links(self, response):
        # ToDo
        pass
