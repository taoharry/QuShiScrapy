import socket


class SpiderStatsMid(object):

    def __init__(self, stats):
        self.stats = stats


    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.stats)

    def spider_closed(self, spider, reason):
        self.stats.set('request_total_url')
        self.stats.set_value('hostname', socket.gethostname())
        self.stats.set('exception_total')

