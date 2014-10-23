# -*- coding: utf-8 -*-
from scrapy.contrib.spiders import CrawlSpider
from scrapy.http import Request
from scrapy.selector import Selector
from scrapy.utils.url import urljoin_rfc
from scrapy import Item, Field
import json,string
from us_university_students.items import StudentItem  
import vobject    
    
        

class UniversitySpider(CrawlSpider):
    download_delay=1
    """
    We can use logger to log any messages like errors, debug or even info messages
    """
    name = "yale"
    allowed_domains = ["yale.edu"]
    url="http://www.yale.edu/search/find_people.html"
    query_url="http://directory.yale.edu/phonebook/index.htm?searchString="
    
    xpaths={
    }
    
    def _urljoin(self, response, url):
        """        takes url and response => converts into absolute url    """     
        return urljoin_rfc(response.url, url, response.encoding)            
    def start_requests(self,):
        yield Request(url=self.url,callback=self.search_results,)
    def search_results(self,response):
        combinations=[ '*'+i+j+k+'*'  for i in string.ascii_lowercase for j in string.ascii_lowercase for k in string.ascii_lowercase]
        
        for combination in combinations:
            yield Request(url=self.query_url+combination, callback=self.parse_students,meta={'dont_merge_cookies':True,},dont_filter=True)
            
        
    def join(self,array,delimiter=' '):
        return delimiter.join([element.strip() for element in array]).strip()
            
    def parse_students(self,response):
        sel=Selector(response)
        students_links=sel.xpath('//ul[contains(@class,"indented")]//@href[contains(.,"view")]').extract()
        for link in students_links:
            full_link=self._urljoin(response,link)
            yield Request(url=full_link,callback=self.parse_student,meta={},dont_filter=True)
            
    def parse_student(self,response):
        sel=Selector(response)
        item=MyItem()
        item['name']=self.join(sel.xpath('//div[@id="main"]//div[contains(@class,"inner")]//tr//th[contains(.,"Name:")]//following-sibling::td//text()').extract())
        item['email']= self.join(sel.xpath('//div[@id="main"]//div[contains(@class,"inner")]//tr//th[contains(.,"Email Address:")]//following-sibling::td//text()').extract())
        item['upi']= self.join(sel.xpath('//div[@id="main"]//div[contains(@class,"inner")]//tr//th[contains(.,"UPI:")]//following-sibling::td//text()').extract())
        item['division']= self.join(sel.xpath('//div[@id="main"]//div[contains(@class,"inner")]//tr//th[contains(.,"Division:")]//following-sibling::td//text()').extract())
        item['curriculum']= self.join(sel.xpath('//div[@id="main"]//div[contains(@class,"inner")]//tr//th[contains(.,"Curriculum:")]//following-sibling::td//text()').extract())
        item['curriculum_code']= self.join(sel.xpath('//div[@id="main"]//div[contains(@class,"inner")]//tr//th[contains(.,"Curriculum Code:")]//following-sibling::td//text()').extract())
        item['class_year']= self.join(sel.xpath('//div[@id="main"]//div[contains(@class,"inner")]//tr//th[contains(.,"Class Year:")]//following-sibling::td//text()').extract())
        yield item

class MyItem(Item):
    name=Field()
    email=Field()
    upi=Field()
    division=Field()
    curriculum=Field()
    curriculum_code=Field()
    class_year=Field()