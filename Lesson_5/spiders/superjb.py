# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem
import re


class SuperjbSpider(scrapy.Spider):
    name = 'superjb'
    allowed_domains = ['superjob.ru']
    start_urls = ['https://russia.superjob.ru/vacancy/search/?keywords=python']

    def parse(self, response: HtmlResponse):
        # this funciton gets vacancy search pages, and gets inside vacancies
        next_page = response.xpath(
            "//a[@class='icMQ_ _1_Cht _3ze9n f-test-button-dalshe f-test-link-Dalshe']/@href"
        ).extract_first()
        yield response.follow(next_page, callback=self.parse)

        vacancy = response.xpath(
            "//div[@class='_3zucV _2GPIV f-test-vacancy-item i6-sc _3VcZr']//div[@class='_2g1F-']/a/@href"
        ).extract()

        for link in vacancy:
            yield response.follow(link, callback=self.vacancy_parse)

    def vacancy_parse(self, response: HtmlResponse):
        # this funciton gets data from vacancy page and passes it ti Scrapy_Items
        name = response.xpath("//div[@class='_3zucV undefined I4QiU']//h1/text()").extract_first()
        link = response.xpath("//head//link[4]/@href").extract_first()
        source = 'superjob'
        salary_min_max = response.xpath(
            "//span[@class='_3mfro _2Wp8I ZON4b PlM3e _2JVkc']/text()"
        ).extract()
        salary = response.xpath(
            "//span[@class='_3mfro _2Wp8I ZON4b PlM3e _2JVkc']/span/text()"
        ).extract()
        # turn salary lists into strings
        salarylist = []
        salary_min_max = str(''.join(salary_min_max))
        salary_min_max.replace(u'\xa0',u'').encode('utf-8')
        salary = str(''.join(salary))
        salary.replace(u'\xa0',u'').encode('utf-8')
        salary.replace(f'₽',f'')
        # salarylist.replace(' ','')
        salarylist.append(salary)

        # put string parts into different fields
        if re.findall(r'от', salary_min_max):
            salary_min = salary
        if salary_min_max == '':
            salary_min = salary
        if salary_min_max == 'до':
            salary_max = salarylist
        else:
            salary_min = salary
            salary_max = 'по договоренности'
        if re.findall(r'—', salary) :
            salary_min, salary_max = salary.split('—')
        if salary_min == '':
            salary_min = 'по договоренности'
        salary_currency = 'руб'
        # yield generated data to scrapy fileds

        yield JobparserItem(name=name,
                            # salary=salarylist,
                            link=link,
                            source=source,
                            salary_min=salary_min,
                            salary_max=salary_max,
                            # salary_net_gross=salary_net_gross,
                            salary_currency=salary_currency)
