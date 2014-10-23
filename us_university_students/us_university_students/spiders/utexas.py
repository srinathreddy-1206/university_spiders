# -*- coding: utf-8 -*-
from scrapy.contrib.spiders import CrawlSpider
from scrapy.http import Request
from scrapy.selector import Selector
from scrapy.utils.url import urljoin_rfc
from scrapy import Item, Field
import json,string
from us_university_students.items import StudentItem  
import vobject    
import csv
import csv,codecs,cStringIO

class MyItem(Item):
    name=Field()
    email=Field()
    school=Field()
    major=Field()
    classification=Field()
    job_title=Field()
    department=Field()
    office_phone=Field()
    office_location=Field()
    office_address=Field()
    campus_mail_code=Field()
    home_phone=Field()
    home_address=Field()    

import string        
class UniversitySpider(CrawlSpider):
    download_delay=2
    """
    We can use logger to log any messages like errors, debug or even info messages
    """
    name = "utexas"
    allowed_domains = ["utexas.edu"]
    url="http://www.utexas.edu/directory/index.php"
    op_file="utexas.csv"
    query_url="http://www.utexas.edu/directory/index.php?scope=student&submit=Search&q="

    def _urljoin(self, response, url):
        """        takes url and response => converts into absolute url    """     
        return urljoin_rfc(response.url, url, response.encoding)            
    def join(self,array,delimiter=' '):
        return delimiter.join([element.strip() for element in array])
    
    def start_requests(self,):
        yield Request(url=self.url,callback=self.make_combinations,)
    
    def make_combinations(self,response):
        combinations=[ i.strip()+j.strip()+k.strip() for i in ' '+string.ascii_lowercase for j in ' '+string.ascii_lowercase for k in ' '+string.ascii_lowercase]
        for combination in combinations:
            yield Request(url=self.query_url+combination, callback=self.parse_student_links,meta={'dont_merge_cookies':False})
            #break
    def parse_student_links(self,response):
        sel=Selector(response)
        links=sel.xpath('//div[@id="results"]//div[contains(@id,"moreinfo")]//@href').extract()
        for link in links:
            yield Request(url=self._urljoin(response,link),callback=self.parse_student_info,meta={})
    def parse_student_info(self,response):
        sel=Selector(response)
        item=MyItem()
        item['name']=self.join(sel.xpath('//div[@id="results"]//tr//td[contains(.,"Name")]//following-sibling::td//text()').extract())
        item['email']=self.join(sel.xpath('//div[@id="results"]//tr//td[contains(.,"Email")]//following-sibling::td//text()').extract())
        item['school']=self.join(sel.xpath('//div[@id="results"]//tr//td[contains(.,"School/College")]//following-sibling::td//text()').extract())                
        item['major']=self.join(sel.xpath('//div[@id="results"]//tr//td[contains(.,"Major")]//following-sibling::td//text()').extract())
        item['classification']=self.join(sel.xpath('//div[@id="results"]//tr//td[contains(.,"Classification")]//following-sibling::td//text()').extract())        


        item['job_title']=self.join(sel.xpath('//div[@id="results"]//tr//td[contains(.,"Job Title")]//following-sibling::td//text()').extract())
        item['department']=self.join(sel.xpath('//div[@id="results"]//tr//td[contains(.,"Department")]//following-sibling::td//text()').extract())
        item['office_phone']=self.join(sel.xpath('//div[@id="results"]//tr//td[contains(.,"Office Phone:")]//following-sibling::td//text()').extract())
        item['office_location']=self.join(sel.xpath('//div[@id="results"]//tr//td[contains(.,"Office Location")]//following-sibling::td//text()').extract())
        item['office_address']=self.join(sel.xpath('//div[@id="results"]//tr//td[contains(.,"Office Address")]//following-sibling::td//text()').extract())
  
        item['campus_mail_code']=self.join(sel.xpath('//div[@id="results"]//tr//td[contains(.,"Campus Mail Code")]//following-sibling::td//text()').extract())
        item['home_phone']=self.join(sel.xpath('//div[@id="results"]//tr//td[contains(.,"Home Phone")]//following-sibling::td//text()').extract())
        item['home_address']=self.join(sel.xpath('//div[@id="results"]//tr//td[contains(.,"Home Address")]//following-sibling::td//text()').extract())
        yield item
        """                                 
        vcf=sel.xpath('//div[@id="results"]//tr//td[contains(.,"Business Card")]//following-sibling::td//@href').extract()
        if vcf:
            url=self._urljoin(response,vcf[0])
            yield Request(url=url,callback=self.parse_vcf,meta={'dont_merge_cookies':True,'item':item})
        else:
            yield item
        """
    def parse_vcf(self,response):
         v=vobject.readOne(response.body)
         print v
         item=response.meta['item']
         item['first_name']=v.n.value.given.strip()
         item['second_name']=v.n.value.family.strip()
         yield item
