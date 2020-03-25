from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from Lesson_5.jobparser import settings
from Lesson_5.jobparser import HhruSpider
from Lesson_5.jobparser import SuperjbSpider

if __name__=='__main__':
    crawler_settings = Settings() #create settings class
    crawler_settings.setmodule(settings) # bind pre_made settings in crawler settings to Class
    process = CrawlerProcess(settings=crawler_settings) #create process using settings
    process.crawl(HhruSpider) # bind spider to process(and to settings)
    process.crawl(SuperjbSpider) # bind spider to process(and to settings)
    process.start() #start
