# -*- coding: utf-8 -*-

import os
import json
from scrapy.crawler import CrawlerProcess

from process import Clean, Hl7Spider
from process import hl7_spider, json_to_yml

# 1. Scrap the JSON text from hl7 reference
process = CrawlerProcess({
    "USER_AGENT":
    "Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0"
})
process.crawl(Hl7Spider)
process.start()

# 2. Clean files to have proper json and also convert to yml
FILE_PATH = os.path.dirname(__file__)
ROOT_FOLDER_SRC_NAME = hl7_spider.SAVING_DIRECTORY
ROOT_FOLDER_DEST_NAME = "resources/json"
ROOT_FOLDER_SRC_PATH = os.path.join(FILE_PATH, os.pardir, ROOT_FOLDER_SRC_NAME)

cleaner = Clean()
for root, dirs, files in os.walk(ROOT_FOLDER_SRC_PATH):
    for fname in files:
        print('Cleaning', root, fname)
        # Clean JSON file
        file_path = os.path.join(root, fname)
        json_file_path = file_path.replace(ROOT_FOLDER_SRC_NAME, ROOT_FOLDER_DEST_NAME)
        yml_file_path = json_file_path.replace("json", "yml")
        cleaner.clean_json(file_path, json_file_path)

        # Convert to YAML
        with open(json_file_path) as input_file:
            new_yml_file = json_to_yml(json.load(input_file))

            if not os.path.exists(os.path.dirname(yml_file_path)):
                os.makedirs(os.path.dirname(yml_file_path))
            with open(yml_file_path, 'w') as output_file:
                output_file.write(new_yml_file)
