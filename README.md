blog-crawler
============

Basic crawler written in python using scrapy framework

To run the crawler you need to install the following on your system :
Scrapy 0.14 and its dependencies

To start the crawler and type the following command :

scrapy crawl weknowfuture -o items.json -t json

or

scrapy crawl filedownloadfull -o items.json -t json

The scraped data ( download links of shared files from the blogs ) will be stored in items.json .
Have fun and use it at your own risk !


