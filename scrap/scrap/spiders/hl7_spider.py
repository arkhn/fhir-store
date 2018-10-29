import scrapy
import urllib.parse
import html2text
import os


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
        self.log('Processing URL: {}'.format(response.url))
        json_html = response.css("#json").css("#json-inner").css(
            "pre").extract_first().strip()
        json_text = html2text.html2text(json_html)
        # self.log(json_text)

        page = response.url.split("/")[-1].replace(".html", "")
        filename = '{}.json'.format(page)
        filepath = os.path.join("../json", filename)
        with open(filepath, 'w') as f:
            f.write(json_text)
        self.log('Saved file \"{}\"'.format(filename))
