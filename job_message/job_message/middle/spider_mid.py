import socket
import logging


logger = logging.getLogger(__name__)

class SpiderMid(object):

    def __init__(self, stats):
        self.stats = stats

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.stats)


    def process_spider_exception(self, response, exception, spider):
        if exception:
            self.stats.inc_value('exception_total')
            logger.info('Except total num:{}'.format(self.stats.get_value('exception_total')))

    def process_start_requests(self, start_requests, spider):
        for r in start_requests:
            self.stats.inc_value('request_total_url')
            logger.debug('Request total num:{}'.format(self.stats.get_value('request_total_url')))
            yield r

