# coding:utf8
__author__ = "harry"

import sys
import os

from scrapy.cmdline import execute

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

#execute(["scrapy", "crawl", "lagou"])
execute(["scrapy", "crawl", "boss"])