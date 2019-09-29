# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


import scrapy
import urllib.parse
import re
from emoji.items import EmojiFile

class EmojiPipeline(object):
    emoji_url_base='https://commons.wikimedia.org/wiki/File:'

    # def open_spider(self, spider):
    #     self.file = open('../emoji_files.json', 'w')

    # def close_spider(self, spider):
    #     self.file.close()

    def process_item(self, item, spider):
        # only handle EmojiFile item
        if isinstance(item, EmojiFile):
            # extract emoji file name
            if item.get('uri'):
                item['name']=re.match(r'/wiki/File:(.*)',item['uri']).group(1)
                # item['name']=item['uri'][len('/wiki/File:'):]

                # go to the page of each emoji and save the emoji with given resolutions
                yield scrapy.Request(urllib.parse.urljoin(self.emoji_url_base,item['name']),spider.open_emoji,meta={'filename':item['name']})
            return item
