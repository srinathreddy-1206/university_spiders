# -*- coding: utf-8 -*-
from scrapy.contrib.spiders import CrawlSpider
from scrapy.http import Request
from scrapy.selector import Selector
from scrapy.utils.url import urljoin_rfc
from scrapy import Item, Field
from scrapy.http import FormRequest
import json,string
class UniversitySpider(CrawlSpider):
    """
    We can use logger to log any messages like errors, debug or even info messages
    """
    name = "umich"
    allowed_domains = ["umich.edu"]
    url="https://mcommunity.umich.edu/#search/"
    def _urljoin(self, response, url):
        """        takes url and response => converts into absolute url    """     
        return urljoin_rfc(response.url, url, response.encoding)            
    def start_requests(self,):
        yield Request(url=self.url,callback=self.make_queries,)
    def make_queries(self,response):
        for i in string.lowercase:
            for j in string.lowercase:
                for k in string.lowercase:
                    yield FormRequest(url="https://mcommunity.umich.edu/mcPeopleService/people/search",method="POST",formdata={'searchCriteria':i+j+k},callback=self.parse_results)        


    def parse_results(self,response):
        json_info=json.loads(response.body)
        for i in json_info['person']:
            item=MyItem()
            item['email']=i.get('email',None)
            item['name']=i.get('displayName',None)
            item['affiliation']=i.get('affiliation',None)
            item['title']=i.get('title',None)
            item['id']=i.get('uniqname',None) 
            yield item
class MyItem(Item):
    name=Field()
    email=Field()
    affiliation=Field()
    title=Field()
    id=Field()
