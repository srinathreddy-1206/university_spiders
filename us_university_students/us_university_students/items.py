# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Item, Field

class UsUniversityStudentsItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass
    
class ResultsItem(Item):
    result=Field()
    url=Field()
    length=Field()
    
class StudentItem(Item):
    name=Field()
    first_name=Field()
    second_name=Field()
    college=Field()
    dept=Field()
    email=Field()
    mail=Field()
    mailbox=Field()
    voice = Field()
    netid=Field()
    title=Field()
    addr=Field()
    student_id=Field()
        
    
    
