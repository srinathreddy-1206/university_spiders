# -*- coding: utf-8 -*-
from scrapy.contrib.spiders import CrawlSpider
from scrapy.http import Request
from scrapy.selector import Selector
from scrapy.utils.url import urljoin_rfc
from scrapy.http import FormRequest
from scrapy import Item, Field
from scrapy.http import FormRequest
import json,string,vobject,random
from pprint import pprint
class UniversitySpider(CrawlSpider):
    """
    We can use logger to log any messages like errors, debug or even info messages
    """
    name = "virginia"
    allowed_domains = ["virginia.edu"]
    url="http://www.virginia.edu"
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
            yield FormRequest(url="http://www.virginia.edu/cgi-local/ldapweb",
                    formdata={'whitepages':query},
                    callback=self.parse_student_links,meta={'dont_merge_cookies':True})
        #yield FormRequest.from_response(response, formname='moteurRecherche', formdata={'recherche_distance_km_0':'20', 'recherche_type_logement':'9'}, callback=self.parseAnnonces)
    
    def parse_student_links(self,response):
        sel=Selector(response)
        for link in sel.xpath('//table//a/@href[contains(.,"cgi-local")]').extract():
            link=self._urljoin(response,link)
            yield Request(url=link,callback=self.parse_student_info,meta={'dont_merge_cookies':True})

    def parse_student_info(self,response):
        sel=Selector(response)
        item=MyItem()
        item['name']=self.join(sel.xpath('//td[@align="center"]/text()').extract())
        item['id']= self.join(sel.xpath('//td[contains(.,"UVa Computing ID")]/following-sibling::td[1]//text()').extract())
        item['classification']= self.join(sel.xpath('//td[contains(.,"Classification")]/following-sibling::td[1]//text()').extract())
        item['dept'] = self.join(sel.xpath('//td[.="Department"]/following-sibling::td[1]//text()').extract())
        item['dept_code']= self.join(sel.xpath('//td[contains(.,"Department Code")]/following-sibling::td[1]//text()').extract())
        item['primary_email']= self.join(sel.xpath('//td[contains(.,"Primary E-Mail Address")]/following-sibling::td[1]//text()').extract())
        item['office_phone']= self.join(sel.xpath('//td[contains(.,"Office Phone")]/following-sibling::td[1]//text()').extract())
        item['office_address']= self.join(sel.xpath('//td[contains(.,"Office Address")]/following-sibling::td[1]//text()').extract())
        item['reg_email'] =self.join(sel.xpath('//td[contains(.,"Registered E-Mail Address")]/following-sibling::td[1]//text()').extract())
        yield item

class MyItem(Item):
    name=Field()
    id=Field()
    classification=Field()
    dept=Field()
    dept_code=Field()
    primary_email=Field()
    office_phone=Field()
    office_address=Field()
    reg_email=Field()