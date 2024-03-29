# this spider is scraping information from "search page", it includes pagination as well
# spider is scraping URL, Title and Address
import scrapy
from scrapy import Request

class JobsSpider(scrapy.Spider):
    name = 'jobs'
    allowed_domains = ['https://newyork.craigslist.org/search/egr']
    start_urls = ['https://newyork.craigslist.org/search/egr/']

    def parse(self, response):
        jobs = response.xpath('//p[@class="result-info"]')
        for job in jobs:
            title = job.xpath('a/text()').extract_first()
            address = job.xpath('span[@class="result-meta"]/span[@class="result-hood"]/text()').extract_first("")[2:-1]
            relative_url = job.xpath('a/@href').extract_first()
            absolute_url = response.urljoin(relative_url)

            yield{'URL':absolute_url, 'Title':title, 'Address':address}

        relative_next_url = response.xpath('//a[@class="button next"]/@href').extract_first()
        absolute_next_url = response.urljoin(relative_next_url)

        yield Request(absolute_next_url, callback=self.parse)

    def parse_page(self, response):
        url = response.meta.get('URL')
        title = response.meta.get('Title')
        address = response.meta.get('Address')
        description = "".join(line for line in response.xpath('//*[@id="postingbody"]/text()').extract())
        yield{'URL': url, 'Title': title, 'Address':address, 'Description':description}
