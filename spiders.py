#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 28 11:06:41 2018

@author: jonathan
"""
from scrapy.spiders import Spider

from scrapy.http import Request
from selenium.webdriver.firefox.options import Options
import time
import os
from datetime import datetime
from sds_scrape import change_pdf_names
class CASSpider(Spider):                                                                       
    name = "cas2"
    start_urls = "http://www.sigmaaldrich.com/technical-service-home/product-catalog.html"
    custom_settings = {
            'COOKIES_ENABLED': True,
            } 
       
    def __init__(self, name=None, driver = None, cas = None,\
                 buffer_path = None, sds_path = None, manufacturer=None,\
                 *args, **kwargs):     
        super(CASSpider, self).__init__(*args, **kwargs)
        self.name = name
        self.webdriver = driver
        self.cas = cas
        self.buffer_path = buffer_path
        self.sds_path = sds_path
        self.manufacturer = manufacturer
        #logging.getLogger('scrapy').setLevel(logging.WARNING)
        #logging.getLogger('selenium').setLevel(logging.WARNING)
              
    def start_requests(self):
        yield Request(self.start_urls, callback=self.parse, dont_filter=True)
        
    def parse(self,response):
        
        os.environ['MOZ_HEADLESS']='1'
        
        chrome_profile = webdriver.ChromeOptions()
        profile = {"download.default_directory": self.buffer_path,
           "download.prompt_for_download": False,
           "plugins.plugins_list": [{"enabled":False,"name":"Chrome PDF Viewer"}]}
        chrome_profile.add_experimental_option("prefs", profile)
        
        driver = self.webdriver.Chrome(chrome_options=chrome_profile)
        
        driver.get(self.start_urls)
        time.sleep(1)
        textinput= driver.find_element_by_name('Query')
        textinput.send_keys(self.cas)
        time.sleep(1)
        
        button = driver.find_element_by_name("submitSearch")
        button.click()
        time.sleep(1)
        try:
            sds = driver.find_element_by_class_name("msdsBulletPoint")
        except:
            print ("COULD NOT FIND {}".format(self.name))
            
        else:
            sds.click()
            time.sleep(10)
            driver.get(driver.current_url)
            print ('Downloaded {}'.format(self.name) , datetime.now())
            change_pdf_names(self.name, self.cas, self.buffer_path, self.sds_path,\
                             self.manufacturer)      
        driver.quit()
        
class FisherSpider(Spider):                                                                       
    name = "fisher"
    start_urls = "https://www.fishersci.com/us/en/catalog/search/sdshome.html"
    custom_settings = {
            'COOKIES_ENABLED': True,
            } 
       
    def __init__(self, name=None, driver = None, cas = None,\
                 buffer_path = None, sds_path = None, manufacturer= None,\
                 *args, **kwargs):     
        super(FisherSpider, self).__init__(*args, **kwargs)
        self.name = name
        self.webdriver = driver
        self.cas = cas
        self.buffer_path = buffer_path
        self.sds_path = sds_path
        self.manufacturer = manufacturer
        #logging.getLogger('scrapy').setLevel(logging.WARNING)
        #logging.getLogger('selenium').setLevel(logging.WARNING)
              
    def start_requests(self):
        yield Request(self.start_urls, callback=self.parse, dont_filter=True)
        
    def parse(self,response):
        
        os.environ['MOZ_HEADLESS']='1'
        
        chrome_profile = self.webdriver.ChromeOptions()
        profile = {"download.default_directory": self.buffer_path,
           "download.prompt_for_download": False,
           "plugins.plugins_list": [{"enabled":False,"name":"Chrome PDF Viewer"}]}
        chrome_profile.add_experimental_option("prefs", profile)
        
        driver = self.webdriver.Chrome(chrome_options=chrome_profile)
        
        driver.get(self.start_urls)
        
        driver.get(self.start_urls)
        time.sleep(1)
        textinput= driver.find_element_by_id('qa_msdsKeyword')
        textinput.send_keys(self.cas)
        time.sleep(1)
        
        button = driver.find_element_by_id("msdsSearch")
        button.click()
        time.sleep(1)
        try:
            sds = driver.find_element_by_class_name("catalog_num_link")
        except:
            print ("COULD NOT FIND {}".format(self.name))
            
        else:
            sds.click()
            time.sleep(1)
            driver.get(driver.current_url)
            print ('Downloaded {}'.format(self.name) , datetime.now())
            change_pdf_names(self.name, self.cas, self.buffer_path, self.sds_path,\
                             self.manufacturer)      
        driver.quit()