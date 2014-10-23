# -*- coding: utf-8 -*-
from scrapy.contrib.spiders import CrawlSpider
from scrapy.http import Request
from scrapy.http import FormRequest
from scrapy.selector import Selector
from scrapy.utils.url import urljoin_rfc
from scrapy import Item, Field
import json,string
from us_university_students.items import StudentItem  
import vobject    
import csv
import csv,codecs,cStringIO
import urllib
class MyItem(Item):
    name=Field()
    phone=Field()
    email=Field()
import string        
class UniversitySpider(CrawlSpider):
    download_delay=0
    """
    We can use logger to log any messages like errors, debug or even info messages
    """
    name = "washington"
    allowed_domains = ["washington.edu"]
    url="https://www.washington.edu/home/peopledir/"
    
    def _urljoin(self, response, url):
        """        takes url and response => converts into absolute url    """     
        return urljoin_rfc(response.url, url, response.encoding)            
    def join(self,array,delimiter=' '):
        return delimiter.join([element.strip() for element in array])
    
    def start_requests(self,):
        yield Request(url=self.url,callback=self.make_combinations,)
    
    def make_combinations(self,response):
        combinations=[ i+j for i in string.ascii_lowercase for j in string.ascii_lowercase]
        for combination in combinations:
            payload = {"length": "sum", "method": "name",'term':combination,'whichdir':"student"}
            print payload
            yield FormRequest.from_response(response,
                                        formname='dirform',
                                        formdata=payload,
                                        callback=self.parse_student_info,dont_filter=True)
            
            

    def parse_student_links(self,response):
        sel=Selector(response)
        forms=sel.xpath('//form[@class="vcard"]')
        for form in forms:
            action_url=form.xpath('./@action').extract()
            if action_url:
                action_url=self._urljoin(response,action_url[0])
                keys=form.xpath('.//input/@name').extract() 
                form_data={}
                for key in keys:
                    key_xpath='.//input[@name="%s"]/@value'.format(key)
                    form_data[key]=self.join(sel.xpath(key_xpath).extract())
                print form_data

    def parse_student_info(self,response):
        sel=Selector(response)
        rows=sel.xpath('//table[contains(@class,"table-striped")]//tr[not(contains(//td,"colspan"))]')
        for row in rows:
            item=MyItem()
            item['name'] =self.join(row.select('.//td[1]//text()').extract())
            item['phone']= self.join(row.select('.//td[2]//text()').extract())
            item['email']=self.join(row.select('.//td[3]//text()').extract())
            yield item
    def parse_vcf(self,response):
         v=vobject.readOne(response.body)
         print v
         item=response.meta['item']
         item['first_name']=v.n.value.given.strip()
         item['second_name']=v.n.value.family.strip()
         yield item
