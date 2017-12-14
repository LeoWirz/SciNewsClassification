# -*- coding: utf-8 -*-
import scrapy
import csv
from multiprocessing import Process, Queue
from urllib.parse import urlparse

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule, CrawlSpider

from twisted.internet import reactor
from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from scrapy.crawler import CrawlerRunner


class DatabloggerSpider(CrawlSpider):
    # The name of the spider
    name = "linkeater"

    # The domains that are allowed (links to other domains are skipped)
    allowed_domains = ['geology.com']

    # This spider has one rule: extract all (unique and canonicalized) links, follow them and parse them using the parse_items method
    rules = [
        Rule(
            LinkExtractor(
                canonicalize=True,
                unique=True
            ),
            follow=True,
            callback="parse"
        )
    ]

    visited_url = []
    final_nodes = []
    limit = -1
    domain = ''
    url = ''
    csv_file = ''


    # Method which starts the requests by visiting all URLs specified in start_urls
    def start_requests(self):
        self.url = getattr(self, 'url', None)
        self.limit = getattr(self, 'limit', None)
        self.domain = '{uri.netloc}'.format(uri=urlparse(self.url)).replace('www.','')

        filename = "../Datasets/crawled_articles_url/{}.csv".format(self.allowed_domains[0])
        self.csv_file = open(filename,'a')
        yield scrapy.Request(self.url, callback=self.parse, dont_filter=False)

    def parse(self, response):
        print('parsing')
        # get all links from the response page
        links = LinkExtractor(canonicalize=True, unique=True).extract_links(response)

        max_links = 100
        if self.limit > 0:
            max_links = int(self.limit)

        for link in links:
            # if we exceed the max number of link we stop
            if len(self.final_nodes) >= max_links:
                break

            # Check whether the domain of the URL of the link is allowed; so whether it is in one of the allowed domains
            is_allowed = False
            for allowed_domain in self.allowed_domains:
                if allowed_domain in link.url:
                    is_allowed = True

            # else we check if it's already in the list
            if is_allowed and (link.url not in self.final_nodes):
                # if not, we add it
                #filename = "../urlspider/csv/{}.csv".format(self.allowed_domains[0])
                #with open(filename, "a+") as csv_file:
                writer = csv.writer(self.csv_file, delimiter=',')
                writer.writerow([response.url,link.url])
                self.final_nodes.append(link.url)
            # follow next link
            yield response.follow(link.url, self.parse)
        # 
        self.visited_url.append(response.url)

class DatabloggerScraperItem(scrapy.Item):
    # The source URL
    url_from = scrapy.Field()
    # The destination URL
    url_to = scrapy.Field()

def run_spider(list_, max_limit=-1):
    print('rennung')
    q = Queue()
    p = Process(target=fu)
    print('starting')
    p.start()
    result = q.get()
    p.join()
    if result is not None:
        raise result

def fu(q,list_, max_limit=-1):
    print(list_)
    print(max_limit)
    try:
        runner = CrawlerRunner()
        deferred = runner.crawl(DatabloggerSpider, url=list_, limit=max_limit)
        deferred.addBoth(lambda _: reactor.stop())
        reactor.run()
        q.put(None)
    except Exception as e:
        q.put(e)