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
    """
    We can use logger to log any messages like errors, debug or even info messages
    """
    name = "princeton"
    allowed_domains = ["princeton.edu"]
    url="http://search.princeton.edu/"
    query_url="http://search.princeton.edu/search?f="
    
    xpaths={
    'pagination':'//div[@class="results-nav"]//@href',
    
    'students_blocks':'//div[contains(@class,"entry")]',
    'name':'.//span[@class="field"]//span[contains(@class,"key") and contains(translate(.,"ABCDEFGHIJKLMNOPQRSTUVWXYZ","abcdefghijklmnopqrstuvwxyz"),"name")]/following-sibling::span[contains(@class,"value")]//text()',
    
    'college':'.//span[@class="field"]//span[contains(@class,"key") and contains(translate(.,"ABCDEFGHIJKLMNOPQRSTUVWXYZ","abcdefghijklmnopqrstuvwxyz"),"college")]/following-sibling::span[contains(@class,"value")]//text()',
    
    'dept':'.//span[@class="field"]//span[contains(@class,"key") and contains(translate(.,"ABCDEFGHIJKLMNOPQRSTUVWXYZ","abcdefghijklmnopqrstuvwxyz"),"dept")]/following-sibling::span[contains(@class,"value")]//text()',
    
    'e-mail':'.//span[@class="field"]//span[contains(@class,"key") and contains(translate(.,"ABCDEFGHIJKLMNOPQRSTUVWXYZ-","abcdefghijklmnopqrstuvwxyz-"),"e-mail")]/following-sibling::span[contains(@class,"value")]//text()',
    
    'mail':'.//span[@class="field"]//span[contains(@class,"key") and translate(.,"ABCDEFGHIJKLMNOPQRSTUVWXYZ","abcdefghijklmnopqrstuvwxyz")="mail:"]/following-sibling::span[contains(@class,"value")]//text()',
    
    'mailbox':'.//span[@class="field"]//span[contains(@class,"key") and contains(translate(.,"ABCDEFGHIJKLMNOPQRSTUVWXYZ","abcdefghijklmnopqrstuvwxyz"),"mailbox")]/following-sibling::span[contains(@class,"value")]//text()',
    
    'voice':'.//span[@class="field"]//span[contains(@class,"key") and contains(translate(.,"ABCDEFGHIJKLMNOPQRSTUVWXYZ","abcdefghijklmnopqrstuvwxyz"),"voice")]/following-sibling::span[contains(@class,"value")]//text()',

    'netid':'.//span[@class="field"]//span[contains(@class,"key") and contains(translate(.,"ABCDEFGHIJKLMNOPQRSTUVWXYZ","abcdefghijklmnopqrstuvwxyz"),"netid")]/following-sibling::span[contains(@class,"value")]//text()',

    'title':'.//span[@class="field"]//span[contains(@class,"key") and contains(translate(.,"ABCDEFGHIJKLMNOPQRSTUVWXYZ","abcdefghijklmnopqrstuvwxyz"),"title")]/following-sibling::span[contains(@class,"value")]//text()',

    'addr':'.//span[@class="field"]//span[contains(@class,"key") and contains(translate(.,"ABCDEFGHIJKLMNOPQRSTUVWXYZ","abcdefghijklmnopqrstuvwxyz"),"addr")]/following-sibling::span[contains(@class,"value")]//text()',    

    'id':'.//span[@class="field"]//span[contains(@class,"key") and contains(translate(.,"ABCDEFGHIJKLMNOPQRSTUVWXYZ","abcdefghijklmnopqrstuvwxyz"),"id #:")]/following-sibling::span[contains(@class,"value")]//text()',

    'v-card':'.//div[contains(@class,"vcard")]//@href',
    }
    
    def _urljoin(self, response, url):
        """        takes url and response => converts into absolute url    """     
        return urljoin_rfc(response.url, url, response.encoding)            
    def start_requests(self,):
        yield Request(url=self.url,callback=self.search_results,)
    def search_results(self,response):
        combinations=[ i+j for i in string.ascii_lowercase for j in string.ascii_lowercase]
        for combination in combinations:
            yield Request(url=self.query_url+combination, callback=self.parse_students,)
            
    def join(self,array):
        return ' '.join([element.strip() for element in array])
            
    def parse_students(self,response):
        sel=Selector(response)    
        students=sel.xpath(self.xpaths['students_blocks'])
        name=Field()
    
        paging_links=sel.xpath(self.xpaths['pagination']).extract()
        for link in paging_links:
            yield Request(url=self._urljoin(response,link),callback=self.parse_students)
        for student in students:
            item=StudentItem()
            item['name']=self.join(student.xpath(self.xpaths['name']).extract())
            item['college']=self.join(student.xpath(self.xpaths['college']).extract())
            item['dept']=self.join(student.xpath(self.xpaths['dept']).extract())
            item['email']=self.join(student.xpath(self.xpaths['e-mail']).extract())           
            item['mail']=self.join(student.xpath(self.xpaths['mail']).extract())  
            item['mailbox']=self.join(student.xpath(self.xpaths['mailbox']).extract())                       
            item['voice']=self.join(student.xpath(self.xpaths['voice']).extract()) 
            item['netid']=self.join(student.xpath(self.xpaths['netid']).extract())                       
            item['title']=self.join(student.xpath(self.xpaths['title']).extract()) 
            item['addr']=self.join(student.xpath(self.xpaths['addr']).extract())                                               
            item['student_id']=self.join(student.xpath(self.xpaths['id']).extract())                                               
            yield item
    def parse_v_card(self,response):
         v=vobject.readOne(response.body)
         item=response.meta['item']
         item['first_name']=v.n.value.given.strip()
         item['second_name']=v.n.value.family.strip()
         yield item
                                                                                                
                                                                             
                       
