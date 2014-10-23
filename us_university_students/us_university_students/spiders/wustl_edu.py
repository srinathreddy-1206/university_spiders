# -*- coding: utf-8 -*-
from scrapy.contrib.spiders import CrawlSpider
from scrapy.http import Request
from scrapy.selector import Selector
from scrapy.utils.url import urljoin_rfc
from scrapy import Item, Field
import json,string
class MyItem(Item):
    result=Field()
    url=Field()
    length=Field()

class UniversitySpider(CrawlSpider):
    """
    We can use logger to log any messages like errors, debug or even info messages
    """
    name = "wustl"
    allowed_domains = ["wustl.edu"]
    url="http://search.princeton.edu/"
    def _urljoin(self, response, url):
        """        takes url and response => converts into absolute url    """     
        return urljoin_rfc(response.url, url, response.encoding)            
    def start_requests(self,):
        yield Request(url=self.url,callback=self.parse_students,)
    
