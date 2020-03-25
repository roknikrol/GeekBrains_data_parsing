# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
from scrapy.loader import ItemLoader
from Lesson_6.leroymparser.items import LeroymparserItem

class LermerparserSpider(scrapy.Spider):
    name = 'lermerparser'
    allowed_domains = ['leroymerlin.ru']
    start_urls = [f'https://leroymerlin.ru/catalogue/suhie-smesi-i-gruntovki/']
    #
    #
    # def __init__(self):
    #     mark = 'suhie-smesi-i-gruntovki/'
    #     self.start_urls = [f'https://leroymerlin.ru/catalogue/']


    def parse(self, response:HtmlResponse):
        cat_links = response.xpath("//div[@class='section-card']//div[@class='items']//li/a/@href").extract()
        for i in cat_links:
            yield response.follow(i,callback=self.parse)
        prod_links = response.xpath("//div[@class='ui-sorting-cards']//div[@class='product-name']/a/@href").extract()
        for link in prod_links:
            yield response.follow(link,callback=self.parse_prod)



    def parse_prod(self, response:HtmlResponse):
        cat_num_link = len(response.xpath("//div[@class='breadcrumbs']/a").getall())
        loader = ItemLoader(item=LeroymparserItem(), response=response)
        loader.add_xpath('name', "//h1[@class='header-2']/text()")
        loader.add_xpath('description', "//section[@id='nav-description']//div/p/text()")
        loader.add_xpath('price', "//uc-pdp-price-view[@class='primary-price']/span[@slot='price']/text()")
        loader.add_xpath('pictures',
                         "//picture[@slot='pictures']/source[@media=' only screen and (min-width: 1024px)']/@srcset"
                         )
        loader.add_xpath('category',f"//div[@class='breadcrumbs']/a[{cat_num_link}]/@data-division")
        yield loader.load_item()

