import random

class IpProxyMid(object):

    def __init__(self, crawler):
        """
        RANDOM_PROXY = {"127.0.0.1":{"creds":"","other":""}, "192.168.0.1":{"creds":"","other":""}}
        """
        super(IpProxyMid, self).__init__()
        self.ip_proxys = crawler.settings.get('RANDOM_PROXY', {})

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)

    def get_proxy_ip_sql(self):
        pass

    def process_request(self, request, spider):
        if self.ip_proxys:
            ip_proxy = random.sample(self.ip_proxys, 1)
            creds = ip_proxy.get('CRED','')
            request.meta['proxy'] = ip_proxy.keys()[0]
            if creds:
                request.headers['Proxy-Authorization'] = b'Basic ' + creds
        else:
            return