# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import re
import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, TakeFirst, Join

from job_message.utils.item_parser import create_md5

class JobItemLoader(ItemLoader):
    default_output_processor = TakeFirst()

class TestItem(scrapy.Item):
    postion = scrapy.Field()

class JobMessageItem(scrapy.Item):
    # define the fields for your item here like:
    postion = scrapy.Field(input_processor=MapCompose())  # sting
    company_location = scrapy.Field()  # sting
    money = scrapy.Field()  # string
    experience = scrapy.Field()  # sting
    education = scrapy.Field()  # sting
    tag = scrapy.Field()  # string
    company = scrapy.Field()  # sting
    business = scrapy.Field()  # 业务 sting
    scaley = scrapy.Field()  # 规模 sting
    financing = scrapy.Field()  # 融资 string
    advantage = scrapy.Field()  # 优势 string
    public_time = scrapy.Field()  # 发布时间 string
    crawl_time = scrapy.Field()  #  string
    postion_url = scrapy.Field()  # 详情页 string
    company_url = scrapy.Field() #  sting
    update_num = scrapy.Field() # int
    md5_postion_url = scrapy.Field


    def get_insert_sql(self):
        raise BaseException;'Need it'

class LaGouItem(JobMessageItem):
    #搜索页
    hr_name = scrapy.Field()  # string
    #详情页
    newbie = scrapy.Field() #职位特色 text
    postion_describe = scrapy.Field() # text include Project description, job responsibilities, job requirements
    worker_location = scrapy.Field() # string
    hr_talk = scrapy.Field() # sting
    hr_activity = scrapy.Field() # sting

    def get_insert_sql(self):
        pass

class BossItem(JobMessageItem):
    # 详情页
    hr_name = scrapy.Field()  # string
    postion_describe = scrapy.Field()  # text include Project description, job responsibilities, job requirements
    worker_location = scrapy.Field()  # string
    company_describe = scrapy.Field()  # text

    def get_insert_sql(self):
        insert_sql = """insert into boss_name(postion, company_location, money, experience, education, tag, company, business,
            scaley, financing, advantage, public_time, crawl_time, postion_url, company_url,
            update_num, hr_name, md5_postion_url, postion_describe, worker_location, company_describe) value(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) on duplicate key update postion_describe=VALUES(postion_describe),
            company_describe=VALUES(company_describe), update_num=VALUES(update_num);"""

        postion_des = re.sub("\"|'", '', self.get('postion_describe', ''))
        company_des = re.sub("\"|'", '', self.get('company_describe', ''))
        md5_p_u = create_md5(self.get('postion_url',''))
        params = (self['postion'], self.get('company_location',''), self.get('money',''), self.get('experience',''),
                  self.get('education',''), self.get('tag',''), self.get('company', ''), self.get('business', ''),
                  self.get('scaley', ''), self.get('financing', ''), self.get('advantage',''), self.get('public_time'),
                  self.get('crawl_time', ''), self.get('postion_url', ''), self.get('company_url', ''), self.get('update_num',0),
                  self.get('hr_name',''), md5_p_u,  postion_des, self.get('worker_location', ''), company_des
                  )

        return insert_sql, params