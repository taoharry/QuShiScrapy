# -*- coding: utf-8 -*-
import time
import scrapy
from selenium import webdriver
from scrapy.signalmanager import dispatcher
from scrapy import signals
from selenium.webdriver.common.by import By
# WebDriverWait 库，负责循环等待
from selenium.webdriver.support.ui import WebDriverWait
# expected_conditions 类，负责条件出发
from selenium.webdriver.support import expected_conditions as EC

from job_message.items import JobItemLoader, LaGouItem
from job_message.settings import CHROME_PATH
from job_message.utils.item_parser import time_now

class LagouSpider(scrapy.Spider):
    name = 'lagou'
    allowed_domains = ['lagou.com']
    start_urls = ['https://www.lagou.com/jobs/list_python%E5%AE%89%E5%85%A8?px=new&yx=15k-25k&gx=%E5%85%A8%E8%81%8C&city=%E5%85%A8%E5%9B%BD#order']
    NEEDJS = 'brower'

    headers = {
        "HOST" : "www.lagou.com",
        "Refere" : "https://www.lagou.com",
    }

    def __init__(self):
        self.logger.info('Lagou webdrive start')
        super(LagouSpider, self).__init__()
        chrome_opt = webdriver.ChromeOptions()
        pref = {"profile.managed_default_content_settings.images":2}
        chrome_opt.add_experimental_option("prefs", pref)
        self.browser = webdriver.Chrome(executable_path=CHROME_PATH,  chrome_options=chrome_opt)
        dispatcher.connect(self.spider_close, signals.spider_closed)

    def spider_close(self, spider):
        self.logger.info('Lagou webdrive closed')
        self.browser.quit()

    def start_requests(self):
        self.logger.info("Lagou crawl start")
        yield scrapy.Request(self.start_urls[0],  callback=self.next_page)


    def next_page(self, response):
        page_list = response.xpath('//span[@class="span totalNum"]/text()').extract()
        if page_list:
            page = int(page_list[0])
        else:
            return
        for i in range(page):
            self.page_parse(response)
            self.browser.find_element_by_xpath("//div[@id='s_position_list']//span[@action='next']").click()
            try:
                WebDriverWait(self.browser, 10).until(EC.presence_of_element_located((By.XPATH, '//span[@class="format-time"]')))
            except:
                self.logger.error('Lagou can not find next page')


        # self.headers['Content-Type'] = 'application/json;charset=UTF-8'
        # page_list = response.xpath('//span[@class="span totalNum"]/text()[]').extract()
        # if page_list:
        #     page = int(page_list[0])
        # else:
        #     self.logger.error("Can't find total num")
        #     return
        # page_data = {"first": False, "pn": 1, "kd": "python爬虫"}
        # # debug start
        # page_data = 'first=true&pn=1&kd=python%E7%88%AC%E8%99%AB$sid=b317970d39ed45cea3d29a1f339d170a'
        # yield scrapy.Request(self.page_url, method="POST", headers=self.headers, body=page_data, callback=self.page_parse)
        # #debug end

        # for i in range(1, page+1):
        #     if i == 1:
        #         page_data['first'] = True
        #     else:
        #         page_data['pn'] = i
        #     yield scrapy.Request(self.page_url, method="POST", headers=self.headers, body=page_data, callback=self.parse)

    def page_parse(self, response):
        ul = response.xpath('//*[@id="s_position_list"]/ul/li[1]')[0]
        lis = ul.xpath('//li[@data-index]')
        for i,li in enumerate(lis):
            self.logger.debug('Lagou crawl li num:{}'.format(i))
            item_loader = JobItemLoader(item=LaGouItem(), response=li)
            item_loader.add_xpath('postion', 'div//h3/text()')
            postion_url = li.xpath('div//a[@class="position_link"]/@href').extract()[0]
            item_loader.add_xpath('postion_url','div//a[@class="position_link"]/@href')
            item_loader.add_xpath('company_location', 'div//em/text()')
            item_loader.add_xpath('money', 'div//span[@class="money"]')
            item_loader.add_xpath('experience', 'div//div[@class="p_bot"]/div/text()').re('经验([0-9-]{3})年')
            item_loader.add_xpath('education', 'div//div[@class="p_bot"]/div/text()').re('/ (\w+?)\n')
            tag = '-'.join(li.xpath('div[@class="list_item_bot"]/div[@class="li_b_l"]/span/text()').extract())
            item_loader.add_xpath('tag', tag)
            item_loader.add_xpath('company', 'div//div[@class="company_name"]/a/text()')
            business, scale, financing = li.xpath('div//div[@class="industry"]/text()').extract()[0].split('/')
            item_loader.add_xpath('scale', scale)
            item_loader.add_xpath('business', business)
            item_loader.add_xpath('financing', financing)
            item_loader.add_xpath('advantage', 'div[@class="list_item_bot"]/div[@class="li_b_r"]/text()')
            item_loader.add_xpath('public_time', 'div//span[@class="format-time"]/text()')
            item_loader.add_xpath('crawl_time', time_now())
            item_loader.add_xpath('update_num', 0)
            item_loader.add_xpath('company_url', 'div//div[@class="company_name"]/a/@href')
            yield scrapy.Request(postion_url, headers=self.headers, meta={"lagou_item": item_loader}, callback=self.parse)

    def parse(self, response):
        print(response.text)
        pass
