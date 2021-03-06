import scrapy
import csv
from urllib.parse import urlparse
from multiprocessing import Process, Queue

# scrapy api
from twisted.internet import reactor
from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from scrapy.crawler import CrawlerRunner

class WebSiteSpider(scrapy.Spider):
    url = ''
    name = "website"
    limit = -1
    domain = ''
    allowed_domains=[]

    def start_requests(self):
        self.url = getattr(self, 'url', None)
        self.limit = getattr(self, 'limit', None)
        self.domain = '{uri.netloc}'.format(uri=urlparse(self.url)).replace('www.','')
        self.allowed_domains.append(self.domain)
        yield scrapy.Request(self.url, self.parse)

    def parse(self, response):
        links = list(set(response.xpath('//a/@href').extract()))

        end_links = [link for link in links if not link.endswith('/')]
        start_links = [self.url + link if link.startswith('/') else link for link in links]

        max_links_number = min(len(end_links), int(self.limit))
        print(max_links_number)

        filename = "../Datasets/crawled_articles_url/{}.csv".format(self.domain)

        with open(filename, "w", encoding='utf-8') as csv_file:
                writer = csv.writer(csv_file, delimiter=',')
                writer.writerow(["base_url","url"])
                for link in start_links[:max_links_number]:
                    writer.writerow([self.url,link])

        next_page = response.css('a::attr(href)').extract_first()
        if next_page is not None:
            yield response.follow(next_page, self.parse)

def sends_spiders(list_, max_limit=-1):

    settings = Settings()

    settings.set("BOT_NAME", 'page_finder')

    settings.set("LOG_ENABLED", 'False')

    crawler = CrawlerProcess(settings)
    for l in list_:
        crawler.crawl(WebSiteSpider(), url=l, limit=max_limit)
    crawler.start(stop_after_crawl=False)

def run_spider(list_, max_limit=-1):
    q = Queue()
    p = Process(target=f, args=(q,list_,max_limit,))
    p.start()
    result = q.get()
    p.join()

    if result is not None:
        raise result

def f(list_, max_limit=-1):
    print(list_)
    print(max_limit)
    try:
        runner = CrawlerRunner()
        deferred = runner.crawl(WebSiteSpider(), url=list_, limit=max_limit)
        deferred.addBoth(lambda _: reactor.stop())
        reactor.run()
    except Exception as e:
