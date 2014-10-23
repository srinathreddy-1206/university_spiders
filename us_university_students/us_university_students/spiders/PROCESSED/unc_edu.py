# -*- coding: utf-8 -*-
from scrapy.contrib.spiders import CrawlSpider
from scrapy.http import Request
from scrapy.selector import Selector
from scrapy.utils.url import urljoin_rfc
from scrapy import Item, Field
from scrapy.http import FormRequest
import json,string
class UniversitySpider(CrawlSpider):
    """
    We can use logger to log any messages like errors, debug or even info messages
    """
    name = "unc"
    allowed_domains = ["unc.edu"]
    url="https://itsapps.unc.edu/dir/dirSearch/view.htm"
    def _urljoin(self, response, url):
        """        takes url and response => converts into absolute url    """     
        return urljoin_rfc(response.url, url, response.encoding)            
    def start_requests(self,):
        yield Request(url=self.url,callback=self.make_queries,)
    def make_queries(self,response):
        for i in string.lowercase:
            for j in string.lowercase:
                headers={'X-Requested-With':'XMLHttpRequest',}
                formdata={"affiliation":"student","email":"","firstname":i+j,"lastname":'',"onyen":"","pid":""}
                yield FormRequest(url="https://itsapps.unc.edu/dir/dirSearch/search",method="POST",formdata=formdata,callback=self.parse_results,headers=headers)        
                
    def parse_results(self,response):
        json_info=json.loads(response.body)
        for i in json_info: 
            item=MyItem()
            item['disp_name']=i.get('uncReverseDisplayName',None)
            item['telephone']=i.get('telephoneNumber',None)
            item['nickname']=i.get('eduPersonNickname',None)
            item['preffered_surname']=i.get('uncPreferredSurname',None)
            item['surname']=i.get('sn',None)
            item['id']=i.get('spid',None)
            item['mail']=i.get('mail',None)
            item['name']=i.get('givenName',None)
            yield item
class MyItem(Item):
    name=Field()
    disp_name=Field()
    telephone=Field()
    nickname=Field()
    preffered_surname=Field()
    surname=Field()
    id=Field()
    mail=Field()
        