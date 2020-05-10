# -*- coding: utf-8 -*-
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import os
import string
from io import BytesIO
import scrapy
import re
from PIL import Image
from lanvshen.items import LanvshenItem


class SlanSpider(CrawlSpider):
    name = 'slan'
    allowed_domains = ['lanvshen.com', 'hywly.com']
    start_urls = ['https://www.lanvshen.com/']

    rules = (
        Rule(LinkExtractor(allow=r'[%s]/\d+' % string.ascii_letters), follow=True, callback='parse_list'),
    )

    def parse_list(self, response):
        item = LanvshenItem()
        item["idd"] = os.path.split(response.url)[0].split("/")[-1]
        item["title"] = response.xpath("//div[@class='weizhi']/h1/text()").get()
        item["shoot"] = response.xpath("//*[contains(text(), '拍摄机构：')]/a/text()").get()
        item["quantity"] = response.xpath("//*[contains(text(), '图片数量：')]/text()").get()
        item["name"] = response.xpath("//*[contains(text(), '出镜模特：')]/a[1]/text()").get()
        item["nickname"] = response.xpath("//*[contains(text(), '出镜模特：')]/a[2]/text()").get()
        item["birthday"] = response.xpath("//*[contains(text(), '出镜模特：')]/text()").re_first("生日：(.*?)；")
        item["height"] = response.xpath("//*[contains(text(), '出镜模特：')]/text()").re_first("身高：(.*?)；")
        if item["name"]:
            yield item
        url_list = re.findall("(https://img.hywly.com/.*?)\"", response.text)
        for url in url_list:
            yield scrapy.Request(url, callback=self.parse_item, priority=10)

    def parse_item(self, response):
        file, name = os.path.split(response.url)
        file_path = f"./images/{file.split('com/')[-1]}"
        if not os.path.exists(file_path):
            os.makedirs(file_path)
        img = Image.open(BytesIO(response.body))
        img.save(f"{file_path}/{name}")
