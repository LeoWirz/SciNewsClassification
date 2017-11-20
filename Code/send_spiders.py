# import dmoz spider class
from web_crawler_spyder import WebSiteSpider

# scrapy api
from twisted.internet import reactor
from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

def sends_spiders(list_):

    settings = Settings()

    settings.set("BOT_NAME", 'page_finder')

    crawler = CrawlerProcess(settings)
    for l in list_:
        crawler.crawl(WebSiteSpider(), url=l)
    crawler.start()
