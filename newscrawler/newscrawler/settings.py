# -*- coding: utf-8 -*-

# Scrapy settings for newscrawler project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'newscrawler'

SPIDER_MODULES = ['newscrawler.spiders']
NEWSPIDER_MODULE = 'newscrawler.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'newscrawler (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

ITEM_PIPELINES = {
    'newscrawler.pipelines.NewscrawlerPipeline': 300
}

#MONGODB
MONGODB_SERVER = '127.0.0.1'
MONGODB_PORT = 27017
MONGODB_DB = 'test'
MONGODB_COLLECTION = 'lives'

#CRAWL Domains & STARTS_URL
#金色财经
# 只看重要的https://api.jinse.com/v4/live/list?limit=20&reading=false&id=0&flag=down&grade=4,5
# 全部https://api.jinse.com/v4/live/list?limit=20&reading=false&id=0&flag=down&sort=0
# 精选https://api.jinse.com/v4/live/list?limit=20&reading=false&id=0&flag=down&sort=1
# 政策https://api.jinse.com/v4/live/list?limit=20&reading=false&id=0&flag=down&sort=2
# 人物https://api.jinse.com/v4/live/list?limit=20&reading=false&id=0&flag=down&sort=3
# 行情https://api.jinse.com/v4/live/list?limit=20&reading=false&id=0&flag=down&sort=4
# 公告https://api.jinse.com/v4/live/list?limit=20&reading=false&id=0&flag=down&sort=5
# 声音https://api.jinse.com/v4/live/list?limit=20&reading=false&id=0&flag=down&sort=6
# 分析https://api.jinse.com/v4/live/list?limit=20&reading=false&id=0&flag=down&sort=7
# 动态https://api.jinse.com/v4/live/list?limit=20&reading=false&id=0&flag=down&sort=8
# 突发https://api.jinse.com/v4/live/list?limit=20&reading=false&id=0&flag=down&sort=9
ALLOWED_DOMAINS_1 = ['www.jinse.com']
# fifter只看重要的
START_URLS_1 = ['https://api.jinse.com/v4/live/list?limit=3&reading=false&flag=down&grade=4,5']

#火球财经
ALLOWED_DOMAINS_2 = ['www.huoqiucj.com']
# fifter只看重要的
START_URLS_2 = ['http://huoqiucj.com/Home/newsflash']

#币世界
ALLOWED_DOMAINS_3 = ['www.bishijie.com']
# fifter只看重要的
START_URLS_3 = ['https://www.bishijie.com/kuaixun']

#WP_REST_API_POST_SETTING
#Normal Account
WP_API_ID = 'xxxx'
WP_API_PW = 'xxxx'
#Administrator Account
# WP_API_ID = 'xxxxx'
# WP_API_PW = 'xxxxx'

END_POINT_URL = 'http://www.newsbtc.work/wp-json/wp/v2/posts'


# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'newscrawler.middlewares.NewscrawlerSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'newscrawler.middlewares.NewscrawlerDownloaderMiddleware': 543,
#}

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
#ITEM_PIPELINES = {
#    'newscrawler.pipelines.NewscrawlerPipeline': 300,
#}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
