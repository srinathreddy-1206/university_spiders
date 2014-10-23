# -*- coding: utf-8 -*-
from scrapy.contrib.spiders import CrawlSpider
from scrapy.http import Request
from scrapy.selector import Selector
from scrapy.utils.url import urljoin_rfc
from scrapy import Item, Field
import json,string
class UniversitySpider(CrawlSpider):
    """
    We can use logger to log any messages like errors, debug or even info messages
    """
    name = "wisc_edu"
    allowed_domains = ["wisc.edu"]
    url="http://www.wisc.edu/directories/?q=ryanz*"
    def _urljoin(self, response, url):
        """        takes url and response => converts into absolute url    """     
        return urljoin_rfc(response.url, url, response.encoding)            
    def join(self,elements,delimiter=' '):
        return delimiter.join([element.strip() for element in elements]).strip()
    def start_requests(self,):
        yield Request(url=self.url,callback=self.make_queries,meta={'dont_merge_cookies':True})
    def make_combinations(self):
        combinations=[ i.strip()+j.strip()+k.strip() for i in ' '+string.ascii_lowercase for j in ' '+string.ascii_lowercase for k in ' '+string.ascii_lowercase]
        return combinations
    def make_queries(self,response):
        sel=Selector(response)
        combinations=self.make_combinations()
        for combination in combinations:
            url="http://www.wisc.edu/directories/?q="+combination+"*"
            yield Request(url=url,callback=self.parse_student_info,meta={'dont_merge_cookies':True})
    def parse_student_info(self,response):
        sel=Selector(response)
        persons=sel.xpath('//div[@class="person"]')
        for person in persons:
            item=MyItem()
            item['name']= self.join(person.xpath('.//div[@class="person_name"]//text()').extract())
            item['phone']= self.join(person.xpath('.//div[@class="person_phone"]//text()').extract())
            item['email']= self.join(person.xpath('.//div[@class="person_email"]//text()').extract())
            url=person.xpath('.//div[@class="person_more"]//@href').extract()
            if url:
                yield Request(url=self._urljoin(response,url[0]),callback=self.parse_more_info,meta={'dont_merge_cookies':True,'item':item})
            else:
                yield item
    def parse_more_info(self,response):
        sel=Selector(response)
        item=response.meta['item']
        item['title']=self.join(sel.xpath('//div[@class="person_title_division"]//text()').extract())
        item['department']=self.join(sel.xpath('//div[@class="person_title_department"]//text()').extract())
        item['sub_department']=self.join(sel.xpath('//div[@class="person_title_subdepartment"]//text()').extract())
        item['address']=self.join(sel.xpath('//div[@class="person_address_room"]//text()').extract(),',')
        yield item
class MyItem(Item):
    name=Field()
    email=Field()
    phone=Field()
    title=Field()
    department=Field()
    sub_department=Field()
    address=Field()


