# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
from Lesson_5.jobparser import JobparserItem
import re


class HhruSpider(scrapy.Spider):
    name = 'hhru'
    allowed_domains = ['hh.ru']
    start_urls = ['https://hh.ru/search/vacancy?area=&st=searchVacancy&text=python']

    def parse(self, response: HtmlResponse):
        # this funciton gets vacancy search pages, and gets inside vacancies
        next_page = response.xpath(
            '//a[@class="bloko-button HH-Pager-Controls-Next HH-Pager-Control"]/@href'
        ).extract_first()
        yield response.follow(next_page, callback=self.parse)

        vacancy = response.xpath("//a[@class='bloko-link HH-LinkModifier']/@href").extract()

        for link in vacancy:
            yield response.follow(link, callback=self.vacancy_parse)

    def vacancy_parse(self, response: HtmlResponse):
        # this funciton gets data from vacancy page and passes it ti Scrapy_Items
        name = response.xpath("//div[contains(@class,'vacancy-title')]/h1/text()").extract_first()
        link = response.xpath("//head//link[9]/@href").extract_first()
        source = 'hh'
        salary = response.xpath(
            "//div[contains(@class,'vacancy-title')]/p[@class='vacancy-salary']/span/text()"
        ).extract()
        # turn salary lists into strings
        salarylist = []
        salary = str(''.join(salary))
        salary.replace(u'\xa0',u'').encode('utf-8')
        # salarylist.replace(' ','')
        salarylist.append(salary)

        # put string parts into different fields
        if  re.findall(r'от (\d+....)', salarylist[0]):
            salary_min = re.findall(r'от (\d+....)', salarylist[0])
        else: salary_min = 'з/п не указана'
        if  re.findall(r'до (\d+....)', salarylist[0]):
            salary_max = re.findall(r'до (\d+....)', salarylist[0])
        else: salary_max = 'з/п не указана'
        if  re.findall(r'на руки', salarylist[0]) or re.findall(r'до вычета', salarylist[0]):
            salary_net_gross = 'net'
        else: salary_net_gross = 'gross'
        if re.findall(r"[A-Z]{3}", salarylist[0]) :
            salary_currency = re.findall(r"[A-Z]{3}", salarylist[0])
        elif re.findall(r"[а-я]{3}\.", salarylist[0]) :
            salary_currency = re.findall(r"[а-я]{3}\.", salarylist[0])
        else: salary_currency = ''
        # yield generated data to scrapy fileds

        yield JobparserItem(name=name,
                            #salary=salarylist,
                            link=link,
                            source=source,
                            salary_min=salary_min,
                            salary_max=salary_max,
                            salary_net_gross=salary_net_gross,
                            salary_currency=salary_currency)