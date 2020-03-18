# -*- coding: utf-8 -*-
import time
import random
import scrapy
from selenium import webdriver
from scrapy.signalmanager import dispatcher
from scrapy import signals, Selector
from selenium.webdriver.common.by import By
# WebDriverWait 库，负责循环等待
from selenium.webdriver.support.ui import WebDriverWait
# expected_conditions 类，负责条件出发
from selenium.webdriver.support import expected_conditions as EC

from job_message.items import JobItemLoader, BossItem, TestItem
from job_message.settings import CHROME_PATH
from job_message.utils.item_parser import time_now, get_string




class BossSpider(scrapy.Spider):
    name = 'boss'
    allowed_domains = ['https://www.zhipin.com']
    start_urls = ['https://www.zhipin.com/c101010100/y_6/?query=python%E7%88%AC%E8%99%AB%E5%B7%A5%E7%A8%8B%E5%B8%88&page={page}&ka=page-{page}']
    NEEDJS = 'brower'
    headers = {
        "HOST": "www.zhipin.com",
        "Refere": "https://www.zhipin.com",
    }

    def __init__(self, *args, **kwargs):
        self.logger.info('Boss webdrive start')
        super(BossSpider, self).__init__()
        chrome_opt = webdriver.ChromeOptions()
        pref = {"profile.managed_default_content_settings.images":2}
        chrome_opt.add_experimental_option("prefs", pref)
        self.browser = webdriver.Chrome(executable_path=CHROME_PATH,  chrome_options=chrome_opt)
        dispatcher.connect(self.spider_close, signals.spider_closed)


    def spider_close(self, spider):
        self.logger.info('Boss webdrive closed')
        self.browser.quit()

    def start_requests(self):
        self.logger.info("Boss crawl start")
        start_url = self.start_urls[0]
        self.logger.debug('just for test')
        # start_url = start_url.format(page=1)
        # yield scrapy.Request(start_url, callback=self.parse)
        for i in range(1,11):
            self.logger.info('Boss page:{}'.format(i))
            url = start_url.format(page=i)
            self.logger.info('start url :{}'.format(url))
            yield scrapy.Request(url,  callback=self.parse)


    def parse(self, response):
        lis = response.xpath('//div[@class="job-list"]/ul/li')
        for i, li in enumerate(lis):
            self.logger.debug('Boss crawl li num:{}'.format(i))
            item_loader = JobItemLoader(item=BossItem(), selector=li)
            item_loader.add_xpath('postion', 'div//span[@class="job-name"]/text()')
            tmp_postion_url = li.xpath('div//a[@class="primary-box"]/@href').extract()
            if not tmp_postion_url:
                self.logger.error('Can not get the {} postion url '.format(tmp_postion_url))
                continue
            postion_url = self.allowed_domains[0] + tmp_postion_url[0]
            item_loader.add_value('postion_url', postion_url)
            item_loader.add_xpath('company_location', 'div//div[@class="company-text"]/h3/a/text()')
            item_loader.add_xpath('money', 'div//span[@class="red"]/text()')
            item_loader.add_xpath('experience', 'div//div[@class="job-limit clearfix"]/p', re = '\w+?月|\d+\-\d+年|应届生|在校生|\d+年以内|\d年以上|不限')
            item_loader.add_xpath('education', 'div//div[@class="job-limit clearfix"]/p', re = '不限|专科|本科|研究生|博士')
            tag = '-'.join(li.xpath('div//span[@class="tag-item"]/text()').extract())
            item_loader.add_value('tag', tag)
            item_loader.add_xpath('company', 'div//div[@class="company-text"]/h3/a/text()')
            try:
                business, scale, financing = li.xpath('div//div[@class="company-text"]/p/text()').extract()
            except:
                business, financing = li.xpath('div//div[@class="company-text"]/p/text()').extract()
                scale = ''
            item_loader.add_value('scaley', scale)
            item_loader.add_value('business', business)
            item_loader.add_value('financing', financing)
            item_loader.add_xpath('advantage', 'div//div[@class="info-desc"]/text()')
            item_loader.add_value('public_time', time_now())
            item_loader.add_value('crawl_time', time_now())
            item_loader.add_value('update_num', 0)
            # company_url = self.allowed_domains + li.xpath('div//div[@class="company-text"]/h3/a/@href').extract()[0]
            item_loader.add_xpath('company_url', 'div//div[@class="company-text"]/h3/a/@href')
            time.sleep(random.random())
            self.browser.get(postion_url)
            postion_page = Selector(text=self.browser.page_source)
            # hr_name = postion_page.xpath('//div[@class="job-box"]//div[@class="detail-op"]/h2[@class="h2"]/text').extract()[0]
            # postion_describe = "".join(postion_page.xpath('//div[@class="detail-content"]//text()').extract()).strip()
            # worker_location = postion_page.xpath('//div[@class="location-address"]/text()').extract()[0]
            # company_describe = "".join(postion_page.xpath('//*[@class="job-sec company-info"]//text()').extract()).strip()

            item_loader.add_value('hr_name', get_string(postion_page, '//div[@class="detail-op"]/h2[@class="name"]/text()'))
            item_loader.add_value('postion_describe',  get_string(postion_page, '//div[@class="job-sec"]/div[@class="text"]//text()', join=True))
            item_loader.add_value('worker_location',  get_string(postion_page, '//div[@class="location-address"]/text()'))
            item_loader.add_value('company_describe',  get_string(postion_page, '//*[@class="job-sec company-info"]//text()', join=True))
            self.logger.debug('Boss crawl li num:{}'.format(i))
            yield item_loader.load_item()



