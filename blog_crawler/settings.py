# Scrapy settings for blog_crawler project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#

BOT_NAME = 'blog_crawler'
BOT_VERSION = '1.0'

SPIDER_MODULES = ['blog_crawler.spiders']
NEWSPIDER_MODULE = 'blog_crawler.spiders'
USER_AGENT = '%s/%s' % (BOT_NAME, BOT_VERSION)

