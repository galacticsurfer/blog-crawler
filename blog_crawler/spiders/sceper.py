#!/usr/bin/env python
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from blog_crawler.items import BlogCrawlerItem
import re

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
 '/category/e-books/[a-zA-Z0-9_/]*$'
 '/category/sr-pack/[a-zA-Z0-9_/]*$'
 '/category/staff-recommended/[a-zA-Z0-9_/]*$'
)

allowed_file_host = 'rapidgator|rapidshare|ultramegabit|uploaded|netload|depositfiles|bitshare|extabit|letitbit|mediafire|lumfile'


class BlogSpider(CrawlSpider):
    name = "sceper"
    allowed_domains = ["sceper.com"]
    start_urls = [
        "http://www.http://sceper.eu/"
    ]
    rules = [
        Rule(SgmlLinkExtractor(allow=(),deny=path_deny_base), follow=True,callback='parse_item')
        ]

    def parse_item(self, response):
        hxs = HtmlXPathSelector(response)
        item = BlogCrawlerItem()
        item['title'] = str(hxs.select(".//title").extract()[0]).replace('<title>','').split('|')[0].strip()
        temp = hxs.select(".//*[@id='content']/div[1]").re('fromCharCode(.*?);')
        s = str(temp)
        num = s[4:-4]
        num = num.split(',')
        array_num = [int(x) for x in num]
        unobs_code = str(''.join(map(unichr, array_num)))
        links = re.findall('<a .*href="(.*?)" target="_blank">',unobs_code)
        final_links = []
        for link in links:
            if re.search(allowed_file_host,link):
                final_links.append(link)
        item['link'] = final_links
        if not item['link']:
            item['title'] = ''
        return item
    