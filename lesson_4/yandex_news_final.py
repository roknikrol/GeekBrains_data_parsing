from lxml import html
import requests
import pandas as pd
from datetime import datetime
from pymongo import MongoClient
import json
from pprint import pprint

def get_yandex_news():
    #define browser header
    header = {'User-Agent':"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) "
                           "Chrome/79.0.3945.136 YaBrowser/20.2.1.248 Yowser/2.5 Yptp/1.46 Safari/537.36"}
    #web site link
    link = 'https://yandex.ru/news/'
    #user requests.get to get website response, set params to text string
    response = requests.get(link, headers=header)
    #use lxml.html to upload response text for a string (standard procedure)
    root = html.fromstring(response.text)
    for i in root:
        news_dict = {}
        news_name = i.xpath('.//div/h2/a/text()')
        news_link = i.xpath('.//div/h2/a/@href')
        news_source_time = i.xpath("//div[@class='story__date']/text()")
        news_dict['Name'] = news_name
        news_dict['link'] = news_link
        news_dict['Source_time'] = news_source_time

    result = pd.DataFrame(news_dict, dtype=str)

    result['Source'] = result['Source_time'].str[:-6]
    result['Time'] = result['Source_time'].str[-5:]
    result['link'] = result['link'].replace(r'/news/', link, regex=True)
    result['Date'] = datetime.today().strftime('%Y-%m-%d')
    del result['Source_time']

    yandex_data = result.to_dict()

    df = pd.DataFrame.from_dict(yandex_data)
    records = json.loads(df.T.to_json()).values()
    return records


def to_mongo(db,data_foo):
    clinet = MongoClient('localhost', 27017)
    db = clinet[f'{db}']
    data_cl = db.new_data
    data_cl.insert_many(data_foo)
