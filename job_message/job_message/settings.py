# -*- coding: utf-8 -*-

# Scrapy settings for job_message project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

import os
import sys
import random

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, PROJECT_DIR)

BOT_NAME = 'job_message'
LOG_LEVEL = 'INFO'
#LOG_FILE = os.path.join(BASE_DIR,'logs/text.log')
SPIDER_MODULES = ['job_message.spiders']
NEWSPIDER_MODULE = 'job_message.spiders'
CHROME_PATH='E:\pachong\scripy_venv\chromedriver.exe'
# Scrapy setting user-agent
#USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)"

# My useraget default is random
#RANDOM_UA_TYPE=random

# My ip pooldefault is dicr
#RANDOM_PROXY = {"127.0.0.1":{"creds":"","other":""}, "192.168.0.1":{"creds":"","other":""}}

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'job_message (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 4

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
CONCURRENT_REQUESTS_PER_IP = random.randint(1,3)

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middle
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
SPIDER_MIDDLEWARES = {
   'job_message.middle.JobMessageSpiderMiddleware': None,
   'job_message.middle.spider_mid.SpiderMid' : None,
}

# Enable or disable downloader middle
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
   'job_message.middlewares.JobMessageDownloaderMiddleware' : None,
   'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware' : None,
   'job_message.middle.user_agent.UserAgentMid' : 543,
   'job_message.middlewares.JsMiddleware' : 999,
}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
EXTENSIONS = {
   'scrapy.extensions.telnet.TelnetConsole': None,
   'job_message.middle.spider_stats.SpiderStatsMid' : 543,
}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   'job_message.pipelines.MysqlPoolInsertPipeline': 300,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
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
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

# MySQL
MYSQL_HOST = "127.0.0.1"
MYSQL_DBNAME = 'job_message'
MYSQL_USER = 'root'
MYSQL_PASSWORD = 'root'