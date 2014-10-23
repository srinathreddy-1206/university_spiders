from scrapy.contrib.spiders import CrawlSpider
from scrapy.selector import HtmlXPathSelector
from scrapy.http import Request

class whatIsMySpider(CrawlSpider):
    url="http://ipecho.net/plain"
    allowed_domains=['ipecho.net']
    name="ipaddress"
    def start_requests(self): 
        """
            crawl the first/starting url
        """
        yield Request(self.url,callback=self.parse_ip_address,meta={'dont_merge_cookies':True,},dont_filter=True)
    def parse_ip_address(self,response):
        hxs=HtmlXPathSelector(response)
        print hxs.select('//body//text()').extract()
        print response.request.headers
