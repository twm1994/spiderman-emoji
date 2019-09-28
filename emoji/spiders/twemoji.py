# -*- coding: utf-8 -*-
import scrapy


class TwemojiSpider(scrapy.Spider):
    name = 'twemoji'
    allowed_domains = ['https://commons.wikimedia.org/w/index.php?title=Category:Twemoji_v2']
    start_urls = ['http://https://commons.wikimedia.org/w/index.php?title=Category:Twemoji_v2/']

    def parse(self, response):
        pass
