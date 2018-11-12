# -*- coding: utf-8 -*-

import scrapy
import urllib.parse
import os
from bs4 import BeautifulSoup


def get_parent_dir(path):
    return os.path.split(path)[0]


FILE_PATH = os.path.dirname(__file__)
PROJECT_PATH = get_parent_dir(
    get_parent_dir(get_parent_dir(get_parent_dir(FILE_PATH))))
SAVING_DIRECTORY = "scrap_files"


class Hl7Spider(scrapy.Spider):
    name = "hl7"
    root_url = "http://www.hl7.org/fhir/"
    saving_path = os.path.join(PROJECT_PATH, SAVING_DIRECTORY)

    custom_settings = {
        'DOWNLOAD_DELAY': 1
    }

    def start_requests(self):
        if not os.path.exists(self.saving_path):
            os.mkdir(self.saving_path)
        urls = [
            urllib.parse.urljoin(self.root_url, 'resourcelist.html'),
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        R2_table_rows = response.css("#tabs-3").css("tr")
        for tr in R2_table_rows:
            table_data = tr.css("td")

            if len(table_data) == 1:
                # Get the parent category
                parent_category = BeautifulSoup(
                    table_data.css("b").extract_first(), "lxml").text

                if not os.path.exists(
                        os.path.join(self.saving_path, parent_category)):
                    os.mkdir(os.path.join(self.saving_path, parent_category))

            elif len(table_data) > 1:
                for td in table_data:
                    # Get the category and the links
                    category = BeautifulSoup(
                        td.css("p").extract_first(), 'lxml').text.replace(
                            "\n", "").replace(":", "")

                    if not os.path.exists(
                            os.path.join(self.saving_path, parent_category,
                                         category)):
                        os.mkdir(
                            os.path.join(self.saving_path, parent_category,
                                         category))

                    links = td.css("a").xpath("@href").extract()
                    titles = td.css("a").xpath("text()").extract()
                    links_struct = list(zip(links, titles))
                    filtered_links = list(
                        filter(lambda x: "#" not in x[0], links_struct))

                    for link in filtered_links:
                        url = urllib.parse.urljoin(self.root_url, link[0])

                        request = scrapy.Request(
                            url=url, callback=self.parse_links)
                        request.meta["parent_category"] = parent_category
                        request.meta["category"] = category
                        request.meta["title"] = link[1]
                        yield request

    def parse_links(self, response):
        self.log('Processing URL: {}'.format(response.url))
        parent_category = response.meta["parent_category"]
        category = response.meta["category"]
        title = response.meta["title"]

        json_html = response.css("#json").css("#json-inner").css(
            "pre").extract_first()
        if json_html:
            json_html = json_html.strip()
            json_text = BeautifulSoup(json_html, 'lxml').text
            # self.log(json_text)

            filename = '{}.json'.format(title)
            filepath = os.path.join(self.saving_path, parent_category,
                                    category, filename)
            with open(filepath, 'w') as f:
                f.write(json_text)
            self.log('Saved file \"{}\"'.format(filename))
        else:
            self.log("No JSON found in page {}".format(response.url))
