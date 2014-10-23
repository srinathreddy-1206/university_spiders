# -*- coding: utf-8 -*-
from scrapy.contrib.spiders import CrawlSpider
from scrapy.http import Request
from scrapy.selector import Selector
from scrapy.utils.url import urljoin_rfc
from scrapy.http import FormRequest
from scrapy import Item, Field
import json,string,vobject,random
from pprint import pprint
class UniversitySpider(CrawlSpider):
    """
    We can use logger to log any messages like errors, debug or even info messages
    """
    name = "cornell"
    allowed_domains = ["cornell.edu"]
    url="https://www.cornell.edu"
    def _urljoin(self, response, url):
        """        takes url and response => converts into absolute url    """     
        return urljoin_rfc(response.url, url, response.encoding)           
    def join(self,elements,delimiter=' '):
        return delimiter.join([element.strip() for element in elements]).strip()

    def make_queries(self,):
        queries=[]
        for i in ' '+string.lowercase:
            for j in ' '+string.lowercase:
                for k in ' '+string.lowercase:
                    queries.append((i.strip()+j.strip()+k.strip()).strip())
        return queries
                    
    
    def start_requests(self,):
        yield Request(url=self.url,callback=self.search_students)
    
    def search_students(self,response):
        sel=Selector(response)
        queries=self.make_queries()
        for query in self.make_queries():
            url='https://www.cornell.edu/search/people.cfm?q='+query
            yield Request(url=url,callback=self.parse_links,meta={'dont_merge_cookies':True})    
    def parse_links(self,response):
        sel=Selector(response)
        for link in sel.xpath('//a[contains(@name,"Student")]/ancestor::table//td[contains(@class,"name")]//a/@href').extract():
            link=self._urljoin(response,link)
            print link
            yield Request(url=link,callback=self.parse_student_info,meta={'dont_merge_cookies':True})
        
    def parse_student_info(self,response):
        sel=Selector(response)
        item=MyItem()
        item['name']= self.join(sel.xpath('//div[contains(@id,"peoplename")]//h3//text()').extract())
        item['type']= self.join(sel.xpath('//div[contains(@id,"peopleprofile")]//th[.="TYPE:"]/following-sibling::td//text()').extract())
        item['netid']= self.join(sel.xpath('//div[contains(@id,"peopleprofile")]//th[.="NETID:"]/following-sibling::td//text()').extract())
        item['email']= self.join(sel.xpath('//div[contains(@id,"peopleprofile")]//th[.="EMAIL:"]/following-sibling::td//text()').extract())
        item['mobile']= self.join(sel.xpath('//div[contains(@id,"phone-block")]//th[contains(.,"MOBILE:")]/following-sibling::td//text()').extract())
        yield item
class MyItem(Item):
    name=Field()
    type=Field()
    netid=Field()
    email=Field()
    mobile=Field()