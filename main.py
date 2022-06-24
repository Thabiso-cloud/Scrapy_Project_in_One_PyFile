""""
Running scrapy project from a single python file. This is useful for instances where one does not need all the other
machinery that comes with a scrapy project. This project scrapes the name, meta info and price of all single malts and
exports them to a csv file
"""

import scrapy
from scrapy.crawler import CrawlerProcess

class WhiskySpider(scrapy.Spider):
    name = 'singlemalts'

    def start_requests(self):
        yield scrapy.Request('https://www.thewhiskyexchange.com/c/40/single-malt-scotch-whisky?pg=1&psize=120&sc')

    def parse(self, response):
        products = response.css('li.product-grid__item')
        for item in products:
            yield {
                'name': item.css('p.product-card__name::text').get().strip(),
                'meta': item.css('p.product-card__meta::text').get().strip(),
                'price': item.css('p.product-card__price::text').get().strip().replace('£', '')
            }

        for x in range(2,25):
            yield(scrapy.Request(f'https://www.thewhiskyexchange.com/c/40/single-malt-scotch-whisky?pg={x}&psize=120&sc'))


process = CrawlerProcess(settings= {
    'FEED_URI': 'whisky.csv',
    'FEED_FORMAT': 'csv'
})

process.crawl(WhiskySpider)
process.start()