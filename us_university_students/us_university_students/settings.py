# -*- coding: utf-8 -*-

# Scrapy settings for us_university_students project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'us_university_students'

SPIDER_MODULES = ['us_university_students.spiders']
NEWSPIDER_MODULE = 'us_university_students.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'us_university_students (+http://www.yourdomain.com)'


DOWNLOADER_MIDDLEWARES = {
	    'scrapy.contrib.downloadermiddleware.useragent.UserAgentMiddleware' : None,
        'us_university_students.random_user_agent.RotateUserAgentMiddleware': 400,
        'scrapy.contrib.downloadermiddleware.retry.RetryMiddleware': 90,
         #'scrapy.contrib.downloadermiddleware.stats.DownloaderStats': 850,
        #if you got proxies from proxies from proxymesh.com uncomment the below two lines
        'scrapy.contrib.downloadermiddleware.httpproxy.HttpProxyMiddleware': 110,
        'us_university_students.middlewares.ProxyMiddleware':100,

}

PROXIES = [
       {'ip_port': 'open.proxymesh.com:31280', 'user_pass':None}, #Get username and password frin proxymesh.com and replace with username and password and ofcourse one can change ip_port and even can add more. middlewares.py is related to this section.
       #based on the configuration in proxymesh you are supposed to uncoment these two lines.
       #{'ip_port': 'us.proxymesh.com:31280', 'user_pass':None},
       #{'ip_port': 'uk.proxymesh.com:31280', 'user_pass':None},
       ]

#ITEM_PIPELINES = {'realtor_com.pipelines.CSVPipeline': 300 }

RETRY_TIMES = 5
# Retry on most error codes since proxies fail for different reasons
RETRY_HTTP_CODES = [500,401, 503, 504, 400, 403, 404, 408,307,407]
PROXY_LIST = 'proxy_list.txt'

