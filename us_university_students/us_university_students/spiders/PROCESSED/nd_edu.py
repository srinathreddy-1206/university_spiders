# -*- coding: utf-8 -*-
from scrapy.contrib.spiders import CrawlSpider
from scrapy.http import Request
from scrapy.selector import Selector
from scrapy.utils.url import urljoin_rfc
from scrapy import Item, Field
import json,string
class MyItem(Item):
    result=Field()
    url=Field()
    length=Field()
class StudentItem(Item):
    profile_name=Field()
    display_name=Field()
    given_name=Field()
    family_name=Field()
    phone=Field()
    fax=Field()
    netid=Field()
    searchguide=Field()
    email=Field()
    affiliation=Field()
    home_address=Field()
    postal_address=Field()

class UniversitySpider(CrawlSpider):
    """
    We can use logger to log any messages like errors, debug or even info messages
    """
    name = "nd_edu"
    allowed_domains = ["nd.edu"]
    url="https://apps.nd.edu/webdirectory/directory.cfm?specificity=contains&cn=aaa&Submit=Submit"
    def _urljoin(self, response, url):
        """        takes url and response => converts into absolute url    """     
        return urljoin_rfc(response.url, url, response.encoding)            
    def start_requests(self,):
        yield Request(url=self.url,callback=self.make_queries,)
    def make_queries(self,response):
        for i in " "+string.ascii_lowercase:
            for j in " "+string.ascii_lowercase:
                for k in " "+string.ascii_lowercase:
                    s=(i.strip()+j.strip()+k.strip()).strip()
                    url="https://apps.nd.edu/webdirectory/directory.cfm?specificity=contains&cn="+s+"&Submit=Submit"          
                    yield Request(url=url,callback=self.parse_student_results,meta={'dont_merge_cookies':True})
        #"https://apps.nd.edu/webdirectory/directory.cfm?specificity=contains&cn=aaa&Submit=Submit"
    def join(self,elements_list,delimiter=' '):
        return delimiter.join([element.strip() for element in elements_list]).strip()
    def parse_student_results(self,response):
        sel=Selector(response)
        links= sel.xpath('//td[contains(@class,"arial")]//i[contains(.,"Student")]/preceding::a[1]//@href').extract()
        for link in links:
            link=self._urljoin(response,link)
            print link
            yield Request(url=link,callback=self.parse_student_info_url,meta={'dont_merge_cookies':True})
    def parse_student_info_url(self,response):
        sel=Selector(response)
        for link in sel.xpath('//td[contains(@class,"arial")]//a[contains(.,"More Info")]/@href').extract():
            yield Request(url=self._urljoin(response,link),callback=self.parse_student_info,meta={'dont_merge_cookies':True})

    def parse_student_info(self,response):
        sel=Selector(response)
        item=StudentItem()
        item['profile_name']= self.join(sel.xpath('//font[@size="+1"]//text()').extract())
        item['display_name']=self.join(sel.xpath('//table[2]//td[1][contains(.,"Display")]/following-sibling::td[1]//text()').extract())
        item['given_name']=self.join(sel.xpath('//table[2]//td[1][contains(.,"Given Name")]/following-sibling::td[1]//text()').extract())
        
        item['family_name']=self.join(sel.xpath('//table[2]//td[1][contains(.,"Family Name")]/following-sibling::td[1]//text()').extract())
        item['phone']= self.join(sel.xpath('//table[2]//td[contains(.,"Phone")]/following-sibling::td[1]//text()').extract())
        item['fax']= self.join(sel.xpath('///table[2]//td[contains(.,"Fax")]/following-sibling::td[1]//text()').extract())
        item['netid']= self.join(sel.xpath('//table[2]//td[contains(.,"NetID")]/following-sibling::td[1]//text()').extract())


        item['searchguide']= self.join(sel.xpath('//table[2]//td[contains(.,"Searchguide")]/following-sibling::td[1]//text()').extract())
        item['email']= self.join(sel.xpath('//table[2]//td[contains(.,"Email Address")]/following-sibling::td[1]//text()').extract())
        
        item['affiliation']= self.join(sel.xpath('//table//td[contains(.,"Affiliation")]/following-sibling::td[1]//text()').extract(),',')
    
        item['home_address']=self.join(sel.xpath('//table//td[contains(.,"Home Address")]/following-sibling::td[1]//text()').extract())
        item['postal_address']=self.join(sel.xpath('//table//td[contains(.,"Postal Address")]/following-sibling::td[1]//text()').extract())
        yield item