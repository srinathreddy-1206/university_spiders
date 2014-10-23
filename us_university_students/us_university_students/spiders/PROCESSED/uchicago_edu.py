# -*- coding: utf-8 -*-
from scrapy.contrib.spiders import CrawlSpider
from scrapy.http import Request
from scrapy.selector import Selector
from scrapy.utils.url import urljoin_rfc
from scrapy import Item, Field
import json,string,vobject
from pprint import pprint
class MyItem(Item):
    name=Field()
    affiliation=Field()
    title=Field()
    dept=Field()
    email=Field()
    phone=Field()
    first_name=Field()
    last_name=Field()
class UniversitySpider(CrawlSpider):
    """
    We can use logger to log any messages like errors, debug or even info messages
    """
    name = "uchicago_edu"
    allowed_domains = ["uchicago.edu"]
    url="https://directory.uchicago.edu/individuals/results?utf8=%E2%9C%93&name=aa*&organization=&cnetid="
    def _urljoin(self, response, url):
        """        takes url and response => converts into absolute url    """     
        return urljoin_rfc(response.url, url, response.encoding)            
    
    def join(self,elements,delimiter=' '):
        return delimiter.join([element.strip() for element in elements]).strip()
    def start_requests(self,):


        yield Request(url=self.url,callback=self.make_queries,)
    def make_queries(self,response):
        sel=Selector(response)
        for i in ' '+string.lowercase:
            for j in ' '+string.lowercase:
                for k in ' '+string.lowercase:
                    query= (i.strip()+j.strip()+k.strip()).strip()+'*'
                    url= 'https://directory.uchicago.edu/individuals/results?utf8=%E2%9C%93&name='+query+'&organization=&cnetid='
                    yield Request(url=url,callback=self.parse_student_links,meta={'dont_merge_cookies':True})
    def parse_student_links(self,response):
        sel=Selector(response)
        for link in sel.xpath('//td[contains(@class,"person")]//a/@href').extract():
            yield Request(url=self._urljoin(response,link),callback=self.parse_student_info,meta={'dont_merge_cookies':True})
    def parse_student_info(self,response):
        sel=Selector(response)
        item=MyItem()
        item['name']=self.join(sel.xpath('//h1[contains(@id,"page-title")]//text()').extract())
        item['affiliation']= self.join(sel.xpath('//table//tr[contains(.,"Affiliation")]//td//text()').extract())
        item['title']= self.join(sel.xpath('//table//tr[contains(.,"Title")]//td//text()').extract())
        item['dept']= self.join(sel.xpath('//table//tr[contains(.,"Department")]//td//text()').extract())
        item['email']= self.join(sel.xpath('//table//tr[contains(.,"Email")]//td//text()').extract())
        item['phone']= self.join(sel.xpath('//table//tr[contains(.,"Phone")]//td//text()').extract())
        item['first_name'],item['last_name']='',''
        vcard=sel.xpath('//tr[contains(.,"VCard")]//a[contains(@href,".vcard")]//@href').extract()
        if vcard:
            link=self._urljoin(response,vcard[0])
            yield Request(url=link,callback=self.parse_vcard_info,meta={'dont_merge_cookies':True,'item':item})
        else:
            yield item
            pass
    def parse_vcard_info(self,response):
         item=response.meta['item']
         v=vobject.readOne(response.body)
         item['first_name']=v.n.value.given.strip()
         item['last_name']=v.n.value.family.strip()
         yield item