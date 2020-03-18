from selenium import webdriver
from scrapy.selector import Selector

#配置
chrome_opt = webdriver.ChromeOptions()
#不加载图片
pref = {"profile.managed_default_content_settings.images":2}
chrome_opt.add_experimental_option("prefs", pref)
brower = webdriver.Chrome(executable_path='E:\pachong\scripy_venv\chromedriver.exe', chrome_options=chrome_opt)

brower.get('https://www.lagou.com/jobs/list_python%E5%AE%89%E5%85%A8?labelWords=&fromSearch=true&suginput=')

page = brower.page_source

t_select = Selector(text=page)

t_select.xpath()