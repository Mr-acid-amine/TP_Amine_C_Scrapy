# Scrapy settings for scrapy_kbo_tp project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = "scrapy_kbo_tp"

SPIDER_MODULES = ["scrapy_kbo_tp.spiders"]
NEWSPIDER_MODULE = "scrapy_kbo_tp.spiders"


ROBOTSTXT_OBEY = False


TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"


ITEM_PIPELINES = {
    'scrapy_kbo_tp.pipelines.MongoPipeline': 300,
}
