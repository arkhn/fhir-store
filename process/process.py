# -*- coding: utf-8 -*-

import os
from scrapy.crawler import CrawlerProcess

from scrap.scrap.spiders.hl7_spider import Hl7Spider
from clean.hl7 import Clean
from convert import yml


# # Scrap the JSON text from hl7 reference
# process = CrawlerProcess({
#     "USER_AGENT":
#     "Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0"
# })
# process.crawl(Hl7Spider)
# process.start()

# Get all file to process
FILE_PATH = os.path.dirname(__file__)
ROOT_FOLDER_SRC_NAME = "json"
ROOT_FOLDER_DEST_NAME = "yaml"
ROOT_FOLDER_SRC_PATH = os.path.join(FILE_PATH, os.pardir, ROOT_FOLDER_SRC_NAME)
ROOT_FOLDER_DEST_PATH = os.path.join(FILE_PATH, os.pardir, ROOT_FOLDER_DEST_NAME)

for root, dirs, files in os.walk(ROOT_FOLDER_SRC_PATH):
    for fname in files:

        # Clean JSON file
        json_file_path = os.path.join(root, fname)
        yaml_file_path = json_file_path.replace("json", "yaml")
        Clean().clean_json(json_file_path, json_file_path)

        # Convert to YAML
        with open(json_file_path) as input_file:
            input_file.readline()
            new_yaml_file = json_to_yml(input_file)
            with open(yaml_file_path, 'w') as output_file:
                output_file.write(new_yaml_file)

