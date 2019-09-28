# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import json
import re
from emoji.items import EmojiFile

class EmojiPipeline(object):
    def open_spider(self, spider):
        self.file = open('../emoji_files.json', 'w')

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        # only handle EmojiFile item
        if not isinstance(item, EmojiFile):
            return item
        # extract emoji file name
        if item.get('uri'):
            item['name']=re.match(r'/wiki/File:(.*)',item['uri']).group(1)
            # item['name']=item['uri'][len('/wiki/File:'):]
        line = json.dumps(dict(item),ensure_ascii=False) + "\n"
        self.file.write(line)
        return item
