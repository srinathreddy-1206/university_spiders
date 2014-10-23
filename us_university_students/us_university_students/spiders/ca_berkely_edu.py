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
    name = "ca_berkely"
    allowed_domains = ["berkeley.edu"]
    url="https://calnet.berkeley.edu"
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
        yield Request(url=self.url,callback=self.parse_make_queries,meta={'dont_merge_cookies':True})
    
    def parse_make_queries(self,response):
        queries=self.make_queries()
        for query in queries:
            url="https://calnet.berkeley.edu/directory/search.pl?search-type=lastfirst&search-base=student&search-term="+query+"&search=Search"
            yield Request(url=url,callback=self.parse_student_links,meta={'dont_merge_cookies':True})
    def parse_student_links(self,response):
        sel=Selector(response)
        for link in sel.xpath('//div[@id="content"]//a[@class="underline"]/@href').extract():
            link=self._urljoin(response,link)
            yield Request(url=link,callback=self.parse_student_info,meta={'dont_merge_cookies':True})
    def parse_student_info(self,response):
        sel=Selector(response)
        item=MyItem()
        item['name']=self.join(sel.xpath('//div[@id="content"]//span[contains(@class,"attribute")][contains(.,"Name:")]/following-sibling::span[1]//text()').extract())
        item['home_dept']= self.join(sel.xpath('//div[@id="content"]//span[contains(@class,"attribute")][contains(.,"Home Department:")]/following-sibling::span[1]//text()').extract())
        item['email']= self.join(sel.xpath('//div[@id="content"]//span[contains(@class,"attribute")][contains(.,"Email:")]/following-sibling::span[1]//text()').extract())
        item['phone']= self.join(sel.xpath('//div[@id="content"]//span[contains(@class,"attribute")][contains(.,"Phone:")]/following-sibling::span[1]//text()').extract())
        item['address_desc']= self.join(sel.xpath('//div[@id="content"]//span[contains(@class,"attribute")][contains(.,"Address Description")]/following-sibling::span[1]//text()').extract())
        item['street']= self.join(sel.xpath('//div[@id="content"]//span[contains(@class,"attribute")][contains(.,"Street, Room")]/following-sibling::span[1]//text()').extract())
        item['city']= self.join(sel.xpath('//div[@id="content"]//span[contains(@class,"attribute")][contains(.,"City:")]/following-sibling::span[1]//text()').extract())
        item['state']= self.join(sel.xpath('//div[@id="content"]//span[contains(@class,"attribute")][contains(.,"State:")]/following-sibling::span[1]//text()').extract())
        item['postal_code']= self.join(sel.xpath('//div[@id="content"]//span[contains(@class,"attribute")][contains(.,"Postal Code:")]/following-sibling::span[1]//text()').extract())
        item['mail_code']= self.join(sel.xpath('//div[@id="content"]//span[contains(@class,"attribute")][contains(.,"Mail Code:")]/following-sibling::span[1]//text()').extract())
        item['dept_name']= self.join(sel.xpath('//div[@id="content"]//span[contains(@class,"attribute")][contains(.,"Department Name:")]/following-sibling::span[1]//text()').extract())
        item['title']= self.join(sel.xpath('//div[@id="content"]//span[contains(@class,"attribute")][contains(.,"Title:")]/following-sibling::span[1]//text()').extract())
        yield item
        #print self.join(sel.xpath('').extract())
        #print self.join(sel.xpath('').extract())
        #print self.join(sel.xpath('').extract())
class MyItem(Item):
    name=Field()
    home_dept=Field()
    email=Field()
    phone=Field()
    address_desc=Field()
    street=Field()
    city=Field()
    state=Field()
    postal_code=Field()
    mail_code=Field()
    dept_name=Field()
    title=Field()