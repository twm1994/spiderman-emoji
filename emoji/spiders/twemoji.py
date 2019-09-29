# -*- coding: utf-8 -*-
import scrapy
import os
import json
import logging
from emoji.items import EmojiFile
import urllib.parse
import re


class TwemojiSpider(scrapy.Spider):
    name = 'twemoji'
    resolution=[768,1024,1000,2000]
    size=[str(i)+'px' for i in resolution]
    pagination_base='https://commons.wikimedia.org'
    start_urls = ['https://commons.wikimedia.org/w/index.php?title=Category:Twemoji_v2']
    # emoji_url_base='https://commons.wikimedia.org/wiki/File:'

    def __init__(self, *args, **kwargs):
        # disable yield in terminal
        logger = logging.getLogger('scrapy.core.scraper')
        logger.setLevel(logging.INFO)
        super().__init__(*args, **kwargs)

    def parse(self, response):
        # get all links to emoji file on current page
        emoji_links=response.css('a.galleryfilename-truncate::attr(href)').getall()
        for i in emoji_links:
            file_name=re.match(r'/wiki/File:(.*)',i).group(1)
            # file_name=i[len('/wiki/File:'):]

            # go to the page of each emoji and save the emoji with given resolutions
            yield scrapy.Request(urllib.parse.urljoin(self.pagination_base,i),self.open_emoji,meta={'filename':file_name})

        # exploit the structure of the page, the second element matched will only be either 'next page' or 'previous page'
        pagination_link=response.css('a[title="Category:Twemoji v2"]:nth-of-type(2)::attr(href)').get()
        pagination_text=response.css('a[title="Category:Twemoji v2"]:nth-of-type(2)::text').get()

        # recursively request all pages
        if pagination_text=='next page':
            yield scrapy.Request(urllib.parse.urljoin(self.pagination_base,pagination_link),self.parse)

    def open_emoji(self, response):
        # actual_link=response.css('a.mw-thumbnail-link:nth-of-type(1)::attr(href)').get()

        # # extract the file download link, 512px is the first occurence
        # download_link=re.match(r'(.*)512px',actual_link).group(1)

        # # download png file of each resolution
        # for i in self.size:
        #     url=i+'-'+response.meta['filename']+'.png'
        #     request=urllib.parse.urljoin(download_link,url)
        #     yield scrapy.Request(request,self.save_png,meta={'filename':url,'size':i})

        # download svg file
        svg_link=response.css('a.internal::attr(href)').get()
        yield scrapy.Request(svg_link,self.save_svg,meta={'filename':response.meta['filename']})

    def save_png(self, response):
        path='pic/'+response.meta['size']
        if not os.path.exists(path):
            os.makedirs(path)
        with open(os.path.join(path,response.meta['filename']),'wb') as f:
            f.write(response.body)

    def save_svg(self, response):
        path='pic/svg'
        if not os.path.exists(path):
            os.makedirs(path)
        with open(os.path.join(path,response.meta['filename']),'wb') as f:
            f.write(response.body)