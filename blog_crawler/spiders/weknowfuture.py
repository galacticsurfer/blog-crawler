#!/usr/bin/env python
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from blog_crawler.items import BlogCrawlerItem

class BlogSpider(CrawlSpider):
    name = "weknowfuture"
    allowed_domains = ["weknowfuture.blogspot.in"]
    start_urls = [
        "http://weknowfuture.blogspot.in/"
    ]
    rules = (
        # Extract links matching 'item.php' and parse them with the spider's method parse_item
        Rule(SgmlLinkExtractor(allow=('\.html', )), callback='parse_item',follow=True),
    )

    def parse_item(self, response):
        hxs = HtmlXPathSelector(response)
        item = BlogCrawlerItem()
        item['title'] = hxs.select(".//*[@id='Blog1']/div[1]/div/div/div/div[1]/h3").re('>\n(.*?)\n<')
        item['link'] = hxs.select(".//*[@id='Blog1']/div[1]/div/div/div/div[1]/div/div/a").re('>(.*?)<')
        item['url'] = response.url
        return item
    