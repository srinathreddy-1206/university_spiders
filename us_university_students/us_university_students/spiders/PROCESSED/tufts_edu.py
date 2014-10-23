# -*- coding: utf-8 -*-
from scrapy.contrib.spiders import CrawlSpider
from scrapy.http import Request
from scrapy.selector import Selector
from scrapy.utils.url import urljoin_rfc
from scrapy.http import FormRequest
from scrapy import Item, Field
import json,string,vobject,random
from pprint import pprint
class MyItem(Item):
    name=Field()
    college=Field()
    major=Field()
    class_year=Field()
    phone=Field()
    email=Field()
    primary_affiliation=Field()
class UniversitySpider(CrawlSpider):
    """
    We can use logger to log any messages like errors, debug or even info messages
    """
    name = "tufts_edu"
    allowed_domains = ["tufts.edu"]
    url="http://directory.tufts.edu/searchresults.cgi"
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
        for query in queries:
            yield FormRequest.from_response(response, formname='search', formdata={'search':str(query), 'type':'Students','x':str(random.randint(0,10)),'y':str(random.randint(0,10))}, callback=self.parse_links,meta={'dont_merge_cookies':True})
    def parse_links(self,response):
        sel=Selector(response)
        for link in sel.xpath('//td//a/@href').extract():
            link=self._urljoin(response,link)
            #print link
            yield Request(url=link,callback=self.parse_student_info,meta={'dont_merge_cookies':True})

    def parse_student_info(self,response):
        sel=Selector(response)
        item=MyItem()
        item['name'] =self.join(sel.xpath('//td[contains(.,"Name:")]/following-sibling::td//text()').extract())
        item['college']= self.join(sel.xpath('//td[contains(.,"College:")]/following-sibling::td//text()').extract())
        item['major'] =self.join(sel.xpath('//td[contains(.,"Major:")]/following-sibling::td//text()').extract())
        item['class_year'] = self.join(sel.xpath('//td[contains(.,"Class Year:")]/following-sibling::td//text()').extract())
        item['phone'] = self.join(sel.xpath('//td[contains(.,"Phone:")]/following-sibling::td//text()').extract())
        item['email'] = self.join(sel.xpath('//td[contains(.,"Email Address:")]/following-sibling::td//text()').extract())
        item['primary_affiliation'] = self.join(sel.xpath('//td[contains(.,"Primary Affiliation:")]/following-sibling::td//text()').extract())
        yield item