# import scrapy
from scrapy.spiders import CrawlSpider, Request
from quoteScraper.items import QuotescraperItem
from dotenv import load_dotenv
import os

load_dotenv()

PROXY = os.getenv('PROXY')
INPUT_URL = os.getenv("INPUT_URL")
OUTPUT_FILE = os.getenv("OUTPUT_FILE")

class QuotespiderSpider(CrawlSpider):
    name = 'quoteSpider'

    def start_requests(self):
        urls = [INPUT_URL + "/page/%d/" % i for i in range(1, 10)]
        yield Request(urls, meta={'playwright': True})

    def parse(self, response):
        for quote in response.css('div.quote'):
            quote_item = QuotescraperItem()
            quote_item['text'] = quote.css('span.text::text').get()
            quote_item['by'] = quote.css('small.author::text').get()
            quote_item['tags'] = quote.css('div.tags a.tag::text').getall()

            file = open(OUTPUT_FILE, "a")
            file.write(quote_item['text'])
            file.write(quote_item['by'])
            file.write(quote_item['tags'])
            file.close()
            yield quote_item


