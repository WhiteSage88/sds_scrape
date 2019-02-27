#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 18 16:01:20 2017

@author: jonathan

This script takes a CSV file and extracts all CAS numbers and Manufacturers.
Then a SDS lookup will be performed based on the manufacturer chosen.

The CSV file must be in the column format of 
Room, CHEM-NAME, CAS, Manufacturer
"""
from __future__ import print_function


import scrapy

from selenium import webdriver

import logging
from shutil import copyfile
from twisted.internet import reactor, defer

import csv  
import glob
import sys

from scrapy.spiders import Spider
import time
import os

from scrapy.http import Request
from selenium.webdriver.chrome.options import Options



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
        profile = {"download.default_directory": buffer_path,
           "download.prompt_for_download": False,
           "plugins.plugins_list": [{"enabled":False,"name":"Chrome PDF Viewer"}]}
        chrome_profile.add_experimental_option("prefs", profile)
        
        driver = self.webdriver.Chrome(chrome_options=chrome_profile,
                                       executable_path='/home/jonathan/Desktop/Chemical-Labeling-master/sds/chromedriver')
        
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
            time.sleep(1)
            try:
                change_pdf_names(self.name, self.cas, self.buffer_path, self.sds_path,\
                                 self.manufacturer)      
                print ('Downloaded {}'.format(self.name) , datetime.now())
            except:
                print ('Error in pdf movement. Failed to find {} {}.'.format \
                       (self.name, self.manufacturer))      
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
        
        chrome_profile = webdriver.ChromeOptions()
        profile = {"download.default_directory": buffer_path,
           "download.prompt_for_download": False,
           "plugins.plugins_list": [{"enabled":False,"name":"Chrome PDF Viewer"}]}
        chrome_profile.add_experimental_option("prefs", profile)
        
        driver = self.webdriver.Chrome(chrome_options=chrome_profile,
                                       executable_path='/home/jonathan/Desktop/Chemical-Labeling-master/sds/chromedriver')
        
        
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
            try:
                change_pdf_names(self.name, self.cas, self.buffer_path, self.sds_path,\
                                 self.manufacturer)      
                print ('Downloaded {}'.format(self.name) , datetime.now())
            except:
                print ('Error in pdf movement. Failed to find {} {}.'.format \
                       (self.name, self.manufacturer))      
        driver.quit()
    
class AlfaSpider(Spider):                                                                       
    name = "alfa"
    start_urls = "https://www.alfa.com/en/"
    custom_settings = {
            'COOKIES_ENABLED': True,
            } 
       
    def __init__(self, name=None, driver = None, cas = None,\
                 buffer_path = None, sds_path = None, manufacturer= None,\
                 *args, **kwargs):     
        super(AlfaSpider, self).__init__(*args, **kwargs)
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
        profile = {"download.default_directory": buffer_path,
           "download.prompt_for_download": False,
           "plugins.plugins_list": [{"enabled":False,"name":"Chrome PDF Viewer"}]}
        chrome_profile.add_experimental_option("prefs", profile)
        #chrome_profile.add_experimental_option("excludeSwitches",["ignore-certificate-errors"])
        #chrome_profile.add_argument('--disable-gpu')
        #chrome_profile.add_argument('--headless')
        
        driver = self.webdriver.Chrome(chrome_options=chrome_profile,
                                       executable_path='/home/jonathan/Desktop/Chemical-Labeling-master/sds/chromedriver')
        
        
        driver.get(self.start_urls)
        time.sleep(1)
        textinput= driver.find_element_by_id('id_q')
        textinput.send_keys(self.cas)
        time.sleep(1)
        
        button = driver.find_element_by_id("search_products")
        button.click()
        time.sleep(1)
        sds_button =  driver.find_element_by_partial_link_text('SDS')
        try:
            
            sds_button.click()
            time.sleep(10)
        except:
            print ("COULD NOT FIND {}".format(self.name))
            
        else:
            print("IN ELSE")                     
            #sds_button = driver.find_element_by_xpath("//a[contains(concat(' ', @href, ' '), ' sds ')")
            
            
            sds_link = driver.find_element_by_partial_link_text('English')
            sds_link.click()
            driver.get(driver.current_url)
            time.sleep(1)
           
            try:
                change_pdf_names(self.name, self.cas, self.buffer_path, self.sds_path,\
                                 self.manufacturer)      
                print ('Downloaded {}'.format(self.name) , datetime.now())
            except:
                print ('Error in pdf movement. Failed to find {} {}.'.format \
                       (self.name, self.manufacturer))
        driver.quit()    
        
class CarolSpider(Spider):                                                                       
    name = "carol"
    start_urls = "https://www.carolina.com/"
    custom_settings = {
            'COOKIES_ENABLED': True,
            } 
       
    def __init__(self, name=None, driver = None, cas = None,\
                 buffer_path = None, sds_path = None, manufacturer= None,\
                 *args, **kwargs):     
        super(CarolSpider, self).__init__(*args, **kwargs)
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
        profile = {"download.default_directory": buffer_path,
           "download.prompt_for_download": False,
           "plugins.plugins_list": [{"enabled":False,"name":"Chrome PDF Viewer"}]}
        chrome_profile.add_experimental_option("prefs", profile)
        #chrome_profile.add_experimental_option("excludeSwitches",["ignore-certificate-errors"])
        #chrome_profile.add_argument('--disable-gpu')
        #chrome_profile.add_argument('--headless')
        
        driver = self.webdriver.Chrome(chrome_options=chrome_profile,
                                       executable_path='/home/jonathan/Desktop/Chemical-Labeling-master/sds/chromedriver')      
        
        driver.get(self.start_urls)
        time.sleep(1)
        textinput= driver.find_element_by_id('Ntt')
        textinput.send_keys(self.name)
        time.sleep(1)
        button = driver.find_element_by_id('search-submit')
        button.click()
        time.sleep(1)
        
        try:
            button = driver.find_element_by_xpath("//*[@id='content']/ul[2]/li[1]/a[1]/span")
        except:
            print ("COULD NOT FIND {}".format(self.name))
            
        else:
            button.click()
            time.sleep(5)
            sds = driver.find_element_by_xpath('//a[@href="#resources"]')
            sds.click()
            time.sleep(1)
            sds_link = driver.find_element_by_xpath('//*[@id="family-item-resources"]/div[2]/ul/li[1]/a')
            driver.get(sds_link.get_attribute("href"))
            time.sleep(1)
            sds_link = driver.find_element_by_xpath('//*[@id="content"]/p[2]/strong/a')
            driver.get(sds_link.get_attribute("href"))
            time.sleep(1)
            try:
                change_pdf_names(self.name, self.cas, self.buffer_path, self.sds_path,\
                                 self.manufacturer)      
                print ('Downloaded {}'.format(self.name) , datetime.now())
            except:
                print ('Error in pdf movement. Failed to find {} {}.'.format \
                       (self.name, self.manufacturer))    
        driver.quit()    
###IMPORTANT 
#These three variables have to be set to where you would like 
#to retrieve the information from (filename). 

filename = '/home/jonathan/Desktop/Chemical-Labeling-master/sds/parse_test.csv'
""" Buffer path is the folder where the SDS sheets will go temporarily.
The SDS path is the path where the final location of the PDF will reside.
This is usually sdsDatabase/{room}
"""
buffer_path = '/home/jonathan/Desktop/Chemical-Labeling-master/sds/TestPDF/buffer/'
sds_path = '/home/jonathan/Desktop/Chemical-Labeling-master/sds/TestPDF/'

"""Because the file is downloaded as PrintMSDSAction.pdf from the website,
this function will take the chemical name (final_name), cas number, and 
rename that file with its new filename.
"""
def change_pdf_names(final_name, cas, buffer_path, sds_path, manu):
    first_file = glob.glob(buffer_path+'*')[0]
    final_path = sds_path+'{}/'.format('final_buffer')
    #os.rename changes from old path to new path
    #The result is in the format sds_path/buffer/name_cas
    os.rename(first_file,final_path+final_name+'_'+cas+\
              '_'+manu)
    for filename in glob.glob(buffer_path+'*'):
        os.remove(filename)
    


from scrapy.crawler import CrawlerRunner
from datetime import datetime
time_now = datetime.now()
'''
old_stdout = sys.stdout
log_file = open("{}.log".format(datetime.now()), 'w')
sys.stdout = log_file
'''
runner = CrawlerRunner()

#reads CSV file and compiles a list of cas numbers in third column 
#and crawls for them
#Returns a value of (name,cas,manufacturer)
def csv_reading(filename, buffer_path):
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        chemicals = []
        for row in reader:
            #builds CAS list for crawler
            ##Following function only works if CAS exists (row[2])
            if row[2]:
                #checks if pdf already exists
                if not glob.glob(sds_path+'final_buffer/'+'*_{}_{}'.format(row[2],row[3])):
                    #checks if cas in chemical list
                    if not (row[1],row[2], row[3]) in chemicals:
                        chemicals.append((row[1],row[2],row[3]))
            #Runs only if CAS does NOT exists and searches by name
            #This will make a file of NAME_NAME_MANU....
            elif row[1]:
                if not glob.glob(sds_path+'final_buffer/'+'*_{}_{}'.format(row[1],row[3])):
                    #checks if ONLY NAME in chemical list
                    if not (row[1],row[1], row[3]) in chemicals:
                        chemicals.append((row[1],row[1],row[3]))
        return chemicals


chemicals = csv_reading(filename, buffer_path)
from pprint import pprint
from scrapy.utils.log import configure_logging
configure_logging()
#logging.getLogger('scrapy').setLevel(logging.WARNING)
#logging.getLogger('selenium').setLevel(logging.WARNING)
#logging.basicConfig(filename='LOG_{}.txt'.format(time_now))

@defer.inlineCallbacks
def crawl(chemicals, CASspider, FisherSpider,AlfaSpider,CarolSpider,buffer_path, sds_path):
    for chemical in chemicals[:]:
        #checks for manufacturer
        if chemical[2] in ('FISHER SCIENTIFIC','Thermo'):
            yield runner.crawl(FisherSpider, cas=chemical[1], name=chemical[0], \
                         driver=webdriver, buffer_path = buffer_path,\
                         sds_path = sds_path, manufacturer=chemical[2])
        elif chemical[2] in ('SIGMA','ALDRICH'):
            yield runner.crawl(CASSpider, cas=chemical[1], name=chemical[0], \
                         driver=webdriver, buffer_path = buffer_path,\
                         sds_path = sds_path, manufacturer=chemical[2])
        elif chemical[2] in ('ALFA','Alfa Aesar','AESAR'):
            yield runner.crawl(AlfaSpider, cas=chemical[1], name=chemical[0], \
                         driver=webdriver, buffer_path = buffer_path,\
                         sds_path = sds_path, manufacturer=chemical[2])
        elif chemical[2] in ('CAROLINA','CAROLINA BIOL'):
            yield runner.crawl(CarolSpider, cas=chemical[1], name=chemical[0], \
                         driver=webdriver, buffer_path = buffer_path,\
                         sds_path = sds_path, manufacturer=chemical[2])
        else:
            print("{}, {}, {} is not a compatible site for this spider. Please check again."\
                  .format(chemical[0],chemical[1],chemical[2]) )
        
    reactor.stop()
try:
    crawl(chemicals, CASSpider,FisherSpider, AlfaSpider, CarolSpider, buffer_path, sds_path)
except:
    sys.exit("Reactor has failed")
reactor.run()

from collections import defaultdict
#quick change of buffer path to final_buffer folder
buffer_path = sds_path + 'final_buffer/'
sds_path = '/home/jonathan/Desktop/Chemical-Labeling-master/sds/TestPDF/'
def pdf_spread(filename, buffer_path, sds_path):
    buffer_path = buffer_path
    d = defaultdict(list)
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            #makes a directory path and checks for its existence, creates it if
            #it does not exist
            directory = sds_path+ '{}'.format(row[0])
            if not os.path.exists(directory):
                print ("Folder {} does not exist, making directory now...".format(row[0]), datetime.now())
                os.makedirs(directory)
            #makes a dictionary with Room:Chemical_CAS_manufacturer list
            if not ('{}_{}_{}'.format(row[1],row[2],row[3])) in d[row[0]]:
                d[row[0]].append('{}_{}_{}'.format(row[1],row[2],row[3]))
    for room in d.keys():
        #Starts setting room paths
        room_path = sds_path+'{}/'.format(room)
        #Tries to copy file from buffer, if fails will log the failed Room/Chemical
        #for manual lookup
        for chemical in d[room]:
            try:
                copyfile(buffer_path + chemical, room_path + chemical+'.pdf')
            except:
                with open('failed_lookups.txt','w') as f:
                    print (d[room], chemical)
    
pdf_spread(filename, buffer_path, sds_path)
    

print ("Finished in.... " , datetime.now() - time_now)
#sys.stdout = old_stdout
#log_file.close()
