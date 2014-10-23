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
    
        
class UniversitySpider(CrawlSpider):
    download_delay=1
    """
    We can use logger to log any messages like errors, debug or even info messages
    """
    name = "mit"
    allowed_domains = ["mit.edu"]
    url="http://web.mit.edu/people.html"
    query_url="http://web.mit.edu/bin/cgicso?options=lastnamesx&query="
    output_file_name='mit.csv'
    
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
    
    
    def csv_write(self,opfile="op.csv",row=[]):
        with open(opfile, 'a') as csvfile:
            writer = csv.writer(csvfile, delimiter=',',quotechar='"', quoting=csv.QUOTE_ALL)
            writer.writerow(row)

    def _urljoin(self, response, url):
        """        takes url and response => converts into absolute url    """     
        return urljoin_rfc(response.url, url, response.encoding)            
    def join(self,array,delimiter=' '):
        return delimiter.join([element.strip() for element in array])
    
    def start_requests(self,):
        self.csv_write(opfile=self.output_file_name,row=['info',])
        yield Request(url=self.url,callback=self.search_results,)
    
    def search_results(self,response):
        combinations=[ i+j for i in string.ascii_lowercase for j in string.ascii_lowercase]
        for combination in combinations:
            yield Request(url=self.query_url+combination, callback=self.parse_students,meta={'combination':combination,'dont_merge_cookies':True},)
            
            
    def parse_students(self,response):
        sel=Selector(response)    
        results=sel.xpath('//td[@class="dir"]//@href').extract()
        for result in results:
            yield Request(url=self._urljoin(response,result),callback=self.parse_student_info,meta={'dont_merge_cookies':True})
            
    def parse_student_info(self,response):
        sel=Selector(response)
        item=MyItem()
        item['val']=self.join(sel.xpath('//td[@class="dir"]').extract())
        yield item
class MyItem(Item):
    val=Field()
