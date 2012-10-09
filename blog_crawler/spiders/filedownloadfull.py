#!/usr/bin/env python
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from blog_crawler.items import BlogCrawlerItem
from scrapy.exceptions import DropItem
import re

#Do not execute the callback function for the following urls
path_deny_base = (
 '/about',
 '/our-downloads/[a-zA-Z0-9_/]*$',
 '/porn/[a-zA-Z0-9_/]*$',
 '/category/games/[a-zA-Z0-9_/]*$',
 '/category/movies/[a-zA-Z0-9_/]*$',
 '/category/magazine/[a-zA-Z0-9_/]*$',
 '/category/music/[a-zA-Z0-9_/]*$',
 '/category/tv-shows/[a-zA-Z0-9_/]*$',
 '/category/uncategorized/[a-zA-Z0-9_/]*$',
 '/category/applications/[a-zA-Z0-9_/]*$'
)

#Allowed filehosts to save
allowed_file_host = 'rapidgator|rapidshare|ultramegabit|uploaded|netload|depositfiles|bitshare|extabit|letitbit|mediafire'

class BlogSpider(CrawlSpider):
    name = "filedownloadfull"
    allowed_domains = ["filedownloadfull.com"]
    start_urls = [
        "http://www.filedownloadfull.com/category/applications/"
    ]
    rules = [
        Rule(SgmlLinkExtractor(allow=(),deny=path_deny_base), follow=True,callback='parse_item')
        ]

    def parse_item(self, response):
        hxs = HtmlXPathSelector(response)
        item = BlogCrawlerItem()
        item['url'] = response.url
        item['title'] = hxs.select(".//title").extract()[0].replace(u'<title>',u'').split(u'|')[0].strip()
        #Lines to eval javascript fromCharCode
        temp = hxs.select(".//*[@id='content']/div[1]").re('fromCharCode(.*?);')
        s = str(temp)
        num = s[4:-4]
        num = num.split(',')
        array_num = [int(x) for x in num]
        unobs_code = str(''.join(map(unichr, array_num)))
        #eval javascript done
        links = re.findall('<a .*href="(.*?)" target="_blank">',unobs_code)
        final_links = []
        for link in links:
            if re.search(allowed_file_host,link):
                final_links.append(link)
        item['link'] = final_links
        if not item['link']:
            item['title'] = ''
            item['url'] = ''
        return item
    