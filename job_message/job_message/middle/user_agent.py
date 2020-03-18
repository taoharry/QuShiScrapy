from fake_useragent import UserAgent
from scrapy.crawler import logger

class UserAgentMid(object):

    def __init__(self, crawler):
        super(UserAgentMid, self).__init__()
        self.ua = UserAgent()
        self.ua_setting = crawler.settings.get('RANDOM_UA_TYPE', 'random')


    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)


    def process_request(self, request, spider):
        def get_setting_ua():
            return getattr(self.ua, self.ua_setting)
        logger.debug(request.headers.get('User_Agent'))
        request.headers.setdefault('User_Agent', get_setting_ua())