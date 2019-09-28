# -*- coding: utf-8 -*-
import scrapy
import os
import json
import logging
from emoji.items import EmojiFile
import urllib.parse


class TwemojiSpider(scrapy.Spider):
    name = 'twemoji'
    resolution=[768,1024,1000,2000]
    size=[str(i)+'px' for i in resolution]
    file_name=''
    pagination_base='https://commons.wikimedia.org'
    emoji_url_base='https://commons.wikimedia.org/wiki/File:'
    file_url_base='https://upload.wikimedia.org/wikipedia/commons/thumb/'
    start_urls = ['https://commons.wikimedia.org/w/index.php?title=Category:Twemoji_v2']
    # start_urls = ['https://upload.wikimedia.org/wikipedia/commons/thumb/6/68/Twemoji2_1f170.svg/2000px-Twemoji2_1f170.svg.png']

    def __init__(self, *args, **kwargs):
        # disable yield in terminal
        logger = logging.getLogger('scrapy.core.scraper')
        logger.setLevel(logging.INFO)
        super().__init__(*args, **kwargs)

    def parse(self, response):
        # get all links to emoji file on current page
        # emoji_links=response.css('a.galleryfilename-truncate::attr(href)').getall()
        # for i in emoji_links:
        #     e=EmojiFile(uri=i)
        #     yield e

        # exploit the structure of the page, the second element matched will only be either 'next page' or 'previous page'
        pagination_link=response.css('a[title="Category:Twemoji v2"]:nth-of-type(2)::attr(href)').get()
        pagination_text=response.css('a[title="Category:Twemoji v2"]:nth-of-type(2)::text').get()
        # # recursively request all pages
        if pagination_text=='next page':
            print(pagination_text)
            yield scrapy.Request(urllib.parse.urljoin(self.pagination_base,pagination_link),self.parse)

    def save_png():
        pass